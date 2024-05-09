from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)



async def start_menu_keyboard():
    registration_button = InlineKeyboardButton(
        text='Registration',
        callback_data='registration'
    )
    my_profile_button = InlineKeyboardButton(
        text='My Profile',
        callback_data='my_profile'
    )
    profiles_button = InlineKeyboardButton(
        text='View Profiles',
        callback_data='view_profiles'
    )

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [registration_button],
            [profiles_button],
            [my_profile_button]
        ]
    )
    return markup