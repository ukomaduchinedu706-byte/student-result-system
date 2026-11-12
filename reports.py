"""reports.py - Report generation functions."""
import os
from datetime import datetime

import results

REPORT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")


def sort_students(students, by="average"):
    """Sort a list of students by average (high to low) or by name (A-Z)."""
    if by == "name":
        return sorted(students, key=lambda s: s.name)
    return sorted(students, key=results.calculate_average, reverse=True)


def report_card_text(student):
    info = results.summary(student)
    lines = [
        "=" * 50,
        "              STUDENT REPORT CARD",
        "=" * 50,
        f"ID      : {student.student_id}",
        f"Name    : {student.name}",
        f"Class   : {student.form}",
        f"Gender  : {student.gender}",
        f"DOB     : {student.dob}",
        f"Entered : {student.date_entered or 'N/A'}",
        "-" * 50,
        f"{'Subject':<30}{'Score':>10}",
        "-" * 50,
    ]
    for subject, score in sorted(student.scores.items()):
        lines.append(f"{subject:<30}{score:>10.1f}")
    lines += [
        "-" * 50,
        f"Total   : {info['total']:.1f}",
        f"Average : {info['average']:.2f}",
        f"Grade   : {info['grade']} ({info['remark']})",
        "=" * 50,
    ]
    return "\n".join(lines)


def results_table_text(students):
    lines = [f"{'Rank':<6}{'ID':<10}{'Name':<25}{'Total':>8}{'Average':>10}{'Grade':>7}",
             "-" * 66]
    for rank, s in enumerate(students, start=1):
        info = results.summary(s)
        lines.append(f"{rank:<6}{s.student_id:<10}{s.name:<25}"
                     f"{info['total']:>8.1f}{info['average']:>10.2f}{info['grade']:>7}")
    return "\n".join(lines)


def statistics_text(students):
    stats = results.class_statistics(students)
    if stats is None:
        return "No scores recorded yet."
    return (f"Students with scores : {stats['count']}\n"
            f"Highest score        : {stats['highest']:.1f}\n"
            f"Lowest score         : {stats['lowest']:.1f}\n"
            f"Class average        : {stats['class_average']:.2f}")


def full_report_text(students):
    ranked = sort_students(students, "average")
    return "\n".join([
        "NEW HORIZON - CLASS RESULT REPORT",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        results_table_text(ranked),
        "",
        "CLASS STATISTICS",
        statistics_text(students),
    ])


def save_report(text, filename=None):
    """Write report text to a file in the reports folder; returns the path."""
    if filename is None:
        filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    os.makedirs(REPORT_DIR, exist_ok=True)
    path = os.path.join(REPORT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text + "\n")
    return path
