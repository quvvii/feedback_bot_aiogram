from aiogram import types

def cancel_kb():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(types.KeyboardButton(text='❌Отмена'))

    return kb

def clear_kb():
    return types.ReplyKeyboardRemove()
