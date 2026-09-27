# Lab report — Practice #03, Requirements Engineering with AI

Name: Yelemes Meyirzhan
Student ID: 24B031740
GitHub username: ImMiko06

---

## 1. Setup

| | |
| --- | --- |
| AI assistant (tool) | Claude.ai |
| Exact model name and version | Claude Sonnet 5 |
| Date of the session | 2026-09-27 |
| Diagram renderer used | PlantUML online server (plantuml.com) |

One tool, one model, used for all three prompts.

---

## 2. Original AI output — user stories (Part 1)

Paste of the unedited response to Prompt 1:

US-01
Story: As a Student, I want to view real-time room availability, so that I can find a free room quickly.
Priority: High
Assumption: Availability is shown at least by room and time slot for the current day.

US-02
Story: As a Student, I want to book a free room for a specific time slot, so that I can guarantee myself a study space.
Priority: High
Assumption: A student can hold only one active booking per time slot.

US-03
Story: As a Student, I want to cancel my booking, so that I free up the room for others if my plans change.
Priority: Medium
Assumption: Cancellation is allowed any time before the booking starts.

US-04
Story: As a Student, I want to receive a confirmation when I book or cancel a room, so that I know the action succeeded.
Priority: Medium
Assumption: Confirmation is shown in the application interface immediately after the action.

US-05
Story: As an Administrator, I want to block a room that is out of service, so that students cannot book a room that isn't usable.
Priority: High
Assumption: Only an Administrator can change a room's blocked status.

US-06
Story: As an Administrator, I want to unblock a room once it's usable again, so that students can resume booking it.
Priority: Medium
Assumption: Unblocking is a separate, explicit action from blocking.

US-07
Story: As an Administrator, I want to review room usage over a period, so that I can understand demand patterns and plan capacity.
Priority: Low
Assumption: Usage data covers at least booking counts per room over a selectable date range.


---

## 3. Story review (Part 2)

| Story (as generated) | What I did | Why | Final ID |
| --- | --- | --- | --- |
| US-01 (availability) | Kept unchanged | Names a real stakeholder (Student), one clear outcome, testable | US-01 |
| US-02 (book room) | Kept unchanged | Clear, testable, in-scope | US-02 |
| US-03 (cancel) | Kept unchanged | Clear, testable, in-scope | US-03 |
| US-04 (confirmation, originally 4th) | Renumbered to US-07, reworded assumption | As generated it read as if the Student actively "receives" the confirmation, blurring who triggers UC-06. Reworded the assumption to state explicitly the system triggers it automatically after UC-02/UC-03, not the Student — this matters directly for the diagram's actor associations (PU-6) | US-07 |
| US-05 (block room) | Renumbered, kept content | No change needed to content, only ID shifted | US-04 |
| US-06 (unblock room) | Renumbered, kept content | No change needed to content, only ID shifted | US-05 |
| US-07 (review usage) | Renumbered, kept content | No change needed to content, only ID shifted | US-06 |

**Did the assistant invent anything outside the scenario?** No. Checked every story against the out-of-scope list (payments, check-in/QR, maintenance, SMS/push, auth, waitlists) — none appear. The confirmation story (US-07) came closest to a misstep, not by introducing a new feature, but by implying the wrong actor triggers UC-06; that was a role/agency problem, not scope creep.

**How many stories did you end with, and why that number?** 7. All seven map cleanly onto the six use cases (UC-04 absorbs both the "block" and "unblock" stories), which is within the required 6–8 range and covers every use case at least once, so trimming further would leave a use case without a story.

---

## 4. Original AI output — acceptance criteria (Part 3)

Generated directly in the finished shape shown in requirements/acceptance-criteria.md — the raw response already matched the Given/When/Then structure with no reformatting needed; only the two boundary assumptions had to be made explicit since the base prompt does not resolve them, per the task instructions.

---

## 5. Criteria review (Part 3)

| Criterion (as generated) | Problem | What I changed it to | Final ID |
| --- | --- | --- | --- |
| Book room — happy path | None | Kept, but added explicit reference to which rule justifies rejection in each negative case (R1–R4), since a plain "the system rejects it" is not traceable to a business rule | AC-01..AC-05 |
| Cancel booking | Missing an explicit link to UC-06 in the confirmation criterion | Added "per UC-06" to AC-08 so it is traceable | AC-06..AC-08 |
| Block room | Was missing an authorization/negative case (a Student trying to block a room) | Added AC-11 explicitly testing that only an Administrator can block | AC-09..AC-11 |

**The two open questions.**

| Question | My decision | Why |
| --- | --- | --- |
| A booking ending exactly when another begins — overlap under R3? | allowed | The two slots do not share any instant of actual use; treating a shared boundary point as an overlap would make back-to-back bookings impossible, which is an unreasonable real-world restriction for a study-room system |
| Is exactly two hours allowed under R2? | allowed | "At most two hours" is an inclusive upper bound in ordinary reading; excluding the boundary would require the rule to say "less than two hours" |

**Which invalid or boundary case did the assistant leave out?** The original, unedited direction from the prompt covered the four business rules but did not include an authorization case (non-Administrator attempting an Administrator-only action). Added AC-11 to cover it.

---

## 6. Original AI output — use-case diagram (Part 4)

Original draft (before fixing the actor associations):

@startuml
left to right direction
actor Student
actor Administrator
rectangle "Smart Campus study room booking" {
  usecase "View availability" as UC01
  usecase "Book room" as UC02
  usecase "Cancel booking" as UC03
  usecase "Block or unblock room" as UC04
  usecase "Review usage" as UC05
  usecase "Send confirmation" as UC06
}
Student --> UC01
Student --> UC02
Student --> UC03
Administrator --> UC01
Administrator --> UC04
Administrator --> UC05
Student --> UC06
Administrator --> UC06
@enduml

