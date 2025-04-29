
import time
from enum import Enum


# class EventType(Enum):
#     """Event types enumeration."""
#     SEND_MSG = "SEND_MSG"
#     RECV_MSG = "RECV_MSG"
#     MSG_DEPT = "MSG_DEPT"

# class Message:
#     _id_counter = 0

#     def __init__(self, source: str, destination: str, payload=None):
#         self.message_id = Message._id_counter
#         Message._id_counter += 1

#         self.source = source
#         self.destination = destination
#         self.payload = payload

#         self.timestamp = time.time()

#     def get_message_id(self) -> int:
#         return self.message_id

#     def get_source(self) -> str:
#         return self.source

#     def get_destination(self) -> str:
#         return self.destination

#     def get_payload(self):
#         return self.payload

#     def get_timestamp(self) -> float:
#         return self.timestamp

#     def set_payload(self, payload) -> None:
#         self.payload = payload

#     def __str__(self) -> str:
#         return (f"Message(id={self.message_id}, source='{self.source}', "
#                 f"destination='{self.destination}', payload={self.payload}, "
#                 f"timestamp={self.timestamp})")

#     def print_message(self):
#         print(self)


# if __name__ == "__main__":
#     message = Message(source="Client1", destination="Server1", payload="Hello, Server!")
#     print(message)



import time

class Message:
    _id_counter = 0

    def __init__(self, source: str, destination: str, payload=None):
        self.message_id  = Message._id_counter
        Message._id_counter += 1

        self.source      = source
        self.destination = destination
        self.payload     = payload
        self.timestamp   = time.time()

    def get_message_id(self) -> int:    return self.message_id
    def get_source(self)     -> str:    return self.source
    def get_destination(self)-> str:    return self.destination
    def get_payload(self):              return self.payload
    def get_timestamp(self)  -> float:  return self.timestamp
    def set_payload(self, payload) -> None:
        self.payload = payload

    def __str__(self) -> str:
        return (f"Message(id={self.message_id}, source='{self.source}', "
                f"destination='{self.destination}', payload={self.payload}, "
                f"timestamp={self.timestamp})")

    def print_message(self) -> None:
        # Build table headers and values
        headers = ["message_id", "source", "destination", "payload", "timestamp"]
        vals    = [str(self.message_id),
                   self.source,
                   self.destination,
                   str(self.payload),
                   f"{self.timestamp:.6f}"]

        # Compute column widths
        col_w = [max(len(h), len(v)) for h, v in zip(headers, vals)]

        # Build border line
        border = "+" + "+".join("-"*(w+2) for w in col_w) + "+"

        # Build header row
        header_row = "|" + "|".join(f" {h.ljust(w)} " for h, w in zip(headers, col_w)) + "|"
        value_row  = "|" + "|".join(f" {v.ljust(w)} " for v, w in zip(vals,   col_w)) + "|"

        # Print the table
        print(border)
        print(header_row)
        print(border)
        print(value_row)
        print(border)