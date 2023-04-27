"""A magical module that forwards everything to [mkdocs_gen_files.editor.FilesEditor.current][].

Just `import mkdocs_gen_files`.

Then `mkdocs_gen_files.open()` is the same as `mkdocs_gen_files.editor.FilesEditor.current.open()`.
"""
from __future__ import annotations

import logging

from .editor import FilesEditor
from .nav import Nav  # noqa

__version__ = "0.5.0"

log = logging.getLogger(f"mkdocs.plugins.{__name__}")


def __getattr__(name: str):
    return getattr(FilesEditor.current(), name)
