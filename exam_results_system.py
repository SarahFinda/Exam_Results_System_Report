"""
===============================================================
 DIGITAL EXAM & RESULTS MANAGEMENT SYSTEM
 PROG211 Object-Oriented Programming 1 - Individual Assignment
 Domain: Education
===============================================================

Run the interactive menu:   python exam_results_system.py
Run the automatic demo:     python exam_results_system.py --demo

The file is organised into clear sections so each part can be
reused on its own:

    SECTION 1 - Fixed grading rules (tuples)
    SECTION 2 - Classes: Student, Course, ExamResult
    SECTION 3 - Record functions (dictionaries)
    SECTION 4 - Sample data
    SECTION 5 - User input helpers
    SECTION 6 - Menu actions
    SECTION 7 - Menu and demo

PRIVACY (DPG): a Student only stores a student ID, a name and a
programme. No date of birth, phone number, home address, national
ID number or password is ever collected or stored.
"""

import sys


# ===============================================================
# SECTION 1 - FIXED GRADING RULES (TUPLES)
# Tuples are used because these values must NEVER change while
# the program runs. A tuple is immutable, so no part of the
# program can accidentally add, remove or edit a grade band.
# ===============================================================

# Each inner tuple is: (minimum score, letter grade, remark)
# Bands are checked from the top down, so they must stay in order.
GRADE_SCALE = (
    (80, "A", "Distinction"),
    (70, "B", "Very Good"),
    (60, "C", "Good"),
    (50, "D", "Pass"),
    (0,  "F", "Fail"),
)

SCORE_RANGE = (0, 100)   # (lowest possible score, highest possible score)
PASS_MARK = 50           # minimum score needed to pass a course


def get_grade(score):
    """Return a (letter, remark) tuple for a numeric score."""
    for minimum, letter, remark in GRADE_SCALE:   # tuple unpacking
        if score >= minimum:
            return letter, remark
    return "F", "Fail"


# ===============================================================
# SECTION 2 - CLASSES
# ===============================================================

class Student:
    """A student who sits exams and receives results."""

    # Class attribute - shared by every Student object
    total_students = 0

    def __init__(self, student_id, name, programme):
        # Instance attributes - unique to each Student object
        self.student_id = student_id
        self.name = name
        self.programme = programme
        # Dictionary of this student's results: {course_code: ExamResult}
        self.results = {}
        Student.total_students += 1

    # ---------- Instance methods ----------
    def add_result(self, result):
        """Attach an ExamResult object to this student."""
        self.results[result.course.course_code] = result

    def calculate_average(self):
        """Return the average score across all of this student's results."""
        if not self.results:
            return 0.0
        total = 0
        for result in self.results.values():
            total += result.score
        return round(total / len(self.results), 1)

    def overall_status(self):
        """Return 'PASSED ALL', 'REFERRED' (failed at least one) or 'NO RESULTS'."""
        if not self.results:
            return "NO RESULTS"
        for result in self.results.values():
            if not result.has_passed():
                return "REFERRED"
        return "PASSED ALL"

    def display_info(self):
        """Print the student's basic details."""
        print(f"  Student ID : {self.student_id}")
        print(f"  Name       : {self.name}")
        print(f"  Programme  : {self.programme}")
        print(f"  Results    : {len(self.results)} recorded")

    def display_result_slip(self):
        """Print a full result slip for this student."""
        print("=" * 62)
        print("                     STUDENT RESULT SLIP")
        print("=" * 62)
        self.display_info()
        print("-" * 62)
        print(f"  {'Code':<9}{'Course':<30}{'Score':>6}{'Grade':>7}  Remark")
        print("-" * 62)
        for result in self.results.values():
            letter, remark = result.get_grade()
            print(f"  {result.course.course_code:<9}{result.course.title:<30}"
                  f"{result.score:>6}{letter:>7}  {remark}")
        print("-" * 62)
        print(f"  Average score  : {self.calculate_average()}")
        print(f"  Overall status : {self.overall_status()}")
        print("=" * 62)

    # ---------- Class methods ----------
    @classmethod
    def from_string(cls, text):
        """Create a Student from text like 'LUCT001, Aminata Kamara, BSc Software Engineering'."""
        student_id, name, programme = (part.strip() for part in text.split(","))
        return cls(student_id, name, programme)

    @classmethod
    def get_total_students(cls):
        """Return how many students are currently registered."""
        return cls.total_students

    @classmethod
    def record_removal(cls):
        """Reduce the student count when a student is deleted."""
        cls.total_students -= 1

    # ---------- Static method ----------
    @staticmethod
    def find_top_student(students):
        """Return the student with the highest average score (or None)."""
        top = None
        for student in students.values():
            if not student.results:
                continue        # skip students with no results yet
            if top is None or student.calculate_average() > top.calculate_average():
                top = student
        return top


