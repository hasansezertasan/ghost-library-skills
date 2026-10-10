#!/usr/bin/env python3
"""Validate native packages and exercise Codex discovery without installing them."""

from __future__ import annotations

import argparse
from contextlib import contextmanager
import json
import os
from pathlib import Path
from queue import Empty, Queue
import subprocess
import threading
import tempfile
import time


class AppServer:
    """A private stdio server; skill-root overrides last only for this process."""

    def __init__(self, cwd: Path, command: list[str] | None = None):
        self.process = subprocess.Popen(
            command or ["codex", "app-server", "--stdio"], cwd=cwd,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
            text=True, bufsize=1,
        )
        self.messages = Queue()
        self.next_id = 1
        self.notifications = []
        threading.Thread(target=self._read, daemon=True).start()

    def _read(self):
        for line in self.process.stdout:
            try:
                self.messages.put(json.loads(line))
            except ValueError:
                self.messages.put({"transport_error": "Non-JSON app-server output"})
        self.messages.put({"transport_error": "App-server closed stdout"})

    def send(self, value: dict):
        self.process.stdin.write(json.dumps(value) + "\n")
        self.process.stdin.flush()

    def receive(self, timeout: float) -> dict:
        try:
            message = self.messages.get(timeout=timeout)
        except Empty:
            raise TimeoutError("App-server response timed out") from None
        if "transport_error" in message:
            raise RuntimeError(message["transport_error"])
        return message

    def request(self, method: str, params: dict, timeout: float = 30) -> dict:
        request_id = self.next_id
        self.next_id += 1
        self.send({"id": request_id, "method": method, "params": params})
        deadline = time.monotonic() + timeout
        while True:
            message = self.receive(max(0, deadline - time.monotonic()))
            if message.get("id") == request_id:
                if "error" in message:
                    raise RuntimeError(message["error"])
                return message["result"]
            self.notifications.append(message)

    def close(self):
        self.process.terminate()
        try:
            self.process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.process.kill()
            self.process.wait()
        for stream in (self.process.stdin, self.process.stdout):
            stream.close()


@contextmanager
def app_server(cwd: Path, command: list[str] | None = None):
    server = AppServer(cwd, command)
    try:
        server.request("initialize", {
            "clientInfo": {"name": "ghost-library-skills-smoke", "version": "0.1.0"},
            "capabilities": {"experimentalApi": True},
        })
        server.send({"method": "initialized"})
        yield server
    finally:
        server.close()


def claude_validation(bundle: Path, repository: bool = False) -> dict:
    base = bundle if repository else bundle / "claude"
    targets = {
        "manifest": base if repository else base / "plugins/ghost-library-skills",
        "marketplace": base / ".claude-plugin/marketplace.json",
    }
    results = {}
    with tempfile.TemporaryDirectory(prefix='ghost-claude-validation-') as profile:
        env = dict(os.environ, CLAUDE_CONFIG_DIR=profile)
        for name, target in targets.items():
            process = subprocess.run(
                ["claude", "plugin", "validate", "--strict", "--json", str(target)],
                capture_output=True, text=True, timeout=30, env=env,
            )
            result = json.loads(process.stdout)
            if process.returncode or not result.get("success"):
                raise RuntimeError(f"Claude {name} validation failed: {result}")
            results[name] = {"valid": True, "warnings": result["manifest"]["warnings"]}
    return results


