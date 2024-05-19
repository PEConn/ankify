from typing import List

from pyfakefs.fake_filesystem import FakeFilesystem

from file_reader import tree_walk, process_tree
from test_utils import read


class Collector:
    def __init__(self):
        self.contents: List[str] = []

    def add(self, value: str):
        self.contents += [value]


def test_tree_walk(fs: FakeFilesystem):
    fs.create_file("/somefile.md")
    fs.create_file("/dir/otherfile.md")

    results = Collector()

    def add_result(path, filename):
        results.add(path)

    tree_walk("/", add_result)

    assert ["/somefile.md", "/dir/otherfile.md"] == results.contents


def test_tree_walk_extension(fs: FakeFilesystem):
    fs.create_file("/somefile.md")
    fs.create_file("/somefile.txt")
    fs.create_file("/dir/otherfile.md")
    fs.create_file("/dir/otherfile.txt")

    results = Collector()

    def add_result(path, filename):
        results.add(path)

    tree_walk("/", add_result, ".txt")

    assert ["/somefile.txt", "/dir/otherfile.txt"] == results.contents


def test_process_tree(fs: FakeFilesystem):
    fs.create_file("/somefile.md", contents="abc")
    fs.create_file("/dir/otherfile.md", contents="def")

    def repeat(filename: str, contents: str):
        return contents + contents

    process_tree("/", repeat)

    assert "abcabc" == read("/somefile.md")
    assert "defdef" == read("/dir/otherfile.md")
