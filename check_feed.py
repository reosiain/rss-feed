from parsers import feed_functions as ff
from participants_extractor import natasha as nt
from utils import io
import time


def run():

    while True:
        print("___Checking___")
        raw_list = ff.parse_latest()
        clean = ff.clean_feed_list(raw_list)

        dump_list = []
        this_iteration_hashes = io.read_storage()
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
            print(news["title"])
            io.write_to_storage(news["link"])

            string = f'{news["title"]}*|*{str(news["time"])}*|*{news["link"]}*|*{news["source"]}*|*{news["hash"]}*|*{";".join(news["tickers"])}*|*{news["text"]}'
            io.dump_news(string)

        time.sleep(20)


if __name__ == "__main__":
    run()
