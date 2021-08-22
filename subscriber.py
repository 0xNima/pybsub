import uuid

import utils


class Subscriber:
    def __init__(self, channel):
        self.channel = channel
        self.id = uuid.uuid4().hex

    async def send(self, message, stream_writer):
        binary_msg = utils.s_serializer(message.body)

        stream_writer.write(len(binary_msg).to_bytes(2, 'big'))
        await stream_writer.drain()

        stream_writer.write(binary_msg)
        await stream_writer.drain()
