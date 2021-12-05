import os

from pymongo import MongoClient

client = MongoClient(os.getenv('MONGO_HOST'), 1002)
news_db = client["news"]["all_feed"]
fresh_news = client["news"]["fresh"]


def dump(news):
    news_db.insert_one(news)


def was_processed(link:str) -> bool :
    num = news_db.find({'link': link})
    if num.count() != 0:
        False
    else:
        True


def store_new(news) -> None :
    fresh_news.insert_one(news)