Rendered diagram: see requirements/use-cases.puml (final, corrected version).


---

## 7. Diagram review (Part 4)

| Element | Problem | What I changed |
| --- | --- | --- |
| Student --> UC06, Administrator --> UC06 | The initial draft connected both actors directly to "Send confirmation," but no person triggers that use case — the system sends it automatically after a booking or cancellation completes | Removed both direct actor associations; connected UC02 and UC03 to UC06 with <<include>> instead, since the confirmation is part of those flows, not a separately actor-triggered function |
| Administrator --> UC01 | Not in the very first draft; added deliberately | Administrators plausibly need to see availability too (e.g. before deciding to block a room), so this association was added with justification rather than left implicit |

**Associations.** The assistant's first draft drew Student --> Send confirmation and Administrator --> Send confirmation. Neither actor actually triggers UC-06 — a person books or cancels, and the system confirms as a consequence. This is exactly the kind of association PU-6 in check_requirements.py flags.

**Did any screen, database or internal component appear as a use case or an actor?** No — checked against the forbidden-terms list (database, screen, form, login, API, table, class, controller, UI); none appear in the diagram.

---

## 8. Traceability (Part 5)

Summary of requirements/traceability.md:

- Use cases with **no story** behind them: none — all six use cases have at least one story.
- Stories with **no use case** they belong to: none — all seven stories map to one of the six use cases.
- Criteria that test **no rule** from section 1: none directly test nothing, but UC-01 (View availability) and UC-05 (Review usage) have **zero acceptance criteria** at all, since Part 3 only covers 3 of the 7 stories, as required by the task.

**What does the largest gap tell you about the generated requirements?** The largest gap is not a defect the AI introduced but a structural consequence of the assignment's own scope limit (only 3 of 7 stories get acceptance criteria). It shows that "generated requirements look complete" and "generated requirements are complete" are different claims — a traceability pass is what actually surfaces which use cases have no test-level specification behind them, and a reader who only skimmed the diagram and the story list would not have noticed that Review usage has no acceptance criteria at all.

---

## 9. Checker runs

Terminal output of check_requirements.py:

PASS   US-1  user-stories.md         no placeholders left
PASS   US-2  user-stories.md         7 stories, IDs US-01…US-07
PASS   US-3  user-stories.md         every story has the required sentence shape
PASS   US-4  user-stories.md         every story has a priority
PASS   US-5  user-stories.md         every story declares an assumption
PASS   US-6  user-stories.md         only Student and Administrator appear as roles
PASS   US-7  user-stories.md         nothing from the out-of-scope list appears
PASS   AC-1  acceptance-criteria.md  no placeholders left
PASS   AC-2  acceptance-criteria.md  three sections, all naming real stories: US-02, US-03, US-04
PASS   AC-3  acceptance-criteria.md  every section has 3 to 5 uniquely numbered criteria
PASS   AC-4  acceptance-criteria.md  all 11 criteria are complete Given/When/Then
PASS   AC-5  acceptance-criteria.md  every section covers an invalid or boundary case
PASS   AC-6  acceptance-criteria.md  3 assumptions listed before the criteria
PASS   AC-7  acceptance-criteria.md  both open questions are settled in the assumptions
PASS   PU-1  use-cases.puml          valid PlantUML block, no placeholders
PASS   PU-2  use-cases.puml          exactly two actors: Student, Administrator
PASS   PU-3  use-cases.puml          all six use cases present
PASS   PU-4  use-cases.puml          system boundary present
PASS   PU-5  use-cases.puml          no screens, databases or internal components
PASS   PU-6  use-cases.puml          no unjustified actor associations found
PASS   TR-1  traceability.md         all six use cases have a row
PASS   TR-2  traceability.md         every ID in the table resolves
PASS   TR-3  traceability.md         every story appears in the table
------------------------------------------------------------------------
23 PASS · 0 FAIL · 0 ERROR   (23 checks)

| | PASS | FAIL | ERROR |
| --- | --- | --- | --- |
| check_requirements.py | 23 | 0 | 0 |

Commit these numbers were produced at (git rev-parse --short HEAD): WILL_FILL_AFTER_COMMIT

**Every FAIL, one line each:** None — the run was clean (0 FAIL, 0 ERROR).

**Did you run the checks by hand instead of with Python?** No — Python 3 was used directly.

---

## 10. Conclusion (150–200 words)

The part of the generated requirements that was most wrong was not any single business rule but the actor association in the use-case diagram: the first draft connected both Student and Administrator directly to "Send confirmation," implying a person triggers it, when the scenario makes clear the system sends it automatically after a booking or cancellation. Without the checker's PU-6 rule explicitly asking "who is connected to Send confirmation, and does a person trigger it," this would have been easy to miss by eye, since the arrow looks syntactically fine in PlantUML.

What the assistant got right, and did noticeably faster than doing it by hand, was producing a complete, correctly-shaped first draft across all three artifacts in seconds — stories with priorities and assumptions, Given/When/Then criteria tied to the four business rules, and a syntactically valid diagram — none of which had gross scope violations.

If I were handing this to an implementer and would not be in the room, I would rewrite the assumptions block in acceptance-criteria.md first: the two boundary decisions (overlap-at-touching, exactly-two-hours) are load-bearing for R2/R3 and easy to silently disagree on downstream.
