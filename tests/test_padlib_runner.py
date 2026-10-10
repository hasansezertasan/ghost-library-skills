"""Exercise discovery and failure detection without a library implementation."""

from types import SimpleNamespace
import unittest

from evals.padlib.run import evaluate, inventory


class PadlibRunnerTests(unittest.TestCase):
    def test_nested_argument_arrays_are_not_counted_as_cases(self):
        data = {"version": "0.1.0", "unicode": {"left_pad": [{"name": "emoji", "input": ["😊", 3], "output": "  😊"}]}}
        cases, issues = inventory(data)
        self.assertEqual(len(cases), 1)
        self.assertEqual(issues, [])

    def test_negative_error_case_catches_normal_return(self):
        data = {"errors": {"pad": [{"name": "invalid", "input": ["x", 2, " ", "INVALID"], "error": True}]}}
        result = evaluate(data, SimpleNamespace(pad=lambda *args: "x"))
        self.assertFalse(result["full_conformance"])
        self.assertEqual(result["totals"]["failed"], 1)
        self.assertEqual(result["totals"]["executed"], 1)

    def test_unknown_assertion_prevents_a_false_pass(self):
        data = {"left_pad": [{"name": "extra", "input": ["x", 2], "output": " x", "unimplemented_check": True}]}
        result = evaluate(data, SimpleNamespace(left_pad=lambda *args: " x"))
        self.assertEqual(result["totals"]["unsupported"], 1)
        self.assertEqual(result["totals"]["executed"], 0)
        self.assertFalse(result["full_conformance"])

    def test_output_comparison_is_exact(self):
        data = {"left_pad": [{"name": "space", "input": ["x", 2], "output": " x"}]}
        result = evaluate(data, SimpleNamespace(left_pad=lambda *args: "x"))
        self.assertEqual(result["totals"]["failed"], 1)
        self.assertFalse(result["full_conformance"])

    def test_zero_discovered_cases_are_not_conformant(self):
        result = evaluate({"version": "0.1.0"}, SimpleNamespace())
        self.assertEqual(result["totals"]["discovered"], 0)
        self.assertFalse(result["full_conformance"])

    def test_duplicate_ids_are_rejected(self):
        case = {"name": "same", "input": ["x", 2], "output": " x"}
        with self.assertRaisesRegex(ValueError, "Duplicate case ID"):
            inventory({"left_pad": [case, case]})


if __name__ == "__main__":
    unittest.main()
