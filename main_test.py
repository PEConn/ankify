from main import Card, ClozeTag, GuidGenerator, parse, parse_card, parse_cloze_tag, separators

SINGLE_CARD = """
some text

<!-- cloze -->

The capital of ==France== is ==Paris==.

some other text.
"""

MULTI_CARD = """
<!-- cloze id:123 -->

The capital of ==France== is ==Paris==.

<!-- cloze -->

The capital of ==Germany== is ==Berlin==.
"""

def counting_generator() -> GuidGenerator:
    num = 0
    while True:
        yield num
        num += 1

def test_parse_num_results_single():
    assert 1 == len(parse(SINGLE_CARD))

def test_parse_num_results_multiple():
    assert 2 == len(parse(MULTI_CARD))

def test_parse_single():
    exp = [Card(contents = "The capital of {{c1::France}} is {{c2::Paris}}.", guid=0)]

    assert exp == parse(SINGLE_CARD, guid_generator=counting_generator())

def test_parse_multiple():
    exp = [
        Card(contents = "The capital of {{c1::France}} is {{c2::Paris}}.", guid=123),
        Card(contents = "The capital of {{c1::Germany}} is {{c2::Berlin}}.", guid=0)
    ]

    assert exp == parse(MULTI_CARD, guid_generator=counting_generator())

def test_separators():
    s = separators()
    assert "{{c1::" == next(s)
    assert "}}" == next(s)
    assert "{{c2::" == next(s)
    assert "}}" == next(s)

def test_parse_card():
    card = "The capital of ==France== is ==Paris==."
    exp = Card(contents = "The capital of {{c1::France}} is {{c2::Paris}}.", guid=0)

    assert exp == parse_card(card, guid=0)

def test_parse_cloze_tag_no_id():
    assert ClozeTag(guid = None) == parse_cloze_tag("<!-- cloze -->")

def test_parse_cloze_tag_invalid_no_keyword():
    assert None is parse_cloze_tag("<!-- -->")

def test_parse_cloze_tag_with_id():
    assert ClozeTag(guid = 123) == parse_cloze_tag("<!-- cloze id:123 -->")

def test_parse_cloze_tag_with_invalid_id():
    assert ClozeTag(guid = None) == parse_cloze_tag("<!-- cloze id:apple -->")

def test_parse_cloze_tag_invalid():
    assert None is parse_cloze_tag("The capital of ==France== is ==Paris==.")