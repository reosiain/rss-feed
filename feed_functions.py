import datetime

import yaml
import feedparser
from pathlib import Path
from constants import *

with open(Path(__file__).parent / "sources.yaml", "r") as f:
    sources = yaml.safe_load(f)

with open(Path(__file__).parent / "source_ids.yaml", "r") as f:
    codes = yaml.safe_load(f)["sources_rss"]


def parse_latest() -> dict():
    """Gets latest news from rss feed"""
    dict_ = {}
    for source in sources["sources_rss"]:
        if source in {"vedomosti", "guru_trade"}:
            continue
        link = sources["sources_rss"][source]
        a = feedparser.parse(link)
        dict_[codes[source]] = a["entries"]
    return dict_


def clean_feed_list(parsed_feed: list) -> list:
    """Cleaner feed version with important parameters"""
    list_ = []
    for key in parsed_feed.keys():
        this_key = parsed_feed[key]
        for elem in this_key:
            element_dict = dict()
            element_dict["title"] = elem["title"]
            if elem["published_parsed"] is not None:
                year = elem["published_parsed"].tm_year
                month = elem["published_parsed"].tm_mon
                day = elem["published_parsed"].tm_mday
                hour = elem["published_parsed"].tm_hour
                minute = elem["published_parsed"].tm_min
                sec = elem["published_parsed"].tm_sec
                element_dict["time"] = datetime.datetime(
                    year, month, day, hour, minute, sec
                )
            else:
                element_dict["time"] = elem["published"]
            element_dict["link"] = elem["link"]
            element_dict["source"] = key
            element_dict["hash"] = hash(
                (element_dict["title"], element_dict["link"], element_dict["source"])
            )
            list_.append(element_dict)
    return list_


def get_text_from_link(link: str, source: str) -> str:
    """Returns text of the news by requesting html page of the news.
    Also resolves, which parser should be used based upon the source of the url.

    Arguments:
        link - url to the news
        source - code of the source format: xxxxx00

    Returns:
        text of the article"""
    fnc = function_router[source]
    if fnc is None:
        return None
    text = fnc(link)
    return text
