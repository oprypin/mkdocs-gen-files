from __future__ import annotations

import logging
import runpy
import tempfile
import urllib.parse
from typing import TYPE_CHECKING

from mkdocs.config import Config
from mkdocs.config import config_options as opt
from mkdocs.exceptions import PluginError
from mkdocs.plugins import BasePlugin, event_priority

from .editor import FilesEditor

if TYPE_CHECKING:
    from mkdocs.config.defaults import MkDocsConfig
    from mkdocs.structure.files import Files
    from mkdocs.structure.pages import Page


log = logging.getLogger(f"mkdocs.plugins.{__name__}")


class PluginConfig(Config):
    scripts = opt.ListOfItems(opt.File(exists=True))


class GenFilesPlugin(BasePlugin[PluginConfig]):
    def on_files(self, files: Files, config: MkDocsConfig) -> Files:
        self._dir = tempfile.TemporaryDirectory(prefix="mkdocs_gen_files_")

        with FilesEditor(files, config, self._dir.name) as ed:
            for file_name in self.config.scripts:
                try:
                    runpy.run_path(file_name, run_name="__main__")
                except SystemExit as e:
                    if e.code:
                        raise PluginError(f"Script {file_name!r} caused {e!r}")

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
