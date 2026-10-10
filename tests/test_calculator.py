from contextlib import redirect_stderr, redirect_stdout
from decimal import Decimal
import io
import unittest

from grade_goal.__main__ import main
from grade_goal.calculator import (
    Component, calculate, format_percentage, parse_component, parse_percentage,
)


class CalculationTests(unittest.TestCase):
    def test_weighted_average_and_remaining_target(self):
        report = calculate([parse_component("20:85"), parse_component("30:92")], "90")
        self.assertEqual(report.completed_weight, Decimal("50"))
        self.assertEqual(report.earned_points, Decimal("44.60"))
        self.assertEqual(report.current_average, Decimal("89.20"))
        self.assertEqual(report.remaining_weight, Decimal("50"))
        self.assertEqual(report.required_average, Decimal("90.80"))
        self.assertEqual(report.status, "possible")

    def test_fractional_weights_and_zero_grades(self):
        report = calculate([parse_component("12.5:80.1"), parse_component("37.5:0")])
        self.assertEqual(report.earned_points, Decimal("10.0125"))
        self.assertEqual(report.current_average, Decimal("20.025"))
        self.assertEqual(format_percentage(report.current_average), "20.03")
        self.assertIsNone(report.status)

    def test_no_completed_work(self):
        report = calculate([], "82.5")
        self.assertIsNone(report.current_average)
        self.assertEqual(report.remaining_weight, Decimal("100"))
        self.assertEqual(report.required_average, Decimal("82.5"))

    def test_secured_target_and_unreachable_target(self):
        secured = calculate([parse_component("90:100")], "85")
        self.assertEqual(secured.required_average, Decimal("0"))
        self.assertEqual(secured.status, "already_secured")
        unreachable = calculate([parse_component("80:50")], "90")
        self.assertEqual(unreachable.required_average, Decimal("250"))
        self.assertEqual(unreachable.status, "unreachable")

    def test_fully_completed_course(self):
        components = [parse_component("40:80"), parse_component("60:90")]
        met = calculate(components, "86")
        missed = calculate(components, "87")
        self.assertEqual(met.current_average, Decimal("86"))
        self.assertEqual(met.status, "met")
        self.assertEqual(missed.status, "missed")
        self.assertIsNone(met.required_average)
        self.assertIsNone(missed.required_average)

    def test_required_average_rounds_up(self):
        report = calculate([parse_component("40:80")], "85")
        self.assertEqual(format_percentage(report.required_average, required=True), "88.34")
        self.assertEqual(format_percentage(report.required_average), "88.33")
        self.assertGreaterEqual(Decimal("32") + Decimal("60") * Decimal("88.34") / 100, Decimal("85"))

    def test_exactly_hundred_required_is_reachable(self):
        report = calculate([parse_component("50:80")], "90")
        self.assertEqual(report.required_average, Decimal("100"))
        self.assertEqual(report.status, "possible")


class ValidationTests(unittest.TestCase):
    def test_percentage_boundaries(self):
        self.assertEqual(parse_percentage("0"), Decimal("0"))
        self.assertEqual(parse_percentage(" 100.000000 "), Decimal("100"))
        self.assertEqual(parse_percentage("0.000001"), Decimal("0.000001"))

    def test_invalid_percentages(self):
        for value in ["-1", "100.000001", "NaN", "Infinity", "1e2", "90%", "", ".5", "1.0000001"]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                parse_percentage(value)

    def test_component_shape_zero_weight_and_total_weight(self):
        for value in ["20", "20:80:90", "0:80", "20:", "101:80"]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                parse_component(value)
        with self.assertRaisesRegex(ValueError, "cannot exceed"):
            calculate([parse_component("60:80"), parse_component("41:80")])
        with self.assertRaises(ValueError):
            calculate([Component(Decimal("20"), Decimal("101"))])


class CliTests(unittest.TestCase):
    def test_documented_example(self):
        output = io.StringIO()
        with redirect_stdout(output):
            main(["--component", "20:85", "--component", "30:92", "--target", "90"])
        self.assertEqual(output.getvalue(), (
            "Completed weight: 50.00%\n"
            "Current average on completed work: 89.20%\n"
            "Earned course percentage points: 44.60 / 100\n"
            "Remaining weight: 50.00%\n"
            "Target overall grade: 90.00%\n"
            "Required average on remaining work: 90.80%\n"
        ))

    def test_cli_validation_returns_error_code(self):
        for args in [[], ["--component", "120:90"], ["--target", "NaN"]]:
            with self.subTest(args=args), redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as caught:
                main(args)
            self.assertEqual(caught.exception.code, 2)

    def test_cli_edge_messages(self):
        cases = [
            (["--target", "80"], "no completed work"),
            (["--component", "90:100", "--target", "85"], "already secured"),
            (["--component", "80:50", "--target", "90"], "cannot be reached"),
            (["--component", "100:90", "--target", "90"], "target was met"),
            (["--component", "100:80", "--target", "90"], "target was not met"),
        ]
        for args, expected in cases:
            output = io.StringIO()
            with self.subTest(args=args), redirect_stdout(output):
                main(args)
            self.assertIn(expected, output.getvalue())


if __name__ == "__main__":
    unittest.main()
