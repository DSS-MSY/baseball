# -*- coding: utf-8 -*-

import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base

# sqlalchemy: table만들때 쓰는 것들
from crawling import settings

Base = declarative_base()
# sqlalchemy data넣을 때 쓰는것들
from sqlalchemy.orm import sessionmaker
Session = sessionmaker()



# ============================================
#      Connect DB and Making Table
# ============================================


# port 매번 바뀌기 때문에 도커창에서 docker ps -a 친후에, port 번호 확인하기
engine = sqlalchemy.create_engine(settings.DB_TYPE + settings.DB_USER + ":" + settings.DB_PASSWORD + "@" +
                                  settings.DB_URL + ":" + settings.DB_PORT + "/" + settings.DB_NAME, echo=settings.QUERY_ECHO)

# Making Table


class Livetext(Base):
    # table name 지정하기:
    __tablename__ = 'livetext'
    # table column 만들기:
    home = Column(String)
    away = Column(String)
    dates = Column(DateTime)
    inning = Column(String)
    btop = Column(String)
    batorder = Column(String)
    batter = Column(String)
    pitcher = Column(String)
    text = Column(String)
    textstyle = Column(String)

class Team(Base):
    # table name
    __tablename__ = 'team'
    # table column
    tcode = Column(String, primary_key=True)


class Team_Season(Base):
    # table name
    __tablename__ = 'team_season'
    # table column: 25
    idx = Column(Integer, primary_key=True)
    tcode = Column(String, ForeignKey('team.tcode'))
    dates = Column(DateTime)
    ab = Column(Float)
    bb = Column(Float)
    bra = Column(Float)
    dra = Column(Float)
    er = Column(Float)
    era = Column(Float)
    err = Column(Float)
    game = Column(Float)
    h2 = Column(Float)
    h3 = Column(Float)
    hit = Column(Float)
    hp = Column(Float)
    hr = Column(Float)
    hra = Column(Float)
    lose = Column(Float)
    lra = Column(Float)
    r = Column(Float)
    rank = Column(Float)
    run = Column(Float)
    same = Column(Float)
    sb = Column(Float)
    sf = Column(Float)
    win = Column(Float)
    wra = Column(Float)
    f_name = Column(String)
    region = Column(String)
    stadium = Column(String)


class Player_Profile(Base):
    # table name:
    __tablename__ = 'player_profile'
    # table column:
    profile_id = Column(Integer, primary_key=True)
    player_id = Column(Integer)
    dates = Column(DateTime)
    backnum = Column(Integer)
    bat = Column(String)
    height = Column(Integer)
    name = Column(String)
    position = Column(String)
    throw = Column(String)
    weight = Column(Integer)
    tcode = Column(String, ForeignKey('team.tcode'))


class Pitcher_Stats(Base):
    # table name:
    __tablename__ = 'pitcher_stats'
    # table column:
    pitcher_id = Column(Integer, primary_key=True)
    dates = Column(DateTime)
    player_id = Column(Integer)
    s_era = Column(Float)
    s_gyear = Column(Float)
    s_hit = Column(Float)
    s_hld = Column(Float)
    s_hr = Column(Float)
    s_kk = Column(Float)
    s_lose = Column(Float)
    s_save = Column(Float)
    s_total_era = Column(Float)
    s_win = Column(Float)
    t_b = Column(Float)
    t_bb = Column(Float)
    t_er = Column(Float)
    t_era = Column(Float)
    t_hbp = Column(Float)
    t_hit = Column(Float)
    t_hr = Column(Float)
    t_ip = Column(Float)
    t_np = Column(Float)
    t_r = Column(Float)
    t_s = Column(Float)
    t_so = Column(Float)


class Batter_Stats(Base):
    # table name:
    __tablename__ = 'batter_stats'
    # table column:
    batter_id = Column(Integer, primary_key=True)
    dates = Column(DateTime)
    player_id = Column(Integer)
    h_1 = Column(Float)
    h_2 = Column(Float)
    h_3 = Column(Float)
    h_4 = Column(Float)
    h_5 = Column(Float)
    h_6 = Column(Float)
    h_7 = Column(Float)
    h_8 = Column(Float)
    h_9 = Column(Float)
    h_10 = Column(Float)
    h_11 = Column(Float)
    h_12 = Column(Float)
    h_13 = Column(Float)
    s_ab = Column(Float)
    s_avg = Column(Float)
    s_bbhp = Column(Float)
    s_cs = Column(Float)
    s_game = Column(Float)
    s_h2 = Column(Float)
    s_h3 = Column(Float)
    s_hit = Column(Float)
    s_hr = Column(Float)
    s_kk = Column(Float)
    s_rbi = Column(Float)
    s_run = Column(Float)
    s_sb = Column(Float)
    s_shf = Column(Float)
    t_ab = Column(Float)
    t_avg = Column(Float)
    t_bb = Column(Float)
    t_bbhp = Column(Float)
    t_h = Column(Float)
    t_hr = Column(Float)
    t_pa = Column(Float)
    t_r = Column(Float)
    t_rbi = Column(Float)
    t_sb = Column(Float)
    t_so = Column(Float)


