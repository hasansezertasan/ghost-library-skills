#!/usr/bin/env python3
"""Exercise wheredirs' comparator, errors, nulls, warnings, and environment isolation."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile


def main() -> None:
    import yaml

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixtures", required=True, type=Path)
    parser.add_argument("--observations", required=True, type=Path)
    parser.add_argument("--implementation", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    args = parser.parse_args()
    fixture_text = args.fixtures.read_text(encoding="utf-8")
    data = yaml.safe_load(fixture_text)
    implementation = args.implementation.read_text(encoding="utf-8")
    wrong = copy.deepcopy(data)
    wrong["which_strategy"][0]["output"] = "deliberately wrong"
    unknown = copy.deepcopy(data)
    unknown["which_strategy"][0]["unknown_assertion"] = True
    controls = [
        ("wrong-expectation", yaml.safe_dump(wrong), "", True),
        ("wrong-return", fixture_text, '\ndef _resolve(*args):\n    return "deliberately wrong"\n', True),
        ("error-returns-normally", fixture_text,
         '\n_original_resolve = _resolve\n_original_picker = which_strategy\ndef _resolve(*args):\n    try:\n        return _original_resolve(*args)\n    except Exception:\n        return None\ndef which_strategy(*args):\n    try:\n        return _original_picker(*args)\n    except Exception:\n        return None\n', True),
        ("null-becomes-empty", fixture_text,
         '\n_original_resolve = _resolve\ndef _resolve(*args):\n    result = _original_resolve(*args)\n    return "" if result is None else result\n', True),
        ("warning-suppressed", fixture_text,
         '\n_original_resolve = _resolve\ndef _resolve(*args):\n    import warnings\n    with warnings.catch_warnings():\n        warnings.simplefilter("ignore")\n        return _original_resolve(*args)\n', True),
        ("spurious-warning", fixture_text,
         '\n_original_resolve = _resolve\ndef _resolve(*args):\n    import warnings\n    warnings.warn("spurious warning")\n    return _original_resolve(*args)\n', True),
        ("ambient-environment-leak", fixture_text,
         '\n_original_resolve = _resolve\ndef _resolve(platform, env, function, args):\n    # Simulate a poisoned ambient HOME without modifying the real process.\n    leaked = dict(env)\n    leaked.setdefault("HOME", "/ambient-sentinel")\n    return _original_resolve(platform, leaked, function, args)\n', True),
        ("unknown-assertion", yaml.safe_dump(unknown), "", True),
        ("empty-suite", 'version: "0.1.0"\n', "", False),
        ("duplicate-key", 'xdg: []\nxdg: []\n', "", False),
    ]
    runner = Path(__file__).with_name("run.py")
    results = []
    with tempfile.TemporaryDirectory(prefix="wheredirs-controls-") as directory:
        root = Path(directory)

        def execute(fixture, module, report, observations=True):
            command = [sys.executable, str(runner), "--fixtures", str(fixture),
                       "--implementation", str(module), "--report", str(report)]
            if observations:
                command.extend(["--observations", str(args.observations.resolve())])
            return subprocess.run(command, capture_output=True, text=True)

        baseline = execute(args.fixtures.resolve(), args.implementation.resolve(), root / "baseline.json")
        if baseline.returncode:
            raise SystemExit(f"Baseline must pass first: {baseline.stdout}{baseline.stderr}")
        for name, content, fault, observations in controls:
            fixture, module, report_path = root / f"{name}.yaml", root / f"{name}.py", root / f"{name}.json"
            fixture.write_text(content, encoding="utf-8")
            module.write_text(implementation + fault, encoding="utf-8")
            process = execute(fixture, module, report_path, observations)
            report = json.loads(report_path.read_text(encoding="utf-8"))
            results.append({"control": name, "exit_code": process.returncode, "decision": report["decision"],
                            "totals": report.get("totals"), "fatal_error": report.get("fatal_error"),
                            "affected_cases": [{key: case[key] for key in ("id", "status", "failures", "reasons") if key in case}
                                               for case in report.get("cases", []) if case["status"] != "passed"]})
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    if any(result["exit_code"] != 1 or result["decision"] == "conformant" for result in results):
        raise SystemExit("A negative control failed to reject its deliberate fault")
    print(f"Detected all {len(results)} deliberate faults")


if __name__ == "__main__":
    main()
