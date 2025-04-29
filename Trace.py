# import time
#
# class Trace:
#     _id_counter = 0
#
#     def __init__(self, event_id, message, event_time=None, event_type=None):
#         """
#         Trace entry for an event in the simulator.
#
#         :param event_id:   Unique identifier of the event.
#         :param message:    The Message instance associated with the event.
#         :param event_time: Timestamp of when the event occurred.
#         :param event_type: Type of the event (e.g., SEND_MSG, RECV_MSG, MSG_DEPT).
#         """
#         self.trace_id   = Trace._id_counter
#         Trace._id_counter += 1
#
#         self.event_id   = event_id
#         self.message    = message
#         self.event_time = event_time if event_time is not None else time.time()
#         self.event_type = event_type
#
#     def __del__(self):
#         # Optional cleanup logic
#         pass
#
#     def set_event_time(self, timestamp):
#         """Set the timestamp for this trace entry."""
#         self.event_time = timestamp
#
#     def get_event_time(self):
#         """Get the timestamp for this trace entry."""
#         return self.event_time
#
#     def set_event_type(self, event_type):
#         """Set the type for this trace entry."""
#         self.event_type = event_type
#
#     def get_event_type(self):
#         """Get the type for this trace entry."""
#         return self.event_type
#
#     def print_trace(self):
#         """
#         Print an ASCII table with columns: Time, Type, Source, Destination
#         showing time in seconds (with decimals).
#         """
#         headers = ["Time (s)", "Type", "Source", "Destination"]
#         # show full float, not int
#         time_str = f"{self.event_time:.6f}"
#         type_str = self.event_type or ""
#         # assume message has get_source()/get_destination()
#         src = self.message.get_source()
#         dst = self.message.get_destination()
#         vals = [time_str, type_str, src, dst]
#
#         # compute column widths
#         col_w = [max(len(h), len(v)) for h, v in zip(headers, vals)]
#         border = "+" + "+".join("-" * (w + 2) for w in col_w) + "+"
#         header_row = "|" + "|".join(f" {h.ljust(w)} " for h, w in zip(headers, col_w)) + "|"
#         value_row = "|" + "|".join(f" {v.ljust(w)} " for v, w in zip(vals, col_w)) + "|"
#
#         print(border)
#         print(header_row)
#         print(border)
#         print(value_row)
#         print(border)
#
#     def __str__(self):
#         return (f"Trace(id={self.trace_id}, event_id={self.event_id}, "
#                 f"message={self.message}, time={self.event_time}, "
#                 f"type={self.event_type})")


import time

class Trace:
    _id_counter = 0

    def __init__(self, event_id, message, event_time=None, event_type=None):
        """
        Trace entry for an event in the simulator.

        :param event_id:   Unique identifier of the event.
        :param message:    The Message instance associated with the event.
        :param event_time: Timestamp of when the event occurred.
        :param event_type: Type of the event (e.g., SEND_MSG, RECV_MSG, MSG_DEPT).
        """
        self.trace_id   = Trace._id_counter
        Trace._id_counter += 1

        self.event_id   = event_id
        self.message    = message
        self.event_time = event_time if event_time is not None else time.time()
        self.event_type = event_type

    def __del__(self):
        # Optional cleanup logic
        pass

    def set_event_time(self, timestamp):
        """Set the timestamp for this trace entry."""
        self.event_time = timestamp

    def get_event_time(self):
        """Get the timestamp for this trace entry."""
        return self.event_time

    def set_event_type(self, event_type):
        """Set the type for this trace entry."""
        self.event_type = event_type

    def get_event_type(self):
        """Get the type for this trace entry."""
        return self.event_type

    def print_trace(self):
        """
        Print an ASCII table with columns: Time (s), Type, Source, Destination
        showing time in seconds (with decimals).
        """
        headers = ["Time (s)", "Type", "Source", "Destination"]
        time_str = f"{self.event_time:.6f}"
        type_str = self.event_type or ""
        src = self.message.get_source()
        dst = self.message.get_destination()
        vals = [time_str, type_str, src, dst]

        # compute column widths
        col_w = [max(len(h), len(v)) for h, v in zip(headers, vals)]
        border = "+" + "+".join("-" * (w + 2) for w in col_w) + "+"
        header_row = "|" + "|".join(f" {h.ljust(w)} " for h, w in zip(headers, col_w)) + "|"
        value_row  = "|" + "|".join(f" {v.ljust(w)} " for v, w in zip(vals,   col_w)) + "|"

        print(border)
        print(header_row)
        print(border)
        print(value_row)
        print(border)
