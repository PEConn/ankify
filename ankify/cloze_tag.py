from dataclasses import dataclass
from typing import Optional

from guid import GuidGenerator


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
