import sqlite3

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.deep_linking import create_start_link

from config import bot, ADMIN_ID, MEDIA_PATH
from database import sql_queries
from database.a_db import AsyncDatabase
from const import START_MENU_TEXT
from keyboards.start import start_menu_keyboard


router = Router()


@router.message(Command("start"))
async def start_menu(message: types.Message,
                     db=AsyncDatabase()):
    command = message.text
    token = command.split()
    print(token)
    if len (token) > 1:
        await process_reference_link(token[1],
                                     message)


    await db.execute_query(
        query=sql_queries.INSERT_USER_QUERY,
        params=(
            None,
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
            None,
            0

        ),
        fetch='none'
    )

    animation_file = types.FSInputFile(MEDIA_PATH + 'giphy.gif')
    await bot.send_animation(
        chat_id=message.from_user.id,
        animation=animation_file,
        caption=START_MENU_TEXT.format(
            user=message.from_user.first_name
        ),
        reply_markup=await start_menu_keyboard()
    )


async def process_reference_link(token, message, db=AsyncDatabase()):
    link = await create_start_link(bot=bot, payload=token)
    owner = await db.execute_query(
        query=sql_queries.SELECT_USER_BY_LINK_QUERY,
        params=(
            link,
        ),
        fetch='one'
    )

    if owner['TELEGRAM_USER_ID'] == message.from_user.id:
        await bot.send_message(
            chat_id=message.from_user.id,
            text='You can not use your own link'
        )
        return
    try:
        await db.execute_query(
            query=sql_queries.INSERT_REFERENCE_USER_QUERY,
            params=(
                None,
                owner['TELEGRAM_USER_ID'],
                message.from_user.id,
            ),
            fetch='one'
        )

        await db.execute_query(
            query=sql_queries.UPDATE_USER_BALANCE_QUERY,
            params=(
                owner['TELEGRAM_USER_ID'],

            ),
            fetch='one'
        )
        await bot.send_message(
            chat_id=owner['TELEGRAM_USER_ID'],
            text='You got new reference user\n'
                 'Congrats'
        )
    except sqlite3.IntegrityError:
        await bot.send_message(
            chat_id=message.from_user.id,
            text='You have used this link'
        )



@router.message(lambda message: message.text == "ak47")
async def admin_start_menu(message: types.Message,
                           db=AsyncDatabase()):
    if int(ADMIN_ID) == message.from_user.id:
        await bot.send_message(
            chat_id=message.from_user.id,
            text="Here is your Admin page"
        )
    else:
        await bot.send_message(
            chat_id=message.from_user.id,
            text="you are not an administrator"
        )