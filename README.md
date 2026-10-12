# Digital Exam & Results Management System

**PROG211 – Object-Oriented Programming 1 | Individual Assignment**
**Domain:** Education
**Language:** Python 3 (no external libraries needed)

A small, open-source Python program that helps a school or university record exam scores, grade them automatically, correct scores after remarking, print result slips, find the top-scoring student, show course statistics and remove students who have left. It is built with Object-Oriented Programming and follows Digital Public Goods (DPG) principles.

---

## 1. The problem

In many schools, exam results are still written in paper registers or scattered spreadsheets. Grades are calculated by hand, mistakes are common, corrections after remarking are hard to track, and students wait a long time for their results. This program keeps every student, course and exam result in one place, applies the same grading rules to everyone and produces clear reports in seconds.

## 2. Features

| # | Menu option | What it does |
|---|---|---|
| 1 | View all students | Lists every registered student |
| 2 | View all courses | Lists every course and its credit hours |
| 3 | View all exam results | Lists every result with its score, grade and remark |
| 4 | Record a new exam result | Adds a score for a student in a course, graded automatically |
| 5 | Update a score | Corrects a score after remarking and shows the old and new grade |
| 6 | Print a result slip | Shows one student's results, average score and overall status |
| 7 | Add a new student | Registers a new student (duplicate IDs are refused) |
| 8 | **Delete a student** | Removes a student **and all their results**, after typing YES to confirm |
| 9 | **Search by name** | Finds students whose name contains the text typed (any case) |
| 10 | **Top-scoring student** | Shows the student with the highest average score |
| 11 | **Course statistics** | For each course: number of results, average, pass rate, highest and lowest score |
| 12 | System summary | Totals for students, courses, results, passes and fails, plus the grade scale |
| 0 | Exit | Closes the program |

## 3. Project files

```
exam-results-system/
├── exam_results_system.py   # The complete program (all code in one file)
├── README.md                # This file
└── LICENSE                  # MIT open-source licence
```

The program is one file, divided into clearly labelled sections:

| Section | Contents |
|---|---|
| 1 – Grading rules | `GRADE_SCALE`, `SCORE_RANGE`, `PASS_MARK` (tuples and constants) and `get_grade()` |
| 2 – Classes | `Student`, `Course`, `ExamResult` |
| 3 – Record functions | `add_record()`, `find_record()`, `delete_student_record()`, `search_students_by_name()`, `display_students()`, `display_courses()`, `display_results()` |
| 4 – Sample data | `load_sample_data()` – made-up students, courses and results |
| 5 – Input helpers | `ask_text()`, `ask_score()` – safe input that never crashes |
| 6 – Menu actions | One function per menu option |
| 7 – Menu and demo | `run_menu()` and `run_demo()` |

## 4. How to run

You only need Python 3.8 or newer.

```bash
git clone https://github.com/<your-username>/exam-results-system.git
cd exam-results-system

python exam_results_system.py           # interactive menu
python exam_results_system.py --demo    # automatic demo of every feature
```

## 5. How the assignment tasks are met

### Task 1 – Classes, attributes and objects

| Class | Attributes | Methods |
|---|---|---|
| `Student` | `student_id`, `name`, `programme`, `results`, `total_students` (class attribute) | `add_result()`, `calculate_average()`, `overall_status()`, `display_info()`, `display_result_slip()`, `from_string()`, `get_total_students()`, `record_removal()`, `find_top_student()` |
| `Course` | `course_code`, `title`, `credit_hours`, `total_courses` (class attribute) | `display_info()`, `get_statistics()`, `get_total_courses()`, `is_valid_code()` |
| `ExamResult` | `result_id`, `student`, `course`, `score`, `total_results` and `next_number` (class attributes) | `get_grade()`, `has_passed()`, `update_score()`, `display_info()`, `from_record()`, `get_total_results()`, `record_removal()`, `is_valid_score()` |

