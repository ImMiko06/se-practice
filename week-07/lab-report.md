# Week 07 — Lab report

**Name:** Yelemes Meyirzhan  
**Group:** not supplied  
**Date:** 5 November 2026

Fill in every section. Do not delete, rename or renumber the headings.

---

## 1. Setup

| | |
| --- | --- |
| Project I continue (week-06 or starter) | starter; no Week 06 checkout/export was present |
| Bolt project link (or not shared, and why) | not shared; used provided starter |
| Assistant that generated the tests (tool) | Codex desktop assistant |
| Exact model | not displayed in the UI |
| Where I ran the tests | my computer, Windows PowerShell |
| Vitest version | 2.1.9 |
| Test command | npx vitest run |

---

## 2. Task 1 — baseline and the booking function

**Before editing:** where did the booking decision live in the project you started from?

| | |
| --- | --- |
| File and function | app/src/App.tsx, inside check() |
| Its inputs | start/end/current time in minutes, blocked flag, selected room bookings |
| What it returned | a boolean stored in result state |
| How the page used it | check() set result; the JSX rendered Available or Unavailable |

**What I changed to extract canBook.**

I moved the range, after-now, duration, blocked-room and overlap decisions from check() in app/src/App.tsx into app/src/booking.ts as canBook. The conditions and order match the starter, including the strict overlap comparisons that allow touching endpoints. The page still converts times and handles validation messages, then passes minutes, the blocked flag and the selected room's booking array to canBook. It uses that returned boolean for the same result state, so this extraction did not intentionally change the starter's decision.

---

## 3. Task 2 — the test plan

| ID | Candidate / changed input | Expected | AC | Reason |
| --- | --- | --- | --- | --- |
| T01 | 660–720 (touching after) | true | AC4 | It starts exactly as the saved booking ends; the intervals do not overlap. |
| T02 | 540–570 (starts now) | false | AC1 | Start must be strictly later than now. |
| T03 | 720–720 (zero duration) | false | AC1 | A valid interval requires start less than end. |
| T04 | 750–720 (reversed) | false | AC1 | The start is after the end. |
| T05 | 1380–1441 (past day end) | false | AC1 | 1441 exceeds the maximum end minute, 1440. |
| T06 | 720–840 (120 minutes) | true | AC2 | Exactly 120 is allowed; only longer durations are rejected. |
| T07 | 720–841 (121 minutes) | false | AC2 | The duration exceeds the limit by one minute. |
| T08 | 570–600 (touching before) | true | AC4 | It ends exactly when the saved booking starts; touching is allowed. |
| T09 | 630–690 (partial overlap) | false | AC4 | The request and booking share the minutes from 630 to 660. |
| T10 | 570–690 (contains booking) | false | AC4 | The request contains the full 600–660 booking. |
| T11 | 615–645 (inside booking) | false | AC4 | The request lies within the saved booking. |
| T12 | 600–660 (identical interval) | false | AC4 | The requested time is already booked. |
| T13 | 660–720, blocked = true | false | AC3 | A blocked room rejects the request regardless of free time. |
| T14 | 630–690, bookings = [] | true | AC4 | There are no intervals to overlap and the remaining rules pass. |
| AC5 | 660–720 and compare a copy of bookings | true, unchanged | AC5 | The available call must preserve the existing booking list. |
| X1 | 1420–1440, bookings = [] | true | AC1 | End minute 1440 is allowed; this 20-minute request is after now. |
| X2 | 720–750; bookings 600–660 and 750–780 | true | AC4 | It touches the second booking at 750 but shares no interval with either. |

---

## 4. Task 3 — the generation prompt and the first suite

**The prompt exactly as I sent it.** The suite was generated in this Codex conversation; the course's fresh-chat step was not used. Prompt template:

