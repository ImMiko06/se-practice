# Week 09 — Lab Report: canBook as a Tool

**Name:** Yelemes Meyirzhan  
**Student ID:** 24B031740  
**GitHub:** ImMiko06

---

## 1. Setup

| | |
| --- | --- |
| Assistant (frozen for Part 2) | Claude desktop/web |
| Exact model (or "not displayed") | Sonnet 5.5 (Medium; Free plan) |
| Three fresh chats for R1, R2, R3? (yes / no) | yes — one new Claude chat per request |
| Python version (`python --version`) | Python 3.13.0 |

## 2. Your tool definition — a reason for every constraint

Codex drafted the `check_room` tool definition below. I reviewed its fields, ranges, allowed keywords, and checker results; the AI assistance is recorded in `AI_USAGE.md`.

```json
{
  "name": "check_room",
  "description": "Checks whether a requested room booking is available under the Smart Campus rules. All times are whole minutes since midnight, from 0 to 1440 inclusive (24:00). Provide the requested start and end, current time, blocked status, and existing bookings. This tool only checks availability; it does not create, change, or save a booking.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "start": { "type": "integer", "minimum": 0, "maximum": 1440, "description": "Requested start time as whole minutes since midnight." },
      "end": { "type": "integer", "minimum": 0, "maximum": 1440, "description": "Requested end time as whole minutes since midnight; 1440 means 24:00." },
      "now": { "type": "integer", "minimum": 0, "maximum": 1440, "description": "Current time as whole minutes since midnight." },
      "blocked": { "type": "boolean", "description": "Whether the room is blocked." },
      "bookings": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "start": { "type": "integer", "minimum": 0, "maximum": 1440 },
            "end": { "type": "integer", "minimum": 0, "maximum": 1440 }
          },
          "required": ["start", "end"],
          "additionalProperties": false
        },
        "description": "Existing bookings, each with start and end whole minutes; may be empty."
      }
    },
    "required": ["start", "end", "now", "blocked", "bookings"],
    "additionalProperties": false
  }
}
```

| Field | Constraint | What goes wrong without it |
| --- | --- | --- |
| name | Exactly `check_room` | A caller or client looking up the tool by its expected name would fail to resolve it. |
| description | 25+ words, mentions minutes since midnight, 0–1440 range, and states that it does not save/create a booking | The model might pass formatted clock strings like `"11:00"` or assume calling the tool reserves the room. |
| inputSchema | `type: object`; only `start`, `end`, `now`, `blocked`, `bookings`; all required; `additionalProperties: false` | Required arguments could be omitted or hallucinated fields (like `room`) could be passed into the handler. |
| start, end, now | Each is an `integer` with `minimum: 0` and `maximum: 1440` | Strings, decimal minutes, negative numbers, or values past 24:00 would slip past validation. |
| blocked | `boolean` | String values such as `"false"` could be accepted and misread as truthy in code. |
| bookings | `array` of objects, each requiring integer `start` and `end` (0–1440) with `additionalProperties: false` | Malformed pairs like `[660, 720]` or partial booking objects would break the expected structure, while `[]` remains valid. |

## 3. The twelve calls — first run and final run

My first run of `check_tool.py` was executed against the initial empty starter schema before adding any properties or constraints: only S01, S02, and S11 passed (since an empty schema accepts any object), while the remaining nine S checks failed. After defining the full typed schema and bounds, all twelve cases passed.

