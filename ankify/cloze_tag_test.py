from typing import Generator, List

from cloze_tag import ClozeTag, parse_cloze_tag
from test_utils import counting_generator


def test_parse_cloze_tag_no_id():
    assert ClozeTag(guid=0, new=True) == parse_cloze_tag(
        "<!-- cloze -->", counting_generator()
    )


def test_parse_cloze_tag_invalid_no_keyword():
    assert None is parse_cloze_tag("<!-- -->", counting_generator())


def test_parse_cloze_tag_with_id():
    assert ClozeTag(guid=123) == parse_cloze_tag(
        "<!-- cloze id:123 -->", counting_generator()
    )


def test_parse_cloze_tag_with_invalid_id():
    assert ClozeTag(guid=0, new=True) == parse_cloze_tag(
        "<!-- cloze id:apple -->", counting_generator()
    )


def test_parse_cloze_tag_invalid():
    assert None is parse_cloze_tag(
        "The capital of ==France== is ==Paris==.", counting_generator()
    )


def test_parse_cloze_tag_preserve_whitespace():
    assert ClozeTag(guid=123, prefix=" ", suffix="  ") == parse_cloze_tag(
        " <!-- cloze id:123 -->  ", counting_generator()
    )


def generator_equals(list: List[str], gen: Generator[str, None, None]):
    for l in list:
        assert l == next(gen)


def test_separators_basic():
    tag = parse_cloze_tag("<!-- cloze -->", counting_generator())

    assert tag is not None

    generator_equals(
        ["{{c1::", "}}", "{{c2::", "}}", "{{c3::", "}}"], tag.get_separators()
    )


def test_separators_grouped():
    tag = parse_cloze_tag("<!-- cloze = -->", counting_generator())

    assert tag is not None

    generator_equals(
        ["{{c1::", "}}", "{{c1::", "}}", "{{c1::", "}}"], tag.get_separators()
    )


def test_separators_explicit():
    tag = parse_cloze_tag("<!-- cloze =:1,2,1 -->", counting_generator())

    assert tag is not None

    generator_equals(
        ["{{c1::", "}}", "{{c2::", "}}", "{{c1::", "}}"], tag.get_separators()
    )


def test_separators_explicit_beyond():
    tag = parse_cloze_tag("<!-- cloze =:2,1 -->", counting_generator())

    assert tag is not None

    generator_equals(
        ["{{c2::", "}}", "{{c1::", "}}", "{{c3::", "}}"], tag.get_separators()
    )
