from pathlib import Path


def write_to_storage(hassh: str):

    with open(Path(__file__).parent.parent / "storage" / "hashes.txt", "a") as f:
        f.write(str(hassh))
        f.write("\n")
        f.close()


def read_storage():
    with open(Path(__file__).parent.parent / "storage" / "hashes.txt", "r") as f:
        alls = f.readlines()
    alls = [x.replace("\n", "") for x in alls]
    alls = set(alls)
    return alls


def dump_news(text):
    with open(Path(__file__).parent.parent / "storage" / "news.txt", "a") as f:
        f.write(text)
        f.write("\n")
        f.close()
