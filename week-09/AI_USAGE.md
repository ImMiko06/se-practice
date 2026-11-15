# AI Usage Disclosure — Week 09

Required by the course academic policy (Generative AI use level **D — AI-integrated**).
I am responsible for checking, understanding, and defending the work submitted.

| Tool | Exact model / plan | Used for | Which files it touched |
| --- | --- | --- | --- |
| ChatGPT Codex desktop | UI label: 6 Luna (Medium) | Drafted and reviewed the JSON Schema definition; generated the R1/R2 call JSON and R3 clarification reply in the existing chat; helped draft the report and declaration. Calls were not generated in three fresh chats. | tool/check_room.json, calls/r1.json, calls/r2.json, calls/r3.txt, lab-report.md, AI_USAGE.md, submission.yml |

**I wrote `tool/check_room.json` myself:** no. Codex drafted it; I reviewed its fields, ranges, allowed keywords and checker results.

**I used an AI to explain a JSON Schema keyword or a check:** yes. Codex explained why integer/range constraints catch malformed inputs and why cross-field rules such as `start < end` remain in canBook.

**Every reply in `calls/` and in lab-report.md section 4 is exactly what the model returned:** no. Codex generated the call content in this existing thread and transcribed it; I did not capture raw replies from three fresh chats.

**Every terminal output in lab-report.md was pasted from a real run, unedited:** yes. Section 8 contains the final checker output.

**Anything I accepted from the AI without fully understanding it:** I have not yet confirmed that I can explain every schema keyword and each conclusion in the report; I will review them before submitting.

Signed: Yelemes Meyirzhan
Date: 2026-11-15

