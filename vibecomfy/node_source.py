"""Read the local Python implementation behind a ComfyUI node class type.

This module deliberately uses file reads and Python's AST only. It never imports
custom-node code, runs ``INPUT_TYPES``, starts ComfyUI, or downloads a source
package. A cached/object-info schema is evidence about node shape, not source;
the implementation is returned only when a matching local class definition is
found unambiguously.
"""

from __future__ import annotations

import ast
import importlib.util
import os
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class NodeSourceResult:
    """Source evidence for a registered node, or why it is unavailable."""

    source: str | None
    path: str | None
    class_name: str | None
    reason: str | None

    @property
    def available(self) -> bool:
        return self.source is not None


def lookup_node_source(
    class_type: str,
    schema: object,
    *,
    search_roots: Sequence[str | Path] | None = None,
) -> NodeSourceResult:
    """Find and return the actual local class implementation for *class_type*.

    ``schema.source_path`` is tried first when it points to Python source. When
    it points at a cache, index, or generated wrapper, it is ignored as source
    and the configured ComfyUI/custom-node roots are searched. Static
    ``NODE_CLASS_MAPPINGS`` aliases (for example ``"easy int" -> Int``) are
    followed without evaluating imports or expressions.
    """

    class_type = str(class_type)
    preferred = _schema_source_path(schema)
    if preferred is not None:
        result = _read_candidate(preferred, class_type)
        if result is not None:
            return result

    roots = _source_roots(search_roots)
    package = _schema_text(schema, "source_package") or _schema_text(schema, "pack")
    candidates: list[tuple[Path, ast.ClassDef, str, bool]] = []
    parse_failures: list[Path] = []
    scanned = 0
    max_files = 5_000

    # Reuse the schema provider's bounded lexical discovery. It only reads
    # source text and avoids importing custom nodes.
    try:
        from vibecomfy.schema.provider import _candidate_python_files

        files = _candidate_python_files(
            roots,
            class_type,
            max_files_per_root=2_000,
            max_total_files=max_files,
        )
    except Exception:
        files = _fallback_candidates(roots, class_type, max_files=max_files)

    for path in files:
        if scanned >= max_files:
            break
        scanned += 1
        if _is_generated_wrapper(path):
            continue
        try:
            text = path.read_text(encoding="utf-8")
            tree = ast.parse(text, filename=str(path))
        except (OSError, UnicodeError, SyntaxError):
            parse_failures.append(path)
            continue
        for cls, name, registered in _matching_classes(tree, class_type):
            candidates.append((path, cls, name, registered))
        candidates.extend(
            _registered_import_classes(path, tree, class_type, roots, seen=set(), depth=0)
        )

    registered_candidates = [candidate for candidate in candidates if candidate[3]]
    if registered_candidates:
        candidates = registered_candidates

    if package:
        package_matches = [item for item in candidates if _matches_package(item[0], package)]
        if package_matches:
            candidates = package_matches

    # Deduplicate discoveries that arise through several static registration
    # assignments in one module.
    unique: dict[tuple[str, int, str], tuple[Path, ast.ClassDef, str, bool]] = {}
    for item in candidates:
        path, cls, name, registered = item
        unique[(str(path.resolve()), cls.lineno, name)] = (path, cls, name, registered)
    candidates = list(unique.values())

    if len(candidates) == 1:
        path, cls, name, _registered = candidates[0]
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            return _unavailable("source_unreadable", f"Cannot read {path}: {exc}")
        return NodeSourceResult(_class_source(text, cls), str(path.resolve()), name, None)
    if len(candidates) > 1:
        paths = sorted({str(path.resolve()) for path, _, _, _ in candidates})
        return _unavailable(
            "ambiguous_source",
            f"Found multiple local implementations for {class_type!r}: " + ", ".join(paths),
        )
    if parse_failures:
        return _unavailable(
            "source_parse_failed",
            f"No matching class was found; {len(parse_failures)} candidate source file(s) could not be parsed",
        )
    return _unavailable(
        "source_unavailable",
        f"No local Python implementation for {class_type!r} was found in configured source roots",
    )


def _schema_text(schema: object, name: str) -> str | None:
    value = schema.get(name) if isinstance(schema, dict) else getattr(schema, name, None)
    return value.strip() if isinstance(value, str) and value.strip() else None


def _schema_source_path(schema: object) -> Path | None:
    value = _schema_text(schema, "source_path")
    if not value:
        return None
    path = Path(value).expanduser()
    if path.suffix.lower() != ".py" or not path.is_file() or _is_generated_wrapper(path):
        return None
    return path


