from pathlib import Path

# import pymorphy2
import yaml
import numpy as np
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

with open(Path(__file__).parent.parent / "configs" / "company_conditions.yaml", "r") as f:
    moex_companies = yaml.safe_load(f)["MOEX_companies"]

root = Path(__file__).parent
emb = NewsEmbedding(root / "navec_news_v1_1B_250K_300d_100q.tar")
segmenter = Segmenter()
morph_vocab = MorphVocab()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)


def parse_text_spans(text):
    # assign doc
    doc = Doc(text)
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    doc.tag_ner(ner_tagger)
    return doc.spans


def levenshtein(s, t):
    """ levenshtein_ratio_and_distance:
        Calculates levenshtein distance between two strings.
        If ratio_calc = True, the function computes the
        levenshtein distance ratio of similarity between two strings
        For all i and j, distance[i,j] will contain the Levenshtein
        distance between the first i characters of s and the
        first j characters of t
    """
    # Initialize matrix of zeros
    rows = len(s)+1
    cols = len(t)+1
    distance = np.zeros((rows,cols),dtype = int)

    # Populate matrix of zeros with the indeces of each character of both strings
    for i in range(1, rows):
        for k in range(1,cols):
            distance[i][0] = i
            distance[0][k] = k

    # Iterate over the matrix to compute the cost of deletions,insertions and/or substitutions
    for col in range(1, cols):
        for row in range(1, rows):
            if s[row-1] == t[col-1]:
                cost = 0 # If the characters are the same in the two strings in a given position [i,j] then the cost is 0
            else:
                # In order to align the results with those of the Python Levenshtein package, if we choose to calculate the ratio
                # the cost of a substitution is 2. If we calculate just distance, then the cost of a substitution is 1.
                cost = 2

            distance[row][col] = min(distance[row-1][col] + 1,      # Cost of deletions
                                 distance[row][col-1] + 1,          # Cost of insertions
                                 distance[row-1][col-1] + cost)     # Cost of substitutions

    # Computation of the Levenshtein Distance Ratio
    Ratio = ((len(s)+len(t)) - distance[row][col]) / (len(s)+len(t))
    return Ratio


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

    return normalized_companies


def ticker_scores(comp:str):
    score_dict = {key:0 for key in moex_companies}
    for k in moex_companies:
        # Checking for any match with negative examples
        if moex_companies[k].get('negative') is not None:
            neg_scores = []
            for negative_example in moex_companies[k]['negative']:
                neg_scores.append(levenshtein(comp.lower(), negative_example.lower()))
            if max(neg_scores) > 0.9:
                score_dict[k] = 0
                continue
        # Regular check for matching patterns
        pos_scores = []
        for positive_example in moex_companies[k]['positive']:
            pos_scores.append(levenshtein(comp.lower(), positive_example.lower()))
        score_dict[k] = max(pos_scores)

    return score_dict


def extract_companies(text) -> dict:
    # list of original names of companies
    companies = []
    # list of normalized (lemmatized) names of companies
    norm_companies = []

    text = text.replace('\r\n', ' ')

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
    norm_companies = set(norm_companies)

    result = []
    for k in norm_companies:
        scores = ticker_scores(k)
        maxes = [k for k in scores if scores[k]>0.9]
        if len(maxes) != 1:
            continue
        result.append(maxes[0])
    return result