class Course:
    """A course (module) that has an exam."""

    total_courses = 0

    def __init__(self, course_code, title, credit_hours):
        if not Course.is_valid_code(course_code):
            raise ValueError(f"'{course_code}' is not a valid course code (example: PROG211).")
        self.course_code = course_code.upper()
        self.title = title
        self.credit_hours = credit_hours
        Course.total_courses += 1

    # ---------- Instance methods ----------
    def display_info(self):
        """Print the course details on one line."""
        print(f"  {self.course_code:<10}{self.title:<34}{self.credit_hours} credits")

    def get_statistics(self, results):
        """
        Work out statistics for this course from the results dictionary.
        Returns a TUPLE: (number of results, average, top result, lowest result, passed)
        """
        count = 0
        total = 0
        passed = 0
        top = None
        lowest = None
        for result in results.values():
            if result.course is not self:
                continue
            count += 1
            total += result.score
            if result.has_passed():
                passed += 1
            if top is None or result.score > top.score:
                top = result
            if lowest is None or result.score < lowest.score:
                lowest = result
        average = round(total / count, 1) if count else 0.0
        return count, average, top, lowest, passed

    # ---------- Class method ----------
    @classmethod
    def get_total_courses(cls):
        """Return how many Course objects have been created."""
        return cls.total_courses

    # ---------- Static method ----------
    @staticmethod
    def is_valid_code(code):
        """A valid code is letters followed by numbers, e.g. PROG211 (no object needed)."""
        code = code.strip()
        letters = code.rstrip("0123456789")
        numbers = code[len(letters):]
        return letters.isalpha() and numbers.isdigit()


class ExamResult:
    """The score one Student obtained in one Course."""

    total_results = 0   # how many results currently exist
    next_number = 1     # used to give every result a unique ID (never reused)

    def __init__(self, student, course, score):
        if not ExamResult.is_valid_score(score):
            low, high = SCORE_RANGE
            raise ValueError(f"Score must be a whole number from {low} to {high}.")
        self.result_id = f"R{ExamResult.next_number:03d}"
        ExamResult.next_number += 1
        ExamResult.total_results += 1
        self.student = student        # a Student OBJECT, not just an ID
        self.course = course          # a Course OBJECT
        self.score = score
        # Objects interacting: the result registers itself with the student
        student.add_result(self)

    # ---------- Instance methods ----------
    def get_grade(self):
        """Return (letter, remark) using the fixed tuple grade scale."""
        return get_grade(self.score)

    def has_passed(self):
        """Return True if the score meets the pass mark."""
        return self.score >= PASS_MARK

    def update_score(self, new_score):
        """Change the score (e.g. after a remark) and report the change."""
        if not ExamResult.is_valid_score(new_score):
            raise ValueError("Score must be a whole number from 0 to 100.")
        old_letter, _ = self.get_grade()
        old_score = self.score
        self.score = new_score
        new_letter, _ = self.get_grade()
        print(f"  Updated {self.result_id}: {old_score} ({old_letter}) -> "
              f"{new_score} ({new_letter})")

    def display_info(self):
        """Print this result on one line."""
        letter, remark = self.get_grade()
        print(f"  {self.result_id:<6}{self.student.student_id:<10}{self.student.name:<18}"
              f"{self.course.course_code:<10}{self.score:>5}{letter:>6}  {remark}")

    # ---------- Class methods ----------
    @classmethod
    def from_record(cls, record_text, students, courses):
        """
        Create an ExamResult from text like 'LUCT001, PROG211, 78'.
        Looks the student and course up in their dictionaries.
        """
        student_id, course_code, score = (part.strip() for part in record_text.split(","))
        student = students.get(student_id)
        course = courses.get(course_code.upper())
        if student is None:
            raise ValueError(f"No student with ID '{student_id}'.")
        if course is None:
            raise ValueError(f"No course with code '{course_code}'.")
        return cls(student, course, int(score))

    @classmethod
    def get_total_results(cls):
        """Return how many results currently exist."""
        return cls.total_results

    @classmethod
    def record_removal(cls):
        """Reduce the result count when a result is deleted."""
        cls.total_results -= 1

    # ---------- Static method ----------
    @staticmethod
    def is_valid_score(score):
        """Check a score is a whole number inside SCORE_RANGE (no object needed)."""
        low, high = SCORE_RANGE
        return isinstance(score, int) and low <= score <= high


