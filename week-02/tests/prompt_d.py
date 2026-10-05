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
    unittest.main()
