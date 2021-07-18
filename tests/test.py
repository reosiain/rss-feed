from parsers import feed_functions as ff
from participants_extractor import natasha as nat


def test_text_grabber():

    raw_list = ff.parse_latest()
    clean = ff.clean_feed_list(raw_list)
    text = ff.get_text_from_link(clean[120]["link"], clean[120]["source"])
    print(text)
    if clean[120]["source"] == "finam01":
        assert text is None
    else:
        assert text is not None


def test_natasha():

    text = """В лидерах роста к середине сессии были расписки TCS Group (+1,91%) и '
    'привилегированные акции Татнефти (+1,12%). В лидерах снижения находились '
    'привилегированные акции Транснефти (-5,20%), которые упали после закрытия '
    'реестра по дивидендам, гдр X5 Retail Group (-1,66%), бумаги АЛРОСы (-1,37%) '
    'и Северстали (-1,26%). |@|Акции X5 Retail Group, АЛРОСы и Северстали в '
    'пятницу корректировались, несмотря на публикацию сильных операционных и '
    'финансовых результатов за 2-й квартал текущего года."""

    list_ = nat.extract_companies(text)
    assert len(list_) != 0
