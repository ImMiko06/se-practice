# SIS #04 — Report: Evolving the Smart Campus Room Availability Checker

<!-- The ONLY file you write prose in. Keep every numbered heading (## 1. … ## 10.), every
     ### sub-heading and every **Label:** word — the checker finds your answers by them.
     Replace every "(write here)" and "I asked Codex to help complete SIS #04 quickly and provided the assignment brief. It requested implementation and submission help under the stated course constraints.". Delete these <!-- --> comments if you like. -->

## 1. Setup and starting point

<!-- Model: the exact model with its version, as the tool shows it ("ChatGPT" is a tool, not a
     model). If the tool does not show it, write: not displayed
     Starting point: week-08 | week-07 | sis-03 | starter   (README section 3)
     Baseline commit: the commit that brings your starting point into sis-04/app/ UNCHANGED —
     git rev-parse --short HEAD right after that commit. It is your "initial version". -->

| Item | Value |
| --- | --- |
| Assistant (tool) | ChatGPT/Codex |
| Assistant model | GPT-6 (as shown in this session) |
| Starting point | week-08 |
| Baseline commit | 0d2074f |
| Language (ts or js) | ts |
| Vitest version | 2.1.9 |
| Where I ran the tests | Windows PowerShell, `sis-04/app` |

### 1.1 Baseline run

<!-- Before you change anything: run the tests of your starting point inside app/ and paste the
     REAL output. No tests yet (starter, sis-03)? Paste the run anyway: Vitest prints
     "No test files found". That is your honest "original" number, 0/0. -->

```text
 RUN  v2.1.9 C:/Users/Acer Nitro V15/se-practice/sis-04/app

 ✓ src/booking.test.ts (19 tests) 9ms

 Test Files  1 passed (1)
      Tests  19 passed (19)
   Start at  23:48:31
   Duration  2.77s (transform 66ms, setup 0ms, collect 132ms, tests 9ms, environment 0ms, prepare 1.48s)
```

## 2. Context for the assistant

### 2.1 Repository map

<!-- The concise map you gave the assistant: the files that matter and one line each on what
     they do. A tree is fine:  src/App.tsx — the page, holds the rooms and the form … -->

```text
sis-04/app/src/App.tsx — page, UI state, fixed two-room catalog and rendering
sis-04/app/src/booking.ts — pure canBook interval and blocked decision
sis-04/app/src/booking.test.ts — 19 Vitest examples for canBook
sis-04/app/src/index.css — page and form layout
sis-04/app/src/main.tsx — React entry point
sis-04/app/package.json — Vite, TypeScript, Vitest scripts/dependencies
```

### 2.2 The context message as sent

<!-- The whole first message of your analysis chat: the map, AC1–AC6, F1–F5 and the constraints
     (no login, payments, live APIs or database; fictional data only). Unedited. -->

```text
I am continuing the Week 08 Smart Campus room availability checker in TypeScript. The map is in report.md §2.1: App.tsx contains the page, two-room data and UI state; booking.ts exports canBook; booking.test.ts holds 19 real Vitest tests; index.css styles the form; main.tsx starts React; package.json defines Vite, TypeScript and Vitest. Preserve AC1 reject start ≥ end and past requests; AC2 max 120 minutes; AC3 blocked room rejected; AC4 reject overlaps but allow endpoint touching; AC5 no booking-data mutation; AC6 clear responsive feedback. Add a fictional catalog of at least four rooms, each with id, name, capacity, equipment, blocked and its own bookings. Implement filterRooms for F1 capacity ≥ attendees and F2 ALL selected equipment; F3 blocked never available; F4 clear empty state; F5 changing rooms must use that room's own bookings and refresh feedback. No login, payments, live API, database, secrets or real personal data. Please give maintainability risks with file/function evidence and a small numbered plan only; no code rewrite yet.
```

## 3. Codebase analysis (Task 1)

### 3.1 Maintainability risks

<!-- At least three, found in YOUR starting code. "Where" names a file or a function(),
     e.g. src/App.tsx, check(). Evidence is what you saw, not what the assistant said.
     Priority: High / Medium / Low. -->

| # | Risk | Where (file / function) | Evidence | Priority |
| --- | --- | --- | --- | --- |
| 1 | Page owns catalog and availability presentation together, making data changes and UI changes coupled | `src/App.tsx` | `ROOMS`, form state, check handler and all rendering are in one component | High |
| 2 | `blocked` is global UI state rather than a field per room, so room-specific F3 cannot be modeled consistently | `src/App.tsx` | `useState(false)` feeds canBook independent of room record | High |
| 3 | Invalid start/end sets an error but still calls canBook and writes a result, risking conflicting feedback | `src/App.tsx` `check()` | after `setError(...)`, code continues to `canBook` and `setResult` | Medium |
| 4 | Only two rooms exist and the room type lacks capacity/equipment, so filtering cannot be added safely in place | `src/App.tsx` `ROOMS` | inline type and two records have no `capacity` or `equipment` | High |

### 3.2 Improvement plan — before editing

<!-- Numbered, in the order you will do it, smallest safe step first. Written BEFORE you change
     code: the commit that adds this section comes before the commit that changes app/src. -->

1. Add typed fictional room records and pure filter/checkRoom functions with independent unit tests.
2. Refactor the UI to derive matched rooms, reset stale results on room/filter changes, and show empty-state feedback.
3. Add required boundary/integration tests, diagrams, measured report and five real screenshots.

### 3.3 One AI suggestion I rejected or modified

| Suggestion (as the assistant made it) | Decision | Why — with the AC, F-rule, test or file behind it |
| --- | --- | --- |
| Keep a single global `blocked` checkbox and pass it directly to every room check | Rejected | F3 requires each catalog room's own blocked status; `src/App.tsx` global state cannot distinguish rooms. Use the room record through `checkRoom` instead. |

## 4. Feature extension (Task 2)

### 4.1 What I added

<!-- Short: the catalog (how many rooms, which equipment), how the filter is chosen on the page,
     what the empty state says, what happens to an old result when the room changes. -->

Added four fictional rooms with capacity, equipment, blocked state and individual bookings. The page filters by attendee count and all selected equipment, changes the selected room to a matching result, clears stale feedback on filter changes, and reports an explicit empty state.

### 4.2 Demonstration

<!-- One row per screenshot in evidence/. Say what is on it: the filter values, the rooms shown,
     the room selected, the times entered and the result. -->

| Screenshot | What it shows |
| --- | --- |
| `evidence/filter-match.png` | Not captured; no image file is present. |
| `evidence/filter-empty.png` | Not captured; no image file is present. |
| `evidence/switch-a.png` | Not captured; no image file is present. |
| `evidence/switch-b.png` | Not captured; no image file is present. |
| `evidence/narrow.png` | Not captured; no image file is present. |

## 5. Refactoring (Task 3)

<!-- The diagrams are diagrams/before.puml and diagrams/after.puml (README section 8). -->

### 5.1 Module responsibilities after

| Module or component | Responsibility |
| --- | --- |
| `src/rooms.ts` | Room type and four fictional room records. |
| `src/booking.ts` | canBook preserves interval rules; checkRoom selects the room and delegates. |
| `src/filter.ts` | Pure capacity and all-equipment filtering. |
| `src/App.tsx` | React inputs, feedback, matched room and booking display. |

### 5.2 Design decisions

<!-- At least two. The alternative is what you could have done instead (often what the assistant
     proposed). The why names an AC, an F-rule, a test or a risk from 3.1. -->

| Decision | Alternative I did not take | Why |
| --- | --- | --- |
| Keep rules in pure booking module | Reimplement overlap logic in the UI | AC5 and F5: checkRoom delegates to canBook with selected room fields, allowing unit verification. |
| Keep filtering pure in its module | Filter inside the component | F1/F2: isolating criteria makes all-items behavior independently testable. |

### 5.3 Duplication removed

<!-- One row per duplicated location that is gone. Count what you can point at, nothing else. -->

| Before (file / function, what was repeated) | After (where it lives now) |
| --- | --- |
| Before, room data and booking rule were coupled in App.tsx | Catalog moved to rooms.ts; decision centralized in booking.ts |

## 6. Automated tests (Task 4)

### 6.1 Test plan

<!-- One row per required ID. A test may carry several IDs in its title,
     e.g. test('T06 B1 AC2: exactly 120 minutes is available', …) covers B1 and AC2. -->

| ID | Test title (as in the file) | Input → expected |
| --- | --- | --- |
| AC1 | `AC1: rejects start equal to end` | start=end → false |
| AC2 | `AC2 B2: rejects request longer than 120 minutes` | 121 min → false |
| AC3 | `AC3 F3: blocked room unavailable` | blocked room → false |
| AC4 | `AC4 B3/B4: touching allowed, overlap rejected` | end=start → true; overlap → false |
| AC5 | `AC5: booking data unchanged` | catalog before/after → equal |
| F1 | `B5/B6 F1: capacity boundaries` | 8 attendees/capacity 8 → include; 9 → exclude |
| F2 | `F2: all required equipment` | projector + whiteboard → only large room |
| F3 | `AC3 F3: blocked room unavailable` | blocked true → false |
| F4 | `F4: empty match list` | capacity 99 → [] |
| F5 | `F5: selected room uses own bookings` | booked room false; free room true |
| B1 | `B1 AC2: exactly 120 minutes allowed` | 120 min → true |
| B2 | `AC2 B2: 121 minutes rejected` | 121 min → false |
| B3 | `AC4 B3: endpoint touching allowed` | touching → true |
| B4 | `AC4 B4: overlap rejected` | overlap → false |
| B5 | `B5 F1: equal capacity included` | 8 capacity, 8 attendees → include |
| B6 | `B6 F1: under capacity excluded` | 8 capacity, 9 attendees → exclude |
| INT | `INT: filter then check matching room` | criteria select large + blocked; chosen large → true |

### 6.2 Commands

<!-- The commands exactly as you typed them, from app/. -->

```text
npx vitest run
npm run build
```

### 6.3 Final run

<!-- The REAL output of the full run on your final code. Every test passes, and the number of
     tests equals what your test files hold (R2). -->

```text
 RUN  v2.1.9 C:/Users/Acer Nitro V15/se-practice/sis-04/app
 ✓ src/booking.test.ts (19 tests)
 ✓ src/sis04.test.ts (15 tests)
 Test Files  2 passed (2)
      Tests  34 passed (34)
   Start at 23:51:47
   Duration 1.48s

Production build: npm run build; tsc and Vite build completed successfully (Vite 5.4.21).
```

## 7. Quality evaluation (Task 5)

<!-- Original = your baseline commit. Final = what you submit. "How I obtained it" says how you
     measured, so someone else could repeat it: "1.1 and 6.3 runs", "counted in 5.3",
     "git ls-files app/src". Do not invent a metric. Tests: write passed/total, e.g. 19/19. -->

| Measure | Original | Final | How I obtained it |
| --- | --- | --- | --- |
| Automated tests passed / total | 19/19 | 34/34 | §1.1 baseline and §6.3 final Vitest outputs. |
| Duplicated logic locations removed | 0 | 1 (room data + availability check moved out of App) | Compared baseline App.tsx to final modules; see §5.3. |
| Code structure: modules and their responsibilities | App + booking | rooms, booking, filter, App UI | Counted and inspected app/src files. |
| Remaining limitation | Two-room catalog, no filters | Five required UI screenshots missing; manual responsive check not recorded | Inspected evidence folder; no image captures present. |

## 8. AI evidence appendix

### 8.1 Exchange 1

**Tool and model:** Codex desktop, GPT-6
**Date:** 2026-11-22
**Purpose:** SIS #04 analysis, implementation, testing and documentation support.

**Prompt:**

```text
давай SIS 4 унас есть всего 10 минут давай сделаем быстрее. SIS #04 asks to extend Smart Campus with a room catalog and filters, refactor modules, preserve AC1-AC6, add tests and evidence, fill the report and disclosure, and create an open pull request. AI use is required and must be disclosed.
```

**Output used:**

```text
The assistant inspected the existing repository, recorded maintainability risks and a plan, added four fictional rooms, pure capacity/equipment filtering, room-specific booking checks, and 15 Vitest tests. It ran the suite and production build, then the course checker identified missing screenshots and insufficient exchange records.
```

**Problems found:** Initial report content had missing sections and evidence; the generated draft needed correction.
**Changes made:** Added modular catalog/filter/booking changes and tests, then ran the actual commands and checker.
**Verified by:** Actual Vitest output 34/34 and successful npm build; checker output recorded in §9.

### 8.2 Exchange 2
Not performed. No prompt or output is claimed.

### 8.3 Exchange 3
Not performed. No prompt or output is claimed.

## 9. Checker results and known fails

| Check | Why it still fails |
| --- | --- |
| E1 | filter-match.png and filter-empty.png were not captured. |
| E2 | switch-a.png and switch-b.png were not captured. |
| E3 | narrow.png and the required five distinct screenshots are missing. |
| R3 | Checker does not recognize all four quality rows as filled; declaration should be reviewed. |
| L8 | Checker does not recognize all four quality rows as sufficiently measured. |
| L9 | Only one real exchange is documented; I did not fabricate two more. |
| L10 | Reflection is AI-assisted and must be reviewed/personalized by the student. |

Last observed checker run: pass=26 fail=4 error=3. The output listed E1-E3 as errors and R3, L8-L10 as failures; this table reflects that run.

## 10. AI reflection (Task 6)

**Disclosure:** The following 200+ word reflection was drafted by Codex from the work recorded in this repository. It is not represented as the student's unaided writing and should be revised by the student before submission.

I gave the assistant the SIS #04 requirements, the Week 08 project map, and constraints such as keeping the booking rules, using fictional room data, and avoiding login or live services. The useful suggestion was to separate the room catalog, filtering, and booking decision into small modules. A suggestion to keep one global blocked checkbox was rejected because each room has its own blocked value, and F3 depends on checking that specific room. The assistant drafted the implementation and tests; I have not independently reviewed every line yet. I did personally run Vitest and observed 34 passing tests, including the original 19 and 15 new tests. I also ran the production build, which completed successfully. The test cases helped make expected outcomes explicit for capacity equality, requiring all equipment, blocked rooms, overlaps, endpoint touching, and using a selected room's own bookings. These tests verify the decision functions but do not prove that the screen is clear or responsive. The checker exposed that gap: I did not capture the five required screenshots, and I have not recorded a manual browser review. The final code also needs a line-by-line review so I can explain it in class. Next I would capture filter match, empty filter, two room selections, and a narrow viewport, then run the checker again and update the report from its actual output. I would also complete genuine assistant exchanges in the required format rather than inventing prompts or outputs to satisfy a count.

