from pathlib import Path
import sys

sys.path.append(Path(__file__).parent.parent.__str__())

from parsers import feed_functions as ff
import check_feed
from utils_news import io


def test_text_grabber():

    raw_list = ff.parse_latest()
    clean = ff.clean_feed_list(raw_list)
    text = ff.get_text_from_link(clean[120]["link"], clean[120]["source"])
    print(text)
    if clean[120]["source"] == "finam01":
        assert text is None
    else:
        assert text is not None


def test_io():

    init_count = io.news_db.find().count()

    check_feed.run(True)

    assert io.news_db.find().count() > init_count

