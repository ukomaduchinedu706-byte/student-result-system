"""results.py - Score calculation and grading logic."""

MIN_SUBJECTS = 5

# (minimum average, grade, remark) checked from highest to lowest
GRADE_TABLE = (
    (70, "A", "Excellent"),
    (60, "B", "Very Good"),
    (50, "C", "Good"),
    (45, "D", "Fair"),
    (0,  "F", "Fail"),
)


def calculate_total(student):
    return sum(student.scores.values())


def calculate_average(student):
    if not student.scores:
        return 0.0
    return calculate_total(student) / len(student.scores)


def assign_grade(average):
    """Return (grade, remark) for an average score."""
    for minimum, grade, remark in GRADE_TABLE:
        if average >= minimum:
            return grade, remark
    return "F", "Fail"


def has_complete_scores(student):
    return len(student.scores) >= MIN_SUBJECTS


def summary(student):
    """Return a dict of total, average, grade and remark for a student."""
    avg = calculate_average(student)
    grade, remark = assign_grade(avg)
    return {"total": calculate_total(student), "average": avg,
            "grade": grade, "remark": remark}


def class_statistics(students):
    """Return highest/lowest individual score and class average, or None."""
    all_scores = []
    averages = []
    for s in students:
        if s.scores:
            all_scores.extend(s.scores.values())
            averages.append(calculate_average(s))
    if not all_scores:
        return None
    return {
        "highest": max(all_scores),
        "lowest": min(all_scores),
        "class_average": sum(averages) / len(averages),
        "count": len(averages),
    }