def _source_roots(search_roots: Sequence[str | Path] | None) -> list[Path]:
    roots: list[Path] = [Path(path).expanduser() for path in search_roots or ()]
    if search_roots is None:
        try:
            # SourceSchemaProvider owns the default source roots and their
            # bounded normalization. Constructing it performs no source scan.
            from vibecomfy.schema.provider import SourceSchemaProvider

            roots.extend(SourceSchemaProvider().roots)
        except Exception:
            roots.extend((Path("custom_nodes"), Path("vendor") / "ComfyUI"))
        try:
            from vibecomfy.local_library import Slot, resolved_path

            custom_nodes = resolved_path(Slot.custom_nodes)
            if custom_nodes is not None:
                roots.append(custom_nodes)
                # Some installations configure only the custom_nodes slot.
                # Include its ComfyUI parent when it is clearly an install
                # root so core nodes.py classes remain discoverable too.
                parent = custom_nodes.parent
                if (parent / "nodes.py").is_file() and (parent / "comfy").is_dir():
                    roots.append(parent)
            # Do not import ``comfy`` to discover its installation: third-party
            # packages can run arbitrary module code at import time. Explicit
            # environment/configured paths and conventional locations suffice.
            if env_root := os.environ.get("COMFYUI_PATH"):
                comfy_root = Path(env_root).expanduser()
                if comfy_root.is_dir():
                    roots.extend((comfy_root, comfy_root / "custom_nodes"))
            # ``find_spec`` locates the installed core package without
            # executing it. ComfyUI's Python package lives under the install
            # root, alongside ``nodes.py`` and ``custom_nodes``.
            try:
                comfy_spec = importlib.util.find_spec("comfy")
                if comfy_spec and comfy_spec.origin:
                    comfy_root = Path(comfy_spec.origin).resolve().parent.parent
                    roots.extend((comfy_root, comfy_root / "custom_nodes"))
            except (ImportError, ValueError, AttributeError):
                pass
            home_comfy = Path.home() / "ComfyUI"
            if home_comfy.is_dir():
                roots.extend((home_comfy, home_comfy / "custom_nodes"))
            cwd = Path.cwd()
            if (cwd / "custom_nodes").is_dir():
                roots.extend((cwd, cwd / "custom_nodes"))
        except Exception:
            pass

    unique: list[Path] = []
    seen: set[str] = set()
    for root in roots:
        key = str(root.resolve()) if root.exists() else str(root.absolute())
        if key not in seen:
            seen.add(key)
            unique.append(root)
    return unique[:8]


def _read_candidate(path: Path, class_type: str) -> NodeSourceResult | None:
    if _is_generated_wrapper(path):
        return None
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
    except (OSError, UnicodeError, SyntaxError):
        return None
    matches = _matching_classes(tree, class_type)
    if len(matches) == 1:
        cls, name, _registered = matches[0]
        return NodeSourceResult(_class_source(text, cls), str(path.resolve()), name, None)
    if len(matches) > 1:
        return _unavailable(
            "ambiguous_source",
            f"Found multiple matching class definitions for {class_type!r} in {path}",
        )
    return None


def _matching_classes(tree: ast.Module, class_type: str) -> list[tuple[ast.ClassDef, str, bool]]:
    # ComfyUI registers module-level classes. Nested helper classes should not
    # be mistaken for node implementations merely because their names match.
    classes = [node for node in tree.body if isinstance(node, ast.ClassDef)]
    by_name: dict[str, list[ast.ClassDef]] = {}
    for node in classes:
        by_name.setdefault(node.name, []).append(node)
    registered_names: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        if not any(isinstance(target, ast.Name) and target.id == "NODE_CLASS_MAPPINGS" for target in targets):
            continue
        value = node.value
        if not isinstance(value, ast.Dict):
            continue
        for key_node, value_node in zip(value.keys, value.values):
            if not isinstance(key_node, ast.Constant) or not isinstance(key_node.value, str):
                continue
            class_name = _static_class_name(value_node)
            if key_node.value == class_type and class_name:
                registered_names.add(class_name)
    if registered_names:
        return [
            (cls, name, True)
            for name in sorted(registered_names)
            for cls in by_name.get(name, ())
        ]
    return [(cls, class_type, False) for cls in by_name.get(class_type, ())]


