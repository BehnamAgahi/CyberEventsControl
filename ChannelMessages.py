import configparser

import json

import asyncio

from datetime import date, datetime

from telethon import TelegramClient

from telethon.errors import SessionPasswordNeededError

from telethon.tl.functions.messages import (GetHistoryRequest)

from telethon.tl.types import ( PeerChannel )

class DateTimeEncoder(json.JSONEncoder):

    def default(self, o):

        if isinstance(o, datetime):

            return o.isoformat()

        if isinstance(o, bytes):

            return list(o)

        return json.JSONEncoder.default(self, o)

config = configparser.ConfigParser()

config.read("config.ini")

api_id = config['Telegram']['api_id']

api_hash = config['Telegram']['api_hash']

api_hash = str(api_hash)

phone = config['Telegram']['phone']

username = config['Telegram']['username']

channelsNames = []

with open("channels.ini") as channelsFile:

    for line in channelsFile:

        line = line.strip()

        channelsNames.append(line)

client = TelegramClient(username, api_id, api_hash)

async def main(phone):

    await client.start()

    print("Client Created")

    if await client.is_user_authorized() == False:

        await client.send_code_request(phone)

        try:

            await client.sign_in(phone, input('Enter the code: '))

        except SessionPasswordNeededError:

            await client.sign_in(password = input('Password: '))

    me = await client.get_me()

    allMessages = []

    for channelIterator in channelsNames:

        if channelIterator.isdigit():

            entity = PeerChannel(int(channelIterator))

        else:

            entity = channelIterator

        my_channel = await client.get_entity(entity)

        offset_id = 0

        limit = 100

        total_messages = 0

        total_count_limit = 500

        all_messages = []

        while True:

            print("Current Offset ID is:", offset_id, "; Total Messages:", total_messages)

            history = await client(GetHistoryRequest(

                peer = my_channel,

                offset_id = offset_id,

                offset_date = None,

                add_offset = 0,

                limit = limit,

                max_id = 0,

                min_id = 0,

                hash = 0

            ))

            if not history.messages:

                break

            messages = history.messages

            j = 0

            while j < len (messages):

                all_messages.append(messages[j].to_dict())

                j = j + 1

            offset_id = messages[len(messages) - 1].id

            total_messages = len(all_messages)

            if total_count_limit != 0 and total_messages >= total_count_limit:

                for messageIterator in all_messages:

                    allMessages.append(messageIterator)

                break

    with open('channels_messages.json', 'w') as outfile:

        json.dump(allMessages, outfile, cls = DateTimeEncoder)

with client:

    client.loop.run_until_complete(main(phone))
