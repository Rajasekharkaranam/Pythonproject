import json
import os
import re
from datetime import datetime
from typing import Any, Dict, List, Optional, TypedDict


# ============================================================
# FILE NAMES
# ============================================================

STUDENT_FILE = "students.json"
ATTENDANCE_FILE = "attendance.json"
PERFORMANCE_FILE = "performance.json"


# ============================================================
# DATA TYPES
# ============================================================

class Student(TypedDict):
    student_id: str
    name: str
    email: str
    mobile: str
    course: str


class AttendanceRecord(TypedDict):
    student_id: str
    date: str
    status: str


class PerformanceRecord(TypedDict):
    student_id: str
    subject: str
    marks: float


# ============================================================
# FILE HANDLING
# ============================================================

def load_data(filename: str) -> List[Dict[str, Any]]:
    """Load data from a JSON file."""

    if not os.path.exists(filename):
        return []

    try:
        with open(filename, "r", encoding="utf-8") as file:
            data: Any = json.load(file)

        if not isinstance(data, list):
            return []

        result: List[Dict[str, Any]] = []

        for item in data:
            if isinstance(item, dict):
                result.append(item)

        return result

    except (json.JSONDecodeError, OSError):
        return []


def save_data(
    filename: str,
    data: List[Dict[str, Any]]
) -> None:
    """Save data to a JSON file."""

    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    except OSError as error:
        print(f"Error saving data: {error}")


# ============================================================
# APPLICATION DATA
# ============================================================

students: List[Student] = []
attendance_records: List[AttendanceRecord] = []
performance_records: List[PerformanceRecord] = []


def load_all_data() -> None:
    """Load and validate all saved application data."""

    global students
    global attendance_records
    global performance_records

    students = []
    attendance_records = []
    performance_records = []

    # --------------------------------------------------------
    # STUDENTS
    # --------------------------------------------------------

    raw_students = load_data(STUDENT_FILE)

    for item in raw_students:

        student_id = item.get("student_id")
        name = item.get("name")
        email = item.get("email")
        mobile = item.get("mobile")
        course = item.get("course")

        if (
            isinstance(student_id, str)
            and isinstance(name, str)
            and isinstance(email, str)
            and isinstance(mobile, str)
            and isinstance(course, str)
        ):
            student = Student(
                student_id=student_id,
                name=name,
                email=email,
                mobile=mobile,
                course=course
            )

            students.append(student)

    # --------------------------------------------------------
    # ATTENDANCE
    # --------------------------------------------------------

    raw_attendance = load_data(ATTENDANCE_FILE)

    for item in raw_attendance:

        student_id = item.get("student_id")
        date = item.get("date")
        status = item.get("status")

        if (
            isinstance(student_id, str)
            and isinstance(date, str)
            and isinstance(status, str)
        ):
            record = AttendanceRecord(
                student_id=student_id,
                date=date,
                status=status
            )

            attendance_records.append(record)

    # --------------------------------------------------------
    # PERFORMANCE
    # --------------------------------------------------------

    raw_performance = load_data(PERFORMANCE_FILE)

    for item in raw_performance:

        student_id = item.get("student_id")
        subject = item.get("subject")
        marks = item.get("marks")

        if (
            isinstance(student_id, str)
            and isinstance(subject, str)
            and isinstance(marks, (int, float))
        ):
            record = PerformanceRecord(
                student_id=student_id,
                subject=subject,
                marks=float(marks)
            )

            performance_records.append(record)


def save_all_data() -> None:
    """Save all application data."""

    student_data: List[Dict[str, Any]] = [
        dict(student)
        for student in students
    ]

    attendance_data: List[Dict[str, Any]] = [
        dict(record)
        for record in attendance_records
    ]

    performance_data: List[Dict[str, Any]] = [
        dict(record)
        for record in performance_records
    ]

    save_data(STUDENT_FILE, student_data)
    save_data(ATTENDANCE_FILE, attendance_data)
    save_data(PERFORMANCE_FILE, performance_data)


# ============================================================
# VALIDATION FUNCTIONS
# ============================================================

def validate_student_id(student_id: str) -> bool:
    """Validate Student ID."""

    if not student_id:
        return False

    return bool(
        re.fullmatch(
            r"[A-Za-z0-9_-]+",
            student_id
        )
    )


def validate_name(name: str) -> bool:
    """Validate student name."""

    if not name.strip():
        return False

    return all(
        character.isalpha() or character.isspace()
        for character in name
    )


