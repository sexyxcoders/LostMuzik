import asyncio
import importlib
import sys

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from config import BANNED_USERS
from LostMuzik import LOGGER, app, userbot
from LostMuzik.core.call import LostMuzik
from LostMuzik.plugins import ALL_MODULES
from LostMuzik.utils.database import get_banned_users, get_gbanned

# 🔁 Async event loop
loop = asyncio.get_event_loop_policy().get_event_loop()


async def init():
    """
    🔰 Main startup function
    - Assistants check
    - Spotify vars check
    - Banned users load
    - Bot + Userbot + VC start
    """

    # ❌ Koi bhi assistant string nahi mila
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER("LostMuzik").error(
            "❌ Koi bhi Assistant Client define nahi hai! Bot band kiya ja raha hai."
        )
        return

    # ⚠️ Spotify vars missing (warning only)
    if not config.SPOTIFY_CLIENT_ID and not config.SPOTIFY_CLIENT_SECRET:
        LOGGER("LostMuzik").warning(
            "⚠️ Spotify credentials set nahi hain. Spotify songs play nahi honge."
        )

    # 🚫 Database se banned users load karo
    try:
        gbanned_users = await get_gbanned()
        for user_id in gbanned_users:
            BANNED_USERS.add(user_id)

        banned_users = await get_banned_users()
        for user_id in banned_users:
            BANNED_USERS.add(user_id)

    except Exception as e:
        LOGGER("LostMuzik").warning(
            f"⚠️ Banned users load karte waqt error aaya: {e}"
        )

    # 🤖 Main bot start
    await app.start()

    # 📦 Saare plugins import karo
    for module in ALL_MODULES:
        importlib.import_module("LostMuzik.plugins" + module)

    LOGGER("LostMuzik.plugins").info(
        "✅ Saare plugins successfully load ho gaye"
    )

    # 👤 Userbot (assistants) start
    await userbot.start()

    # 🎧 Voice call client start
    await LostMuzik.start()

    # 🔊 Log group me VC ON hai ya nahi — test stream
    try:
        await LostMuzik.stream_call(
            "http://docs.evostream.com/sample_content/assets/sintel1m720p.mp4"
        )

    except NoActiveGroupCall:
        LOGGER("LostMuzik").error(
            "❌ LOG GROUP me Voice Chat OFF hai!\n"
            "👉 Please apne Log Group ka voice chat ON rakhein.\n"
            "👉 Voice chat band ya end nahi honi chahiye."
        )
        sys.exit()

    except Exception:
        # Agar test silently fail ho jaaye to ignore
        pass

    # 🧩 Extra decorators / handlers load
    await LostMuzik.decorators()

    LOGGER("LostMuzik").info(
        "🚀 Lost Muzik Bot successfully start ho gaya!"
    )

    # ⏳ Bot idle state (running)
    await idle()


# ▶️ Entry point
if __name__ == "__main__":
    loop.run_until_complete(init())
    LOGGER("LostMuzik").info("🛑 Lost Muzik Bot band ho gaya")