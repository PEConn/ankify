
from math_tags import convert_math_tags

def test_basic():
    assert "\(n^2\)" == convert_math_tags("$n^2$")
