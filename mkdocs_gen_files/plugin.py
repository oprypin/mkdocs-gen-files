from __future__ import annotations

import logging
import runpy
import shlex
import sys
import tempfile
import urllib.parse
from typing import TYPE_CHECKING, Any, TypeVar, Union

from mkdocs.config import Config
from mkdocs.config import config_options as opt
from mkdocs.config.base import BaseConfigOption, ValidationError
from mkdocs.exceptions import PluginError
from mkdocs.plugins import BasePlugin, event_priority

from .editor import FilesEditor

if TYPE_CHECKING:
    from mkdocs.config.defaults import MkDocsConfig
    from mkdocs.structure.files import Files
    from mkdocs.structure.pages import Page

    T = TypeVar("T")


log = logging.getLogger(f"mkdocs.plugins.{__name__}")


class _ScriptValue(Config):
    """Config value to store a path to a script to execute and its arguments"""

    path = opt.File(exists=True)
    args = opt.Optional(opt.Type(str))


class _Script(BaseConfigOption[Union[_ScriptValue, str]]):
    """Config option that stores either a `_ScriptValue` or `str`, where the
    latter contains a path to a script to execute"""

    def run_validation(self, value: object) -> dict[Any, Any] | str:
        if not isinstance(value, (dict, str)):
            raise ValidationError(
                f"Invalid configuration.  Expected a dict or str.  Found '{type(value)}'"
            )
        return value


class PluginConfig(Config):
    """Base plugin configuration"""

    scripts = opt.ListOfItems(_Script())


class GenFilesPlugin(BasePlugin[PluginConfig]):
    def on_files(self, files: Files, config: MkDocsConfig) -> Files:
        self._dir = tempfile.TemporaryDirectory(prefix="mkdocs_gen_files_")

        with FilesEditor(files, config, self._dir.name) as ed:
            for sub_config in self.config.scripts:
                """Parse the script configuration.  The sub_config may just be a
                string, in which case it's treated as a path ane executed
                directly.  Otherwise, the sub_config is a dictionary, with keys
                path and optionally argv, where path is the path to the executable,
                and argv is the arguments to the executable.  The arguments to the
                scripts are _always_ overridden, i.e. sys.argv is always modified.
                """
                # get the path to the executable and optionally arguments
                argv: list[str] = []
                if isinstance(sub_config, str):  # treat it as a path
                    file_name = sub_config
                else:  # treat it as a `_ScriptValue`
                    file_name = sub_config["path"]
                    if "argv" in sub_config:  # optionally add argv
                        argv = shlex.split(sub_config["argv"])
                # override sys.argv, but save it for later to restore
                old_sys_argv = sys.argv
                sys.argv = [file_name, *argv]
                # run the script
                try:
                    runpy.run_path(file_name)
                except SystemExit as e:
                    if e.code:
                        raise PluginError(f"Script {file_name!r} caused {e!r}")
                finally:  # restore sys.argv
                    sys.argv = old_sys_argv

        self._edit_paths = dict(ed.edit_paths)
        return ed.files

    def on_page_content(self, html, page: Page, config: MkDocsConfig, files: Files):
        repo_url = config.repo_url
        edit_uri = config.edit_uri

        src_path = page.file.src_uri
        if src_path in self._edit_paths:
            path = self._edit_paths.pop(src_path)
            if repo_url and edit_uri:
                # Ensure urljoin behavior is correct
                if not edit_uri.startswith(("?", "#")) and not repo_url.endswith("/"):
                    repo_url += "/"

                page.edit_url = path and urllib.parse.urljoin(
                    urllib.parse.urljoin(repo_url, edit_uri), path
                )

        return html

    @event_priority(-100)
    def on_post_build(self, config: MkDocsConfig):
        self._dir.cleanup()

        unused_edit_paths = {k: str(v) for k, v in self._edit_paths.items() if v}
        if unused_edit_paths:
            msg = "mkdocs_gen_files: These set_edit_path invocations went unused (the files don't exist): %r"
            log.warning(msg, unused_edit_paths)