# ===============================================================
# SECTION 3 - RECORD FUNCTIONS (DICTIONARIES)
# A DICTIONARY is the one data structure used to store multiple
# objects. Each object is stored with its unique ID as the key:
#     students = {"LUCT001": <Student>, ...}
#     courses  = {"PROG211": <Course>,  ...}
#     results  = {"R001":    <ExamResult>, ...}
# ===============================================================

def add_record(records, key, item):
    """Add an object to a dictionary. Refuses duplicate IDs."""
    if key in records:
        print(f"  [!] A record with ID '{key}' already exists - not added.")
        return False
    records[key] = item
    return True


def find_record(records, key):
    """Return the object stored under key, or None if it does not exist."""
    return records.get(key)


def delete_student_record(students, results, student_id):
    """
    Remove a student AND all of their exam results.
    Returns the deleted Student object, or None if the ID was not found.
    """
    student = students.pop(student_id, None)
    if student is None:
        return None
    for result in student.results.values():
        del results[result.result_id]
        ExamResult.record_removal()
    Student.record_removal()
    return student


def search_students_by_name(students, text):
    """Display every student whose name contains the search text."""
    text = text.lower()
    found = 0
    for student in students.values():
        if text in student.name.lower():
            print(f"  {student.student_id:<10}{student.name:<20}{student.programme}")
            found += 1
    return found


def display_students(students):
    """Display every Student object in the dictionary."""
    print(f"\n  ALL STUDENTS ({len(students)})")
    print("  " + "-" * 58)
    for student_id, student in students.items():
        print(f"  {student_id:<10}{student.name:<20}{student.programme}")


def display_courses(courses):
    """Display every Course object in the dictionary."""
    print(f"\n  ALL COURSES ({len(courses)})")
    print("  " + "-" * 58)
    for course in courses.values():
        course.display_info()


def display_results(results):
    """Display every ExamResult object in the dictionary."""
    print(f"\n  ALL EXAM RESULTS ({len(results)})")
    print("  " + "-" * 60)
    print(f"  {'ID':<6}{'Student':<10}{'Name':<18}{'Course':<10}{'Score':>5}{'Grade':>6}  Remark")
    print("  " + "-" * 60)
    for result in results.values():
        result.display_info()


# ===============================================================
# SECTION 4 - SAMPLE DATA (made-up students - no real personal data)
# ===============================================================

def load_sample_data():
    """Create sample objects and store them in dictionaries."""
    students = {}
    courses = {}
    results = {}

    # Creating Student objects - normal constructor and class method
    sample_students = (
        Student("LUCT001", "Aminata Kamara", "BSc Software Engineering"),
        Student("LUCT002", "Mohamed Sesay", "BSc Information Technology"),
        Student.from_string("LUCT003, Fatmata Conteh, BSc Software Engineering"),
        Student("LUCT004", "Ibrahim Bangura", "BSc Information Technology"),
    )
    for student in sample_students:
        add_record(students, student.student_id, student)

    # Creating Course objects
    sample_courses = (
        Course("PROG211", "Object-Oriented Programming 1", 3),
        Course("DCOMP114", "Database Systems", 3),
        Course("COMP315", "Intro to Information Systems", 3),
    )
    for course in sample_courses:
        add_record(courses, course.course_code, course)

    # Creating ExamResult objects from text records (class method)
    sample_records = (
        "LUCT001, PROG211, 82",
        "LUCT001, DCOMP114, 74",
        "LUCT001, COMP315, 68",
        "LUCT002, PROG211, 47",
        "LUCT002, DCOMP114, 63",
        "LUCT003, PROG211, 91",
        "LUCT003, COMP315, 55",
        "LUCT004, DCOMP114, 38",
    )
    for line in sample_records:
        result = ExamResult.from_record(line, students, courses)
        add_record(results, result.result_id, result)

    return students, courses, results


# ===============================================================
# SECTION 5 - USER INPUT HELPERS (clear prompts, never crash)
# ===============================================================

def ask_text(prompt):
    """Ask for text and remove extra spaces."""
    return input(prompt).strip()


