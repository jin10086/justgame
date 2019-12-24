import requests
import json

s = requests.Session()

from pymongo import MongoClient

from loguru import logger

logger.add(
    "transactions.log",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss} - {level} - {file} - {line} - {message}",
    rotation="10 MB",
)

db = MongoClient()["just"]["transactions"]


def getTransaction(url):
    print("getpage:", url)
    z1 = s.get(url)
    d = z1.json()
    if d["success"]:
        nextpage = d["meta"]["links"]["next"]
        data = d["data"]
        db.insert_many(data)
        return nextpage


if __name__ == "__main__":
    url = "https://api.trongrid.io/v1/accounts/TWjkoz18Y48SgWoxEeGG11ezCCzee8wo1A/transactions?only_confirmed=True&limit=50&search_internal=False&min_timestamp=0"
    while True:
        nextpage = getTransaction(url)
        if nextpage:
            url = nextpage
        else:
            break
