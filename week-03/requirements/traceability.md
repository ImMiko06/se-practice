# Traceability — use cases → stories → criteria

| Use case | Stories (US-nn) | Criteria (AC-nn) | Gap? |
| --- | --- | --- | --- |
| UC-01 View availability | US-01 | none | AC gap: no acceptance criteria were generated for this story (only 3 of 7 stories were selected for Part 3) |
| UC-02 Book room | US-02 | AC-01, AC-02, AC-03, AC-04, AC-05 | |
| UC-03 Cancel booking | US-03 | AC-06, AC-07, AC-08 | |
| UC-04 Block or unblock room | US-04, US-05 | AC-09, AC-10, AC-11 | |
| UC-05 Review usage | US-06 | none | AC gap: no acceptance criteria were generated for this story |
| UC-06 Send confirmation | US-07 | AC-08 | Weak: only one criterion (from the cancellation flow) covers this use case; booking confirmation has no dedicated criterion |

**Stories that belong to no use case:** none

**What the gaps tell you:** The AI generated six use cases and seven stories that map onto all of them one-to-one (with UC-04 absorbing two stories, block and unblock), so there are no orphan stories. The real gap is in acceptance criteria: because the task fixes Part 3 at exactly three stories, UC-01 (View availability) and UC-05 (Review usage) end up with zero acceptance criteria at all, and UC-06 (Send confirmation) is covered by only one incidental criterion written for a different story. This is expected given the scope of the exercise, not a defect in the AI's output — but it is a real coverage gap a reviewer must flag before calling the requirements "done."
