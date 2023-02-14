import os

from telethon import sync

_min_id = 0
_users_cache = set()

MESSAGE_TEMPLATE = os.getenv("AUTO_DM")


async def _dm_user(client: sync.TelegramClient, user_id: int):
    try:
        if user_id in _users_cache:
            return

        await client.send_message(user_id, MESSAGE_TEMPLATE)
        _users_cache.add(user_id)
    except Exception as e:
        print(f"Failed to DM user {user_id}: {e}")


async def process(client: sync.TelegramClient, channel):
    global _min_id

    logs = await client.get_admin_log(channel, join=True, min_id=_min_id)

    for log in logs[::-1]:
        try:
            if log.joined and log.input_user and hasattr(log.input_user, "user_id"):
                user_id = log.input_user.user_id
                await _dm_user(client, user_id)
                _min_id = log.id
        except Exception as e:
            print(f"Failed to process log {log.id}: {e}")
