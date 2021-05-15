import pytest

from mkdocs_gen_files import Nav


@pytest.fixture
def golden(request, golden):
    return golden.open(f"nav/{request.node.name}.yml")


def test_nav_empty(golden):
    nav = Nav()
    assert "".join(nav.build_literate_nav()) == golden.out["output"]


def test_nav_basic(golden):
    nav = Nav()
    nav["Hello"] = "test.md"
    assert "".join(nav.build_literate_nav()) == golden.out["output"]


def test_nav_with_index_item(golden):
    nav = Nav()
    nav["Hello", "World"] = "hello/world.md"
    nav["Hello"] = "hello/index.md"
    assert "".join(nav.build_literate_nav()) == golden.out["output"]


def test_nav_chaotic(golden):
    nav = Nav()
    nav["Hello", "World"] = "hello/world.md"
    nav["Hello"] = "hello/index.md"
    nav["a"] = "b/c/d/a.md"
    nav["b/c/d/a"] = "a.md"
    nav["Hello", "Beautiful", "World"] = "hello/world.md"
    assert "".join(nav.build_literate_nav()) == golden.out["output"]


def test_nav_special_chars(golden):
    nav = Nav()
    nav["__init__"] = "a.md"
    nav["__init__.py"] = "a.md"
    nav["`hi`"] = "a.md"
    assert "".join(nav.build_literate_nav()) == golden.out["output"]


def test_errors():
    nav = Nav()
    with pytest.raises(ValueError):
        nav[()] = "index.md"
    with pytest.raises(ValueError):
        nav[""] = "index.md"
    with pytest.raises(TypeError):
        nav[5] = "index.md"
    with pytest.raises(TypeError):
        nav["a", 5] = "index.md"