def ask_score(prompt):
    """Keep asking until a valid score (0-100) is entered."""
    while True:
        text = input(prompt).strip()
        if text.isdigit() and ExamResult.is_valid_score(int(text)):
            return int(text)
        low, high = SCORE_RANGE
        print(f"  [!] Please type a whole number from {low} to {high}.")


# ===============================================================
# SECTION 6 - MENU ACTIONS
# ===============================================================

def record_new_result(students, courses, results):
    student_id = ask_text("  Enter student ID (e.g. LUCT002): ").upper()
    student = find_record(students, student_id)
    if student is None:
        print(f"  [!] No student found with ID '{student_id}'.")
        return
    course_code = ask_text("  Enter course code (e.g. COMP315): ").upper()
    course = find_record(courses, course_code)
    if course is None:
        print(f"  [!] No course found with code '{course_code}'.")
        return
    if course_code in student.results:
        print(f"  [!] {student.name} already has a {course_code} result. "
              "Use option 5 to update it.")
        return
    score = ask_score("  Enter score (0-100): ")
    result = ExamResult(student, course, score)
    add_record(results, result.result_id, result)
    letter, remark = result.get_grade()
    print(f"  [OK] Saved as {result.result_id}: {student.name}, {course_code}, "
          f"{score} - Grade {letter} ({remark})")


def update_existing_score(results):
    result_id = ask_text("  Enter result ID to update (e.g. R004): ").upper()
    result = find_record(results, result_id)
    if result is None:
        print(f"  [!] No result found with ID '{result_id}'.")
        return
    result.display_info()
    new_score = ask_score("  Enter the new score (0-100): ")
    result.update_score(new_score)


def show_result_slip(students):
    student_id = ask_text("  Enter student ID (e.g. LUCT001): ").upper()
    student = find_record(students, student_id)
    if student is None:
        print(f"  [!] No student found with ID '{student_id}'.")
        return
    print()
    student.display_result_slip()


def add_new_student(students):
    student_id = ask_text("  Enter new student ID (e.g. LUCT005): ").upper()
    if not student_id:
        print("  [!] Student ID cannot be empty.")
        return
    if student_id in students:
        print(f"  [!] A student with ID '{student_id}' already exists - not added.")
        return
    name = ask_text("  Enter student name: ")
    programme = ask_text("  Enter programme: ")
    if not name or not programme:
        print("  [!] Name and programme cannot be empty.")
        return
    student = Student(student_id, name, programme)
    add_record(students, student_id, student)
    print(f"  [OK] Student {student_id} added.")


def delete_student(students, results):
    student_id = ask_text("  Enter the ID of the student to delete: ").upper()
    student = find_record(students, student_id)
    if student is None:
        print(f"  [!] No student found with ID '{student_id}'.")
        return
    student.display_info()
    confirm = ask_text("  Type YES to delete this student and all their results: ")
    if confirm.upper() != "YES":
        print("  Cancelled - nothing was deleted.")
        return
    count = len(student.results)
    delete_student_record(students, results, student_id)
    print(f"  [OK] Deleted {student.name} ({student_id}) and {count} result(s).")


def search_by_name(students):
    text = ask_text("  Enter part of a name to search for: ")
    if not text:
        print("  [!] Please type at least one letter.")
        return
    print(f"\n  SEARCH RESULTS FOR '{text}'")
    print("  " + "-" * 58)
    found = search_students_by_name(students, text)
    if found == 0:
        print("  No students matched your search.")


def show_top_student(students):
    """Uses the STATIC method Student.find_top_student()."""
    top = Student.find_top_student(students)
    print("\n  TOP-SCORING STUDENT (highest average)")
    print("  " + "-" * 40)
    if top is None:
        print("  No results have been recorded yet.")
        return
    print(f"  {top.name} ({top.student_id})")
    print(f"  Programme      : {top.programme}")
    print(f"  Average score  : {top.calculate_average()}")
    print(f"  Courses taken  : {len(top.results)}")
    print(f"  Overall status : {top.overall_status()}")


def show_course_statistics(courses, results):
    """Uses the INSTANCE method course.get_statistics(), which returns a tuple."""
    print("\n  COURSE STATISTICS")
    for course in courses.values():
        count, average, top, lowest, passed = course.get_statistics(results)  # tuple unpacking
        print("  " + "-" * 58)
        print(f"  {course.course_code} - {course.title}")
        if count == 0:
            print("    No results yet.")
            continue
        print(f"    Results : {count}    Average : {average}    "
              f"Pass rate : {round(passed / count * 100)}%")
        print(f"    Highest : {top.score} ({top.student.name})")
        print(f"    Lowest  : {lowest.score} ({lowest.student.name})")
    print("  " + "-" * 58)


