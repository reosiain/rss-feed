from parsers import feed_functions as ff


def run():

    raw_list = ff.parse_latest()
    clean = ff.clean_feed_list(raw_list)
