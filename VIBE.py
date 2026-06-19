from dataclasses import dataclass, field
from typing import List


@dataclass
class Student:
    student_id: str
    name: str
    scores: List[int] = field(default_factory=list)

    def add_score(self, score: int) -> None:
        if 0 <= score <= 100:
            self.scores.append(score)
        else:
            raise ValueError("Score must be between 0 and 100.")

    def average(self) -> float:
        if not self.scores:
            return 0.0
        return sum(self.scores) / len(self.scores)

    def letter_grade(self) -> str:
        avg = self.average()
        if avg >= 90:
            return "A"
        elif avg >= 80:
            return "B"
        elif avg >= 70:
            return "C"
        elif avg >= 60:
            return "D"
        else:
            return "F"


def display_menu() -> None:
    print("\n=== Student Record Manager ===")
    print("1. Add a student")
    print("2. Add a test score")
    print("3. View all students")
    print("4. View one student's details")
    print("5. Remove a student")
    print("6. Exit")


def get_valid_int(prompt: str, min_value: int = None, max_value: int = None) -> int:
    while True:
        try:
            value = int(input(prompt))
            if min_value is not None and value < min_value:
                print(f"Value must be at least {min_value}.")
                continue
            if max_value is not None and value > max_value:
                print(f"Value must be at most {max_value}.")
                continue
            return value
        except ValueError:
            print("Please enter a valid integer.")


def find_student(students: List[Student], student_id: str):
    for student in students:
        if student.student_id == student_id:
            return student
    return None


def main() -> None:
    students: List[Student] = []

    while True:
        display_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            student_id = input("Enter student ID: ").strip()
            name = input("Enter student name: ").strip()

            if find_student(students, student_id):
                print("A student with that ID already exists.")
                continue

            students.append(Student(student_id=student_id, name=name))
            print(f"Added {name} ({student_id}).")

        elif choice == "2":
            student_id = input("Enter student ID: ").strip()
            student = find_student(students, student_id)

            if student is None:
                print("Student not found.")
                continue

            score = get_valid_int("Enter test score (0-100): ", 0, 100)
            try:
                student.add_score(score)
                print(f"Added score {score} for {student.name}.")
            except ValueError as error:
                print(error)

        elif choice == "3":
            if not students:
                print("No students recorded yet.")
            else:
                print("\nStudent Records:")
                for student in students:
                    print(
                        f"ID: {student.student_id} | Name: {student.name} | "
                        f"Average: {student.average():.1f} | Grade: {student.letter_grade()}"
                    )

        elif choice == "4":
            student_id = input("Enter student ID: ").strip()
            student = find_student(students, student_id)
            if student is None:
                print("Student not found.")
            else:
                print(f"\nStudent ID: {student.student_id}")
                print(f"Name: {student.name}")
                print(f"Scores: {student.scores}")
                print(f"Average: {student.average():.1f}")
                print(f"Letter Grade: {student.letter_grade()}")

        elif choice == "5":
            student_id = input("Enter student ID to remove: ").strip()
            student = find_student(students, student_id)
            if student is None:
                print("Student not found.")
            else:
                students.remove(student)
                print(f"Removed {student.name}.")

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("Please enter a valid menu option.")


if __name__ == "__main__":
    main()
