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
