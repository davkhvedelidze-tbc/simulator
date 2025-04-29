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
                 num_sources: int = 2,
                 simulation_time: float = 10.0,
                 lam: float = 4.0,
                 mu: float = 8.0):
        self.current_time    = time.time()       # float, simulation start
        self.n_clients       = n_clients         # int
        self.simulation_time = simulation_time   # float, e.g. 10.0
        self.lam             = lam               # arrival rate
        self.mu              = mu                # service rate

        # destinations (“gateways”) numbered 1…num_sources
        self.sources = [str(i+1) for i in range(num_sources)]

        # will hold our Client instances
        self.clients = []

        # event scheduler & trace log
        self.scheduler = Scheduler()
        self.traces    = []

    def CreateClients(self) -> None:
        """Instantiate n_clients and store them in self.clients."""
        for _ in range(self.n_clients):
            c = Client(self.lam)
            self.clients.append(c)
        print(f"Created {len(self.clients)} clients.")

    def InitEvents(self) -> None:
        """Ask each Client to start and schedule its first SEND_MSG."""
        for client in self.clients:
            ev = client.start(destination=random.choice(self.sources))
            self.scheduler.add_event(ev)

    def GenerateTrace(self, event: Event) -> None:
        """Log + print a Trace for the given Event."""
        tr = Trace(
            event.get_event_id(),
            event.get_message(),
            event.get_event_time(),
            event.get_event_type()
        )
        self.traces.append(tr)
        tr.print_trace()

    def Run(self) -> None:
        """Drive simulation until current_time + simulation_time."""
        self.CreateClients()
        self.InitEvents()

        end_time = self.current_time + self.simulation_time
        while True:
            next_evt_time = self.scheduler.get_current_time()
            if next_evt_time is None or next_evt_time > end_time:
                break

            evt = self.scheduler.get_event()
            self.GenerateTrace(evt)

            typ = evt.get_event_type()
            msg = evt.get_message()

            if typ == EventType.SEND_MSG.value:
                # schedule arrival
                recv = Event(msg, evt.get_event_time(), EventType.RECV_MSG.value)
                self.scheduler.add_event(recv)
                # schedule next send
                ia   = random.expovariate(self.lam)
                t_nx = evt.get_event_time() + ia
                client_id = int(msg.get_source()) - 1
                new_msg = Message(source=msg.get_source(),
                                  destination=random.choice(self.sources))
                new_msg.timestamp = t_nx
                nxt = Event(new_msg, t_nx, EventType.SEND_MSG.value)
                self.scheduler.add_event(nxt)

            elif typ == EventType.RECV_MSG.value:
                # schedule departure
                st = random.expovariate(self.mu)
                t_dep = evt.get_event_time() + st
                dep_evt = Event(msg, t_dep, EventType.MSG_DEPT.value)
                self.scheduler.add_event(dep_evt)

            # MSG_DEPT: no further chaining

    def main(self) -> None:
        print(f"Simulation start @ {self.current_time:.6f}")
        self.Run()
        print("Simulation complete.")

if __name__ == "__main__":
    engine = Engine(
        n_clients=3,
        num_sources=2,
        simulation_time=10.0,
        lam=4.0,
        mu=8.0
    )
    engine.main()