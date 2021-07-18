import feed_functions as ff

import yaml
from pathlib import Path

with open(Path(__file__).parent / "sources.yaml", "r") as f:
    sources = yaml.safe_load(f)

with open(Path(__file__).parent / "source_ids.yaml", "r") as f:
    codes = yaml.safe_load(f)["sources_rss"]


def run():

    raw_list = ff.parse_latest()
    clean = ff.clean_feed_list(raw_list)
