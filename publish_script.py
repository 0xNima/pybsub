import utils
import sys
import asyncio


async def create_connection(action, channel_name, message):
    reader, writer = await asyncio.open_unix_connection(path='server.socket')
    if isinstance(action, utils.Action):
        action = action.value
    writer.write(utils.p_serialize(action, channel_name, message))
    await writer.drain()


if __name__ == '__main__':
    channel_name_, body_ = sys.argv[1], sys.argv[2]
    asyncio.run(create_connection(utils.Action.PUBLISH, channel_name_, body_))
