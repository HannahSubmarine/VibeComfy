# vibecomfy:generated
# pack: comfy_extras
# source: object_info cache comfy_extras@zz-official-6338e4bd.json sha256:637e2eb421d9
# source_sha256: e9dee0c0af25eca89856b722ffa5bc421efd2dae4f18d95ceec82d7b166dd700
# generator_version: 2.0.0
# generated_at: 1970-01-01T00:00:00+00:00
# classes: 1
#
# DO NOT EDIT — regenerate with:
#   vibecomfy nodes generate-wrappers comfy_extras

"""Auto-generated public wrappers for the comfy_extras custom-node pack.

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

def MiniMaxH3ImageToVideo(
    *args: VibeWorkflow,
    _id: str | None = None,
    clip: Any | _Omitted = _UNSET,
    vae: Any | _Omitted = _UNSET,
    height: int | _Omitted = _UNSET,
    length: int | _Omitted = _UNSET,
    prompt: str | _Omitted = _UNSET,
    width: int | _Omitted = _UNSET,
    first_frame: Any | _Omitted = _UNSET,
    last_frame: Any | _Omitted = _UNSET,
    pass_raw: bool = False,
    **_extras: Any,
) -> Any:
    """Public wrapper for the ComfyUI node ``MiniMaxH3ImageToVideo``.

    Display name: MiniMax H3 Image to Video

    Category: model/conditioning/minimax

    t2va and fl2va: prompt (+ optional first/last keyframes) -> conditioning + AV latent.

    Returns: positive, LATENT

    Source: object_info cache comfy_extras@zz-official-6338e4bd.json sha256:637e2eb421d9
    """
    if len(args) > 1:
        raise TypeError(f"MiniMaxH3ImageToVideo() takes at most 1 positional argument, got {len(args)}")
    wf = args[0] if args else _current_workflow_or_raise()
    _kwargs: dict[str, Any] = {}
    if clip is not _UNSET:
        _kwargs['clip'] = clip
    if vae is not _UNSET:
        _kwargs['vae'] = vae
    if height is not _UNSET:
        _kwargs['height'] = height
    if length is not _UNSET:
        _kwargs['length'] = length
    if prompt is not _UNSET:
        _kwargs['prompt'] = prompt
    if width is not _UNSET:
        _kwargs['width'] = width
    if first_frame is not _UNSET:
        _kwargs['first_frame'] = first_frame
    if last_frame is not _UNSET:
        _kwargs['last_frame'] = last_frame
    _kwargs.update(_extras)
    return node(wf, 'MiniMaxH3ImageToVideo', _id, pass_raw=pass_raw, **_kwargs)

__all__ = ['MiniMaxH3ImageToVideo']
__vibecomfy_class_types__ = {'MiniMaxH3ImageToVideo': 'MiniMaxH3ImageToVideo'}
