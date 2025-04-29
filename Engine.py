import time
import random
from Message import Message
from Trace import Trace
from Event import Event, EventType
from Scheduler import Scheduler
from Client import Client

class Engine:
    def __init__(self,
                 n_clients: int = 3,
                 simulation_time: float = 10.0,
                 lam: float = 4.0):
        # record simulation start wall‐clock time
        self.start_time      = time.time()
        self.simulation_time = simulation_time   # total simulation duration
        self.lam             = lam               # client arrival rate λ
        self.n_clients       = n_clients

        # components
        self.clients   = []                       # will hold Client instances
        self.scheduler = Scheduler()              # event priority queue
        self.traces    = []                       # collected Trace entries

    def CreateClients(self) -> None:
        """Instantiate n_clients and store in self.clients."""
        for _ in range(self.n_clients):
            c = Client(self.lam)
            self.clients.append(c)
        print(f"Created {len(self.clients)} clients.")

    def InitEvents(self) -> None:
        """Schedule each client's first SEND_MSG Event."""
        for client in self.clients:
            # destination should be "0" (your single gateway)
            ev = client.start(destination="0")
            self.scheduler.add_event(ev)

    def GenerateTrace(self, event: Event) -> None:
        """Log only SEND_MSG events as traces."""
        if event.get_event_type() != EventType.SEND_MSG.value:
            return

        rel_time = event.get_event_time() - self.start_time
        tr = Trace(
            event.get_event_id(),
            event.get_message(),
            rel_time,
            event.get_event_type()
        )
        self.traces.append(tr)
        tr.print_trace()

    def Run(self) -> None:
        """
        Drive the simulation: process SEND_MSG events only,
        scheduling each client's next send until time expires.
        """
        self.CreateClients()
        self.InitEvents()

        end_time = self.start_time + self.simulation_time
        while True:
            next_time = self.scheduler.get_current_time()
            if next_time is None or next_time > end_time:
                break

            evt = self.scheduler.get_event()
            # only SEND_MSG are in the queue, but we still check type
            self.GenerateTrace(evt)

            if evt.get_event_type() == EventType.SEND_MSG.value:
                # schedule this client’s next send
                ia   = random.expovariate(self.lam)
                t_nx = evt.get_event_time() + ia

                src = evt.get_message().get_source()
                # destination should be "0"
                new_msg = Message(
                    source=src,
                    destination="0"
                )
                new_msg.timestamp = t_nx

                next_evt = Event(
                    message=new_msg,
                    event_time=t_nx,
                    event_type=EventType.SEND_MSG.value
                )
                self.scheduler.add_event(next_evt)

    def main(self) -> None:
        elapsed = time.time() - self.start_time
        print(f"Simulation start @ {elapsed:.2f}s")
        self.Run()
        print("Simulation complete.")

if __name__ == "__main__":
    engine = Engine(
        n_clients=3,
        simulation_time=10.0,
        lam=1.0
    )
    engine.main()