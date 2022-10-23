from dataclasses import dataclass
from typing import Generator, List

# TODO: Clean up my terminology.
@dataclass
class Card:
    """Keeps the result of parsing a single card."""

    contents: str
    guid: int


# TODO: HTML encode contents:
# https://github.com/kerrickstaley/genanki#my-field-data-is-getting-garbled
def parse_card(card: str, guid: int) -> Card:
    card = card.strip()
    # card = "The capital of ==France== is ==Paris==."
    # 1. Split on ==.
    # 2. Join with ['{{c1::', '}}', '{{c2::', '}}', ..]
    parts = card.split("==")
    assert len(parts) % 2 == 1
    # TODO: What about cards that end with a ==?

    result: List[str] = []
    s = separators()
    for part in parts:
        result += [part, next(s)]

    return Card(contents="".join(result[:-1]), guid=guid)


def separators() -> Generator[str, None, None]:
    num = 1
    while True:
        yield f"{{{{c{num}::"
        yield "}}"
        num += 1
