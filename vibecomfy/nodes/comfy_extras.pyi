# vibecomfy:generated
# pack: comfy_extras
# source: object_info cache comfy_extras@zz-official-6338e4bd.json sha256:637e2eb421d9
# source_sha256: e9dee0c0af25eca89856b722ffa5bc421efd2dae4f18d95ceec82d7b166dd700
# generator_version: 2.0.0
# generated_at: 1970-01-01T00:00:00+00:00
# classes: 1

"""Type stubs for generated public node wrappers."""
from __future__ import annotations

from typing import Any, Literal

from vibecomfy.workflow import VibeWorkflow

class _Omitted: ...
_UNSET: _Omitted

def MiniMaxH3ImageToVideo(
    *args: VibeWorkflow,
    _id: str | None = ...,
    clip: Any | _Omitted = ...,
    vae: Any | _Omitted = ...,
    height: int | _Omitted = ...,
    length: int | _Omitted = ...,
    prompt: str | _Omitted = ...,
    width: int | _Omitted = ...,
    first_frame: Any | _Omitted = ...,
    last_frame: Any | _Omitted = ...,
    pass_raw: bool = ...,
    **_extras: Any,
) -> Any: ...

__all__ = ['MiniMaxH3ImageToVideo']
