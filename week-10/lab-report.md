# Week 10 — Lab report

**Name:** Yelemes Meyirzhan
**Group:** Not supplied
**Date:** 22 November 2026

Fill in every section. **Do not delete, rename or renumber the headings.** The checker and the
grader find your answers by them. You can add rows to any table, but never remove its header.

---

## 1. Setup

| | |
| --- | --- |
| Assistant I reviewed with (tool) | Claude desktop/web |
| Exact model (with its version, or `not displayed`) | Sonnet 5.5, Medium (as displayed) |
| Where the assistant read the project (Bolt.new / Claude Code / Cursor / Copilot / chat with pasted files) | Chat with pasted excerpts; no repository workspace |
| Starting point (`week-08` or `week-07`) | week-08 |
| Baseline commit — the checkpoint of Part 0 | 5a04b58 |
| Where I ran the tests (Bolt terminal / my computer / Codespace) | My computer, PowerShell, inside week-10/app |
| Vitest version (the `RUN  v…` line of a run) | 2.1.9 |

---

## 2. Task 1 — the baseline

### 2.1 The project's commands

Run each command in `week-10/app/` before any change. **Exists:** `yes` or `no` (is there such a
script, or such a tool in `package.json`?). **Result:** `pass`, `fail`, `missing` or `not run`.

| Command | Exists | Result | Note |
| --- | --- | --- | --- |
| `npx vitest run` | yes | pass | 19 tests passed before changes |
| `npm test` | yes | pass | 19 tests passed before changes |
| `npm run test:unit` (the test command in `AGENTS.md`) | no | missing | no such package.json script |
| `npm run build` | yes | pass | TypeScript and Vite production build |
| `npm run lint` | no | missing | no lint script or linter dependency |

### 2.2 The baseline test run

The **real** output of `npx vitest run` in `week-10/app/`, before any change:

```text
 RUN  v2.1.9 C:/Users/Acer Nitro V15/se-practice/week-10/app

 ✓ src/booking.test.ts (19 tests) 10ms

 Test Files  1 passed (1)
      Tests  19 passed (19)
   Start at  22:37:32
   Duration  2.85s (transform 95ms, setup 0ms, collect 123ms, tests 10ms, environment 0ms, prepare 1.96s)
```

### 2.3 The agent reads the playbook

