from markdown2 import Markdown

converter = Markdown(extras=["cuddled-lists"])


def convert(md: str) -> str:
    # Double each newline to that contiguous lines can be interpreted as different
    return converter.convert(md.replace("\n", "\n\n"))
