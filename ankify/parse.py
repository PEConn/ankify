from dataclasses import dataclass
from typing import List, Optional

import yaml

from file_data import FileData
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
        filedata: FileData,
        guid_generator: GuidGenerator = random_generator()
) -> ParseParagraphResult:
    paragraph = paragraphs[index]
    cloze = parse_cloze_tag(paragraph, guid_generator)

    if cloze:
        if cloze.new:
            print("New card found in " + filedata.name)

        # Consume (and update) the cloze and the next paragraph.
        contents = paragraphs[index + 1]
        card = parse_card(contents, cloze, filedata)

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

    if len(paragraphs) == 0:
        return ParseResult([], contents)

    frontmatter = parse_frontmatter(paragraphs[0])
    filedata = FileData(filename, frontmatter.deck)

    index = 0
    while index < len(paragraphs):
        r = parse_paragraph(paragraphs, index, filedata, guid_generator)

        updated_file += r.updated_paragraphs
        cards += r.cards
        index = r.next_index

    return ParseResult(cards, updated_file = "\n\n".join(updated_file))

@dataclass
class ParseFrontmatterResult:
    deck: Optional[str] = None

def parse_frontmatter(paragraph: str):
    # Frontmatter should start with a "---" and end with a "---".
    lines = paragraph.split("\n")
    if len(lines) < 3:
        return ParseFrontmatterResult()
    if lines[0] != "---" or lines[-1] != "---":
        return ParseFrontmatterResult()

    y = "\n".join(lines[1:-1])
    parsed = yaml.safe_load(y)
    if "deck" in parsed:
        return ParseFrontmatterResult(parsed["deck"])

    return ParseFrontmatterResult()
