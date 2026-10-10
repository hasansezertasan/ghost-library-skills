#!/usr/bin/env python3
"""Evaluate a downstream Python implementation against padlib's fixture profile."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import sys


FUNCTIONS = {"left_pad", "right_pad", "center_pad", "pad", "zero_pad"}
CASE_FIELDS = {"name", "input", "output", "error", "description"}


def inventory(data: dict) -> tuple[list[tuple[str, str, dict]], list[str]]:
    """Stop at case containers so arguments and expected lists aren't cases."""
    cases = []
    issues = []
    if not isinstance(data, dict):
        raise ValueError("Fixture root must be a mapping")

    def visit(value, path):
        if isinstance(value, list):
            function = path[-1]
            seen = set()
            for index, case in enumerate(value):
                if not isinstance(case, dict):
                    raise ValueError(f"Malformed case at {'/'.join(path)}/{index}")
                name = case.get("name", f"index-{index}")
                if not isinstance(name, str) or not name:
                    raise ValueError(f"Invalid case name at {'/'.join(path)}/{index}")
                if name in seen:
                    raise ValueError(f"Duplicate case ID: {'/'.join(path)}/{name}")
                seen.add(name)
                cases.append(("/".join([*path, name]), function, case))
        elif isinstance(value, dict):
            for key, child in value.items():
                visit(child, [*path, str(key)])
        else:
            issues.append(f"Unsupported group: {'/'.join(path)}")

    for group, value in data.items():
        if group != "version":
            if group not in FUNCTIONS | {"unicode", "errors"}:
                issues.append(f"Unknown fixture group: {group}")
            visit(value, [str(group)])
    return cases, issues


def evaluate(data: dict, implementation) -> dict:
    cases, issues = inventory(data)
    results = []
    for case_id, function, case in cases:
        result = {"id": case_id, "function": function}
        unsupported = []
        if function not in FUNCTIONS:
            unsupported.append(f"Unknown function: {function}")
        if not callable(getattr(implementation, function, None)):
            unsupported.append(f"Missing callable: {function}")
        unknown = sorted(set(case) - CASE_FIELDS)
        if unknown:
            unsupported.append(f"Unknown assertion fields: {unknown}")
        if not isinstance(case.get("input"), list):
            unsupported.append("padlib input must be a positional argument list")
        expects_error = case.get("error", False)
        if not isinstance(expects_error, bool):
            unsupported.append("error must be a boolean")
        if expects_error and "output" in case:
            unsupported.append("Conflicting output and error assertions")
        if not expects_error and "output" not in case:
            unsupported.append("Missing output assertion")
        if case_id.startswith("errors/") and not expects_error:
            unsupported.append("Error-group case must assert error: true")
        if unsupported:
            result.update(status="unsupported", reasons=unsupported)
            results.append(result)
            continue
        try:
            actual = getattr(implementation, function)(*case["input"])
        except Exception as error:
            if expects_error:
                result.update(status="passed", assertion="detectable-error", error_type=type(error).__name__)
            else:
                result.update(status="failed", stage="call", error_type=type(error).__name__, error=str(error))
        else:
            if expects_error:
                result.update(status="failed", stage="assertion", expected="detectable error", actual=actual)
            elif type(actual) is not type(case["output"]) or actual != case["output"]:
                result.update(status="failed", stage="assertion", expected=case["output"], actual=actual)
            else:
                result.update(status="passed", assertion="exact-output")
        results.append(result)
    counts = Counter(result["status"] for result in results)
    totals = {"discovered": len(cases), "executed": counts["passed"] + counts["failed"]}
    totals.update({status: counts[status] for status in ("passed", "failed", "skipped", "unsupported")})
    full = bool(cases) and not issues and counts["passed"] == len(cases)
    return {"full_conformance": full, "totals": totals, "suite_issues": issues, "cases": results}


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixtures", required=True, type=Path)
    parser.add_argument("--implementation", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    args = parser.parse_args()
    report = {"full_conformance": False, "runtime": sys.version.split()[0]}
    try:
        import yaml

        # Catch duplicate YAML keys instead of allowing silent replacement.
        class UniqueLoader(yaml.SafeLoader):
            pass

        def unique_mapping(loader, node, deep=False):
            result = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                if key in result:
                    raise ValueError(f"Duplicate YAML key: {key}")
                result[key] = loader.construct_object(value_node, deep=deep)
            return result

        UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)
        data = yaml.load(args.fixtures.read_text(encoding="utf-8"), Loader=UniqueLoader)
        # Validate inventory before importing downstream code.
        inventory(data)
        spec = importlib.util.spec_from_file_location("padlib_candidate", args.implementation)
        if spec is None or spec.loader is None:
            raise ValueError("Cannot load implementation")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        report.update(evaluate(data, module))
        report["identity"] = {
            "fixture_sha256": file_hash(args.fixtures),
            "implementation_sha256": file_hash(args.implementation),
            "harness_sha256": file_hash(Path(__file__)),
        }
    except Exception as error:
        report.update(decision="incomplete", fatal_error=f"{type(error).__name__}: {error}")
    else:
        report["decision"] = "conformant" if report["full_conformance"] else "not-conformant"
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2, ensure_ascii=False, default=repr) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in ("decision", "full_conformance", "totals", "fatal_error") if key in report}))
    return 0 if report["full_conformance"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
