from .editor import FilesEditor


def __getattr__(name: str):
    return getattr(FilesEditor.current(), name)