**Objects interacting:**
- An `ExamResult` object holds a real `Student` object and a real `Course` object, not just their IDs.
- When a result is created, it calls `student.add_result(self)`, so the student "knows" about its own results.
- A result slip is made by the `Student` asking each of its `ExamResult` objects for a grade, and each result reading the course title from its `Course` object.
- Deleting a student also removes that student's `ExamResult` objects from the results dictionary.
- Course statistics are worked out by a `Course` object checking which results belong to it.

### Task 2 – Data structure (dictionary)

The program uses **one data structure, the dictionary**, to store multiple objects. Each object's unique ID is its key:

```python
students = {"LUCT001": <Student>, "LUCT002": <Student>, ...}
courses  = {"PROG211": <Course>,  "DCOMP114": <Course>, ...}
results  = {"R001": <ExamResult>, "R002": <ExamResult>, ...}
```

Simple functions work with these dictionaries:
- **Add:** `add_record()` adds an object and refuses duplicate IDs.
- **Find:** `find_record()` looks an object up by its ID.
- **Delete:** `delete_student_record()` removes a student and their results.
- **Search:** `search_students_by_name()` finds students by part of their name.
- **Display:** `display_students()`, `display_courses()` and `display_results()` print the records.

Using the ID as the key means any record can be found or deleted instantly, without looping through every item.

**Optional tuples (bonus):** fixed values that must never change are stored as tuples:

```python
GRADE_SCALE = (
    (80, "A", "Distinction"),
    (70, "B", "Very Good"),
    (60, "C", "Good"),
    (50, "D", "Pass"),
    (0,  "F", "Fail"),
)
SCORE_RANGE = (0, 100)
```

Tuples are also used for:
- **The menu and the sample data** (`MENU`, `sample_students`, `sample_courses`, `sample_records`).
- **Returned values:** `get_grade()` returns `(letter, remark)`, and `course.get_statistics()` returns `(count, average, top, lowest, passed)`.

Tuple unpacking reads them, for example:

```python
for minimum, letter, remark in GRADE_SCALE:
    ...
count, average, top, lowest, passed = course.get_statistics(results)
```

### Task 3 – Methods

| Type | Example | What it does |
|---|---|---|
| Instance method | `result.update_score(52)` | Changes one result's score after a remark |
| Instance method | `student.calculate_average()` | Works out one student's average score |
| Instance method | `course.get_statistics(results)` | Works out one course's average, pass count, highest and lowest result |
| Class method | `ExamResult.from_record("LUCT002, COMP315, 71", students, courses)` | Creates a result object from a line of text |
| Class method | `Student.from_string("LUCT003, Fatmata Conteh, BSc Software Engineering")` | Creates a student object from a line of text |
| Class method | `Student.get_total_students()` / `ExamResult.get_total_results()` | Read the class attributes that count objects |
| Class method | `Student.record_removal()` / `ExamResult.record_removal()` | Update the counts when a student is deleted |
| Static method | `ExamResult.is_valid_score(105)` | Checks a score is from 0 to 100 (needs no object) |
| Static method | `Course.is_valid_code("PROG211")` | Checks a course code's format (needs no object) |
| Static method | `Student.find_top_student(students)` | Finds the student with the highest average |

## 6. How the solution meets DPG standards

| DPG principle | How this project meets it |
|---|---|
| **Open-source** | All source code is public on GitHub under the **MIT licence**, so anyone (schools, NGOs, government) can use, study, change and share it for free. It uses only standard Python, so there is nothing to buy. |
| **Inclusive and accessible design** | It runs in any text terminal on low-cost computers, with no internet connection needed. The numbered menu uses plain English, and every prompt gives an example (e.g. "Enter student ID (e.g. LUCT002)"). IDs and name searches work in upper or lower case. Wrong input never crashes the program: it shows a clear message and asks again. Messages use text labels such as `[OK]` and `[!]` rather than colour, so they work for colour-blind users and screen readers. Deleting asks for confirmation, so mistakes are not permanent. |
| **Privacy-respecting** | Only the minimum data needed for results is stored: student ID, name and programme. **No** date of birth, phone number, home address, national ID number, photo or password is collected. Data stays in memory on the local machine and is never sent anywhere. Deleting a student removes all of their results too, so no orphaned personal data is left behind. All sample data is made up. |
| **Modular and reusable** | The code is organised into labelled sections, each with one job: grading rules, classes, record functions, sample data, input helpers, menu actions and the menu itself. Each feature is its own small function. The grade scale can be changed in one place. The three classes can be copied or imported into another program (for example a web or mobile results portal) without being changed. |