def _registered_import_classes(
    path: Path,
    tree: ast.Module,
    class_type: str,
    roots: Sequence[Path],
    *,
    seen: set[Path],
    depth: int,
) -> list[tuple[Path, ast.ClassDef, str, bool]]:
    """Resolve common relative imports used by pack ``__init__.py`` files."""
    if depth >= 4:
        return []
    try:
        resolved_path = path.resolve()
    except OSError:
        return []
    if resolved_path in seen:
        return []
    seen.add(resolved_path)

    wanted: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        if not any(isinstance(target, ast.Name) and target.id == "NODE_CLASS_MAPPINGS" for target in targets):
            continue
        if not isinstance(node.value, ast.Dict):
            continue
        for key_node, value_node in zip(node.value.keys, node.value.values):
            if (
                isinstance(key_node, ast.Constant)
                and key_node.value == class_type
                and isinstance(value_node, ast.Name)
            ):
                wanted.add(value_node.id)

    imports: dict[str, tuple[ast.ImportFrom, str]] = {}
    for node in tree.body:
        if not isinstance(node, ast.ImportFrom) or node.level < 1:
            continue
        for alias in node.names:
            imports[alias.asname or alias.name] = (node, alias.name)

    found: list[tuple[Path, ast.ClassDef, str, bool]] = []
    for name in wanted:
        imported = imports.get(name)
        if imported is None:
            continue
        import_node, imported_name = imported
        module_path = _relative_import_path(path, import_node)
        if module_path is None or not module_path.is_file() or _is_generated_wrapper(module_path):
            continue
        if roots and not any(_within(module_path, root) for root in roots):
            continue
        try:
            imported_text = module_path.read_text(encoding="utf-8")
            imported_tree = ast.parse(imported_text, filename=str(module_path))
        except (OSError, UnicodeError, SyntaxError):
            continue
        for cls in imported_tree.body:
            if isinstance(cls, ast.ClassDef) and cls.name == imported_name:
                found.append((module_path, cls, cls.name, True))
        found.extend(
            _registered_import_classes(
                module_path,
                imported_tree,
                imported_name,
                roots,
                seen=seen,
                depth=depth + 1,
            )
        )
    return found


def _relative_import_path(path: Path, node: ast.ImportFrom) -> Path | None:
    if node.level < 1:
        return None
    package_dir = path.parent
    for _ in range(node.level - 1):
        package_dir = package_dir.parent
    if node.module:
        package_dir = package_dir.joinpath(*node.module.split("."))
    source_path = package_dir.with_suffix(".py")
    if source_path.is_file():
        return source_path
    init_path = package_dir / "__init__.py"
    return init_path if init_path.is_file() else None


def _within(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except (OSError, ValueError):
        return False


def _static_class_name(node: ast.expr | None) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return None


def _class_source(text: str, cls: ast.ClassDef) -> str:
    lines = text.splitlines()
    start = min((decorator.lineno for decorator in cls.decorator_list), default=cls.lineno)
    return "\n".join(lines[start - 1 : cls.end_lineno]).rstrip()


def _is_generated_wrapper(path: Path) -> bool:
    parts = [part.lower() for part in path.parts]
    for index in range(len(parts) - 1):
        if parts[index] == "porting" and parts[index + 1] == "wrappers":
            return True
        if parts[index] == "vibecomfy" and parts[index + 1] == "nodes":
            return True
    return False


def _matches_package(path: Path, package: str) -> bool:
    normalized = package.lower().replace("-", "_")
    return path.stem.lower().replace("-", "_") == normalized or any(
        part.lower().replace("-", "_") == normalized for part in path.parts
    )


def _fallback_candidates(roots: Sequence[Path], class_type: str, *, max_files: int) -> list[Path]:
    candidates: list[Path] = []
    scanned = 0
    for root in roots:
        if not root.exists():
            continue
        try:
            for path in sorted(root.rglob("*.py")):
                if any(part in {".git", "__pycache__", ".venv", "venv", "node_modules"} for part in path.parts):
                    continue
                if scanned >= max_files:
                    return candidates
                scanned += 1
                try:
                    content = path.read_text(encoding="utf-8", errors="ignore")
                except OSError:
                    continue
                if f"class {class_type}" in content or f'"{class_type}"' in content or f"'{class_type}'" in content:
                    candidates.append(path)
        except OSError:
            continue
    return candidates


def _unavailable(reason: str, detail: str) -> NodeSourceResult:
    return NodeSourceResult(None, None, None, f"{reason}: {detail}")


__all__ = ["NodeSourceResult", "lookup_node_source"]
