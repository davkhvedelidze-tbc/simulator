# Engine.py

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
        # record wall‐clock start
        self.start_time      = time.time()
        self.simulation_time = simulation_time   # duration in seconds
        self.lam             = lam               # arrival rate λ
        self.mu              = mu                # service rate μ

        # gateways labeled “1”…“num_sources”
        self.sources   = [str(i+1) for i in range(num_sources)]
        self.clients   = []                       # will hold Client instances
        self.scheduler = Scheduler()              # event queue
        self.traces    = []                       # logged traces

    def CreateClients(self) -> None:
        """Instantiate n_clients and store in self.clients."""
        for _ in range(n_clients := len(self.clients), n_clients + 3):
            c = Client(self.lam)
            self.clients.append(c)
        print(f"Created {len(self.clients)} clients.")

    def InitEvents(self) -> None:
        """Have each client produce its first SEND_MSG Event and schedule it."""
        for client in self.clients:
            ev = client.start(destination=random.choice(self.sources))
            self.scheduler.add_event(ev)

    def GenerateTrace(self, event: Event) -> None:
        """
        Compute relative time, wrap into Trace, log & print it.
        """
        # relative to simulation start
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
        Main event loop: pull events until simulation_time elapses.
        """
        # bootstrap
        self.CreateClients()
        self.InitEvents()

        end_time = self.start_time + self.simulation_time
        while True:
            next_time = self.scheduler.get_current_time()
            # stop if no events or past simulation window
            if next_time is None or next_time > end_time:
                break

            evt = self.scheduler.get_event()
            self.GenerateTrace(evt)

            typ = evt.get_event_type()
            msg = evt.get_message()

            if typ == EventType.SEND_MSG.value:
                # schedule arrival at gateway
                recv_evt = Event(
                    message=msg,
                    event_time=evt.get_event_time(),
                    event_type=EventType.RECV_MSG.value
                )
                self.scheduler.add_event(recv_evt)

                # schedule client's next send
                ia   = random.expovariate(self.lam)
                t_nx = evt.get_event_time() + ia
                # reuse same client ID
                new_msg = Message(
                    source=msg.get_source(),
                    destination=random.choice(self.sources)
                )
                new_msg.timestamp = t_nx
                next_evt = Event(
                    message=new_msg,
                    event_time=t_nx,
                    event_type=EventType.SEND_MSG.value
                )
                self.scheduler.add_event(next_evt)

            elif typ == EventType.RECV_MSG.value:
                # schedule departure after service
                st       = random.expovariate(self.mu)
                dept_t   = evt.get_event_time() + st
                dept_evt = Event(
                    message=msg,
                    event_time=dept_t,
                    event_type=EventType.MSG_DEPT.value
                )
                self.scheduler.add_event(dept_evt)

    def main(self) -> None:
        elapsed = time.time() - self.start_time
        print(f"Simulation start @ {elapsed:.2f}s")
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