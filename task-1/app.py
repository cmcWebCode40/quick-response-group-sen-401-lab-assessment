from students import students
from helpers.utils import (
    get_highest_scorer,
    get_lowest_scorer,
    get_average_score,
    get_passing_students,
    get_failing_students,
    sort_students_by_score,
    get_student_count,
)


def main():
    print("=" * 50)
    print("       STUDENT SCORE ANALYSIS")
    print("=" * 50)

    print(f"\nTotal Students: {get_student_count(students)}")

    highest = get_highest_scorer(students)
    print(f"\nHighest Scorer: {highest['name']} with {highest['score']} points")

    lowest = get_lowest_scorer(students)
    print(f"Lowest Scorer: {lowest['name']} with {lowest['score']} points")

    print(f"\nAverage Score: {get_average_score(students)}")

    print("\n--- Students Ranked by Score ---")
    for rank, student in enumerate(sort_students_by_score(students), start=1):
        print(f"  {rank}. {student['name']}: {student['score']}")

    passing = get_passing_students(students)
    print(f"\nPassing Students ({len(passing)}):")
    for student in passing:
        print(f"  - {student['name']}: {student['score']}")

    failing = get_failing_students(students)
    print(f"\nFailing Students ({len(failing)}):")
    for student in failing:
        print(f"  - {student['name']}: {student['score']}")

    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
