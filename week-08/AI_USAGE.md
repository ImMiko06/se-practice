# Generative AI Use Disclosure (Level D — AI-Integrated)

In compliance with the course academic policy (Generative AI use level D — AI-integrated), this disclosure records the workflow, manual contributions, and AI tools consulted during this assignment. I (Yelemes) remain fully responsible for the implementation, testing, code changes, and final deliverables.

## Tool Usage Summary

| Tool | Model / Plan | Purpose | Files Affected |
| :--- | :--- | :--- | :--- |
| **Claude desktop/web** (chat: “Room-booking test failure”) | Sonnet 3.5 / Free plan | Task 4: Diagnostic assistance without code editing (consultation on overlap logic). | None |
| **Claude desktop/web** (chat: “Bug detector procedure”) | Sonnet 3.5 / Free plan | Task 5: Prompt-only simulation of the bug detector workflow and code evaluation. | None |

## Work Process & Declarations

* **Repository & Skill Setup:** I manually configured the repository structure, authored `skills/bug-detector/SKILL.md` using the course material guidelines, and created the required `bug-detector.zip` archive.
* **Code Fixes & Implementation:**
  * **BUG-A:** I analyzed the interval logic and implemented the strict overlap condition in `app/src/booking.ts` to prevent invalid overlapping room bookings.
  * **BUG-B:** I identified the duplicate entry creation issue and removed the redundant `bookings.push` call after confirming the test assertions in `app/src/booking.test.ts`.
* **Testing & Verification:** I executed all test runs directly in the terminal using Vitest and ran the local validation scripts (`check_debugging.py` and `validate_submission.py`). All test suites passed successfully.
* **Understanding:** I have reviewed all changes in `app/src/booking.ts` and test assertions in `app/src/booking.test.ts`. I fully understand how the fixes resolve the edge cases identified in BUG-A and BUG-B.
