import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from crawling.database import Base, engine


class Livetext(Base):
    # table name 지정하기:
    __tablename__ = 'livetext'
    # table column 만들기:
    id = Column(Integer, primary_key=True)
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