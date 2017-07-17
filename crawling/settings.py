#config settings
class DevSettings():
    DB_TYPE = "postgresql://"
    DB_USER = "postgres"
    DB_PASSWORD = "1234"
    DB_URL = "192.168.99.100"
    DB_PORT = "32771"
    DB_NAME = "baseball"
    QUERY_ECHO = False

    MATCH_URL = 'http://score.sports.media.daum.net/planus/do/v2/api/sports_games.json?category=kbo&date='
    CAST_URL = "http://data.cast.sports.media.daum.net/bs/kbo/"