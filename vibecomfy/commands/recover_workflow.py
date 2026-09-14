"""Recover a settled Astrid workflow result without admitting a second task."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Mapping


def _cmd_recover(args: argparse.Namespace) -> int:
    from vibecomfy.commands._astrid_workflows import (
        AstridWorkflowError,
        _data,
        digest_bytes,
        download_outputs,
        materialize_outputs,
        open_client,
        read_receipt,
        report_for_outputs,
        save_receipt,
        task_workflow_context,
        wait_for_task,
    )

    try:
        receipt = read_receipt(args.task_id)
        if receipt is None and not args.out:
            raise AstridWorkflowError(
                f"no local recovery receipt exists for {args.task_id}; pass --out so recovery never guesses a local write target"
            )
        client = open_client()
        task = _data(client.tasks.show(args.task_id), action=f"read task {args.task_id}")
        state = str(task.get("state", "") if isinstance(task, Mapping) else getattr(task, "state", "")).lower()
        if state not in {"succeeded", "completed"}:
            task = wait_for_task(client, args.task_id)
        if receipt is None:
            context = task_workflow_context(task, args.task_id)
            receipt = {
                "schema_version": 1,
                "task_id": args.task_id,
                **context,
                "target_path": str(Path(args.out).expanduser().resolve()),
                "separate_output": True,
                "outputs": {},
                "report_digest": None,
            }
        _task_id, outputs, manifest = download_outputs(
            client,
            task,
            expected_names={"python", "companion", "source", "report"},
        )
        transition_kind = str(receipt.get("transition_kind") or "")
        report = report_for_outputs(
            outputs,
            manifest,
            workflow_id=str(receipt.get("workflow_id") or ""),
            transition_kind=transition_kind,
            parent_revision=receipt.get("parent_revision"),
            parent_task_id=receipt.get("parent_task_id"),
            origin_task_id=receipt.get("origin_task_id"),
        )

        expected_outputs = {
            "workflow.py": manifest["python"],
            "workflow.vibe.json": manifest["companion"],
            "source.json": manifest["source"],
        }
        receipt_target = receipt.get("target_path")
        if not args.out and not isinstance(receipt_target, str):
            raise AstridWorkflowError("local recovery receipt has no destination; pass --out")
        target = Path(args.out).expanduser().resolve() if args.out else Path(receipt_target).expanduser()

        # A repeat recovery after a successful materialization is a read-only
        # acknowledgement. The original operation is never re-admitted.
        from vibecomfy.commands.edit import _read_members

        already_materialized = False
        try:
            _python, members, _digests = _read_members(target)
            already_materialized = all(
                digest_bytes(members[name]) == expected_outputs[name]
                for name in expected_outputs
            )
        except (OSError, ValueError):
            pass
        if already_materialized:
            status = "already_materialized"
            destination = target
        else:
            expected_local = None
            if not args.out and not receipt.get("separate_output"):
                raw_precondition = receipt.get("materialize_precondition")
                if isinstance(raw_precondition, Mapping):
                    expected_local = {
                        name: value.removeprefix("sha256:") if isinstance(value, str) else value
                        for name, value in raw_precondition.items()
                    }
                elif receipt.get("transition_kind") != "origin":
                    raise AstridWorkflowError(
                        "recovery receipt lacks a safe local-parent check; use `--out` to preserve the settled branch"
                    )
                # Origins and first writes have no existing local parent.
            destination = materialize_outputs(outputs, target, expected_members=expected_local)
            status = "recovered"

        receipt["outputs"] = expected_outputs
        receipt["report_digest"] = manifest["report"]
        receipt["revision_id"] = report.get("revision_id")
        if args.out:
            receipt["recovered_to"] = str(destination)
        else:
            receipt["target_path"] = str(destination)
            receipt["materialized"] = True
        try:
            save_receipt(receipt)
            receipt_persisted = True
        except Exception:
            # Publication is already complete. The returned task ID and this
            # command remain sufficient to repeat/verify recovery.
            receipt_persisted = False
        payload = {
            "status": status,
            "task_id": args.task_id,
            "transition_kind": transition_kind,
            "workflow_id": receipt.get("workflow_id"),
            "revision_id": report.get("revision_id"),
            "report_digest": manifest["report"],
            "folder": str(destination),
            "members": expected_outputs,
            "re_admitted": False,
            "receipt_persisted": receipt_persisted,
            "next": {
                "validate": f"vibecomfy validate {destination}",
                "history": f"astrid tasks show {args.task_id}; astrid tasks events {args.task_id}",
            },
        }
    except Exception as exc:
        payload = {"status": "error", "message": f"{type(exc).__name__}: {exc}"}
        if args.json:
            print(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))
        else:
            print(f"Recovery failed: {payload['message']}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))
    else:
        print(f"{payload['status']}: {payload['folder']}")
        print(f"  task: {payload['task_id']} (no new task admitted)")
        print(f"  report digest: {payload['report_digest']}")
        print(f"  validate: {payload['next']['validate']}")
        print(f"  history: {payload['next']['history']}")
    return 0


def register(subparsers) -> None:
    parser = subparsers.add_parser(
        "recover",
        help="Materialize an already-settled Astrid workflow task by ID.",
        description=(
            "Recover exact settled outputs from an existing Astrid task. This only reads the task and its output objects;\n"
            "it never admits another edit. A changed local parent is preserved and requires an alternate --out path.\n"
            "If the original local receipt could not be written, pass the --out path shown by the failed import/edit command."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("task_id", help="Task ID printed by tracked import/edit output or its post-admission error.")
    parser.add_argument("--out", help="Write a separate recovered bundle if the original parent changed.")
    parser.add_argument("--json", action="store_true", help="Emit a machine-readable result.")
    parser.set_defaults(func=_cmd_recover)


__all__ = ["register"]
