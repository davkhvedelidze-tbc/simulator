import random
from Event import EventType, Event
from Message import Message


class Server:
    def __init__(self):
        """
        Initialize a new Server with a busy status and a random service rate mu.

        The server starts as not busy (busy=False) and with a random mu value.
        """
        self.busy = False
        self.mu = random.randrange(1, 3)  # Initialize with a random value between 1--3

    def setBusy(self, busy: bool) -> None:
        """
        Set the busy status of the server.

        Args:
            busy (bool): The busy status to set
        """
        self.busy = busy

    def getBusy(self) -> bool:
        """
        Get the busy status of the server.

        Returns:
            bool: The current busy status
        """
        return self.busy

    def BeginService(self, msg: Message) -> Event:
        eventTime = random.expovariate(self.mu).__round__(2)
        newEvent = Event(message=msg, event_time=eventTime, event_type=EventType.MSG_DEPT.value)

        self.busy = True
        return newEvent


