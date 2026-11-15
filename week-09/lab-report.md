# Week 09 — Lab Report: canBook as a Tool

**Name:** Yelemes Meyirzhan  
**Student ID:** 24B031740  
**GitHub:** ImMiko06

---

## 1. Setup

| | |
| --- | --- |
| Assistant (frozen for the whole lab) | ChatGPT Codex desktop |
| Exact model (or "not displayed") | 6 Luna (Medium; exact model name was not shown in the UI) |
| Three fresh chats for R1, R2, R3? (yes / no) | no — the calls were produced in the existing Codex chat, not three fresh chats |
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

These are the Codex-generated replies saved for the exercise. They were drafted in the existing chat and transcribed into the files; I did not open three fresh chats or capture independent reply transcripts, so the fresh-chat and verbatim-transcript requirements were not met.

### R1

```text
{
  "name": "check_room",
  "arguments": {
    "start": 600,
    "end": 660,
    "now": 540,
    "blocked": false,
    "bookings": [
      { "start": 660, "end": 720 }
    ]
  }
}
```

Match: yes. 9:00 = 540, 10:00 = 600, 11:00 = 660, and the existing 11:00–12:00 booking is 660–720. The intervals touch, so the request is still a valid tool call; canBook decides availability.

### R2

```text
{
  "name": "check_room",
  "arguments": {
    "start": 840,
    "end": 990,
    "now": 810,
    "blocked": true,
    "bookings": []
  }
}
```

Match: yes. 13:30 = 810, 14:00 = 840, 16:30 = 990, and there are no bookings. The call should be made even though the room is blocked; canBook will return Unavailable.

### R3

```text
What exact start and end times, current time, blocked status, and existing bookings should I use?
```

The request does not give exact clock times for “afternoon” or “a couple of hours,” the current time, blocked status, or the existing bookings. The model asked instead of inventing values. It also did not follow the requested one-JSON-or-one-question distinction? It correctly used a short question, which is allowed when required values are missing.

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

Pending final run.

## 9. What still fails

The process requirement for three fresh chats is not satisfied: I used the current Codex chat and transcribed its generated calls. This is a process limitation not measured by the structural checker, so it remains disclosed even if all 30 checker rows pass.

## 10. Conclusion (80–150 words)

This lab showed me that a tool schema checks the shape of a request, while the booking function decides whether the request makes sense. For example, the schema rejects `end` as the string `"11:00"`, but it cannot compare `start` with `end` or calculate whether a request lasts more than 120 minutes. R2 is a useful example: the model should still send a correctly formed call when `blocked` is true; canBook, not the schema, returns Unavailable. R3 showed why required fields matter: “tomorrow afternoon” does not supply exact minutes, current time, blocked status, or bookings, so asking is safer than guessing. I would also keep an agent away from `.env` and require review before behavior changes or destructive Git commands.

