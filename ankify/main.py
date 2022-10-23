import sys
from abc import ABC, abstractmethod

from genanki import Deck, Note, Package, CLOZE_MODEL  # type: ignore

from typing import Callable, List
from card import Card
from guid import GuidGenerator, random_generator
from parse import parse
from file_reader import process_tree

# Get the input args.
# Create some object.
# Process all the files (writing in place).
# Spit out the deck.


class ParseProcessor:
    def __init__(self, generator: GuidGenerator):
        self.cards: List[Card] = []
        self.generator = generator

    def process_file(self, contents: str):
        result = parse(contents, self.generator)

        self.cards += result.cards
        return result.updated_file


def write_anki_deck(cards: List[Card]) -> None:
    deck = Deck(123456789, "Markdown Notes")

    for card in cards:
        deck.add_note(Note(model=CLOZE_MODEL, fields=[card.contents, ""], guid=card.guid))  # type: ignore

    Package(deck).write_to_file("output.apkg")  # type: ignore


def generate_cards(
    root: str, generator: GuidGenerator = random_generator()
) -> List[Card]:
    # TODO: Dry run?
    # TODO: Return code?
    # TODO: Consider using the fileinput module?

    processor = ParseProcessor(generator)

    # TODO: Check if directory exists.
    process_tree(root, processor.process_file)

    return processor.cards


if __name__ == "__main__":
    args = sys.argv

    if len(args) < 2:
        print("Usage: ankify <root directory>")
    else:
        cards = generate_cards(args[1])

        print(f"Generated {len(cards)} cards.")

        if (len(cards)) > 0:
            write_anki_deck(cards)
