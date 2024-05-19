import os
from collections.abc import Callable
from typing import Optional


def tree_walk(root: str, function: Callable[[str, str], None], extension: str = ".md"):
    for root, _subdirs, files in os.walk(root):
        for filename in files:
            if not filename.endswith(extension):
                continue

            print(filename)

            function(os.path.join(root, filename), filename)


def process_tree(root: str, function: Callable[[str, str], str], extension: str = ".md"):
    def process(filename_and_path: str, filename: str) -> None:
        new_contents: Optional[str] = None
        with open(filename_and_path, "r+", encoding="utf-8") as f:
            contents = f.read()
            new_contents = function(filename.replace('.md', ''), contents)

            if contents != new_contents:
                f.seek(0)
                f.write(new_contents)
                f.truncate()

    tree_walk(root, process, extension=extension)
