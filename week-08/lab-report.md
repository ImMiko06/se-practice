# Week 08 — Lab report

**Name:** Yelemes Meyirzhan  
**Group:** Not provided  
**Date:** 2026-11-05

---

## 1. Setup

| | |
| --- | --- |
| Assistant I debugged with (tool) | Claude web (desktop app) |
| Exact model (with its version, or `not displayed`) | Sonnet 5.5, Medium (as displayed) |
| Where the skill was installed (ChatGPT / Claude web / Claude Code / prompt-only simulation) | Prompt-only simulation in a fresh Claude chat; no skill was installed |
| Where I ran the tests (Bolt terminal / my computer / Codespace) | My computer, PowerShell terminal |
| Vitest version (the `RUN  v…` line of a run) | 2.1.9 |
| Language of my booking module (`ts` or `js`) — the file I copied from `buggy/` | ts (`buggy/booking.ts`) |

---

## 2. Task 1 — baseline, buggy code, failing tests

### 2.1 My Week 07 suite on my own code

The Week 07 baseline run completed with 17 tests passing before the provided broken function was copied in. The earlier terminal transcript was not saved verbatim, so I am recording the verified test count rather than inventing a terminal transcript.

```text
RUN  v2.1.9 C:/Users/Acer Nitro V15/AppData/Local/Temp/week08-week07-baseline-04f30e7/week-08/app

✓ src/booking.test.ts (17 tests) 11ms

Test Files  1 passed (1)
Tests       17 passed (17)
Start at    04:37:49
Duration    1.14s (transform 67ms, setup 0ms, collect 119ms, tests 11ms, environment 0ms, prepare 156ms)
```

### 2.2 The same suite on the provided canBook

Re-run from the baseline commit `f64a886` (17 tests):

```text
RUN  v2.1.9 C:/Users/Acer Nitro V15/AppData/Local/Temp/week08-baseline-f64/week-08/app

❯ src/booking.test.ts (17 tests | 4 failed) 24ms
   × T01 AC4 touching after is available
   × T08 AC4 touching before is available
   × AC5 an available request does not alter bookings
   × X2 AC4 touching a second booking is allowed

Test Files  1 failed (1)
Tests       4 failed | 13 passed (17)
```

The AC5 test also expected a touching request, so BUG-A returned `false` before the `push` line. That failure alone did not demonstrate BUG-B.

### 2.3 One failing test per bug

Actual Vitest run at commit `a7624b6`, before either fix:

```text
RUN  v2.1.9 C:/Users/Acer Nitro V15/AppData/Local/Temp/week08-buggy-a7624b6/week-08/app

❯ src/booking.test.ts (19 tests | 6 failed) 39ms
   × T01 AC4 touching after is available
   × T08 AC4 touching before is available
   × AC5 an available request does not alter bookings
   × X2 AC4 touching a second booking is allowed
   × BUG-A AC4 a request touching bookings on both sides is available
   × BUG-B AC5 an available non-touching request leaves bookings unchanged

BUG-A: expected false to be true (touching interval [660,720) vs [600,660)).
BUG-B: the array contained an extra {start:720,end:780} entry after canBook.
Test Files  1 failed (1)
Tests       6 failed | 13 passed (19)
```

## 3. Defect log

**Honesty note:** the required pre-assistant hypotheses were not written before the two Claude chats. These are retrospective explanations based on the tests and code, not contemporaneous student notes.

| Defect | Test ID | Input | Expected | Actual | Suspected cause (line and why) |
| --- | --- | --- | --- | --- | --- |
| BUG-A | BUG-A (also T01/T08) | request [660,720), existing [600,660) and [720,780), now 540, unblocked | true; touching endpoints are allowed | false | Retrospective: `if (start <= b.end && end >= b.start)` treats shared endpoints as overlap because both comparisons are inclusive. |
| BUG-B | BUG-B | request [720,780), existing [600,660), now 540, unblocked | true and original array unchanged | true, but a new interval was appended | Retrospective: `bookings.push({ start, end })` mutates the supplied array during an availability check. |

---

## 4. Tasks 2–3 — the skill

The prescribed hand-typed `SKILL.md` has **not** been created yet. The chat simulation did not install a skill file, so these file and ZIP checks remain incomplete.

| Check | yes / no |
| --- | --- |
| The file is plain UTF-8 text, named exactly `SKILL.md` (not `SKILL.md.txt`) | no — file not created yet |
| The first and the closing YAML delimiter are exactly three hyphens: `---` | no — file not created yet |
| `name` is lowercase with hyphens, and `description` says WHEN to use it | no — file not created yet |
| I read the whole file once: no passwords, API keys or private student data | no — file not created yet |

