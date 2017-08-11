import urllib3
import json
from crawling.settings import DevSettings

http = urllib3.PoolManager()

# insert dates
if len(sys.argv) > 2:
    date1 = sys.argv[1]
    date2 = sys.argv[2]
    if date1 <= date2:
        date1 = int(date1)
        date2 = int(date2)
    else:
        print("ERROR: 2nd date must later than 1st date!")
elif len(sys.argv) == 2:
    date1 = sys.argv[1]
    date2 = dt.datetime.now()
    if dt.datetime.strptime(date1, "%Y%m%d") <= date2:
        date1 = int(date1)
        date2 = int(dt.datetime.strftime(date2, "%Y%m%d"))
    else:
        print("ERROR: 2nd date must later than 1st date!")
else:
    date1 = int(dt.datetime.strftime(dt.datetime.now() - dt.timedelta(days=1), "%Y%m%d"))
    date2 = int(dt.datetime.strftime(dt.datetime.now(), "%Y%m%d"))


def date_count(date1, date2):
    """
    date count function
    :param date1: int type, date1 must earlier than date2
    :param date2: int type, you have to input the day after that you want to calculate,
    if you put nothing in date2, it will automatically insert dt.datetime.now()

    ex) if date1 = 20170601, date2 = 20170630 return list is from June 1st to June 29th

    :return: a list of dates from date1 to date2, inverse sorted
    """

    date1 = dt.datetime.strptime(str(date1), '%Y%m%d')
    date2 = dt.datetime.strptime(str(date2), '%Y%m%d')
    delta = (date2 - date1).days
    date_list = []
    for i in range(delta):
        date = date2 - dt.timedelta(days=(i+1))
        date_list.append(date.strftime('%Y%m%d'))
    return date_list