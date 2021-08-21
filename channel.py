import uuid
import time


class Channel:
    def __init__(self, name):
        self.name = name
        self.id = uuid.uuid4().hex
        self.created_at = time.time_ns()

    def __repr__(self):
        return self.name
