# Grade Goal

A small Python CLI that calculates your weighted average and the average you need on remaining course work to reach a target. You supply the weights and grades; the app does not assume a school's grading policy.

## Features

- Calculates the current average **on completed work** and the percentage points earned toward the whole course.
- Finds the weighted average needed across all remaining work.
- Explains when a target is already secured, unreachable with grades capped at 100%, or fully decided.
- Uses `Decimal` arithmetic and validates percentages and total weight.
- Runs with the Python standard library only.

## Setup

Requires **Python 3.11 or newer**. Run from this project folder; no package installation is needed.

```bash
python -m grade_goal --help
```

If your system uses `python3`, substitute that for `python` in the examples.

## Example

Suppose completed work includes a component worth 20% of the course with a grade of 85%, and another worth 30% with a grade of 92%. For an overall goal of 90%:

```bash
python -m grade_goal --component 20:85 --component 30:92 --target 90
```

```text
Completed weight: 50.00%
Current average on completed work: 89.20%
Earned course percentage points: 44.60 / 100
Remaining weight: 50.00%
Target overall grade: 90.00%
Required average on remaining work: 90.80%
```

Each `--component WEIGHT:GRADE` represents **completed work**. `WEIGHT` is its percentage of the whole course, not its share of work completed so far. Repeat the option for as many completed components as you need. A component can be a single assessment or an already finalized category average, provided you use its correct whole-course weight.

## More commands

```bash
# Show the current weighted average without requesting a target.
python -m grade_goal --component 25:88 --component 15:94

# Plan before completing any work.
python -m grade_goal --target 85

# Check a fully completed course.
python -m grade_goal --component 40:80 --component 60:90 --target 85

# See a target that cannot be reached under the supplied weights.
python -m grade_goal --component 80:50 --target 90
```

Percentages must be between 0 and 100, without `%` symbols, and may have up to six decimal places. Component weights must be greater than zero, and their sum cannot exceed 100. `NaN`, infinity, negative numbers, and scientific notation are rejected. Omit unfinished components rather than entering a grade of zero, unless that zero is an actual finalized grade.

## Calculation

For completed components with weights `w` and grades `g`:

```text
earned points = sum(w × g / 100)
current average = earned points × 100 / sum(w)
remaining weight = 100 - sum(w)
required remaining average = (target - earned points) × 100 / remaining weight
```

The required average is a **weighted average across the remaining work**, not the score required on every assessment. Ordinary results display two decimals with half-up rounding. The required minimum rounds **up** to two decimals, so a displayed target such as `88.34%` does not understate a computed requirement of `88.333…%`.

## Tests

```bash
python -m unittest discover -s tests -v
```

Tests cover fractional weights, exact weighted contributions, zero grades, no completed work, completed courses, secured and unreachable targets, upward rounding, invalid percentages, total-weight validation, and CLI output. GitHub Actions is configured to run them on Python 3.11 and 3.14.

## Scope

This calculator models a simple weighted percentage course with grades from 0 to 100. It does not infer letter-grade cutoffs or support extra credit, dropped assignments, curves, attendance rules, category-specific averaging, school-specific rounding, or minimum exam requirements. Enter finalized grades and weights from your course's actual policy; those rules can change the result. It does not store grades or connect to a learning platform.

## Project layout

```text
grade_goal/calculator.py  Decimal calculations and validation
grade_goal/__main__.py    Command-line interface
tests/test_calculator.py  Standard-library unittest suite
```

## License

MIT — see [LICENSE](LICENSE).
