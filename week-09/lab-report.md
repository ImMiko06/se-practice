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

The definition below was drafted by Codex and reviewed against the checker; it was not typed by me. I checked that the schema has exactly the required five fields and uses only allowed keywords.

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
| name | Exactly `check_room` | A caller looking up this tool by the required name would not find it. |
| description | 25+ words, minutes since midnight, 0–1440, explicitly says it does not save/create a booking | The model could send clock strings or mistake a check for an action that makes a booking. |
| inputSchema | `type: object`; exactly `start`, `end`, `now`, `blocked`, `bookings`; all required; `additionalProperties: false` | Missing values or invented fields could reach the function in an ambiguous shape. |
| start, end, now | Each is an integer in the inclusive range 0–1440 | Strings, fractional minutes, negative values, or times beyond one day could pass. |
| blocked | Boolean | A string such as `"false"` could be confused with the boolean false. |
| bookings | Array of objects; each has required integer `start` and `end` in 0–1440; no extra item keys | A pair/list or incomplete booking would not represent the documented booking shape. Empty arrays remain valid. |

## 3. The twelve calls — first run and final run

The first run was captured with the empty starter schema before I edited it: S01, S02 and S11 passed; the other nine S checks failed. Final S results are from the run after adding the typed object and bounds.

| Case | First run | Final run | What you changed |
| --- | --- | --- | --- |
| S01 | PASS | PASS | Kept valid R1 call shape accepted. |
| S02 | PASS | PASS | Kept an empty bookings array valid. |
| S03 | FAIL | PASS | Made `end` an integer. |
| S04 | FAIL | PASS | Added `now` to required fields. |
| S05 | FAIL | PASS | Forbade extra top-level fields. |
| S06 | FAIL | PASS | Bounded `start` at a minimum of 0. |
| S07 | FAIL | PASS | Bounded `end` at a maximum of 1440. |
| S08 | FAIL | PASS | Required both fields in each booking object. |
| S09 | FAIL | PASS | Made `blocked` a boolean. |
| S10 | FAIL | PASS | Made `start` an integer. |
| S11 | PASS | PASS | Preserved 1440 as a valid end time. |
| S12 | FAIL | PASS | Required each booking item to be an object. |

## 4. Function calling — what the model wrote

I sent the exact deck prompt and the same tool definition to Claude Sonnet 5.5 in three separate fresh chats. The replies below are copied as returned.

### R1

```text
{"name": "check_room", "arguments": {"start": 600, "end": 660, "now": 540, "blocked": false, "bookings": [{"start": 660, "end": 720}]}}
```

Match: yes. The model converted 9:00 to 540, 10:00 to 600, 11:00 to 660, and the existing 11:00–12:00 booking to 660–720. The touching intervals are valid inputs; canBook decides availability.

### R2

```text
{"name": "check_room", "arguments": {"start": 840, "end": 990, "now": 810, "blocked": true, "bookings": []}}
```

Match: yes. The model converted 13:30 to 810, 14:00 to 840 and 16:30 to 990, and used an empty bookings list. This call should be made even though the room is blocked; canBook returns Unavailable.

### R3

```text
Which exact start and end times do you want tomorrow afternoon, and is the room currently blocked? Also, what existing bookings does the room have for tomorrow?
```

The model asked rather than calling. The request lacked exact start and end times, current time, blocked status and existing bookings. Claude asked about times, blocked status and bookings, but omitted the required current time (`now`) from its follow-up. A complete call still needs that value. “Tomorrow” needs no tool argument because the schema has no date field. The model did not invent values.
## 5. What the schema cannot check

The schema can enforce the shape and individual ranges of AC1: `start`, `end`, and `now` must be integer minutes from 0 through 1440. It cannot compare fields, so it cannot enforce `start < end` or `start > now`; those AC1 relationships stay in canBook. AC2 (duration no longer than 120 minutes) also compares `end - start`, which these allowed schema keywords cannot express. AC3 (a blocked room is unavailable) and AC4 (existing bookings do not overlap, with touching allowed) require decision logic over values and intervals. AC5 is a behavior guarantee: the function must not save or mutate bookings; a schema cannot prevent side effects. AC6 is page feedback, which belongs to the UI. The description can explain some of these rules, but explanation does not enforce them.

## 6. Permissions — allow, ask or block

| # | Action | Decision (allow / ask / block) | Reason (the risk, in one sentence or more) |
| --- | --- | --- | --- |
| A1 | call `check_room` with the times the user just typed | allow | The call only checks availability and has no booking side effect; the agent must copy the user’s values instead of guessing missing fields. |
| A2 | read `week-08/app/src/booking.ts` | allow | Reading the project code is reversible and helps verify the actual rules; it does not change the source file. |
| A3 | edit `booking.ts` to raise the 120-minute limit to 180 | ask | This changes an acceptance rule and could invalidate existing tests or course requirements, so the owner must approve the behavior change first. |
| A4 | run `npm test` in `week-08/app` | allow | A scoped test run is useful verification, but the agent should inspect the package script first because npm scripts execute repository code. |
| A5 | run `git reset --hard` to undo its own last three edits | ask | This destroys tracked uncommitted changes, and “its own” edits must be verified before discarding anything that could include the user’s work. |
| A6 | `git commit` its change on the `week-09` branch | ask | A commit records the exact diff in history; the agent should show the diff and get review before creating that checkpoint. |
| A7 | `git push` to `main` | block | A direct push bypasses the required open pull request and review path and could publish an unreviewed change on the shared branch. |
| A8 | send the contents of `.env` to an MCP server it found online | block | `.env` can contain credentials, and sending them to an unknown server could expose accounts or services. |

## 7. Checkpoint

Checkpoint: `35be4c1` (`Week 09: define the check_room schema`). To return to it, run `git reset --hard 35be4c1`. That discards tracked edits and commits after this checkpoint from the current branch/worktree; it does not remove untracked files. I would first confirm that the checkpoint is the intended one and that no later user changes need keeping.

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

Final checker: 30 PASS, 0 FAIL, 0 ERROR. I used one fresh Claude chat for each request and saved its reply as returned. No checker FAIL or ERROR remains.
## 10. Conclusion (80–150 words)

This lab showed me that a tool schema checks the shape of a request, while the booking function decides whether the request makes sense. For example, the schema rejects `end` as the string `"11:00"`, but it cannot compare `start` with `end` or calculate whether a request lasts more than 120 minutes. R2 is a useful example: the model should still send a correctly formed call when `blocked` is true; canBook, not the schema, returns Unavailable. R3 showed why required fields matter: “tomorrow afternoon” does not supply exact minutes, current time, blocked status, or bookings, so asking is safer than guessing. Claude's follow-up still omitted `now`, so another review against the schema was necessary. I would also keep an agent away from `.env` and require review before behavior changes or destructive Git commands.
