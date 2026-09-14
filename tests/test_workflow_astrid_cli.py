from __future__ import annotations

import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

from vibecomfy.cli import build_parser
from vibecomfy.security import GateContext, set_gate_context
from vibecomfy.schema import (
    FrozenSchemaSnapshotProvider,
    InputSpec,
    NodeSchema,
    capture_schema_snapshot,
    schema_payload_from_node_schema,
)
from vibecomfy.workflow import VibeWorkflow, WorkflowSource
from vibecomfy.workflow_bundle import emit_bundle_with_candidate, load_bundle
from vibecomfy.security.provenance import Provenance


def _provider() -> FrozenSchemaSnapshotProvider:
    integer = NodeSchema(
        class_type="Integer",
        pack="core",
        inputs={"value": InputSpec(type="INT", required=True)},
        outputs=[],
        widget_input_order=("value",),
    )
    snapshot = capture_schema_snapshot(
        class_types=("Integer",),
        request_snapshot={
            "contract_version": "schema_snapshot_v1",
            "schemas": {"Integer": schema_payload_from_node_schema("Integer", integer)},
            "missing_classes": [],
        },
        node_classes={"1": "Integer"},
    )
    return FrozenSchemaSnapshotProvider(snapshot)


def _digest(payload: bytes) -> str:
    return "sha256:" + hashlib.sha256(payload).hexdigest()


