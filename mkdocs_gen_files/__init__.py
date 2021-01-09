"""A magical module that forwards everything to [mkdocs_gen_files.editor.FilesEditor.current][].

Just `import mkdocs_gen_files`.

Then `mkdocs_gen_files.open()` is the same as `mkdocs_gen_files.editor.FilesEditor.current.open()`.
"""

from .editor import FilesEditor


def __getattr__(name: str):
    return getattr(FilesEditor.current(), name)
