from genanki import Note, CLOZE_MODEL

from dataclasses import dataclass

# TODO: Clean up my terminology.
@dataclass
class Card:
    """Keeps the result of parsing a single card."""
    contents: str

def parse(contents):
    paragraphs = contents.split("\n\n")
    cards = []
    next_is_card = False

    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if next_is_card:
            cards += [paragraph]
            next_is_card = False
        elif paragraph == "<!-- cloze -->":
            next_is_card = True

    return [parse_card(card) for card in cards]

def parse_card(card):
    # card = "The capital of ==France== is ==Paris==."
    # 1. Split on ==.
    # 2. Join with ['{{c1::', '}}', '{{c2::', '}}', ..]
    parts = card.split("==")
    assert len(parts) % 2 == 1
    # TODO: What about cards that end with a ==?

    result = []
    s = separators()
    for part in parts:
        result += [part, next(s)]

    return Card(contents="".join(result[:-1]))

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
