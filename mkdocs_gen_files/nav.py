import dataclasses
import os
from typing import Iterable, Mapping, Optional, Tuple, Union


class Nav:
    def __init__(self):
        self._data = {}

    def __setitem__(self, keys: Union[str, Tuple[str, ...]], value: str):
        if isinstance(keys, str):
            keys = (keys,)
        cur = self._data
        if not keys:
            raise ValueError(f"The navigation path must not be empty (got {keys!r})")
        for key in keys:
            if not isinstance(key, str):
                raise TypeError(
                    f"The navigation path must consist of strings, but got a {type(key)}"
                )
            if not key:
                raise ValueError(f"The navigation name parts must not be empty (got {keys!r})")
            cur = cur.setdefault(key, {})
        cur[None] = os.fspath(value)

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

    _markdown_escape_chars = tuple("!#()*+-[\\]_`{}")

    def build_literate_nav(self, indentation: Union[int, str] = "") -> Iterable[str]:
        if isinstance(indentation, int):
            indentation = " " * indentation
        for item in self.items():
            line = item.title
            if line.startswith(self._markdown_escape_chars):
                line = "\\" + line
            if item.filename is not None:
                line = f"[{line}]({item.filename})"
            yield indentation + "    " * item.level + "* " + line + "\n"
