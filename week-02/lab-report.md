# Lab report — Practice #02: The Prompt Is an Engineering Input

**Name:Yelemes Meyirzhan**
**Group:*Monday 16-19*
**Date:*2026-09-19*

> Fill in every section. **Do not delete or renumber the headings** — the grading pass reads them
> by number. If something did not happen, write "did not happen" and why; an empty section and a
> fabricated one are graded the same way.

---

## 1. The frozen experiment

| | |
| --- | --- |
| AI assistant | Gemini |
| Exact model name | Gemini 3.6 Flash|
| Implementation language |	Python |
| Date of the runs |Prompt A 
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

Prompt B:
def analyze_marks(marks, pass_mark=50):
    if not isinstance(marks, (list, tuple)) or len(marks) == 0:
        raise ValueError("The marks input must be a non-empty sequence.")

    valid_marks = []
    for mark in marks:
        # Reject booleans (since bool is a subclass of int in Python)
        if isinstance(mark, bool) or not isinstance(mark, (int, float)):
            raise ValueError(f"Invalid non-numeric value found: {mark}")

        if not (0 <= mark <= 100):
            raise ValueError(f"Mark out of range [0, 100]: {mark}")

        valid_marks.append(float(mark))

    total_count = len(valid_marks)
    highest = max(valid_marks)
    lowest = min(valid_marks)
    average = sum(valid_marks) / total_count

    passed_count = sum(1 for mark in valid_marks if mark >= pass_mark)
    pass_rate = (passed_count / total_count) * 100

    return {
        "average": average,
        "highest": highest,
        "lowest": lowest,
        "pass_rate": pass_rate
    }

Prompt C
You are a Python developer. Implement analyze_marks(marks, pass_mark=50). Return
average, highest, lowest, and pass_rate in a dictionary. Accept marks from 0 to 100;
raise ValueError for an empty list, non-numeric values, or out-of-range values. Use
no external libraries. Return code plus a short explanation.

Example: analyze_marks([40, 60, 80], 50) → average 60, highest 80, lowest 40,
pass_rate 66.67. Include tests for: one mark, decimals, custom pass_mark, empty list,
text value, and marks below 0 or above 100. State any remaining assumptions before
the code.

Prompt D
def analyze_marks(marks: list, pass_mark: float = 50) -> dict:
    """Analyze student marks and return summary statistics.

    Raises ValueError for empty lists, non-numeric values (including booleans),
    or marks out of the range [0, 100].
    """
    if not isinstance(marks, list) or len(marks) == 0:
        raise ValueError("The marks parameter must be a non-empty list.")

    # Validate pass_mark
    if isinstance(pass_mark, bool) or not isinstance(pass_mark, (int, float)):
        raise ValueError("pass_mark must be a valid number.")
    if not (0 <= pass_mark <= 100):
        raise ValueError("pass_mark must be between 0 and 100.")

    # Validate marks
    for mark in marks:
        if isinstance(mark, bool) or not isinstance(mark, (int, float)):
            raise ValueError(f"Invalid mark value '{mark}'. Marks must be int or float.")
        if not (0 <= mark <= 100):
            raise ValueError(f"Mark {mark} is out of the valid range [0, 100].")

    total_marks = len(marks)
    avg_mark = sum(marks) / total_marks
    highest_mark = max(marks)
    lowest_mark = min(marks)

    passed_count = sum(1 for mark in marks if mark >= pass_mark)
    pass_rate = round((passed_count / total_marks) * 100, 2)

    return {
        "average": avg_mark,
        "highest": highest_mark,
        "lowest": lowest_mark,
        "pass_rate": pass_rate,
    }

# =====================================================================
# Unit Tests
# =====================================================================
import unittest

class TestAnalyzeMarks(unittest.TestCase):

    def test_single_mark(self):
        result = analyze_marks([75])
        expected = {"average": 75.0, "highest": 75, "lowest": 75, "pass_rate": 100.0}
        self.assertEqual(result, expected)

    def test_decimals(self):
        result = analyze_marks([49.5, 50], pass_mark=50)
        expected = {"average": 49.75, "highest": 50, "lowest": 49.5, "pass_rate": 50.0}
        self.assertEqual(result, expected)

    def test_custom_pass_mark(self):
        result = analyze_marks([60, 70, 80], pass_mark=75)
        expected = {"average": 70.0, "highest": 80, "lowest": 60, "pass_rate": 33.33}
        self.assertEqual(result, expected)

    def test_empty_list_raises_value_error(self):
        with self.assertRaises(ValueError):
            analyze_marks([])

    def test_text_value_raises_value_error(self):
        with self.assertRaises(ValueError):
            analyze_marks([50, "60", 70])

    def test_boolean_value_raises_value_error(self):
        with self.assertRaises(ValueError):
            analyze_marks([50, True, 70])

    def test_out_of_bounds_marks_raise_value_error(self):
        with self.assertRaises(ValueError):
            analyze_marks([-1, 50, 80])
        with self.assertRaises(ValueError):
            analyze_marks([50, 80, 101])

