# from pathlib import Path
#
# import numpy as np
# import pandas as pd
# import pymorphy2
# import yaml
# from navec import Navec
# from razdel import sentenize, tokenize
# from slovnet import NER, Syntax
#
# from rss_feed.participants_extractor import natasha_parser as nt
#
# with open(Path(__file__).parent.parent / "configs" / "moex_comps.yaml", "r") as f:
#     companies = yaml.safe_load(f)["MOEX_companies"]
#
# root = Path(__file__).parent
# ner = NER.load(root / "slovnet_ner_news_v1.tar")
# navec = Navec.load(root / "navec_news_v1_1B_250K_300d_100q.tar")
# syntax = Syntax.load(root / "slovnet_syntax_news_v1.tar")
# syntax.navec(navec)
# ner.navec(navec)
# morph = pymorphy2.MorphAnalyzer(lang="ru")
#
#
# def relevancy_coefficient(text):
#     paragraphs = text.split("|@|")
#
#     chunk = []
#     orgs_in_sent = {}  # extracted names
#     sent_num = 1
#     for par in paragraphs:
#         for sent in sentenize(par):
#             if sent.text == "":
#                 continue
#             orgs_in_sent[sent_num] = nt.extract_companies(sent.text)
#             tokens = [_.text for _ in tokenize(sent.text)]
#             chunk.append(tokens)
#             sent_num += 1
#
#     markup = list(syntax.map(chunk))
#
#     token_dict = {}
#     name_targets = {}
#     structure = {}
#     sent_num = 1
#
#     for sent in markup:
#         structure[sent_num] = {}
#         for token in sent.tokens:
#             normal = morph.parse(token.text)[0].normal_form
#
#             structure[sent_num][int(token.id)] = int(token.head_id)
#
#             if sent_num not in token_dict.keys():
#                 token_dict[sent_num] = {normal: int(token.id)}  # words in sentence
#             else:
#                 token_dict[sent_num][normal] = int(token.id)  # words to locations
#
#             if normal not in name_targets.keys():
#                 name_targets[(sent_num, int(token.id))] = [int(token.head_id)]
#             else:
#                 name_targets[(sent_num, int(token.id))].append(int(token.head_id))
#
#         sent_num += 1
#
#     clean_ner_dict = {}
#     for sent_num in orgs_in_sent.keys():
#         for org in orgs_in_sent[sent_num]:
#             entity_name = org[0]
#             if entity_name not in clean_ner_dict.keys():
#                 clean_ner_dict[entity_name] = []
#             for word in token_dict[sent_num]:
#                 if word in entity_name:
#                     clean_ner_dict[entity_name].append(
#                         (sent_num, token_dict[sent_num][word])
#                     )
#
#     # for coef 3
#     ORG_deps = {}
#     for ORG in clean_ner_dict:
#         ORG_deps[ORG] = {"to": set(), "from": set()}
#         for loc in clean_ner_dict[ORG]:
#             # here we look up dependencies for all related tokens
#             sentence_num = loc[0]
#             token_id = loc[1]
#
#             sentence = structure[sentence_num]
#             sentence_reverse = {lead: [] for lead in sentence.values()}
#             for follow in sentence:
#                 lead = sentence[follow]
#                 sentence_reverse[lead].append(follow)
#
#             look_up_token = token_id
#             for times in range(len(sentence)):
#                 try:
#                     new_look_up = sentence[look_up_token]
#                     ORG_deps[ORG]["from"].add((sentence_num, new_look_up))
#                     look_up_token = new_look_up
#                 except KeyError:
#                     continue
#
#             try:
#                 for follow in sentence_reverse[token_id]:
#                     ORG_deps[ORG]["to"].add((sentence_num, follow))
#             except KeyError:
#                 continue
#             for times in range(len(sentence.keys())):
#                 for follow in ORG_deps[ORG]["to"]:
#                     if follow not in sentence_reverse.keys():
#                         continue
#                     loc = (sentence_num, sentence_reverse[follow])
#                     if loc not in ORG_deps[ORG]["to"]:
#                         ORG_deps[ORG]["to"].append(loc)
#
#     # for coef 2
#     coef2_dict = {}
#     for ORG in clean_ner_dict:
#         coef2_dict[ORG] = set()
#         for pos in clean_ner_dict[ORG]:
#             coef2_dict[ORG].add(pos[0])
#     coef2_dict = {x: len(coef2_dict[x]) for x in coef2_dict}
#
#     # for coef 1
#     org_org_dict = {}
#     for ORG in ORG_deps:
#
#         org_org_dict[ORG] = {"from": 0, "to": 0}
#
#         for to in ORG_deps[ORG]["to"]:
#             for ORG_2 in ORG_deps:
#                 if ORG_2 == ORG:
#                     continue
#                 if to in ORG_deps[ORG_2]["from"]:
#                     org_org_dict[ORG]["to"] += 1
#
#         for from_ in ORG_deps[ORG]["from"]:
#             for ORG_2 in ORG_deps:
#                 if ORG_2 == ORG:
#                     continue
#                 if from_ in ORG_deps[ORG_2]["to"]:
#                     org_org_dict[ORG]["from"] += 1
#
#     # ___________ Calculating coefficients
#     total_tokens = 0
#     coefficients = {}
#     for key in token_dict:
#         total_tokens += len(token_dict[key])
#
#     total_org_orgs = 1
#     for key in org_org_dict:
#         total_org_orgs += org_org_dict[key]["to"]
#         total_org_orgs += org_org_dict[key]["from"]
#
#     for ORG in ORG_deps:
#         ticker = nt.get_ticker(ORG)
#         if len(ticker) == 0:
#             continue
#         else:
#             ticker = ticker[0]
#             coefficients[ticker] = {
#                 "ORG_ORG": {"to": 0, "from": 0},
#                 "ORG_count": 0,
#                 "ORG_cover": 0,
#             }
#
#         coefficients[ticker]["ORG_ORG"]["to"] = org_org_dict[ORG]["to"]
#         coefficients[ticker]["ORG_ORG"]["from"] = org_org_dict[ORG]["from"]
#         coefficients[ticker]["ORG_count"] = coef2_dict[ORG]
#         coefficients[ticker]["ORG_cover"] = (
#             len(ORG_deps[ORG]["to"]) + len(ORG_deps[ORG]["from"])
#         ) / total_tokens
#
#     coef_list = {}
#     for ticker in coefficients:
#         coef_1 = (
#             coefficients[ticker]["ORG_ORG"]["from"]
#             + coefficients[ticker]["ORG_ORG"]["to"]
#         ) / total_org_orgs
#         coef_2 = coefficients[ticker]["ORG_count"] / len(markup)
#         coef_3 = coefficients[ticker]["ORG_count"] / sum(coef2_dict.values())
#         coef_4 = np.minimum(coefficients[ticker]["ORG_cover"] * np.log(len(text)), 1)
#
#         val = coef_1 * (1 / 6) + coef_2 * (1 / 6) + coef_3 * (3 / 6) + coef_4 * (1 / 6)
#         coef_list[ticker] = [coef_1, coef_2, coef_3, coef_4]
#
#     return coef_list
#
#
# if __name__ == "__main__":
#
#     import json
#     import os
#
#     path = "/home/stbarkhatov/billy_trades"
#     trades = os.listdir(path)
#
#     dict_ = {
#         "text": [],
#         "return": [],
#         "coef1": [],
#         "coef2": [],
#         "coef3": [],
#         "coef4": [],
#         "ticker": [],
#         "found_ticker": [],
#     }
#     for trd in trades:
#         if "json" not in trd:
#             continue
#
#         with open(path + "/" + trd, "rb") as f:
#             _ = json.load(f)
#
#         text = _["TEXT"]
#         ret = _["CALCULATED_RETURN"]
#         ticker = _["TICKER"]
#         val = relevancy_coefficient(text)
#         if len(val) != 1:
#             continue
#         relev_ticker = list(val.keys())[0]
#         val = val[relev_ticker]
#
#         dict_["text"].append(text)
#         dict_["return"].append(ret)
#         dict_["ticker"].append(ticker)
#         dict_["coef1"].append(val[0])
#         dict_["coef2"].append(val[1])
#         dict_["coef3"].append(val[2])
#         dict_["coef4"].append(val[3])
#         dict_["found_ticker"].append(relev_ticker)
#         print(ret, ticker, val)
#
#     tab = pd.DataFrame(dict_)
#     tab.to_excel("/home/stbarkhatov/resuts_1.xlsx")