class _FakeAstrid:
    """Small offline SDK fake that settles VibeComfy task artifacts."""

    def __init__(self, schema_provider, source_bytes: bytes):
        self.schema_provider = schema_provider
        self.source_bytes = source_bytes
        self.objects: dict[str, bytes] = {}
        self.tasks_by_id: dict[str, dict] = {}
        self.tasks_by_key: dict[str, str] = {}
        self.admissions: list[dict] = []
        self.create_calls = 0
        self.show_calls = 0
        self.projects = SimpleNamespace(show=lambda _project: SimpleNamespace(ok=True, data={"project_id": "project-1"}))
        self.media = SimpleNamespace(import_file=self._import_file, read_bytes=self._read_bytes)
        self.tasks = SimpleNamespace(
            create=self._create_task,
            show=self._show_task,
        )

    def _import_file(self, *, project, path, idempotency_key):
        payload = Path(path).read_bytes()
        digest = _digest(payload)
        self.objects[digest] = payload
        return {"object_id": digest, "digest": digest}

    def _read_bytes(self, object_id):
        return self.objects[object_id]

    def _settle_outputs(self, payloads: dict[str, bytes]) -> list[dict[str, str]]:
        outputs = []
        for name, payload in payloads.items():
            digest = _digest(payload)
            self.objects[digest] = payload
            outputs.append({"name": name, "digest": digest})
        return outputs

    def _origin(self, workflow_id: str, source_bytes: bytes) -> dict[str, bytes]:
        from tempfile import TemporaryDirectory

        with TemporaryDirectory(prefix="fake-astrid-origin-") as directory:
            root = Path(directory)
            workflow = VibeWorkflow(
                workflow_id,
                WorkflowSource(workflow_id, path="source.json", source_type="scratchpad"),
            )
            workflow.add_node("Integer", uid="integer-one", value=7)
            python_path = root / "workflow.py"
            bundle = emit_bundle_with_candidate(
                workflow,
                python_path,
                {"operation": "imported", "source_hash": _digest(source_bytes)},
                None,
                operation="imported",
                source_provenance={"operation": "imported", "source_hash": _digest(source_bytes)},
            )
            python_bytes = python_path.read_bytes()
            companion_bytes = python_path.with_suffix(".vibe.json").read_bytes()
            bundle = load_bundle(
                python_path,
                trust=Provenance.USER_CONFIRMED,
                schema_provider=self.schema_provider,
            )
            source_path = root / "source.json"
            source_path.write_bytes(source_bytes)
            members = {
                "workflow.py": _digest(python_bytes),
                "workflow.vibe.json": _digest(companion_bytes),
                "source.json": _digest(source_bytes),
            }
            report = {
                "schema_version": 1,
                "transition_kind": "origin",
                "workflow_id": workflow_id,
                "workflow_identity": bundle.workflow_identity,
                "revision_id": bundle.revision_id,
                "parent_revision": None,
                "parent_task_id": None,
                "origin_task_id": None,
                "before": None,
                "after": {
                    "revision_id": bundle.revision_id,
                    "parent_revision": None,
                    "semantic_digest": bundle.semantic_digest,
                    "ui_digest": bundle.ui_digest,
                    "members": members,
                },
                "members": members,
                "readiness": {"status": "conversion_validated"},
                "diagnostics": [],
            }
            return {
                "python": python_bytes,
                "companion": companion_bytes,
                "source": source_bytes,
                "report": (json.dumps(report, sort_keys=True, separators=(",", ":")) + "\n").encode(),
            }

    def _edit(self, inputs: dict[str, bytes], spec: dict) -> dict[str, bytes]:
        from tempfile import TemporaryDirectory

        from vibecomfy.porting.edit.bundle_service import transition_bundle

        with TemporaryDirectory(prefix="fake-astrid-edit-") as directory:
            root = Path(directory)
            parent = root / "parent"
            parent.mkdir()
            parent_path = parent / "workflow.py"
            parent_path.write_bytes(inputs["python"])
            (parent / "workflow.vibe.json").write_bytes(inputs["companion"])
            (parent / "source.json").write_bytes(inputs["source"])
            transition_kind = spec["inputs"]["transition_kind"]
            parent_revision = spec["inputs"]["parent_revision"]
            if "operations" in inputs:
                envelope = json.loads(inputs["operations"])
                result = transition_bundle(
                    parent_path,
                    tool_calls=[{"tool": "edit_batch", "args": {"ops": envelope["ops"]}}],
                    schema_provider=self.schema_provider,
                )
            else:
                candidate_dir = root / "candidate"
                candidate_dir.mkdir()
                candidate_path = candidate_dir / "workflow.py"
                candidate_path.write_bytes(inputs["capture_python"])
                candidate_path.with_suffix(".vibe.json").write_bytes(inputs["companion"])
                result = transition_bundle(
                    parent_path,
                    capture=True,
                    candidate_python=candidate_path,
                    expected_parent_revision=parent_revision,
                    schema_provider=self.schema_provider,
                )

            python_bytes = parent_path.read_bytes()
            companion_bytes = parent_path.with_suffix(".vibe.json").read_bytes()
            members = {
                "workflow.py": _digest(python_bytes),
                "workflow.vibe.json": _digest(companion_bytes),
                "source.json": _digest(inputs["source"]),
            }
            after_bundle = load_bundle(
                parent_path,
                trust=Provenance.USER_CONFIRMED,
                schema_provider=self.schema_provider,
            )
            input_members = {
                "workflow.py": _digest(inputs["python"]),
                "workflow.vibe.json": _digest(inputs["companion"]),
                "source.json": _digest(inputs["source"]),
            }
            report = {
                "schema_version": 1,
                "transition_kind": transition_kind,
                "workflow_id": after_bundle.workflow.id,
                "workflow_identity": after_bundle.workflow_identity,
                "revision_id": after_bundle.revision_id,
                "parent_revision": parent_revision,
                "parent_task_id": spec["inputs"]["parent_task_id"],
                "origin_task_id": spec["inputs"]["origin_task_id"],
                "before": {
                    "revision_id": parent_revision,
                    "semantic_digest": result.before_semantic_digest,
                    "ui_digest": result.before_ui_digest,
                    "members": input_members,
                },
                "after": {
                    "revision_id": after_bundle.revision_id,
                    "parent_revision": parent_revision,
                    "semantic_digest": result.semantic_digest,
                    "ui_digest": result.ui_digest,
                    "members": members,
                },
                "members": members,
                "operations": list(result.operations),
                "diff": result.to_dict().get("diff"),
                "diagnostics": list(result.diagnostics),
            }
            return {
                "python": python_bytes,
                "companion": companion_bytes,
                "source": inputs["source"],
                "report": (json.dumps(report, sort_keys=True, separators=(",", ":")) + "\n").encode(),
            }

    def _create_task(self, *, project_id, capability, spec, input_manifest, idempotency_key):
        self.create_calls += 1
        if idempotency_key in self.tasks_by_key:
            return {"task_id": self.tasks_by_key[idempotency_key]}
        self.admissions.append({"capability": capability, "spec": spec, "idempotency_key": idempotency_key})
        task_id = f"task-{len(self.admissions)}"
        names = [item["name"] for item in spec["input_digests"]]
        uploaded = dict(zip(names, input_manifest))
        inputs = {name: self.objects[object_id] for name, object_id in uploaded.items()}
        if capability == "vibecomfy.import":
            outputs = self._origin(spec["inputs"]["workflow_id"], inputs["source"])
        elif capability == "vibecomfy.edit":
            outputs = self._edit(inputs, spec)
        else:
            raise AssertionError(capability)
        manifest = self._settle_outputs(outputs)
        self.tasks_by_id[task_id] = {
            "task_id": task_id,
            "state": "succeeded",
            "result": {"outputs": manifest},
        }
        self.tasks_by_key[idempotency_key] = task_id
        return {"task_id": task_id}

    def _show_task(self, task_id):
        self.show_calls += 1
        return self.tasks_by_id[task_id]


