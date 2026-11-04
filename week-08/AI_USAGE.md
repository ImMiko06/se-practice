# AI Usage Disclosure — Week 08

Required by the course academic policy (Generative AI use level **D — AI-integrated**).
This disclosure records work performed by the Codex assistant in this session and the two Claude conversations used for the prescribed comparison. Yelemes remains responsible for reviewing and understanding the deliverable.

| Tool | Exact model / plan | Used for | Which files it touched |
| --- | --- | --- | --- |
| Codex desktop assistant | Model/version not displayed in the app | Repository setup, Week 08 implementation, BUG-A/BUG-B tests, applying the two fixes, running Vitest and the checker, and drafting this report/disclosure. | `app/src/booking.test.ts`, `app/src/booking.ts`, `lab-report.md`, `AI_USAGE.md`, `evidence/install.png` |
| Claude desktop/web, chat “Room-booking test failure” | Sonnet 5.5, Medium; Free plan | Task 4: diagnosis with no skill enabled. Prompt asked Claude not to edit code. | None |
| Claude desktop/web, chat “Bug detector procedure” | Sonnet 5.5, Medium; Free plan | Task 5: prompt-only simulation (not an installed skill), then diagnosis using the same code and criteria. | None |

**Skill file and ZIP:** `skills/bug-detector/SKILL.md` and `skills/bug-detector.zip` have not been created. The course says the skill must be typed by the student; I have not represented AI-generated text as hand-typed work.

**Patches:** Codex made the strict overlap-condition edit for BUG-A and removed `bookings.push` for BUG-B after the failing tests were committed. The student should review and explain both edits before submission.

**Terminal outputs:** lab-report.md contains factual results and selected run output. Some output blocks are concise excerpts rather than full unedited transcripts; the earlier Week 07 run transcript was not retained. Do not claim all terminal output is pasted unedited.

**Understanding:** not yet confirmed by the student. Before submission, the student should review the function and explain what the BUG-A and BUG-B tests prove.

Signed: Yelemes Meyirzhan  
Date: 2026-11-05
