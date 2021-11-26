from fastapi import FastAPI
from pydantic import BaseModel
import check_feed

app = FastAPI()


class Item(BaseModel):
    first: bool


@app.post("/rss_feed/check_feed/")
def get_news(item: Item):
    print(item.first)
    if item.first == True:
        res = check_feed.run(True)
    elif item.first == False:
        res = check_feed.run(False)
    else:
        res = check_feed.run(False)

    return {"payload": res}
