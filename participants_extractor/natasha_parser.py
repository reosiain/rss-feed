from pathlib import Path

import pymorphy2
import yaml
from navec import Navec
from slovnet import NER

with open(Path(__file__).parent.parent / "configs" / "moex_comps.yaml", "r") as f:
    companies = yaml.safe_load(f)["MOEX_companies"]

root = Path(__file__).parent
ner = NER.load(root / "slovnet_ner_news_v1.tar")
navec = Navec.load(root / "navec_news_v1_1B_250K_300d_100q.tar")
ner.navec(navec)
morph = pymorphy2.MorphAnalyzer(lang="ru")


def extract_companies(text) -> dict:
    markup = ner(text)
    results = list()
    intermed_unique = set()
    intermed = list()
    for span in markup.spans:
        if span.type != "ORG":
            continue
        txt = text[span.start : span.stop]
        normal = morph.parse(txt)[0].normal_form
        intermed.append(normal)
        intermed_unique.add(normal)
    aux = dict()
    count = len(intermed)
    if count == 0:
        return []
    for unique in intermed_unique:
        aux[unique] = round(intermed.count(unique) / count, 3)
    for key in aux:
        results.append((key, aux[key]))
    return results


def is_in_moex_list(comp_name: str) -> bool:
    """Compares text provided with public companies in the MOEX list"""
    for key in companies.keys():
        if comp_name.lower() in key.lower():
            return True
    return False


def get_ticker(comp_name: str) -> list:
    """Returns tickers if company is in the MOEX list"""
    tickers = []
    if comp_name.lower() == "банк":
        return []
    for key in companies.keys():
        if comp_name.lower() in key.lower():
            tickers.append(companies[key])
            if comp_name.lower() == key.lower():
                return [companies[key]]
    if len(tickers) > 1:
        return []
    else:
        return tickers
