from collections.abc import Hashable, Iterator, MutableMapping
from typing import Never, cast, overload

__unset__ = object()


class BidirectionalMapping[K: Hashable, V: Hashable](MutableMapping[K, V]):
    """\
    An associative data structure in which the ``(key, value)`` pairs form a
    one-to-one correspondence in both directions.

    For example, when ``(a, b)`` is added to the mapping, ``b`` can be found
    when ``a`` is used as a key, and ``a`` can *also* be found when ``b`` is
    provided to ``get_key``.
    """

    def __init__(self, data: MutableMapping[K, V]) -> None:
        self.__data: MutableMapping[K, V] = data
        self.__inverse: dict[V, K] = {v: k for k, v in data.items()}
        if len(self.__data) != len(self.__inverse):
            raise ValueError("duplicate value provided")

    def __getitem__(self, key: K) -> V:
        return self.__data[key]

    def __setitem__(self, key: K, value: V) -> None:
        if not isinstance(key, Hashable):
            raise TypeError("key must be hashable")

        if not isinstance(value, Hashable):
            raise TypeError("value must be hashable")

        if value in self.__inverse:
            raise ValueError("value already present")

        previous = self.__data.pop(key, __unset__)
        if previous is not __unset__:
            assert self.__inverse.pop(cast(V, previous)) == key

        self.__data[key] = value
        self.__inverse[value] = key

    def __delitem__(self, key: K) -> None:
        del self.__inverse[self.__data.pop(key)]

    def __iter__(self) -> Iterator[K]:
        return iter(self.__data)

    def __len__(self) -> int:
        return len(self.__data)

    @overload
    def get_key(self, value: V, default: Never = ...) -> K: ...

    @overload
    def get_key[D](self, value: V, default: D) -> K | D: ...

    def get_key(self, value: V, default: object = __unset__) -> object:
        try:
            return self.__inverse[value]
        except KeyError:
            if default is __unset__:
                raise
            else:
                return default

    def inverse(self) -> dict[V, K]:
        return self.__inverse.copy()
