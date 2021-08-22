import utils
import sys
import asyncio


async def create_connection(action, channel_name, message):
    reader, writer = await asyncio.open_unix_connection(path='server.socket')
    if isinstance(action, utils.Action):
        action = action.value

    writer.write(utils.p_serialize(action, channel_name, message))
    await writer.drain()
    writer.write_eof()

    while True:
        if reader.at_eof():
            return
        buffer = await reader.read(2)
        buffer_size = 0
        for byte in buffer:
            buffer_size += byte
        stream = await reader.read(buffer_size)
        message = utils.s_deserializer(stream)
        print(message)
        await asyncio.sleep(0.1)

if __name__ == '__main__':
    channel_name_ = sys.argv[1]
    asyncio.run(create_connection(utils.Action.SUBSCRIBE, channel_name_, str()))
