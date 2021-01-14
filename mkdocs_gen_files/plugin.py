import runpy
import tempfile

import mkdocs.config
import mkdocs.config.config_options
import mkdocs.plugins
import mkdocs.structure.files

try:
    from mkdocs.exceptions import PluginError
except ImportError:
    PluginError = SystemExit

from . import editor


class GenFilesPlugin(mkdocs.plugins.BasePlugin):
    config_scheme = (("scripts", mkdocs.config.config_options.Type(list)),)

    def on_files(self, files: mkdocs.structure.files.Files, config: mkdocs.config.Config):
        self._dir = tempfile.TemporaryDirectory(prefix="mkdocs_gen_files_")

        with editor.FilesEditor(files, config, self._dir.name) as ed:
            for file_name in self.config["scripts"]:
                try:
                    runpy.run_path(file_name)
                except SystemExit as e:
                    if e.code:
                        raise PluginError(f"Script {file_name!r} caused {e!r}")

        return ed.files

    def on_post_build(self, config: mkdocs.config.Config):
        self._dir.cleanup()