def _run(argv: list[str]) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


def test_tracked_import_edit_capture_and_recover_use_task_lineage_without_extra_admission(
    tmp_path: Path, monkeypatch, capsys
) -> None:
    provider = _provider()
    fake = _FakeAstrid(provider, b'{"source":"fixture"}\n')
    receipt_root = tmp_path / "receipts"
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("vibecomfy.commands._astrid_workflows.open_client", lambda: fake)
    monkeypatch.setattr("vibecomfy.commands._astrid_workflows.receipt_root", lambda: receipt_root)
    monkeypatch.setattr("vibecomfy.schema.get_authoring_schema_provider", lambda **_kwargs: provider)
    monkeypatch.setenv("HOME", str(tmp_path))
    set_gate_context(GateContext(non_interactive=True, assume_yes=True))

    source = tmp_path / "incoming.json"
    source.write_bytes(fake.source_bytes)
    bundle_dir = tmp_path / "workflows" / "incoming"
    assert _run(["import", str(source), "--project", "demo", "--json"]) == 0
    origin = json.loads(capsys.readouterr().out)
    assert origin["tracking"]["mode"] == "astrid"
    assert sorted(path.name for path in bundle_dir.iterdir()) == ["source.json", "workflow.py", "workflow.vibe.json"]
    origin_bundle = load_bundle(bundle_dir, trust=Provenance.USER_CONFIRMED, schema_provider=provider)
    assert origin_bundle.workflow.source.provenance["operation"] == "imported"
    assert origin_bundle.revision_id == origin["revision"]

    # A typed edit uses the last accepted task outputs as immutable parent and
    # publishes a separate bundle only after verifying all task/report digests.
    edit_dir = tmp_path / "branches" / "edited"
    assert _run([
        "edit", str(bundle_dir), "--project", "demo", "--out", str(edit_dir), "--json", "set", "integer-one.value", "23"
    ]) == 0
    edit = json.loads(capsys.readouterr().out)
    edit_admission = fake.admissions[-1]
    assert edit["transition_kind"] == "typed_edit"
    assert edit["parent_task_id"] == origin["task_id"]
    assert edit["origin_task_id"] == origin["task_id"]
    assert edit_admission["spec"]["inputs"]["parent_revision"] == origin["revision"]
    edited = load_bundle(edit_dir, trust=Provenance.USER_CONFIRMED, schema_provider=provider)
    assert edited.workflow.nodes["1"].inputs["value"] == 23
    assert (edit_dir / "source.json").read_bytes() == fake.source_bytes
    assert sorted(path.name for path in edit_dir.iterdir()) == ["source.json", "workflow.py", "workflow.vibe.json"]
    assert load_bundle(bundle_dir, trust=Provenance.USER_CONFIRMED, schema_provider=provider).workflow.nodes["1"].inputs["value"] == 7

    # Direct Python capture is calculated against the immutable accepted task,
    # not against the edited candidate bytes used as input.
    python_path = edit_dir / "workflow.py"
    candidate = python_path.read_bytes().replace(b"value=23", b"value=31")
    python_path.write_bytes(candidate)
    assert _run(["edit", str(edit_dir), "--project", "demo", "--json", "capture"]) == 0
    capture = json.loads(capsys.readouterr().out)
    capture_admission = fake.admissions[-1]
    assert capture["transition_kind"] == "manual_capture"
    assert capture["parent_task_id"] == edit["task_id"]
    assert capture["origin_task_id"] == origin["task_id"]
    assert capture_admission["spec"]["inputs"]["parent_revision"] == edit["revision_id"]
    assert capture["report"]["operations"] == []
    assert capture["report"]["before"]["semantic_digest"] == edited.semantic_digest
    assert capture["report"]["before"]["ui_digest"] == edited.ui_digest
    assert load_bundle(edit_dir, trust=Provenance.USER_CONFIRMED, schema_provider=provider).workflow.nodes["1"].inputs["value"] == 31

    # Recovery can materialize already settled bytes by task ID. The command
    # only reads the task and never submits another task.
    recovery_folder = tmp_path / "recovered"
    python_path.write_bytes(b"preserve this local branch")
    before_admissions = len(fake.admissions)
    assert _run(["recover", capture["task_id"], "--out", str(recovery_folder), "--json"]) == 0
    recovered = json.loads(capsys.readouterr().out)
    assert recovered["re_admitted"] is False
    assert len(fake.admissions) == before_admissions
    assert sorted(path.name for path in recovery_folder.iterdir()) == ["source.json", "workflow.py", "workflow.vibe.json"]
    assert (recovery_folder / "workflow.py").read_bytes() == fake.objects[capture["members"]["workflow.py"]]


