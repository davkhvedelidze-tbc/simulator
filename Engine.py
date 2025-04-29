# from Message import Message

# class Engine:
#     def testMsg(self):
#         for i in range(1, 6):
#             msg = Message("1", "0", f"Hello World, iteration {i}")
#             msg.print_message()

#     def main(self):
#         self.testMsg()

# if __name__ == "__main__":
#     engine = Engine()
#     engine.main()




from Message import Message
from trace import Trace
from Message import EventType

# from Event import Event  # Event class to be implemented per slide 13

class Engine:
    def __init__(self, n_clients: int = 1, simulation_time: float = 10.0):
        # Main parameters
        self.n_clients = n_clients
        self.simulation_time = simulation_time
        self.gateway = None  # single gateway placeholder

        # Internal state
        self.traces = []
        self.event_counter = 0

    def GenerateTrace(self, event) -> None:
        """
        Create a Trace from an Event and store/print it.

        :param event: An object with get_event_id(), get_message(),
                      get_event_time(), get_event_type().
        """
        trace = Trace(
            event_id=event.get_event_id(),
            message=event.get_message(),
            event_time=event.get_event_time(),
            event_type=event.get_event_type()
        )
        self.traces.append(trace)
        trace.print_trace()

    def CreateClients(self, n_clients: int):
        """
        Stub for creating client instances.
        """
        self.clients = [f"Client{i}" for i in range(n_clients)]
        print(f"Created {n_clients} clients: {self.clients}")

    def Run(self):
        """
        Stub run loop to generate test messages and traces.
        """
        for i in range(1, 6):
            msg = Message(source="Client1", destination="Server1", payload=f"Iteration {i}")
            msg.print_message()

            # Dummy Event object to illustrate trace generation
            class DummyEvent:
                def __init__(self, eid, message):
                    self._eid = eid
                    self._msg = message
                    self._time = message.get_timestamp()
                    self._type = EventType.SEND_MSG.name
                def get_event_id(self): return self._eid
                def get_message(self): return self._msg
                def get_event_time(self): return self._time
                def get_event_type(self): return self._type

            event = DummyEvent(self.event_counter, msg)
            self.GenerateTrace(event)
            self.event_counter += 1

    def main(self):
        # slide 11: main() should invoke Run()
        self.Run()

if __name__ == "__main__":
    engine = Engine(n_clients=1, simulation_time=10.0)
    engine.main()