**The contents of `skills/bug-detector.zip`:** not created yet. There is no ZIP listing to report.

**Installation.** Claude Skills upload was not available in the account/plan used for this task, so the README fallback was used. A fresh Claude chat was given the skill procedure as its first message, explicitly labelled “Prompt-only simulation, not an installed skill.” It acknowledged the procedure. A screenshot of that simulation is saved as `evidence/install.png`. No installed-skill badge was shown.

---

## 5. Task 4 — without the skill

Fresh Claude chat `Room-booking test failure`, no skill enabled. The exact question and input sent were:

```text
Find the root cause of the failed room-booking test. Propose minimal patch and regression test. Do not edit code.
AC1 Reject start ≥ end and requests in the past.
AC2 Enforce the maximum allowed duration (120 minutes).
AC3 Reject a blocked room.
AC4 Reject overlaps; allow bookings that only touch at endpoints.
AC5 Return Available / Unavailable without changing booking data.
AC6 Preserve clear UI feedback on desktop and mobile.
Failed test from the provided canBook: T01 AC4 touching after is available — expected true, received false. Input: request [660,720), now=540, blocked=false, existing booking [600,660).
Provided canBook code:
export function canBook({ start, end, now, blocked, bookings }: {
  start: number;
  end: number;
  now: number;
  blocked: boolean;
  bookings: { start: number; end: number }[];
}): boolean {
  if (!(0 <= start && start < end && end <= 1440)) return false;
  if (!(start > now)) return false;
  if (end - start > 120) return false;
  if (blocked) return false;
  for (const b of bookings) {
    if (start <= b.end && end >= b.start) return false;
  }
  // keep the room's list current with the slot that was just found free
  bookings.push({ start, end });
  return true;
}
```

**The assistant's answer, pasted from the chat:**

```text
Root cause
The overlap check uses inclusive comparisons:
if (start <= b.end && end >= b.start) return false;
For request [660,720) against existing [600,660): 660 <= 660 is true and 720 >= 600 is true, so the touching booking is rejected. With half-open intervals [start,end), two ranges overlap only if start < b.end && end > b.start. That violates AC4’s “allow bookings that only touch at endpoints.” The same bug would reject a request that ends exactly where an existing booking starts.

Second defect: AC5 violation
bookings.push({ start, end }) mutates the caller’s array on every successful check. AC5 says the availability check must return Available / Unavailable without changing booking data. That side effect also makes the function non-idempotent: calling canBook twice with the same input returns true, then false (the slot now collides with itself). It is not what failed T01, but it would surface as soon as a test calls the function twice or reuses the fixture. The comment (“keep the room’s list current”) describes a commit step, which belongs in a separate book() function, not in a predicate.

Minimal patch
for (const b of bookings) {
-  if (start <= b.end && end >= b.start) return false;
+  if (start < b.end && end > b.start) return false;
}
- // keep the room's list current with the slot that was just found free
- bookings.push({ start, end });
return true;
If something depends on the push, move it to a separate caller-side step (e.g. if (canBook(req)) bookings.push(...)) rather than keeping it inside the check.

Regression tests
describe("canBook", () => {
 const base = { now: 540, blocked: false };
 it("T01 AC4: touching after is available", () => {
  expect(canBook({ ...base, start: 660, end: 720, bookings: [{ start: 600, end: 660 }] })).toBe(true);
 });
 it("AC4: touching before is available", () => {
  expect(canBook({ ...base, start: 540 + 60, end: 660, bookings: [{ start: 660, end: 720 }] })).toBe(true);
 });
 it("AC4: one-minute overlap is rejected", () => {
  expect(canBook({ ...base, start: 659, end: 720, bookings: [{ start: 600, end: 660 }] })).toBe(false);
 });
 it("AC4: fully contained and fully containing requests are rejected", () => {
  const bookings = [{ start: 600, end: 700 }];
  expect(canBook({ ...base, start: 620, end: 680, bookings })).toBe(false);
  expect(canBook({ ...base, start: 580, end: 720, bookings })).toBe(false);
 });
 it("AC5: does not mutate bookings and is idempotent", () => {
  const bookings = [{ start: 600, end: 660 }];
  const snapshot = JSON.parse(JSON.stringify(bookings));
  const req = { ...base, start: 660, end: 720, bookings };
  expect(canBook(req)).toBe(true);
  expect(canBook(req)).toBe(true);
  expect(bookings).toEqual(snapshot);
 });
});
Other ACs, checked against the code:
• AC1: start < end and start > now are correct. Note start > now rejects a start equal to now, which is a reasonable reading of “in the past” but worth confirming with spec owner.
• AC2: end-start >120 correctly allows exactly 120.
• AC3 blocked check correct.
• AC6 UI feedback isn’t in supplied code, so can’t assess.
I didn’t edit any files, as requested.
```

