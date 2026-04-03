def get_highest_scorer(students):
    return max(students, key=lambda s: s["score"])


def get_lowest_scorer(students):
    return min(students, key=lambda s: s["score"])


def get_average_score(students):
    total = sum(s["score"] for s in students)
    return round(total / len(students), 2)


def get_passing_students(students, passing_score=50):
    return [s for s in students if s["score"] >= passing_score]


def get_failing_students(students, passing_score=50):
    return [s for s in students if s["score"] < passing_score]


def sort_students_by_score(students, descending=True):
    return sorted(students, key=lambda s: s["score"], reverse=descending)


def get_student_count(students):
    return len(students)
