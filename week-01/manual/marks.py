"""
Student marks statistics — Week 01, Part 1 (manual, no AI).

Takes a list of student marks and prints:
  - number of valid marks
  - average (2 decimals)
  - highest and lowest
  - pass rate (1 decimal)

Rules:
  - a valid mark is a number from 0 to 100 inclusive; anything else
    (text, empty, negative, > 100) is ignored and must not crash the program
  - a mark passes if it is >= 50
  - if there are no valid marks, print a clear message instead of statistics
"""


def parse_marks(raw_marks):
    """Take a list of raw values (numbers or strings) and return only the
    valid marks: numbers in the inclusive range 0..100. Anything that is
    not a number, or is out of range, is silently skipped."""
    valid = []
    for item in raw_marks:
        # Normalize: strip whitespace if it's a string
        if isinstance(item, str):
            item = item.strip()
            if item == "":
                continue  # empty value, skip

        try:
            value = float(item)
        except (ValueError, TypeError):
            continue  # not a number at all (e.g. "abc"), skip

        if 0 <= value <= 100:
            valid.append(value)
        # else: out of range (-5, 101, ...), skip

    return valid


def compute_stats(valid_marks):
    """Given a list of valid marks, return a dict with count, average,
    highest, lowest and pass_rate. Caller must ensure the list is non-empty."""
    count = len(valid_marks)
    average = sum(valid_marks) / count
    highest = max(valid_marks)
    lowest = min(valid_marks)
    passing = [m for m in valid_marks if m >= 50]
    pass_rate = (len(passing) / count) * 100

    return {
        "count": count,
        "average": average,
        "highest": highest,
        "lowest": lowest,
        "pass_rate": pass_rate,
    }


def format_mark(value):
    """Print whole numbers without a trailing .0, matching how marks are
    normally written (92, not 92.0)."""
    if value == int(value):
        return str(int(value))
    return str(value)


def print_report(raw_marks):
    valid = parse_marks(raw_marks)

    if not valid:
        print("No valid marks were provided — nothing to report.")
        return

    stats = compute_stats(valid)

    print(f"Valid marks: {stats['count']}")
    print(f"Average: {stats['average']:.2f}")
    print(f"Highest: {format_mark(stats['highest'])}")
    print(f"Lowest: {format_mark(stats['lowest'])}")
    print(f"Pass rate: {stats['pass_rate']:.1f}%")


if __name__ == "__main__":
    # ---- Change this list to test different inputs ----
    marks = [85, 23, 45, 90, 92]
    print_report(marks)