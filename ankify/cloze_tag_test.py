from cloze_tag import ClozeTag, parse_cloze_tag
from test_utils import counting_generator


def test_parse_cloze_tag_no_id():
    assert ClozeTag(guid=0) == parse_cloze_tag("<!-- cloze -->", counting_generator())


def test_parse_cloze_tag_invalid_no_keyword():
    assert None is parse_cloze_tag("<!-- -->", counting_generator())


def test_parse_cloze_tag_with_id():
    assert ClozeTag(guid=123) == parse_cloze_tag(
        "<!-- cloze id:123 -->", counting_generator()
    )


def test_parse_cloze_tag_with_invalid_id():
    assert ClozeTag(guid=0) == parse_cloze_tag(
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
