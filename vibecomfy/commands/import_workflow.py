"""Import a ComfyUI workflow as an inspectable VibeComfy work folder."""
from __future__ import annotations

import argparse
import contextlib
import io
import json
import os
import re
import shlex
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any


def _folder_name(source: Path) -> str:
    """Make a predictable, portable folder name from the source stem."""
    name = re.sub(r"[^\w.-]+", "-", source.stem, flags=re.UNICODE).strip(".-_")
    return name or "workflow"


def _convert(
    source: Path,
    python_path: Path,
    *,
    dry_run: bool,
    assume_yes: bool = False,
    non_interactive: bool = False,
    logical_source_path: Path | None = None,
    logical_workflow_id: str | None = None,
) -> tuple[int, dict[str, Any], str]:
    """Invoke the canonical port converter and capture its machine result."""
    from vibecomfy.cli import build_parser

    argv = ["port", "convert", str(source), "--out", str(python_path), "--json"]
    if assume_yes:
        argv.append("--yes")
    if non_interactive:
        argv.append("--non-interactive")
    if dry_run:
        argv.append("--dry-run")
    args = build_parser().parse_args(argv)
    if logical_source_path is not None:
        # Internal bridge to the canonical port converter: load bytes from the
        # staged source snapshot while recording their final logical location.
        args._logical_source_path = str(logical_source_path)
    if logical_workflow_id is not None:
        args._logical_workflow_id = logical_workflow_id
    stdout = io.StringIO()
    stderr = io.StringIO()
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        code = args.func(args)
    output = stdout.getvalue()
    try:
        payload = json.loads(output) if output.strip() else {}
    except json.JSONDecodeError:
        payload = {"status": "error", "message": "The converter returned an unreadable result."}
        code = code or 1
    return code, payload, stderr.getvalue()


def _emit(payload: dict[str, Any], *, json_output: bool) -> None:
    if json_output:
        print(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))
        return
    if payload.get("status") == "error":
        print(f"Import failed: {payload.get('message', 'conversion failed')}", file=sys.stderr)
        return
    if payload.get("status") == "preview":
        print(f"Would import {payload['source']} into {payload['folder']}/")
        print(f"  {payload['python']}")
        print(f"  {payload['companion']}")
        print(f"  {payload['original']}")
        return

    folder = payload["folder"]
    print(f"Imported workflow into {folder}/")
    print(f"  Edit:     {payload['python']}")
    print(f"  Metadata: {payload['companion']}")
    print(f"  Original: {payload['original']}")
    print("Edit the Python file directly, or use VibeComfy's workflow editing tools.")
    print("Explore and check it with:")
    quoted_folder = shlex.quote(folder)
    for command in ("inspect", "analyze info", "validate", "doctor"):
        print(f"  vibecomfy {command} {quoted_folder}")
    print("For node schemas and socket details: vibecomfy nodes spec <node-class>")
    print("Editing guide: https://github.com/peteromallet/VibeComfy/blob/main/docs/guides/workflow-onboarding.md")
    diagnostics = payload.get("diagnostics", [])
    if diagnostics:
        print(f"Conversion reported {len(diagnostics)} diagnostic(s); inspect the JSON result or run doctor.")


