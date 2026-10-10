"""Decimal-based calculations without course-specific grading assumptions."""

from dataclasses import dataclass
from decimal import Decimal, ROUND_CEILING, ROUND_HALF_UP, localcontext
import re


HUNDRED = Decimal("100")
ZERO = Decimal("0")


@dataclass(frozen=True)
class Component:
    weight: Decimal
    grade: Decimal


@dataclass(frozen=True)
class GradeReport:
    completed_weight: Decimal
    earned_points: Decimal
    current_average: Decimal | None
    remaining_weight: Decimal
    target: Decimal | None
    required_average: Decimal | None
    status: str | None


def parse_percentage(value, label="percentage"):
    """Accept a finite percentage from 0 to 100, with up to six decimals."""
    text = str(value).strip()
    if not re.fullmatch(r"[0-9]+(?:\.[0-9]{1,6})?", text):
        raise ValueError(f"{label} must be a number from 0 to 100 with at most six decimal places")
    result = Decimal(text)
    if result > HUNDRED:
        raise ValueError(f"{label} must be from 0 to 100")
    return result


def parse_component(value):
    """Parse WEIGHT:GRADE, where weight is a percentage of the whole course."""
    parts = value.split(":")
    if len(parts) != 2:
        raise ValueError("component must use WEIGHT:GRADE, for example 25:88")
    weight = parse_percentage(parts[0], "weight")
    grade = parse_percentage(parts[1], "grade")
    if weight == ZERO:
        raise ValueError("component weight must be greater than zero")
    return Component(weight, grade)


def calculate(components, target=None):
    """Return a report for completed components and an optional overall target."""
    # Validate API callers too; a manually constructed Component is not trusted.
    validated = [parse_component(f"{item.weight}:{item.grade}") for item in components]
    target = parse_percentage(target, "target") if target is not None else None
    with localcontext() as context:
        context.prec = 50
        completed = sum((item.weight for item in validated), ZERO)
        if completed > HUNDRED:
            raise ValueError("completed component weights cannot exceed 100%")
        earned = sum((item.weight * item.grade / HUNDRED for item in validated), ZERO)
        remaining = HUNDRED - completed
        current = earned * HUNDRED / completed if completed else None
        required = None
        status = None
        if target is not None:
            if remaining == ZERO:
                status = "met" if earned >= target else "missed"
            elif earned >= target:
                required = ZERO
                status = "already_secured"
            else:
                required = (target - earned) * HUNDRED / remaining
                status = "possible" if required <= HUNDRED else "unreachable"
    return GradeReport(completed, earned, current, remaining, target, required, status)


def format_percentage(value, required=False):
    """Round ordinary displays to nearest; round a required minimum upward."""
    rounding = ROUND_CEILING if required else ROUND_HALF_UP
    with localcontext() as context:
        context.prec = 50
        return f"{value.quantize(Decimal('0.01'), rounding=rounding):.2f}"
