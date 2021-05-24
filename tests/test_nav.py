import pytest

from mkdocs_gen_files import Nav


@pytest.mark.golden_test("nav/*.yml")
def test_nav(golden):
    nav = Nav()
    exec(golden["code"], locals())
    assert "".join(nav.build_literate_nav()) == golden.out["output"]
