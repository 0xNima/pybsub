import uuid
import time


class Channel:
    def __init__(self, name):
        self.name = name
        self.id = uuid.uuid4().hex
        self.created_at = time.time_ns()
        self.subscribers = dict()

    def register_subscriber(self, subscriber, conn):
        self.subscribers[subscriber] = conn

    def remove_subscriber(self, subscriber):
        self.subscribers.pop(subscriber)

    def __repr__(self):
        return self.name
