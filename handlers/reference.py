import binascii
import os
import sqlite3

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile
from aiogram.utils.deep_linking import create_start_link

from config import bot, ADMIN_ID, MEDIA_PATH
from const import PROFILE_TEXT
from database import sql_queries
from database.a_db import AsyncDatabase
from keyboards.reference import reference_menu_keyboard
from keyboards.start import start_menu_keyboard

router = Router()


@router.callback_query(lambda call: call.data == "reference_menu")
async def reference_menu(call: types.CallbackQuery):
    await bot.send_message(
        chat_id=call.from_user.id,
        text="Hi, This is Reference Menu\n"
             "u can create Reference link, share with ur friends\n"
             "We will send to ur account wallet 100 points",
        reply_markup=await reference_menu_keyboard()
    )


@router.callback_query(lambda call: call.data == "reference_link")
async def reference_link_creation(call: types.CallbackQuery,
                                  db=AsyncDatabase()):
    token = binascii.hexlify(os.urandom(8)).decode()
    print(token)
    link = await create_start_link(bot=bot, payload=token)
    print(link)
    user = await db.execute_query(
        query=sql_queries.SELECT_USER_QUERY,
        params=(
            call.from_user.id,
        ),
        fetch='one'
    )
    print(user)
    if user['REFERENCE_LINK']:
        await bot.send_message(
            chat_id=call.from_user.id,
            text=f"Your old link {user['REFERENCE_LINK']}"
        )
    else:
        await db.execute_query(
            query=sql_queries.UPDATE_USER_LINK_QUERY,
            params=(
                link,
                call.from_user.id,
            ),
            fetch='none'
        )
        await bot.send_message(
            chat_id=call.from_user.id,
            text=f"Your new link {link}"
        )


@router.callback_query(lambda call: call.data == "reference_balance")
async def view_balance(call: types.CallbackQuery,
                       db=AsyncDatabase()):
    user = await db.execute_query(
        query=sql_queries.SELECT_USER_QUERY,
        params=(
            call.from_user.id,
        ),
        fetch='one'
    )
    await bot.send_message(
        chat_id=call.from_user.id,
        text=f"Your balance: {user['BALANCE']}"
    )


# @router.callback_query(lambda call: call.data == "reference_list")
# async def view_list(call: types.CallbackQuery,
#                     db=AsyncDatabase()):
#     await db.execute_query(
#         query=sql_queries.SELECT_REFERENCE_QUERY,
#         params=(
#             call.from_user.id,
#         ),
#         fetch='one'
#     )
#     await bot.send_message(
#         chat_id=call.from_user.id,
#         text=f'{user['OWNER_TELEGRAM_ID']}'
#     )