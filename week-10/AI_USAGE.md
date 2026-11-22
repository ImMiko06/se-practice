# AI Usage Disclosure — Week 10

This is a Level D lab. I used the tools below and remain responsible for the code, report, and checks.

| Tool | Exact model / plan | Used for | Files touched |
| --- | --- | --- | --- |
| Claude desktop/web | Sonnet 5.5, Medium, Free | Task 1 playbook summary and Task 2 read-only review of pasted excerpts | None; it had no repository workspace |
| Codex | GPT-6 | Read repository files, run commands, draft report and disclosure, patch AGENTS.md, add regression test, refactor booking validation, and run checks | week-10/app/AGENTS.md, week-10/app/src/booking.test.ts, week-10/app/src/booking.ts, week-10/lab-report.md, week-10/AI_USAGE.md, week-10/submission.yml |

The Claude Task 2 chat was read-only because it received pasted excerpts and had no connected project; the repository had no changes from that review. Claude's full response transcript was not retained in the notes. The report labels its answer as a summary rather than presenting it as a verbatim transcript. The same limitation applies to the Task 6 answer.

The regression test was run before the fix and failed; after the pure validation refactor, the 20-test suite passed and `npm run build` passed. I reviewed the patches through their diffs and confirmed the command results from actual terminal output.

The student supplied desktop and responsive mobile screenshots. I saved them as `evidence/ui-desktop.png` and `evidence/ui-mobile.png` and inspected them: the desktop view shows clear Unavailable feedback, and the mobile view stacks the fields with the bookings list visible. The earlier manual interaction also showed stale Available feedback after toggling Room blocked; this remains an open risk in the report. The npm audit request could not reach the registry, so the reported vulnerability count could not be independently inspected.

Signed: Yelemes Meyirzhan
Date: 2026-11-22
