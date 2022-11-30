import asyncio
import os

import dotenv
from telethon import sync

import spam
import archive


dotenv.load_dotenv()
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
UPDATE_PERIOD = 5  # seconds


async def main():
    async with sync.TelegramClient("session", API_ID, API_HASH) as client:
        while True:
            dialogs = await client.get_dialogs(archived=False)
            await spam.process(client, dialogs)
            await archive.process(dialogs)
            await asyncio.sleep(UPDATE_PERIOD)


if __name__ == "__main__":
    asyncio.run(main())