```text
Generate tests for the existing booking function using Vitest. Use AC1–AC6 and the reviewed case table below.

Import the real function used by the page. Keep its code unchanged. Use fixed time and fresh fixtures. Assert exact decisions and unchanged booking data.

Return the test file, run command, and AC mapping. Flag unclear requirements. We will run the tests ourselves.

Case table: T01 true AC4; T02 false AC1; T03 false AC1; T04 false AC1; T05 false AC1; T06 true AC2; T07 false AC2; T08 true AC4; T09 false AC4; T10 false AC4; T11 false AC4; T12 false AC4; T13 false AC3; T14 true AC4; AC5 available request true with unchanged data; X1 1420–1440 true AC1; X2 720–750 touching a second booking true AC4.
```

The assistant's answer: run command, AC mapping and unclear requirements, pasted here:

```text
Run command: npx vitest run src/booking.test.ts.
AC mapping: T01, T08–T12 and T14 → AC4; T02–T05 → AC1; T06–T07 → AC2; T13 → AC3; unchanged data → AC5; X1 and X2 → their listed ACs.
Unclear requirement: no AC specifies how an invalid existing booking should be handled. T06 in the generated first suite expects false; review that boundary against AC2 before accepting it.
```

The first suite was saved to suites/first/ before changes: yes.

---

## 5. Task 4 — review of the first suite

| # | Test or part | What is weak or wrong | Decision | AC or reason |
| --- | --- | --- | --- | --- |
| 1 | T06 expected value | It says exactly 120 minutes is unavailable. | revise | AC2 rejects only durations greater than 120; equality is allowed. |
| 2 | Import and fixtures | It imports the real module and creates fresh bookings per call; no mock, clock, skip, focus or duplicate case. | accept | It tests the same function used by the page with fixed inputs. |
| 3 | AC5 | It compares booking data before and after an available call. | accept | AC5 requires the existing data to remain unchanged. |

---

## 6. Task 5 — running, diagnosing, improving

### 6.1 The first run

```text
 RUN  v2.1.9 C:/Users/Acer Nitro V15/se-practice/week-07/app

 ❯ src/booking.test.ts (17 tests | 1 failed) 26ms
   × assistant first suite: booking decisions > T06 AC2 exactly 120 minutes is unavailable
     → expected true to be false // Object.is equality

 Test Files  1 failed (1)
      Tests  1 failed | 16 passed (17)
   Start at  03:05:23
   Duration  1.15s
```

| Failing test | Observed failure | First check | Test repair or implementation fix? | Action taken |
| --- | --- | --- | --- | --- |
| T06 | Expected false, received true for 720–840. | Compare duration with AC2. | Test repair | Changed expectation to true; 120 equals the limit and is allowed. |

### 6.2 The improvement prompt

```text
Review this test suite against AC1–AC6 and our case table. Identify incorrect expectations, weak assertions, duplicated cases, and missing boundaries.

For each proposed change, explain the requirement and the defect it could detect. Improve the tests without changing correct expectations to match buggy behavior.

Use the actual failure output below. Separate test repairs from implementation fixes.

Actual output: first run produced one assertion mismatch: T06 expected false but received true for 720–840. The suite had 17 tests, 16 passed and 1 failed. AC2 rejects durations longer than 120 minutes, so exactly 120 minutes should be true.
```

Assistant answer: revise T06 from false to true because AC2 permits the inclusive 120-minute boundary; keep implementation unchanged. Keep exact boolean assertions and the real booking import. The suite already has fresh fixtures, an AC5 data-preservation comparison and two extra cases. M1 should be caught by T06, M2 by T01/T08, and M3 by T13. Derive expected values from the criteria.

### 6.3 The final run

```text
 RUN  v2.1.9 C:/Users/Acer Nitro V15/se-practice/week-07/app

 ✓ src/booking.test.ts (17 tests) 15ms

 Test Files  1 passed (1)
      Tests  17 passed (17)
   Start at  03:08:01
   Duration  1.80s
```

---

## 7. Task 6 — deliberate defects

| Trial | Intentional change | Detected / Survived | Failing test IDs | If it survived |
| --- | --- | --- | --- | --- |
| M1 | Reject duration >= 120 instead of > 120 | Detected | T06 | n/a |
| M2 | Treat touching endpoints as overlap | Detected | T01, T08, AC5, X2 | n/a |
| M3 | Remove blocked-room rejection | Detected | T13 | n/a |

