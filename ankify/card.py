from dataclasses import dataclass
from typing import Generator, List, Optional

from markdown import convert

from cloze_tag import ClozeTag
from file_data import FileData

# TODO: Clean up my terminology.
@dataclass
class Card:
    """Keeps the result of parsing a single card."""

    contents: str
    guid: int
    tags: [str]

    # Whether or not the card is new.
    new: bool = False

    # TODO: Make this into an enum?
    grouping: str = ""

    deck: Optional[str] = None


def parse_card(card: str, tag: ClozeTag, filedata: FileData) -> Card:
    card = card.strip()
    # card = "The capital of ==France== is ==Paris==."
    # 1. Split on ==.
    # 2. Join with ['{{c1::', '}}', '{{c2::', '}}', ..]
    parts = card.split("==")
    if len(parts) % 2 != 1:
        print(card)
    assert len(parts) % 2 == 1
    # TODO: What about cards that end with a ==?

    result: List[str] = []
    s = tag.get_separators()
    for part in parts:
        result += [part, next(s)]

    contents: str = convert("".join(result[:-1]))

    return Card(
            contents=contents,
            guid=tag.guid,
            tags=[filedata.name.replace(' ', '_')],
            new=tag.new,
            deck = filedata.deck
    )
