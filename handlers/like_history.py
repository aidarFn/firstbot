import sqlite3
import re
import random

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from config import bot, ADMIN_ID, MEDIA_PATH
from database import sql_queries
from database.a_db import AsyncDatabase
from const import PROFILE_TEXT
from keyboards.start import start_menu_keyboard
from keyboards.like_dislike import like_dislike_keyboard
from keyboards.like_dislike import history_keyboard


router = Router()


@router.callback_query(lambda call: call.data == 'history')
async def detect_like_history_call(call: types.CallbackQuery,
                                   db=AsyncDatabase()):
    profiles = await db.execute_query(
        query=sql_queries.SELECT_LIKE_PROFILES,
        params=(
            call.from_user.id,
        ),
        fetch='all'
    )
    print(profiles)
    randomizer = random.choice(profiles)
    random_profile = await db.execute_query(
        query=sql_queries.SELECT_PROFILE_QUERY,
        params=(
            randomizer['OWNER_TELEGRAM_ID'],
        ),
        fetch='one'
    )
    photo = types.FSInputFile(random_profile["PHOTO"])
    await bot.send_photo(
        chat_id=call.from_user.id,
        photo=photo,
        caption=PROFILE_TEXT.format(
            nickname=random_profile['NICKNAME'],
            bio=random_profile['BIO']
        ),
        reply_markup=await history_keyboard(tg_id=random_profile['TELEGRAM_ID'])
    )