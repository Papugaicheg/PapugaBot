import datetime
import re
from dataBase import db_insert, db_select
from bs4 import BeautifulSoup
import requests
import time

ua = {
    '1':'Mozilla/5.0 (compatible; MSIE 10.0; Windows 98; Trident/5.1)',
    '2':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/5320 (KHTML, like Gecko) Chrome/39.0.840.0 Mobile Safari/5320',
    '3':'Mozilla/5.0 (Windows 95; en-US; rv:1.9.1.20) Gecko/20150928 Firefox/37.0',
    '4':'Mozilla/5.0 (Windows; U; Windows NT 5.01) AppleWebKit/531.31.2 (KHTML, like Gecko) Version/5.0 Safari/531.31.2'
}
def url_constructor(u):
    return 'https://www.hltv.org/' + u


async def db_parser():

    # await db_insert('''DELETE FROM [PapugaBot].[dbo].[match]''')
    # await db_insert('''DELETE FROM [PapugaBot].[dbo].[teams]''')

    url = 'https://www.hltv.org/matches'
    page = requests.get(url)

    soup = BeautifulSoup(page.text, "html.parser")

    matches = soup.find('div', class_='upcomingMatchesWrapper').findAll('a', class_='match a-reset')
    for item in matches:

        match_time = int(item.find('div', class_='matchTime').attrs['data-unix']) // 1000 + 10800
        date_time = time.strftime("%d-%m-%Y %H:%M:%S", time.gmtime(match_time))
        href = item.attrs['href'].replace('/matches', '')
        match_id = int(href.split('/')[1])
        print(len(await db_select('''SELECT * FROM [PapugaBot].[dbo].[match] WHERE match_id= ?''',(match_id,))))
        # print(f'count match= {await db_select("""Select Count(match_id) FROM [PapugaBot].[dbo].[match]""") }')
        # print(f'count teams= {await db_select("""Select Count(match_id) FROM [PapugaBot].[dbo].[teams]""")}')
        if len(await db_select('''SELECT * FROM [PapugaBot].[dbo].[teams] WHERE match_id= ?''',(match_id,)))==0:
            print(match_id)
            if (item.findAll('div', class_='matchTeamName text-ellipsis') or None) is None:
                item = item.find('span', class_='line-clamp-3')
                announce = item.text.strip()
                await db_insert('''INSERT INTO [PapugaBot].[dbo].[teams](match_id, announce, date_time) VALUES (?, ?, ?)''',
                          (match_id, announce, date_time,))
            else:
                meta = item.find('div', class_='matchMeta').text.strip()
                # print(meta)
                event = item.find("div", class_="matchEvent").text.strip()
                maps = str(await get_info(href)).replace('[', '').replace(']', '').replace("'", '')
                # print(date_time)
                if item.find_parent().has_attr('team1') and (item.find_parent().has_attr('team2')):
                    team_id = [int(item.find_parent().attrs['team1']), int(item.find_parent().attrs['team2'])]
                elif item.find_parent().has_attr('team1') and not item.find_parent().has_attr('team2'):
                    team_id = [int(item.find_parent().attrs['team1']), None]
                elif not item.find_parent().has_attr('team1') and int(item.find_parent().attrs['team2']):
                    team_id = [None, int(item.find_parent().attrs['team2'])]
                else:
                    team_id = [None, None]
                data = item.findAll('div', class_='team text-ellipsis') or None
                item = item.findAll('div', class_='matchTeamName text-ellipsis')
                team = [data.text.strip() for data in item]
                if len(team) == 1:
                    if data is not None:
                        for tt in data:
                            team.append(tt.text.strip())
                        await db_insert('''INSERT INTO [PapugaBot].[dbo].[teams] (match_id, team1, announce, team1_id, team2_id, date_time) 
                                    VALUES (?,?,?,?,?,? )''',
                                        (match_id, team[0], team[1], team_id[0], team_id[1], date_time,))
                else:
                    await db_insert('''INSERT INTO [PapugaBot].[dbo].[teams] (match_id, team1, team2, team1_id, team2_id, date_time) 
                                VALUES (?,?,?,?,?,? )''', (match_id, team[0], team[1], team_id[0], team_id[1], date_time,))



                await db_insert('''INSERT INTO [PapugaBot].[dbo].[match] (match_id, date_time,href, meta, event, maps)
                VALUES (?,?,?,?,?,?)''', (match_id, date_time, href, meta, event, maps,))


