"""storage.py - Load and save data (JSON)."""
import json
import os

from student import Student

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
DATA_FILE = os.path.join(DATA_DIR, "students.json")


def load_students(path=DATA_FILE):
    """Load students from JSON. Returns {} if the file is missing or damaged."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except FileNotFoundError:
        print("No data file found - starting with an empty database.")
        return {}
    except json.JSONDecodeError:
        print("Data file is corrupted - starting with an empty database.")
        return {}
    else:
        return {item["student_id"]: Student.from_dict(item) for item in raw}


def save_students(students, path=DATA_FILE):
    """Save all students to JSON. Returns True on success."""
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump([s.to_dict() for s in students.values()], f, indent=4)
    except OSError as err:
        print(f"Could not save data: {err}")
        return False
    return True
