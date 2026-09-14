from __future__ import annotations

from pathlib import Path

from vibecomfy.node_source import lookup_node_source


def test_lookup_returns_class_body_from_schema_source_path(tmp_path: Path) -> None:
    source_path = tmp_path / "nodes.py"
    source_path.write_text(
        "@register_node\n"
        "class ExampleNode:\n"
        "    def run(self, value):\n"
        "        return value\n",
        encoding="utf-8",
    )

    result = lookup_node_source(
        "ExampleNode",
        {"source_path": str(source_path), "source_package": "example"},
        search_roots=(),
    )

    assert result.available
    assert result.path == str(source_path.resolve())
    assert result.class_name == "ExampleNode"
    assert result.source == (
        "@register_node\n"
        "class ExampleNode:\n"
        "    def run(self, value):\n"
        "        return value"
    )


def test_lookup_resolves_registered_name_to_python_class(tmp_path: Path) -> None:
    pack = tmp_path / "example_pack"
    pack.mkdir()
    source_path = pack / "nodes.py"
    source_path.write_text(
        "class InternalIntNode:\n"
        "    FUNCTION = 'run'\n"
        "    def run(self, value):\n"
        "        return value\n"
        "\n"
        "NODE_CLASS_MAPPINGS = {'easy int': InternalIntNode}\n",
        encoding="utf-8",
    )

    result = lookup_node_source(
        "easy int",
        {"source_package": "example_pack"},
        search_roots=(tmp_path,),
    )

    assert result.available
    assert result.path == str(source_path.resolve())
    assert result.class_name == "InternalIntNode"
    assert result.source.startswith("class InternalIntNode:")
    assert "NODE_CLASS_MAPPINGS" not in result.source


def test_registered_core_class_wins_over_unregistered_same_name(tmp_path: Path) -> None:
    helper = tmp_path / "samplers.py"
    helper.write_text("class KSampler:\n    pass\n", encoding="utf-8")
    nodes = tmp_path / "nodes.py"
    nodes.write_text(
        "class KSampler:\n"
        "    def sample(self):\n"
        "        return 'node implementation'\n"
        "\n"
        "NODE_CLASS_MAPPINGS = {'KSampler': KSampler}\n",
        encoding="utf-8",
    )

    result = lookup_node_source("KSampler", {}, search_roots=(tmp_path,))

    assert result.available
    assert result.path == str(nodes.resolve())
    assert "node implementation" in result.source


def test_lookup_follows_static_relative_registration_import(tmp_path: Path) -> None:
    pack = tmp_path / "pack"
    pack.mkdir()
    (pack / "__init__.py").write_text(
        "from .nodes import ActualNode\n"
        "NODE_CLASS_MAPPINGS = {'Fancy': ActualNode}\n",
        encoding="utf-8",
    )
    implementation = pack / "nodes.py"
    implementation.write_text(
        "class ActualNode:\n"
        "    def run(self):\n"
        "        return 'actual'\n",
        encoding="utf-8",
    )

    result = lookup_node_source("Fancy", {}, search_roots=(tmp_path,))

    assert result.available
    assert result.path == str(implementation.resolve())
    assert result.class_name == "ActualNode"
    assert "return 'actual'" in result.source


def test_lookup_reports_unavailable_for_cache_provenance_without_source(tmp_path: Path) -> None:
    cache_path = tmp_path / "object_info.json"
    cache_path.write_text("{}", encoding="utf-8")

    result = lookup_node_source(
        "MissingNode",
        {"source_path": str(cache_path), "source_package": "not_installed"},
        search_roots=(),
    )

    assert not result.available
    assert result.source is None
    assert result.path is None
    assert result.class_name is None
    assert result.reason.startswith("source_unavailable:")


def test_lookup_reports_syntax_and_ambiguity_instead_of_guessing(tmp_path: Path) -> None:
    broken = tmp_path / "broken.py"
    broken.write_text("NODE_CLASS_MAPPINGS = {'BrokenNode':\n", encoding="utf-8")
    broken_result = lookup_node_source("BrokenNode", {}, search_roots=(tmp_path,))
    assert not broken_result.available
    assert broken_result.reason.startswith("source_parse_failed:")

    first = tmp_path / "first.py"
    second = tmp_path / "second.py"
    first.write_text("class DuplicateNode:\n    pass\n", encoding="utf-8")
    second.write_text("class DuplicateNode:\n    pass\n", encoding="utf-8")
    ambiguous = lookup_node_source("DuplicateNode", {}, search_roots=(tmp_path,))
    assert not ambiguous.available
    assert ambiguous.reason.startswith("ambiguous_source:")
    assert "first.py" in ambiguous.reason and "second.py" in ambiguous.reason

    duplicated = tmp_path / "duplicated.py"
    duplicated.write_text(
        "class RepeatedNode:\n"
        "    pass\n"
        "\n"
        "class RepeatedNode:\n"
        "    pass\n",
        encoding="utf-8",
    )
    same_file_ambiguous = lookup_node_source(
        "RepeatedNode",
        {"source_path": str(duplicated)},
        search_roots=(),
    )
    assert not same_file_ambiguous.available
    assert same_file_ambiguous.reason.startswith("ambiguous_source:")


def test_lookup_ignores_nested_classes_and_generated_vibecomfy_wrappers(tmp_path: Path) -> None:
    source_root = tmp_path / "custom_nodes"
    generated = source_root / "vibecomfy" / "nodes"
    generated.mkdir(parents=True)
    (generated / "core.py").write_text(
        "class FakeNode:\n    pass\n", encoding="utf-8"
    )
    nested_only = source_root / "nested.py"
    nested_only.write_text(
        "class Container:\n"
        "    class FakeNode:\n"
        "        pass\n",
        encoding="utf-8",
    )

    result = lookup_node_source("FakeNode", {}, search_roots=(source_root,))

    assert not result.available
    assert result.reason.startswith("source_unavailable:")
