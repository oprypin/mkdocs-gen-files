from __future__ import annotations

import collections
import os
import os.path
import pathlib
import shutil
from typing import IO, ClassVar, Optional

import mkdocs.config
import mkdocs.structure.files


def _normpath(*path: str):
    return os.path.normpath(os.path.join(*path)).replace(os.sep, "/")


def _file_sort_key(f: mkdocs.structure.files.File):
    parts = pathlib.PurePath(f.src_path).parts
    return tuple(chr(i != len(parts) - 1) + chr(f.name != "index") + p for i, p in enumerate(parts))


class FilesEditor:
    def open(self, name: str, mode="a", buffering=-1, encoding="utf-8", *args, **kwargs) -> IO:
        path = self._get_file(name, new="w" in mode)
        return open(path, mode, buffering, encoding, *args, **kwargs)

    @property
    def files(self) -> mkdocs.structure.files.Files:
        files = sorted(self._files.values(), key=_file_sort_key)
        return mkdocs.structure.files.Files(files)

    def _get_file(self, name: str, new: bool = False) -> str:
        new_f = mkdocs.structure.files.File(
            name,
            src_dir=self.directory,
            dest_dir=self.config["site_dir"],
            use_directory_urls=self.config["use_directory_urls"],
        )
        normname = _normpath(name)

        if new or normname not in self._files:
            os.makedirs(os.path.dirname(new_f.abs_src_path), exist_ok=True)
            self._files[normname] = new_f
            return new_f.abs_src_path

        f = self._files[normname]
        if f.abs_src_path != new_f.abs_src_path:
            os.makedirs(os.path.dirname(new_f.abs_src_path), exist_ok=True)
            self._files[normname] = new_f
            shutil.copyfile(f.abs_src_path, new_f.abs_src_path)
            return new_f.abs_src_path

        return f.abs_src_path

    def __init__(
        self,
        files: mkdocs.structure.files.Files,
        config: mkdocs.config.Config,
        directory: Optional[str] = None,
    ):
        self._files = collections.ChainMap({}, {_normpath(f.src_path): f for f in files})
        self.config = config
        if directory is None:
            directory = config["docs_dir"]
        self.directory = directory

    _current: ClassVar[Optional["FilesEditor"]] = None
    _default: ClassVar[Optional["FilesEditor"]] = None

    @classmethod
    def current(cls) -> FilesEditor:
        if cls._current:
            return cls._current
        if not cls._default:
            config = mkdocs.config.load_config("mkdocs.yml")
            config["plugins"].run_event("config", config)
            cls._default = FilesEditor(mkdocs.structure.files.Files([]), config)
        return cls._default

    def __enter__(self):
        type(self)._current = self
        return self

    def __exit__(self, *exc):
        type(self)._current = None
