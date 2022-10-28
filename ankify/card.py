from dataclasses import dataclass
from typing import Generator, List

from cloze_tag import ClozeTag

# TODO: Clean up my terminology.
@dataclass
class Card:
    """Keeps the result of parsing a single card."""

    contents: str
    guid: int

    # Whether or not the card is new.
    new: bool = False

    # TODO: Make this into an enum?
    grouping: str = ""


# TODO: HTML encode contents:
# https://github.com/kerrickstaley/genanki#my-field-data-is-getting-garbled
def parse_card(card: str, tag: ClozeTag) -> Card:
    card = card.strip()
    # card = "The capital of ==France== is ==Paris==."
    # 1. Split on ==.
    # 2. Join with ['{{c1::', '}}', '{{c2::', '}}', ..]
    parts = card.split("==")
    assert len(parts) % 2 == 1
    # TODO: What about cards that end with a ==?

    result: List[str] = []
    s = tag.get_separators()
    for part in parts:
        result += [part, next(s)]

    return Card(contents="".join(result[:-1]), guid=tag.guid, new=tag.new)
