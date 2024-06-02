from dataclasses import dataclass
from typing import List, Optional

from card import Card, parse_card
from cloze_tag import ClozeTag, create_cloze, parse_inline_cloze_tag, strip_inline_cloze
from file_data import FileData
from guid import GuidGenerator, random_generator

@dataclass
class ParseMultiClozeResult:
    cards: List[Card]
    updated_paragraph: str 

def parse_multi_cloze(
        paragraph: str,
        file_data: FileData,
        guid_generator: GuidGenerator = random_generator()
) -> Optional[ParseMultiClozeResult]:
    # A multi-cloze looks like this:
    #
    # <!-- clozes -->
    # - Question ==one==. <!-- cloze id: 123 -->
    # - Question ==two== is ==this==.
    #
    # If there's cloze missing at the end of the line (and it has a highlight,
    # then one is inserted).

    lines = paragraph.split("\n")
    if len(lines) < 2:
        return None
    if lines[0].strip() != "<!-- clozes -->":
        return None

    cards = []
    updated_paragraph = [lines[0]]

    # For each line after the first, treat it as an inline cloze:
    for line in lines[1:]:
        cloze = parse_inline_cloze_tag(line, guid_generator)
        sep = ""
        if not cloze:
            sep = " "
            cloze = create_cloze([], "", "", guid_generator)

        contents = strip_inline_cloze(line)

        if not "==" in contents:
            print(f"Ignoring line: {line}")
            continue

        prefix = ""
        if contents.strip().startswith("- "):
            i = contents.find("- ") + 2
            prefix = contents[:i]
            contents = contents[i:]
        else:
            print(f"Ignoring line: {line}")
            continue

        card = parse_card(contents, cloze, file_data)
        cards += [parse_card(contents, cloze, file_data)]
        updated_paragraph += [prefix + contents + sep + cloze.to_string()]

    return ParseMultiClozeResult(cards, "\n".join(updated_paragraph))
