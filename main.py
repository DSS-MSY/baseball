from crawling.models import Livetext, Team, Team_Season, Player_Profile, Pitcher_Stats, Batter_Stats
from crawling.database import Base, session, engine


def init():
    engine
    Base.metadata.create_all(engine)