```text
M1 — RUN v2.1.9; T06 AC2 exactly 120 minutes is available failed (expected true, received false).
      Tests 1 failed | 16 passed (17)

M2 — RUN v2.1.9; T01 AC4 touching after is available; T08 AC4 touching before is available;
      AC5 an available request does not alter bookings; X2 AC4 touching a second booking is allowed failed.
      Tests 4 failed | 13 passed (17)

M3 — RUN v2.1.9; T13 AC3 blocked room is unavailable failed (expected false, received true).
      Tests 1 failed | 16 passed (17)
```

All three changes reverted, then the full suite was run again: yes.

---

## 8. Task 7 — manual UI checks

| # | Action | Expected | AC | What I observed | Result |
| --- | --- | --- | --- | --- | --- |
| U1 | Check 11:00–12:00, unblocked | Available and sample booking shown | AC5 | Available appeared and the 10:00–11:00 booking remained visible; saved as evidence/ui-1.jpg. | Pass |
| U2 | Enable blocked and check again | Unavailable replaces earlier result | AC3, AC5 | Available changed to Unavailable; saved as evidence/ui-2.jpg. | Pass |
| U3 | Clear a required input and submit | Understandable validation feedback | AC6 | The empty native time control reverted to 11:00 on submit, so the missing-input branch could not be reached. The blank field before submit is shown in evidence/ui-3.jpg. | Not testable |
| U4 | Use phone width | Controls and result remain usable | AC6 | At 375 × 812, fields stacked vertically and the result and booking list remained readable; saved as evidence/ui-4.jpg. | Pass |
| U5 | Repeat checks on same data | Existing bookings unchanged | AC5 | Rechecked with start 11:15; the 10:00–11:00 booking remained unchanged; saved as evidence/ui-5.jpg. | Pass |

---

## 9. Comparison and what still fails

### 9.1 Checks I am keeping as FAIL or ERROR

| Check | Why it stays |
| --- | --- |
| none | All five screenshots are present. U3 remains Not testable in section 8 because the browser time control reverted before submission. |

### 9.2 Original and improved suites

| Measure | First suite | Improved suite |
| --- | --- | --- |
| Executed / passed / failed | 17 / 16 / 1 | 17 / 17 / 0 |
| Requirements with meaningful tests | AC1–AC5 and X1/X2; T06 expected value was wrong; AC6 is manual. | AC1–AC5 and X1/X2; AC6 is manual and empty-input feedback was not testable. |
| Selected mutants detected | Not run against failing first suite. | M1, M2 and M3 detected. |
| Accepted / revised / rejected tests | Accepted real import and fixed fixtures; revised T06; rejected its incorrect expectation. | All 17 cases assert exact outcomes and include AC5 data preservation. |
| Remaining limitations | T06 could have legitimized a wrong implementation. | Missing-input feedback could not be reached through this browser's time control; reversed existing-booking behavior has no AC. |

### 9.3 What no AC decides

I called canBook with start 660, end 720, now 540, blocked false, and bookings [{start:700,end:650}]. It returned true. No AC defines how an invalid existing interval should be handled. The overlap predicate sees no overlap because that interval ends before it starts. I declare returns-true and would document the policy if malformed bookings were possible in the real project.

---

## 10. Conclusion (120–180 words)

The first suite's important mistake was T06: it expected a booking of exactly 120 minutes to be rejected. AC2 says only a duration longer than 120 minutes is rejected. The first run failed on that case, and checking the expected value against AC2 showed the test was wrong while canBook was right. I changed the test, not the implementation. The final run proves that the 17 named cases pass for the code that was run, including the tested time boundaries, overlaps, blocked state and unchanged booking list. It does not prove every possible booking input is correct, or that the page's feedback is clear in every browser. The defect trials provide evidence for three specific faults: the suite caught the duration cutoff, endpoint overlap and missing blocked-room check. The five screenshots show the states I inspected, including a portrait 375-pixel view. One manual limitation remains: this browser's time control reverted an empty field before submit, so I could not verify missing-input feedback. Behavior for malformed existing bookings is also unspecified by the criteria.
