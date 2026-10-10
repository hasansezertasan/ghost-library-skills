#!/usr/bin/env python3
"""Prove that the padlib runner rejects seven deliberate faults."""

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
    parser.add_argument("--implementation", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    args = parser.parse_args()
    runner = Path(__file__).with_name("run.py")
    fixtures = yaml.safe_load(args.fixtures.read_text(encoding="utf-8"))
    implementation = args.implementation.read_text(encoding="utf-8")
    wrong = copy.deepcopy(fixtures)
    wrong["left_pad"][0]["output"] = "deliberately wrong expectation"
    unknown = copy.deepcopy(fixtures)
    unknown["left_pad"][0]["unknown_assertion"] = True
    controls = [
        ("wrong-expectation", yaml.safe_dump(wrong, allow_unicode=True), implementation),
        ("wrong-return", None, implementation + '\ndef left_pad(*args, **kwargs):\n    return "deliberately wrong"\n'),
        ("error-returns-normally", None, implementation + '\n_original_pad = pad\ndef pad(*args, **kwargs):\n    try:\n        return _original_pad(*args, **kwargs)\n    except ValueError:\n        return ""\n'),
        ("unknown-assertion", yaml.safe_dump(unknown, allow_unicode=True), implementation),
        ("empty-suite", 'version: "0.1.0"\n', implementation),
        ("duplicate-key", 'left_pad: []\nleft_pad: []\n', implementation),
        ("continued-center-pattern", None, implementation + '\n_original_center_pad = center_pad\ndef center_pad(string, length, fill_char=" "):\n    _original_center_pad(string, length, fill_char)\n    string = "" if string is None else str(string)\n    needed = max(0, int(length) - len(string))\n    left = needed // 2\n    filled = (fill_char * needed)[:needed]\n    return filled[:left] + string + filled[left:]\n'),
    ]
    results = []
    with tempfile.TemporaryDirectory(prefix="padlib-controls-") as directory:
        root = Path(directory)
        # Require a passing baseline before faults can establish failure detection.
        baseline = subprocess.run([sys.executable, str(runner), "--fixtures", str(args.fixtures.resolve()),
                                   "--implementation", str(args.implementation.resolve()), "--report", str(root / "baseline.json")],
                                  capture_output=True, text=True)
        if baseline.returncode:
            raise SystemExit(f"Baseline must pass first: {baseline.stdout}{baseline.stderr}")
        for name, fixture_text, module_text in controls:
            fixture = args.fixtures.resolve()
            if fixture_text is not None:
                fixture = root / f"{name}.yaml"
                fixture.write_text(fixture_text, encoding="utf-8")
            module = root / f"{name}.py"
            module.write_text(module_text, encoding="utf-8")
            output = root / f"{name}.json"
            process = subprocess.run([sys.executable, str(runner), "--fixtures", str(fixture),
                                      "--implementation", str(module), "--report", str(output)], capture_output=True, text=True)
            report = json.loads(output.read_text(encoding="utf-8"))
            results.append({"control": name, "exit_code": process.returncode, "decision": report["decision"],
                            "totals": report.get("totals"), "fatal_error": report.get("fatal_error")})
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    if any(result["exit_code"] != 1 or result["decision"] == "conformant" for result in results):
        raise SystemExit("A negative control failed to reject its deliberate fault")
    print(f"Detected all {len(results)} deliberate faults")


if __name__ == "__main__":
    main()
