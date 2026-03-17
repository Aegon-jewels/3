# Bankai - UserBot
# Ported from CatUserBot by TgCatUB
"""
✘ Commands Available -

• `{i}scam <action> <seconds>`
    Fake a chat action for given seconds.
    Actions: typing, contact, game, location, voice, round, video, photo, document

• `{i}prankpromote <reply/user>`
    Promote with only 'Other' rights (fake admin).

• `{i}padmin`
    Show a fake admin promotion animation.
"""

import asyncio
from random import choice, randint

from telethon.errors import BadRequestError
from telethon.tl.functions.channels import EditAdminRequest
from telethon.tl.types import ChatAdminRights

from . import ultroid_cmd, eor, eod, OWNER_NAME
from pyUltroid.fns.tools import get_user_from_event

ACTIONS = ["typing", "contact", "game", "location", "voice", "round", "video", "photo", "document"]


@ultroid_cmd(pattern="scam(?:\s|$)([\s\S]*)")
async def scam_action(event):
    """Fake a Telegram chat action."""
    input_str = event.pattern_match.group(1).strip()
    args = input_str.split()
    if not args:
        action = choice(ACTIONS)
        secs = randint(300, 360)
    elif len(args) == 1:
        if args[0].isnumeric():
            action = choice(ACTIONS)
            secs = int(args[0])
        else:
            action = args[0].lower()
            secs = randint(300, 360)
    elif len(args) == 2:
        action = args[0].lower()
        try:
            secs = int(args[1])
        except ValueError:
            return await event.eor("`Invalid syntax. Use: .scam <action> <seconds>`")
    else:
        return await event.eor("`Invalid syntax. Use: .scam <action> <seconds>`")
    if action not in ACTIONS:
        return await event.eor(f"`Invalid action. Choose from: {', '.join(ACTIONS)}`")
    await event.delete()
    async with event.client.action(event.chat_id, action):
        await asyncio.sleep(secs)


@ultroid_cmd(pattern="prankpromote(?:\s|$)([\s\S]*)", require_admin=True, groups_only=True)
async def prank_promote(event):
    """Fake promote with zero real rights."""
    msg = await event.eor("`Promoting...`")
    try:
        user = await get_user_from_event(event)
    except Exception:
        return await msg.edit("`Reply to a user or provide username/ID.`")
    if not user:
        return await msg.edit("`Couldn't find user.`")
    new_rights = ChatAdminRights(other=True)
    try:
        await event.client(EditAdminRequest(event.chat_id, user.id, new_rights, "Admin"))
        await msg.edit("`Promoted Successfully! Now gib Party 🎉`")
    except BadRequestError:
        await msg.edit("`I don't have permission to promote.`")
    except Exception as e:
        await msg.edit(f"**Error:** `{e}`")


@ultroid_cmd(pattern="padmin$", groups_only=True)
async def fake_admin_anim(event):
    """Fake admin promotion animation."""
    frames = [
        "**Promoting User As Admin...**",
        "**Enabling All Permissions...**",
        "**(1) Send Messages: ☑️**",
        "**(1) Send Messages: ✅**",
        "**(2) Send Media: ☑️**",
        "**(2) Send Media: ✅**",
        "**(3) Send Stickers & GIFs: ☑️**",
        "**(3) Send Stickers & GIFs: ✅**",
        "**(4) Send Polls: ☑️**",
        "**(4) Send Polls: ✅**",
        "**(5) Embed Links: ☑️**",
        "**(5) Embed Links: ✅**",
        "**(6) Add Users: ☑️**",
        "**(6) Add Users: ✅**",
        "**(7) Pin Messages: ☑️**",
        "**(7) Pin Messages: ✅**",
        "**(8) Change Chat Info: ☑️**",
        "**(8) Change Chat Info: ✅**",
        "**Permission Granted Successfully ✅**",
        f"**Promoted Successfully by: {OWNER_NAME} 👑**",
    ]
    msg = await event.eor("`promoting.......`")
    for frame in frames:
        await asyncio.sleep(1)
        await msg.edit(frame)
