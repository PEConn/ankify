from main import Card, GuidGenerator, parse, parse_card, separators

SINGLE_CARD = """
some text

<!-- cloze -->

The capital of ==France== is ==Paris==.

some other text.
"""

MULTI_CARD = """
<!-- cloze -->

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
        Card(contents = "The capital of {{c1::France}} is {{c2::Paris}}.", guid=0),
        Card(contents = "The capital of {{c1::Germany}} is {{c2::Berlin}}.", guid=1)
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

    assert exp == parse_card(card, guid_generator=counting_generator())