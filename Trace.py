import time

class Trace:
    _id_counter = 0

    def __init__(self, event_id, message, event_time=None, event_type=None):
        """
        Trace entry for an event in the simulator.

        Members per slide 12: EventID, Message, plus here we expose the node (source) and msgID  nca-09- Simulator.pdf](file-service://file-Db9srttiKnm1KyZSGSksvw)
        """
        self.trace_id = Trace._id_counter
        Trace._id_counter += 1

        self.event_id = event_id
        self.message = message
        self.event_time = event_time if event_time is not None else time.time()
        self.event_type = event_type

    def print_trace(self):
        """
        Print an ASCII table with columns:
          Time (s)  | Node | Type     | Destination | MsgID
        Node is the message source; MsgID is the unique ID of the message.
        """
        headers = ["Time (s)", "Node", "Type", "Destination", "MsgID"]

        # format relative time to two decimals
        time_str = f"{self.event_time:.2f}"
        node_str = self.message.get_source()
        type_str = self.event_type or ""
        dst_str = self.message.get_destination()
        msgid_str = str(self.message.get_message_id())

        vals = [time_str, node_str, type_str, dst_str, msgid_str]

        # compute column widths
        col_w = [max(len(h), len(v)) for h, v in zip(headers, vals)]
        border = "+" + "+".join("-" * (w + 2) for w in col_w) + "+"
        header_row = "|" + "|".join(f" {h.ljust(w)} " for h, w in zip(headers, col_w)) + "|"
        value_row = "|" + "|".join(f" {v.ljust(w)} " for v, w in zip(vals, col_w)) + "|"

        print(border)
        print(header_row)
        print(border)
        print(value_row)
        print(border)