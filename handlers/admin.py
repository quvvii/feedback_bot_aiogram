from dispatcher import dp, bot
from database import db
from utils import date, states, kb
from misc import config

from aiogram import types
from aiogram.dispatcher import FSMContext

import logging, datetime

# <-------------- START COMMAND -------------->
@dp.message_handler(commands=['start'], is_admin=True)
async def start_admin_cmd(message: types.Message):
    start_time = datetime.datetime.now()
    delm = await message.answer('ping')
    end_time = datetime.datetime.now()
    delta_time = (end_time - start_time).microseconds / 1000
    await bot.edit_message_text(chat_id=message.chat.id,
                                message_id=delm.message_id,
                                text=f'Привет, <b>владелец!</b>\n<i>Время ответа:</i> <code>{int(delta_time)}ms</code>')

# <-------------- ABOUT USER -------------->
@dp.message_handler(commands=['who'], is_admin=True, reply_to_message=True)
async def get_who_ask_question(message: types.Message):
    try:
        user_id = message.reply_to_message.text.split('\n')[-1].split('id')[1]
        user = await db.check_user(user_id)
        banlist = await db.check_user_banlist(user_id)

        if user[1]:
            user_link = f'<a href="t.me/{user[1]}">{user[0]}</a>'
        else:
            user_link = f'<a href="tg://openmessage?user_id={user[2]}"><b>{user[0]}</b></a>'

        msg_text = f'Это пользователь {user_link}:\n\nID: <code>{user[2]}</code>\nUsername: <code>{"@" + user[1] if user[1] else "Нету"}</code>\nПервое появление: <code>{user[3]}</code>\nЗабанен: {"✅" if banlist else "❌"}'

        await message.answer(msg_text)

    except Exception as e:
        logging.error(f'[{date.get_date()}][{message.from_user.id}] Error: {e}')

# <-------------- ADD / DELETE FROM BANLIST -------------->
@dp.message_handler(commands=['ban', 'ban_user', 'bu'], is_admin=True, reply_to_message=True)
async def ban_user(message: types.Message):
    try:
        user_id = message.reply_to_message.text.split('\n')[-1].split('id')[1]
        user = await db.check_user(user_id)

        if not user:
            await message.answer('<i>Я не нашел данного пользователя в своей базе данных.</i>')
            return
        
        await db.save_user_banlist(user_id=user_id,
                                   date=date.get_date())
        
        await message.answer(f'Пользователь <b>{user[0]}</b> успешно добавлен в банлист.')
    
    except Exception as e:
        logging.error(f'[{date.get_date()}][{message.from_user.id}] Error: {e}')

@dp.message_handler(commands=['unban', 'unban_user', 'unbu'], is_admin=True, reply_to_message=True)
async def unban_user(message: types.Message):
    try:
        user_id = message.reply_to_message.text.split('\n')[-1].split('id')[1]
        user = await db.check_user(user_id)

        if not user:
            await message.answer('<i>Я не нашел данного пользователя в своей базе данных.</i>')
            return
        
        await db.delete_banlist(user_id=user_id)
        
        await message.answer(f'Пользователь <b>{user[0]}</b> успешно удален из банлиста.')
    
    except Exception as e:
        logging.error(f'[{date.get_date()}][{message.from_user.id}] Error: {e}')

# <-------------- ANSWER -------------->
@dp.message_handler(content_types=['text'], is_admin=True, reply_to_message=True)
async def answer_question(message: types.Message):
    if '#id' in message.reply_to_message.text:
        question_user_id = message.reply_to_message.text.split('\n')[-1].split('id')[1]
    
    else:
        await message.answer('<i>Похоже, сособщение на которое вы ответили не является вопросом. Повторите попытку</i>')
        return
    
    if message.text.startswith('/'):
        return
    
    try:
        await bot.send_message(chat_id=question_user_id,
                               text=f'<i>Ответ на ваш вопрос:</i>\n{message.text}')
        
        await message.answer('Я успешно отправил ответ на вопрос.')
    
    except Exception as e:
        logging.error(f'[{date.get_date()}][{message.from_user.id}] Error: {e}')
    