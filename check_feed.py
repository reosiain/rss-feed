import datetime
import sys
from pathlib import Path
import time

sys.path.append(Path(__file__).parent.__str__())

from loguru import logger
from parsers import feed_functions as ff
from participants_extractor import natasha_parser as nt
from utils_news import io


def run(first) -> None:
    try:
        raw_list = ff.parse_latest()
    except Exception as er:
        logger.exception(er)
        logger.error(f"News text parsing error")
        return []

    clean = ff.clean_feed_list(raw_list)
    if first:
        logger.debug("Performing initial news dump..")
        logger.debug(f"Skipping {len(clean)} new articles.")
        for news in clean:
            news['TAG'] = 'Initial  dump'
            io.dump(news)
        return []

    for news in clean:
        if io.was_processed(news["link"]):
            continue

        try:
            text = ff.get_text_from_link(news["link"], news["source"])
        except Exception as err:
            #logger.exception(err)
            logger.error(news["link"])
            news['TAG'] = 'fetching error'
            io.dump(news)
            continue

        if text is None:
            news['TAG'] = 'no text'
            io.dump(news)
            continue

        try:
            if text != "":
                text_comps = nt.extract_companies(text)
            else:
                news['TAG'] = 'no text'
                io.dump(news)
                continue

        except Exception as er:
            logger.exception(er)
            logger.error("Error when extracting comps from text")

            news['TAG'] = 'unknown error'
            io.dump(news)
            continue

        tickers = []
        for comp_extracted in text_comps:
            comp_name = comp_extracted[0]
            tick = nt.get_ticker(comp_name)
            tickers.extend(tick)

        if len(tickers) == 0:
            news['TAG'] = 'no ticker'
            io.dump(news)
            continue

        news["text"] = text.replace("\n", "").replace("\r", "").replace('"', "")
        news["tickers"] = tickers
        news['TAG'] = 'ok'
        io.store_new(news)
        io.dump(news)


if __name__ == '__main__':
    first = True
    while True:
        io.refresh_fresh_news()
        logger.info(f'Cycle at {datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")}')
        run(first)
        first = False
        time.sleep(20)
