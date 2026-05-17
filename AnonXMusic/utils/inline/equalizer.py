# AnonXMusic/utils/inline/equalizer.py
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup(_, chat_id):
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="📊 Flat",
                    callback_data=f"EQPreset {chat_id}|flat",
                ),
                InlineKeyboardButton(
                    text="🔊 Bass Boost",
                    callback_data=f"EQPreset {chat_id}|bass_boost",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🎸 Rock",
                    callback_data=f"EQPreset {chat_id}|rock",
                ),
                InlineKeyboardButton(
                    text="🎵 Pop",
                    callback_data=f"EQPreset {chat_id}|pop",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🎤 Vocal",
                    callback_data=f"EQPreset {chat_id}|vocal",
                ),
                InlineKeyboardButton(
                    text="🌙 Lofi",
                    callback_data=f"EQPreset {chat_id}|lofi",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_["CLOSE_BUTTON"],
                    callback_data="close",
                ),
            ],
        ]
    )
    return upl
