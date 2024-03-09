from dispatcher import dp, bot
from database import db
from utils import date, states, kb
from misc import config

from aiogram import types
from aiogram.dispatcher import FSMContext

import logging

# <-------------- START COMMAND -------------->
@dp.message_handler(commands=['start'], is_user=True)
async def start_cmd(message: types.Message):
    user = await db.check_user(user_id=message.from_user.id)
    banlist = await db.check_user_banlist(user_id=message.from_user.id)

    if user:
        if banlist:
            await message.answer('Вы были забанены в боте.')
            return

    else:
        await db.save_user(
            name=message.from_user.full_name,
            username=message.from_user.username,
            user_id=message.from_user.id,
            date=date.get_date()
        )

    await bot.send_photo(chat_id=message.chat.id,
                        photo='https://ibb.co/r0YN5Dd',
                        caption=f'Привет, <b>{message.from_user.full_name}</b>! Через меня ты можешь задать вопрос владельцу. <i>Напиши свой вопрос:</i>',
                        reply_markup=kb.cancel_kb())
    
    await states.UserState.user_text.set()

# <-------------- SEND QUESTION -------------->
@dp.message_handler(state=states.UserState.user_text, content_types=['text'])
async def send_question_to_admin(message: types.Message, state: FSMContext):
    try:
        if message.text != '❌Отмена':
            await bot.send_message(chat_id=config.admin_id,
                                   text=f'<b>Новый вопрос [<code>{date.get_date()}</code>]:</b>\n{message.text}\n\n#id{message.from_user.id}')
            
            await message.answer('<b>Я отправил твой вопрос!</b> Жди ответа.',
                                 reply_markup=kb.clear_kb())
        
        else:
            await message.answer('Отмена действия.', 
                                 reply_markup=kb.clear_kb())
        
        await state.finish()
            
    except Exception as e:
        logging.error(f'[{date.get_date()}][{message.from_user.id}] Error: {e}')