def _cmd_import(args: argparse.Namespace) -> int:
    source = Path(args.source).expanduser()
    if not source.is_file():
        payload = {"status": "error", "message": f"Source workflow is not a file: {source}"}
        _emit(payload, json_output=args.json)
        return 1

    destination = (
        Path(args.out).expanduser()
        if args.out
        else Path.cwd() / "workflows" / _folder_name(source)
    )
    if destination.is_symlink():
        payload = {"status": "error", "folder": str(destination), "message": f"Destination is a symbolic link: {destination}. Choose another directory with --out."}
        _emit(payload, json_output=args.json)
        return 1
    destination = destination.resolve()
    python_path = destination / "workflow.py"
    companion_path = destination / "workflow.vibe.json"
    original_path = destination / "source.json"

    if destination.exists():
        payload = {
            "status": "error",
            "folder": str(destination),
            "message": f"Destination already exists: {destination}. Choose another directory with --out.",
        }
        _emit(payload, json_output=args.json)
        return 1

    if args.dry_run:
        try:
            code, converted, stderr = _convert(
                source,
                python_path,
                dry_run=True,
                assume_yes=bool(getattr(args, "assume_yes", False)),
                non_interactive=bool(getattr(args, "non_interactive", False)),
                logical_source_path=Path("source.json"),
                logical_workflow_id=_folder_name(source),
            )
        except Exception as exc:
            _emit({"status": "error", "folder": str(destination), "message": str(exc)}, json_output=args.json)
            return 1
        if code:
            message = converted.get("message") or stderr.strip() or "conversion preflight failed"
            _emit({"status": "error", "folder": str(destination), "message": message, "conversion": converted}, json_output=args.json)
            return code
        _emit({
            "status": "preview",
            "source": str(source.absolute()),
            "folder": str(destination),
            "python": str(python_path),
            "companion": str(companion_path),
            "original": str(original_path),
            "conversion": converted,
        }, json_output=args.json)
        return 0

    parent = destination.parent
    try:
        parent.mkdir(parents=True, exist_ok=True)
        if destination.exists():
            raise FileExistsError(f"Destination already exists: {destination}")
        staging = Path(tempfile.mkdtemp(prefix=f".{destination.name}.import-", dir=parent))
    except OSError as exc:
        _emit({"status": "error", "folder": str(destination), "message": str(exc)}, json_output=args.json)
        return 1

    try:
        # Archive the exact bytes that will be converted. The converter reads
        # this staged copy, so provenance hash and source.json cannot diverge.
        staged_source = staging / "source.json"
        shutil.copyfile(source, staged_source)
        staged_python = staging / "workflow.py"
        code, converted, stderr = _convert(
            staged_source,
            staged_python,
            dry_run=False,
            assume_yes=bool(getattr(args, "assume_yes", False)),
            non_interactive=bool(getattr(args, "non_interactive", False)),
            logical_source_path=Path("source.json"),
            logical_workflow_id=_folder_name(source),
        )
        if code:
            message = converted.get("message") or stderr.strip() or "conversion failed"
            raise RuntimeError(message)
        staged_companion = staging / "workflow.vibe.json"
        if not staged_python.is_file() or not staged_companion.is_file():
            raise RuntimeError("converter did not produce both workflow.py and workflow.vibe.json")
        # Same-parent rename makes the complete folder visible at once.
        if destination.exists():
            raise FileExistsError(f"Destination already exists: {destination}. Choose another directory with --out.")
        os.rename(staging, destination)
    except Exception as exc:
        shutil.rmtree(staging, ignore_errors=True)
        _emit({"status": "error", "folder": str(destination), "message": str(exc), "conversion": converted if "converted" in locals() else {}}, json_output=args.json)
        return 1

    # Replace staging paths in the child result so machine consumers never see
    # an implementation directory that disappeared during publication.
    staging_prefix = str(staging)

    def replace_path(value: Any) -> Any:
        if isinstance(value, str):
            if value == staging_prefix or value.startswith(staging_prefix + os.sep):
                return str(destination) + value[len(staging_prefix):]
            return value
        if isinstance(value, list):
            return [replace_path(item) for item in value]
        if isinstance(value, dict):
            return {key: replace_path(item) for key, item in value.items()}
        return value

    converted = replace_path(converted)
    report = converted.get("report", {})
    diagnostics = (
        report.get("diagnostics", report.get("issues", []))
        if isinstance(report, dict)
        else []
    )
    _emit({
        "status": "ok",
        "source": str(source.absolute()),
        "folder": str(destination),
        "python": str(python_path),
        "companion": str(companion_path),
        "original": str(original_path),
        "diagnostics": diagnostics if isinstance(diagnostics, list) else [],
        "conversion": converted,
    }, json_output=args.json)
    return 0


def register(subparsers) -> None:
    parser = subparsers.add_parser(
        "import",
        help="Import a ComfyUI workflow into an editable, inspectable folder.",
        description=(
            "Import a ComfyUI workflow into ./workflows/<name>/ with an editable Python\n"
            "workflow, its VibeComfy companion metadata, and an unchanged source copy."
        ),
        epilog=(
            "Edit workflow.py, then use 'vibecomfy validate <folder>'. "
            "Use 'vibecomfy inspect <folder>' to explore the graph and "
            "'vibecomfy nodes spec <ClassType>' for node inputs and sockets."
        ),
    )
    parser.add_argument("source", help="Source ComfyUI workflow JSON file.")
    parser.add_argument("--out", help="Destination directory (defaults to ./workflows/<source-name>/).")
    parser.add_argument("--dry-run", action="store_true", help="Check and preview the import without writing files.")
    parser.add_argument("--json", action="store_true", help="Print a machine-readable result.")
    parser.set_defaults(func=_cmd_import)
