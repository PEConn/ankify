import sys
from abc import ABC, abstractmethod
from typing import Callable, List
import argparse

from genanki import Deck, Note, Package, CLOZE_MODEL  # type: ignore

from card import Card
from guid import GuidGenerator, random_generator
from parse import parse
from file_reader import process_tree
from model import MY_CLOZE_MODEL


# Get the input args.
# Create some object.
# Process all the files (writing in place).
# Spit out the deck.


class ParseProcessor:
    def __init__(self, dry: bool, generator: GuidGenerator):
        self.cards: List[Card] = []
        self.dry = dry
        self.generator = generator

    def process_file(self, filename: str, contents: str):
        result = parse(contents, filename, self.generator)

        self.cards += result.cards
        
        if self.dry:
            return contents

        return result.updated_file


def write_anki_deck(cards: List[Card], dry: bool = False) -> None:
    deck = Deck(123456789, "Obsidian Notes")

    for card in cards:
        # print(card.tags)
        deck.add_note(Note(
            # model=CLOZE_MODEL,
            model=MY_CLOZE_MODEL,
            fields=[card.contents, ""],
            tags=card.tags,
            guid=card.guid))  # type: ignore

    if not dry:
        Package(deck).write_to_file("output.apkg")  # type: ignore


def generate_cards(
        root: str, dry: bool = False, generator: GuidGenerator = random_generator()
) -> List[Card]:
    # TODO: Return code?
    # TODO: Consider using the fileinput module?

    processor = ParseProcessor(dry, generator)

    # TODO: Check if directory exists.
    process_tree(root, processor.process_file)

    return processor.cards

parser = argparse.ArgumentParser(
    prog="ankify"
)
parser.add_argument(
    dest="root",
    help="The base directory to search for files to ankify."
)
parser.add_argument(
    "--dry-run",
    dest="dry",
    action="store_true",
    help="Whether to change input files and produce an output file."
)

if __name__ == "__main__":
    args = parser.parse_args()

    if args.dry:
        print("Dry run...")

    cards = generate_cards(args.root, args.dry)

    new_cards = len([card for card in cards if card.new])

    print(f"Generated {len(cards)} ({new_cards} new) cards.")

    if (len(cards)) > 0:
        write_anki_deck(cards, args.dry)
