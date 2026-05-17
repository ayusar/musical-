# AnonXMusic/plugins/admins/equalizer.py
from pyrogram import filters
from pyrogram.types import Message

from AnonXMusic import app
from AnonXMusic.core.call import Anony
from AnonXMusic.misc import db
from AnonXMusic.utils.database import is_active_chat
from AnonXMusic.utils.decorators.language import language, languageCB
from AnonXMusic.utils.inline import close_markup, equalizer_markup
from config import BANNED_USERS

checker = []


@app.on_message(
    filters.command(["equalizer", "eq", "ceq", "cequalizer"])
    & filters.group
    & ~BANNED_USERS
)
@language
async def equalizer(cli, message: Message, _):
    chat_id = message.chat.id
    playing = db.get(chat_id)
    if not playing:
        return await message.reply_text(_["queue_2"])
    duration_seconds = int(playing[0]["seconds"])
    if duration_seconds == 0:
        return await message.reply_text(_["eq_1"])
    file_path = playing[0]["file"]
    if "downloads" not in file_path:
        return await message.reply_text(_["eq_1"])
    upl = equalizer_markup(_, chat_id)
    return await message.reply_text(
        text=_["eq_2"].format(app.mention),
        reply_markup=upl,
    )


@app.on_callback_query(filters.regex("EQPreset") & ~BANNED_USERS)
@languageCB
async def eq_callback(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    chat, preset = callback_request.split("|")
    chat_id = int(chat)
    if not await is_active_chat(chat_id):
        return await CallbackQuery.answer(_["general_5"], show_alert=True)
    playing = db.get(chat_id)
    if not playing:
        return await CallbackQuery.answer(_["queue_2"], show_alert=True)
    duration_seconds = int(playing[0]["seconds"])
    if duration_seconds == 0:
        return await CallbackQuery.answer(_["eq_1"], show_alert=True)
    file_path = playing[0]["file"]
    if "downloads" not in file_path:
        return await CallbackQuery.answer(_["eq_1"], show_alert=True)
    current_preset = (playing[0]).get("eq_preset")
    if current_preset and str(current_preset) == str(preset):
        return await CallbackQuery.answer(_["eq_3"], show_alert=True)
    if chat_id in checker:
        return await CallbackQuery.answer(_["eq_4"], show_alert=True)
    else:
        checker.append(chat_id)
    try:
        await CallbackQuery.answer(_["eq_5"])
    except:
        pass
    mystic = await CallbackQuery.edit_message_text(
        text=_["eq_6"].format(CallbackQuery.from_user.mention),
    )
    try:
        await Anony.equalizer_stream(
            chat_id,
            file_path,
            preset,
            playing,
        )
    except:
        if chat_id in checker:
            checker.remove(chat_id)
        return await mystic.edit_text(_["eq_7"], reply_markup=close_markup(_))
    if chat_id in checker:
        checker.remove(chat_id)
    preset_label = preset.replace("_", " ").title()
    await mystic.edit_text(
        text=_["eq_8"].format(preset_label, CallbackQuery.from_user.mention),
        reply_markup=close_markup(_),
    )
