# Acceptance criteria — three selected stories

## Assumptions

- **Overlap:** a booking that ends exactly when another begins is allowed under R3, because the two time slots do not actually overlap — one ends at the instant the other starts.
- **Duration:** a booking of exactly two hours is allowed under R2, because the rule says "at most two hours," which includes the boundary value.
- Bookings are evaluated against the server's current time to decide whether the start is "in the future" (R1).

---

## US-02 — Book a room

### AC-01
- **Given** a room is free for the requested time slot and the slot starts in the future
- **When** the Student submits a booking for that room and slot
- **Then** the system creates the booking and marks the slot as reserved

### AC-02
- **Given** the requested slot starts in the past
- **When** the Student submits the booking
- **Then** the system rejects the booking as invalid, citing R1

### AC-03
- **Given** the requested slot duration is longer than two hours
- **When** the Student submits the booking
- **Then** the system rejects the booking because it exceeds the maximum duration allowed by R2

### AC-04
- **Given** another booking already exists for the same room that overlaps the requested slot
- **When** the Student submits the booking
- **Then** the system rejects the booking as an overlap under R3

### AC-05
- **Given** the room is currently blocked by an Administrator
- **When** the Student submits a booking for that room
- **Then** the system rejects the booking because a blocked room cannot be booked, per R4

---

## US-03 — Cancel a booking

### AC-06
- **Given** the Student has an existing future booking
- **When** the Student cancels that booking
- **Then** the system releases the reservation and the slot becomes available again

### AC-07
- **Given** the booking the Student is trying to cancel does not exist or already started
- **When** the Student attempts to cancel it
- **Then** the system denies the cancellation and reports that the booking cannot be cancelled

### AC-08
- **Given** the Student has successfully cancelled a booking
- **When** the cancellation completes
- **Then** the system sends a cancellation confirmation per UC-06

---

## US-04 — Block a room

### AC-09
- **Given** a room is currently usable and has no active bookings that would be affected
- **When** the Administrator blocks the room
- **Then** the system marks the room as blocked and it no longer appears as available

### AC-10
- **Given** a room is already blocked
- **When** a Student attempts to book it
- **Then** the system prevents the booking because a blocked room cannot be booked, per R4

### AC-11
- **Given** a non-Administrator (a Student) attempts to block a room
- **When** the block action is submitted
- **Then** the system rejects the action because only an Administrator is authorized to change a room's blocked status
