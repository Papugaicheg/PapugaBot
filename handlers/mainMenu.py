
from aiogram import types
from keyboards import i_k_main_menu

from tokenBot import bot, dp

last_message_id = {}


@dp.message_handler(commands=['start', 'restart'])
async def main_menu(message: types.Message):
    if message.text == '/start':
        await message.delete()
        msg = await bot.send_message(text="MENU",
                                     chat_id=message.chat.id,
                                     reply_markup=i_k_main_menu())
        last_message_id[message.chat.id] = msg.message_id
    elif message.text == '/restart':
        await message.delete()
        await bot.edit_message_text(text="MENU",
                                    chat_id=message.chat.id,
                                    reply_markup=i_k_main_menu(),
                                    message_id=last_message_id[message.chat.id]
                                    )
