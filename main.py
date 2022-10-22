from dataclasses import dataclass
from typing import Generator, List, Optional
from random import randrange

from genanki import Note, CLOZE_MODEL  # type: ignore

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


@dataclass
class ParseResult:
    """Holds the list of cards and the updated file as a result of a parse."""

    cards: List[Card]
    updated_file: str


def parse(
    contents: str, guid_generator: GuidGenerator = random_generator()
) -> ParseResult:
    paragraphs = contents.split("\n\n")
    cards: List[Card] = []
    cloze_for_next: Optional[ClozeTag] = None
    updated_file: List[str] = []

    for paragraph in paragraphs:
        if cloze_for_next:
            cards += [parse_card(paragraph, cloze_for_next.guid)]

        cloze_for_next = parse_cloze_tag(paragraph, guid_generator)

        if cloze_for_next:
            updated_file += [cloze_for_next.to_string()]
        else:
            updated_file += [paragraph]

    return ParseResult(cards, updated_file="\n\n".join(updated_file))


@dataclass
class ClozeTag:
    """Holds information about the <!-- cloze --> tag, used to signify a card is coming next."""

    guid: int

    # The leading and trailing whitespace the cloze originally had.
    # We need this to preserve it for the output.
    prefix: str = ""
    suffix: str = ""

    def to_string(self):
        return f"{self.prefix}<!-- cloze id:{self.guid} -->{self.suffix}"


def parse_cloze_tag(line: str, guid_generator: GuidGenerator) -> Optional[ClozeTag]:
    unstripped_line = line
    line = line.strip()

    if not line.startswith("<!--") or not line.endswith("-->"):
        return None

    # If the cloze has some leading or trailing whitespace, we want to preserve it for the output.
    prefix = unstripped_line[: unstripped_line.find("<")]
    suffix = unstripped_line[unstripped_line.find(">") + 1 :]

    parts = line.split(" ")

    if not "cloze" in parts:
        return None

    for part in parts:
        if not part.startswith("id:"):
            continue
        try:
            return ClozeTag(guid=int(part[len("id:") :]), prefix=prefix, suffix=suffix)
        except ValueError:
            pass

    return ClozeTag(guid=next(guid_generator), prefix=prefix, suffix=suffix)


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


if __name__ == "__main__":
    note = Note(
        model=CLOZE_MODEL, fields=["{{c1::Rome}} is the capital of {{c2::Italy}}", ""]
    )

    print(note)
