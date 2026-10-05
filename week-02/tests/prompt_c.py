def analyze_marks(marks, pass_mark=50):
    """
    Analyzes a list of student marks and returns statistics.
    
    :param marks: List of numeric values between 0 and 100 inclusive.
    :param pass_mark: Threshold value for a passing mark (default: 50).
    :return: Dictionary containing 'average', 'highest', 'lowest', and 'pass_rate'.
    :raises ValueError: If marks is empty, contains non-numeric values, 
                        or values are out of [0, 100].
    """
    if not isinstance(marks, (list, tuple)):
        raise ValueError("Marks must be a list or tuple of numbers.")

    if len(marks) == 0:
        raise ValueError("Marks list cannot be empty.")

    # Validate pass_mark type and range
    if isinstance(pass_mark, bool) or not isinstance(pass_mark, (int, float)):
        raise ValueError("Pass mark must be a numeric value.")
    if not (0 <= pass_mark <= 100):
        raise ValueError("Pass mark must be between 0 and 100.")

    validated_marks = []
    for mark in marks:
        # Reject booleans (since bool inherits from int in Python)
        if isinstance(mark, bool) or not isinstance(mark, (int, float)):
            raise ValueError(f"Non-numeric value found: {mark}")

        if not (0 <= mark <= 100):
            raise ValueError(f"Mark out of range [0, 100]: {mark}")

        validated_marks.append(float(mark))

    total = sum(validated_marks)
    count = len(validated_marks)
    highest = max(validated_marks)
    lowest = min(validated_marks)

    passed_count = sum(1 for mark in validated_marks if mark >= pass_mark)
    pass_rate = (passed_count / count) * 100

    return {
        "average": round(total / count, 2),
        "highest": highest if highest % 1 != 0 else int(highest),
        "lowest": lowest if lowest % 1 != 0 else int(lowest),
        "pass_rate": round(pass_rate, 2),
    }


# =====================================================================
# Unit Tests
# =====================================================================

def run_tests():
    # 1. Standard Case (from prompt example)
    res = analyze_marks([40, 60, 80], 50)
    assert res == {"average": 60.0, "highest": 80, "lowest": 40, "pass_rate": 66.67}, f"Failed standard case: {res}"

    # 2. Single Mark
    res = analyze_marks([75], 50)
    assert res == {"average": 75.0, "highest": 75, "lowest": 75, "pass_rate": 100.0}, f"Failed single mark test: {res}"

    # 3. Decimals
    res = analyze_marks([45.5, 62.3, 88.8], 50)
    assert res == {"average": 65.53, "highest": 88.8, "lowest": 45.5, "pass_rate": 66.67}, f"Failed decimal mark test: {res}"

    # 4. Custom Pass Mark
    res = analyze_marks([40, 60, 80], pass_mark=70)
    assert res == {"average": 60.0, "highest": 80, "lowest": 40, "pass_rate": 33.33}, f"Failed custom pass_mark test: {res}"

    # 5. Empty List (should raise ValueError)
    try:
        analyze_marks([], 50)
        assert False, "Expected ValueError for empty list"
    except ValueError as e:
        assert str(e) == "Marks list cannot be empty."

    # 6. Text Value (should raise ValueError)
    try:
        analyze_marks([50, "eighty", 90], 50)
        assert False, "Expected ValueError for text value"
    except ValueError as e:
        assert "Non-numeric value found" in str(e)

    # 7. Marks Below 0 (should raise ValueError)
    try:
        analyze_marks([-5, 50, 70], 50)
        assert False, "Expected ValueError for negative mark"
    except ValueError as e:
        assert "Mark out of range" in str(e)

    # 8. Marks Above 100 (should raise ValueError)
    try:
        analyze_marks([50, 70, 105], 50)
        assert False, "Expected ValueError for mark > 100"
    except ValueError as e:
        assert "Mark out of range" in str(e)

    print("All tests passed successfully!")


if __name__ == "__main__":
    run_tests()
