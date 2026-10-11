# Grade Goal

Works out a weighted grade and what average is needed on the remaining work. Written in Python, using `Decimal` for the arithmetic.

Python 3.11+. Run from this folder:

```sh
python3 -m grade_goal --component 20:85 --component 30:92 --target 90
```

`20:85` means a grade of 85 on work worth 20% of the whole course. This example gives a current average of **89.20%** and needs **90.80%** on the remaining half.

Repeat `--component` for completed work. Leave unfinished work out; a zero counts as a real grade. Omit `--target` to see just the current average, or use `--target 85` alone before anything is graded.

Weights must be positive and total at most 100. Grades and targets are 0–100, with up to six decimal places. The required average rounds up to two decimals so the displayed minimum isn't too low.

The calculation is in `grade_goal/calculator.py`. It assumes ordinary weighted percentages, without curves, extra credit, or dropped assignments.

Tests:

```sh
python3 -m unittest discover -s tests -v
```

[MIT](LICENSE)
