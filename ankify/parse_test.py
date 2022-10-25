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


def test_parse_num_results_single():
    assert 1 == len(parse(SINGLE_CARD).cards)


def test_parse_num_results_multiple():
    assert 2 == len(parse(MULTI_CARD).cards)


def test_parse_single():
    exp = [
        Card(
            contents="The capital of {{c1::France}} is {{c2::Paris}}.", guid=0, new=True
        )
    ]

    assert exp == parse(SINGLE_CARD, guid_generator=counting_generator()).cards


def test_parse_single_updated_file():
    exp = dedent(
        """
    some text

    <!-- cloze id:0 -->

    The capital of ==France== is ==Paris==.

    some other text.
    """
    )

    assert exp == parse(SINGLE_CARD, guid_generator=counting_generator()).updated_file


def test_parse_multiple():
    exp = [
        Card(
            contents="The capital of {{c1::France}} is {{c2::Paris}}.",
            guid=123,
            new=False,
        ),
        Card(
            contents="The capital of {{c1::Germany}} is {{c2::Berlin}}.",
            guid=0,
            new=True,
        ),
    ]

    assert exp == parse(MULTI_CARD, guid_generator=counting_generator()).cards


def test_parse_multiple_updated_file():
    exp = dedent(
        """
    <!-- cloze id:123 -->

    The capital of ==France== is ==Paris==.

    <!-- cloze id:0 -->

    The capital of ==Germany== is ==Berlin==.
    """
    )

    assert exp == parse(MULTI_CARD, guid_generator=counting_generator()).updated_file
