# AnonXMusic/plugins/admins/bassboost.py
from pyrogram import filters
from pyrogram.types import Message

from AnonXMusic import app
from AnonXMusic.core.call import Anony
from AnonXMusic.misc import db
from AnonXMusic.utils.database import is_active_chat
from AnonXMusic.utils.decorators.language import language, languageCB
from AnonXMusic.utils.inline import bassboost_markup, close_markup
from config import BANNED_USERS

checker = []


@app.on_message(
    filters.command(["bassboost", "bass", "cbass", "cbassboost"])
    & filters.group
    & ~BANNED_USERS
)
@language
async def bassboost(cli, message: Message, _):
    chat_id = message.chat.id
    playing = db.get(chat_id)
    if not playing:
        return await message.reply_text(_["queue_2"])
    duration_seconds = int(playing[0]["seconds"])
    if duration_seconds == 0:
        return await message.reply_text(_["bass_1"])
    file_path = playing[0]["file"]
    if "downloads" not in file_path:
        return await message.reply_text(_["bass_1"])
    upl = bassboost_markup(_, chat_id)
    return await message.reply_text(
        text=_["bass_2"].format(app.mention),
        reply_markup=upl,
    )


@app.on_callback_query(filters.regex("BassBoostUP") & ~BANNED_USERS)
@languageCB
async def bass_callback(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    chat, level = callback_request.split("|")
    chat_id = int(chat)
    if not await is_active_chat(chat_id):
        return await CallbackQuery.answer(_["general_5"], show_alert=True)
    playing = db.get(chat_id)
    if not playing:
        return await CallbackQuery.answer(_["queue_2"], show_alert=True)
    duration_seconds = int(playing[0]["seconds"])
    if duration_seconds == 0:
        return await CallbackQuery.answer(_["bass_1"], show_alert=True)
    file_path = playing[0]["file"]
    if "downloads" not in file_path:
        return await CallbackQuery.answer(_["bass_1"], show_alert=True)
    check_bass = (playing[0]).get("bass")
    if check_bass:
        if str(check_bass) == str(level):
            if str(level) == str("0"):
                return await CallbackQuery.answer(
                    _["bass_3"],
                    show_alert=True,
                )
    else:
        if str(level) == str("0"):
            return await CallbackQuery.answer(
                _["bass_3"],
                show_alert=True,
            )
    if chat_id in checker:
        return await CallbackQuery.answer(
            _["bass_4"],
            show_alert=True,
        )
    else:
        checker.append(chat_id)
    try:
        await CallbackQuery.answer(
            _["bass_5"],
        )
    except:
        pass
    mystic = await CallbackQuery.edit_message_text(
        text=_["bass_6"].format(CallbackQuery.from_user.mention),
    )
    try:
        await Anony.bassboost_stream(
            chat_id,
            file_path,
            level,
            playing,
        )
    except:
        if chat_id in checker:
            checker.remove(chat_id)
        return await mystic.edit_text(_["bass_7"], reply_markup=close_markup(_))
    if chat_id in checker:
        checker.remove(chat_id)
    await mystic.edit_text(
        text=_["bass_8"].format(level, CallbackQuery.from_user.mention),
        reply_markup=close_markup(_),
    )
