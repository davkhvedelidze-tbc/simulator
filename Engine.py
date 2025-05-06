# Engine.py

import random
from Message import Message
from Queue import Queue
from Trace import Trace
from Event import Event, EventType
from Scheduler import Scheduler
from Client import Client
from Server import Server
from GateWay import GateWay


class Engine:
    def __init__(self,
                 n_clients: int = 3,
                 num_sources: int = 2,
                 simulation_time: float = 10.0,
                 lam: float = 4.0,
                 mu: float = 8.0,
                 transmission_delay=1.0
                 ):
        # Main parameters
        self.n_clients = n_clients
        self.simulation_time = simulation_time
        self.lam = lam  # client arrival rate
        self.mu = mu  # gateway service rate

        # Gateways numbered from 1..num_sources
        self.sources = [str(i + 1) for i in range(num_sources)]

        # Components
        self.scheduler = Scheduler()
        self.clients = []
        self.traces = []

    def Test_msg(self) -> None:
        """Demonstrate basic Message usage."""
        print("\n--- Test_msg ---")
        msg = Message(source="1", destination="2", payload="Example")
        print(f"Message ID:  {msg.get_message_id()}")
        print(f"Source:      {msg.get_source()}")  # prints "1"
        print(f"Destination: {msg.get_destination()}")  # prints "2"
        msg.print_message()

    def Test_event(self) -> None:
        """Demonstrate basic Event usage."""
        print("\n--- Test_event ---")
        msg = Message(source="1", destination="2", payload="EvtPayload")
        event = Event(message=msg, event_type=EventType.SEND_MSG.value)
        event.set_event_time(msg.get_timestamp())
        event.print_event()

    def Test_Queue(self) -> None:
        """Test the Queue class functionality."""
        print("\n--- Test_Queue ---")
        queue = Queue(sizeQueue=3, numMsg=0)

        # Create test messages
        msg1 = Message(source="Client1", destination="Server1", payload="Message 1")
        msg2 = Message(source="Client2", destination="Server2", payload="Message 2")
        msg3 = Message(source="Client3", destination="Server3", payload="Message 3")
        msg4 = Message(source="Client4", destination="Server4", payload="Message 4")

        # Test 1: Add messages to the queue
        print("\nAdding 3 messages to the queue (capacity: 3)")
        queue.addMsg(msg1)
        queue.addMsg(msg2)
        queue.addMsg(msg3)
        print(f"Queue size after adding 3 messages: {queue.numMsg}")

        # Test 2: Try to add a message when the queue is full
        print("\nTrying to add a 4th message (should not be added)")
        queue.addMsg(msg4)
        print(f"Queue size after trying to add 4th message: {queue.numMsg}")

        # Test 3: Retrieve messages in FIFO order
        print("\nRetrieving messages in FIFO order:")
        first_msg = queue.getMsg()
        print("First message retrieved:")
        if first_msg:
            first_msg.print_message()
            print(f"Queue size after retrieving first message: {queue.numMsg}")

        second_msg = queue.getMsg()
        print("\nSecond message retrieved:")
        if second_msg:
            second_msg.print_message()
            print(f"Queue size after retrieving second message: {queue.numMsg}")

        third_msg = queue.getMsg()
        print("\nThird message retrieved:")
        if third_msg:
            third_msg.print_message()
            print(f"Queue size after retrieving third message: {queue.numMsg}")

        # Test 4: Try to retrieve from an empty queue
        print("\nTrying to retrieve from an empty queue (should return None)")
        empty_msg = queue.getMsg()
        print(f"Result of retrieving from empty queue: {empty_msg}")
        print(f"Queue size: {queue.numMsg}")

    def Test_Server(self) -> None:
        """Test the Server class functionality."""
        print("\n--- Test_Server ---")
        server = Server()
        current_time = 0.0

        # Create a message
        msg1 = Message(source="Client1", destination="Server1", payload="Message 1")
        print("\nCreated message:")
        msg1.print_message()

        # Call BeginService with the message
        print("\nCalling BeginService with the message...")
        event1 = server.BeginService(msg1)
        print(f"Returned event with type: {event1.get_event_type()}")

        # Update the current time and add the event to the scheduler
        current_time += event1.get_event_time()
        # event1.set_event_time(current_time)
        self.scheduler.add_event(event1)
        print(f"Added event to scheduler with updated time: {current_time}")

        # Create another message
        msg2 = Message(source="Client2", destination="Server2", payload="Message 2")
        print("\nCreated another message:")
        msg2.print_message()

        # Call BeginService again with the new message
        print("\nCalling BeginService with the new message...")
        event2 = server.BeginService(msg2)
        print(f"Returned event with type: {event2.get_event_type()}")

        # Update the current time and add the event to the scheduler
        current_time += event2.get_event_time()
        self.scheduler.add_event(event2)
        print(f"Added event to scheduler with updated time: {event2.get_event_time()}")

        # Get and print the events from the scheduler
        print("\nEvents in the scheduler:")
        event = self.scheduler.get_event()
        while event:
            print(f"Event ID: {event.get_event_id()}, Type: {event.get_event_type()}, Time: {event.get_event_time()}")
            event = self.scheduler.get_event()
        print(f"Total busy time: {current_time}")

    def Test_GateWay(self) -> None:
        """Test the GateWay class functionality."""
        print("\n--- Test_GateWay ---")
        # Create a gateway with a small queue size to test dropped messages
        gateway = GateWay(numServers=3, queueSize=3)

        # Print initial state
        print(f"\nInitial state:")
        print(f"Number of servers: {gateway.getNumServers()}")
        print(f"Number of messages: {gateway.getNumMsg()}")
        print(f"Number of dropped messages: {gateway.getDroppedMsg()}")

        # Create a message
        msg1 = Message(source="Client1", destination="Gateway1", payload="Message 1")

        # Call ReceiveMsg with the message
        print("\nCalling ReceiveMsg with the message...")
        gateway.ReceiveMsg(msg1)
        print(f"Number of messages after receiving: {gateway.getNumMsg()}")
        print(f"Number of dropped messages: {gateway.getDroppedMsg()}")

        # Create another message
        msg2 = Message(source="Client2", destination="Gateway1", payload="Message 2")
        msg5 = Message(source="Client2", destination="Gateway1", payload="Message 2")
        msg6 = Message(source="Client2", destination="Gateway1", payload="Message 2")
        msg7 = Message(source="Client2", destination="Gateway1", payload="Message 2")
        msg8 = Message(source="Client2", destination="Gateway1", payload="Message 2")

        # Call ReceiveMsg with the second message
        print("\nCalling ReceiveMsg with the second message...")
        gateway.ReceiveMsg(msg2)
        gateway.ReceiveMsg(msg5)
        gateway.ReceiveMsg(msg6)
        gateway.ReceiveMsg(msg7)
        gateway.ReceiveMsg(msg8)
        print(f"Number of messages after receiving second message: {gateway.getNumMsg()}")
        print(f"Number of dropped messages: {gateway.getDroppedMsg()}")

        # Create a third message
        msg3 = Message(source="Client3", destination="Gateway1", payload="Message 3")

        # Call ReceiveMsg with the third message
        print("\nCalling ReceiveMsg with the third message...")
        gateway.ReceiveMsg(msg3)
        print(f"Number of messages after receiving third message: {gateway.getNumMsg()}")
        print(f"Number of dropped messages: {gateway.getDroppedMsg()}")

        # Create a fourth message to test dropped messages
        msg4 = Message(source="Client4", destination="Gateway1", payload="Message 4")

        # Call ReceiveMsg with the fourth message
        print("\nCalling ReceiveMsg with the fourth message...")
        gateway.ReceiveMsg(msg4)
        print(f"Number of messages after receiving fourth message: {gateway.getNumMsg()}")
        print(f"Number of dropped messages: {gateway.getDroppedMsg()}")

        # Call departureMsg with the first message
        print("\nCalling departureMsg with the first message...")
        gateway.departureMsg(msg1)
        print(f"Number of messages after departure: {gateway.getNumMsg()}")
        print(f"Number of dropped messages: {gateway.getDroppedMsg()}")

        # Call departureMsg with the second message
        print("\nCalling departureMsg with the second message...")
        gateway.departureMsg(msg2)
        print(f"Number of messages after second departure: {gateway.getNumMsg()}")
        print(f"Number of dropped messages: {gateway.getDroppedMsg()}")

        # Call departureMsg with the third message
        print("\nCalling departureMsg with the third message...")
        gateway.departureMsg(msg3)
        print(f"Number of messages after third departure: {gateway.getNumMsg()}")
        print(f"Number of dropped messages: {gateway.getDroppedMsg()}")

        # Call departureMsg with the fourth message
        print("\nCalling departureMsg with the fourth message...")
        gateway.departureMsg(msg4)
        print(f"Number of messages after fourth departure: {gateway.getNumMsg()}")
        print(f"Number of dropped messages: {gateway.getDroppedMsg()}")

    def CreateClients(self) -> None:
        """Instantiate n_clients Client objects."""
        for _ in range(self.n_clients):
            c = Client(self.lam)
            self.clients.append(c)
        print(f"\nCreated {len(self.clients)} clients.")

    def InitEvents(self) -> None:
        """Schedule each client's first SEND_MSG to one of the gateways."""
        for client in self.clients:
            ia = random.expovariate(self.lam)
            send_time = ia
            # client IDs: offset by +1 so they start at "1"
            src = str(client.get_client_id() + 1)
            dest = random.choice(self.sources)
            msg = Message(source=src, destination=dest)
            msg.timestamp = send_time
            evt = Event(
                message=msg,
                event_time=send_time,
                event_type=EventType.SEND_MSG.value
            )
            self.scheduler.add_event(evt)

    def GenerateTrace(self, event: Event) -> None:
        """Record and print a Trace for the given Event."""
        trace = Trace(
            event.get_event_id(),
            event.get_message(),
            event.get_event_time(),
            event.get_event_type()
        )
        self.traces.append(trace)
        trace.print_trace()

    def Run(self) -> None:
        """Drive the simulation until simulation_time is reached."""
        self.CreateClients()
        self.InitEvents()

        while True:
            next_time = self.scheduler.get_current_time()
            if next_time is None or next_time > self.simulation_time:
                break

            evt = self.scheduler.get_event()
            self.GenerateTrace(evt)

            etype = evt.get_event_type()
            msg = evt.get_message()

            if etype == EventType.SEND_MSG.value:
                # 1) arrival at gateway
                recv_evt = Event(
                    message=msg,
                    event_time=evt.get_event_time(),
                    event_type=EventType.RECV_MSG.value
                )
                self.scheduler.add_event(recv_evt)

                # 2) schedule client's next send
                ia = random.expovariate(self.lam)
                t_next = evt.get_event_time() + ia
                # propagate same client ID (already offset in InitEvents)
                src = msg.get_source()
                dest = random.choice(self.sources)
                new_msg = Message(source=src, destination=dest)
                new_msg.timestamp = t_next
                next_evt = Event(
                    message=new_msg,
                    event_time=t_next,
                    event_type=EventType.SEND_MSG.value
                )
                self.scheduler.add_event(next_evt)

            elif etype == EventType.RECV_MSG.value:
                # schedule departure after service time
                st = random.expovariate(self.mu)
                dept_time = evt.get_event_time() + st
                dept_evt = Event(
                    message=msg,
                    event_time=dept_time,
                    event_type=EventType.MSG_DEPT.value
                )
                self.scheduler.add_event(dept_evt)

    def main(self) -> None:
        # Optionally run demos/tests
        # self.Test_msg()
        # self.Test_event()
        # self.Test_Queue()
        # self.Test_Server()
        self.Test_GateWay()
        # Run the actual simulation
        self.Run()


if __name__ == "__main__":
    engine = Engine(
        n_clients=3,
        num_sources=2,
        simulation_time=10.0,
        lam=4.0,
        mu=8.0
    )
    engine.main()
