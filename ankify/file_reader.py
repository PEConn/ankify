import os
from collections.abc import Callable
from typing import Optional


def tree_walk(root: str, function: Callable[[str], None], extension: str = ".md"):
    for root, _subdirs, files in os.walk(root):
        for filename in files:
            if not filename.endswith(extension):
                continue

            print(filename)

            function(os.path.join(root, filename))


def process_tree(root: str, function: Callable[[str], str], extension: str = ".md"):
    def process(filename: str) -> None:
        new_contents: Optional[str] = None
        with open(filename, "r+", encoding="utf-8") as f:
            contents = f.read()
            new_contents = function(contents)

            if contents != new_contents:
                f.seek(0)
                f.write(new_contents)
                f.truncate()

    tree_walk(root, process, extension=extension)
