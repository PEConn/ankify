from dataclasses import dataclass
from typing import Optional

@dataclass
class FileData:
    """Holds data specific to the file we're currently reading."""

    name: str
    deck: Optional[str] = None
