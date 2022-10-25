from dataclasses import dataclass
from typing import List, Optional

from card import Card, parse_card
from guid import GuidGenerator, random_generator
from cloze_tag import ClozeTag, parse_cloze_tag

# TODO: Do error handling.
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
            cards += [parse_card(paragraph, cloze_for_next)]

        cloze_for_next = parse_cloze_tag(paragraph, guid_generator)

        if cloze_for_next:
            updated_file += [cloze_for_next.to_string()]
        else:
            updated_file += [paragraph]

    return ParseResult(cards, updated_file="\n\n".join(updated_file))
