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

@dataclass
class ParseParagraphResult:
    updated_paragraphs: List[str]
    next_index: int
    cards: List[Card]

def parse_paragraph(
        paragraphs: List[str], index: int,
        filename: str,
        guid_generator: GuidGenerator = random_generator()
) -> ParseParagraphResult:
    paragraph = paragraphs[index]
    cloze = parse_cloze_tag(paragraph, guid_generator)

    if cloze:
        if cloze.new:
            print("New card found in " + filename)

        # Consume (and update) the cloze and the next paragraph.
        contents = paragraphs[index + 1]
        card = parse_card(contents, cloze, filename)

        return ParseParagraphResult(
                updated_paragraphs = [cloze.to_string(), contents],
                next_index = index + 2,
                cards = [card]
        )
    else:
        # Consume the paragraph
        return ParseParagraphResult(
                updated_paragraphs = [paragraph],
                next_index = index + 1,
                cards = []
        )

def parse(
        contents: str, filename: str,
        guid_generator: GuidGenerator = random_generator()
) -> ParseResult:
    paragraphs = contents.split("\n\n")
    cards: List[Card] = []
    updated_file: List[str] = []

    index = 0
    while index < len(paragraphs):
        r = parse_paragraph(paragraphs, index, filename, guid_generator)

        updated_file += r.updated_paragraphs
        cards += r.cards
        index = r.next_index

    return ParseResult(cards, updated_file = "\n\n".join(updated_file))