# Make table command
Base.metadata.create_all(engine)



import sys
import datetime as dt
import time
import urllib3
import json
import pandas as pd
# ============================================
#  Start Crawling
# ============================================
# 환경설정
MATCH_URL = "http://score.sports.media.daum.net/planus/do/v2/api/sports_games.json?category=kbo&date="
CAST_URL = "http://data.cast.sports.media.daum.net/bs/kbo/"
http = urllib3.PoolManager()

# Interval control
#interval = str(sys.argv)
#interval = int(interval)
##########################
# functions
##########################
interval = 10

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
    :param interval:
        how many days that you want to crawling. (default = 1)
    :return:
        returns are in your Database.
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
            urls_list.append(MATCH_URL + game_date)

        # get highlight_json file
        high_json_list = []
        for i in urls_list:
            high_json = http.request('GET', i)
            time.sleep(1)
            high_json_list.append(json.loads(high_json.data.decode('utf-8')))

        # get 'cp_game_id' from highlight_json_list
        cast_id_list = []
        for i in high_json_list:
            if i:  # equal to i !=[]
                for j in range(len(i)):
                    if i[j]['status'] != 'CANCEL':
                        cast_id_list.append(i[j]['cp_game_id'])

        # get cast_urls_json from
        cast_json_list =[]
        for i in cast_id_list:
            cast_url = CAST_URL + i
            raw_cast_json = http.request('GET', cast_url)
            time.sleep(1)
            cast_json_list.append(json.loads(raw_cast_json.data.decode('utf-8')))

        # get unique list
        array = pd.DataFrame(cast_id_list, columns=['cast_id'])
        array['date'] = array.cast_id.str[:8]
        array['idx'] = ~array.date.duplicated(keep='first')
        cast_id_list_unique = array.cast_id[array.idx].tolist()
        cast_json_list_unique = []
        for i in cast_id_list_unique:
            for j in cast_json_list:
                if i == j['game_code']:
                    cast_json_list_unique.append(j)
        switch = False

    return cast_id_list, cast_json_list, cast_id_list_unique, cast_json_list_unique

# get cast_id & files
cast_id_list, cast_json_list, cast_id_list_unique, cast_json_list_unique = crawling(interval)

##########################
# Inputting Data to Database
##########################

# team table
team_key_list = cast_json_list[0]['registry']['team'].keys()
team_list = []
for j in team_key_list:
    if 'season' in cast_json_list[0]['registry']['team'][j].keys():
        team_list.append(j)

datalist = []
for i in team_list:
    datalist.append(Team(tcode=i))

# team_season table
# datalist = []
for cast_json in cast_json_list_unique:
    for i in team_list:
        f_name_ = cast_json['registry']['team'][i]['profile']['teamname1'] + ' ' + cast_json['registry']['team'][i]['profile']['teamname2'] if i != 'KT' else cast_json['registry']['team'][i]['profile']['teamname1'] + ' ' + 'wiz'
        region_ = cast_json['registry']['team'][i]['profile']['region'] if i != 'KT' else '수원시'
        stadium_ = cast_json['registry']['team'][i]['profile']['stadium']  if i != 'KT' else '수원야구장 (경기도 수원시 장안구 경수대로 839)'
        datalist.append(Team_Season(
            dates=dt.datetime.strptime(cast_json['game_code'][:8], '%Y%m%d'),
            tcode=cast_json['registry']['team'][i]['season']['team_cd'],
            ab=cast_json['registry']['team'][i]['season']['ab'],
            bb=cast_json['registry']['team'][i]['season']['bb'],
            bra=cast_json['registry']['team'][i]['season']['bra'],
            dra=cast_json['registry']['team'][i]['season']['dra'],
            er=cast_json['registry']['team'][i]['season']['er'],
            era=cast_json['registry']['team'][i]['season']['era'],
            err=cast_json['registry']['team'][i]['season']['err'],
            game=cast_json['registry']['team'][i]['season']['game'],
            h2=cast_json['registry']['team'][i]['season']['h2'],
            h3=cast_json['registry']['team'][i]['season']['h3'],
            hit=cast_json['registry']['team'][i]['season']['hit'],
            hp=cast_json['registry']['team'][i]['season']['hp'],
            hr=cast_json['registry']['team'][i]['season']['hr'],
            hra=cast_json['registry']['team'][i]['season']['hra'],
            lose=cast_json['registry']['team'][i]['season']['lose'],
            lra=cast_json['registry']['team'][i]['season']['lra'],
            r=cast_json['registry']['team'][i]['season']['r'],
            rank=cast_json['registry']['team'][i]['season']['rank'],
            run=cast_json['registry']['team'][i]['season']['run'],
            same=cast_json['registry']['team'][i]['season']['same'],
            sb=cast_json['registry']['team'][i]['season']['sb'],
            sf=cast_json['registry']['team'][i]['season']['sf'],
            win=cast_json['registry']['team'][i]['season']['win'],
            wra=cast_json['registry']['team'][i]['season']['wra'],
            f_name=f_name_,
            region=region_,
            stadium=stadium_,
            ))

