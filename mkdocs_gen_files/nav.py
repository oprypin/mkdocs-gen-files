from __future__ import annotations

import dataclasses
import os
from typing import Iterable, Mapping


class Nav:
    """An object representing MkDocs navigation, consisting of files under nested sequences of
    titles, which are treated like paths.
    """

    def __init__(self):
        self._data = {}

    def __setitem__(self, keys: str | tuple[str, ...], value: str):
        """Add a link to a file (*value*) into the nav, under the sequence of titles (*keys*).

        For example, writing `nav["Foo", "Bar"] = "foo/bar.md"` would mean creating a nav:
        `{"Foo": {"Bar": "foo/bar.md"}}`.

        Then, writing `nav["Foo", "Another"] = "test.md"` would merge with the existing sections
        where possible:
        `{"Foo": {"Bar": "foo/bar.md", "Another": "test.md"}}`.

        *keys* here can be any non-empty sequence of strings, it's just that Python implicitly
        creates a tuple from the comma-separated items in those square brackets.
        """
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
        filename: str | None

    def items(self) -> Iterable[Item]:
        return self._items(self._data, 0)

    @classmethod
    def _items(cls, data: Mapping, level: int) -> Iterable[Item]:
        for key, value in data.items():
            if key is not None:
                yield cls.Item(level=level, title=key, filename=value.get(None))
                yield from cls._items(value, level + 1)

    _markdown_escape_chars = tuple("!#()*+-[\\]_`{}")

    def build_literate_nav(self, indentation: int | str = "") -> Iterable[str]:
        if isinstance(indentation, int):
            indentation = " " * indentation
        for item in self.items():
            line = item.title
            if line.startswith(self._markdown_escape_chars):
                line = "\\" + line
            if item.filename is not None:
                line = f"[{line}]({item.filename})"
            yield indentation + "    " * item.level + "* " + line + "\n"
