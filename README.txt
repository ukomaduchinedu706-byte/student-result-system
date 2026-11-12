=====================================================
 STUDENT RESULT MANAGEMENT SYSTEM
 New Horizon - Introduction to Python Project
=====================================================

1. DESCRIPTION
--------------
A menu-driven Python application that lets a school register
students, record subject scores, calculate totals, averages and
grades, generate report cards and class reports, and store all
data permanently in a JSON file.

2. REQUIREMENTS
---------------
- Python 3.8 or newer
- No external libraries needed (standard library only)

3. HOW TO RUN
-------------
1. Open a terminal / command prompt.
2. Go into the project folder:
       cd student_result_system
3. Start the program:
       python main.py
   (use "python3 main.py" on Linux/Mac)

The data file (data/students.json) is created automatically
the first time you add a student.

4. PROJECT STRUCTURE
--------------------
student_result_system/
|-- main.py        Entry point and main menu
|-- student.py     Student class, ID/date validation (regex)
|-- results.py     Totals, averages, grading, class statistics
|-- storage.py     Load and save data (JSON)
|-- reports.py     Sorting and report generation
|-- data/
|   |-- students.json   Persistent data (auto-created)
|-- reports/       Saved text reports (auto-created)
|-- README.txt     Project documentation

5. FEATURES
-----------
A. Student Management
   - Add, view, search (by ID or name), update and delete students
B. Score Management
   - Record at least 5 subjects per student
   - Total, average and grade calculated automatically
   - Update existing scores
   - Individual report card
C. Reporting and Analysis
   - List all students with total, average and grade
   - Sort by average (highest first) or by name
   - Class statistics: highest score, lowest score, class average
   - Save a text report to a file
D. Data Persistence
   - Saves automatically after every change
   - Loads data on start-up
   - Handles a missing or corrupted data file

6. GRADING SCALE (based on average)
-----------------------------------
   70 - 100  : A  (Excellent)
   60 - 69   : B  (Very Good)
   50 - 59   : C  (Good)
   45 - 49   : D  (Fair)
   0  - 44   : F  (Fail)

7. INPUT FORMATS
----------------
- Student ID : letters followed by digits, e.g. STU001
- Date of birth : YYYY-MM-DD, e.g. 2010-05-21
- Scores : numbers from 0 to 100

8. PYTHON CONCEPTS USED
-----------------------
- Variables, data types and type conversion (float(), str)
- Flow control: if/elif/else, for and while loops
- Lists, tuples (GRADE_TABLE) and dictionaries (students, scores)
- Functions with parameters and return values
- Sorting with sorted(), key and lambda
- Exception handling: try / except / else / finally
- File handling with JSON (json module)
- Modules and packages: code split across several .py files
- Object-Oriented Programming: the Student class
- Dates and times: datetime records when scores are entered
- Standard library: os, json, re, datetime
- Regular expressions: validating the Student ID

9. AUTHOR
---------
Name        : ______________________
Matric No.  : ______________________
Department  : ______________________
GitHub      : ______________________
