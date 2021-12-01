from pathlib import Path

# import pymorphy2
import yaml
# from navec import Navec
# from slovnet import NER
import re
from natasha import (
    Segmenter,
    MorphVocab,
    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,
    NamesExtractor,
    Doc
)

with open(Path(__file__).parent.parent / "configs" / "moex_comps.yaml", "r") as f:
    moex_companies = yaml.safe_load(f)["MOEX_companies"]

#root = Path(__file__).parent
# ner = NER.load(root / "slovnet_ner_news_v1.tar")
# navec = Navec.load(root / "navec_news_v1_1B_250K_300d_100q.tar")
# ner.navec(navec)
# morph = pymorphy2.MorphAnalyzer(lang="ru")
segmenter = Segmenter()
morph_vocab = MorphVocab()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)

names_extractor = NamesExtractor(morph_vocab)

def parse_text_spans(text):
    # assign doc
    doc = Doc(text)
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    doc.tag_ner(ner_tagger)
    return doc.spans


def true_normalize_companies(companies: list) -> list:
    remove_words = ['оао', 'ооо', 'зао', 'ок', 'ик', 'гмк', 'нк']
    not_companies = ['фтс', 'сми', 'росстат', 'минфин', 'фас']

    # remove symbols and odd words from the company name
    normalized_companies = []
    for norm_company in companies:
        true_norm_company = norm_company.lower()
        
        # replace all digits and characters (except "-" and ".")
        # replace all words from remove_words if not surrounded by letters
        for word in remove_words:            
            regex = f'[^A-Za-zА-Яа-я\s]+|[^A-Za-zА-Яа-я]{word}[^A-Za-zА-Яа-я]|^{word}[^A-Za-zА-Яа-я]'
            true_norm_company = re.sub(regex, '', true_norm_company).strip()
        
        normalized_companies.append(true_norm_company)
        
    result = []
    # 1. replacing long names of companies with shorter ones(e.g. 'сбербанк россии' -> 'сбербанк')
    # 2. if company name straight in moex_companies list - replace the original by one from moex
    # 3. save only if not in not_companies list
    for i, company in enumerate(normalized_companies):
        for j, another_company in enumerate(normalized_companies):
            if i == j:
                continue
            if another_company in company:
                company = another_company
                
        for moex_company in moex_companies:
            if moex_company.lower() in company:
                company = moex_company.lower()
                break
        
        if company not in not_companies:
            result.append(company)

    return result


def extract_companies(text) -> dict:
    # list of original names of companies
    companies = []
    # list of normalized (lemmatized) names of companies
    norm_companies = []
        
    for span in parse_text_spans(text):
        if span.type != "ORG":
            continue
        span.normalize(morph_vocab)
        companies.append(span.text)
        norm_companies.append(span.normal)
        
    count = len(companies)
    if count == 0:
        return []
    
    # normalize companies even more
    norm_companies = true_normalize_companies(norm_companies)
    
    # create a dict like it was before
    aux = dict()
    results = []
    for unique in set(norm_companies):
        aux[unique] = round(norm_companies.count(unique) / count, 3)
    for key in aux:
        results.append((key, aux[key]))
        
    return results


def get_ticker(comp_name: str) -> list:
    """Returns ticker if company is in the MOEX list"""
    if comp_name == "банк":
        return []
    for moex_company, moex_ticker in moex_companies.items():
        # get normalized moex company name - remove all symbols and lower it
        normalized_moex_company = re.sub('[^A-Za-zА-Яа-я\s]', '', moex_company).lower()
        if comp_name == normalized_moex_company:
            return [moex_ticker]
    return []
