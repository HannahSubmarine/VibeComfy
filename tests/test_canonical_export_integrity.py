from __future__ import annotations

import argparse
import json
from pathlib import Path

import pytest

from tests._cli_helpers import _write_port_node_index, _write_port_workflow
from vibecomfy.commands import port as port_commands
from vibecomfy.porting.layout_store import read_store, store_from_ui_json
from vibecomfy.porting.refuse import EditorAheadError
from vibecomfy.workflow import VibeNode, VibeWorkflow, WorkflowSource


def _args(workflow: Path, out: Path | None = None, **overrides: object) -> argparse.Namespace:
    values = {
        "workflow": str(workflow),
        "ready": False,
        "to": "ui",
        "json": False,
        "object_info_cache": None,
        "no_object_info_cache": True,
        "out": str(out) if out is not None else None,
        "persist_sidecar": False,
        "from_path": None,
        "fresh": False,
        "strict": False,
        "main_positions": False,
        "no_virtual_wires": False,
        "force_drop": False,
        "dry_run": False,
        "change_report_out": None,
    }
    values.update(overrides)
    return argparse.Namespace(**values)


def _fake_workflow(path: Path) -> VibeWorkflow:
    workflow = VibeWorkflow("draft", WorkflowSource("draft", str(path), "python"))
    workflow.nodes["1"] = VibeNode("1", "LoadImage", uid="uid-1")
    return workflow


def _fake_ui(*, pos: list[int] | None = None) -> dict[str, object]:
    return {
        "nodes": [{
            "id": 1,
            "type": "LoadImage",
            "pos": pos or [12, 34],
            "size": [200, 80],
            "properties": {"vibecomfy_uid": "uid-1"},
            "widgets_values": ["input.png"],
        }],
        "links": [],
        "groups": [],
        "extra": {},
    }


