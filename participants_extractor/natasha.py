from navec import Navec
from slovnet import NER
from pathlib import Path
import pymorphy2

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
