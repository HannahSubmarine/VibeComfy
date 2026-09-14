"""Optional Astrid task adapter for tracked VibeComfy workflow transitions.

Local VibeComfy remains independent of Astrid. This module is imported only
when a user explicitly supplies ``--project`` or asks to recover a task.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import tempfile
import time
from pathlib import Path
from typing import Any, Mapping


class AstridWorkflowError(RuntimeError):
    """A tracked workflow operation could not be admitted or recovered."""


def _value(value: Any, key: str, default: Any = None) -> Any:
    if isinstance(value, Mapping):
        return value.get(key, default)
    return getattr(value, key, default)


def _data(result: Any, *, action: str) -> Any:
    if hasattr(result, "ok"):
        if not result.ok:
            error = getattr(result, "error", None)
            message = _value(error, "message", None) or str(error or "request failed")
            raise AstridWorkflowError(f"Astrid {action} failed: {message}")
        return result.data
    if isinstance(result, Mapping) and result.get("ok") is False:
        error = result.get("error")
        raise AstridWorkflowError(f"Astrid {action} failed: {_value(error, 'message', error)}")
    if isinstance(result, Mapping) and "data" in result:
        return result["data"]
    return result


def open_client() -> Any:
    """Open the optional public SDK at its explicit launcher boundary."""
    try:
        from astrid.sdk.client import AstridClient
    except ImportError as exc:
        raise AstridWorkflowError(
            "Astrid tracking needs Astrid's Python SDK in this environment; local commands do not."
        ) from exc
    try:
        return AstridClient.open_from_launcher(start_pack_host=True)
    except Exception as exc:
        raise AstridWorkflowError(f"could not connect to Astrid: {exc}") from exc


def resolve_project(client: Any, project: str) -> str:
    """Resolve a project ID or slug without silently selecting/creating one."""
    direct = client.projects.show(project)
    if getattr(direct, "ok", False):
        data = _data(direct, action="project lookup")
        resolved = _value(data, "project_id") or _value(data, "id")
        if resolved:
            return str(resolved)

    listing = _data(client.projects.list(), action="project listing")
    rows = listing
    if isinstance(listing, (list, tuple)) and len(listing) == 2 and isinstance(listing[0], list):
        rows = listing[0]
    if isinstance(rows, list):
        for row in rows:
            if str(_value(row, "slug", "")) == project or str(_value(row, "project_id", "")) == project:
                resolved = _value(row, "project_id") or _value(row, "id")
                if resolved:
                    return str(resolved)
    raise AstridWorkflowError(f"Astrid project {project!r} was not found; pass an existing project ID or slug")


def digest_bytes(payload: bytes) -> str:
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def upload_bytes(
    client: Any,
    project_id: str,
    name: str,
    payload: bytes,
    *,
    key: str,
    filename: str | None = None,
) -> dict[str, str]:
    """Upload an immutable member and verify Astrid stored the exact bytes."""
    suffix = Path(name).suffix or ".bin"
    with tempfile.TemporaryDirectory(prefix="vibecomfy-astrid-input-") as temporary:
        path = Path(temporary) / (filename or Path(name).name or f"member{suffix}")
        path.write_bytes(payload)
        result = _data(
            client.media.import_file(project=project_id, path=path, idempotency_key=key),
            action=f"upload {name}",
        )
    object_id = _value(result, "object_id")
    digest = _value(result, "digest")
    if not isinstance(object_id, str) or not object_id or not isinstance(digest, str):
        raise AstridWorkflowError(f"Astrid upload for {name} did not return an object ID and digest")
    if digest != digest_bytes(payload):
        raise AstridWorkflowError(f"Astrid stored different bytes for {name}; expected {digest_bytes(payload)}, got {digest}")
    return {"name": name, "object_id": object_id, "digest": digest}


def _stable_key(prefix: str, value: Mapping[str, Any]) -> str:
    canonical = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return prefix + hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def create_task(
    client: Any,
    *,
    project_id: str,
    capability: str,
    workflow_id: str,
    transition_kind: str,
    uploads: list[dict[str, str]],
    idempotency_key: str,
    parent_revision: str | None = None,
    parent_task_id: str | None = None,
    origin_task_id: str | None = None,
    extra_inputs: Mapping[str, Any] | None = None,
) -> str:
    inputs = {
        "workflow_id": workflow_id,
        "transition_kind": transition_kind,
        **dict(extra_inputs or {}),
    }
    if parent_revision is not None:
        inputs["parent_revision"] = parent_revision
    if parent_task_id is not None:
        inputs["parent_task_id"] = parent_task_id
    if origin_task_id is not None:
        inputs["origin_task_id"] = origin_task_id
    input_digests = [{"name": item["name"], "digest": item["digest"]} for item in uploads]
    spec = {
        "inputs": inputs,
        "input_digests": input_digests,
        "transition_kind": transition_kind,
        "parent_task_id": parent_task_id,
        "origin_task_id": origin_task_id,
    }
    admitted = _data(
        client.tasks.create(
            project_id=project_id,
            capability=capability,
            spec=spec,
            input_manifest=[item["object_id"] for item in uploads],
            idempotency_key=idempotency_key,
        ),
        action=f"admit {transition_kind} task",
    )
    task_id = _value(admitted, "task_id")
    if not isinstance(task_id, str) or not task_id:
        raise AstridWorkflowError("Astrid admitted the task without returning a task ID")
    return task_id


def wait_for_task(client: Any, task_id: str, *, timeout_seconds: float = 90.0) -> dict[str, Any]:
    """Poll an admitted task; timeout is recoverable and never re-admits."""
    deadline = time.monotonic() + timeout_seconds
    delay = 0.2
    while True:
        task = _data(client.tasks.show(task_id), action=f"read task {task_id}")
        state = str(_value(task, "state", "unknown")).lower()
        if state in {"succeeded", "completed"}:
            return dict(task) if isinstance(task, Mapping) else vars(task)
        if state in {"failed", "cancelled", "rejected", "expired"}:
            raise AstridWorkflowError(
                f"Astrid task {task_id} ended {state}; inspect it with `astrid tasks show {task_id}` and `astrid tasks events {task_id}`"
            )
        if time.monotonic() >= deadline:
            raise AstridWorkflowError(
                f"Astrid task {task_id} is still {state}; continue with `vibecomfy recover {task_id}` (this does not admit another task)"
            )
        time.sleep(delay)
        delay = min(delay * 1.5, 2.0)


def download_outputs(client: Any, task: Mapping[str, Any], *, expected_names: set[str]) -> tuple[str, dict[str, bytes], dict[str, str]]:
    task_id = str(_value(task, "task_id", ""))
    result = _value(task, "result")
    outputs = _value(result, "outputs")
    if not isinstance(outputs, list):
        raise AstridWorkflowError(f"completed Astrid task {task_id} has no settled output manifest")
    manifests: dict[str, str] = {}
    bytes_by_name: dict[str, bytes] = {}
    for item in outputs:
        name = _value(item, "name")
        digest = _value(item, "digest")
        if not isinstance(name, str) or not isinstance(digest, str):
            raise AstridWorkflowError(f"task {task_id} has a malformed output manifest")
        if name in manifests:
            raise AstridWorkflowError(f"task {task_id} repeats output name {name!r}")
        manifests[name] = digest
        if name not in expected_names:
            continue
        payload = _data(client.media.read_bytes(digest), action=f"download {name} from task {task_id}")
        if not isinstance(payload, bytes) or digest_bytes(payload) != digest:
            raise AstridWorkflowError(f"downloaded output {name} from task {task_id} does not match settled digest {digest}")
        bytes_by_name[name] = payload
    missing = expected_names - bytes_by_name.keys()
    if missing:
        raise AstridWorkflowError(f"completed task {task_id} is missing required outputs: {', '.join(sorted(missing))}")
    return task_id, bytes_by_name, manifests


def receipt_root() -> Path:
    return Path.home() / ".vibecomfy" / "workflow-task-receipts"


def save_receipt(receipt: Mapping[str, Any]) -> Path:
    task_id = str(receipt.get("task_id", ""))
    if not task_id or any(ch not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_." for ch in task_id):
        raise AstridWorkflowError("task ID is not safe to use as a local receipt name")
    root = receipt_root()
    root.mkdir(parents=True, exist_ok=True)
    destination = root / f"{task_id}.json"
    fd, raw = tempfile.mkstemp(prefix=f".{task_id}.", suffix=".tmp", dir=root)
    temporary = Path(raw)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(dict(receipt), handle, indent=2, sort_keys=True, ensure_ascii=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, destination)
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass
    return destination


def read_receipt(task_id: str) -> dict[str, Any] | None:
    path = receipt_root() / f"{task_id}.json"
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) and value.get("task_id") == task_id else None


def find_receipt(
    *,
    project_id: str,
    workflow_id: str | None,
    member_digests: Mapping[str, str | None],
    allow_python_mismatch: bool = False,
) -> dict[str, Any] | None:
    """Find an exact prior tracked parent by project, identity and digests."""
    root = receipt_root()
    try:
        files = sorted(root.glob("*.json"), key=lambda path: path.stat().st_mtime_ns, reverse=True)
    except OSError:
        return None
    matches: list[dict[str, Any]] = []
    for path in files:
        try:
            item = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if (
            not isinstance(item, dict)
            or item.get("project_id") != project_id
            or (workflow_id is not None and item.get("workflow_id") != workflow_id)
        ):
            continue
        outputs = item.get("outputs")
        if not isinstance(outputs, Mapping):
            continue
        expected_keys = ("workflow.vibe.json", "source.json")
        if any(outputs.get(key) != member_digests.get(key) for key in expected_keys):
            continue
        if not allow_python_mismatch and outputs.get("workflow.py") != member_digests.get("workflow.py"):
            continue
        matches.append(item)
    return matches[0] if matches else None


def stable_idempotency_key(prefix: str, request: Mapping[str, Any]) -> str:
    return _stable_key(prefix, request)


def report_for_outputs(
    outputs: Mapping[str, bytes],
    manifest: Mapping[str, str],
    *,
    workflow_id: str,
    transition_kind: str,
    parent_revision: str | None,
    parent_task_id: str | None,
    origin_task_id: str | None,
) -> dict[str, Any]:
    """Validate and decode the report included in a settled transition."""
    required = {"python", "companion", "source", "report"}
    if set(outputs) != required:
        raise AstridWorkflowError("settled transition must provide python, companion, source, and report outputs")
    try:
        report = json.loads(outputs["report"].decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise AstridWorkflowError(f"settled edit-report.json is not valid UTF-8 JSON: {exc}") from exc
    if not isinstance(report, dict):
        raise AstridWorkflowError("settled edit-report.json must contain an object")
    if report.get("workflow_id") != workflow_id or report.get("transition_kind") != transition_kind:
        raise AstridWorkflowError("settled report does not match the admitted workflow transition")
    if report.get("parent_revision") != parent_revision:
        raise AstridWorkflowError("settled report names a different parent revision than the admitted task")
    if report.get("parent_task_id") != parent_task_id or report.get("origin_task_id") != origin_task_id:
        raise AstridWorkflowError("settled report task lineage does not match the admitted task")
    members = report.get("after", {}).get("members") if isinstance(report.get("after"), Mapping) else None
    if not isinstance(members, Mapping):
        members = report.get("members")
    expected_member_names = {
        "python": "workflow.py",
        "companion": "workflow.vibe.json",
        "source": "source.json",
    }
    for output_name, member_name in expected_member_names.items():
        digest = manifest.get(output_name)
        if not isinstance(digest, str) or digest_bytes(outputs[output_name]) != digest:
            raise AstridWorkflowError(f"settled output digest for {output_name} is inconsistent")
        if not isinstance(members, Mapping) or members.get(member_name) != digest:
            raise AstridWorkflowError(f"settled report does not bind the exact {member_name} output")
    return report


def _workflow_python_path(reference: str | Path) -> Path:
    path = Path(reference).expanduser()
    if path.is_dir() or (not path.suffix and not path.exists()):
        return (path / "workflow.py").resolve()
    if path.suffix.lower() == ".py":
        return path.resolve()
    return (path / "workflow.py").resolve()


def materialize_outputs(
    outputs: Mapping[str, bytes],
    destination: str | Path,
    *,
    expected_members: Mapping[str, str | None] | None = None,
) -> Path:
    """Publish exact settled output bytes using VibeComfy's pair rollback.

    An empty destination is assembled in a sibling staging directory. An
    existing canonical bundle uses the existing rollback-capable pair writer;
    only the canonical Python/companion/source trio is materialized. The
    immutable report remains in Astrid and its digest is kept in the local
    recovery receipt. ``expected_members`` is a compare-and-swap digest map over current
    local members and is required for replacement.
    """
    required = {"python", "companion", "source", "report"}
    if set(outputs) != required:
        raise AstridWorkflowError("settled output members are incomplete")
    python_path = _workflow_python_path(destination)
    folder = python_path.parent
    if python_path.exists() or python_path.is_symlink():
        if expected_members is None:
            raise AstridWorkflowError(f"destination already contains a workflow: {folder}; choose a separate --out path")
        actual: dict[str, str | None] = {}
        member_paths = {
            "workflow.py": python_path,
            "workflow.vibe.json": python_path.with_suffix(".vibe.json"),
            "source.json": folder / "source.json",
        }
        for name, path in member_paths.items():
            if path.is_symlink():
                actual[name] = "<symlink>"
            else:
                try:
                    actual[name] = hashlib.sha256(path.read_bytes()).hexdigest()
                except FileNotFoundError:
                    actual[name] = None
        if any(actual.get(name) != expected for name, expected in expected_members.items()):
            raise AstridWorkflowError(
                "local workflow changed after the task was admitted; its settled result remains recoverable. "
                "Choose an explicit --out destination or run `vibecomfy recover <TASK_ID>` after resolving the local branch."
            )
        try:
            companion = json.loads(outputs["companion"].decode("utf-8"))
        except (UnicodeError, json.JSONDecodeError) as exc:
            raise AstridWorkflowError(f"settled workflow companion is not valid JSON: {exc}") from exc
        from vibecomfy.testing.canonical import canonical_json

        if canonical_json(companion).encode("utf-8") != outputs["companion"]:
            raise AstridWorkflowError("settled workflow companion is not in canonical byte form")
        from vibecomfy.workflow_bundle import _atomic_publish_pair

        _atomic_publish_pair(
            python_path,
            outputs["python"],
            companion,
            expected_members={
                member_paths[name]: value
                for name, value in expected_members.items()
            },
            extra_members={
                folder / "source.json": outputs["source"],
            },
        )
        return folder

    folder.parent.mkdir(parents=True, exist_ok=True)
    if folder.exists() or folder.is_symlink():
        raise AstridWorkflowError(f"destination already exists: {folder}; choose another directory with --out")
    staging = Path(tempfile.mkdtemp(prefix=f".{folder.name}.astrid-", dir=folder.parent))
    try:
        (staging / "workflow.py").write_bytes(outputs["python"])
        (staging / "workflow.vibe.json").write_bytes(outputs["companion"])
        (staging / "source.json").write_bytes(outputs["source"])
        if folder.exists() or folder.is_symlink():
            raise AstridWorkflowError(f"destination already exists: {folder}; choose another directory with --out")
        os.rename(staging, folder)
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise
    return folder


__all__ = [
    "AstridWorkflowError", "create_task", "digest_bytes", "download_outputs",
    "find_receipt", "open_client", "read_receipt", "resolve_project",
    "materialize_outputs", "report_for_outputs", "save_receipt",
    "stable_idempotency_key", "upload_bytes", "wait_for_task",
]