# player_profile table
# datalist = []
for cast_json in cast_json_list_unique:
    for j in list(cast_json['registry']['player'].keys()):
        datalist.append(Player_Profile(
            player_id = int(j),
            dates = dt.datetime.strptime(cast_json['game_code'][:8], '%Y%m%d'),
            backnum = cast_json['registry']['player'][j]['profile']['backnum'],
            bat = cast_json['registry']['player'][j]['profile']['bat'],
            height = cast_json['registry']['player'][j]['profile']['height'],
            name = cast_json['registry']['player'][j]['profile']['name'],
            position = cast_json['registry']['player'][j]['profile']['position'],
            throw = cast_json['registry']['player'][j]['profile']['throw'],
            weight = cast_json['registry']['player'][j]['profile']['weight'],
            tcode = cast_json['registry']['player'][j]['profile']['tcode'],
            ))

# batter_stats table
# datalist = []
for cast_json in cast_json_list:
    for j in list(cast_json['registry']['player'].keys()):
        if (len(cast_json['registry']['player'][j].keys()) >= 2) & ('batter' in cast_json['registry']['player'][j].keys()):
            # 그날 그팀 명단 중 batter인 사람
            if len(cast_json['registry']['player'][j]['batter'].keys()) == 3:
                # 출전한 사람
                datalist.append(Batter_Stats(
                    player_id = int(j),
                    dates = dt.datetime.strptime(cast_json['game_code'][:8], '%Y%m%d'),
                    h_1=cast_json['registry']['player'][j]['batter']['hotzone']['1'],
                    h_2=cast_json['registry']['player'][j]['batter']['hotzone']['2'],
                    h_3=cast_json['registry']['player'][j]['batter']['hotzone']['3'],
                    h_4=cast_json['registry']['player'][j]['batter']['hotzone']['4'],
                    h_5=cast_json['registry']['player'][j]['batter']['hotzone']['5'],
                    h_6=cast_json['registry']['player'][j]['batter']['hotzone']['6'],
                    h_7=cast_json['registry']['player'][j]['batter']['hotzone']['7'],
                    h_8=cast_json['registry']['player'][j]['batter']['hotzone']['8'],
                    h_9=cast_json['registry']['player'][j]['batter']['hotzone']['9'],
                    h_10=cast_json['registry']['player'][j]['batter']['hotzone']['10'],
                    h_11=cast_json['registry']['player'][j]['batter']['hotzone']['11'],
                    h_12=cast_json['registry']['player'][j]['batter']['hotzone']['12'],
                    h_13=cast_json['registry']['player'][j]['batter']['hotzone']['13'],
                    s_ab=cast_json['registry']['player'][j]['batter']['season']['ab'],
                    s_avg=cast_json['registry']['player'][j]['batter']['season']['avg'],
                    s_bbhp=cast_json['registry']['player'][j]['batter']['season']['bbhp'],
                    s_cs=cast_json['registry']['player'][j]['batter']['season']['cs'],
                    s_game=cast_json['registry']['player'][j]['batter']['season']['game'],
                    s_h2=cast_json['registry']['player'][j]['batter']['season']['h2'],
                    s_h3=cast_json['registry']['player'][j]['batter']['season']['h3'],
                    s_hit=cast_json['registry']['player'][j]['batter']['season']['hit'],
                    s_hr=cast_json['registry']['player'][j]['batter']['season']['hr'],
                    s_kk=cast_json['registry']['player'][j]['batter']['season']['kk'],
                    s_rbi=cast_json['registry']['player'][j]['batter']['season']['rbi'],
                    s_run=cast_json['registry']['player'][j]['batter']['season']['run'],
                    s_sb=cast_json['registry']['player'][j]['batter']['season']['sb'],
                    s_shf=cast_json['registry']['player'][j]['batter']['season']['shf'],
                    t_ab=cast_json['registry']['player'][j]['batter']['today']['ab'],
                    t_avg=cast_json['registry']['player'][j]['batter']['today']['avg'],
                    t_bb=cast_json['registry']['player'][j]['batter']['today']['bb'],
                    t_bbhp=cast_json['registry']['player'][j]['batter']['today']['bbhp'],
                    t_h=cast_json['registry']['player'][j]['batter']['today']['h'],
                    t_hr=cast_json['registry']['player'][j]['batter']['today']['hr'],
                    t_pa=cast_json['registry']['player'][j]['batter']['today']['pa'],
                    t_r=cast_json['registry']['player'][j]['batter']['today']['r'],
                    t_rbi=cast_json['registry']['player'][j]['batter']['today']['rbi'],
                    t_sb=cast_json['registry']['player'][j]['batter']['today']['sb'],
                    t_so=cast_json['registry']['player'][j]['batter']['today']['so'],
                ))

