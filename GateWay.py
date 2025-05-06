from Event import EventType, Event
from Message import Message
from Server import Server
from Queue import Queue

class GateWay:
    def __init__(self, numServers: int, queueSize: int):
        """
        Initialize a GateWay object.

        Args:
            numServers (int): The number of servers in the gateway
            queueSize (int): The maximum size of the queue
        """
        self.numServers = numServers
        self.droppedMsg = 0  # Initialize counter for dropped messages

        # Initialize metrics
        self.totalQueueDelay = 0.0
        self.totalServerDelay = 0.0
        self.totalMessagesServed = 0
        self.totalMessagesDropped = 0

        # Dictionary to store message entry times
        self.messageEntryTimes = {}
        self.messageServiceTimes = {}

        self.servers = [Server() for _ in range(numServers)]

        # Initialize a Queue object
        self.queue = Queue(sizeQueue=queueSize, numMsg=0)


    def ReceiveMsg(self, msg: Message) -> None:
        """
        Receive a message in the gateway.

        Args:
            msg (Message): The message to receive
        """
        # First check if any server is not busy
        for server in self.servers:
            if not server.getBusy():
                # If a server is not busy, call its BeginService method
                event = server.BeginService(msg)
                # Record the time when the message starts being served
                self.messageServiceTimes[msg.get_message_id()] = event.get_event_time()
                return

        # If all servers are busy, add the message to the queue
        if self.queue.addMsg(msg) == 1:
            # Record the time when the message enters the queue
            self.messageEntryTimes[msg.get_message_id()] = msg.get_timestamp()
        else:
            # If the message couldn't be added to the queue (queue is full), increment dropped messages
            self.droppedMsg += 1
            self.totalMessagesDropped += 1

    def getNumServers(self) -> int:
        """
        Get the number of servers in the gateway.

        Returns:
            int: The number of servers
        """
        return self.numServers

    def getNumMsg(self) -> int:
        """
        Get the current number of messages in the gateway.

        Returns:
            int: The number of messages
        """
        return self.queue.numMsg

    def getDroppedMsg(self) -> int:
        """
        Get the number of dropped messages in the gateway.

        Returns:
            int: The number of dropped messages
        """
        return self.droppedMsg

    def getAverageQueueDelay(self) -> float:
        """
        Get the average delay in queue.

        Returns:
            float: The average delay in queue, or 0 if no messages have been served
        """
        if self.totalMessagesServed == 0:
            return 0.0
        return self.totalQueueDelay / self.totalMessagesServed

    def getAverageServerDelay(self) -> float:
        """
        Get the average delay in server.

        Returns:
            float: The average delay in server, or 0 if no messages have been served
        """
        if self.totalMessagesServed == 0:
            return 0.0
        return self.totalServerDelay / self.totalMessagesServed

    def getAverageMessagesServed(self) -> float:
        """
        Get the average number of messages served.

        Returns:
            float: The average number of messages served
        """
        return self.totalMessagesServed

    def getAverageMessagesDropped(self) -> float:
        """
        Get the average number of messages dropped.

        Returns:
            float: The average number of messages dropped
        """
        return self.totalMessagesDropped

    def departureMsg(self, msg: Message) -> None:
        """
        Process the departure of a message from the gateway.

        Args:
            msg (Message): The message to depart
        """
        # Check if all servers are busy
        all_servers_busy = all(server.getBusy() for server in self.servers)

        # Calculate delays and update metrics for the departing message
        msg_id = msg.get_message_id()
        current_time = msg.get_timestamp()

        # Update server delay if we have a service time for this message
        if msg_id in self.messageServiceTimes:
            service_time = self.messageServiceTimes[msg_id]
            server_delay = current_time - service_time
            self.totalServerDelay += server_delay
            del self.messageServiceTimes[msg_id]

        # Update queue delay if we have an entry time for this message
        if msg_id in self.messageEntryTimes:
            entry_time = self.messageEntryTimes[msg_id]
            queue_delay = service_time - entry_time if 'service_time' in locals() else 0
            self.totalQueueDelay += queue_delay
            del self.messageEntryTimes[msg_id]

        # Increment the total messages served counter
        self.totalMessagesServed += 1

        # Display metrics
        print(f"Total Queue Delay: {self.totalQueueDelay}")
        print(f"Total Server Delay: {self.totalServerDelay}")
        print(f"Total Messages Served: {self.totalMessagesServed}")
        print(f"Total Messages Dropped: {self.totalMessagesDropped}")

        # Find a busy server and mark it as not busy
        for server in self.servers:
            if server.getBusy():

                # Check if there are messages in the queue
                message = self.queue.getMsg()

                # If a message was retrieved, process it
                if message is not None:
                    # Process the next message
                    event = server.BeginService(message)
                    # Record the time when the message starts being served
                    self.messageServiceTimes[message.get_message_id()] = event.get_event_time()

                return

        # If no busy server was found, just try to get a message from the queue
        message = self.queue.getMsg()

        # If a message was retrieved, process it
        if message is not None:
            # Find a non-busy server to process the message
            for server in self.servers:
                if not server.getBusy():
                    event = server.BeginService(message)
                    # Record the time when the message starts being served
                    self.messageServiceTimes[message.get_message_id()] = event.get_event_time()
                    break
