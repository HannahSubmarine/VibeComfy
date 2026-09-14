from __future__ import annotations

import builtins
import hashlib
import json
import shlex
from pathlib import Path

import pytest

from tests._cli_helpers import (
    _load_emitted_provenance,
    _write_port_node_index,
    _write_port_workflow,
)
from vibecomfy.cli import build_parser
from vibecomfy.commands import import_workflow
from vibecomfy.porting.import_service import ImportArtifacts


def _run(argv: list[str]) -> int:
    args = build_parser().parse_args(["import", *argv])
    return args.func(args)


def test_import_creates_inspectable_origin_bundle_and_points_to_tools(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    _write_port_node_index(tmp_path)
    source = _write_port_workflow(tmp_path)
    original = source.read_bytes()
    monkeypatch.chdir(tmp_path)

    code = _run([str(source), "--json"])

    destination = tmp_path / "workflows" / "port_workflow"
    assert code == 0
    output = json.loads(capsys.readouterr().out)
    assert (destination / "source.json").read_bytes() == original
    assert (destination / "workflow.py").is_file()
    assert (destination / "workflow.vibe.json").is_file()
    assert not (destination / "edit-report.json").exists()
    report = output["report"]
    assert report["transition_kind"] == "origin"
    assert report["parent_revision"] is None
    assert report["parent_task_id"] is None
    assert report["after"]["parent_revision"] is None
    assert report["members"]["source.json"] == f"sha256:{hashlib.sha256(original).hexdigest()}"
    assert _load_emitted_provenance(destination / "workflow.py")["source_hash"] == f"sha256:{hashlib.sha256(original).hexdigest()}"
    emitted_python = (destination / "workflow.py").read_text(encoding="utf-8")
    assert "source_ref='source.json'" in emitted_python
    assert str(tmp_path) not in emitted_python
    assert str(source.resolve()) not in emitted_python
    assert str(tmp_path).encode() not in (destination / "workflow.vibe.json").read_bytes()
    assert output["next"]["targets"] == f"vibecomfy edit {destination} targets"
    parsed_targets = build_parser().parse_args(output["next"]["targets"].split()[1:])
    assert parsed_targets.action == "targets"
    assert parsed_targets.workflow == str(destination)
    assert output["next"]["validate"] == f"vibecomfy validate {destination}"
    assert output["next"]["node"] == "vibecomfy node <ClassType>"
    assert output["tracking"]["mode"] == "untracked"
    assert not list((tmp_path / "workflows").glob(".*.import-*"))

    from vibecomfy.cli_loader import load_bundle
    from vibecomfy.security.provenance import Provenance

    bundle = load_bundle(destination, trust=Provenance.USER_CONFIRMED)
    bundle.require_canonical_authority("workflow validation")
    from vibecomfy.porting.edit.bundle_service import _is_canonical_python_source

    assert _is_canonical_python_source(bundle, destination / "workflow.py")
    assert bundle.workflow.id == "port_workflow"
    assert bundle.provenance["operation"] == "imported"
    assert bundle.revision_id == output["revision"]
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

    def unexpected_import(*_args, **_kwargs):
        nonlocal called
        called = True
        raise AssertionError("existing destination must be rejected before conversion")

    monkeypatch.setattr("vibecomfy.porting.import_service.import_workflow_bytes", unexpected_import)
    assert _run([str(source), "--out", str(destination), "--json"]) == 1
    assert destination.is_dir() and list(destination.iterdir()) == []
    assert not called
    capsys.readouterr()

    destination.rmdir()

    def failed_import(*_args, **_kwargs):
        raise ValueError("conversion rejected")

    monkeypatch.setattr("vibecomfy.porting.import_service.import_workflow_bytes", failed_import)
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
    source_bytes = source.read_bytes()
    members = {
        "workflow.py": "sha256:" + "a" * 64,
        "workflow.vibe.json": "sha256:" + "b" * 64,
        "source.json": "sha256:" + hashlib.sha256(source_bytes).hexdigest(),
    }
    artifacts = ImportArtifacts(
        source_bytes=source_bytes,
        python_bytes=b"python",
        companion_bytes=b"{}",
        report={"workflow_id": "incoming", "revision_id": "rev-1", "members": members, "readiness": {}, "diagnostics": []},
    )
    observed: list[tuple[bytes, str]] = []

    def preview_import(source_value: bytes, *, workflow_id: str, **_kwargs):
        observed.append((source_value, workflow_id))
        return artifacts

    monkeypatch.setattr("vibecomfy.porting.import_service.import_workflow_bytes", preview_import)
    assert _run([str(source), "--dry-run", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "preview"
    assert payload["folder"] == str(tmp_path / "workflows" / "incoming")
    assert observed == [(source_bytes, "incoming")]
    assert not (tmp_path / "workflows").exists()


def test_local_import_does_not_import_or_require_astrid(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    source = tmp_path / "incoming.json"
    source.write_bytes(b"{}\n")
    monkeypatch.chdir(tmp_path)
    artifacts = ImportArtifacts(
        source_bytes=source.read_bytes(),
        python_bytes=b"# local Python workflow\n",
        companion_bytes=b"{}\n",
        report={"workflow_id": "incoming", "revision_id": "revision", "members": {}},
    )
    monkeypatch.setattr("vibecomfy.porting.import_service.import_workflow_bytes", lambda *_a, **_kw: artifacts)
    args = build_parser().parse_args(["import", str(source), "--json"])
    real_import = builtins.__import__

    def forbid_astrid(name, *args, **kwargs):
        if name == "astrid" or name.startswith("astrid."):
            raise AssertionError("the local import path attempted to import Astrid")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", forbid_astrid)
    assert args.func(args) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["tracking"]["mode"] == "untracked"
    assert sorted(path.name for path in (tmp_path / "workflows" / "incoming").iterdir()) == [
        "source.json", "workflow.py", "workflow.vibe.json"
    ]


def test_import_followup_commands_quote_folder_paths_with_spaces(capsys: pytest.CaptureFixture[str]) -> None:
    folder = "/tmp/my workflows/first import"
    import_workflow._emit(
        {
            "status": "ok",
            "folder": folder,
            "python": f"{folder}/workflow.py",
            "companion": f"{folder}/workflow.vibe.json",
            "source_copy": f"{folder}/source.json",
            "report_path": f"{folder}/edit-report.json",
        },
        json_output=False,
    )
    output = capsys.readouterr().out
    command = next(line.strip() for line in output.splitlines() if " targets" in line and "vibecomfy edit" in line)
    assert command == f"vibecomfy edit '{folder}' targets"
    import shlex

    parsed_targets = build_parser().parse_args(shlex.split(command)[1:])
    assert parsed_targets.action == "targets"
    assert parsed_targets.workflow == folder
    assert f"vibecomfy validate '{folder}'" in output


def test_tracked_import_followups_keep_project_scope_in_human_output(
    capsys: pytest.CaptureFixture[str],
) -> None:
    folder = "/tmp/my workflows/first import"
    project_id = "project with spaces"
    import_workflow._emit(
        {
            "status": "ok",
            "folder": folder,
            "python": f"{folder}/workflow.py",
            "companion": f"{folder}/workflow.vibe.json",
            "source_copy": f"{folder}/source.json",
            "tracking": {"mode": "astrid", "project_id": project_id},
            "next": import_workflow._next_commands(folder, project=project_id),
        },
        json_output=False,
    )
    output = capsys.readouterr().out
    targets_command = next(
        line.strip() for line in output.splitlines()
        if " targets" in line and "vibecomfy edit" in line
    )
    edit_command = next(
        line.strip() for line in output.splitlines()
        if " set <target>.<field> " in line
    )
    for command, expected_action in ((targets_command, "targets"), (edit_command, "set")):
        parsed = build_parser().parse_args(shlex.split(command)[1:])
        assert parsed.project == project_id
        assert parsed.action == expected_action