def validate_email(email: str) -> bool:
    """Validate email."""

    pattern = (
        r"^[A-Za-z0-9._%+-]+"
        r"@[A-Za-z0-9.-]+\."
        r"[A-Za-z]{2,}$"
    )

    return bool(re.fullmatch(pattern, email))


def validate_mobile(mobile: str) -> bool:
    """Validate mobile number."""

    return mobile.isdigit() and len(mobile) == 10


def validate_subject(subject: str) -> bool:
    """Validate subject name."""

    if not subject.strip():
        return False

    return all(
        character.isalpha() or character.isspace()
        for character in subject
    )


def validate_marks(marks: float) -> bool:
    """Validate marks."""

    return 0.0 <= marks <= 100.0


def validate_attendance_status(status: str) -> bool:
    """Validate attendance status."""

    return status.upper() in {
        "P",
        "A",
        "PRESENT",
        "ABSENT"
    }


def normalize_attendance_status(
    status: str
) -> Optional[str]:

    status = status.upper()

    if status in {"P", "PRESENT"}:
        return "Present"

    if status in {"A", "ABSENT"}:
        return "Absent"

    return None


def validate_date(date: str) -> bool:

    try:
        datetime.strptime(
            date,
            "%d-%m-%Y"
        )

        return True

    except ValueError:
        return False


# ============================================================
# STUDENT SEARCH
# ============================================================

def find_student(
    student_id: str
) -> Optional[Student]:

    for student in students:

        if student["student_id"] == student_id:
            return student

    return None


def student_exists(student_id: str) -> bool:

    return find_student(student_id) is not None


# ============================================================
# STUDENT MANAGEMENT
# ============================================================

def add_student() -> None:

    print("\n========== ADD STUDENT ==========")

    student_id = input(
        "Enter Student ID: "
    ).strip()

    if not validate_student_id(student_id):

        print(
            "Invalid Student ID."
        )

        return

    if student_exists(student_id):

        print(
            "Error: Student ID already exists."
        )

        return

    name = input(
        "Enter Name: "
    ).strip()

    if not validate_name(name):

        print(
            "Name cannot be empty."
        )

        return

    email = input(
        "Enter Email: "
    ).strip()

    if not validate_email(email):

        print(
            "Invalid email address."
        )

        return

    mobile = input(
        "Enter Mobile Number: "
    ).strip()

    if not validate_mobile(mobile):

        print(
            "Invalid mobile number. "
            "Enter exactly 10 digits."
        )

        return

    course = input(
        "Enter Course: "
    ).strip()

    if not course:

        print(
            "Course cannot be empty."
        )

        return

    student = Student(
        student_id=student_id,
        name=name,
        email=email,
        mobile=mobile,
        course=course
    )

    students.append(student)

    save_all_data()

    print(
        "Student added successfully."
    )


def view_students() -> None:

    print(
        "\n========== STUDENT LIST =========="
    )

    if not students:

        print(
            "No students available."
        )

        return

    print(
        f"{'ID':<12}"
        f"{'Name':<25}"
        f"{'Email':<30}"
        f"{'Mobile':<15}"
        f"{'Course':<20}"
    )

    print("-" * 102)

    for student in students:

        print(
            f"{student['student_id']:<12}"
            f"{student['name']:<25}"
            f"{student['email']:<30}"
            f"{student['mobile']:<15}"
            f"{student['course']:<20}"
        )


def search_student() -> None:

    print(
        "\n========== SEARCH STUDENT =========="
    )

    student_id = input(
        "Enter Student ID: "
    ).strip()

    student = find_student(student_id)

    if student is None:

        print(
            "Student not found."
        )

        return

    print("\nStudent Found")
    print("-------------------------------")

    print(
        "Student ID :",
        student["student_id"]
    )

    print(
        "Name       :",
        student["name"]
    )

    print(
        "Email      :",
        student["email"]
    )

    print(
        "Mobile     :",
        student["mobile"]
    )

    print(
        "Course     :",
        student["course"]
    )


