import time
from enum import Enum
import Message

class EventType(Enum):
    """Event types enumeration (moved from message.py)."""
    SEND_MSG = "SEND_MSG"
    RECV_MSG = "RECV_MSG"
    MSG_DEPT = "MSG_DEPT"

class Event:
    _id_counter = 0

    def __init__(self,
                 message: Message,
                 event_time: float = None,
                 event_type: str = None):
        self.event_id   = Event._id_counter
        Event._id_counter += 1

        self.message    = message
        self.event_time = event_time if event_time is not None else time.time()
        self.event_type = event_type

    def __del__(self):
        pass

    def get_event_id(self)   -> int:    return self.event_id
    def get_message(self)    -> Message:return self.message
    def get_event_time(self)-> float:  return self.event_time
    def get_event_type(self)-> str:    return self.event_type
    def set_event_time(self, ts: float)  -> None: self.event_time = ts
    def set_event_type(self, et: str)    -> None: self.event_type = et

    def print_event(self) -> None:
        # you could do an analogous table here if desired
        print(self)

    def __str__(self) -> str:
        return (f"Event(id={self.event_id}, message={self.message}, "
                f"time={self.event_time}, type={self.event_type})")