import datetime

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from dataBase import db_select
from parserBot import get_date, get_live_matches, get_match_from_date, db_parser
from aiogram.utils.callback_data import CallbackData

cb = CallbackData("id", "date")
cb_back = CallbackData("date", "id")
cb_for_match = CallbackData("date", "id")


def i_k_main_menu():
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    reload_db_button = InlineKeyboardButton('Reload', callback_data='reload')
    matches_button = InlineKeyboardButton('Matches', callback_data='matches')

    keyboard.row(matches_button)
    keyboard.row(reload_db_button)
    return keyboard


async def i_k_match_day(date):
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)

    teams = await db_select('''SELECT [PapugaBot].[dbo].[teams].match_id, team1, team2, date_time
    FROM[PapugaBot].[dbo].[teams] WHERE FORMAT(CAST (date_time as date),'MM-dd') = ?''', (date,))

    print(teams)
    for data in teams:
        if data[3] > datetime.datetime.now():

            data_temp = (data[1] if data[1] is not None else 'NULL') + ' vs ' \
                    + (data[2] if data[2] is not None else 'NULL') + ' | ' + data[3].strftime("%H:%M")
            print(data)
            keyboard.row(InlineKeyboardButton(text=str(data_temp), callback_data=cb_for_match.new(id = data[0])))
            print(f"[{str(data_temp)}] -- cb = {data[0]}")
    print(data[0])
    keyboard.row(InlineKeyboardButton(text='Back', callback_data="matches"))

    return keyboard


async def i_k_matches():
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    keyboard.row(InlineKeyboardButton(text='Live',
                                      callback_data='live'))

    date_today = await db_select\
        ('''SELECT DISTINCT FORMAT(CAST (date_time as date),?) as DATE from [PapugaBot].[dbo].match ''', ('MM-dd',))
    print(date_today)
    for i in range(0, len(date_today) - len(date_today) % 3, +3):
        button1 = InlineKeyboardButton(text=date_today[i][0],
                                       callback_data=cb.new(date=date_today[i][0]))

        button2 = InlineKeyboardButton(text=date_today[i + 1][0],
                                       callback_data=cb.new(date=date_today[i + 1][0]))

        button3 = InlineKeyboardButton(text=date_today[i + 2][0],
                                       callback_data=cb.new(date=date_today[i + 2][0]))

        keyboard.row(button1, button2, button3)

    if len(date_today) % 3 == 2:
        button1 = InlineKeyboardButton(text=date_today[len(date_today) - 2][0],
                                       callback_data=cb.new(date=date_today[len(date_today) - 2][0]))
        button2 = InlineKeyboardButton(text=date_today[len(date_today) - 1][0],
                                       callback_data=cb.new(date=date_today[len(date_today) - 1][0]))
        keyboard.row(button1, button2)

    elif len(date_today) % 3 == 1:
        button1 = InlineKeyboardButton(text=date_today[len(date_today) - 1][0],
                                       callback_data=cb.new(date=date_today[len(date_today) - 1][0]))
        keyboard.row(button1)
    keyboard.row(InlineKeyboardButton(text='Back', callback_data='matches_back'))
    return keyboard


async def i_k_live_matches():
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    live_matches = await get_live_matches()
    for data in live_matches:
        if data is not None:
            data = data[1] + ' vs ' + data[2]
            keyboard.row(InlineKeyboardButton(text=data, callback_data=data))

    keyboard.row(InlineKeyboardButton(text='Back', callback_data='live_back'))
    return keyboard


async def i_k_match(id):
    print(await db_select('''SELECT FORMAT(CAST (date_time as date),'MM-dd') from [PapugaBot].[dbo].[match] where match_id = ?''', (id, )))
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    keyboard.row(InlineKeyboardButton(text='Back', callback_data=cb_back.new(id=id)))
    return keyboard

