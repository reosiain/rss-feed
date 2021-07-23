import bs4
import requests

investing_header = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9",
    "Pragma": "no-cache",
}

finaz_header = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip",
    "Accept-Language": "en-US,en;q=0.9",
    "Pragma": "no-cache",
}


def prime1_parser(url: str) -> str:
    """Specific parser for prime1 source"""
    response = requests.get(url, headers=investing_header)
    if response.status_code != 200:
        raise ValueError(
            f"Fetching error, url replied with {response.status_code} status code"
        )
    bs_obj = bs4.BeautifulSoup(response.content, "html.parser")
    article = bs_obj.find_all("div", {"class": "article-body__content"})
    article = article[0].find_all("p")
    texts = []
    for elem in article:
        texts.append(elem.text.replace("\xa0", " "))
    res = "|@|".join(texts)
    return res


def investing_parser(url: str) -> str:
    """Specific parser for Investing source"""
    response = requests.get(url, headers=investing_header)
    if response.status_code != 200:
        raise ValueError(
            f"Fetching error, url replied with {response.status_code} status code"
        )
    bs_obj = bs4.BeautifulSoup(response.content, "html.parser")
    article = bs_obj.find_all("div", {"class": "WYSIWYG articlePage"})
    article = article[0].find_all("p")
    texts = []
    for elem in article:
        texts.append(elem.text.replace("\xa0", " "))
    res = "|@|".join(texts)
    return res


def finaz_parser(url: str) -> str:
    """Specific parser for Finaz source"""
    response = requests.get(url, headers=finaz_header)
    if response.status_code != 200:
        raise ValueError(
            f"Fetching error, url replied with {response.status_code} status code"
        )
    bs_obj = bs4.BeautifulSoup(response.content.decode("utf-8"), "html.parser")
    article = bs_obj.find_all("div", {"class": "content"})
    article = article[0].find_all("p")
    texts = []
    for elem in article:
        texts.append(elem.text.replace("\xa0", " "))
    res = "|@|".join(texts)
    return res


def finmarket_interfax_parser(url: str) -> str:
    """Specific parser for finmarket source"""
    response = requests.get(url, headers=finaz_header)
    if response.status_code != 200:
        raise ValueError(
            f"Fetching error, url replied with {response.status_code} status code"
        )
    bs_obj = bs4.BeautifulSoup(response.content, "html.parser")
    article = bs_obj.find_all("div", {"itemprop": "articleBody"})
    texts = article[0].text.split("\r\n\t")
    res = "|@|".join(texts)
    return res


def finam_parser(url: str) -> str:
    """Specific parser for finmarket source"""
    response = requests.get(url, headers=finaz_header)
    if response.status_code != 200:
        raise ValueError(
            f"Fetching error, url replied with {response.status_code} status code"
        )
    bs_obj = bs4.BeautifulSoup(response.content, "html.parser")
    article = bs_obj.find_all("div", {"class": "handmade mid f-newsitem-text"})
    article = article[0].find_all("p")
    texts = []
    for elem in article:
        texts.append(elem.text.replace("\xa0", " "))
    res = "|@|".join(texts)
    return res
