from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .settings import DevSettings

engine = create_engine(DevSettings.DB_TYPE + DevSettings.DB_USER + ":" + DevSettings.DB_PASSWORD + "@" +
                       DevSettings.DB_URL + ":" + DevSettings.DB_PORT + "/" + DevSettings.DB_NAME, echo=DevSettings.QUERY_ECHO)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()