# import packages
import settings
import sys
import datetime as dt
import time
import urllib3
import json

# sqlalchemy: table만들때 쓰는 것들
import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
# sqlalchemy data넣을 때 쓰는것들
from sqlalchemy.orm import sessionmaker
Session = sessionmaker()


# ============================================
#      Connect DB and Making Table
# ============================================
# 환경설정
MATCH_URL = "http://score.sports.media.daum.net/planus/do/v2/api/sports_games.json?category=kbo&date="
CAST_URL = "http://data.cast.sports.media.daum.net/bs/kbo/"
http = urllib3.PoolManager()

# port 매번 바뀌기 때문에 도커창에서 docker ps -a 친후에, port 번호 확인하기
engine = sqlalchemy.create_engine(settings.DB_TYPE + settings.DB_USER + ":" + settings.DB_PASSWORD + "@" +
                                  settings.DB_URL + ":" + settings.DB_PORT + "/" + settings.DB_NAME, echo=settings.QUERY_ECHO)

# Making Table


class Livetext(Base):

    # table name
    __tablename__ = 'livetext'
    # table column
    id = Column(Integer, primary_key=True)
    dates = Column(DateTime)
    inning = Column(String)
    btop = Column(String)
    batorder = Column(String)
    batter = Column(String)
    pitcher = Column(String)
    text = Column(String)
    textstyle = Column(String)
    tcode = Column(String)


class Team(Base):
    # table name
    __tablename__ = 'team'
    # table column
    tcode = Column(String, primary_key=True)


class Team_Season(Base):
    # table name
    __tablename__ = 'team_season'
    # table column
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


class Player(Base):
    # table name
    __tablename__ = 'player'
    # table column
    player_id = Column(Integer, primary_key=True)
    tcode = Column(String, ForeignKey('team.tcode'))


class Player_Profile(Base):
    # table name
    __tablename__ = 'player_profile'
    # table column
    profile_id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('player.player_id'))
    dates = Column(DateTime)
    backnum = Column(Integer)
    bat = Column(String)
    height = Column(Integer)
    name = Column(String)
    position = Column(String)
    throw = Column(String)
    weight = Column(Integer)


class Pitcher_Stats(Base):
    # table name
    __tablename__ = 'pitcher_stats'
    # table column
    pitcher_id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('player_profile.profile_id'))
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
    # table name
    __tablename__ = 'batter_stats'
    # table column
    batter_id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('player_profile.profile_id'))
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

# ============================================
#  Start Crawling
# ============================================

# Interval control
interval = str(sys.argv)
interval = int(interval)
##########################
# functions
##########################


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
                if 'season' in cast_json['registry']['team'][j].keys():
                    team_list.append(j)

datalist = []
for i in range(len(team_list)):
    datalist.append(Team(tcode=team_list[i]))

    Session.configure(bind=engine)  # once engine is available
    session = Session()
    session.add_all(datalist)  # list로 한 번에 넣기
    session.commit()


