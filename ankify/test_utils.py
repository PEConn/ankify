from guid import GuidGenerator


def counting_generator() -> GuidGenerator:
    num = 0
    while True:
        yield num
        num += 1
