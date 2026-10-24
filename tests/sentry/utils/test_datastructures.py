from typing import cast

import pytest

from sentry.utils.datastructures import BidirectionalMapping


def test_bidirectional_mapping() -> None:
    value: BidirectionalMapping[str, int] = BidirectionalMapping({"a": 1, "b": 2})

    assert value["a"] == 1
    assert value["b"] == 2
    assert value.get_key(1) == "a"
    assert value.get_key(2) == "b"
    assert value.inverse() == {1: "a", 2: "b"}

    value["c"] = 3
    assert value["c"] == 3
    assert value.get_key(3) == "c"

    with pytest.raises(KeyError):
        value["d"]

    with pytest.raises(KeyError):
        value.get_key(4)

    assert value.get_key(4, "missing") == "missing"

    unhashable_value: list[int] = [1, 2, 3]
    with pytest.raises(TypeError):
        value["d"] = cast(int, unhashable_value)

    assert len(value) == len(value.inverse()) == 3

    del value["c"]

    assert len(value) == len(value.inverse()) == 2
