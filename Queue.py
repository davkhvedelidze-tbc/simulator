class Queue:
    def __init__(self, sizeQueue: int, numMsg: int):
        """
        Initialize a Queue object.

        Args:
            sizeQueue (int): The maximum size of the queue
            numMsg (int): The current number of messages in the queue
        """
        self.sizeQueue = sizeQueue
        self.numMsg = numMsg
        self.messages = []

    def addMsg(self, message) -> int:
        """
        Add a message to the queue using FIFO principle.
        If the queue is full (reached sizeQueue), no message will be added.

        Args:
            message: The message to add to the queue

        Returns:
            int: 1 if the message was added, 0 otherwise
        """
        # Only add the message if the queue is not full
        if len(self.messages) < self.sizeQueue:
            # Add the new message
            self.messages.append(message)
            self.numMsg += 1
            return 1
        return 0

    def getMsg(self):
        """
        Return the first message in the queue (FIFO principle).
        If the queue is empty, return None.

        Returns:
            The first message in the queue or None if empty
        """
        if self.numMsg > 0 and len(self.messages) > 0:
            self.numMsg -= 1
            return self.messages.pop(0)
        return None
