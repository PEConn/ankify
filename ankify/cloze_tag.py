from dataclasses import dataclass
from typing import Generator, List, Optional

from guid import GuidGenerator


@dataclass
class ClozeTag:
    """Holds information about the <!-- cloze --> tag, used to signify a card is coming next."""

    guid: int

    # The leading and trailing whitespace the cloze originally had.
    # We need this to preserve it for the output.
    prefix: str = ""
    suffix: str = ""

    # Whether this cloze already had a guid, or whether it's new.
    new: bool = False

    # TODO: Figure out how to make this less ugly.
    # This member determines how the parts of the cloze are grouped.
    # None means that each cloze should have its own number.
    # An empty list means that each cloze should have the same number.
    # A populated list gives the number each cloze should have.
    groupings: Optional[List[int]] = None

    def to_string(self):
        if self.groupings is None:
            grouping = ""
        elif self.groupings == []:
            grouping = "= "
        else:
            groups = ",".join([str(x) for x in self.groupings])
            grouping = f"=:{groups} "

        return f"{self.prefix}<!-- cloze id:{self.guid} {grouping}-->{self.suffix}"

    def get_separators(self) -> Generator[str, None, None]:
        num = 1

        if self.groupings:
            for g in self.groupings:
                yield f"{{{{c{g}::"
                yield "}}"

                num = max(num, g + 1)

        while True:
            yield f"{{{{c{num}::"
            yield "}}"

            if self.groupings == []:
                pass
            else:
                num += 1


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

    guid = None
    new = True
    groupings: Optional[List[int]] = None

    for part in parts:
        if part.startswith("id:"):
            try:
                guid = int(part[len("id:") :])
                new = False
            except ValueError:
                print(f"Poorly formatted id: '{part}'")
        elif part == "=":
            groupings = []
        elif part.startswith("=:"):
            try:
                groupings = [int(x) for x in part[len("=:") :].split(",")]
            except ValueError:
                print(f"Poorly formatted grouping: '{part}'")

    if guid is None:
        guid = next(guid_generator)

    return ClozeTag(
        guid=guid, prefix=prefix, suffix=suffix, new=new, groupings=groupings
    )
