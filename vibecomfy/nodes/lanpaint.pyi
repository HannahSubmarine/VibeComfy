# vibecomfy:generated
# pack: LanPaint
# source: object_info cache LanPaint@2.1.0.json sha256:c6f9ee4548d2
# source_sha256: 3c13d201969dc620333c5e94869f272cdb4f0316cac2bf3b704681df5d4dd1e0
# generator_version: 2.0.0
# generated_at: 1970-01-01T00:00:00+00:00
# classes: 4

"""Type stubs for generated public node wrappers."""
from __future__ import annotations

from typing import Any, Literal

from vibecomfy.workflow import VibeWorkflow

class _Omitted: ...
_UNSET: _Omitted

def LanPaint_AVDecode(
    *args: VibeWorkflow,
    _id: str | None = ...,
    audio_mask: Any | _Omitted = ...,
    audio_vae: Any | _Omitted = ...,
    mask: Any | _Omitted = ...,
    samples: Any | _Omitted = ...,
    vae: Any | _Omitted = ...,
    video: Any | _Omitted = ...,
    audio_crossfade: float | _Omitted = ...,
    blend_overlap: int | _Omitted = ...,
    pass_raw: bool = ...,
    **_extras: Any,
) -> Any: ...

def LanPaint_AVEncode(
    *args: VibeWorkflow,
    _id: str | None = ...,
    audio_mask: Any | _Omitted = ...,
    audio_vae: Any | _Omitted = ...,
    mask: Any | _Omitted = ...,
    vae: Any | _Omitted = ...,
    video: Any | _Omitted = ...,
    pass_raw: bool = ...,
    **_extras: Any,
) -> Any: ...

def LanPaint_SamplerCustomAdvanced(
    *args: VibeWorkflow,
    _id: str | None = ...,
    guider: Any | _Omitted = ...,
    latent_image: Any | _Omitted = ...,
    noise: Any | _Omitted = ...,
    sampler: Any | _Omitted = ...,
    sigmas: Any | _Omitted = ...,
    LanPaint_Info: str | _Omitted = ...,
    LanPaint_Lambda: float | _Omitted = ...,
    LanPaint_NumSteps: int | _Omitted = ...,
    LanPaint_PromptMode: Literal['Image First', 'Prompt First'] | _Omitted = ...,
    LanPaint_StepSize: float | _Omitted = ...,
    pass_raw: bool = ...,
    **_extras: Any,
) -> Any: ...

def LanPaint_VideoMaskEditor(
    *args: VibeWorkflow,
    _id: str | None = ...,
    video: Any | _Omitted = ...,
    audio_mask: str | _Omitted = ...,
    keyframes: str | _Omitted = ...,
    pass_raw: bool = ...,
    **_extras: Any,
) -> Any: ...

__all__ = ['LanPaint_AVDecode', 'LanPaint_AVEncode', 'LanPaint_SamplerCustomAdvanced', 'LanPaint_VideoMaskEditor']
