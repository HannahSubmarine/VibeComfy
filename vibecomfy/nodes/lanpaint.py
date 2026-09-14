# vibecomfy:generated
# pack: LanPaint
# source: object_info cache LanPaint@2.1.0.json sha256:c6f9ee4548d2
# source_sha256: 3c13d201969dc620333c5e94869f272cdb4f0316cac2bf3b704681df5d4dd1e0
# generator_version: 2.0.0
# generated_at: 1970-01-01T00:00:00+00:00
# classes: 4
#
# DO NOT EDIT — regenerate with:
#   vibecomfy nodes generate-wrappers LanPaint

"""Auto-generated public wrappers for the LanPaint custom-node pack.

Each function wraps one ComfyUI node class and delegates through the
public ``vibecomfy.templates.node`` ABI.
"""

from __future__ import annotations

from typing import Any, Literal

from vibecomfy.templates import _current_workflow_or_raise, node
from vibecomfy.workflow import VibeWorkflow

class _Omitted:
    pass

_UNSET = _Omitted()

def LanPaint_AVDecode(
    *args: VibeWorkflow,
    _id: str | None = None,
    audio_mask: Any | _Omitted = _UNSET,
    audio_vae: Any | _Omitted = _UNSET,
    mask: Any | _Omitted = _UNSET,
    samples: Any | _Omitted = _UNSET,
    vae: Any | _Omitted = _UNSET,
    video: Any | _Omitted = _UNSET,
    audio_crossfade: float | _Omitted = _UNSET,
    blend_overlap: int | _Omitted = _UNSET,
    pass_raw: bool = False,
    **_extras: Any,
) -> Any:
    """Public wrapper for the ComfyUI node ``LanPaint_AVDecode``.

    Category: video

    Decode a nested AV latent and merge the inpainted video and audio with the original.

    Returns: video, audio

    Source: object_info cache LanPaint@2.1.0.json sha256:c6f9ee4548d2
    """
    if len(args) > 1:
        raise TypeError(f"LanPaint_AVDecode() takes at most 1 positional argument, got {len(args)}")
    wf = args[0] if args else _current_workflow_or_raise()
    _kwargs: dict[str, Any] = {}
    if audio_mask is not _UNSET:
        _kwargs['audio_mask'] = audio_mask
    if audio_vae is not _UNSET:
        _kwargs['audio_vae'] = audio_vae
    if mask is not _UNSET:
        _kwargs['mask'] = mask
    if samples is not _UNSET:
        _kwargs['samples'] = samples
    if vae is not _UNSET:
        _kwargs['vae'] = vae
    if video is not _UNSET:
        _kwargs['video'] = video
    if audio_crossfade is not _UNSET:
        _kwargs['audio_crossfade'] = audio_crossfade
    if blend_overlap is not _UNSET:
        _kwargs['blend_overlap'] = blend_overlap
    _kwargs.update(_extras)
    return node(wf, 'LanPaint_AVDecode', _id, pass_raw=pass_raw, **_kwargs)

def LanPaint_AVEncode(
    *args: VibeWorkflow,
    _id: str | None = None,
    audio_mask: Any | _Omitted = _UNSET,
    audio_vae: Any | _Omitted = _UNSET,
    mask: Any | _Omitted = _UNSET,
    vae: Any | _Omitted = _UNSET,
    video: Any | _Omitted = _UNSET,
    pass_raw: bool = False,
    **_extras: Any,
) -> Any:
    """Public wrapper for the ComfyUI node ``LanPaint_AVEncode``.

    Category: video

    Encode a video's frames and audio into a nested AV latent with per-stream masks.

    Returns: latent

    Source: object_info cache LanPaint@2.1.0.json sha256:c6f9ee4548d2
    """
    if len(args) > 1:
        raise TypeError(f"LanPaint_AVEncode() takes at most 1 positional argument, got {len(args)}")
    wf = args[0] if args else _current_workflow_or_raise()
    _kwargs: dict[str, Any] = {}
    if audio_mask is not _UNSET:
        _kwargs['audio_mask'] = audio_mask
    if audio_vae is not _UNSET:
        _kwargs['audio_vae'] = audio_vae
    if mask is not _UNSET:
        _kwargs['mask'] = mask
    if vae is not _UNSET:
        _kwargs['vae'] = vae
    if video is not _UNSET:
        _kwargs['video'] = video
    _kwargs.update(_extras)
    return node(wf, 'LanPaint_AVEncode', _id, pass_raw=pass_raw, **_kwargs)