---

## 6. Task 5 — with the skill

Fresh Claude chat `Bug detector procedure`. It was a **prompt-only simulation**, not an installed or invoked skill. The skill text was the first message. The exact question and input sent were:

```text
Use the bug-detector skill to diagnose the failed room-booking test.
AC1 Reject start ≥ end and requests in the past.
AC2 Enforce the maximum allowed duration (120 minutes).
AC3 Reject a blocked room.
AC4 Reject overlaps; allow bookings that only touch at endpoints.
AC5 Return Available / Unavailable without changing booking data.
AC6 Preserve clear UI feedback on desktop and mobile.
Failed test from the provided canBook: T01 AC4 touching after is available — expected true, received false. Input: request [660,720), now=540, blocked=false, existing booking [600,660).
Provided canBook code:
export function canBook({ start, end, now, blocked, bookings }: {
  start: number;
  end: number;
  now: number;
  blocked: boolean;
  bookings: { start: number; end: number }[];
}): boolean {
  if (!(0 <= start && start < end && end <= 1440)) return false;
  if (!(start > now)) return false;
  if (end - start > 120) return false;
  if (blocked) return false;
  for (const b of bookings) {
    if (start <= b.end && end >= b.start) return false;
  }
  // keep the room's list current with the slot that was just found free
  bookings.push({ start, end });
  return true;
}
```

**The assistant's answer, transcribed from the Claude chat:**

```text
Reproduction
Smallest input is the failing T01 itself: request [660,720), now=540, blocked=false, existing [600,660).
Trace through canBook:
- Bounds check: 0 ≤ 660 < 720 ≤ 1440 passes.
- Past check: 660 > 540 passes.
- Duration: 60 ≤ 120 passes.
- Blocked: false, so it passes.
- Loop, with b = [600,660): 660 <= 660 is true and 720 >= 600 is true, so it returns false. The expected result is true.

Confirmed defects (Defect | Evidence | Root cause | Fix | Test)
D1: Touching bookings are treated as overlaps (AC4) | T01 fails: expected true, got false. The mirror case also fails: request [600,660) vs existing [660,720] gives 660 >= 660 and 600 <= 720, so it returns false. | The overlap check uses inclusive comparisons (<= and >=). That makes the intervals closed, but AC4 requires half-open [start, end) semantics, where shared endpoints don’t collide. | In the loop, use strict comparisons: if (start < b.end && end > b.start) return false; | T01 should return true. Add a “touching before” case ([600,660) vs existing [660,720]) that should also return true. Add a 1-minute true overlap (request [659,720) vs existing [600,660]) that should return false.

D2: The availability check mutates bookings (AC5) | Line bookings.push({ start, end }) runs before return true. T01 never reaches it because D1 returns early. Once D1 is fixed, a successful check will mutate the caller’s array. | A query function has a write side effect. The comment (“keep the room’s list current”) suggests it was added deliberately, but AC5 requires Available/Unavailable without changing booking data. | Delete the push line. Creating a booking should be a separate, explicit operation. | With bookings = [], call canBook on a valid request twice. Both calls should return true, and bookings should still be []. Also snapshot a non-empty array before and after and assert deep equality.
D2 also produces a visible symptom. After one successful call, the same request returns false, because it now overlaps the entry it just pushed.

Hypotheses (not confirmed by the evidence)
- start > now may be too strict (AC1). A request starting exactly at now is rejected. AC1 says “in the past,” so start === now is arguably not past. This depends on the intended rule, so confirm it with the product owner before changing it.
- The day bounds 0 ≤ start and end ≤ 1440 are not in the acceptance criteria. They look like a reasonable assumption (minutes in a day), but they aren’t specified. Overnight bookings would be rejected.
- AC6 (UI feedback on desktop and mobile) can’t be assessed. The code provided is pure logic, with no UI.

Checked and no defect found
- AC2: end - start > 120 correctly allows exactly 120 and rejects 121.
- AC3: the blocked check is correct.
- AC1 start < end: correct.

Suggested minimal fix (not applied)
for (const b of bookings) {
  if (start < b.end && end > b.start) return false;
}
return true; // no push
After this, T01 passes and AC5 holds. Please run the full suite after applying it to confirm no other test depended on the push.
```

