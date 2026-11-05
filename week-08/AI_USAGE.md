# Generative AI Use Disclosure (Level D — AI-Integrated)

In compliance with the course academic policy (Generative AI use level D — AI-integrated), this document records the workflow, tool usage, and development process for the current assignment. I (Yelemes) take full responsibility for reviewing, understanding, and submitting all deliverables.

## Tool Usage Summary

| Tool | Model / Plan | Purpose | Files Affected |
| :--- | :--- | :--- | :--- |
| **Codex Assistant** | Desktop App | Repository setup, assistance with Week 08 implementation, structuring BUG-A/BUG-B tests, verifying test runs (Vitest), and drafting initial documentation outlines. | `app/src/booking.test.ts`, `app/src/booking.ts`, `lab-report.md`, `AI_USAGE.md`, `evidence/install.png` |
| **Claude** (Chat: *“Room-booking test failure”*) | Sonnet 3.5 (Free) | Task 4: Diagnostic analysis without active skills (strict prompt: no code editing). | None |
| **Claude** (Chat: *“Bug detector procedure”*) | Sonnet 3.5 (Free) | Task 5: Prompt-only simulation of the bug detector workflow and comparative code analysis. | None |

## Development Notes & Declarations

* **Skill Configuration:** Created and structured `skills/bug-detector/SKILL.md` based on course materials and packaged it into the required ZIP archive. All contents have been thoroughly reviewed.
* **Bug Fixes & Implementation:** 
  * **BUG-A:** Implemented the strict overlap-condition check to correctly handle conflicting booking intervals.
  * **BUG-B:** Cleaned up redundant logic (`bookings.push`) to prevent duplicate entry creation after confirming test failures.
* **Verification:** Ran and validated all tests locally via Vitest. Results and relevant logs are compiled in `lab-report.md`.
* **Code Review:** I have personally reviewed all implementation details, test assertions, and diagnostic steps, and I fully understand how the BUG-A and BUG-B test suites operate.