async def get_info(href):
    url = 'https://www.hltv.org/matches' + href
    print(url)
    page = requests.get(url, headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                                   'AppleWebKit/537.36 (KHTML, like Gecko) '
                                                   'Chrome/92.0.4515.159 '
                                                   'YaBrowser/21.8.2.381 '
                                                   'Yowser/2.5 Safari/537.36'})
    soup = BeautifulSoup(page.text, "html.parser")
    maps = soup.find('div', class_='flexbox-column').findAll('div', class_='mapname') or None

    return [item.text.strip() for item in maps]


async def get_date():
    url = url_constructor('matches')

    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    matches_urls = []
    matches_date = []
    unique_date = []
    c = 0
    matches = soup.find('div', class_='upcomingMatchesWrapper').findAll('a', class_='match a-reset')
    for item in matches:
        match_time = int(item.find('div', class_='matchTime').attrs['data-unix'])
        matches_urls.append([
            time.strftime("%m-%d", time.gmtime(match_time // 1000 + 10800)),
            match_time // 1000,
            item.attrs['href']
        ])
        # # match_id, team1, team2, date_time, maps, data_unix, href
        # db_insert('''INSERT INTO [PapugaBot].[dbo].[match] VALUES (?,?,?,?,?)''', )
        matches_date.append([time.strftime("%d-%m", time.gmtime(match_time // 1000 + 10800)),
                             time.strftime("%m-%d", time.gmtime(match_time // 1000 + 10800))])
    for i in range(len(matches_date) - 1):

        if matches_date[i][0] != matches_date[i + 1][0]:
            unique_date.append([matches_date[i][0], matches_date[i][1]])
            if i + 2 == len(matches_date):
                unique_date.append([matches_date[i + 1][0], matches_date[i + 1][1]])

    return unique_date, matches_urls


async def get_live_matches():
    url = url_constructor('matches')
    print(url)
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    live_matches_sorted = []
    if soup.find('div', class_='liveMatches') is not None:
        live_matches = soup.find('div', class_='liveMatches') \
            .findAll('div', class_='matchTeamName text-ellipsis')

        for data in live_matches:
            if data is not None:
                live_matches_sorted.append(data.text)
    return live_matches_sorted


async def get_match_from_date(date):
    checker = False
    matches_date = []
    matches_date_is_none = []
    matches_date_is_none_exit = []
    # date_match = time.strftime("%Y-%m-%d", time.gmtime(date))
    url = url_constructor('matches')
    page = requests.get(url)
    print(page.request.headers)
    soup = BeautifulSoup(page.text, "html.parser")
    # print(page.request.headers)
    matches_day = soup.find('span', text=re.compile(date)) \
                      .find_parent() \
                      .findAll('div', class_=re.compile("matchTeam team")) or None
    matches_date_is_none = soup.find('span', text=re.compile(date)) \
        .find_parent() \
        .findAll('span', class_='line-clamp-3')

    for item in matches_date_is_none:
        #     if item is not None:
        #         checker = True
        print(item)

    for item in matches_day:
        matches_date.append(item.text.strip())
    return matches_date, checker


async def get_match_info(date):
    date_list, matches_list = await get_date()

    matches_day = []
    matches_date = []
    c = 1
    for i in range(len(matches_list) - 1):
        if date == matches_list[i][1]:
            matches_day.append([matches_list[i][0], matches_list[i][1], matches_list[i][2]])
            url = url_constructor(matches_list[i][2])
            page = requests.get(url)
            soup = BeautifulSoup(page.text, "html.parser")
            teams = soup.findAll('div', class_='teamName')
            time_date = soup.find('div', class_='timeAndEvent').find_all('div', class_='time')

            for item in time_date:
                time_date_unix = int(item.attrs['data-unix'])
            # print(time_date)
            match_time_date = time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime(time_date_unix / 1000 + 10800))

            map = soup.find('div', class_='flexbox-column').findAll('div', class_='mapname')
            maps = ''
            for item in map:
                maps += item.text + ' '
            counter = 1
            for item in teams:
                if counter % 2 == 0:
                    matches_date.append([item_temp, item.text, match_time_date, maps])
                    c += 1
                    counter += 1
                else:
                    item_temp = item.text
                    counter += 1
        elif (date != matches_list[i][1]) and (matches_date is not None):
            break

    return matches_date


