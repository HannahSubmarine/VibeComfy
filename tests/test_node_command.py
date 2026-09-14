from __future__ import annotations

import json
from types import SimpleNamespace

from vibecomfy.cli import build_parser
from vibecomfy.commands import COMMANDS
from vibecomfy.commands.node import _cmd_node
from vibecomfy.commands.nodes import _cmd_nodes_spec
from vibecomfy.schema.provider import InputSpec, NodeSchema, OutputSpec


class _Provider:
    def __init__(self, schema):
        self.schema = schema

    def get_schema(self, class_type):
        return self.schema if self.schema and class_type == self.schema.class_type else None


def _schema() -> NodeSchema:
    return NodeSchema(
        class_type="KSampler",
        pack="comfy-core",
        inputs={
            "seed": InputSpec(type="INT", required=True, default=12, min=0, max=99),
            "sampler": InputSpec(type="COMBO", choices=["euler", "heun"]),
        },
        outputs=[OutputSpec(type="LATENT", name="latent"), OutputSpec(type="INT", name="seed")],
        source_provider="object_info_cache",
        source_path="/cache/core.json",
        source_package="comfy-core",
        source_version="1.2",
    )


def _args(*argv):
    return build_parser().parse_args(["node", *argv])


def test_node_command_is_registered_as_a_top_level_command():
    assert "node" in [spec.name for spec in COMMANDS]
    parser = build_parser()
    assert "node" in parser._subparsers._group_actions[0].choices


def test_node_default_includes_identity_inputs_outputs_and_unavailable_source(monkeypatch, capsys):
    import vibecomfy.node_source as source_module
    import vibecomfy.commands.node as command

    monkeypatch.setattr(command, "get_authoring_schema_provider", lambda **kwargs: _Provider(_schema()))
    monkeypatch.setattr(source_module, "lookup_node_source", lambda *args, **kwargs: SimpleNamespace(
        available=False, path=None, class_name=None, reason="source_not_found", source=None
    ))
    assert _cmd_node(_args("KSampler")) == 0
    out = capsys.readouterr().out
    assert "Node: KSampler" in out and "Pack: comfy-core" in out
    assert "source provider: object_info_cache" in out
    assert "seed: INT (required; default=12; range min=0, max=99)" in out
    assert "sampler: COMBO (optional; choices=['euler', 'heun'])" in out
    assert "latent: LATENT" in out and "seed: INT" in out
    assert "Implementation source unavailable: source_not_found" in out


def test_node_filters_are_combinable_and_json_has_same_selected_sections(monkeypatch, capsys):
    import vibecomfy.node_source as source_module
    import vibecomfy.commands.node as command

    monkeypatch.setattr(command, "get_authoring_schema_provider", lambda **kwargs: _Provider(_schema()))
    monkeypatch.setattr(source_module, "lookup_node_source", lambda *args, **kwargs: SimpleNamespace(
        available=True, path="/nodes/sampler.py", class_name="KSampler", reason=None,
        source="class KSampler:\n    RETURN_TYPES = ('LATENT',)"
    ))
    args = _args("KSampler", "--inputs", "--source", "--json")
    assert args.func(args) == 0
    result = json.loads(capsys.readouterr().out)
    assert set(result) == {"identity", "inputs", "source"}
    assert "outputs" not in result
    assert result["inputs"]["seed"]["required"] is True
    assert result["source"]["path"] == "/nodes/sampler.py"
    assert "class KSampler" in result["source"]["code"]


def test_unknown_node_fails_with_nodes_list_hint(monkeypatch, capsys):
    import vibecomfy.commands.node as command

    monkeypatch.setattr(command, "get_authoring_schema_provider", lambda **kwargs: _Provider(None))
    assert _cmd_node(_args("MissingNode")) == 1
    err = capsys.readouterr().err
    assert "not found" in err
    assert "vibecomfy nodes list" in err


def test_unknown_node_json_error_is_structured(monkeypatch, capsys):
    import vibecomfy.commands.node as command

    monkeypatch.setattr(command, "get_authoring_schema_provider", lambda **kwargs: _Provider(None))
    assert _cmd_node(_args("MissingNode", "--json")) == 1
    result = json.loads(capsys.readouterr().out)
    assert result["error"] == "node_not_found"
    assert "vibecomfy nodes list" in result["message"]


def test_input_filter_does_not_scan_source_or_dump_provenance(monkeypatch, capsys):
    import vibecomfy.commands.node as command
    import vibecomfy.node_source as source_module

    monkeypatch.setattr(command, "get_authoring_schema_provider", lambda **kwargs: _Provider(_schema()))
    monkeypatch.setattr(source_module, "lookup_node_source", lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("unexpected source scan")))
    assert _cmd_node(_args("KSampler", "--inputs")) == 0
    out = capsys.readouterr().out
    assert out.count("Node: KSampler") == 1
    assert "Inputs:" in out and "Outputs:" not in out
    assert "Provenance:" not in out and "Pack:" not in out


def test_object_info_cache_is_passed_to_authoring_provider(monkeypatch, capsys, tmp_path):
    import vibecomfy.commands.node as command
    import vibecomfy.node_source as source_module

    seen = {}
    monkeypatch.setattr(command, "get_authoring_schema_provider", lambda **kwargs: (seen.update(kwargs) or _Provider(_schema())))
    monkeypatch.setattr(source_module, "lookup_node_source", lambda *args, **kwargs: SimpleNamespace(
        available=False, path=None, class_name=None, reason="source_unavailable", source=None
    ))
    cache = tmp_path / "object-info.json"
    assert _cmd_node(_args("KSampler", "--inputs", "--object-info-cache", str(cache))) == 0
    assert seen == {"object_info_cache_path": str(cache)}


def test_explicit_source_only_fails_when_source_is_unavailable(monkeypatch, capsys):
    import vibecomfy.node_source as source_module
    import vibecomfy.commands.node as command

    monkeypatch.setattr(command, "get_authoring_schema_provider", lambda **kwargs: _Provider(_schema()))
    monkeypatch.setattr(source_module, "lookup_node_source", lambda *args, **kwargs: SimpleNamespace(
        available=False, path=None, class_name=None, reason="source_not_found", source=None
    ))
    assert _cmd_node(_args("KSampler", "--source")) == 1
    assert "Implementation source unavailable" in capsys.readouterr().out


def test_default_keeps_schema_when_source_inspection_raises(monkeypatch, capsys):
    import vibecomfy.node_source as source_module
    import vibecomfy.commands.node as command

    monkeypatch.setattr(command, "get_authoring_schema_provider", lambda **kwargs: _Provider(_schema()))
    monkeypatch.setattr(source_module, "lookup_node_source", lambda *args, **kwargs: (_ for _ in ()).throw(OSError("source unreadable")))
    assert _cmd_node(_args("KSampler")) == 0
    out = capsys.readouterr().out
    assert "seed: INT" in out and "latent: LATENT" in out
    assert "Implementation source unavailable" in out
    assert "OSError: source unreadable" in out


def test_nodes_spec_parser_and_handler_remain_available(monkeypatch, capsys):
    import vibecomfy.commands.nodes as nodes_command

    schema = _schema()
    monkeypatch.setattr(nodes_command, "get_authoring_schema_provider", lambda **kwargs: _Provider(schema))
    args = build_parser().parse_args(["nodes", "spec", "KSampler"])
    assert args.func is _cmd_nodes_spec
    assert _cmd_nodes_spec(args) == 0
    assert json.loads(capsys.readouterr().out)["class_type"] == "KSampler"
