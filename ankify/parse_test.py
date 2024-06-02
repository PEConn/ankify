from textwrap import dedent

from card import Card
from parse import parse
from test_utils import counting_generator


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

FILENAME = "test file.md"
FILENAME_TAG = ["test_file.md"]

def test_parse_num_results_single():
    assert 1 == len(parse(SINGLE_CARD, FILENAME).cards)


def test_parse_num_results_multiple():
    assert 2 == len(parse(MULTI_CARD, FILENAME).cards)


def test_parse_single():
    exp = [
        Card(
            contents="<p>The capital of {{c1::France}} is {{c2::Paris}}.</p>\n",
            guid=0,
            new=True,
            tags=FILENAME_TAG,
        )
    ]

    assert exp == parse(SINGLE_CARD, FILENAME, guid_generator=counting_generator()).cards


def test_parse_single_updated_file():
    exp = dedent(
        """
    some text

    <!-- cloze id:0 -->

    The capital of ==France== is ==Paris==.

    some other text.
    """
    )

    assert exp == parse(SINGLE_CARD, FILENAME, guid_generator=counting_generator()).updated_file


def test_parse_multiple():
    exp = [
        Card(
            contents="<p>The capital of {{c1::France}} is {{c2::Paris}}.</p>\n",
            guid=123,
            new=False,
            tags=FILENAME_TAG,
        ),
        Card(
            contents="<p>The capital of {{c1::Germany}} is {{c2::Berlin}}.</p>\n",
            guid=0,
            new=True,
            tags=FILENAME_TAG,
        ),
    ]

    assert exp == parse(MULTI_CARD, FILENAME, guid_generator=counting_generator()).cards


def test_parse_multiple_updated_file():
    exp = dedent(
        """
    <!-- cloze id:123 -->

    The capital of ==France== is ==Paris==.

    <!-- cloze id:0 -->

    The capital of ==Germany== is ==Berlin==.
    """
    )

    assert exp == parse(MULTI_CARD, FILENAME, guid_generator=counting_generator()).updated_file

def test_parse_inline():
    file = "The capital of ==France== is ==Paris==. <!-- cloze -->"
    exp_cards = [
        Card(
            contents="<p>The capital of {{c1::France}} is {{c2::Paris}}.</p>\n",
            guid=0,
            new=True,
            tags=FILENAME_TAG,
        )
    ]

    exp_file = "The capital of ==France== is ==Paris==. <!-- cloze id:0 -->"

    res = parse(file, FILENAME, guid_generator=counting_generator())
    assert exp_cards == res.cards
    assert exp_file == res.updated_file

def new_card(guid: int, contents: str):
    return Card(contents = contents, guid=guid, new=True, tags=FILENAME_TAG)

def test_parse_multicloze():
    file = dedent("""
    <!-- clozes -->
    - Some ==cloze==.
    - Another ==cloze== is ==this==.

    """)

    exp_cards = [
            new_card(0, "<p>Some {{c1::cloze}}.</p>\n"),
            new_card(1, "<p>Another {{c1::cloze}} is {{c2::this}}.</p>\n"),
    ]

    exp_file = dedent("""
    <!-- clozes -->
    - Some ==cloze==. <!-- cloze id:0 -->
    - Another ==cloze== is ==this==. <!-- cloze id:1 -->

    """)
    
    res = parse(file, FILENAME, guid_generator=counting_generator())
    assert exp_cards == res.cards
    assert exp_file == res.updated_file
