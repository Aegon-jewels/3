# Bankai - UserBot
# Ported from CatUserBot by TgCatUB
"""
✘ Commands Available -

• `{i}create b <name>`
    Create a private supergroup.

• `{i}create g <name>`
    Create a private basic group.

• `{i}create c <name>`
    Create a private channel.
"""

from telethon.tl import functions

from . import ultroid_cmd, eor, eod
from pyUltroid import udB


@ultroid_cmd(
    pattern="create (b|g|c) ([\s\S]+)",
)
async def create_chat(event):
    """Create private group/channel/supergroup."""
    type_of = event.pattern_match.group(1)
    name = event.pattern_match.group(2)
    client = event.client
    bot_uname = udB.get_key("BOT_USERNAME") or udB.get_key("TG_BOT_USERNAME")
    desc = f"Created using Bankai Bot | {'Channel' if type_of == 'c' else 'Group'}: {name}"
    msg = await event.eor("`Creating...`")

    if type_of == "g":
        try:
            result = await client(
                functions.messages.CreateChatRequest(
                    users=[bot_uname],
                    title=name,
                )
            )
            chat_id = result.chats[0].id
            inv = await client(
                functions.messages.ExportChatInviteRequest(peer=chat_id)
            )
            await msg.edit(f"✅ Group **{name}** created!\nJoin: {inv.link}")
        except Exception as e:
            await msg.edit(f"**Error:** `{e}`")

    elif type_of == "c":
        try:
            r = await client(
                functions.channels.CreateChannelRequest(
                    title=name, about=desc, megagroup=False
                )
            )
            chat_id = r.chats[0].id
            inv = await client(
                functions.messages.ExportChatInviteRequest(peer=chat_id)
            )
            await msg.edit(f"✅ Channel **{name}** created!\nJoin: {inv.link}")
        except Exception as e:
            await msg.edit(f"**Error:** `{e}`")

    elif type_of == "b":
        try:
            r = await client(
                functions.channels.CreateChannelRequest(
                    title=name, about=desc, megagroup=True
                )
            )
            chat_id = r.chats[0].id
            await client(
                functions.channels.InviteToChannelRequest(
                    channel=chat_id, users=[bot_uname]
                )
            )
            inv = await client(
                functions.messages.ExportChatInviteRequest(peer=chat_id)
            )
            await msg.edit(f"✅ Supergroup **{name}** created!\nJoin: {inv.link}")
        except Exception as e:
            await msg.edit(f"**Error:** `{e}`")
    else:
        await msg.edit("`Invalid type. Use b, g or c.`")
