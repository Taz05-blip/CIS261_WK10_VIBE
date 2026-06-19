from pathlib import Path
from typing import List

DATA_FILE = "student_grades.txt"


class Student:
    def __init__(self, name: str, id: str, test1: float, test2: float, test3: float):
        self.name = name
        self.id = id
        self.test1 = test1
        self.test2 = test2
        self.test3 = test3
        self.average = self._calculate_average()
        self.grade = self._calculate_grade()

    def _calculate_average(self) -> float:
        return (self.test1 + self.test2 + self.test3) / 3

    def _calculate_grade(self) -> str:
        if self.average >= 90:
            return "A"
        if self.average >= 80:
            return "B"
        if self.average >= 70:
            return "C"
        if self.average >= 60:
            return "D"
        return "F"


def display_menu() -> None:
    print("\n=== Student Grade Manager ===")
    print("1. Add student")
    print("2. Display all students")
    print("3. View one student")
    print("4. Search by name")
    print("5. Show class statistics")
    print("6. Edit student")
    print("7. Delete student")
    print("8. Save records")
    print("ESC. Exit")


def get_valid_score(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt))
            if 0 <= value <= 100:
                return value
            print("Score must be between 0 and 100.")
        except ValueError:
            print("Please enter a valid number.")


def get_valid_text(prompt: str) -> str:
    value = input(prompt).strip()
    while not value:
        print("This field cannot be empty.")
        value = input(prompt).strip()
    return value


def load_students() -> List[Student]:
    students: List[Student] = []
    file_path = Path(DATA_FILE)

    if not file_path.exists():
        print(f"No file found yet. A new file will be created as '{DATA_FILE}'.")
        return students

    try:
        with file_path.open("r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                text = line.strip()
                if not text:
                    continue
                parts = [part.strip() for part in text.split(",")]
                if len(parts) != 5:
                    print(f"Skipping invalid line {line_number} in {DATA_FILE}.")
                    continue
                student_id, name, test1, test2, test3 = parts
                try:
                    students.append(
                        Student(
                            name=name,
                            id=student_id,
                            test1=float(test1),
                            test2=float(test2),
                            test3=float(test3),
                        )
                    )
                except ValueError:
                    print(f"Skipping invalid score data on line {line_number}.")
    except OSError as error:
        print(f"Error reading file: {error}")

    return students


def save_students(students: List[Student]) -> None:
    try:
        with Path(DATA_FILE).open("w", encoding="utf-8") as file:
            for student in students:
                file.write(
                    f"{student.id},{student.name},{student.test1:.2f},{student.test2:.2f},{student.test3:.2f}\n"
                )
        print(f"Records saved successfully to {DATA_FILE}.")
    except OSError as error:
        print(f"Error saving file: {error}")


def find_student(students: List[Student], student_id: str):
    for student in students:
        if student.id == student_id:
            return student
    return None


def display_student_table(students: List[Student]) -> None:
    if not students:
        print("No students found.")
        return

    print("\nStudent Records")
    print(
        f"{'ID':<10} {'Name':<15} {'Test 1':>8} {'Test 2':>8} {'Test 3':>8} {'Avg':>8} {'Grade':>6}"
    )
    print("-" * 76)
    for student in students:
        print(
            f"{student.id:<10} {student.name:<15} "
            f"{student.test1:>8.2f} {student.test2:>8.2f} {student.test3:>8.2f} "
            f"{student.average:>8.2f} {student.grade:>6}"
        )


def display_class_statistics(students: List[Student]) -> None:
    if not students:
        print("No students found.")
        return

    averages = [student.average for student in students]
    highest = max(averages)
    lowest = min(averages)
    class_average = sum(averages) / len(averages)

    print("\nClass Statistics")
    print(f"Highest average: {highest:.2f}")
    print(f"Lowest average:  {lowest:.2f}")
    print(f"Class average:   {class_average:.2f}")


def search_by_name(students: List[Student], query: str) -> List[Student]:
    return [student for student in students if query.lower() in student.name.lower()]


def edit_student(students: List[Student]) -> None:
    student_id = get_valid_text("Enter student ID to edit: ")
    student = find_student(students, student_id)

    if student is None:
        print("Student not found.")
        return

    print(f"Editing student: {student.name} ({student.id})")
    student.name = get_valid_text("New name: ")
    student.test1 = get_valid_score("New Test 1: ")
    student.test2 = get_valid_score("New Test 2: ")
    student.test3 = get_valid_score("New Test 3: ")
    student.average = student._calculate_average()
    student.grade = student._calculate_grade()
    print("Student updated successfully.")


def delete_student(students: List[Student]) -> None:
    student_id = get_valid_text("Enter student ID to delete: ")
    student = find_student(students, student_id)

    if student is None:
        print("Student not found.")
        return

    students.remove(student)
    print(f"Deleted {student.name} ({student.id}).")


def view_student(students: List[Student]) -> None:
    student_id = get_valid_text("Enter student ID to view: ")
    student = find_student(students, student_id)

    if student is None:
        print("Student not found.")
        return

    print("\nStudent Details")
    print(f"ID: {student.id}")
    print(f"Name: {student.name}")
    print(f"Test 1: {student.test1:.2f}")
    print(f"Test 2: {student.test2:.2f}")
    print(f"Test 3: {student.test3:.2f}")
    print(f"Average: {student.average:.2f}")
    print(f"Grade: {student.grade}")


def main() -> None:
    students = load_students()
    if students:
        print(f"Loaded {len(students)} student records from {DATA_FILE}.")
    else:
        print(f"No records loaded from {DATA_FILE}.")

    while True:
        display_menu()
        choice = input("Choose an option: ").strip()

        if choice == "\x1b" or choice.upper() == "ESC":
            print("Goodbye!")
            break

        elif choice == "1":
            student_id = get_valid_text("Enter student ID: ")
            name = get_valid_text("Enter student name: ")

            if find_student(students, student_id):
                print("A student with that ID already exists.")
                continue

            print("Enter scores from 0 to 100:")
            test1 = get_valid_score("Test 1: ")
            test2 = get_valid_score("Test 2: ")
            test3 = get_valid_score("Test 3: ")

            students.append(
                Student(
                    name=name,
                    id=student_id,
                    test1=test1,
                    test2=test2,
                    test3=test3,
                )
            )
            save_students(students)
            print(f"Added {name} ({student_id}) and saved the record.")

        elif choice == "2":
            display_student_table(students)

        elif choice == "3":
            view_student(students)

        elif choice == "4":
            query = get_valid_text("Enter student name to search: ")
            results = search_by_name(students, query)
            if results:
                display_student_table(results)
            else:
                print("No matching students found.")

        elif choice == "5":
            display_class_statistics(students)

        elif choice == "6":
            edit_student(students)
            save_students(students)

        elif choice == "7":
            delete_student(students)
            save_students(students)

        elif choice == "8":
            save_students(students)

        else:
            print("Please enter a valid option.")


if __name__ == "__main__":
    main()
