from textwrap import dedent

from markdown import convert


def test_html_escapes():
    assert "<p>big &gt; small</p>\n" == convert("big > small")
    assert "<p>gin &amp; tonic</p>\n" == convert("gin & tonic")
    assert "<p>small &lt; big</p>\n" == convert("small < big")


def test_lists():
    input = dedent(
        """
    Here is my list:
    * Apples
    * Oranges
    * Pears
    """
    )

    exp = dedent(
        """    <p>Here is my list:</p>

    <ul>
    <li><p>Apples</p></li>
    <li><p>Oranges</p></li>
    <li><p>Pears</p></li>
    </ul>
    """
    )

    assert exp == convert(input)