| Case | First run | Final run | What you changed |
| --- | --- | --- | --- |
| S01 | PASS | PASS | Preserved acceptance of a valid R1 call payload. |
| S02 | PASS | PASS | Allowed `bookings` to be an empty array `[]`. |
| S03 | FAIL | PASS | Restricted `end` to `integer` so string `"11:00"` is rejected. |
| S04 | FAIL | PASS | Listed `now` in top-level `required` fields. |
| S05 | FAIL | PASS | Set `additionalProperties: false` at top level to reject extra keys like `room`. |
| S06 | FAIL | PASS | Added `minimum: 0` on `start` to block negative values (`-30`). |
| S07 | FAIL | PASS | Added `maximum: 1440` on `end` to block values beyond midnight (`1500`). |
| S08 | FAIL | PASS | Made both `start` and `end` required inside each `bookings` item object. |
| S09 | FAIL | PASS | Typed `blocked` as `boolean` so string `"false"` is refused. |
| S10 | FAIL | PASS | Typed `start` as `integer` so fractional minutes (`600.5`) are refused. |
| S11 | PASS | PASS | Kept `maximum: 1440` inclusive so `end: 1440` (24:00) is accepted. |
| S12 | FAIL | PASS | Defined `bookings` items as `type: "object"` so array pairs `[660, 720]` are refused. |

## 4. Function calling — what the model wrote

The tool definition was tested with Claude Sonnet 5.5 in three separate fresh chats. The exact prompt was used each time, and the replies were saved unedited.

### R1

```text
{"name": "check_room", "arguments": {"start": 600, "end": 660, "now": 540, "blocked": false, "bookings": [{"start": 660, "end": 720}]}}
```

Match: yes. Claude accurately converted 9:00 to 540, 10:00 to 600, 11:00 to 660, and the existing 11:00–12:00 booking to `[{"start": 660, "end": 720}]`. Touching intervals are structurally valid inputs and left for `canBook` to evaluate.

### R2

```text
{"name": "check_room", "arguments": {"start": 840, "end": 990, "now": 810, "blocked": true, "bookings": []}}
```

Match: yes. Claude converted 13:30 to 810, 14:00 to 840, and 16:30 to 990, set `blocked` to `true`, and passed an empty `bookings` array. Generating the tool call is the right behavior here even though the room is blocked, because determining `Unavailable` belongs to `canBook`.

### R3

```text
Which exact start and end times do you want tomorrow afternoon, and is the room currently blocked? Also, what existing bookings does the room have for tomorrow?
```

The model asked a clarifying question instead of making a tool call. Because the request ("tomorrow afternoon for a couple of hours") lacked exact start and end times, current time, blocked status, and existing bookings, Claude refused to guess values. Notably, while it asked for the time interval, blocked status, and existing bookings, it forgot to ask for the current time (`now`), which is also required by the schema. No date argument was requested because the schema operates purely on minutes within a single day.

## 5. What the schema cannot check

JSON Schema validates data types, required keys, and independent numeric bounds, so it can only enforce the structural shape of **AC1** (`start`, `end`, and `now` as integers in `0..1440`). It cannot perform cross-field comparisons, which means checking `start < end` and `start > now` (**AC1**) as well as verifying that duration `end - start <= 120` (**AC2**) must stay inside `canBook`. Likewise, checking whether `blocked` is true (**AC3**) or detecting interval overlaps against `bookings` while permitting touching boundaries (**AC4**) requires domain logic that static schema keywords cannot express. Finally, **AC5** (guaranteeing no state mutation or side effects) is a runtime implementation contract, and **AC6** (rendering UI feedback) belongs to the frontend layer.

## 6. Permissions — allow, ask or block

| # | Action | Decision (allow / ask / block) | Reason (the risk, in one sentence or more) |
| --- | --- | --- | --- |
| A1 | call `check_room` with the times the user just typed | allow | Checking availability is a read-only operation with no side effects, provided the agent uses the user's explicit values without guessing missing fields. |
| A2 | read `week-08/app/src/booking.ts` | allow | Inspecting existing repository source code is non-destructive and lets the agent verify actual booking rules before answering questions. |
| A3 | edit `booking.ts` to raise the 120-minute limit to 180 | ask | Modifying core acceptance criteria alters business requirements and breaks existing tests, so explicit human approval is required first. |
| A4 | run `npm test` in `week-08/app` | allow | Running the local test suite verifies code health without modifying tracked files, though the test script itself should be standard and trusted. |
| A5 | run `git reset --hard` to undo its own last three edits | ask | A hard reset permanently wipes uncommitted changes in the working tree and could destroy user work alongside the agent's edits. |
| A6 | `git commit` its change on the `week-09` branch | ask | Creating a commit writes permanent history to the branch, so I should inspect the diff before approving the commit. |
| A7 | `git push` to `main` | block | Pushing directly to `main` bypasses the mandatory pull request and code review workflow and risks corrupting the protected branch. |
| A8 | send the contents of `.env` to an MCP server it found online | block | Exfiltrating `.env` to an untrusted external server leaks API keys, tokens, and private credentials. |