def update_student() -> None:

    print(
        "\n========== UPDATE STUDENT =========="
    )

    student_id = input(
        "Enter Student ID: "
    ).strip()

    student = find_student(student_id)

    if student is None:

        print(
            "Student not found."
        )

        return

    print(
        "Press Enter to keep existing information."
    )

    name = input(
        f"Name [{student['name']}]: "
    ).strip()

    email = input(
        f"Email [{student['email']}]: "
    ).strip()

    mobile = input(
        f"Mobile [{student['mobile']}]: "
    ).strip()

    course = input(
        f"Course [{student['course']}]: "
    ).strip()

    if name:

        if not validate_name(name):

            print(
                "Invalid name."
            )

            return

        student["name"] = name

    if email:

        if not validate_email(email):

            print(
                "Invalid email."
            )

            return

        student["email"] = email

    if mobile:

        if not validate_mobile(mobile):

            print(
                "Invalid mobile number."
            )

            return

        student["mobile"] = mobile

    if course:
        student["course"] = course

    save_all_data()

    print(
        "Student updated successfully."
    )


def remove_student() -> None:

    print(
        "\n========== REMOVE STUDENT =========="
    )

    student_id = input(
        "Enter Student ID: "
    ).strip()

    student = find_student(student_id)

    if student is None:

        print(
            "Student not found."
        )

        return

    confirmation = input(
        f"Remove {student['name']}? (Y/N): "
    ).strip().upper()

    if confirmation != "Y":

        print(
            "Operation cancelled."
        )

        return

    students.remove(student)

    attendance_records[:] = [
        record
        for record in attendance_records
        if record["student_id"] != student_id
    ]

    performance_records[:] = [
        record
        for record in performance_records
        if record["student_id"] != student_id
    ]

    save_all_data()

    print(
        "Student and associated records "
        "removed successfully."
    )


# ============================================================
# ATTENDANCE MANAGEMENT
# ============================================================

def record_attendance() -> None:

    print(
        "\n========== RECORD ATTENDANCE =========="
    )

    student_id = input(
        "Enter Student ID: "
    ).strip()

    if not student_exists(student_id):

        print(
            "Error: Student does not exist."
        )

        return

    date = input(
        "Enter Date (DD-MM-YYYY): "
    ).strip()

    if not validate_date(date):

        print(
            "Invalid date. "
            "Use DD-MM-YYYY format."
        )

        return

    status_input = input(
        "Enter Attendance Status "
        "(Present/Absent or P/A): "
    ).strip()

    if not validate_attendance_status(
        status_input
    ):

        print(
            "Invalid attendance status."
        )

        return

    status = normalize_attendance_status(
        status_input
    )

    if status is None:

        print(
            "Invalid attendance status."
        )

        return

    for record in attendance_records:

        if (
            record["student_id"] == student_id
            and record["date"] == date
        ):

            print(
                "Attendance already recorded "
                "for this date."
            )

            return

    attendance = AttendanceRecord(
        student_id=student_id,
        date=date,
        status=status
    )

    attendance_records.append(
        attendance
    )

    save_all_data()

    print(
        "Attendance recorded successfully."
    )


def calculate_attendance_percentage(
    student_id: str
) -> float:

    records = [
        record
        for record in attendance_records
        if record["student_id"] == student_id
    ]

    if not records:
        return 0.0

    present_count = sum(
        1
        for record in records
        if record["status"] == "Present"
    )

    total_classes = len(records)

    percentage = (
        float(present_count)
        / float(total_classes)
        * 100.0
    )

    return percentage


def view_student_attendance() -> None:

    print(
        "\n========== STUDENT ATTENDANCE =========="
    )

    student_id = input(
        "Enter Student ID: "
    ).strip()

    if not student_exists(student_id):

        print(
            "Student does not exist."
        )

        return

    records = [
        record
        for record in attendance_records
        if record["student_id"] == student_id
    ]

    if not records:

        print(
            "No attendance records found."
        )

        return

    print(
        f"\n{'Date':<20}"
        f"{'Status':<15}"
    )

    print("-" * 35)

    for record in records:

        print(
            f"{record['date']:<20}"
            f"{record['status']:<15}"
        )

    percentage = calculate_attendance_percentage(
        student_id
    )

    print("-" * 35)

    print(
        f"Attendance Percentage: "
        f"{percentage:.2f}%"
    )


# ============================================================
# PERFORMANCE
# ============================================================

def calculate_grade(
    average: float
) -> str:

    if average >= 90:
        return "A+"

    elif average >= 80:
        return "A"

    elif average >= 70:
        return "B"

    elif average >= 60:
        return "C"

    elif average >= 50:
        return "D"

    else:
        return "F"


