import os

from pymongo import MongoClient

client = MongoClient(os.getenv('MONGO_HOST'), 1002)
news_db = client["news"]["all_feed"]
fresh_news = client["news"]["fresh"]


def dump(news):
    news_db.insert_one(news)


def refresh_fresh_news():
    """Delete all unprocessed news"""
    fresh_news.delete_many({})


def was_processed(link:str) -> bool :
    num = news_db.find({'link': link})
    if len(list(num)) != 0:   # absolute garbage
        return True
    else:
        return False


def store_new(news) -> None :
    fresh_news.insert_one(news)

