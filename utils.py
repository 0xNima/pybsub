import enum


class Action(enum.Enum):
    PUBLISH = 1
    SUBSCRIBE = 2

    def name(self):
        name = super(Action, self).name
        return name.lower()


class Schema(enum.Enum):
    CHANNEL_NAME = 1
    MESSAGE = 2
    ACTION = 3

    def name(self):
        name = super(Schema, self).name
        return name.lower()


def p_serialize(action, channel_name, message):
    # Final payload overview: | 0 | 1 | 2 | 2 | 3 |...| 3 | 4 | 5 | 5 | 6 |...| 6 |
    # 0: <action: pub/sub> -> 1 byte
    # 1: <channel_name block identifier> -> 1 byte
    # 2: <channel_name string length> -> 2 bytes
    # 3: <channel_name chars> -> n bytes
    # 4: <message block identifier> -> 1 bytes
    # 5: <message string length> -> 2 bytes
    # 6: <message chars> -> m bytes

    binary_chn = channel_name.encode('utf-8')
    binary_msg = message.encode('utf-8')

    size = 3 + 4 + 1 + len(binary_chn) + len(binary_msg)
    payloads = bytearray(size)

    index = 0

    payloads[index] = Schema.ACTION.value
    index += 1
    for _byte in (action.to_bytes(1, 'big')):
        payloads[index] = _byte
        index += 1

    payloads[index] = Schema.CHANNEL_NAME.value
    index += 1
    for _byte in (len(binary_chn).to_bytes(2, 'big')):
        payloads[index] = _byte
        index += 1

    for c in binary_chn:
        payloads[index] = c
        index += 1

    payloads[index] = Schema.MESSAGE.value
    index += 1
    for _byte in (len(binary_msg).to_bytes(2, 'big')):
        payloads[index] = _byte
        index += 1

    for c in binary_msg:
        payloads[index] = c
        index += 1

    return payloads


def p_deserialize(byte_array):
    data = {}
    block_size = len(Schema) - 1
    index = 0

    action = byte_array[index]
    index += 1

    data[Schema(action).name()] = byte_array[index]
    index += 1

    for _ in range(block_size):
        key = byte_array[index]
        index += 1

        length = 0
        binary_length = byte_array[index: index+2]
        for _byte in binary_length:
            length += _byte
        index += 2

        string = str()
        for _ in range(length):
            string += chr(byte_array[index])
            index += 1

        data[Schema(key).name()] = string

    return data


def s_serializer(message):
    binary_msg = message.encode('utf-8')
    size = len(binary_msg)
    bytes_array = bytearray(size)
    for i, c in enumerate(binary_msg):
        bytes_array[i] = c
    return bytes_array


def s_deserializer(byte_array):
    message = str()
    for _byte in byte_array:
        message += chr(_byte)
    return message


class AsyncIterable:
    def __init__(self, iterable):
        if isinstance(iterable, list):
            self.iterable = iterable
        elif isinstance(iterable, dict):
            self.iterable = iterable.copy()

        self.index = 0

    def __aiter__(self):
        return self

    async def __anext__(self):
        if isinstance(self.iterable, list):
            if self.index < len(self.iterable):
                value = self.iterable[self.index]
                self.index += 1
                return value
        elif isinstance(self.iterable, dict):
            if self.iterable:
                return self.iterable.popitem()
        raise StopAsyncIteration
