#!/usr/bin/env python3
"""Evaluate wheredirs' explicit-environment profile and optional warning observations."""

from __future__ import annotations

import argparse
from collections import Counter
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import sys
import warnings


DIRECTORIES = {"config_dir", "data_dir", "cache_dir", "state_dir", "logs_dir", "runtime_dir"}
PLATFORMS = {**dict.fromkeys(("linux", "freebsd", "openbsd", "netbsd", "dragonfly"), "xdg"),
             **dict.fromkeys(("macos", "darwin"), "apple"), **dict.fromkeys(("windows", "win32"), "windows")}
GROUPS = {"which_strategy", "xdg", "apple", "windows", "single-folder", "errors", "project", "observations"}
FIELDS = {"name", "function", "args", "strategy", "platform", "env", "output", "raises", "description", "warning"}
PLACEHOLDER = re.compile(r"\$([A-Za-z_][A-Za-z0-9_]*)")


def normalize(value: str) -> str:
    return re.sub(r"/+", "/", value.replace("\\", "/")).rstrip("/")


def expected_path(value: str, env: dict) -> str:
    # Match a complete variable token once; unknown names remain literal.
    return normalize(PLACEHOLDER.sub(lambda match: env.get(match[1], match[0]), value))


def inventory(data: dict) -> tuple[list[tuple[str, dict]], list[str]]:
    if not isinstance(data, dict):
        raise ValueError("Fixture root must be a mapping")
    cases, issues = [], []
    for group, entries in data.items():
        if group == "version":
            continue
        if group not in GROUPS:
            issues.append(f"Unknown group: {group}")
        if not isinstance(entries, list):
            raise ValueError(f"Group must contain case records: {group}")
        seen = set()
        for index, case in enumerate(entries):
            if not isinstance(case, dict) or not isinstance(case.get("name"), str) or not case["name"]:
                raise ValueError(f"Malformed case: {group}/{index}")
            if case["name"] in seen:
                raise ValueError(f"Duplicate case ID: {group}/{case['name']}")
            seen.add(case["name"])
            cases.append((f"{group}/{case['name']}", case))
    return cases, issues


