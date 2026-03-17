# Bankai - UserBot
# Ported from CatUserBot by TgCatUB
"""
✘ Commands Available -

• `{i}dart [1-6]`
    Send dart emoji with specific outcome.

• `{i}dice [1-6]`
    Send dice emoji with specific outcome.

• `{i}bb [1-5]`
    Send basketball emoji with specific outcome.

• `{i}fb [1-5]`
    Send football emoji with specific outcome.

• `{i}jp [1-64]`
    Send jackpot/slot emoji with specific outcome.

• `{i}bowl [1-6]`
    Send bowling emoji with specific outcome.
"""

import contextlib
from telethon.tl.types import InputMediaDice
from . import ultroid_cmd

DART = "🎯"
DICE = "🎲"
BALL = "🏀"
FOOT = "⚽"
SLOT = "🎰"
BOWL = "🎳"


async def _play_dice(event, emoticon, target, max_val):
    if not (1 <= target <= max_val):
        return await event.eor(f"`Value must be between 1 and {max_val}.`")
    reply = await event.get_reply_message() or event
    await event.delete()
    r = await reply.reply(file=InputMediaDice(emoticon=emoticon))
    with contextlib.suppress(Exception):
        while r.media.value != target:
            await r.delete()
            r = await reply.reply(file=InputMediaDice(emoticon=emoticon))


@ultroid_cmd(pattern=f"(dart|{DART}) ([1-6])$", groups_only=True)
async def _dart(event):
    await _play_dice(event, DART, int(event.pattern_match.group(2)), 6)


@ultroid_cmd(pattern=f"(dice|{DICE}) ([1-6])$", groups_only=True)
async def _dice(event):
    await _play_dice(event, DICE, int(event.pattern_match.group(2)), 6)


@ultroid_cmd(pattern=f"(bb|{BALL}) ([1-5])$", groups_only=True)
async def _ball(event):
    await _play_dice(event, BALL, int(event.pattern_match.group(2)), 5)


@ultroid_cmd(pattern=f"(fb|{FOOT}) ([1-5])$", groups_only=True)
async def _foot(event):
    await _play_dice(event, FOOT, int(event.pattern_match.group(2)), 5)


@ultroid_cmd(pattern=f"(jp|{SLOT}) ([0-9]+)$", groups_only=True)
async def _slot(event):
    val = int(event.pattern_match.group(2))
    await _play_dice(event, SLOT, val, 64)


@ultroid_cmd(pattern=f"(bowl|{BOWL}) ([1-6])$", groups_only=True)
async def _bowl(event):
    await _play_dice(event, BOWL, int(event.pattern_match.group(2)), 6)
