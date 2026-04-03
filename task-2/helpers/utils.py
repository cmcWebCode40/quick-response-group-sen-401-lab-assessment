"""
utils.py — Utility functions for student score analysis.

This module provides reusable helper functions for analysing student scores,
including statistics, filtering, and sorting.

Corrective Maintenance:
    - All functions now guard against empty student lists to prevent
      ValueError, ZeroDivisionError, and IndexError at runtime.

Adaptive Maintenance:
    - Uses Python 3.12+ compatible type hints (list[], dict[], |).
    - Uses statistics.median from the standard library.

Perfective Maintenance:
    - Added median_score calculation for richer statistical output.
    - Added grade_student() for letter-grade classification.
    - Improved return types to use Student model objects.

Preventive Maintenance:
    - Every function has a docstring explaining purpose, parameters, and return value.
    - Meaningful inline comments added throughout.
"""

from __future__ import annotations

import statistics
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import Student


# ──────────────────────────────────────
#  Statistical Functions
# ──────────────────────────────────────


def get_highest_scorer(students: list[Student]) -> Student | None:
    """
    Return the student with the highest score.

    Args:
        students: A list of Student objects.

    Returns:
        The Student with the highest score, or None if the list is empty.
    """
    if not students:
        return None
    return max(students, key=lambda s: s.score)


def get_lowest_scorer(students: list[Student]) -> Student | None:
    """
    Return the student with the lowest score.

    Args:
        students: A list of Student objects.

    Returns:
        The Student with the lowest score, or None if the list is empty.
    """
    if not students:
        return None
    return min(students, key=lambda s: s.score)


def get_average_score(students: list[Student]) -> float:
    """
    Calculate and return the average score of all students.

    Args:
        students: A list of Student objects.

    Returns:
        The average score rounded to 2 decimal places, or 0.0 if the list is empty.
    """
    if not students:
        return 0.0
    total = sum(s.score for s in students)
    return round(total / len(students), 2)


def get_median_score(students: list[Student]) -> float:
    """
    Calculate and return the median score of all students.

    Uses the statistics.median function from the Python standard library.

    Args:
        students: A list of Student objects.

    Returns:
        The median score, or 0.0 if the list is empty.
    """
    if not students:
        return 0.0
    scores = [s.score for s in students]
    return float(statistics.median(scores))


# ──────────────────────────────────────
#  Filtering Functions
# ──────────────────────────────────────


def get_passing_students(students: list[Student], passing_score: int = 50) -> list[Student]:
    """
    Return students whose score meets or exceeds the passing threshold.

    Args:
        students: A list of Student objects.
        passing_score: The minimum score required to pass (default 50).

    Returns:
        A filtered list of Student objects who passed.
    """
    return [s for s in students if s.score >= passing_score]


def get_failing_students(students: list[Student], passing_score: int = 50) -> list[Student]:
    """
    Return students whose score is below the passing threshold.

    Args:
        students: A list of Student objects.
        passing_score: The minimum score required to pass (default 50).

    Returns:
        A filtered list of Student objects who failed.
    """
    return [s for s in students if s.score < passing_score]


# ──────────────────────────────────────
#  Sorting & Counting
# ──────────────────────────────────────


def sort_students_by_score(students: list[Student], descending: bool = True) -> list[Student]:
    """
    Return a new list of students sorted by their score.

    Args:
        students: A list of Student objects.
        descending: If True, sort highest-first; if False, sort lowest-first.

    Returns:
        A sorted list of Student objects.
    """
    return sorted(students, key=lambda s: s.score, reverse=descending)


def get_student_count(students: list[Student]) -> int:
    """
    Return the total number of students.

    Args:
        students: A list of Student objects.

    Returns:
        The count of students in the list.
    """
    return len(students)


# ──────────────────────────────────────
#  Grading (Perfective Enhancement)
# ──────────────────────────────────────


def grade_student(score: int) -> str:
    """
    Assign a letter grade based on a numeric score.

    Grading scale:
        A  = 70–100
        B  = 60–69
        C  = 50–59
        F  = 0–49

    Args:
        score: An integer score between 0 and 100.

    Returns:
        A single-letter grade string.
    """
    if score >= 70:
        return "A"
    elif score >= 60:
        return "B"
    elif score >= 50:
        return "C"
    else:
        return "F"
