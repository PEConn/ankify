from guid import GuidGenerator


def counting_generator() -> GuidGenerator:
    num = 0
    while True:
        yield num
        num += 1


def read(filename: str) -> str:
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()