What you sent, exactly (the Practice #09 prompt):

```text
Read the root AGENTS.md before making changes. Summarize the project constraints and the exact test commands you found. Do not edit anything yet. If you cannot read AGENTS.md, tell me, and I will paste its content. Do not claim that AGENTS.md was automatically loaded.
```

The assistant's answer, pasted unedited:

```text
I could not read AGENTS.md from the workspace; the answer was based only on the text pasted into chat. It summarized the React + TypeScript Vite project, canBook, App.tsx and booking tests; repeated the provided claims about real KBTU data, endpoint-touch overlap, unrestricted edits, Supabase/login and Netlify production deploy; and listed npm install, npm run dev, npm run test:unit and npm run build. It also noticed the package.json scripts did not include test:unit and questioned a production deploy. This is a concise record from the chat; the verbatim transcript was not retained in the working notes.
```

```

Which rules in its summary are wrong for this project, and how you know:

Wrong rules: endpoint-touch is allowed by AC4; real data, Supabase/login and deploy violate the scope; test:unit is absent. The claim that package installs were blocked was contradicted by my successful npm install.

Claude chat (Sonnet 5.5 Medium, Free plan), fresh chat with pasted code/config excerpts only; it had no project-editing workspace and stated it opened no files and ran nothing. The review chat made no repository changes. The following answer is a factual summary from the retained conversation notes, not a verbatim full transcript; that required evidence is incomplete.

---

## 3. Tasks 2–3 — the read-only review and the challenge

### 3.1 The review prompt and the answer

Where it ran, and how you made sure it could not edit: a fresh Claude chat received pasted excerpts only; it had no project workspace or write access. I checked git status after the review and no app files changed.

What you sent, exactly (the deck's prompt):

```text
Act as a cautious software reviewer. Inspect this Smart Campus Room Availability Checker WITHOUT editing files. Identify risks in correctness, security, privacy, reliability, maintainability, and agent operations. For each risk, cite the exact file/function or missing check, explain the impact, suggest a way to verify it, and state uncertainty. Do not invent test results.
```

The assistant's answer, pasted unedited:

```text
The reviewer said it inspected only pasted excerpts, opened no files and ran nothing. It identified a contract conflict: the half-open overlap expression in src/booking.ts allows endpoint touching, while AGENTS.md says touching is overlap. It noted stale feedback when the blocked-room checkbox changes without clearFeedback, and check() can set an error then still call canBook. It flagged agent operations: AGENTS.md permits arbitrary edits, packages, Supabase/login and npx netlify deploy --prod. It noted test:unit is missing, no explicit integer-minute validation, unclear date/time interpretation, and no integration/CI checks in the excerpts. It raised privacy risk from using real KBTU schedules, possible UI accessibility/feedback issues, missing server enforcement if persistence is added, magic numbers, and an incomplete definition of done. It explicitly marked uncertainty where it had not seen full files/config. This paragraph is a summary, not the entire unedited response; I cannot claim it satisfies the verbatim-paste requirement.
```

### 3.2 Challenging the AI's claims

At least **five** claims from the answer, across at least **three** categories. **What I
inspected** is what you opened or ran yourself. **Label:** `confirmed`, `plausible` or
`unsupported`.

| # | The AI's claim (short) | Category | What I inspected | Label | Why |
| --- | --- | --- | --- | --- | --- |
| 1 | Touching endpoints treated as overlap | Correctness | Opened canBook; tested T01/T08 and AC4 contract | unsupported | The inequality allows endpoints to touch and tests expect available; the playbook statement is false. |
| 2 | Blocked toggle leaves stale feedback | Correctness | Read App.tsx and manually checked Available then toggled Room blocked | confirmed | UI still displayed Available with blocked checkbox selected. |
| 3 | Production deploy and broad edits risk | Agent operations | Read provided and patched AGENTS.md; confirmed netlify --prod directive | confirmed | The instruction can cause an unreviewed external production release. |
| 4 | test:unit command missing | Reliability | Read package.json and ran the command | confirmed | Scripts contain test, not test:unit; command returns missing script. |
| 5 | Fractional minutes accepted | Correctness | Read canBook and added failing R1 test | confirmed | 720.5 was accepted with no bookings, though the helper models whole-minute time. |
| 6 | npm install is blocked | Reliability | Ran npm install in app successfully | unsupported | It installed dependencies; the earlier chat claim was not true for this environment. |

---

## 4. Task 4 — the risk register

### 4.1 The register

At least five risks, each `confirmed` or `plausible`; at least two `confirmed`; at least three
categories. **Score = L × I.** **Component** is a path inside `app/` or `missing: <check>`.

| ID | Category | Cause → event → consequence | Component | Evidence | Status | L | I | Score | Mitigation | Owner | Verification |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R1 | Correctness | Fractional time passes validation → invalid minute slot is reported available | src/booking.ts canBook | Failing R1 test: 720.5 returned true | confirmed | 3 | 2 | 6 | Validate whole-minute inputs in extracted pure guard | Student | R1 test fails before and passes after; full Vitest suite |
| R2 | Agent operations | Unsafe playbook → agent deploys or adds auth/data → public unreviewed change | AGENTS.md | Explicit netlify --prod, Supabase/login and arbitrary edits | confirmed | 3 | 3 | 9 | Minimal approved playbook patch prohibiting deploy/data/auth and restricting scope | Student | Diff audit; checker A2/A3/C1-C6 |
| R3 | Reliability | Stale test command → agent cannot verify → bad change accepted | AGENTS.md | test:unit absent from package.json; command fails | confirmed | 2 | 2 | 4 | Use existing npm test in playbook | Student | Run npm test |
| R4 | Correctness | Blocked checkbox does not clear result → stale Available remains visible | src/App.tsx | Manually checked Available, then selected Room blocked; Available stayed visible | confirmed | 2 | 2 | 4 | Clear feedback when blocked state changes | Student | Manual browser interaction reproduced stale result |
| R5 | Security | Dependency advisories may remain → vulnerable dependency used → exposure | package.json | npm install reported 6 vulnerabilities; npm audit could not reach registry | plausible | 2 | 3 | 6 | Re-run npm audit with network and review exact advisories | Student | Successful npm audit in connected environment |
| R6 | Privacy | Agent uses real timetable → personal schedule exposed or inaccurate | AGENTS.md | Real KBTU portal data instruction conflicts with fictional-only scope | confirmed | 2 | 2 | 4 | Prohibit real portal data; use fictional room/bookings | Student | Inspect fixtures and instruction |

### 4.2 The top two for action

Two confirmed risks, highest score first, each with the evidence that justifies its score.

1. **R2** — Score 9 (3×3): AGENTS.md explicitly authorizes production deploy and scope expansion, with public impact.
2. **R1** — Score 6 (3×2): the new test reproduced a fractional-minute request returning true; invalid input can be accepted by the exported rule.

---

## 5. Task 5 — the agent-readiness audit

### 5.1 The rows

`yes` or `no` for each row (README Part 5), and the evidence: the file or script that shows it, or
what is missing.

| Row | What | yes / no | Evidence |
| --- | --- | --- | --- |
| 1a | Formatter | no | No Prettier config or dependency |
| 1b | Linter | no | No ESLint config or dependency |
| 1c | Type checks | yes | tsconfig.json and TypeScript in package.json; npm run build type-checks |
| 1d | Unit tests | yes | src/booking.test.ts and Vitest dependency |
| 1e | Pinned dependencies (lockfile) | yes | committed package-lock.json |
| 2a | `.env.example` | no | No .env.example |
| 2b | Architecture notes | no | No README or module architecture note in app |
| 2c | `AGENTS.md` | yes | app/AGENTS.md |
| 3a | CI | no | No .github workflow |
| 3b | Pre-commit hooks | no | No hook config/dependency |
| 3c | Integration checks | no | Only canBook unit tests; no page integration test |
| 3d | Reviewable evidence | no | No CI log or PR template required to attach test output |

### 5.2 The level and the gaps

**Level:** 0 — Level 1 has only 3/5 (60%).

**Missing evidence for the next level:**

<!-- Name the rows and what would have to exist. Then one or two lines on the README's accuracy
     and the folder layout. -->
- Next level requires at least 4/5 at Level 1: add a formatter or linter. Level 2 also needs 3/3, including .env.example and architecture notes. The app has no README, so its layout is not documented; its simple src layout is understandable but unexplained.

---

## 6. Task 6 — the agent playbook

### 6.1 The playbook prompt and the answer

What you sent, exactly (the deck's prompt):

```text
Review AGENTS.md and project documentation only. Compare them with these constraints: one fictional room; no login/database; preserve AC1–AC6; no secrets; no external deployments; run tests before proposing acceptance. Report missing or conflicting rules. Draft a minimal patch to AGENTS.md, but wait for my approval before applying it.
```

The assistant's answer, pasted unedited:

```text
I did not retain Claude's verbatim answer to this prompt. Claude had no local project workspace; I used the supplied instructions and checked the files directly. This absence is a disclosed evidence gap, not a claimed transcript.
```

### 6.2 Findings and my decisions

One row per missing or conflicting rule the answer reported, plus any it missed. **Decision:**
`approve`, `reject` or `modify`.

| # | Rule or line in AGENTS.md | Missing / conflicting | Decision | Why |
| --- | --- | --- | --- | --- |
| 1 | Use real KBTU timetable | Conflicts with fictional-only scope | approve | Removed this instruction and require fictional data. |
| 2 | AC4 endpoint touch overlap; AC6 missing | Conflicts with AC4 and omits AC6 | approve | Corrected endpoint rule and added UI feedback requirement. |
| 3 | test:unit | Script absent | approve | Replaced with npm test, which exists. |
| 4 | Broad edits, packages, Supabase/login, production deploy | Violates scope/security/release constraints | approve | Restricted task files; prohibited secrets, auth/database and deploy. |

### 6.3 The approved patch

`git diff app/AGENTS.md`, after you applied only what you approved:

```diff
diff --git a/week-10/app/AGENTS.md b/week-10/app/AGENTS.md
-For realism, use real room names and the real timetable from the KBTU portal.
+Use one fictional room and fictional bookings only; do not use real portal data.
-- AC4 Reject overlaps. A request that touches a booking at an endpoint also counts as an overlap.
+- AC4 Reject overlaps; allow bookings that only touch at endpoints.
 - AC5 Return Available / Unavailable without changing booking data.
+- AC6 Preserve clear UI feedback on desktop and mobile.
-- Tests: `npm run test:unit`
+- Tests: `npm test`
-- Edit any file in the project; allow extra packages, Supabase/login and external production deployment.
+- Edit only files needed for the approved task; do not change acceptance criteria or hide failures.
+- Do not add packages, login, a database, credentials, secrets or real personal data.
+- Never deploy externally; report test and build results for human review.
```

---

## 7. Task 7 — verify safely

### 7.1 The regression test fails before the mitigation

The risk it covers: **R1**. The real run, with the new test failing:

```text
> smart-campus-availability@0.0.0 test
> vitest run
 RUN  v2.1.9 C:/Users/Acer Nitro V15/se-practice/week-10/app
 ❯ src/booking.test.ts (20 tests | 1 failed) 22ms
   × assistant first suite: booking decisions > R1 AC1 fractional minute inputs are unavailable 11ms
     → expected true to be false // Object.is equality
 FAIL  src/booking.test.ts > assistant first suite: booking decisions > R1 AC1 fractional minute inputs are unavailable
AssertionError: expected true to be false // Object.is equality
 Test Files  1 failed (1)
      Tests  1 failed | 19 passed (20)
   Start at  22:55:47
   Duration  1.06s
```

### 7.2 The manual UI check

| View | Width | What I checked | Result | Screenshot |
| --- | --- | --- | --- | --- |
| Desktop | 1280 px | Submitted the default 11:00–12:00 query; checked for clipping and feedback | Pass: Available is legible, form and booking fit | not saved to evidence file |
| Mobile | not checked | Did not set a phone-width viewport | not run | not captured |

### 7.3 Tests and checks I did not run

<!-- Name each one and why. "None" only if it is true. -->
- Mobile UI inspection and both required screenshot files were not completed. npm audit attempted but registry DNS failed, so advisories were not verified. No browser integration test or lint ran; neither is configured.

---

## 8. Task 8 — mitigate two risks

### 8.1 The first mitigation

**Risk:** R1

**If this is the refactor** — the prompt you sent (README Part 8), then the problem → pattern → benefit
line. Otherwise leave both empty.

```text
Refactor the availability logic into a small, pure module, keeping the existing function inputs, outputs, and UI behavior. Use a pattern only if the identified design problem justifies it. Do not add new features or dependencies. Show the files you plan to edit before making changes.
```

**Problem → pattern → benefit:** Validation was inline and accepted fractional minute values; I extracted pure validation and overlap helpers in booking.ts. Keeping the public function contract and pure helpers makes the minute-domain rule easy to test without changing UI behavior.

**What I rejected from the agent's patch, and why:** No Claude code patch was proposed; I kept scope to booking logic and rejected dependencies and UI changes as unrelated.

The diff I approved (`git diff`):

```diff
- inline range, past-time, duration and overlap checks in canBook
+ isValidRequest enforces integer-minute, range, past-time and duration constraints
+ hasOverlap applies the existing half-open interval rule
+ canBook retains its input/output and delegates to the pure helpers
```

### 8.2 The second mitigation

**Risk:** R2

This is the separately committed playbook correction, not the refactor.

**Problem → pattern → benefit:** Not applicable; R2 is mitigated by correcting unsafe agent instructions rather than refactoring application code.

**What I rejected from the agent's patch, and why:** Rejected broad rewrite, external deploy, login, database, extra packages and real campus data because these conflict with written constraints.

The approved minimal patch is recorded in §6.3 and committed as `7688899`.

```diff
- unsafe data, permission and deployment instructions
+ fictional-only scope, no credentials/auth/database, no deployment, npm test
```

### 8.3 The residual risk

| ID | L before | I before | Score before | L after | I after | Score after | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| R1 | 3 | 2 | 6 | 1 | 2 | 2 | Regression failed before the pure validation guard and passes after; other malformed interval data remain untested. |
| R2 | 3 | 3 | 9 | 1 | 3 | 3 | Unsafe playbook directions removed; a human can still deploy manually outside repository controls. |

### 8.4 The final run

The real output of the **full** suite after both mitigations. Every test must pass.

```text
> smart-campus-availability@0.0.0 test
> vitest run
 RUN  v2.1.9 C:/Users/Acer Nitro V15/se-practice/week-10/app
 ✓ src/booking.test.ts (20 tests) 6ms
 Test Files 1 passed (1)
      Tests 20 passed (20)
   Start at 22:56:18
   Duration 901ms
```

---

## 9. Task 9, and what still fails

### 9.1 A background agent on this project

Rules for an agent working asynchronously on a separate branch. Be specific to this project: name
its files and its commands.

| Rule | What I require |
| --- | --- |
| Isolation | Work on a dedicated week-10 branch or worktree; never share the active checkout. |
| Permitted files | Only app/src/booking.ts, app/src/booking.test.ts and an approved UI file; report evidence only for the requested task. |
| Commands | In app run npm test and npm run build; test:unit and lint do not exist. |
| Prohibited actions | No credentials, real timetable, database, login, new packages, force push or external deployment. |
| Required evidence | Focused diff, passing Vitest output, build output, updated risk register and reviewer note. |
| Before merging or deploying | Human reviews diff/tests and explicitly approves release; this repository authorizes no deployment. |

### 9.2 Optional — the deck's checklist prompt (not graded)

<!-- If you sent it: the answer, and one thing it has that your rules in 9.1 do not, or the reverse. -->

### 9.3 Checks I am keeping as FAIL or ERROR

Use the same IDs as `known_fails` in `submission.yml`. Write `none` if the run is clean.

| Check | Why it stays |
| --- | --- |
| E1/E2 | Required desktop/mobile screenshot files were not saved; mobile review is also still pending. |
| L3/L9 | Full verbatim Claude answers were not retained; report labels answers as summaries. |
| B2 | Generated node_modules/dist are untracked locally and were not staged. |

---

## 10. Release decision and conclusion

**Decision:** CONDITIONAL

<!-- Keep one word above. GO is not allowed while any confirmed risk still scores 6 or more.
     Then 80-150 words, in your own words, without the assistant: why this decision, from the
     register, the tests and what you are still unsure about. Name at least two risk IDs.
     Worthless: "The project is mostly fine, so GO."
     Worth everything: "CONDITIONAL. R2 (the deploy line in AGENTS.md, 3 x 3 = 9) is closed by the
     approved patch, now 1 x 3. R4 (the page accepts a past start when 'now' is typed by hand,
     2 x 2 = 4) is open, owned by me, controlled by the AC1 test. The UI was checked at two widths,
     but no test covers App.tsx, so a regression there would be invisible." -->

The release decision is CONDITIONAL. R2 started at 3×3 because the supplied playbook permitted external production deployment and scope expansion; I removed those directions, but repository text cannot stop a person from deploying manually. R1 started at 3×2: a fractional minute passed the pure booking rule, and the new regression test demonstrated it. The pure validation helper now rejects fractional input, and the final 20-test suite plus production build pass. The readiness audit is Level 0 because only three of five baseline checks exist. I did not complete manual desktop/mobile UI inspection or capture screenshots, and the Claude review transcripts in my notes are summaries rather than full verbatim answers. Those evidence gaps must be closed before calling this release ready.
