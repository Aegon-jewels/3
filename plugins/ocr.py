# Bankai - UserBot
# Ported from CatUserBot by TgCatUB
"""
✘ Commands Available -

• `{i}ocr` (reply to image)
    Extract text from an image using OCR.
"""

import os
from . import ultroid_cmd, async_searcher
from pyUltroid import udB


@ultroid_cmd(pattern="ocr$")
async def ocr_image(event):
    """Extract text from replied image."""
    reply = await event.get_reply_message()
    if not (reply and reply.media):
        return await event.eor("`Reply to an image to extract text.`")
    msg = await event.eor("`🔍 Reading image...`")
    file = await reply.download_media()
    if not file:
        return await msg.edit("`Failed to download image.`")
    api_key = udB.get_key("OCR_SPACE_API_KEY") or "helloworld"
    try:
        import aiohttp
        async with aiohttp.ClientSession() as session:
            with open(file, "rb") as f:
                data = aiohttp.FormData()
                data.add_field("file", f, filename="image.png", content_type="image/png")
                data.add_field("apikey", api_key)
                data.add_field("language", "eng")
                async with session.post("https://api.ocr.space/parse/image", data=data) as resp:
                    result = await resp.json()
        parsed = result.get("ParsedResults", [])
        if parsed:
            text = parsed[0].get("ParsedText", "").strip()
            if text:
                await msg.edit(f"**📝 Extracted Text:**\n\n`{text}`")
            else:
                await msg.edit("`No text found in image.`")
        else:
            await msg.edit("`OCR failed. Try another image.`")
    except Exception as e:
        await msg.edit(f"**Error:** `{e}`")
    finally:
        try:
            os.remove(file)
        except Exception:
            pass
