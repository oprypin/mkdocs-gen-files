# mkdocs-gen-files

**[Plugin][] for [MkDocs][] to programmatically generate documentation pages during the build**

[![PyPI](https://img.shields.io/pypi/v/mkdocs-gen-files)](https://pypi.org/project/mkdocs-gen-files/)
[![GitHub](https://img.shields.io/github/license/oprypin/mkdocs-gen-files)](LICENSE.md)
[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/oprypin/mkdocs-gen-files/CI)](https://github.com/oprypin/mkdocs-gen-files/actions?query=event%3Apush+branch%3Amaster)

```shell
pip install mkdocs-gen-files
```

**Continue to the [documentation site][].**

[mkdocs]: https://www.mkdocs.org/
[plugin]: https://www.mkdocs.org/user-guide/plugins/
[documentation site]: https://oprypin.github.io/mkdocs-gen-files

## Usage

Activate the plugin in **mkdocs.yml** (`scripts` is a required list of Python scripts to execute):

```yaml
plugins:
  - search
  - mkdocs-gen-files:
      scripts:
        - gen_pages.py  # or any other name or path
```

Then create such a script **gen_pages.py** (this is relative to the root, *not* to the *docs* directory).

```python
import mkdocs_gen_files

with mkdocs_gen_files.open("foo.md") as f:
    print("Hello, world!", file=f)
```

This added a programmatically generated page to our site. That is, the document doesn't actually appear in our source files, it only *virtually* becomes part of the site to be built by MkDocs.

**Continue to the [documentation site][].**
