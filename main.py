"""main.py - Entry point and main menu for the Student Result Management System."""
import storage
import results
import reports
from student import Student, is_valid_id, is_valid_date

students = {}   # {student_id: Student}


# ---------- input helpers ----------
def ask(prompt):
    return input(prompt).strip()


def ask_score(prompt):
    """Keep asking until a number between 0 and 100 is entered."""
    while True:
        try:
            value = float(ask(prompt))
        except ValueError:
            print("  Please enter a number.")
            continue
        if 0 <= value <= 100:
            return value
        print("  Score must be between 0 and 100.")


def ask_gender():
    while True:
        g = ask("Gender (M/F): ").upper()
        if g in ("M", "F"):
            return "Male" if g == "M" else "Female"
        print("  Enter M or F.")


def ask_dob():
    while True:
        dob = ask("Date of birth (YYYY-MM-DD): ")
        if is_valid_date(dob):
            return dob
        print("  Invalid date. Use YYYY-MM-DD, e.g. 2010-05-21.")


def find_student(prompt="Enter Student ID: "):
    sid = ask(prompt).upper()
    student = students.get(sid)
    if student is None:
        print("  Student not found.")
    return student


def save():
    storage.save_students(students)


# ---------- student management ----------
def add_student():
    sid = ask("Student ID (e.g. STU001): ").upper()
    if not is_valid_id(sid):
        print("  Invalid ID format. Use letters then digits, e.g. STU001.")
        return
    if sid in students:
        print("  That ID already exists.")
        return
    name = ask("Full name: ")
    if not name:
        print("  Name cannot be empty.")
        return
    form = ask("Class/Form (e.g. SS1): ")
    gender = ask_gender()
    dob = ask_dob()
    students[sid] = Student(sid, name, form, gender, dob)
    save()
    print("  Student added.")


def view_students():
    if not students:
        print("  No students registered.")
        return
    print(f"{'ID':<10} {'Name':<25} {'Class':<8} {'Gender':<7} DOB")
    print("-" * 62)
    for s in reports.sort_students(students.values(), "name"):
        print(s)


def search_student():
    term = ask("Search by ID or name: ").lower()
    found = [s for s in students.values()
             if term == s.student_id.lower() or term in s.name.lower()]
    if not found:
        print("  No match found.")
    for s in found:
        print(s)


def update_student():
    s = find_student()
    if s is None:
        return
    print("Leave a field blank to keep the current value.")
    name = ask(f"Name [{s.name}]: ")
    form = ask(f"Class/Form [{s.form}]: ")
    gender = ask(f"Gender M/F [{s.gender}]: ").upper()
    dob = ask(f"DOB [{s.dob}]: ")
    if name:
        s.name = name.title()
    if form:
        s.form = form
    if gender in ("M", "F"):
        s.gender = "Male" if gender == "M" else "Female"
    if dob:
        if is_valid_date(dob):
            s.dob = dob
        else:
            print("  Invalid date ignored.")
    save()
    print("  Student updated.")


def delete_student():
    s = find_student()
    if s is None:
        return
    if ask(f"Delete {s.name}? (y/n): ").lower() == "y":
        del students[s.student_id]
        save()
        print("  Student deleted.")


# ---------- scores ----------
def record_scores():
    s = find_student()
    if s is None:
        return
    print(f"Enter at least {results.MIN_SUBJECTS} subjects. Type 'done' as subject name to finish.")
    while True:
        subject = ask("Subject name: ")
        if subject.lower() == "done":
            if len(s.scores) >= results.MIN_SUBJECTS:
                break
            print(f"  Only {len(s.scores)} subject(s) so far - need {results.MIN_SUBJECTS}.")
            continue
        if not subject:
            continue
        s.set_score(subject, ask_score(f"Score for {subject.title()} (0-100): "))
    save()
    print("  Scores saved.")


def update_score():
    s = find_student()
    if s is None:
        return
    if not s.scores:
        print("  No scores recorded for this student yet.")
        return
    print("Current subjects:", ", ".join(s.scores))
    subject = ask("Subject to update: ").title()
    if subject not in s.scores:
        print("  Subject not found.")
        return
    s.set_score(subject, ask_score("New score (0-100): "))
    save()
    print("  Score updated.")


def show_report_card():
    s = find_student()
    if s is None:
        return
    if not s.scores:
        print("  No scores recorded for this student yet.")
        return
    text = reports.report_card_text(s)
    print(text)
    if ask("Save to file? (y/n): ").lower() == "y":
        print("  Saved to", reports.save_report(text, f"{s.student_id}_report_card.txt"))


# ---------- reporting ----------
def list_results():
    scored = [s for s in students.values() if s.scores]
    if not scored:
        print("  No results to show.")
        return
    choice = ask("Sort by (1) average or (2) name: ")
    ordered = reports.sort_students(scored, "name" if choice == "2" else "average")
    print(reports.results_table_text(ordered))


def show_statistics():
    print(reports.statistics_text(list(students.values())))


def export_report():
    scored = [s for s in students.values() if s.scores]
    if not scored:
        print("  Nothing to report yet.")
        return
    try:
        path = reports.save_report(reports.full_report_text(scored))
    except OSError as err:
        print(f"  Could not save report: {err}")
    else:
        print("  Report saved to", path)


# ---------- menu ----------
MENU = """
===== STUDENT RESULT MANAGEMENT SYSTEM =====
 1. Add student           7. Update score
 2. View all students     8. Show report card
 3. Search student        9. List results (sorted)
 4. Update student       10. Class statistics
 5. Delete student       11. Save text report to file
 6. Record scores         0. Exit
"""

ACTIONS = {
    "1": add_student, "2": view_students, "3": search_student,
    "4": update_student, "5": delete_student, "6": record_scores,
    "7": update_score, "8": show_report_card, "9": list_results,
    "10": show_statistics, "11": export_report,
}


def main():
    global students
    students = storage.load_students()
    while True:
        print(MENU)
        choice = ask("Choose an option: ")
        if choice == "0":
            save()
            print("Data saved. Goodbye!")
            break
        action = ACTIONS.get(choice)
        if action is None:
            print("  Invalid option.")
            continue
        try:
            action()
        except (KeyboardInterrupt, EOFError):
            print("\n  Cancelled.")
        finally:
            pass


if __name__ == "__main__":
    main()
