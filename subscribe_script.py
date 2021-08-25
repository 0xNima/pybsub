import utils
import sys
import asyncio


if __name__ == '__main__':
    channel_name_ = sys.argv[1]
    asyncio.run(utils.create_sub_connection(utils.Action.SUBSCRIBE, channel_name_, str()))
