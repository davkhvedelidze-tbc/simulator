import random
import time
from Message import Message
from Event import Event, EventType

class Client:
    _id_counter = 0

    def __init__(self, lam: float):
        """Initialize a new Client with exponential inter-arrival rate λ."""
        self.client_id = Client._id_counter
        Client._id_counter += 1

        self.lam = lam
        self.msg = None

    def get_client_id(self) -> int:
        return self.client_id

    def get_lambda(self) -> float:
        return self.lam

    def set_lambda(self, lam: float) -> None:
        self.lam = lam

    def get_msg(self) -> Message:
        return self.msg

    def set_msg(self, msg: Message) -> None:
        self.msg = msg

    def send_msg(self, destination: str, payload=None):
        """
        Generate a new Message and schedule next inter-arrival.
        Returns (Message, inter_arrival_time).
        """
        inter_arrival = random.expovariate(self.lam)
        msg = Message(source=str(self.client_id + 1),  # IDs start at 1
                      destination=destination,
                      payload=payload)
        # assign simulated timestamp
        msg.timestamp = time.time() + inter_arrival
        self.msg = msg
        return msg, inter_arrival

    def start(self, destination: str, payload=None) -> Event:
        """
        Kick off this client's first event:
        calls send_msg() and wraps result in a SEND_MSG Event.
        """
        msg, _ = self.send_msg(destination, payload)
        evt = Event(
            message=msg,
            event_time=msg.get_timestamp(),
            event_type=EventType.SEND_MSG.value
        )
        return evt