# pitcher stats table
# datalist = []
for cast_json in cast_json_list:
    for j in list(cast_json['registry']['player'].keys()):
        if (len(cast_json['registry']['player'][j].keys()) >= 2) & ('pitcher' in cast_json['registry']['player'][j].keys()):
            # 그날 그팀 명단 중 pitcher인 사람
            datalist.append(Pitcher_Stats(
                player_id=int(j),
                dates=dt.datetime.strptime(cast_json['game_code'][:8], '%Y%m%d'),
                s_era=cast_json['registry']['player'][j]['pitcher']['season']['era'],
                s_gyear=cast_json['registry']['player'][j]['pitcher']['season']['gyear'],
                s_hit=cast_json['registry']['player'][j]['pitcher']['season']['hit'],
                s_hld=cast_json['registry']['player'][j]['pitcher']['season']['hld'],
                s_hr=cast_json['registry']['player'][j]['pitcher']['season']['hr'],
                s_kk=cast_json['registry']['player'][j]['pitcher']['season']['kk'],
                s_lose=cast_json['registry']['player'][j]['pitcher']['season']['lose'],
                s_save=cast_json['registry']['player'][j]['pitcher']['season']['save'],
                s_total_era=cast_json['registry']['player'][j]['pitcher']['season']['total_era'],
                s_win=cast_json['registry']['player'][j]['pitcher']['season']['win'],
                t_b=cast_json['registry']['player'][j]['pitcher']['today']['b'],
                t_bb=cast_json['registry']['player'][j]['pitcher']['today']['bb'],
                t_er=cast_json['registry']['player'][j]['pitcher']['today']['er'],
                t_era=cast_json['registry']['player'][j]['pitcher']['today']['era'],
                t_hbp=cast_json['registry']['player'][j]['pitcher']['today']['hbp'],
                t_hit=cast_json['registry']['player'][j]['pitcher']['today']['hit'],
                t_hr=cast_json['registry']['player'][j]['pitcher']['today']['hr'],
                t_ip=cast_json['registry']['player'][j]['pitcher']['today']['ip'],
                t_np=cast_json['registry']['player'][j]['pitcher']['today']['np'],
                t_r=cast_json['registry']['player'][j]['pitcher']['today']['r'],
                t_s=cast_json['registry']['player'][j]['pitcher']['today']['s'],
                t_so=cast_json['registry']['player'][j]['pitcher']['today']['so'],
            ))


# livetext table
# datalist = []
for cast_json in cast_json_list:
    home_ = cast_json['game_code'][8:10]
    away_ = cast_json['game_code'][10:12]
    dates_ = dt.datetime.strptime(cast_json['game_code'][:8], '%Y%m%d'),
    livetext_ = cast_json['livetext']
    for i in livetext_:
        datalist.append(Livetext(
            home=home_,
            away=away_,
            dates=dates_,
            inning=i['inning'],
            btop=i['btop'],
            batorder=i['batorder'],
            batter=i['batter'],
            pitcher=i['pitcher'],
            text=i['text'],
            textstyle=i['textstyle'],
            ))

Session.configure(bind=engine)  # once engine is available
session = Session()
session.add_all(datalist)  # list로 한 번에 넣기
session.commit()