def evaluate(data: dict, implementation) -> dict:
    cases, issues = inventory(data)
    results = []
    for case_id, case in cases:
        result = {"id": case_id}
        reasons = []
        unknown = set(case) - FIELDS
        if unknown:
            reasons.append(f"Unknown assertion fields: {sorted(unknown)}")
        function = case.get("function")
        args = case.get("args")
        env = case.get("env", {})
        raises = case.get("raises", False)
        if function == "which_strategy":
            if not isinstance(args, list) or len(args) != 1 or any(key in case for key in ("env", "platform", "strategy")):
                reasons.append("which_strategy needs one positional argument and no ambient inputs")
            if not callable(getattr(implementation, "which_strategy", None)):
                reasons.append("Missing which_strategy callable")
        elif function in DIRECTORIES:
            if not isinstance(args, dict) or "app" not in args or set(args) - {"app", "author"}:
                reasons.append("Directory args must map app and optional author")
            if "platform" not in case or "env" not in case:
                reasons.append("Directory cases need explicit platform and env")
            if not callable(getattr(implementation, "_resolve", None)):
                reasons.append("Missing explicit-environment _resolve callable")
        else:
            reasons.append(f"Unknown function: {function}")
        if not isinstance(env, dict) or any(not isinstance(k, str) or not isinstance(v, str) for k, v in env.items()):
            reasons.append("env must map variable names to strings")
        if not isinstance(raises, bool) or raises and "output" in case or not raises and "output" not in case:
            reasons.append("Exactly one output or raises: true assertion is required")
        if "output" in case and case["output"] is not None and not isinstance(case["output"], str):
            reasons.append("output must be a path/strategy string or null")
        if "warning" in case and not isinstance(case["warning"], bool):
            reasons.append("warning must be a boolean observation")
        if reasons:
            results.append({**result, "status": "unsupported", "reasons": reasons})
            continue
        call_env, call_args = copy.deepcopy(env), copy.deepcopy(args)
        ambient_before = dict(os.environ)
        platform_before = sys.platform
        failures = []
        with warnings.catch_warnings(record=True) as observed:
            warnings.simplefilter("always")
            try:
                if function == "which_strategy":
                    actual = implementation.which_strategy(*call_args)
                else:
                    call_args["strategy"] = case.get("strategy")
                    actual = implementation._resolve(case["platform"], call_env, function, call_args)
            except Exception as error:
                result["error_type"] = type(error).__name__
                if not raises:
                    failures.append(f"Unexpected {type(error).__name__}: {error}")
            else:
                if raises:
                    failures.append("Required error returned normally")
                    result["actual"] = actual
                else:
                    expected = case["output"]
                    if expected is None:
                        matches = actual is None
                    elif function == "which_strategy":
                        matches = isinstance(actual, str) and actual == expected
                    else:
                        expected = expected_path(expected, env)
                        matches = isinstance(actual, str) and normalize(actual) == expected
                    if not matches:
                        result.update(expected=expected, actual=actual)
                        failures.append("Output assertion failed")
        result["warning_count"] = len(observed)
        required_warning = case.get("warning")
        strategy = case.get("strategy")
        if strategy is None:
            strategy = PLATFORMS.get(case.get("platform"))
        # INSTALL requires warnings on successful XDG runtime fallbacks even
        # though the original fixtures encode only their returned paths.
        if function == "runtime_dir" and strategy == "xdg" and not raises and not env.get("XDG_RUNTIME_DIR", "").startswith("/"):
            if required_warning is False:
                failures.append("Observation contradicts required runtime-fallback warning")
            required_warning = True
        if required_warning is not None:
            result["warning_expected"] = required_warning
            if bool(observed) != required_warning:
                failures.append("Warning observation failed")
        expected_args = copy.deepcopy(args)
        if function in DIRECTORIES:
            expected_args["strategy"] = case.get("strategy")
        if call_env != env or call_args != expected_args:
            failures.append("Implementation mutated explicit inputs")
        if dict(os.environ) != ambient_before or sys.platform != platform_before:
            failures.append("Implementation mutated process inputs")
        result["status"] = "failed" if failures else "passed"
        if failures:
            result["failures"] = failures
        results.append(result)
    counts = Counter(case["status"] for case in results)
    totals = {"discovered": len(cases), "executed": counts["passed"] + counts["failed"]}
    totals.update({status: counts[status] for status in ("passed", "failed", "skipped", "unsupported")})
    totals["warning_assertions"] = sum("warning_expected" in case for case in results)
    return {"full_conformance": bool(cases) and not issues and counts["passed"] == len(cases),
            "totals": totals, "suite_issues": issues, "cases": results}


def load_fixtures(path: Path) -> dict:
    import yaml

    class UniqueLoader(yaml.SafeLoader):
        pass

    def mapping(loader, node, deep=False):
        values = {}
        for key_node, value_node in node.value:
            key = loader.construct_object(key_node, deep=deep)
            if key in values:
                raise ValueError(f"Duplicate YAML key: {key}")
            values[key] = loader.construct_object(value_node, deep=deep)
        return values

    UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, mapping)
    data = yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueLoader)
    inventory(data)
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixtures", required=True, type=Path)
    parser.add_argument("--observations", type=Path)
    parser.add_argument("--implementation", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    args = parser.parse_args()
    report = {"full_conformance": False, "runtime": sys.version.split()[0]}
    try:
        data = load_fixtures(args.fixtures)
        if args.observations:
            extra = load_fixtures(args.observations)
            if extra.get("version") != data.get("version"):
                raise ValueError("Observation fixture version differs")
            for group, entries in extra.items():
                if group != "version":
                    data.setdefault(group, []).extend(entries)
        inventory(data)
        spec = importlib.util.spec_from_file_location("wheredirs_candidate", args.implementation)
        if spec is None or spec.loader is None:
            raise ValueError("Cannot load implementation")
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        report.update(evaluate(data, module))
        identity_paths = {"fixtures": args.fixtures, "implementation": args.implementation, "harness": Path(__file__)}
        if args.observations:
            identity_paths["observations"] = args.observations
        report["identity"] = {name + "_sha256": hashlib.sha256(path.read_bytes()).hexdigest() for name, path in identity_paths.items()}
    except Exception as error:
        report.update(decision="incomplete", fatal_error=f"{type(error).__name__}: {error}")
    else:
        report["decision"] = "conformant" if report["full_conformance"] else "not-conformant"
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2, ensure_ascii=False, default=repr) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in ("decision", "totals", "fatal_error") if key in report}))
    return 0 if report["full_conformance"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
