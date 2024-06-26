from card import Card, parse_card
from cloze_tag import ClozeTag
from file_data import FileData


def test_parse_card():
    card = "The capital of ==France== is ==Paris==."
    exp = Card(
        contents="<p>The capital of {{c1::France}} is {{c2::Paris}}.</p>\n",
        guid=0,
        new=True,
        tags=['file_name.md']
    )

    assert exp == parse_card(card, ClozeTag(guid=0, new=True), FileData("file name.md"))
