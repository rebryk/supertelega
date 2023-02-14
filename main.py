import argparse
import asyncio
import os

import dotenv
from telethon import sync

import archive
import dm
import spam

dotenv.load_dotenv()
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
UPDATE_PERIOD = 5  # seconds


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--filter-spam", action="store_true")
    parser.add_argument("--auto-archive", action="store_true")
    parser.add_argument("--auto-dm", type=str)
    return parser.parse_args()


async def main(filter_spam: bool, auto_archive: bool, auto_dm: bool):
    async with sync.TelegramClient("session", API_ID, API_HASH) as client:
        if auto_dm:
            auto_dm = await client.get_entity(auto_dm)

        while True:
            dialogs = await client.get_dialogs(archived=False)

            if filter_spam:
                await spam.process(client, dialogs)

            if auto_archive:
                await archive.process(dialogs)

            if auto_dm:
                await dm.process(client, auto_dm)

            # wait for next update
            await asyncio.sleep(UPDATE_PERIOD)


if __name__ == "__main__":
    args = parse_args()
    asyncio.run(main(**vars(args)))
