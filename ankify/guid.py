from typing import Generator
from random import randrange

GuidGenerator = Generator[int, None, None]


def random_generator() -> GuidGenerator:
    # Anki card ids are stored as sqlite3 integers.
    # https://github.com/ankidroid/Anki-Android/wiki/Database-Structure
    # The max value is 8 bytes long, but is signed.
    MAX = 1 << 63
    while True:
        yield randrange(MAX)
