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
from keyboards.profile import my_profile_keyboard


router = Router()


class DonateStateGroup(StatesGroup):
    amount = State()


@router.callback_query(lambda call: 'donate_' in call.data)
async def detect_donate_call(call: types.CallbackQuery,
                             state: FSMContext,
                             db=AsyncDatabase()):
    recipient_id = call.data.replace('donate_', '')
    print(recipient_id)
    donate_user = await db.execute_query(
        query=sql_queries.SELECT_USER_QUERY,
        params=(
            call.from_user.id,
        ),
        fetch='one'
    )
    print(donate_user)
    await bot.send_message(
        chat_id=call.from_user.id,
        text='How much do you want to donate?\n'
             f'Your balance: {donate_user["BALANCE"]}',
    )
    await state.update_data(owner_id=recipient_id)
    await state.update_data(balance_limit=donate_user['BALANCE'])
    await state.set_state(DonateStateGroup.amount)


@router.message(DonateStateGroup.amount)
async def process_donate_amount(message: types.Message,
                                state: FSMContext,
                                db=AsyncDatabase()):
    data = await state.get_data()
    print(data)

    try:
        int(message.text)
        if int(message.text) < 1:
            await bot.send_message(
                chat_id=message.chat.id,
                text='Please send more than 1 dollar'
            )
            await state.clear()
            return

        if int(message.text) <= data['balance_limit']:
            await db.execute_query(
                query=sql_queries.UPDATE_SENDER_BALANCE_QUERY,
                params=(
                    int(message.text),
                     message.from_user.id,
                ),
                fetch='none'
            )
            await db.execute_query(
                query=sql_queries.UPDATE_RECIPIENT_BALANCE_QUERY,
                params=(
                    int(message.text),
                    data['owner_id'],
                ),
                fetch='none'
            )
            await db.execute_query(
                query=sql_queries.INSERT_DONATE_TARNSACTIONS_QUERY,
                params=(
                    None,
                    message.from_user.id,
                    data['owner_id'],
                    int(message.text),
                ),
                fetch='none'
            )
            await bot.send_message(
                chat_id=data['owner_id'],
                text=f'Someone sent to you donate\n'
                     f'Amount of donate: {message.text}'
            )
            await bot.send_message(
                chat_id=message.from_user.id,
                text='Donate successful!'
            )
        else:
            await bot.send_message(
                chat_id=message.chat.id,
                text='not enough money!'
            )
            await state.clear()
            return

    except ValueError:
        await bot.send_message(
            chat_id=message.chat.id,
            text='Please use numeric answer'
        )
        await state.clear()
        return

