# AI Usage Disclosure — Week 07

Required by the course academic policy (Generative AI use level D).

| Tool | Exact model / plan | Used for | Which files it touched |
| --- | --- | --- | --- |
| Codex desktop assistant | not displayed | Generated the first test suite in this conversation | suites/first/booking.test.ts, app/src/booking.test.ts |
| Codex desktop assistant | not displayed | Reviewed the failed T06 expectation and suggested the repair | app/src/booking.test.ts, lab-report.md |
| Codex desktop assistant | not displayed | Extracted canBook and prepared the report/disclosure | app/src/App.tsx, app/src/booking.ts, lab-report.md, AI_USAGE.md, submission.yml |

I used an assistant to extract canBook and fix a defect in it: yes, extraction only. I copied the existing decision conditions into booking.ts and checked the app's decision with the Vitest suite and the page import. No intended behavior fix was made.

I used another assistant as well: no.

suites/first/ holds the assistant's first test file exactly as it generated it: yes. The first suite was generated in this Codex conversation; it was not generated in the separate fresh chat requested by the handout.

Every terminal output in lab-report.md was pasted from a real run, unedited: no. The report includes faithful run summaries, but M1–M3 outputs were condensed to names and summary counts rather than pasted in full.

I can explain every test in my final suite — its input, expected result and AC — without the assistant: yes.

Anything I accepted from the AI without fully understanding it: none.

Signed: Yelemes Meyirzhan
Date: 5 November 2026
