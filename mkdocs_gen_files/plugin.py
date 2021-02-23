import logging
import runpy
import tempfile
import urllib.parse

import mkdocs.config
import mkdocs.config.config_options
import mkdocs.plugins
import mkdocs.structure.files

try:
    from mkdocs.exceptions import PluginError
except ImportError:
    PluginError = SystemExit

from . import editor

log = logging.getLogger(f"mkdocs.plugins.{__name__}")
log.addFilter(mkdocs.utils.warning_filter)


class GenFilesPlugin(mkdocs.plugins.BasePlugin):
    config_scheme = (("scripts", mkdocs.config.config_options.Type(list)),)

    def on_files(
        self, files: mkdocs.structure.files.Files, config: mkdocs.config.Config
    ) -> mkdocs.structure.files.Files:
        self._dir = tempfile.TemporaryDirectory(prefix="mkdocs_gen_files_")

        with editor.FilesEditor(files, config, self._dir.name) as ed:
            for file_name in self.config["scripts"]:
                try:
                    runpy.run_path(file_name)
                except SystemExit as e:
                    if e.code:
                        raise PluginError(f"Script {file_name!r} caused {e!r}")

        self._edit_paths = ed.edit_paths
        return ed.files

    def on_page_content(
        self,
        html,
        page: mkdocs.structure.pages.Page,
        config: mkdocs.config.Config,
        files: mkdocs.structure.files.Files,
    ):
        repo_url = config.get("repo_url", None)
        edit_uri = config.get("edit_uri", None)

        if page.file.src_path in self._edit_paths:
            path = self._edit_paths.pop(page.file.src_path)
            if repo_url and edit_uri:
                page.edit_url = path and urllib.parse.urljoin(
                    urllib.parse.urljoin(repo_url, edit_uri), path
                )

        return html

    def on_post_build(self, config: mkdocs.config.Config):
        self._dir.cleanup()

        if self._edit_paths:
            msg = "mkdocs_gen_files: These set_edit_path invocations went unused (the files don't exist): %r"
            log.warning(msg, self._edit_paths)
