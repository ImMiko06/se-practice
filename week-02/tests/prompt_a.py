from typing import Dict, List, Any

# Sample Dataset: Student Name -> Dict of Subject Marks
STUDENT_DATA = {
    "Alice": {"Math": 88, "Science": 92, "English": 85, "History": 78},
    "Bob": {"Math": 75, "Science": 65, "English": 70, "History": 80},
    "Charlie": {"Math": 95, "Science": 98, "English": 90, "History": 92},
    "Diana": {"Math": 58, "Science": 62, "English": 68, "History": 55},
    "Ethan": {"Math": 82, "Science": 88, "English": 84, "History": 86},
}

def calculate_grade(percentage: float) -> str:
    """Returns a letter grade based on percentage."""
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 50:
        return "D"
    else:
        return "F"

def analyze_student_marks(data: Dict[str, Dict[str, int]]) -> Dict[str, Any]:
    """Analyzes overall class performance and individual metrics."""
    student_summaries = {}
    total_class_marks = 0
    total_subjects_count = 0
    subject_totals: Dict[str, List[int]] = {}

    # Process individual student metrics
    for student, marks in data.items():
        total_marks = sum(marks.values())
        num_subjects = len(marks)
        average = total_marks / num_subjects
        grade = calculate_grade(average)

        student_summaries[student] = {
            "Total": total_marks,
            "Average": round(average, 2),
            "Grade": grade
        }

        # Aggregate class data
        total_class_marks += total_marks
        total_subjects_count += num_subjects

        for subject, score in marks.items():
            subject_totals.setdefault(subject, []).append(score)

    # Class-wide calculations
    class_average = round(total_class_marks / total_subjects_count, 2)
    
    # Identify top and lowest performer
    top_student = max(student_summaries, key=lambda s: student_summaries[s]["Total"])
    lowest_student = min(student_summaries, key=lambda s: student_summaries[s]["Total"])

    # Subject averages
    subject_averages = {
        subject: round(sum(scores) / len(scores), 2)
        for subject, scores in subject_totals.items()
    }

    return {
        "student_summaries": student_summaries,
        "class_average": class_average,
        "top_student": (top_student, student_summaries[top_student]["Total"]),
        "lowest_student": (lowest_student, student_summaries[lowest_student]["Total"]),
        "subject_averages": subject_averages,
    }

def print_report(results: Dict[str, Any]) -> None:
    """Displays formatted results in the console."""
    print("=" * 45)
    print("         STUDENT MARKS ANALYSIS REPORT       ")
    print("=" * 45)

    print("\n--- Individual Performance ---")
    print(f"{'Name':<12} | {'Total':<6} | {'Average':<8} | {'Grade':<5}")
    print("-" * 42)
    for name, stats in results["student_summaries"].items():
        print(f"{name:<12} | {stats['Total']:<6} | {stats['Average']:<8.2f} | {stats['Grade']:<5}")

    print("\n--- Class Highlights ---")
    print(f"Overall Class Average : {results['class_average']}%")
    print(f"Top Performer         : {results['top_student'][0]} ({results['top_student'][1]} marks)")
    print(f"Lowest Performer      : {results['lowest_student'][0]} ({results['lowest_student'][1]} marks)")

    print("\n--- Subject Averages ---")
    for subject, avg in results["subject_averages"].items():
        print(f"{subject:<10} : {avg}%")
    print("=" * 45)

if __name__ == "__main__":
    results = analyze_student_marks(STUDENT_DATA)
    print_report(results)
