from fastapi import FastAPI
from pydantic import BaseModel
import check_feed
import requests
import json

app = FastAPI()


class Item(BaseModel):
    first: bool


@app.post("/rss_feed/check_feed")
def get_news(item: Item):

    if item.first:
        res = check_feed.run(True)
    elif not item.first:
        res = check_feed.run(False)
    else:
        res = check_feed.run(False)

    return {"list": res}


@app.get("/rss_feed/ping")
def ping():

    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    data = json.dumps({'text': "Сбербанк заработал рекордную прибыль"})
    a = requests.post("http://192.168.55.3:1001/sentiment/predict_one", data=data, headers=headers)

    return {"result": a.content}