def LanPaint_SamplerCustomAdvanced(
    *args: VibeWorkflow,
    _id: str | None = None,
    guider: Any | _Omitted = _UNSET,
    latent_image: Any | _Omitted = _UNSET,
    noise: Any | _Omitted = _UNSET,
    sampler: Any | _Omitted = _UNSET,
    sigmas: Any | _Omitted = _UNSET,
    LanPaint_Info: str | _Omitted = _UNSET,
    LanPaint_Lambda: float | _Omitted = _UNSET,
    LanPaint_NumSteps: int | _Omitted = _UNSET,
    LanPaint_PromptMode: Literal['Image First', 'Prompt First'] | _Omitted = _UNSET,
    LanPaint_StepSize: float | _Omitted = _UNSET,
    pass_raw: bool = False,
    **_extras: Any,
) -> Any:
    """Public wrapper for the ComfyUI node ``LanPaint_SamplerCustomAdvanced``.

    Category: sampling/custom_sampling

    LanPaint custom sampler with advanced controls.

    Returns: output, denoised_output

    Source: object_info cache LanPaint@2.1.0.json sha256:c6f9ee4548d2
    """
    if len(args) > 1:
        raise TypeError(f"LanPaint_SamplerCustomAdvanced() takes at most 1 positional argument, got {len(args)}")
    wf = args[0] if args else _current_workflow_or_raise()
    _kwargs: dict[str, Any] = {}
    if guider is not _UNSET:
        _kwargs['guider'] = guider
    if latent_image is not _UNSET:
        _kwargs['latent_image'] = latent_image
    if noise is not _UNSET:
        _kwargs['noise'] = noise
    if sampler is not _UNSET:
        _kwargs['sampler'] = sampler
    if sigmas is not _UNSET:
        _kwargs['sigmas'] = sigmas
    if LanPaint_Info is not _UNSET:
        _kwargs['LanPaint_Info'] = LanPaint_Info
    if LanPaint_Lambda is not _UNSET:
        _kwargs['LanPaint_Lambda'] = LanPaint_Lambda
    if LanPaint_NumSteps is not _UNSET:
        _kwargs['LanPaint_NumSteps'] = LanPaint_NumSteps
    if LanPaint_PromptMode is not _UNSET:
        _kwargs['LanPaint_PromptMode'] = LanPaint_PromptMode
    if LanPaint_StepSize is not _UNSET:
        _kwargs['LanPaint_StepSize'] = LanPaint_StepSize
    _kwargs.update(_extras)
    return node(wf, 'LanPaint_SamplerCustomAdvanced', _id, pass_raw=pass_raw, **_kwargs)

def LanPaint_VideoMaskEditor(
    *args: VibeWorkflow,
    _id: str | None = None,
    video: Any | _Omitted = _UNSET,
    audio_mask: str | _Omitted = _UNSET,
    keyframes: str | _Omitted = _UNSET,
    pass_raw: bool = False,
    **_extras: Any,
) -> Any:
    """Public wrapper for the ComfyUI node ``LanPaint_VideoMaskEditor``.

    Category: video

    Loads a video and outputs video and audio inpainting masks.

    Returns: video, mask, audio_mask

    Source: object_info cache LanPaint@2.1.0.json sha256:c6f9ee4548d2
    """
    if len(args) > 1:
        raise TypeError(f"LanPaint_VideoMaskEditor() takes at most 1 positional argument, got {len(args)}")
    wf = args[0] if args else _current_workflow_or_raise()
    _kwargs: dict[str, Any] = {}
    if video is not _UNSET:
        _kwargs['video'] = video
    if audio_mask is not _UNSET:
        _kwargs['audio_mask'] = audio_mask
    if keyframes is not _UNSET:
        _kwargs['keyframes'] = keyframes
    _kwargs.update(_extras)
    return node(wf, 'LanPaint_VideoMaskEditor', _id, pass_raw=pass_raw, **_kwargs)

__all__ = ['LanPaint_AVDecode', 'LanPaint_AVEncode', 'LanPaint_SamplerCustomAdvanced', 'LanPaint_VideoMaskEditor']
__vibecomfy_class_types__ = {'LanPaint_AVDecode': 'LanPaint_AVDecode', 'LanPaint_AVEncode': 'LanPaint_AVEncode', 'LanPaint_SamplerCustomAdvanced': 'LanPaint_SamplerCustomAdvanced', 'LanPaint_VideoMaskEditor': 'LanPaint_VideoMaskEditor'}
