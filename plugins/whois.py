# Bankai - UserBot
# Ported from CatUserBot by TgCatUB
"""
✘ Commands Available -

• `{i}whois` (reply or mention)
    Get detailed info about a user.
"""

from . import ultroid_cmd, inline_mention


@ultroid_cmd(pattern="whois(?:\s|$)([\s\S]*)")
async def whois_user(event):
    """Get full user info."""
    msg = await event.eor("`🔍 Fetching user info...`")
    reply = await event.get_reply_message()
    input_str = event.pattern_match.group(1).strip()
    try:
        if reply:
            user = await event.client.get_entity(reply.sender_id)
        elif input_str:
            user = await event.client.get_entity(input_str)
        else:
            user = await event.client.get_entity(event.sender_id)
    except Exception as e:
        return await msg.edit(f"**Error:** `{e}`")

    if not user:
        return await msg.edit("`Couldn't fetch user.`")

    name = f"{getattr(user, 'first_name', '') or ''} {getattr(user, 'last_name', '') or ''}".strip()
    username = f"@{user.username}" if getattr(user, 'username', None) else "None"
    dc = getattr(getattr(user, 'photo', None), 'dc_id', 'Unknown')
    is_bot = "✅" if getattr(user, 'bot', False) else "❌"
    is_verified = "✅" if getattr(user, 'verified', False) else "❌"
    is_scam = "⚠️ YES" if getattr(user, 'scam', False) else "❌ No"
    is_fake = "⚠️ YES" if getattr(user, 'fake', False) else "❌ No"
    is_restricted = "⚠️ YES" if getattr(user, 'restricted', False) else "❌ No"

    try:
        photos = await event.client.get_profile_photos(user.id, limit=1)
        photo_count = photos.total if hasattr(photos, 'total') else len(photos)
    except Exception:
        photo_count = "N/A"

    text = (
        f"👤 **User Info**\n\n"
        f"**Name:** {name}\n"
        f"**ID:** `{user.id}`\n"
        f"**Username:** {username}\n"
        f"**DC Server:** `{dc}`\n"
        f"**Bot:** {is_bot}\n"
        f"**Verified:** {is_verified}\n"
        f"**Scam:** {is_scam}\n"
        f"**Fake:** {is_fake}\n"
        f"**Restricted:** {is_restricted}\n"
        f"**Profile Photos:** `{photo_count}`\n"
        f"**Mention:** {inline_mention(user)}"
    )
    await msg.edit(text)
