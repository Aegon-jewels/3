# Bankai - UserBot
# Ported from CatUserBot by TgCatUB
"""
✘ Commands Available -

• `{i}q` (reply to a message)
    Generate a Telegram-style quote sticker of the message.
"""

import os
from . import ultroid_cmd


@ultroid_cmd(pattern="q$")
async def make_quote(event):
    """Create a quote sticker from replied message."""
    reply = await event.get_reply_message()
    if not reply:
        return await event.eor("`Reply to a message to quote it.`")
    msg = await event.eor("`✍️ Generating quote...`")
    try:
        import aiohttp
        sender = await reply.get_sender()
        name = getattr(sender, 'first_name', 'Unknown') or 'Unknown'
        if getattr(sender, 'last_name', None):
            name += f" {sender.last_name}"
        color = "#1a1a2e"
        # Download sender photo
        photo_b64 = None
        try:
            import base64
            import io
            photo_bytes = io.BytesIO()
            await event.client.download_profile_photo(sender.id, file=photo_bytes)
            photo_bytes.seek(0)
            data = photo_bytes.read()
            if data:
                photo_b64 = base64.b64encode(data).decode()
        except Exception:
            pass

        payload = {
            "type": "quote",
            "format": "webp",
            "backgroundColor": color,
            "width": 512,
            "height": 512,
            "scale": 2,
            "messages": [
                {
                    "entities": [],
                    "avatar": True,
                    "from": {
                        "id": sender.id,
                        "name": name,
                        "photo": {"url": f"data:image/jpeg;base64,{photo_b64}"} if photo_b64 else None,
                    },
                    "text": reply.text or "[media]",
                    "replyMessage": {},
                }
            ],
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://bot.lyo.su/quote/generate",
                json=payload,
                headers={"Content-Type": "application/json"},
            ) as resp:
                if resp.status != 200:
                    return await msg.edit("`Quote API failed. Try again later.`")
                result = await resp.json()
                b64img = result.get("image") or result.get("result", {}).get("image")
                if not b64img:
                    return await msg.edit("`Couldn't generate quote.`")
                import base64
                img_data = base64.b64decode(b64img)
                fname = "quote_sticker.webp"
                with open(fname, "wb") as f:
                    f.write(img_data)
        await event.client.send_file(
            event.chat_id,
            fname,
            reply_to=event.reply_to_msg_id,
        )
        await msg.delete()
        os.remove(fname)
    except Exception as e:
        await msg.edit(f"**Error:** `{e}`")