def test_tracked_edit_stale_local_parent_keeps_task_outputs_and_rejects_writeback(
    tmp_path: Path, monkeypatch, capsys
) -> None:
    provider = _provider()
    fake = _FakeAstrid(provider, b'{"source":"fixture"}\n')
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("vibecomfy.commands._astrid_workflows.open_client", lambda: fake)
    monkeypatch.setattr("vibecomfy.commands._astrid_workflows.receipt_root", lambda: tmp_path / "receipts")
    monkeypatch.setattr("vibecomfy.schema.get_authoring_schema_provider", lambda **_kwargs: provider)
    monkeypatch.setenv("HOME", str(tmp_path))
    set_gate_context(GateContext(non_interactive=True, assume_yes=True))

    source = tmp_path / "incoming.json"
    source.write_bytes(fake.source_bytes)
    bundle_dir = tmp_path / "workflows" / "incoming"
    assert _run(["import", str(source), "--project", "demo", "--json"]) == 0
    capsys.readouterr()
    python_path = bundle_dir / "workflow.py"
    original = python_path.read_bytes()
    # Alter an unrelated local byte after admission by mutating just before the
    # pair writer's CAS check.
    import importlib

    adapter = importlib.import_module("vibecomfy.commands._astrid_workflows")
    real_materialize = adapter.materialize_outputs
    monkeypatch.setattr(
        "vibecomfy.commands._astrid_workflows.materialize_outputs",
        lambda outputs, destination, *, expected_members=None: (
            python_path.write_bytes(b"concurrent local writer"),
            real_materialize(outputs, destination, expected_members=expected_members),
        )[1],
    )
    code = _run([
        "edit", str(bundle_dir), "--project", "demo", "--json", "set", "integer-one.value", "23"
    ])
    assert code == 1
    result = json.loads(capsys.readouterr().out)
    assert "local workflow changed" in result["message"]
    assert python_path.read_bytes() == b"concurrent local writer"
    assert len(fake.admissions) == 2  # origin plus the one immutable edit task
    assert original != python_path.read_bytes()
    edit_receipt = __import__("vibecomfy.commands._astrid_workflows", fromlist=["read_receipt"]).read_receipt("task-2")
    assert edit_receipt["outputs"]["workflow.py"]

    # The completed task can still be recovered to a separate folder.
    out = tmp_path / "settled-copy"
    assert _run(["recover", "task-2", "--out", str(out), "--json"]) == 0
    recovered = json.loads(capsys.readouterr().out)
    assert recovered["re_admitted"] is False
    assert sorted(path.name for path in out.iterdir()) == ["source.json", "workflow.py", "workflow.vibe.json"]


