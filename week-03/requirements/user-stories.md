# User stories — Smart Campus study room booking

6 to 8 stories. Keep the shape exactly: ID, the As/I want/so that sentence, a priority, one
assumption. Roles are **Student** or **Administrator** only.

---

### US-01
**Story:** As a Student, I want to view real-time room availability, so that I can find a free room quickly.
**Priority:** High
**Assumption:** Availability is shown at least by room and time slot for the current day.

### US-02
**Story:** As a Student, I want to book a free room for a specific time slot, so that I can guarantee myself a study space.
**Priority:** High
**Assumption:** A student can hold only one active booking per time slot.

### US-03
**Story:** As a Student, I want to cancel my booking, so that I free up the room for others if my plans change.
**Priority:** Medium
**Assumption:** Cancellation is allowed any time before the booking starts.

### US-04
**Story:** As an Administrator, I want to block a room that is out of service, so that students cannot book a room that isn't usable.
**Priority:** High
**Assumption:** Only an Administrator can change a room's blocked status.

### US-05
**Story:** As an Administrator, I want to unblock a room once it is usable again, so that students can resume booking it.
**Priority:** Medium
**Assumption:** Unblocking is a separate, explicit action from blocking.

### US-06
**Story:** As an Administrator, I want to review room usage over a period, so that I can understand demand patterns and plan capacity.
**Priority:** Low
**Assumption:** Usage data covers at least booking counts per room over a selectable date range.

### US-07
**Story:** As a Student, I want to get a confirmation after I book or cancel a room, so that I know the system registered my action.
**Priority:** Medium
**Assumption:** The confirmation is triggered automatically by the system right after UC-02 or UC-03 completes, not by a separate student action.