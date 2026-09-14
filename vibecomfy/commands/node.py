"""Inspect one ComfyUI node schema and its available Python implementation."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from vibecomfy.schema import SchemaIndexError, SchemaProviderError, get_authoring_schema_provider


def _error(args: argparse.Namespace, code: str, message: str) -> int:
    if args.json:
        print(json.dumps({"error": code, "class_type": args.class_type, "message": message}, indent=2))
    else:
        print(message, file=sys.stderr)
    return 1


def _input_payload(spec: Any) -> dict[str, Any]:
    return {
        "type": getattr(spec, "type", None),
        "required": bool(getattr(spec, "required", False)),
        "default": getattr(spec, "default", None),
        "choices": getattr(spec, "choices", None),
        "unresolved_choices": bool(getattr(spec, "unresolved_choices", False)),
        "asset_kind": getattr(spec, "asset_kind", None),
        "min": getattr(spec, "min", None),
        "max": getattr(spec, "max", None),
    }


def _schema_payload(schema: Any) -> dict[str, Any]:
    return {
        "identity": {"class_type": schema.class_type, "pack": schema.pack},
        "provenance": {
            key: getattr(schema, key, None)
            for key in (
                "source_provider", "source_path", "source_cache_path",
                "source_server_url", "source_package", "source_version",
                "source_hash", "confidence", "conflicts", "ignored_evidence",
            )
        },
        "inputs": {
            name: _input_payload(spec)
            for name, spec in (schema.inputs or {}).items()
        },
        "outputs": [
            {
                "name": getattr(spec, "name", None),
                "type": getattr(spec, "type", None),
                "is_list": bool(
                    index < len(getattr(schema, "output_is_list", ()))
                    and schema.output_is_list[index]
                ),
            }
            for index, spec in enumerate(schema.outputs or [])
        ],
    }


def _render_text(
    payload: dict[str, Any], source: Any, selected: set[str], *, filtered: bool
) -> str:
    identity = payload["identity"]
    provenance = payload["provenance"]
    rows = [f"Node: {identity['class_type']}"]
    if not filtered:
        rows.append(f"Pack: {identity['pack'] or 'unknown'}")
        known = {
            name: value for name, value in provenance.items()
            if value is not None and value != "" and value != () and value != []
        }
        if known:
            rows.append("Provenance:")
            for name, value in known.items():
                if isinstance(value, (tuple, list)):
                    value = ", ".join(str(item) for item in value)
                rows.append(f"  {name.replace('_', ' ')}: {value}")

    if "inputs" in selected:
        rows.append("Inputs:")
        if not payload["inputs"]:
            rows.append("  (none)")
        for name, spec in payload["inputs"].items():
            tags = ["required" if spec["required"] else "optional"]
            if spec["default"] is not None:
                tags.append(f"default={spec['default']!r}")
            if spec["choices"] is not None:
                tags.append(f"choices={spec['choices']!r}")
            elif spec["unresolved_choices"]:
                tags.append("choices=unresolved")
            bounds = [f"{bound}={spec[bound]}" for bound in ("min", "max") if spec[bound] is not None]
            if bounds:
                tags.append("range " + ", ".join(bounds))
            rows.append(f"  {name}: {spec['type'] or 'unknown'} ({'; '.join(tags)})")

    if "outputs" in selected:
        rows.append("Outputs:")
        if not payload["outputs"]:
            rows.append("  (none)")
        for index, output in enumerate(payload["outputs"]):
            name = output["name"] or str(index)
            rows.append(f"  {name}: {output['type'] or 'unknown'}")

    if "source" in selected:
        if getattr(source, "available", False):
            rows.extend((f"Implementation source: {source.path}", f"Class: {source.class_name or identity['class_type']}", "", source.source.rstrip()))
        else:
            rows.append(f"Implementation source unavailable: {getattr(source, 'reason', None) or 'not found'}")
    return "\n".join(rows)


def _cmd_node(args: argparse.Namespace) -> int:
    try:
        provider = get_authoring_schema_provider(object_info_cache_path=args.object_info_cache)
        schema = provider.get_schema(args.class_type)
    except (SchemaIndexError, SchemaProviderError, OSError, ValueError) as exc:
        return _error(args, "schema_load_failed", f"Could not load schema for {args.class_type!r}: {exc}")
    if schema is None:
        message = (
            f"Node {args.class_type!r} was not found. Look it up with `vibecomfy nodes list` "
            "and sync sources or provide an object-info cache if needed."
        )
        return _error(args, "node_not_found", message)

    payload = _schema_payload(schema)
    selected = {name for name in ("inputs", "outputs", "source") if getattr(args, name)}
    filtered = bool(selected)
    if not filtered:
        selected = {"inputs", "outputs", "source"}
    source = None
    if "source" in selected:
        from vibecomfy.node_source import NodeSourceResult, lookup_node_source
        try:
            source = lookup_node_source(args.class_type, schema)
        except Exception as exc:
            source = NodeSourceResult(
                source=None,
                path=None,
                class_name=None,
                reason=f"Could not inspect local source: {type(exc).__name__}: {exc}",
            )
    if args.json:
        result = {key: value for key, value in payload.items() if key in {"identity", "provenance", *selected}}
        if filtered:
            result = {key: value for key, value in result.items() if key in {"identity", *selected}}
        if "source" in selected:
            result["source"] = {
                "available": bool(getattr(source, "available", False)),
                "path": getattr(source, "path", None),
                "class_name": getattr(source, "class_name", None),
                "reason": getattr(source, "reason", None),
                "code": getattr(source, "source", None),
            }
        print(json.dumps(result, indent=2, sort_keys=True, default=str))
    else:
        print(_render_text(payload, source, selected, filtered=filtered))
    return 1 if args.source and not getattr(source, "available", False) else 0


def register(subparsers) -> None:
    parser = subparsers.add_parser(
        "node",
        help="Inspect one node's schema and Python implementation.",
        description=(
            "Show a node's identity, pack, provenance, complete input and output schema, "
            "and available local implementation source. Source lookup reads local Python files "
            "without importing custom-node code. Use `vibecomfy nodes list` to find a class name."
        ),
        epilog=(
            "Examples:\n"
            "  vibecomfy node KSampler\n"
            "  vibecomfy node KSampler --inputs --outputs\n"
            "  vibecomfy node KSampler --source --json\n"
            "\n"
            "If implementation source is unavailable, the default command still shows the node "
            "schema. An explicit --source request exits with status 1 when source is unavailable."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("class_type", help="ComfyUI class type, for example KSampler")
    parser.add_argument("--inputs", action="store_true", help="Show input definitions")
    parser.add_argument("--outputs", action="store_true", help="Show named outputs and socket types")
    parser.add_argument(
        "--source", action="store_true",
        help="Show locally available Python implementation source (exit 1 if unavailable)",
    )
    parser.add_argument("--json", action="store_true", help="Emit the selected sections as JSON")
    parser.add_argument("--object-info-cache", help="Use a captured ComfyUI /object_info JSON file")
    parser.set_defaults(func=_cmd_node)
