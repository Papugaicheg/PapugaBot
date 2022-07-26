from aiogram import types
from tokenBot import bot, dp
@dp.message_handler(content_types=['text'])
async def message_come(message: types.Message):
    await bot.delete_message(message_id=message.message_id, chat_id= message.chat.id)
