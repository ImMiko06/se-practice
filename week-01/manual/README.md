# Manual solution — student marks statistics

Python 3, standard library only, no AI assistance.

## How to run

```bash
python marks.py
```

Edit the `marks` list at the bottom of `marks.py` to try different input.

## How to verify against all 4 spec test cases

```bash
python test_cases.py
```

Expected output: `4/4 cases passed`.

## Design notes

- `parse_marks()` filters the raw input down to valid marks only (numbers in 0–100
  inclusive). Text, empty strings, negative numbers and anything above 100 are
  silently skipped — never crashes the program.
- `compute_stats()` assumes the list it receives is non-empty; the caller
  (`print_report`) checks for the empty case first and prints a message instead of
  calling it, so there is no division by zero.
- Pass threshold is `>= 50` as specified.