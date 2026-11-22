# AI Usage Disclosure — SIS #04

AI was used as required by the course's Level D policy. Codex desktop (GPT-6) assisted with repository analysis, a plan, app code, tests, diagrams and report drafting on 2026-11-22 and 2026-11-23. It affected `app/src/App.tsx`, `booking.ts`, `filter.ts`, `rooms.ts`, `sis04.test.ts`, `app/README.md`, `diagrams/*`, `report.md`, `AI_USAGE.md`, and `submission.yml`.

Codex also used Selenium to operate the local application and capture the five UI screenshots. These are actual rendered screenshots, not mockups. The narrow capture used a 400×844 viewport and had 400px document width.

The assistant helped write `app/src/sis04.test.ts`; the recorded Vitest run reported 34/34 passing. `npm run build` completed successfully. I have not reviewed every generated source line and must do so before claiming I can defend the code. The terminal output cited in the report came from real runs. No credentials or private data were shared. The GitHub token was consumed by the local Git credential helper and was not printed or stored in the repository.

Signed: Yelemes Meyirzhan
Date: 2026-11-23
