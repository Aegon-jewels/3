# Bankai - UserBot
# Ported from CatUserBot by TgCatUB
"""
✘ Commands Available -

• `{i}getid`
    Get your ID and current chat ID.

• `{i}getid` (reply to user)
    Get that user's ID, username and DC.

• `{i}getid` (reply to forwarded msg)
    Get the original sender's ID.
"""

from . import ultroid_cmd


@ultroid_cmd(pattern="getid$")
async def get_id(event):
    """Get user/chat IDs."""
    reply = await event.get_reply_message()
    if not reply:
        text = (
            f"🆔 **Your ID:** `{event.sender_id}`\n"
            f"💬 **Chat ID:** `{event.chat_id}`"
        )
        return await event.eor(text)

    # Forwarded message — get original sender
    if reply.forward and reply.forward.sender_id:
        fwd_id = reply.forward.sender_id
        text = f"↪️ **Original Sender ID:** `{fwd_id}`"
        return await event.eor(text)

    # Reply to a user
    user = await reply.get_sender()
    if not user:
        return await event.eor("`Couldn't fetch user info.`")

    username = f"@{user.username}" if getattr(user, 'username', None) else "No username"
    dc = getattr(getattr(user, 'photo', None), 'dc_id', 'Unknown')
    text = (
        f"🆔 **User ID:** `{user.id}`\n"
        f"👤 **Name:** {user.first_name or ''} {user.last_name or ''}\n"
        f"🔗 **Username:** {username}\n"
        f"🌐 **DC:** `{dc}`"
    )
    await event.eor(text)
