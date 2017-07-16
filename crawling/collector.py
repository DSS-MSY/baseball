# -*- coding: utf-8 -*-
import sys
import datetime as dt
import time
import urllib3
import json

# ============================================
#  Start Crawling
# ============================================
# 환경설정
MATCH_URL = "http://score.sports.media.daum.net/planus/do/v2/api/sports_games.json?category=kbo&date="
CAST_URL = "http://data.cast.sports.media.daum.net/bs/kbo/"
http = urllib3.PoolManager()

# Interval control
interval = str(sys.argv)
interval = int(interval)
##########################
# functions
##########################

def asdfasdfasdf():
    return 0


def asdfasdfasdf():
    return 0


def asdfasdfasdf():
    return 0


def date_count(interval=1):
    date_list = []
    for i in range(interval):
        date = dt.datetime.now() - dt.timedelta(days=(i+1))
        date_list.append(date.strftime('%Y%m%d'))
    return date_list


def crawling(interval=1):
    """
    Main Function to start crawling. Generally, there are 5 games for each interval.
    If there is no input for interval, it will be 1. Just crawling for
    :param interval: how many days that you want to crawling. (default = 1)
    :return: returns are in your Database.
    """
    switch = True
    while switch:
        ##########################
        # get cast_json files
        ##########################
        # taking urls
        urls_list = []

        for i in range(interval):
            game_date = date_count(interval)[i]
            if dt.datetime.strptime(game_date, '%Y%m%d').weekday() == 0:  # SHUT DOWN CRAWLING FOR MONDAY
                switch = False  # if there is no cast_list means there are no games(monday), shut down the crawling
                print('Today is Monday! No Games on Monday.')
            else:
                urls_list.append(MATCH_URL + game_date)

        # get highlight_json file
        high_json_list = []
        for i in urls_list:
            high_json = http.request('GET', i)
            time.sleep(0.5)
            high_json_list.append(json.loads(high_json.data.decode('utf-8')))

        # get 'cp_game_id' from highlight_json_list
        cast_id_list = []
        for i in high_json_list:
            if i:  # equal to i !=[]
                for j in range(len(i)):
                    cast_id_list.append(i[j]['cp_game_id'])

        # get cast_urls_json from
        cast_json_list =[]
        for i in cast_id_list:
            cast_url = CAST_URL + i
            raw_cast_json = http.request('GET', cast_url)
            time.sleep(0.5)
            cast_json_list.append(json.loads(raw_cast_json.data.decode('utf-8')))

        ##########################
        # Inputting Data to Database
        ##########################


        for cast_json in cast_json_list:
            team_key_list = cast_json['registry']['team'].keys()
            team_list = []
            for j in team_key_list:
                if 'season' in cast_json['registry2']['team'][j].keys():
                    team_list.append(j)


        for cast_json in cast_json_list:





datalist = []
for i in range(len(team_list)):
    datalist.append(Team(tcode=team_list[i]))

    Session.configure(bind=engine)  # once engine is available
    session = Session()
    session.add_all(datalist)  # list로 한 번에 넣기
    session.commit()

tabacd = 0