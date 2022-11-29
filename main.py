import os
import asyncio
import dotenv
from telethon import sync

dotenv.load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
UPDATE_PERIOD = 30  # seconds


async def archive():
    async with sync.TelegramClient("session", API_ID, API_HASH) as client:
        async for dialog in client.iter_dialogs(archived=False):
            if dialog.pinned or dialog.unread_count > 0 or dialog.unread_mentions_count > 0:
                continue

            await dialog.archive()


async def main():
    while True:
        await archive()
        await asyncio.sleep(UPDATE_PERIOD)


if __name__ == "__main__":
    asyncio.run(main())
