import urllib3
import json
from .settings import DevSettings

http = urllib3.PoolManager()

def test():
    return 0