## 7. Example usage

### Recording a result (option 4), including invalid input

```
  Your choice: 4
  Enter student ID (e.g. LUCT002): luct002
  Enter course code (e.g. COMP315): COMP315
  Enter score (0-100): abc
  [!] Please type a whole number from 0 to 100.
  Enter score (0-100): 150
  [!] Please type a whole number from 0 to 100.
  Enter score (0-100): 58
  [OK] Saved as R009: Mohamed Sesay, COMP315, 58 - Grade D (Pass)
```

### Updating a score after remarking (option 5)

```
  Your choice: 5
  Enter result ID to update (e.g. R004): R004
  R004  LUCT002   Mohamed Sesay     PROG211      47     F  Fail
  Enter the new score (0-100): 53
  Updated R004: 47 (F) -> 53 (D)
```

### Deleting a student (option 8)

```
  Your choice: 8
  Enter the ID of the student to delete: LUCT002
  Student ID : LUCT002
  Name       : Mohamed Sesay
  Programme  : BSc Information Technology
  Results    : 2 recorded
  Type YES to delete this student and all their results: yes
  [OK] Deleted Mohamed Sesay (LUCT002) and 2 result(s).
```

If anything other than YES is typed, the program shows `Cancelled - nothing was deleted.`

### Searching by name (option 9)

```
  Your choice: 9
  Enter part of a name to search for: fat

  SEARCH RESULTS FOR 'fat'
  ----------------------------------------------------------
  LUCT003   Fatmata Conteh      BSc Software Engineering
```

### Top-scoring student (option 10)

```
  Your choice: 10

  TOP-SCORING STUDENT (highest average)
  ----------------------------------------
  Aminata Kamara (LUCT001)
  Programme      : BSc Software Engineering
  Average score  : 74.7
  Courses taken  : 3
  Overall status : PASSED ALL
```

### Course statistics (option 11)

```
  Your choice: 11

  COURSE STATISTICS
  ----------------------------------------------------------
  PROG211 - Object-Oriented Programming 1
    Results : 3    Average : 73.3    Pass rate : 67%
    Highest : 91 (Fatmata Conteh)
    Lowest  : 47 (Mohamed Sesay)
  ----------------------------------------------------------
  DCOMP114 - Database Systems
    Results : 3    Average : 58.3    Pass rate : 67%
    Highest : 74 (Aminata Kamara)
    Lowest  : 38 (Ibrahim Bangura)
  ----------------------------------------------------------
  COMP315 - Intro to Information Systems
    Results : 2    Average : 61.5    Pass rate : 100%
    Highest : 68 (Aminata Kamara)
    Lowest  : 55 (Fatmata Conteh)
  ----------------------------------------------------------
```

### Result slip (option 6)

```
==============================================================
                     STUDENT RESULT SLIP
==============================================================
  Student ID : LUCT001
  Name       : Aminata Kamara
  Programme  : BSc Software Engineering
  Results    : 3 recorded
--------------------------------------------------------------
  Code     Course                         Score  Grade  Remark
--------------------------------------------------------------
  PROG211  Object-Oriented Programming 1     82      A  Distinction
  DCOMP114 Database Systems                  74      B  Very Good
  COMP315  Intro to Information Systems      68      C  Good
--------------------------------------------------------------
  Average score  : 74.7
  Overall status : PASSED ALL
==============================================================
```

## 8. Possible future improvements

- Save records to a file or database so they remain after the program closes.
- Add staff log-in so only authorised lecturers can change or delete records.
- Add a verification code to each result slip so employers can confirm results are genuine.

## 9. Licence

Released under the MIT Licence – see [LICENSE](LICENSE).
