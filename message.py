import time
import uuid


class Message:
    def __init__(self, channel, body):
        self.channel = channel
        self.body = body
        self.created_at = time.time_ns()
        self.id = uuid.uuid4().hex

    def __repr__(self):
        return "body: {} \t[created at: {}]".format(self.body, self.created_at)
