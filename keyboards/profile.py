from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)



async def my_profile_keyboard():
    update_button = InlineKeyboardButton(
        text='Update',
        callback_data='update_profile'
    )
    delete_button = InlineKeyboardButton(
        text='Delete',
        callback_data='delete_profile'
    )
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [update_button],
            [delete_button]
        ]
    )
    return markup