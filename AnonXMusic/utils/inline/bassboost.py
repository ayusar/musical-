# AnonXMusic/utils/inline/bassboost.py
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup(_, chat_id):
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="🔈 Off",
                    callback_data=f"BassBoostUP {chat_id}|0",
                ),
                InlineKeyboardButton(
                    text="🔉 Low",
                    callback_data=f"BassBoostUP {chat_id}|5",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🔊 Medium",
                    callback_data=f"BassBoostUP {chat_id}|10",
                ),
                InlineKeyboardButton(
                    text="📢 High",
                    callback_data=f"BassBoostUP {chat_id}|15",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="💥 Extreme",
                    callback_data=f"BassBoostUP {chat_id}|20",
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
