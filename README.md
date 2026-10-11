# Grade Goal

A command-line calculator for weighted grades. Enter your completed work and a target, and it works out the average needed on the remaining work.

## Run it

Python 3.11 or newer; no packages to install. Run from this folder:

```sh
python3 -m grade_goal --component 20:85 --component 30:92 --target 90
```

Here, the first component is worth 20% of the whole course and received 85%. The second is worth 30% and received 92%.

```text
Completed weight: 50.00%
Current average on completed work: 89.20%
Earned course percentage points: 44.60 / 100
Remaining weight: 50.00%
Target overall grade: 90.00%
Required average on remaining work: 90.80%
```

Repeat `--component WEIGHT:GRADE` for each completed assessment or finalized category. Leave unfinished work out: entering zero counts as a real grade. Without `--target`, the command just shows the current average. You can also use `--target 85` alone before any work is completed.

Weights must be positive and total no more than 100. Grades and targets must be between 0 and 100, with up to six decimal places and no `%` symbol. Use `--help` for the options.

## The calculation

The calculation lives in `grade_goal/calculator.py`; the CLI is in `grade_goal/__main__.py`. It uses `Decimal` rather than floating-point numbers.

```text
earned points = sum(weight × grade / 100)
current average = earned points × 100 / completed weight
required average = (target - earned points) × 100 / remaining weight
```

The required value is a weighted average across the remaining work. Results display two decimals: ordinary values round half-up, while the required minimum rounds up (`88.333…` becomes `88.34`). The app also reports targets that are already secured or would need more than 100% on the remaining work.

This assumes a simple weighted percentage scheme. It doesn't handle extra credit, dropped assignments, curves, or letter-grade rules. Use the weights and finalized grades from your actual course policy.

## Check the code

```sh
python3 -m unittest discover -s tests -v
```

The tests check the calculations and CLI, including fractional weights and unreachable targets.

[MIT license](LICENSE).
