from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import pytest

from vibecomfy.cli import build_parser
from vibecomfy.commands import import_workflow
from tests._cli_helpers import _load_emitted_provenance, _write_port_node_index, _write_port_workflow


def _run(argv: list[str]) -> int:
    args = build_parser().parse_args(["import", *argv])
    return args.func(args)


def test_import_creates_complete_folder_preserves_source_and_points_to_followups(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    _write_port_node_index(tmp_path)
    source = _write_port_workflow(tmp_path)
    original = source.read_bytes()
    monkeypatch.chdir(tmp_path)

    code = _run([str(source)])

    destination = tmp_path / "workflows" / "port_workflow"
    assert code == 0
    assert (destination / "source.json").read_bytes() == original
    assert (destination / "workflow.py").is_file()
    assert (destination / "workflow.vibe.json").is_file()
    assert _load_emitted_provenance(destination / "workflow.py")["source_hash"] == f"sha256:{hashlib.sha256(original).hexdigest()}"
    emitted_python = (destination / "workflow.py").read_text(encoding="utf-8")
    assert "source_ref='source.json'" in emitted_python
    assert str(tmp_path) not in emitted_python
    assert str(source.resolve()) not in emitted_python
    assert str(tmp_path).encode() not in (destination / "workflow.vibe.json").read_bytes()
    output = capsys.readouterr().out
    assert f"vibecomfy inspect {destination}" in output
    assert f"vibecomfy analyze info {destination}" in output
    assert f"vibecomfy validate {destination}" in output
    assert f"vibecomfy doctor {destination}" in output
    assert "Edit the Python file directly" in output
    assert not list((tmp_path / "workflows").glob(".*.import-*"))

    from vibecomfy.cli_loader import load_bundle
    from vibecomfy.security.provenance import Provenance

    bundle = load_bundle(destination, trust=Provenance.USER_CONFIRMED)
    bundle.require_canonical_authority("workflow validation")
    assert bundle.workflow.id == "port_workflow"
    assert bundle.workflow.validate().ok
    relocated = tmp_path / "moved workflow"
    destination.rename(relocated)
    moved_bundle = load_bundle(relocated, trust=Provenance.USER_CONFIRMED)
    moved_bundle.require_canonical_authority("workflow validation")
    assert moved_bundle.workflow.validate().ok


def test_import_collision_and_conversion_failure_leave_no_partial_destination(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    source = tmp_path / "incoming.json"
    source.write_text("{}", encoding="utf-8")
    destination = tmp_path / "destination"
    destination.mkdir()
    called = False

    def unexpected_convert(*_args, **_kwargs):
        nonlocal called
        called = True
        return 0, {}, ""

    monkeypatch.setattr(import_workflow, "_convert", unexpected_convert)
    assert _run([str(source), "--out", str(destination), "--json"]) == 1
    assert destination.is_dir() and list(destination.iterdir()) == []
    assert not called
    capsys.readouterr()

    destination.rmdir()

    def failed_convert(*_args, **_kwargs):
        return 1, {"status": "error", "message": "conversion rejected"}, ""

    monkeypatch.setattr(import_workflow, "_convert", failed_convert)
    assert _run([str(source), "--out", str(destination), "--json"]) == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "error"
    assert "conversion rejected" in payload["message"]
    assert not destination.exists()
    assert not list(tmp_path.glob(".destination.import-*"))


def test_import_dry_run_previews_paths_without_creating_anything(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    source = tmp_path / "incoming.json"
    source.write_text("{}", encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    observed: list[tuple[Path, bool]] = []

    def preview_convert(source_path: Path, python_path: Path, *, dry_run: bool, **_kwargs):
        observed.append((python_path, dry_run))
        return 0, {"status": "ok", "write": {"dry_run": True}}, ""

    monkeypatch.setattr(import_workflow, "_convert", preview_convert)
    assert _run([str(source), "--dry-run", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "preview"
    assert payload["folder"] == str(tmp_path / "workflows" / "incoming")
    assert observed == [(tmp_path / "workflows" / "incoming" / "workflow.py", True)]
    assert not (tmp_path / "workflows").exists()


def test_import_followup_commands_quote_folder_paths_with_spaces(capsys: pytest.CaptureFixture[str]) -> None:
    folder = "/tmp/my workflows/first import"
    import_workflow._emit(
        {
            "status": "ok",
            "folder": folder,
            "python": f"{folder}/workflow.py",
            "companion": f"{folder}/workflow.vibe.json",
            "original": f"{folder}/source.json",
        },
        json_output=False,
    )
    output = capsys.readouterr().out
    assert f"vibecomfy inspect '{folder}'" in output
    assert f"vibecomfy validate '{folder}'" in output
