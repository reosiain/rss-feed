from fastapi import FastAPI, Request
from pydantic import BaseModel
import check_feed
import requests
import threading
import json
import logging
from utils_news import io


app = FastAPI()

logging.basicConfig(level=logging.INFO)
name_logger = logging.getLogger(__name__)
name_logger.setLevel(logging.INFO)


class Item(BaseModel):
    first: bool


@app.on_event("startup")
def run():
    trd = threading.Thread(target=check_feed.launch_module)
    trd.start()


# Possibly not used
# @app.post("/rss_feed/check_feed")
# def get_news(item: Item):
#
#     if item.first:
#         res = check_feed.run(True)
#     elif not item.first:
#         res = check_feed.run(False)
#     else:
#         res = check_feed.run(False)
#     return {"list": res}
#

@app.get("/rss_feed/ping")
def ping():
    return {"result": {}}


@app.post("/rss_feed/import_quik")
async def import_quik(news: Request):
    _ = await news.json()
    news = json.loads(_)
    io.store_new(news)
    io.dump(news)
    logging.info(news)



