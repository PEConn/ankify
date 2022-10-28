from textwrap import dedent
from pyfakefs.fake_filesystem import FakeFilesystem
from typing import List

from parse_test import SINGLE_CARD, MULTI_CARD
from main import generate_cards
from card import Card

from test_utils import counting_generator, read


def test_run(fs: FakeFilesystem):
    fs.create_file("/basic.md", contents=SINGLE_CARD)
    fs.create_file("/dir/otherfile.md", contents=MULTI_CARD)

    cards = generate_cards("/", counting_generator())

    assert (
        dedent(
            """
    some text

    <!-- cloze id:0 -->

    The capital of ==France== is ==Paris==.

    some other text.
    """
        )
        == read("/basic.md")
    )

    assert (
        dedent(
            """
    <!-- cloze id:123 -->

    The capital of ==France== is ==Paris==.

    <!-- cloze id:1 -->

    The capital of ==Germany== is ==Berlin==.
    """
        )
        == read("/dir/otherfile.md")
    )

    assert [
        Card(
            contents="<p>The capital of {{c1::France}} is {{c2::Paris}}.</p>\n",
            guid=0,
            new=True,
        ),
        Card(
            contents="<p>The capital of {{c1::France}} is {{c2::Paris}}.</p>\n",
            guid=123,
            new=False,
        ),
        Card(
            contents="<p>The capital of {{c1::Germany}} is {{c2::Berlin}}.</p>\n",
            guid=1,
            new=True,
        ),
    ] == cards