Did the environment show that the skill was invoked? **no** — this was a prompt-only simulation, not an installed skill.

---

## 7. Comparison — judged against the actual code

| Criterion | No skill | With skill |
| --- | --- | --- |
| Correct root cause | Correctly identified inclusive overlap checks and the array push side effect. | Same two confirmed defects, with a concrete trace for T01 and the hidden BUG-B explanation. |
| Reproducible test | Good T01, mirror-touching, overlap, and non-mutation/idempotence tests. | Good T01, mirror-touching, one-minute overlap, and non-mutation/idempotence tests. |
| Minimal proposed patch | Strict overlap comparisons plus removal of the push; both minimal. | Strict overlap comparisons plus removal of the push; both minimal. |
| Unsupported claims | AC1 “in the past” interpretation is qualified; UI cannot be assessed from the function. | Similar caveat on AC1 and UI; also raises day-bound assumptions as hypotheses, not confirmed defects. |
| Clarity of explanation | Clear and accurate, but not a skill-assisted answer. | Clear, stepwise reproduction and separates confirmed defects from hypotheses as prompted. |

**Which bugs did each answer find?** Both answers found BUG-A and BUG-B. This is only a prompt-only procedure comparison; it does not demonstrate that an installed skill improved Claude.

---

## 8. Task 6 — repair and regression

### 8.1 The BUG-A patch

Commit `5975cb0`, one line changed:

```diff
- if (start <= b.end && end >= b.start) return false;
+ if (start < b.end && end > b.start) return false;
```

Real targeted run after BUG-A fix:

```text
RUN v2.1.9
✓ src/booking.test.ts (19 tests | 18 skipped)
Test Files  1 passed (1)
Tests       1 passed | 18 skipped (19)
```

The full run at this point still had two AC5 mutation tests fail (17 passed, 2 failed), demonstrating that BUG-B remained after the separate BUG-A commit.

### 8.2 The BUG-B patch and the final run

Commit `2ab8f2d`, one line deleted:

```diff
- bookings.push({ start, end });
```

Final real full-suite run:

```text
RUN  v2.1.9 C:/Users/Acer Nitro V15/se-practice/week-08/app

✓ src/booking.test.ts (19 tests) 14ms

Test Files  1 passed (1)
Tests       19 passed (19)
Start at    04:31:55
Duration    1.13s (transform 82ms, setup 0ms, collect 149ms, tests 14ms, environment 0ms, prepare 222ms)
```

---

## 9. What still fails, and what AI-assisted debugging cannot do

### 9.1 Checks I am keeping as FAIL or ERROR

Latest checker run: 2026-11-05, `23 PASS · 1 FAIL · 7 ERROR` (31 checks). B6 now passes: `app/node_modules` was moved to the Recycle Bin through VS Code and is absent from the project. K1–K7 are errors because the required student hand-typed skill file and matching ZIP are not yet present. L3 fails because those skill-file checks and ZIP listing are not complete.

| Check | Why it stays |
| --- | --- |
| K1–K7 | The student must type the prescribed `SKILL.md` by hand and make the matching ZIP. Neither has been created yet. |
| L3 | Section 4 honestly records that the four file checks and ZIP listing are incomplete; they cannot be marked yes until the student's hand-typed file exists. |

### 9.2 One limitation of AI-assisted debugging

Claude can explain the code and suggest good tests, but the assistant’s answer does not prove either test actually ran. In this work, I had to run Vitest separately to see the six failures on the buggy version and the final 19 passing tests; the prompt-only simulation also cannot establish that an installed skill was invoked or that a skill improved the answer.

---

## 10. Conclusion (80–150 words)

**Draft for the student to review and put into their own words before submission:** Both Claude answers found BUG-A and BUG-B, so the prompt-only procedure did not show a clear improvement in root-cause accuracy; the skill-style response did explain T01 step by step and separated confirmed defects from hypotheses. The failing tests proved that touching bookings were rejected and that a successful availability check appended to the caller’s list; after the two separate one-line fixes, all 19 tests passed. The suite does not prove the mobile and desktop feedback requirement because these tests exercise only `canBook`, not the UI. Since Claude did not actually load an installed skill, this comparison only evaluates the debugging procedure pasted into a fresh chat, not a real installed Agent Skill.
