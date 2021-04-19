import dataclasses
from typing import Iterable, Mapping, Optional, Tuple, Union


class Nav:
    def __init__(self):
        self._data = {}

    def __setitem__(self, keys: Union[str, Tuple[str, ...]], value: str):
        if isinstance(keys, str):
            keys = (keys,)
        cur = self._data
        for key in keys:
            if not isinstance(key, str):
                raise TypeError(
                    f"The navigation path must consist of strings, but got a {type(key)}"
                )
            cur = cur.setdefault(key, {})
        cur[None] = value

    @dataclasses.dataclass
    class Item:
        level: int
        title: str
        filename: Optional[str]

    def items(self) -> Iterable[Item]:
        return self._items(self._data, 0)

    @classmethod
    def _items(cls, data: Mapping, level: int) -> Iterable[Item]:
        for key, value in data.items():
            if key is not None:
                yield cls.Item(level=level, title=key, filename=value.get(None))
                yield from cls._items(value, level + 1)

    def build_literate_nav(self, indentation: Union[int, str] = "") -> Iterable[str]:
        if isinstance(indentation, int):
            indentation = " " * indentation
        for item in self.items():
            line = item.title
            if item.filename is not None:
                line = f"[{line}]({item.filename})"
            yield indentation + "    " * item.level + "* " + line + "\n"
