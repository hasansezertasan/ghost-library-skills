"""Check assertion behavior that differs from the padlib profile."""

from types import SimpleNamespace
import unittest
import warnings

from evals.wheredirs.run import evaluate, expected_path, inventory


def directory_case(**changes):
    return {"name": "case", "function": "config_dir", "args": {"app": "App"},
            "strategy": "xdg", "platform": "linux", "env": {}, "output": "/fixture/App", **changes}


class WheredirsRunnerTests(unittest.TestCase):
    def test_unknown_placeholder_is_not_partially_substituted(self):
        self.assertEqual(expected_path("$HOME/$HOMEBREW", {"HOME": "/fixture"}), "/fixture/$HOMEBREW")

    def test_normalization_is_profile_specific(self):
        self.assertEqual(expected_path("$LOCAL/Company//App/", {"LOCAL": "C:\\Fixture\\"}), "C:/Fixture/Company/App")

    def test_missing_environment_is_explicit_and_does_not_use_host(self):
        received = []

        def resolve(platform, env, function, args):
            received.append(env.copy())
            return "/fixture/App"

        result = evaluate({"xdg": [directory_case()]}, SimpleNamespace(_resolve=resolve))
        self.assertTrue(result["full_conformance"])
        self.assertEqual(received, [{}])

    def test_null_is_distinct_from_empty_string(self):
        result = evaluate({"apple": [directory_case(output=None)]}, SimpleNamespace(_resolve=lambda *args: ""))
        self.assertEqual(result["totals"]["failed"], 1)

    def test_error_is_distinct_from_null(self):
        case = directory_case(raises=True)
        del case["output"]
        result = evaluate({"errors": [case]}, SimpleNamespace(_resolve=lambda *args: None))
        self.assertEqual(result["totals"]["failed"], 1)

    def test_warning_is_required_even_when_path_matches(self):
        result = evaluate({"observations": [directory_case(warning=True)]}, SimpleNamespace(_resolve=lambda *args: "/fixture/App"))
        self.assertEqual(result["totals"]["failed"], 1)
        self.assertEqual(result["cases"][0]["failures"], ["Warning observation failed"])

    def test_spec_warning_applies_without_a_fixture_warning_field(self):
        case = directory_case(function="runtime_dir", env={"HOME": "/fixture"})
        result = evaluate({"xdg": [case]}, SimpleNamespace(_resolve=lambda *args: "/fixture/App"))
        self.assertEqual(result["totals"]["failed"], 1)
        self.assertEqual(result["totals"]["warning_assertions"], 1)

    def test_warning_capture_is_not_suppressed_by_repetition(self):
        def resolve(*args):
            warnings.warn("runtime fallback", stacklevel=2)
            return "/fixture/App"

        cases = [directory_case(name="first", warning=True), directory_case(name="second", warning=True)]
        result = evaluate({"observations": cases}, SimpleNamespace(_resolve=resolve))
        self.assertTrue(result["full_conformance"])
        self.assertEqual(result["totals"]["warning_assertions"], 2)

    def test_unknown_assertion_cannot_pass(self):
        result = evaluate({"xdg": [directory_case(unknown=True)]}, SimpleNamespace(_resolve=lambda *args: "/fixture/App"))
        self.assertEqual(result["totals"]["unsupported"], 1)
        self.assertEqual(result["totals"]["executed"], 0)

    def test_input_mutation_is_a_failure(self):
        def resolve(platform, env, function, args):
            env["XDG_CONFIG_HOME"] = "/mutated"
            return "/fixture/App"

        case = directory_case()
        result = evaluate({"xdg": [case]}, SimpleNamespace(_resolve=resolve))
        self.assertEqual(result["totals"]["failed"], 1)
        self.assertEqual(case["env"], {})

    def test_strategy_outputs_are_not_path_normalized(self):
        case = {"name": "linux", "function": "which_strategy", "args": ["linux"], "output": "xdg"}
        result = evaluate({"which_strategy": [case]}, SimpleNamespace(which_strategy=lambda *args: "xdg/"))
        self.assertEqual(result["totals"]["failed"], 1)

    def test_duplicate_case_ids_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "Duplicate case ID"):
            inventory({"xdg": [directory_case(), directory_case()]})

    def test_empty_suite_is_not_conformant(self):
        self.assertFalse(evaluate({"version": "0.1.0"}, SimpleNamespace())["full_conformance"])


if __name__ == "__main__":
    unittest.main()
