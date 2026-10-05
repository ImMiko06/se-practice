# Rocket (rocket.new) — prompt log

## Prompt 1 — exact, verbatim, as given in week-01/README.md

Build a small program that processes a list of student marks and prints:
average, highest, lowest, and pass rate.


## Rocket's prompt-completeness score and question

Agent detected prompt score: **69%** — "good enough to proceed", but Rocket offered to improve it
with one question before building.

**Question Rocket asked:**
> Who will be using this tool?
> Options: Just me / Teachers or lecturers / School admin team / Students can view results / Other

**My answer:** Just me (a personal tool only I use to process marks)

## Rocket's rewritten ("enhanced") prompt

Final prompt score after my answer: **87%**

A student marks processing tool for teachers and lecturers to input or upload a list of
student marks and instantly view key statistics — average score, highest mark, lowest mark,
and pass rate. Designed as a clean, focused internal tool for individual educators to quickly
analyze class performance.

Building with Next.js and TypeScript.


**Note:** I answered "Just me" to the audience question, but Rocket's rewritten prompt still says
"for teachers and lecturers" — it did not actually follow my answer. It also added a tech stack
(Next.js + TypeScript) that was never mentioned anywhere in my original one-line prompt.

## What Rocket built (unprompted additions)

From the "What I did" summary after building (17 files generated):

- A full web app ("MarksProcessor") with manual entry form AND CSV upload/paste, not just a
  simple list-in-list-out program
- Student **names** required per mark (the spec only asked for a list of marks, no names)
- Live-recalculating stat cards: average, highest, lowest, pass rate, total students, **and grade
  breakdown** (none of this was asked for)
- A **configurable pass-threshold slider** (spec fixes the threshold at >= 50; this makes it a
  variable the user can change, which is a different feature than asked for)
- A **grade distribution bar chart** (A/B/C/D/F bands) — not requested
- A **pass/fail donut chart** — not requested
- Median score and standard deviation — not requested, not in spec
- A sortable, searchable student table with CSV export and a "Clear All" modal — not requested
- A CSV template download feature — not requested

## Testing against the 4 spec cases

### Case A — `85, 23, 45, 90, 92` (via CSV paste: S1,85 / S2,23 / S3,45 / S4,90 / S5,92)
- Expected: avg 67.00, high 92, low 23, pass 60.0%
- Got: avg 67.00, high 92, low 23, pass 60.0%
- **Match: yes**

### Case B — `88, 47, -5, 101, abc, 73, 50, , 100` (via CSV paste)
- Expected: avg 71.60, high 100, low 47, pass 80.0% (5 valid marks)
- Got (first run, before fix): avg 71.60, high 100, low 47, pass 80.0% (5 valid) — correct
- Got (re-run, after fix): same correct numbers, but the skipped-row counter said
  "5 invalid rows skipped" when only 4 rows were actually invalid (-5, 101, abc, empty) — an
  off-by-one in the reporting message, though the statistics themselves stayed correct
- **Match: yes, with a minor counting bug in the skip message**

### Case C — `10, 20, 30` (via CSV paste)
- Expected: avg 20.00, high 30, low 10, pass 0.0%
- Got: avg 20.00, high 30, low 10, pass 0.0%
- **Match: yes**

### Case D — `abc, , xyz` (via CSV paste)
- Expected: no valid marks, clear message, no crash
- Got **before** the fix: upload was **rejected entirely** with the error
  `Could not parse file: Row 1: invalid score "abc" for S1` — nothing was imported, and the whole
  batch failed because of one bad row instead of skipping just that row
- **Match before fix: NO — this is the defect**

### Manual-entry form behaviour (separate from CSV path)
Tested by hand through the "Add Student Mark" form:
- `-5` → blocked at input time: "Score cannot be below 0"
- `101` → blocked at input time: "Score cannot exceed 100"
- empty score → blocked at input time: "Score is required"
- These are **not crashes**, but they are a different behaviour than the spec: the spec wants
  invalid values silently ignored while processing a list, not blocked at the point of entry.
  This is a reasonable UX choice for a form, but it is not what was asked for, and it would not
  work at all for a bulk/list-style input the way the original prompt implied.

## The defect and the fix

**Defect:** On CSV upload/paste, a single invalid row (non-numeric, empty, or out of 0–100 range)
caused the **entire import to fail**, with zero rows processed — this is the file-level version of
"the program crashes on bad input," even though no error page was shown.

**Follow-up prompt I used:**