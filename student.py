"""student.py - Student class and validation helpers."""
import re
from datetime import datetime

ID_PATTERN = re.compile(r"^[A-Za-z]{2,5}/?\d{2,6}$")   # e.g. STU001, NH/2026
DATE_FORMAT = "%Y-%m-%d"


def is_valid_id(student_id):
    """Return True if the Student ID matches the allowed format (regex)."""
    return bool(ID_PATTERN.match(student_id))


def is_valid_date(text):
    """Return True if text is a real date in YYYY-MM-DD format."""
    try:
        datetime.strptime(text, DATE_FORMAT)
        return True
    except ValueError:
        return False


class Student:
    """Represents one student and their subject scores."""

    def __init__(self, student_id, name, form, gender, dob,
                 scores=None, date_entered=None):
        self.student_id = student_id.upper()
        self.name = name.title()
        self.form = form
        self.gender = gender
        self.dob = dob
        self.scores = scores if scores is not None else {}   # {subject: score}
        self.date_entered = date_entered                     # when scores were recorded

    def set_score(self, subject, score):
        """Record or update a score and stamp the date/time it was entered."""
        self.scores[subject.title()] = float(score)
        self.date_entered = datetime.now().strftime("%Y-%m-%d %H:%M")

    def to_dict(self):
        return {
            "student_id": self.student_id, "name": self.name,
            "form": self.form, "gender": self.gender, "dob": self.dob,
            "scores": self.scores, "date_entered": self.date_entered,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["student_id"], data["name"], data["form"],
                   data["gender"], data["dob"],
                   data.get("scores", {}), data.get("date_entered"))

    def __str__(self):
        return (f"{self.student_id:<10} {self.name:<25} {self.form:<8} "
                f"{self.gender:<7} {self.dob}")
