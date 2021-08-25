import utils
import sys
import asyncio


if __name__ == '__main__':
    channel_name_, body_ = sys.argv[1], sys.argv[2]
    asyncio.run(utils.create_pub_connection(utils.Action.PUBLISH, channel_name_, body_))
