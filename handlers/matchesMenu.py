from tokenBot import dp, bot
from aiogram import types
from keyboards import i_k_matches, i_k_main_menu, i_k_match_day


@dp.callback_query_handler(lambda call: call.data == "matches" or
                                        call.data == "live_back" or
                                        call.data == "day_back")
async def matches_menu(call):

    await bot.edit_message_text(text='choose',
                                chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                reply_markup=await i_k_matches()
                                )


@dp.callback_query_handler(lambda call: call.data == "matches_back")
async def matches_back(call):
    await bot.edit_message_text(text="MENU",
                                chat_id=call.message.chat.id,
                                reply_markup=i_k_main_menu(),
                                message_id=call.message.message_id
                                )



