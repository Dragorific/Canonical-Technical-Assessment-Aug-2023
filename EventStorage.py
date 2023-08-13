class EventStorage:
    def __init__(self):
        self.events = []

    def add_event(self, event):
        self.events.append(event.to_dict())

    def query_events(self, filter_dict):
        return [e for e in self.events if all(e[k] == v for k, v in filter_dict.items())]