def test_draft_json_export_without_readiness(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    _write_port_node_index(tmp_path)
    source = _write_port_workflow(tmp_path)
    monkeypatch.chdir(tmp_path)

    code = port_commands._cmd_port_export(_args(source, tmp_path / "draft.json", to="json"))

    assert code == 0
    assert json.loads(capsys.readouterr().out)["2"]["class_type"] == "SaveImage"


def test_draft_python_export_without_readiness(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    source = tmp_path / "draft.py"
    source.write_text(
        "from vibecomfy.workflow import VibeNode, VibeWorkflow, WorkflowSource\n"
        "def build():\n"
        "    wf = VibeWorkflow('draft', WorkflowSource('draft'))\n"
        "    wf.nodes['1'] = VibeNode('1', 'LoadImage', uid='uid-1')\n"
        "    return wf\n",
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)

    code = port_commands._cmd_port_export(_args(source, tmp_path / "draft-ui.json"))

    assert code == 0
    assert (tmp_path / "draft-ui.json").exists()


def test_explicit_out_does_not_write_sidecar_but_persist_sidecar_does(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = tmp_path / "draft.py"
    source.write_text("# draft\n", encoding="utf-8")
    workflow = _fake_workflow(source)
    monkeypatch.setattr(port_commands, "_build_conversion_provider", lambda args: object())
    monkeypatch.setattr(port_commands, "load_workflow_reference", lambda *args, **kwargs: workflow)
    monkeypatch.setattr(port_commands, "emit_ui_json", lambda *args, **kwargs: _fake_ui(pos=[90, 100]))

    out = tmp_path / "explicit.json"
    assert port_commands._cmd_port_export(_args(source, out)) == 0
    assert not source.with_suffix(".layout.json").exists()

    assert port_commands._cmd_port_export(_args(source, out, persist_sidecar=True)) == 0
    assert read_store(source)["entries"]["uid-1"]["pos"] == [90, 100]


def test_from_and_breadcrumb_preserve_layout(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    source = tmp_path / "draft.py"
    source.write_text("# draft\n", encoding="utf-8")
    workflow = _fake_workflow(source)
    prior = _fake_ui(pos=[700, 800])
    prior_path = tmp_path / "prior.json"
    prior_path.write_text(json.dumps(prior), encoding="utf-8")
    seen: list[dict[str, object]] = []

    monkeypatch.setattr(port_commands, "_build_conversion_provider", lambda args: object())
    monkeypatch.setattr(port_commands, "load_workflow_reference", lambda *args, **kwargs: workflow)
    monkeypatch.setattr(port_commands, "emit_ui_json", lambda *args, **kwargs: (seen.append(kwargs) or _fake_ui()))

    assert port_commands._cmd_port_export(_args(source, tmp_path / "from.json", from_path=str(prior_path))) == 0
    assert seen[-1]["prior_store"]["entries"]["uid-1"]["pos"] == [700, 800]

    breadcrumb = tmp_path / "breadcrumb.json"
    breadcrumb.write_text(json.dumps({**prior, "extra": {"vibecomfy": {"prior_path": str(source)}}}), encoding="utf-8")
    monkeypatch.setattr("vibecomfy.commands.port._export.default_output_path", lambda *args, **kwargs: breadcrumb)
    assert port_commands._cmd_port_export(_args(source, tmp_path / "breadcrumb-out.json")) == 0
    assert seen[-1]["prior_store"]["entries"]["uid-1"]["pos"] == [700, 800]


def test_v2_export_passes_canonical_presentation_directly(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from vibecomfy.commands.port import _export as port_export_cmd

    source = tmp_path / "canonical.py"
    source.write_text("# canonical\n", encoding="utf-8")
    workflow = _fake_workflow(source)
    presentation = {
        "nodes": {
            "ui_only_2": {
                "id": 2, "class_type": "MarkdownNote", "pos": [91, 92],
                "size": [301, 88], "color": "#123456", "bgcolor": "#654321",
            },
        },
        "links": [], "groups": [], "canvas": {},
        "annotations": [{
            "annotation_id": "ui_only_2", "scope_path": "",
            "owner": {"kind": "node", "uid": "ui_only_2"},
            "class_type": "MarkdownNote", "title": "H3", "content": "exact note",
        }],
    }
    seen: list[dict[str, object]] = []
    monkeypatch.setattr(port_commands, "_build_conversion_provider", lambda args: object())
    monkeypatch.setattr(port_commands, "load_workflow_reference", lambda *args, **kwargs: workflow)
    monkeypatch.setattr(port_export_cmd, "_read_canonical_presentation", lambda *args: presentation)
    monkeypatch.setattr(port_export_cmd, "_resolve_preserve_source", lambda *args: ({"entries": {}}, str(source), None, None))
    monkeypatch.setattr(port_commands, "emit_ui_json", lambda *args, **kwargs: (seen.append(kwargs) or _fake_ui()))

    assert port_commands._cmd_port_export(_args(source, tmp_path / "out.json")) == 0
    assert seen[-1]["presentation"] == presentation
    assert "prior_store" not in seen[-1]


def test_v2_from_overlay_preserves_annotation_content_and_applies_furniture(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from vibecomfy.commands.port import _export as port_export_cmd

    source = tmp_path / "canonical.py"
    source.write_text("# canonical\n", encoding="utf-8")
    workflow = _fake_workflow(source)
    presentation = {
        "nodes": {
            "uid-1": {"id": 1, "class_type": "LoadImage", "pos": [1, 2]},
            "note-1": {"id": 2, "class_type": "MarkdownNote", "pos": [3, 4]},
        },
        "links": [], "groups": [], "canvas": {},
        "annotations": [{
            "annotation_id": "note-1", "scope_path": "",
            "owner": {"kind": "node", "uid": "note-1"},
            "class_type": "MarkdownNote", "title": "H3", "content": "keep this",
        }],
    }
    seen: list[dict[str, object]] = []
    monkeypatch.setattr(port_commands, "_build_conversion_provider", lambda args: object())
    monkeypatch.setattr(port_commands, "load_workflow_reference", lambda *args, **kwargs: workflow)
    monkeypatch.setattr(port_export_cmd, "_read_canonical_presentation", lambda *args: presentation)
    monkeypatch.setattr(
        port_export_cmd,
        "_resolve_preserve_source",
        lambda *args: ({"entries": {"uid-1": {"pos": [90, 100]}}}, str(source), None, None),
    )
    monkeypatch.setattr(
        port_commands,
        "emit_ui_json",
        lambda *args, **kwargs: (seen.append(kwargs) or _fake_ui()),
    )

    prior = tmp_path / "prior.json"
    prior.write_text("{}", encoding="utf-8")
    assert port_commands._cmd_port_export(
        _args(source, tmp_path / "out.json", from_path=str(prior))
    ) == 0

    emitted = seen[-1]["presentation"]
    assert emitted["nodes"]["uid-1"]["pos"] == [90, 100]
    assert emitted["annotations"][0]["content"] == "keep this"


def test_presentation_overlay_preserves_canvas_id_when_semantic_id_collides() -> None:
    from vibecomfy.porting.emit.ui import _overlay_validated_presentation

    envelope = {
        "nodes": [{
            "id": 170,
            "type": "NestedSemantic",
            "properties": {"vibecomfy_uid": "semantic"},
        }],
        "links": [[1, 170, 0, 170, 0, "*"],],
    }
    presentation = {
        "nodes": {
            "ui_only_170": {
                "id": 170, "class_type": "MarkdownNote",
                "pos": [-1, -2], "size": [301, 88],
                "color": "#123456", "bgcolor": "#654321", "z_order": 7,
            },
        },
        "annotations": [{
            "annotation_id": "ui_only_170", "scope_path": "",
            "owner": {"kind": "node", "uid": "ui_only_170"},
            "class_type": "MarkdownNote", "title": "H3", "content": "exact note",
        }],
    }

    _overlay_validated_presentation(envelope, presentation, object())

    semantic = next(node for node in envelope["nodes"] if node["type"] == "NestedSemantic")
    note = next(node for node in envelope["nodes"] if node["type"] == "MarkdownNote")
    assert semantic["id"] != 170
    assert note["id"] == 170
    assert note["widgets_values"] == ["exact note"]
    assert envelope["links"] == [[1, semantic["id"], 0, semantic["id"], 0, "*"]]

def test_strict_refusal_is_explicit(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    source = tmp_path / "draft.py"
    source.write_text("# draft\n", encoding="utf-8")
    workflow = _fake_workflow(source)
    monkeypatch.setattr(port_commands, "_build_conversion_provider", lambda args: object())
    monkeypatch.setattr(port_commands, "load_workflow_reference", lambda *args, **kwargs: workflow)
    monkeypatch.setattr(port_commands, "emit_ui_json", lambda *args, **kwargs: (_ for _ in ()).throw(ValueError("schema-less node")))

    code = port_commands._cmd_port_export(_args(source, tmp_path / "strict.json", strict=True))

    assert code == 2
    assert "strict" in capsys.readouterr().err.lower()


def test_force_drop_is_visible_and_opt_in(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    source = tmp_path / "draft.py"
    source.write_text("# draft\n", encoding="utf-8")
    workflow = _fake_workflow(source)
    calls: list[bool] = []

    monkeypatch.setattr(port_commands, "_build_conversion_provider", lambda args: object())
    monkeypatch.setattr(port_commands, "load_workflow_reference", lambda *args, **kwargs: workflow)

    def emit(*args: object, **kwargs: object) -> dict[str, object]:
        forced = bool(kwargs["force_drop_editor_only"])
        calls.append(forced)
        if not forced:
            raise EditorAheadError([{"uid": "editor-1", "class_type": "Note"}])
        return _fake_ui()

    monkeypatch.setattr(port_commands, "emit_ui_json", emit)
    out = tmp_path / "forced.json"
    assert port_commands._cmd_port_export(_args(source, out)) == 4
    assert "--force-drop" in capsys.readouterr().err
    assert port_commands._cmd_port_export(_args(source, out, force_drop=True)) == 0
    assert calls == [False, False, True]


def test_recovery_report_is_visible_and_preview_is_no_write(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    source = tmp_path / "draft.py"
    source.write_text("# draft\n", encoding="utf-8")
    workflow = _fake_workflow(source)
    sidecar = source.with_suffix(".layout.json")
    sidecar.write_text(json.dumps(store_from_ui_json(_fake_ui(pos=[1, 2]))), encoding="utf-8")
    monkeypatch.setattr(port_commands, "_build_conversion_provider", lambda args: object())
    monkeypatch.setattr(port_commands, "load_workflow_reference", lambda *args, **kwargs: workflow)

    def emit(*args: object, **kwargs: object) -> dict[str, object]:
        kwargs["recovery_report"].append({"node_id": "1", "class_type": "LoadImage", "schema_less": True, "confidence": 0.0})
        return _fake_ui(pos=[3, 4])

    monkeypatch.setattr(port_commands, "emit_ui_json", emit)
    out = tmp_path / "preview.json"
    before = sidecar.read_bytes()
    assert port_commands._cmd_port_export(_args(source, out, dry_run=True)) == 0
    assert not out.exists()
    assert sidecar.read_bytes() == before
    assert "recovery-report" in capsys.readouterr().err
