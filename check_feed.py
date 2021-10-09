import sys
from pathlib import Path

sys.path.append(Path(__file__).parent.__str__())

from loguru import logger
from parsers import feed_functions as ff
from participants_extractor import natasha_parser as nt
from utils_news import io


def run(first):
    raw_list = ff.parse_latest()
    clean = ff.clean_feed_list(raw_list)

    dump_list = []
    this_iteration_hashes = io.read_storage()

    if first:
        logger.debug("Performing initial news dump..")
        logger.debug(f"Skipping {len(clean)} new articles.")
        for news in clean:
            io.write_to_storage(news["link"])
        return []

    for news in clean:
        if str(news["link"]) in this_iteration_hashes:
            io.write_to_storage(news["link"])
            continue

        text = ff.get_text_from_link(news["link"], news["source"])
        if text is None:
            io.write_to_storage(news["link"])
            continue

        if text != "":
            text_comps = nt.extract_companies(text)
        else:
            io.write_to_storage(news["link"])
            continue

        tickers = []
        for comp_extracted in text_comps:
            comp_name = comp_extracted[0]
            tick = nt.get_ticker(comp_name)
            tickers.extend(tick)

        if len(tickers) == 0:
            io.write_to_storage(news["link"])
            continue
        news["text"] = text.replace("\n", "").replace("\r", "")
        news["tickers"] = tickers
        dump_list.append(news)
        logger.debug(news["title"])
        io.write_to_storage(news["link"])

        string = f'{news["title"]}*|*{str(news["time"])}*|*{news["link"]}*|*{news["source"]}*|*{news["hash"]}*|*{";".join(news["tickers"])}*|*{news["text"]}'
        io.dump_news(string)

    return dump_list
