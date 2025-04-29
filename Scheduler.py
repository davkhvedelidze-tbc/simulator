from __future__ import annotations

from Event import Event

class Scheduler:
    """
    Scheduler for events: maintains a chronological queue of Event objects.

    Methods:
    +--------------+----------------------------------------------------------+
    | __init__     | Initialize empty event list                              |
    | add_event    | Insert an Event into the list in ascending time order    |
    | get_event    | Pop and return the next Event (earliest time)            |
    | get_current_time | Peek at the next Event’s timestamp                   |
    +--------------+----------------------------------------------------------+
    """
    def __init__(self):
        self.events: list[Event] = []

    def add_event(self, event: Event) -> None:
        """Insert `event` so that self.events stays sorted by event_time."""
        et = event.get_event_time()
        # fast path: append if it belongs at the end
        if not self.events or et >= self.events[-1].get_event_time():
            self.events.append(event)
            return
        # otherwise find first slot where new event is earlier
        for i, existing in enumerate(self.events):
            if et < existing.get_event_time():
                self.events.insert(i, event)
                return

    def get_event(self) -> Event | None:
        """
        Remove and return the earliest Event.
        Returns None if no events are scheduled.
        """
        if not self.events:
            return None
        return self.events.pop(0)

    def get_current_time(self) -> float | None:
        """
        Return the timestamp of the next Event without removing it.
        Returns None if the queue is empty.
        """
        if not self.events:
            return None
        return self.events[0].get_event_time()