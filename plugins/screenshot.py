# Bankai - UserBot
# Ported from CatUserBot by TgCatUB
"""
✘ Commands Available -

• `{i}ss <url>`
    Take a screenshot of any website.
"""

import os
from . import ultroid_cmd
from pyUltroid import udB


@ultroid_cmd(pattern="ss (.+)")
async def take_screenshot(event):
    """Screenshot a website URL."""
    url = event.pattern_match.group(1).strip()
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    msg = await event.eor(f"`📸 Capturing {url}...`")
    api_key = udB.get_key("SCREENSHOT_API_KEY")
    try:
        import aiohttp
        if api_key:
            api_url = f"https://api.screenshotapi.net/screenshot?token={api_key}&url={url}&output=image&file_type=png&wait_for_event=load"
        else:
            # Free fallback: thum.io
            api_url = f"https://image.thum.io/get/width/1280/{url}"
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as resp:
                if resp.status != 200:
                    return await msg.edit("`Failed to take screenshot.`")
                content = await resp.read()
        fname = "screenshot.png"
        with open(fname, "wb") as f:
            f.write(content)
        await event.client.send_file(
            event.chat_id,
            fname,
            caption=f"📸 **Screenshot of:** `{url}`",
            reply_to=event.reply_to_msg_id,
        )
        await msg.delete()
        os.remove(fname)
    except Exception as e:
        await msg.edit(f"**Error:** `{e}`")
