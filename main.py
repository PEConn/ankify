from dataclasses import dataclass
from typing import Generator, List
from random import randrange

from genanki import Note, CLOZE_MODEL # type: ignore

# TODO: Do error handling.
# TODO: Typing.
# TODO: Clean up my terminology.
@dataclass
class Card:
    """Keeps the result of parsing a single card."""
    contents: str
    guid: int

GuidGenerator = Generator[int, None, None]
def random_generator() -> GuidGenerator:
    # Anki card ids are stored as sqlite3 integers.
    # https://github.com/ankidroid/Anki-Android/wiki/Database-Structure
    # The max value is 8 bytes long.
    MAX = 1 << 64
    while True:
        yield randrange(MAX)

def parse(contents: str,
        guid_generator: GuidGenerator = random_generator()) -> List[Card]:
    paragraphs = contents.split("\n\n")
    cards: List[str] = []
    next_is_card = False

    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if next_is_card:
            cards += [paragraph]
            next_is_card = False
        elif paragraph == "<!-- cloze -->":
            next_is_card = True

    return [parse_card(card, guid_generator) for card in cards]

# TODO: HTML encode contents:
# https://github.com/kerrickstaley/genanki#my-field-data-is-getting-garbled
def parse_card(card: str, guid_generator: GuidGenerator) -> Card:
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

    return Card(
        contents="".join(result[:-1]),
        guid=next(guid_generator)
    )

def separators():
    num = 1
    while True:
        yield f"{{{{c{num}::"
        yield "}}"
        num += 1

if __name__ == "__main__":
    note = Note(
        model=CLOZE_MODEL,
        fields=[
           '{{c1::Rome}} is the capital of {{c2::Italy}}', ''
        ])

    print(note)
