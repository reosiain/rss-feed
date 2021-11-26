from fastapi import FastAPI
from pydantic import BaseModel
import check_feed

app = FastAPI()


class Item(BaseModel):
    first: bool


@app.get("/rss_feed/check_feed/")
def model_predict(item: Item):
    res = check_feed.run(item.first)
    return {"payload": res}
