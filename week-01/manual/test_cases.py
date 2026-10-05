"""
Runs all 4 test cases from week-01/README.md against marks.py and checks
the output matches the spec exactly. Run with: python test_cases.py
"""

from marks import parse_marks, compute_stats


def check(name, raw_marks, expected):
    valid = parse_marks(raw_marks)

    if expected is None:
        ok = (len(valid) == 0)
        status = "PASS" if ok else "FAIL"
        print(f"[{status}] {name}: expected no valid marks, got {len(valid)}")
        return ok

    stats = compute_stats(valid)
    ok = (
        stats["count"] == expected["count"]
        and round(stats["average"], 2) == expected["average"]
        and stats["highest"] == expected["highest"]
        and stats["lowest"] == expected["lowest"]
        and round(stats["pass_rate"], 1) == expected["pass_rate"]
    )
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}: {stats}")
    return ok


results = []

results.append(check(
    "Case A",
    [85, 23, 45, 90, 92],
    {"count": 5, "average": 67.00, "highest": 92, "lowest": 23, "pass_rate": 60.0},
))

results.append(check(
    "Case B",
    [88, 47, -5, 101, "abc", 73, 50, "", 100],
    {"count": 5, "average": 71.60, "highest": 100, "lowest": 47, "pass_rate": 80.0},
))

results.append(check(
    "Case C",
    [10, 20, 30],
    {"count": 3, "average": 20.00, "highest": 30, "lowest": 10, "pass_rate": 0.0},
))

results.append(check(
    "Case D",
    ["abc", "", "xyz"],
    None,  # no valid marks -> expect the "no valid marks" message path
))

print()
print(f"{sum(results)}/{len(results)} cases passed")