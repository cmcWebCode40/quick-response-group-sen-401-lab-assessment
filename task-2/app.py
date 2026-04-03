"""
app.py — Main entry point for the Student Score Analysis application.

This module imports student data and utility functions, then displays a
comprehensive, well-formatted score analysis report to the console.

Perfective Maintenance:
    - Enhanced console output using the `tabulate` library for table formatting.
    - Added median score and letter-grade column to the report.
    - Improved section headers and visual separators for readability.

Corrective Maintenance:
    - Handles the edge case of an empty student list gracefully.
"""

from tabulate import tabulate

from students import students
from helpers.utils import (
    get_highest_scorer,
    get_lowest_scorer,
    get_average_score,
    get_median_score,
    get_passing_students,
    get_failing_students,
    sort_students_by_score,
    get_student_count,
    grade_student,
)


# ──────────────────────────────────────
#  Display Helpers
# ──────────────────────────────────────

BORDER = "=" * 60
SECTION = "-" * 60


def print_header(title: str) -> None:
    """Print a centred section header."""
    print(f"\n{SECTION}")
    print(f"  {title}")
    print(SECTION)


# ──────────────────────────────────────
#  Main Application Logic
# ──────────────────────────────────────


def main() -> None:
    """Run the student score analysis and display the report."""

    print(f"\n{BORDER}")
    print("        📊  STUDENT SCORE ANALYSIS REPORT")
    print(BORDER)

    # ── Guard: empty list ────────────────────────
    if not students:
        print("\n⚠️  No student records found. Nothing to analyse.")
        print(BORDER)
        return

    # ── Summary Statistics ───────────────────────
    count = get_student_count(students)
    average = get_average_score(students)
    median = get_median_score(students)
    highest = get_highest_scorer(students)
    lowest = get_lowest_scorer(students)

    print_header("Summary Statistics")
    summary_table = [
        ["Total Students", count],
        ["Average Score", average],
        ["Median Score", median],
        ["Highest Scorer", f"{highest.name} ({highest.score})"],
        ["Lowest Scorer", f"{lowest.name} ({lowest.score})"],
    ]
    print(tabulate(summary_table, headers=["Metric", "Value"], tablefmt="fancy_grid"))

    # ── Full Rankings with Grades ────────────────
    print_header("Student Rankings (Highest → Lowest)")
    ranked = sort_students_by_score(students)
    ranking_rows = [
        [rank, s.name, s.score, grade_student(s.score)]
        for rank, s in enumerate(ranked, start=1)
    ]
    print(
        tabulate(
            ranking_rows,
            headers=["Rank", "Student Name", "Score", "Grade"],
            tablefmt="fancy_grid",
            colalign=("center", "left", "center", "center"),
        )
    )

    # ── Passing Students ─────────────────────────
    passing = get_passing_students(students)
    print_header(f"Passing Students ({len(passing)} of {count})")
    if passing:
        pass_rows = [[s.name, s.score, grade_student(s.score)] for s in passing]
        print(
            tabulate(
                pass_rows,
                headers=["Student Name", "Score", "Grade"],
                tablefmt="fancy_grid",
            )
        )
    else:
        print("  (none)")

    # ── Failing Students ─────────────────────────
    failing = get_failing_students(students)
    print_header(f"Failing Students ({len(failing)} of {count})")
    if failing:
        fail_rows = [[s.name, s.score, grade_student(s.score)] for s in failing]
        print(
            tabulate(
                fail_rows,
                headers=["Student Name", "Score", "Grade"],
                tablefmt="fancy_grid",
            )
        )
    else:
        print("  (none)")

    print(f"\n{BORDER}")
    print("        ✅  Report Complete")
    print(f"{BORDER}\n")


if __name__ == "__main__":
    main()
