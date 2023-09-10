import pytest
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import File

from mkdocs_gen_files import editor


@pytest.mark.parametrize(
    "names",
    [
        ["a/b.md", "b/index.md", "b/a.md"],
        ["SUMMARY.md", "foo/a.md", "foo/bar/index.md", "foo/bar/SUMMARY.md"],
    ],
)
@pytest.mark.parametrize("use_directory_urls", [False, True])
def test_file_sort_key(use_directory_urls, names):
    files = [
        File(name, src_dir="", dest_dir="", use_directory_urls=use_directory_urls) for name in names
    ]
    sorted_names = [f.src_uri for f in sorted(files, key=editor.file_sort_key)]
    assert sorted_names == names


def test_edit_paths_consistency():
    conf = MkDocsConfig()
    conf["docs_dir"] = "."
    ed = editor.FilesEditor([], conf)
    ed.set_edit_path("foo//bar", "zzz//xxx")
    assert ed.edit_paths == {"foo/bar": "zzz//xxx"}