def show_summary(results):
    """Uses CLASS METHODS to report totals for the whole system."""
    passed = 0
    for result in results.values():
        if result.has_passed():
            passed += 1
    total = ExamResult.get_total_results()
    print("\n  SYSTEM SUMMARY")
    print("  " + "-" * 40)
    print(f"  Students registered : {Student.get_total_students()}")
    print(f"  Courses offered     : {Course.get_total_courses()}")
    print(f"  Results recorded    : {total}")
    print(f"  Passed              : {passed}")
    print(f"  Failed              : {total - passed}")
    print(f"  Pass mark           : {PASS_MARK}")
    print("\n  GRADE SCALE (fixed tuple)")
    for minimum, letter, remark in GRADE_SCALE:
        print(f"    {letter}  {minimum:>3}+   {remark}")


# ===============================================================
# SECTION 7 - MENU AND DEMO
# ===============================================================

MENU = (
    " 1. View all students",
    " 2. View all courses",
    " 3. View all exam results",
    " 4. Record a new exam result",
    " 5. Update a score (after remarking)",
    " 6. Print a student's result slip",
    " 7. Add a new student",
    " 8. Delete a student",
    " 9. Search for a student by name",
    "10. Show the top-scoring student",
    "11. Show course statistics",
    "12. System summary",
    " 0. Exit",
)


def run_menu():
    students, courses, results = load_sample_data()
    print("\n" + "=" * 62)
    print("        DIGITAL EXAM & RESULTS MANAGEMENT SYSTEM")
    print("=" * 62)
    print("  Type the number of an option and press Enter.")
    while True:
        print()
        for option in MENU:
            print(f"  {option}")
        choice = ask_text("\n  Your choice: ")
        if choice == "1":
            display_students(students)
        elif choice == "2":
            display_courses(courses)
        elif choice == "3":
            display_results(results)
        elif choice == "4":
            record_new_result(students, courses, results)
        elif choice == "5":
            update_existing_score(results)
        elif choice == "6":
            show_result_slip(students)
        elif choice == "7":
            add_new_student(students)
        elif choice == "8":
            delete_student(students, results)
        elif choice == "9":
            search_by_name(students)
        elif choice == "10":
            show_top_student(students)
        elif choice == "11":
            show_course_statistics(courses, results)
        elif choice == "12":
            show_summary(results)
        elif choice == "0":
            print("  Goodbye!")
            break
        else:
            print("  [!] That is not an option. Please type a number from the menu.")


def run_demo():
    """Automatic demonstration of every requirement (no typing needed)."""
    print("=" * 62)
    print("  DEMO: Digital Exam & Results Management System")
    print("=" * 62)

    print("\n[Task 1] Creating objects and showing their attributes")
    students, courses, results = load_sample_data()
    students["LUCT001"].display_info()

    print("\n[Task 2] Records stored in dictionaries (ID -> object)")
    display_students(students)
    display_courses(courses)
    display_results(results)

    print("\n[Task 3] Instance method: update_score() after a remark")
    results["R004"].update_score(52)

    print("\n[Task 3] Class method: ExamResult.from_record()")
    new_result = ExamResult.from_record("LUCT002, COMP315, 71", students, courses)
    add_record(results, new_result.result_id, new_result)
    new_result.display_info()

    print("\n[Task 3] Static method: ExamResult.is_valid_score()")
    for value in (85, 105, -3):
        print(f"  is_valid_score({value}) -> {ExamResult.is_valid_score(value)}")

    print("\n[Validation] Trying to save an invalid score")
    try:
        ExamResult(students["LUCT003"], courses["DCOMP114"], 120)
    except ValueError as error:
        print(f"  [!] Rejected: {error}")

    print("\n[Interaction] Result slip built from Student + Course + ExamResult objects\n")
    students["LUCT002"].display_result_slip()

    print("\n[Feature] Top-scoring student (static method)")
    show_top_student(students)

    print("\n[Feature] Course statistics (instance method returning a tuple)")
    show_course_statistics(courses, results)

    print("\n[Feature] Deleting student LUCT004 and their results")
    deleted = delete_student_record(students, results, "LUCT004")
    print(f"  [OK] Deleted {deleted.name} ({deleted.student_id}).")
    display_students(students)

    show_summary(results)


if __name__ == "__main__":
    if "--demo" in sys.argv:
        run_demo()
    else:
        run_menu()
