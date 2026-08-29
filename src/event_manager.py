"""
Professional Event Manager

Features
--------
- No ENTER on first observation
- Temporal confirmation
- Stable occupancy
- Track cleanup
"""

from dataclasses import dataclass


CONFIRM_FRAMES = 3
MAX_MISSING_FRAMES = 30


@dataclass
class TrackState:

    inside: bool

    candidate: bool | None = None

    candidate_count: int = 0

    last_seen: int = 0


class EventManager:

    def __init__(self):

        self.states = {}

    def update(self,
               track_id,
               is_inside,
               frame_number):

        event = None

        # --------------------------
        # First observation
        # --------------------------

        if track_id not in self.states:

            self.states[track_id] = TrackState(

                inside=is_inside,

                last_seen=frame_number

            )

            return None

        state = self.states[track_id]

        state.last_seen = frame_number

        # Nothing changed
        if is_inside == state.inside:

            state.candidate = None

            state.candidate_count = 0

            return None

        # New candidate
        if state.candidate != is_inside:

            state.candidate = is_inside

            state.candidate_count = 1

            return None

        # Same candidate again
        state.candidate_count += 1

        # Not enough confirmations
        if state.candidate_count < CONFIRM_FRAMES:

            return None

        # Confirm transition
        state.inside = is_inside

        state.candidate = None

        state.candidate_count = 0

        if is_inside:

            event = "ENTER"

        else:

            event = "EXIT"

        return event

    def cleanup(self, frame_number):

        remove = []

        for tid, state in self.states.items():

            if frame_number - state.last_seen > MAX_MISSING_FRAMES:

                remove.append(tid)

        for tid in remove:

            del self.states[tid]

    def get_count(self):

        return sum(

            state.inside

            for state in self.states.values()

        )