def codex_smoke(bundle: Path, workspace: Path | None = None, target: str = "contract", repository: bool = False) -> dict:
    base = bundle if repository else bundle / "codex"
    marketplace = base / ".agents/plugins/marketplace.json"
    plugin = base / "plugins/ghost-library-skills"
    with app_server(workspace or base) as server:
        detail = server.request("plugin/read", {"marketplacePath": str(marketplace), "pluginName": "ghost-library-skills"})["plugin"]
        expected = {f"ghost-library-skills:{skill.parent.name}" for skill in (plugin / "skills").glob("*/SKILL.md")}
        registered = {skill["name"] for skill in detail["skills"]}
        if not expected or registered != expected:
            raise RuntimeError(f"Codex plugin inventory differs: {registered} != {expected}")
        server.request("skills/extraRoots/set", {"extraRoots": [str(plugin / "skills")]})
        discovery = server.request("skills/list", {"cwds": [str(workspace or base)], "forceReload": True})
        found = [skill for entry in discovery["data"] for skill in entry["skills"] if Path(skill["path"]).is_relative_to(plugin)]
        if {skill["name"] for skill in found} != expected:
            raise RuntimeError("Codex skill discovery did not retain the plugin inventory")
        result = {"registered_skills": sorted(registered), "discovered_skills": sorted(skill["name"] for skill in found)}
        if workspace is not None:
            contract = (workspace / target).resolve()
            if not contract.is_relative_to(workspace) or not contract.is_dir():
                raise ValueError("Audit target must be a directory within the isolated workspace")
            thread_result = server.request("thread/start", {
                "cwd": str(workspace), "ephemeral": True, "sandbox": "read-only", "approvalPolicy": "never",
                "developerInstructions": "This is a native skill smoke test. Do not use network, MCP tools, or subagents. Do not edit files.",
            })
            thread = thread_result["thread"]
            turn = server.request("turn/start", {
                "threadId": thread["id"],
                "input": [
                    {"type": "skill", "name": "ghost-library-skills:ghost-audit", "path": str(plugin / "skills/ghost-audit/SKILL.md")},
                    {"type": "text", "text": f"Audit {contract} without editing it. Read relevant packaged resources. Return located findings and scope limits in at most 500 words."},
                ],
            })["turn"]
            deadline = time.monotonic() + 180
            commands = []
            try:
                pending = iter(server.notifications)
                while True:
                    message = next(pending, None)
                    if message is None:
                        message = server.receive(max(0, deadline - time.monotonic()))
                    if message.get("method") == "item/completed":
                        item = message["params"]["item"]
                        if item.get("type") == "commandExecution":
                            commands.append({key: item.get(key) for key in ("command", "cwd", "status", "exitCode", "aggregatedOutput")})
                    if message.get("method") == "turn/completed" and message["params"]["turn"]["id"] == turn["id"]:
                        completed = message["params"]["turn"]
                        if completed["status"] != "completed":
                            raise RuntimeError(f"Codex invocation failed: {completed.get('error')}")
                        result["invocation"] = {"status": "completed", "model": thread_result.get("model"), "completed_commands": commands,
                                                "messages": [item["text"] for item in completed["items"] if item.get("type") == "agentMessage"], "installed": False}
                        break
            except TimeoutError:
                server.request("turn/interrupt", {"threadId": thread["id"], "turnId": turn["id"]}, timeout=5)
                raise
        return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--bundle", type=Path)
    source.add_argument("--repository", type=Path, help="Validate native metadata and discovery directly from a checkout")
    parser.add_argument("--report", required=True, type=Path)
    parser.add_argument("--invoke-codex", type=Path, metavar="WORKSPACE", help="Also run one read-only model audit; uses existing CLI authentication")
    parser.add_argument("--target", default="contract", help="Audit target relative to WORKSPACE")
    args = parser.parse_args()
    report = {}
    try:
        repository = args.repository is not None
        bundle = (args.repository or args.bundle).resolve()
        report["source_kind"] = "repository" if repository else "bundle"
        report["versions"] = {
            host: subprocess.check_output([host, "--version"], text=True).strip() for host in ("claude", "codex")
        }
        report["claude"] = claude_validation(bundle, repository)
        report["codex"] = codex_smoke(bundle, args.invoke_codex.resolve() if args.invoke_codex else None, args.target, repository)
        report["success"] = True
    except (ValueError, OSError, RuntimeError, subprocess.SubprocessError, TimeoutError) as error:
        report.update(success=False, error=str(error))
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if report["success"] else 1)


if __name__ == "__main__":
    main()
