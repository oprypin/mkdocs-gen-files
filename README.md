# mkdocs-gen-files

**[Plugin][] for [ProperDocs][] to programmatically generate documentation pages during the build**

[![PyPI](https://img.shields.io/pypi/v/mkdocs-gen-files)](https://pypi.org/project/mkdocs-gen-files/)
[![License](https://img.shields.io/github/license/oprypin/mkdocs-gen-files)](https://github.com/oprypin/mkdocs-gen-files/blob/master/LICENSE.md)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/oprypin/mkdocs-gen-files/ci.yml.svg)](https://github.com/oprypin/mkdocs-gen-files/actions?query=event%3Apush+branch%3Amaster)

```shell
pip install mkdocs-gen-files
```

**Continue to the [documentation site][].**

[properdocs]: https://github.com/ProperDocs/properdocs#readme
[plugin]: https://properdocs.org/user-guide/plugins/
[documentation site]: https://oprypin.github.io/mkdocs-gen-files

## Usage

Activate the plugin in **properdocs.yml** (`scripts` is a required list of Python scripts to execute, always relative to **properdocs.yml**):

```yaml
plugins:
  - search
  - gen-files:
      scripts:
        - gen_pages.py  # or any other name or path
```

Then create such a script **gen_pages.py** (this is relative to the root, *not* to the **docs** directory).

```python
import mkdocs_gen_files

with mkdocs_gen_files.open("foo.md", "w") as f:
    print("Hello, world!", file=f)
```

This added a programmatically generated page to our site. That is, the document doesn't actually appear in our source files, it only *virtually* becomes part of the site to be built by ProperDocs.

**Continue to the [documentation site][].**
