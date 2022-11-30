import utils

MESSAGE_DISPLAY_TIME = 30  # seconds

dialogs_to_archive = dict()


def filter(dialog):
    if dialog.dialog.pinned:
        return False

    if dialog.dialog.unread_mark:
        return False

    if dialog.dialog.unread_count > 0:
        return False

    if dialog.dialog.unread_mentions_count > 0:
        return False

    if dialog.dialog.unread_reactions_count > 0:
        return False

    return True


def add(dialog):
    if dialog.id not in dialogs_to_archive:
        current_date = utils.get_current_date()
        dialogs_to_archive[dialog.id] = (current_date, dialog)


def remove(dialog):
    if dialog.id in dialogs_to_archive:
        del dialogs_to_archive[dialog.id]


async def update():
    current_date = utils.get_current_date()

    ids_to_archive = []
    for dialog_id, values in dialogs_to_archive.items():
        date, _ = values
        duration = (current_date - date).total_seconds()

        if duration >= MESSAGE_DISPLAY_TIME:
            ids_to_archive.append(dialog_id)

    for dialog_id in ids_to_archive:
        _, dialog = dialogs_to_archive.pop(dialog_id)
        await dialog.archive()


async def process(dialogs):
    for dialog in dialogs:
        if filter(dialog):
            add(dialog)
        else:
            remove(dialog)

    await update()
