# import time

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
from enum import Enum


class EventType(Enum):
    """Event types enumeration."""
    SEND_MSG = "SEND_MSG"
    RECV_MSG = "RECV_MSG"
    MSG_DEPT = "MSG_DEPT"

class Message:
    _id_counter = 0

    def __init__(self, source: str, destination: str, payload=None):
        self.message_id = Message._id_counter
        Message._id_counter += 1

        self.source = source
        self.destination = destination
        self.payload = payload

        self.timestamp = time.time()

    def get_message_id(self) -> int:
        return self.message_id

    def get_source(self) -> str:
        return self.source

    def get_destination(self) -> str:
        return self.destination

    def get_payload(self):
        return self.payload

    def get_timestamp(self) -> float:
        return self.timestamp

    def set_payload(self, payload) -> None:
        self.payload = payload

    def __str__(self) -> str:
        return (f"Message(id={self.message_id}, source='{self.source}', "
                f"destination='{self.destination}', payload={self.payload}, "
                f"timestamp={self.timestamp})")

    def print_message(self):
        print(self)


if __name__ == "__main__":
    message = Message(source="Client1", destination="Server1", payload="Hello, Server!")
    print(message)