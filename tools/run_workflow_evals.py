#!/usr/bin/env python3
"""Run native Codex skill scenarios in fresh disposable workspaces."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import time

try:
    from .build_plugins import build_plugins
    from .build_skills import ROOT
    from .smoke_plugins import app_server
except ImportError:
    from build_plugins import build_plugins
    from build_skills import ROOT
    from smoke_plugins import app_server


def snapshot(workspace: Path) -> dict[str, str]:
    return {
        str(path.relative_to(workspace)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(workspace.rglob("*"))
        if path.is_file() and not path.is_symlink() and "__pycache__" not in path.parts and ".git" not in path.parts
    }


def invoke(plugin: Path, workspace: Path, skill: str, request: str, read_only: bool, timeout: int) -> dict:
    plugin = plugin.resolve()
    workspace = workspace.resolve()
    with app_server(workspace) as server:
        server.request("skills/extraRoots/set", {"extraRoots": [str(plugin / "skills")]})
        discovered = server.request("skills/list", {"cwds": [str(workspace)], "forceReload": True})
        expected_path = plugin / "skills" / skill / "SKILL.md"
        if not any(entry["path"] == str(expected_path) for group in discovered["data"] for entry in group["skills"]):
            raise RuntimeError(f"Skill not discovered: {skill}")
        thread = server.request("thread/start", {
            "cwd": str(workspace), "ephemeral": True, "approvalPolicy": "never",
            "sandbox": "read-only" if read_only else "workspace-write",
            "developerInstructions": (
                "Evaluate the selected skill using the supplied user task. Work only in this workspace and read relevant packaged skill resources. "
                "Do not inspect other evaluation workspaces or evaluator scripts. Do not use network, MCP tools, or subagents. "
                "Do not read authentication files or change host settings. Do not commit, tag, publish, install dependencies, or contact others. "
                "If a material user decision is missing, surface it in the final response; do independent work without inventing an answer."
            ),
        })["thread"]
        before = snapshot(workspace)
        turn = server.request("turn/start", {"threadId": thread["id"], "input": [
            {"type": "skill", "name": f"ghost-library-skills:{skill}", "path": str(expected_path)},
            {"type": "text", "text": request},
        ]})["turn"]
        events = list(server.notifications)
        pending = iter(events.copy())
        deadline = time.monotonic() + timeout
        while True:
            message = next(pending, None)
            if message is None:
                try:
                    message = server.receive(max(0, deadline - time.monotonic()))
                except TimeoutError:
                    server.request("turn/interrupt", {"threadId": thread["id"], "turnId": turn["id"]}, timeout=5)
                    return {"skill": skill, "status": "timed-out", "model": thread.get("model"), "events": events,
                            "before": before, "after": snapshot(workspace)}
                events.append(message)
            if "method" in message and "id" in message:
                # A non-interactive eval must not silently answer a material decision.
                server.send({"id": message["id"], "error": {"code": -32000, "message": "Non-interactive evaluation; surface the question in the final response"}})
            if message.get("method") == "turn/completed" and message["params"]["turn"]["id"] == turn["id"]:
                completed = message["params"]["turn"]
                return {
                    "skill": skill, "status": completed["status"], "model": thread.get("model"),
                    "duration_ms": completed.get("durationMs"), "error": completed.get("error"),
                    "messages": [item["text"] for item in completed["items"] if item.get("type") == "agentMessage"],
                    "events": events, "before": before, "after": snapshot(workspace),
                }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path, help="Fresh disposable output directory outside this repository")
    parser.add_argument("--case", action="append", help="Skill name; defaults to all six scenarios")
    parser.add_argument("--timeout", type=int, default=600, help="Maximum seconds per native model turn")
    args = parser.parse_args()
    output = args.output.resolve()
    if output.is_relative_to(ROOT) or output.exists():
        parser.error("Use a fresh output directory outside the source repository")
    cases = json.loads((ROOT / "evals/native/cases.json").read_text(encoding="utf-8"))
    selected = set(args.case or [case["skill"] for case in cases])
    if selected - {case["skill"] for case in cases}:
        parser.error("Unknown scenario")
    output.mkdir(parents=True)
    build_plugins(ROOT, output / "bundle")
    plugin = output / "bundle/codex"
    results = []
    for case in cases:
        if case["skill"] not in selected:
            continue
        workspace = output / "workspaces" / case["skill"]
        workspace.mkdir(parents=True)
        for name, contents in case["files"].items():
            path = workspace / name
            if not path.resolve().is_relative_to(workspace):
                raise ValueError(f"Fixture path escapes workspace: {name}")
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(contents, encoding="utf-8")
        print(f"Starting {case['skill']}", flush=True)
        result = invoke(plugin, workspace, case["skill"], case["request"], case["read_only"], args.timeout)
        (output / f"{case['skill']}.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        results.append({key: result[key] for key in ("skill", "status", "model", "duration_ms") if key in result})
        (output / "summary.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
        print(f"Finished {case['skill']}: {result['status']}", flush=True)
    raise SystemExit(0 if all(result["status"] == "completed" for result in results) else 1)


if __name__ == "__main__":
    main()
