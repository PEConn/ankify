from typing import Generator, Set
from random import randrange
import hashlib

GuidGenerator = Generator[int, None, None]

# Anki card ids are stored as sqlite3 integers.
# https://github.com/ankidroid/Anki-Android/wiki/Database-Structure
# The max value is 8 bytes long, but is signed.
MAX = 1 << 63

def random_generator() -> GuidGenerator:
    while True:
        yield randrange(MAX)

def counting_generator(collisions: Set[str]) -> GuidGenerator:
    for count in range(0, MAX):
        if count in collisions:
            continue

        yield count


# Yeah, this isn't really "Globally Unique" so maybe doesn't belong in this file.
def generate_deck_id(deck_name: str) -> int:
    return int(hashlib.sha1(deck_name.encode("utf-8")).hexdigest(), 16) % MAX
