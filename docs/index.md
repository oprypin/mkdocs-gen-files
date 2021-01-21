# mkdocs-gen-files

[Plugin][] for [MkDocs][] to programmatically generate documentation pages during the build.

## Installation

```shell
pip install mkdocs-gen-files
```

[mkdocs]: https://www.mkdocs.org/
[plugin]: https://www.mkdocs.org/user-guide/plugins/

## Usage

Activate the plugin in *mkdocs.yml* (`scripts` is a required list of Python scripts to execute):

```yaml
plugins:
  - search
  - gen-files:
      scripts:
        - gen_pages.py  # or any other name or path
```

Then create such a script *gen_pages.py* (this is relative to the root, *not* to the *docs* directory).

???+ example "Basic gen_pages.py"
    ```python
    import mkdocs_gen_files

    with mkdocs_gen_files.open("foo.md") as f:
        print("Hello, world!", file=f)
    ```

Or something a bit more interesting:

???+ example "Interesting gen_pages.py"
    ```python
    --8<-- "docs/gen_pages.py"
    ```

This adds programmatically generated pages to our site. This example script has been applied to this very site, you can see [sample/99-bottles.md](sample/99-bottles.md) etc.

## Description

For all intents and purposes, please conceptualize the [`mkdocs_gen_files.open()`](api.md) function as the actual [`open()`](https://docs.python.org/3/library/functions.html#open) function running under the [docs_dir](https://www.mkdocs.org/user-guide/configuration/#docs_dir) (*./docs/* by default, picked up from *mkdocs.yml*). In fact, if a script using *mkdocs_gen_files* is launched standalone, that is *actually* the case; you can use that to try out how the results look (though manual cleanup will be required).

But if attached as a MkDocs plugin, it represents that directory only virtually; **all file modifications affect only the ongoing site build and aren't persisted**. But you can still read (and even virtually append to) the actual files under *docs/*.

This is implemented by implicitly transferring the files to a temporary directory (which is what you really end up opening) and telling MkDocs to fetch them from there instead.
Note that this happens before MkDocs reads any of the doc files, so all of the outputs should look to it exactly as if the files were there all along.

All file modes are supported (even e.g. `ab+`). You could even open a file to read it, replace something in it, and write it back anew. Though at that point you may be better served by the ["macros" plugin](https://github.com/fralau/mkdocs_macros_plugin/).

Note that this function is separate from the top-level built-in `open()`, which is unaffected and can still be used normally, relative to the current working directory (which is *not* changed to *./docs/*, instead it's just the directory that you ran `mkdocs` from).

