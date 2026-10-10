"""Run with python -m grade_goal --help."""

import argparse

from .calculator import calculate, format_percentage, parse_component


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Calculate a weighted grade and the remaining average needed for a target."
    )
    parser.add_argument(
        "--component", action="append", default=[], metavar="WEIGHT:GRADE",
        help="completed component as whole-course weight and grade percentages; repeat as needed",
    )
    parser.add_argument("--target", metavar="PERCENT", help="desired overall course percentage")
    args = parser.parse_args(argv)
    if not args.component and args.target is None:
        parser.error("provide at least one --component or a --target")
    try:
        report = calculate([parse_component(value) for value in args.component], args.target)
    except ValueError as exc:
        parser.error(str(exc))

    print(f"Completed weight: {format_percentage(report.completed_weight)}%")
    current = (
        f"{format_percentage(report.current_average)}%" if report.current_average is not None
        else "not available (no completed work)"
    )
    print(f"Current average on completed work: {current}")
    print(f"Earned course percentage points: {format_percentage(report.earned_points)} / 100")
    print(f"Remaining weight: {format_percentage(report.remaining_weight)}%")
    if report.target is not None:
        print(f"Target overall grade: {format_percentage(report.target)}%")
        if report.required_average is not None:
            print(
                "Required average on remaining work: "
                f"{format_percentage(report.required_average, required=True)}%"
            )
        if report.status == "already_secured":
            print("The target is already secured under the supplied weights, even with 0% on remaining work.")
        elif report.status == "unreachable":
            print("The target cannot be reached with remaining grades capped at 100%.")
        elif report.status == "met":
            print("All weight is completed; the target was met.")
        elif report.status == "missed":
            print("All weight is completed; the target was not met.")


if __name__ == "__main__":
    main()
