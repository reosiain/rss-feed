from pathlib import Path
import sys

sys.path.append(Path(__file__).parent.parent.__str__())

from participants_extractor import natasha_parser as nt


def test_extraction():
    """Not a real test"""
    with open(Path(__file__).parent / 'texts', 'r') as f:
        texts = f.readlines()

    new = []
    for text in texts:
        t_ = text.replace('\xa0', ' ').replace('\t', ' ')
        new.append(t_)
    for t in new:
        print(nt.extract_companies(t))

    assert True