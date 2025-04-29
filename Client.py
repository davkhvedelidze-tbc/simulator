import random
import time
from Message import Message

class Client:
    _id_counter = 0

    def __init__(self, lam: float):
        """Initialize a new Client with exponential inter-arrival rate lambda."""
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

    def get_msg(self):
        return self.msg

    def set_msg(self, msg: Message) -> None:
        self.msg = msg

    def send_msg(self, destination: str, payload=None):
        """
        Generate a new Message from this client, schedule next inter-arrival.

        :param destination: Target entity identifier
        :param payload: Optional payload content
        :return: Tuple(Message, float) with generated Message and inter-arrival time
        """
        # Generate inter-arrival time
        inter_arrival = random.expovariate(self.lam)
        # Create the message
        msg = Message(source=str(self.client_id), destination=destination, payload=payload)
        # Simulated timestamp advancement
        msg.timestamp = time.time() + inter_arrival
        self.msg = msg
        return msg, inter_arrival