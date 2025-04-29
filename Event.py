import time

class Event:
    _id_counter = 0

    def __init__(self, message, event_time: float = None, event_type: str = None):
        self.event_id = Event._id_counter
        Event._id_counter += 1

        self.message = message
        self.event_time = event_time if event_time is not None else time.time()
        self.event_type = event_type

    def __del__(self):
        # Optional cleanup logic
        pass

    def get_event_id(self) -> int:
        return self.event_id

    def get_message(self):
        return self.message

    def get_event_time(self) -> float:
        return self.event_time

    def get_event_type(self) -> str:
        return self.event_type

    def set_event_time(self, timestamp: float) -> None:
        self.event_time = timestamp

    def set_event_type(self, event_type: str) -> None:
        self.event_type = event_type

    def print_event(self) -> None:
        print(self)

    def __str__(self) -> str:
        return (f"Event(id={self.event_id}, message={self.message}, "
                f"time={self.event_time}, type={self.event_type})")

