from __future__ import annotations

import sys
import types
from pathlib import Path

from vibecomfy.commands import runpod


def test_vibecomfy_runpod_command_uses_lifecycle_shared_env_loader(
    monkeypatch, tmp_path: Path
) -> None:
    root = tmp_path / "runpod-lifecycle"
    root.mkdir()
    loader_calls: list[Path] = []
    command_calls: list[list[str]] = []

    package = types.ModuleType("runpod_lifecycle")
    package.__path__ = []
    config = types.ModuleType("runpod_lifecycle.config")
    config.load_runpod_env = lambda path: loader_calls.append(Path(path))
    cli = types.ModuleType("runpod_lifecycle.cli")
    cli.main = lambda argv: command_calls.append(list(argv)) or 17
    monkeypatch.setitem(sys.modules, "runpod_lifecycle", package)
    monkeypatch.setitem(sys.modules, "runpod_lifecycle.config", config)
    monkeypatch.setitem(sys.modules, "runpod_lifecycle.cli", cli)
    monkeypatch.setattr(runpod, "_runpod_lifecycle_root", lambda: root)

    result = runpod._runpod_lifecycle_main(["list", "--json"])

    assert result == 17
    assert loader_calls == [root / ".env"]
    assert command_calls == [["list", "--json"]]