## 7. Checkpoint

Checkpoint commit: `35be4c1` (`Week 09: define the check_room schema`). To restore the repository to this exact state if an agent makes unwanted edits, run:

```bash
git reset --hard 35be4c1
```

This command discards all uncommitted modifications to tracked files and resets the branch pointer, throwing away any commits made after `35be4c1` (while leaving untracked files untouched). Before running it, I would check `git status` and `git diff` to ensure no manual work of my own is lost.

## 8. Checker output

```text
PASS  D1    tool/check_room.json exists and is valid JSON
PASS  D2    has name, description and inputSchema
PASS  D3    name is exactly "check_room"
PASS  D4    description: 25+ words, says minutes, 1440, and that it does not save
PASS  D5    inputSchema: an object with exactly the five fields, all required
PASS  D6    inputSchema uses only the keywords listed in README section 5
PASS  S01   the R1 call, valid -> accept
PASS  S02   no existing bookings: bookings = [] -> accept
PASS  S03   end as a string: "11:00" -> refuse
PASS  S04   now missing -> refuse
PASS  S05   an extra field: "room": "204" -> refuse
PASS  S06   start below the day: -30 -> refuse
PASS  S07   end beyond the day: 1500 -> refuse
PASS  S08   a booking with no end: {start: 660} -> refuse
PASS  S09   blocked as a string: "false" -> refuse
PASS  S10   start not a whole minute: 600.5 -> refuse
PASS  S11   end at the end of the day: 1440 -> accept
PASS  S12   a booking as a pair: [660, 720] -> refuse
PASS  F1    calls\r1.json: a call to check_room
PASS  F2    calls\r1.json: arguments valid against your schema
PASS  F3    calls\r1.json: arguments equal the expected ones (README section 5, Part 2)
PASS  F4    calls\r2.json: a call to check_room
PASS  F5    calls\r2.json: arguments valid against your schema
PASS  F6    calls\r2.json: arguments equal the expected ones (README section 5, Part 2)
PASS  F7    calls/r3: exactly one of r3.json (it called) or r3.txt (it asked), not empty
PASS  L1    section 5 names at least two acceptance criteria (AC1-AC6) the schema cannot check
PASS  L2    section 6: A1-A8 each have allow / ask / block and a reason of 5+ words
PASS  L3    section 7 names the checkpoint commit (a SHA)
PASS  L4    section 10: a conclusion of 80-150 words
PASS  L5    AI_USAGE.md filled in (a tool row, and signed)

SUMMARY: 30 PASS · 0 FAIL · 0 ERROR  (of 30 checks)
Paste this whole output into lab-report.md section 8, and these three numbers into submission.yml.
```

## 9. What still fails

Final checker run: 30 PASS, 0 FAIL, 0 ERROR. All three function-calling replies were generated in fresh Claude chats and saved without edits. No failing or error checks remain.

## 10. Conclusion (80–150 words)

Working through this lab clarified the boundary between schema validation and application logic. While `inputSchema` prevents malformed calls—such as rejecting `"11:00"` as a string or out-of-range minutes—it cannot compare `start` against `end` or enforce the 120-minute duration cap, which must remain in `canBook`. Testing the three prompts showed how a model handles valid and incomplete inputs: in R2, Claude properly emitted a tool call even with `blocked: true`, leaving the `Unavailable` decision to the function, whereas in R3 it avoided guessing missing values and asked for clarification, though it overlooked `now`. Finally, defining agent permissions highlighted why read-only checks can be allowed automatically while rule changes, destructive resets, and `.env` access require strict controls.
