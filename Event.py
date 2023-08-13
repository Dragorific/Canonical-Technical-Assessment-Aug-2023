import json
from datetime import datetime

class Event:
    def __init__(self, event_type, user_id, variant_data):
        self.timestamp = datetime.now().isoformat()
        self.event_type = event_type
        self.user_id = user_id
        self.variant_data = variant_data

    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "event_type": self.event_type,
            "user_id": self.user_id,
            "variant_data": json.loads(self.variant_data),
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["event_type"],
            data["user_id"],
            json.dumps(data["variant_data"])
        )