def find_performance_record(
    student_id: str,
    subject: str
) -> Optional[PerformanceRecord]:

    for record in performance_records:

        if (
            record["student_id"] == student_id
            and record["subject"].lower()
            == subject.lower()
        ):

            return record

    return None


def add_marks() -> None:

    print(
        "\n========== ADD MARKS =========="
    )

    student_id = input(
        "Enter Student ID: "
    ).strip()

    if not student_exists(student_id):

        print(
            "Error: Student does not exist."
        )

        return

    subject = input(
        "Enter Subject Name: "
    ).strip()

    if not validate_subject(subject):

        print(
            "Invalid subject name."
        )

        return

    existing = find_performance_record(
        student_id,
        subject
    )

    if existing is not None:

        print(
            "Marks already exist for this subject. "
            "Use Update Marks."
        )

        return

    marks_input = input(
        "Enter Marks (0-100): "
    ).strip()

    try:

        marks = float(marks_input)

    except ValueError:

        print(
            "Marks must be a number."
        )

        return

    if not validate_marks(marks):

        print(
            "Marks must be between 0 and 100."
        )

        return

    performance = PerformanceRecord(
        student_id=student_id,
        subject=subject.title(),
        marks=marks
    )

    performance_records.append(
        performance
    )

    save_all_data()

    print(
        "Marks added successfully."
    )


def update_marks() -> None:

    print(
        "\n========== UPDATE MARKS =========="
    )

    student_id = input(
        "Enter Student ID: "
    ).strip()

    if not student_exists(student_id):

        print(
            "Student does not exist."
        )

        return

    subject = input(
        "Enter Subject Name: "
    ).strip()

    record = find_performance_record(
        student_id,
        subject
    )

    if record is None:

        print(
            "Performance record not found."
        )

        return

    marks_input = input(
        "Enter New Marks (0-100): "
    ).strip()

    try:

        marks = float(marks_input)

    except ValueError:

        print(
            "Marks must be numeric."
        )

        return

    if not validate_marks(marks):

        print(
            "Marks must be between 0 and 100."
        )

        return

    record["marks"] = marks

    save_all_data()

    print(
        "Marks updated successfully."
    )


def student_performance_report() -> None:

    print(
        "\n========== STUDENT PERFORMANCE =========="
    )

    student_id = input(
        "Enter Student ID: "
    ).strip()

    if not student_exists(student_id):

        print(
            "Student does not exist."
        )

        return

    records = [
        record
        for record in performance_records
        if record["student_id"] == student_id
    ]

    if not records:

        print(
            "No marks available."
        )

        return

    print(
        f"\n{'Subject':<25}"
        f"{'Marks':<10}"
    )

    print("-" * 35)

    total = 0.0

    for record in records:

        marks = float(
            record["marks"]
        )

        print(
            f"{record['subject']:<25}"
            f"{marks:<10.2f}"
        )

        total += marks

    average = (
        total
        / float(len(records))
    )

    grade = calculate_grade(
        average
    )

    print("-" * 35)

    print(
        f"Total   : {total:.2f}"
    )

    print(
        f"Average : {average:.2f}"
    )

    print(
        f"Grade   : {grade}"
    )


# ============================================================
# REPORTS
# ============================================================

def attendance_percentage_report() -> None:

    print(
        "\n========== ATTENDANCE PERCENTAGE REPORT =========="
    )

    if not students:

        print(
            "No students available."
        )

        return

    print(
        f"{'Student ID':<15}"
        f"{'Name':<25}"
        f"{'Attendance %':<15}"
    )

    print("-" * 55)

    for student in students:

        percentage = (
            calculate_attendance_percentage(
                student["student_id"]
            )
        )

        print(
            f"{student['student_id']:<15}"
            f"{student['name']:<25}"
            f"{percentage:<15.2f}"
        )


def below_attendance_threshold() -> None:

    print(
        "\n========== LOW ATTENDANCE REPORT =========="
    )

    try:

        threshold = float(
            input(
                "Enter Minimum Attendance Percentage: "
            )
        )

    except ValueError:

        print(
            "Invalid percentage."
        )

        return

    found = False

    print(
        f"\n{'Student ID':<15}"
        f"{'Name':<25}"
        f"{'Attendance %':<15}"
    )

    print("-" * 55)

    for student in students:

        percentage = (
            calculate_attendance_percentage(
                student["student_id"]
            )
        )

        if percentage < threshold:

            print(
                f"{student['student_id']:<15}"
                f"{student['name']:<25}"
                f"{percentage:<15.2f}"
            )

            found = True

    if not found:

        print(
            "No students below the threshold."
        )


