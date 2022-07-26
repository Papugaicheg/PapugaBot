import time

from tokenBot import dp, bot
from aiogram import types
from parserBot import db_parser
from dataBase import db_select
from keyboards import i_k_live_matches, i_k_match_day, i_k_match
from keyboards import cb, cb_for_match, cb_back


@dp.callback_query_handler(lambda call: call.data == 'reload')
async def db_reload(call):
    await db_parser()


@dp.callback_query_handler(lambda call: call.data == "live")
async def live_matches_printer(call):
    await bot.edit_message_text(text="Live:",
                                chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                reply_markup=await i_k_live_matches()
                                )

@dp.callback_query_handler(cb_for_match.filter())
async def match_button_id_handler(call, callback_data):
    id = (callback_data["id"])
    data = await db_select('''Select team1, team2, event, maps, meta, CAST ([PapugaBot].[dbo].[match].date_time as smalldatetime), [PapugaBot].[dbo].[match].match_id from [PapugaBot].[dbo].[match] join [PapugaBot].[dbo].[teams] on [PapugaBot].[dbo].[match].match_id=[PapugaBot].[dbo].[teams].match_id where [PapugaBot].[dbo].[match].match_id = ?''', (id,))
    for info in data:
        msg = f"{info[0]} vs {info[1]}\n {info[2]} \n {info[3]} \n {info[4]} \n {info[5]} \n {info[6]}"
    await bot.edit_message_text(text=msg,
                                chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                reply_markup=await i_k_match(id))

@dp.callback_query_handler(cb.filter())
async def matches_button_id_handler(call, callback_data):
    date = (callback_data["date"])
    print(date)
    print(123123)
    await bot.edit_message_text(text="Matches for that: "+date,
                                chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                reply_markup=await i_k_match_day(date)
                                )

@dp.callback_query_handler(cb_back.filter())
async def match_back(call, callback_data):
    id = (callback_data['id'])
    date = await db_select('''SELECT FORMAT(CAST (date_time as date),'MM-dd') from match where match_id = ?''', (id, ))
    print(f"if = {id} date = {date}")
    await bot.edit_message_text(text="Choose match",
                                chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                reply_markup=await i_k_match_day(date)
                                )



