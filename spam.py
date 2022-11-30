MESSAGE_LIMIT = 3

white_list = set()


def _is_contact(entity):
    return hasattr(entity, "contact") and entity.contact


def _is_premium(entity):
    return hasattr(entity, "premium") and entity.premium


def _is_verified(entity):
    return hasattr(entity, "verified") and entity.verified


def _is_scam(entity):
    return hasattr(entity, "scam") and entity.scam


async def filter(client, dialog):
    if not dialog.is_user:
        return False

    entity = dialog.entity

    if _is_contact(entity):
        return False

    if _is_premium(entity):
        return False

    if _is_verified(entity):
        return False

    if _is_scam(entity):
        return True

    # Single message and it is forwarded
    messages = await client.get_messages(dialog.id, limit=MESSAGE_LIMIT)
    if len(messages) == 1 and dialog.message.fwd_from is not None:
        return True

    return False


async def process(client, dialogs):
    for dialog in dialogs:
        if dialog.id in white_list:
            continue

        if await filter(client, dialog):
            # TODO: remove and block
            await dialog.archive()
        else:
            white_list.add(dialog.id)