def subject_wise_performance() -> None:

    print(
        "\n========== SUBJECT-WISE PERFORMANCE =========="
    )

    subject = input(
        "Enter Subject: "
    ).strip()

    records = [
        record
        for record in performance_records
        if record["subject"].lower()
        == subject.lower()
    ]

    if not records:

        print(
            "No records found for this subject."
        )

        return

    print(
        f"\n{'Student ID':<15}"
        f"{'Student Name':<25}"
        f"{'Marks':<10}"
    )

    print("-" * 50)

    for record in records:

        student = find_student(
            record["student_id"]
        )

        if student is None:
            name = "Unknown"
        else:
            name = student["name"]

        marks = float(
            record["marks"]
        )

        print(
            f"{record['student_id']:<15}"
            f"{name:<25}"
            f"{marks:<10.2f}"
        )


def highest_marks_report() -> None:

    print(
        "\n========== HIGHEST MARKS =========="
    )

    if not performance_records:

        print(
            "No performance records available."
        )

        return

    subjects = sorted(
        {
            record["subject"]
            for record in performance_records
        }
    )

    for subject in subjects:

        records = [
            record
            for record in performance_records
            if record["subject"] == subject
        ]

        if not records:
            continue

        highest = max(
            float(record["marks"])
            for record in records
        )

        print(
            f"\nSubject: {subject}"
        )

        print(
            f"Highest Marks: {highest:.2f}"
        )

        top_records = [
            record
            for record in records
            if float(record["marks"]) == highest
        ]

        for record in top_records:

            student = find_student(
                record["student_id"]
            )

            if student is not None:

                print(
                    f"Student: {student['name']} "
                    f"({student['student_id']})"
                )


def grade_distribution() -> None:

    print(
        "\n========== GRADE DISTRIBUTION =========="
    )

    distribution: Dict[str, int] = {
        "A+": 0,
        "A": 0,
        "B": 0,
        "C": 0,
        "D": 0,
        "F": 0
    }

    students_with_marks = 0

    for student in students:

        records = [
            record
            for record in performance_records
            if record["student_id"]
            == student["student_id"]
        ]

        if records:

            total = sum(
                float(record["marks"])
                for record in records
            )

            average = (
                total
                / float(len(records))
            )

            grade = calculate_grade(
                average
            )

            distribution[grade] += 1

            students_with_marks += 1

    if students_with_marks == 0:

        print(
            "No performance records available."
        )

        return

    print(
        f"\n{'Grade':<10}"
        f"{'Students':<10}"
    )

    print("-" * 20)

    for grade, count in distribution.items():

        print(
            f"{grade:<10}"
            f"{count:<10}"
        )


def complete_student_report() -> None:

    print(
        "\n========== COMPLETE STUDENT REPORT =========="
    )

    student_id = input(
        "Enter Student ID: "
    ).strip()

    student = find_student(student_id)

    if student is None:

        print(
            "Student does not exist."
        )

        return

    # --------------------------------------------------------
    # STUDENT DETAILS
    # --------------------------------------------------------

    print(
        "\nSTUDENT DETAILS"
    )

    print("--------------------------------")

    print(
        "Student ID :",
        student["student_id"]
    )

    print(
        "Name       :",
        student["name"]
    )

    print(
        "Email      :",
        student["email"]
    )

    print(
        "Mobile     :",
        student["mobile"]
    )

    print(
        "Course     :",
        student["course"]
    )

    # --------------------------------------------------------
    # ATTENDANCE
    # --------------------------------------------------------

    attendance = [
        record
        for record in attendance_records
        if record["student_id"] == student_id
    ]

    present = sum(
        1
        for record in attendance
        if record["status"] == "Present"
    )

    absent = len(attendance) - present

    percentage = (
        calculate_attendance_percentage(
            student_id
        )
    )

    print(
        "\nATTENDANCE"
    )

    print("--------------------------------")

    print(
        "Total Classes :",
        len(attendance)
    )

    print(
        "Present       :",
        present
    )

    print(
        "Absent        :",
        absent
    )

    print(
        f"Percentage    : {percentage:.2f}%"
    )

    # --------------------------------------------------------
    # PERFORMANCE
    # --------------------------------------------------------

    records = [
        record
        for record in performance_records
        if record["student_id"] == student_id
    ]

    print(
        "\nPERFORMANCE"
    )

    print("--------------------------------")

    if not records:

        print(
            "No performance records available."
        )

        return

    total = 0.0

    for record in records:

        marks = float(
            record["marks"]
        )

        print(
            f"{record['subject']:<20}: "
            f"{marks:.2f}"
        )

        total += marks

    average = (
        total
        / float(len(records))
    )

    grade = calculate_grade(
        average
    )

    print("--------------------------------")

    print(
        f"Total   : {total:.2f}"
    )

    print(
        f"Average : {average:.2f}"
    )

    print(
        f"Grade   : {grade}"
    )


