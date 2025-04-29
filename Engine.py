# Engine.py

import random
from Message import Message
from Trace import Trace
from Event import Event, EventType
from Scheduler import Scheduler
from Client import Client

class Engine:
    def __init__(self,
                 n_clients: int = 3,
                 num_sources: int = 2,
                 simulation_time: float = 10.0,
                 lam: float = 4.0,
                 mu: float = 8.0):
        # Main parameters
        self.n_clients       = n_clients
        self.simulation_time = simulation_time
        self.lam             = lam   # client arrival rate
        self.mu              = mu    # gateway service rate

        # Gateways numbered from 1..num_sources
        self.sources = [str(i+1) for i in range(num_sources)]

        # Components
        self.scheduler = Scheduler()
        self.clients   = []
        self.traces    = []

    def Test_msg(self) -> None:
        """Demonstrate basic Message usage."""
        print("\n--- Test_msg ---")
        msg = Message(source="1", destination="2", payload="Example")
        print(f"Message ID:  {msg.get_message_id()}")
        print(f"Source:      {msg.get_source()}")       # prints "1"
        print(f"Destination: {msg.get_destination()}")  # prints "2"
        msg.print_message()

    def Test_event(self) -> None:
        """Demonstrate basic Event usage."""
        print("\n--- Test_event ---")
        msg   = Message(source="1", destination="2", payload="EvtPayload")
        event = Event(message=msg, event_type=EventType.SEND_MSG.value)
        event.set_event_time(msg.get_timestamp())
        event.print_event()

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
            msg   = evt.get_message()

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
        self.Test_msg()
        self.Test_event()
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