import os

import dotenv
from telethon import sync

_users_cache = set()  # to avoid double DMs

dotenv.load_dotenv()
MESSAGE_TEMPLATE = os.getenv("AUTO_DM")
CURSOR_FILE = "cursor.txt"


def _read_cursor() -> int:
    if os.path.exists(CURSOR_FILE):
        with open(CURSOR_FILE) as file:
            return int(file.read())

    return 0


def _write_cursor(cursor: int):
    with open(CURSOR_FILE, "w") as file:
        file.write(str(cursor))


async def _dm_user(client: sync.TelegramClient, user_id: int):
    try:
        if user_id in _users_cache:
            return

        await client.send_message(user_id, MESSAGE_TEMPLATE)
        _users_cache.add(user_id)
    except Exception as e:
        print(f"Failed to DM user {user_id}: {e}")


async def process(client: sync.TelegramClient, channel):
    min_id = _read_cursor()
    logs = await client.get_admin_log(channel, join=True, min_id=min_id)
    for log in logs[::-1]:
        try:
            if log.joined and log.input_user and hasattr(log.input_user, "user_id"):
                user_id = log.input_user.user_id
                await _dm_user(client, user_id)
                min_id = log.id
        except Exception as e:
            print(f"Failed to process log {log.id}: {e}")

    _write_cursor(min_id)
