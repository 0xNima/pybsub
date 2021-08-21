import asyncio
import os
import utils
import channel as ch
import message as msg
import uvloop
import signal


class Broker:
    def __init__(self):
        self.channels = dict()
        self.loop = asyncio.get_event_loop()
        self.messages = asyncio.queues.Queue(loop=self.loop)
        self.connections = []

    def get_channel(self, channel_name):
        return self.channels.setdefault(channel_name, ch.Channel(channel_name))

    async def send_to_q(self, message):
        await self.messages.put(message)

    async def publish(self, *args):
        data = args[0]

        channel_name = data.pop("channel_name")
        message = data.pop("message")

        await self.send_to_q(
            msg.Message(self.get_channel(channel_name), message)
        )

    async def subscribe(self, *args):
        data, writer = args
        self.connections.append(writer)
        while True:
            message = await self.messages.get()
            print(">>>", message)
            if data.get("channel_name") == message.channel.name:
                binary_msg = utils.s_serializer(message.body)
                writer.write(len(binary_msg).to_bytes(2, 'big'))
                await writer.drain()
                writer.write(binary_msg)
                await writer.drain()
            await asyncio.sleep(0.5)

    async def process_data(self, data, writer):
        action = data.pop("action")
        if action == utils.Action.PUBLISH:
            writer.close()
        await getattr(self, utils.Action(action).name())(data, writer)

    async def handler(self, reader, writer):
        stream = await reader.read()
        data = utils.p_deserialize(stream)
        await self.process_data(data, writer)

    def add_exit_handlers(self):
        for sig in [signal.SIGINT, signal.SIGTERM]:
            self.loop.add_signal_handler(sig, lambda: asyncio.ensure_future(self.disconnect(), loop=self.loop))

    def run(self):
        socket_file = "server.socket"
        if os.path.exists(socket_file):
            os.remove(socket_file)

        uvloop.install()

        self.add_exit_handlers()

        server = asyncio.start_unix_server(self.handler, path=socket_file)
        self.loop.run_until_complete(server)
        self.loop.run_forever()

    async def disconnect(self):
        async for connection in utils.AsyncIterable(self.connections):
            connection.close()

        for task in asyncio.Task.all_tasks(loop=self.loop):
            task.cancel()
        self.loop.stop()
