# AI Usage Disclosure — Week 09

Required by the course academic policy (Generative AI use level **D — AI-integrated**).
I am responsible for checking, understanding, and defending the work submitted.

| Tool | Exact model / plan | Used for | Which files it touched |
| --- | --- | --- | --- |
| Claude desktop/web | Sonnet 5.5 / Medium / Free plan | Part 2 — wrote one reply for each R1, R2 and R3 in three separate fresh chats using the exact deck prompt and tool definition; the replies were copied without editing. | calls/r1.json, calls/r2.json, calls/r3.txt, lab-report.md §4 |
| ChatGPT Codex desktop | UI label: 6 Luna (Medium; version not displayed) | Parts 1, 3, 5–10 — drafted the tool definition, checker explanations, report text and declaration; reviewed constraints and checker output. | tool/check_room.json, lab-report.md, AI_USAGE.md, submission.yml |

**I wrote `tool/check_room.json` myself:** no. Codex drafted it; I reviewed its fields, ranges, allowed keywords and checker results.

**I used an AI to explain a JSON Schema keyword or a check:** yes. Codex explained why integer/range constraints catch malformed inputs and why cross-field rules such as `start < end` remain in canBook.

**Every reply in `calls/` and in lab-report.md section 4 is exactly what the model returned:** yes. The Claude replies were copied from three separate fresh chats without editing.

**Every terminal output in lab-report.md was pasted from a real run, unedited:** yes. Section 8 contains the final checker output.

**Anything I accepted from the AI without fully understanding it:** The schema and report were AI-drafted; I still need to review each constraint and explanation so I can defend them independently.

Signed: Yelemes Meyirzhan
Date: 2026-11-15