# ============================================================
# MENUS
# ============================================================

def student_menu() -> None:

    while True:

        print(
            "\n========== STUDENT MANAGEMENT =========="
        )

        print("1. Add Student")
        print("2. View Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Remove Student")
        print("6. Back")

        choice = input(
            "Enter Choice: "
        ).strip()

        if choice == "1":

            add_student()

        elif choice == "2":

            view_students()

        elif choice == "3":

            search_student()

        elif choice == "4":

            update_student()

        elif choice == "5":

            remove_student()

        elif choice == "6":

            break

        else:

            print(
                "Invalid choice."
            )


def attendance_menu() -> None:

    while True:

        print(
            "\n========== ATTENDANCE MANAGEMENT =========="
        )

        print("1. Record Attendance")
        print("2. View Student Attendance")
        print("3. Back")

        choice = input(
            "Enter Choice: "
        ).strip()

        if choice == "1":

            record_attendance()

        elif choice == "2":

            view_student_attendance()

        elif choice == "3":

            break

        else:

            print(
                "Invalid choice."
            )


def performance_menu() -> None:

    while True:

        print(
            "\n========== PERFORMANCE MANAGEMENT =========="
        )

        print("1. Add Marks")
        print("2. Update Marks")
        print("3. Student Performance Report")
        print("4. Back")

        choice = input(
            "Enter Choice: "
        ).strip()

        if choice == "1":

            add_marks()

        elif choice == "2":

            update_marks()

        elif choice == "3":

            student_performance_report()

        elif choice == "4":

            break

        else:

            print(
                "Invalid choice."
            )


def reports_menu() -> None:

    while True:

        print(
            "\n========== REPORTS =========="
        )

        print(
            "1. Student Attendance Percentage"
        )

        print(
            "2. Students Below Attendance Threshold"
        )

        print(
            "3. Subject-wise Performance"
        )

        print(
            "4. Student Average / Performance"
        )

        print(
            "5. Highest Marks"
        )

        print(
            "6. Grade Distribution"
        )

        print(
            "7. Complete Student Report"
        )

        print(
            "8. Back"
        )

        choice = input(
            "Enter Choice: "
        ).strip()

        if choice == "1":

            attendance_percentage_report()

        elif choice == "2":

            below_attendance_threshold()

        elif choice == "3":

            subject_wise_performance()

        elif choice == "4":

            student_performance_report()

        elif choice == "5":

            highest_marks_report()

        elif choice == "6":

            grade_distribution()

        elif choice == "7":

            complete_student_report()

        elif choice == "8":

            break

        else:

            print(
                "Invalid choice."
            )


# ============================================================
# MAIN PROGRAM
# ============================================================

def main() -> None:

    load_all_data()

    while True:

        print("\n")
        print("=" * 60)

        print(
            "      STUDENT ATTENDANCE & "
            "PERFORMANCE ANALYZER"
        )

        print("=" * 60)

        print(
            "1. Student Management"
        )

        print(
            "2. Attendance"
        )

        print(
            "3. Performance"
        )

        print(
            "4. Reports"
        )

        print(
            "5. Exit"
        )

        choice = input(
            "\nEnter Choice: "
        ).strip()

        if choice == "1":

            student_menu()

        elif choice == "2":

            attendance_menu()

        elif choice == "3":

            performance_menu()

        elif choice == "4":

            reports_menu()

        elif choice == "5":

            save_all_data()

            print(
                "\nData saved successfully."
            )

            print(
                "Thank you for using the system."
            )

            break

        else:

            print(
                "Invalid choice. "
                "Please select 1-5."
            )


# ============================================================
# START PROGRAM
# ============================================================

if __name__ == "__main__":
    main()