def test_tracked_edit_retry_after_timeout_reuses_admitted_task_key(
    tmp_path: Path, monkeypatch, capsys
) -> None:
    import importlib

    from vibecomfy.commands._astrid_workflows import AstridWorkflowError

    provider = _provider()
    fake = _FakeAstrid(provider, b'{"source":"fixture"}\n')
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("vibecomfy.commands._astrid_workflows.open_client", lambda: fake)
    monkeypatch.setattr("vibecomfy.commands._astrid_workflows.receipt_root", lambda: tmp_path / "receipts")
    monkeypatch.setattr("vibecomfy.schema.get_authoring_schema_provider", lambda **_kwargs: provider)
    set_gate_context(GateContext(non_interactive=True, assume_yes=True))

    source = tmp_path / "incoming.json"
    source.write_bytes(fake.source_bytes)
    bundle_dir = tmp_path / "workflows" / "incoming"
    assert _run(["import", str(source), "--project", "demo", "--json"]) == 0
    capsys.readouterr()

    adapter = importlib.import_module("vibecomfy.commands._astrid_workflows")
    original_wait = adapter.wait_for_task
    interrupted: set[str] = set()

    def timeout_once(client, task_id, **kwargs):
        if task_id != "task-1" and task_id not in interrupted:
            interrupted.add(task_id)
            raise AstridWorkflowError(f"simulated timeout for {task_id}")
        return original_wait(client, task_id, **kwargs)

    monkeypatch.setattr(adapter, "wait_for_task", timeout_once)
    argv = ["edit", str(bundle_dir), "--project", "demo", "--json", "set", "integer-one.value", "23"]
    assert _run(argv) == 1
    first_error = json.loads(capsys.readouterr().out)
    assert "simulated timeout" in first_error["message"]
    assert len(fake.admissions) == 2
    first_edit_key = fake.admissions[-1]["idempotency_key"]

    # Recover can settle a receipt after the caller timed out. The receipt is
    # durable before waiting and recovery reads the exact task result only.
    recovered_dir = tmp_path / "recovered-after-timeout"
    assert _run(["recover", "task-2", "--out", str(recovered_dir), "--json"]) == 0
    recovered = json.loads(capsys.readouterr().out)
    assert recovered["task_id"] == "task-2"
    assert recovered["re_admitted"] is False
    assert len(fake.admissions) == 2

    # Repeating the exact request after a timeout reaches the SDK's same
    # idempotency key and reads the already-settled task; it doesn't admit a
    # second transition.
    assert _run(argv) == 0
    result = json.loads(capsys.readouterr().out)
    assert result["task_id"] == "task-2"
    assert fake.admissions[-1]["idempotency_key"] == first_edit_key
    assert len(fake.admissions) == 2
    assert fake.create_calls == 3
    assert load_bundle(bundle_dir, trust=Provenance.USER_CONFIRMED, schema_provider=provider).workflow.nodes["1"].inputs["value"] == 23


def test_receipt_write_failure_removes_temporary_file(tmp_path: Path, monkeypatch) -> None:
    import importlib

    from vibecomfy.commands._astrid_workflows import save_receipt

    adapter = importlib.import_module("vibecomfy.commands._astrid_workflows")
    root = tmp_path / "receipts"
    monkeypatch.setattr(adapter, "receipt_root", lambda: root)

    def fail_replace(_source, _destination):
        raise OSError("injected receipt publication failure")

    monkeypatch.setattr(adapter.os, "replace", fail_replace)
    try:
        save_receipt({"task_id": "task-cleanup", "transition_kind": "origin"})
    except OSError as exc:
        assert "injected receipt publication failure" in str(exc)
    else:  # pragma: no cover - assertion clarity
        raise AssertionError("injected failure should escape")
    assert list(root.iterdir()) == []