if __name__ == "__main__":
    unittest.main() |

**Non-Python students only** — paste your substituted Prompt B text here, so the substitution can
be checked:

```
(paste here, or write "n/a — used Python")
```

**Confirmations:**

- Each prompt was sent in a **fresh chat**: yes / no
- No follow-up questions were asked before Part 7: yes / no
- Every output was saved **before** any editing: yes / no

---

## 2. Prompt A — minimal

**Prompt sent** (should be exactly one sentence):

```

```

**Assumptions the AI made that I never gave it** — list them, one per line. A data format, a pass
threshold, a rounding rule, an input method, an invented feature all count.

1.
2.
3.

**Questions it should have asked and did not:**

1.
2.

**Is the function named `analyze_marks` with the required signature?** yes / no — if no, what is it
called:

**First impression before testing** (one sentence — you will compare this with section 6 later):

---

## 3. Prompt B — structured context

**Prompt sent** (paste it in full, including any substitutions):

```

```

**What B fixed compared to A:**

1.
2.

**What B still leaves open:**

1.
2.

---

## 4. Prompt C — examples and tests

**What I appended to Prompt B:**

```

```

**Tests the AI wrote for itself** — how many, and which situations do they cover?

| Situation | Covered by the AI's tests? |
| --- | --- |
| one mark | |
| decimals | |
| custom pass_mark | |
| empty list | |
| text value | |
| below 0 / above 100 | |

**Do the AI's own tests pass against the AI's own code?** yes / no

**Do they agree with the harness in section 6?** yes / no — if no, where do they disagree:

**Assumptions C stated explicitly before the code:**

---

## 5. Prompt D — my combined prompt

**The complete prompt I wrote** (one message, sent to a fresh chat):

```

```

**What I deliberately added that A, B and C did not have:**

1.
2.
3.

**The ambiguity I found in the specification, and how I resolved it inside Prompt D:**

---

## 6. Test results — the evidence

Six cases × four prompts. Verdicts are **PASS**, **FAIL** or **ERROR** only.

| # | Call | Required | A | B | C | D |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `analyze_marks([40, 60, 80], 50)` | avg 60 · high 80 · low 40 · rate 66.67 | | | | |
| 2 | `analyze_marks([100], 50)` | avg 100 · high 100 · low 100 · rate 100 | | | | |
| 3 | `analyze_marks([49.5, 50], 50)` | avg 49.75 · high 50 · low 49.5 · rate 50 | | | | |
| 4 | `analyze_marks([], 50)` | raises ValueError | | | | |
| 5 | `analyze_marks([40, "60"], 50)` | raises ValueError | | | | |
| 6 | `analyze_marks([-1, 50, 101], 50)` | raises ValueError | | | | |
| | **Totals** | | /6 | /6 | /6 | /6 |

**For every FAIL and ERROR above, one line: what was returned or raised instead.**

| Prompt | Case | What actually happened |
| --- | --- | --- |
| | | |
| | | |
| | | |

### Pasted terminal output — all four runs

> This is the part that makes the table above count. Paste the **whole** output, unedited,
> including the header lines. A table with nothing behind it is not accepted.

**Prompt A**

```

```

**Prompt B**

```

```

**Prompt C**

```

```

**Prompt D**

```

```

---

## 7. Scoring

0–2 per criterion, using the rubric in `README.md` Part 7.

| Criterion | A | B | C | D |
| --- | --- | --- | --- | --- |
| Correctness (cases passed) | | | | |
| Requirement coverage | | | | |
| Verifiability (tests) | | | | |
| Assumptions stated | | | | |
| Noise (2 = none) | | | | |
| **Total / 10** | | | | |

**Prompt length, in words:** A ____ · B ____ · C ____ · D ____

**Words added per point gained** — B over A, C over B, D over C. One line on what that ratio says:

---

## 8. Conclusion — 150–200 words

Answer in this order: (1) which prompt scored best, and whether it is the one you would actually
use at work; (2) which single addition bought the most correctness, naming the exact case that
changed verdict; (3) what was pure noise; (4) the ambiguity and your resolution.

Name test cases and real returned values. "More detailed prompts work better" scores zero.

```
(150–200 words)



```

**Word count:**

---

## 9. Two questions for the debrief

Written before class, answered in class.

1.
2.
