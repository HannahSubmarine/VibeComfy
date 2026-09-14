"""Focused contracts for the pinned official MiniMax H3 wrapper."""
from __future__ import annotations

import inspect
from pathlib import Path

from vibecomfy.porting.wrappers.codegen import render_pack, render_pack_stub
from vibecomfy.porting.wrappers.discovery import discover_pack
from vibecomfy.schema.provider import ObjectInfoIndexSchemaProvider
from vibecomfy.workflow import VibeWorkflow, WorkflowSource


PACK = "comfy_extras"
CLASS = "MiniMaxH3ImageToVideo"


def test_pinned_h3_schema_and_provenance_are_exact() -> None:
    spec = discover_pack(PACK, sources=("cache",))[0]
    assert spec.class_type == CLASS
    assert spec.source_provenance.startswith(
        "object_info cache comfy_extras@zz-official-6338e4bd.json"
    )
    assert tuple(spec.inputs) == (
        "clip", "vae", "prompt", "width", "height", "length", "first_frame", "last_frame"
    )
    assert spec.outputs == ("positive", "LATENT")
    assert spec.output_types == ("CONDITIONING", "LATENT")
    assert spec.inputs["prompt"].widget_metadata == {"dynamicPrompts": True, "multiline": True}
    assert spec.inputs["width"].default == 1344
    assert spec.inputs["height"].default == 768
    assert spec.inputs["length"].widget_metadata == {"default": 124, "max": 3600, "min": 5, "step": 17}


def test_h3_wrapper_is_importable_omits_unset_inputs_and_keeps_slots() -> None:
    from vibecomfy.nodes.comfy_extras import MiniMaxH3ImageToVideo

    wf = VibeWorkflow("h3", WorkflowSource(id="h3", path="h3.py", source_type="inline"))
    built = MiniMaxH3ImageToVideo(wf, clip="clip", vae="vae", prompt="a test", width=1344, height=768, length=124)
    assert built.node.class_type == CLASS
    assert built.node.inputs == {"clip": "clip", "vae": "vae", "prompt": "a test", "width": 1344, "height": 768, "length": 124}
    assert tuple(built.node.native_output_names or ()) == ("POSITIVE", "LATENT")
    assert inspect.signature(MiniMaxH3ImageToVideo).parameters["prompt"].annotation == "str | _Omitted"


def test_h3_schema_provider_and_generation_are_registered_and_deterministic() -> None:
    provider = ObjectInfoIndexSchemaProvider("vibecomfy/porting/cache/object_info")
    schema = provider.get_schema(CLASS)
    assert schema is not None
    assert schema.source_package == PACK
    assert schema.source_version == "zz-official-6338e4bd"
    specs = discover_pack(PACK, sources=("cache",))
    rendered = render_pack(PACK, specs, out_dir=Path("vibecomfy/nodes"))
    assert rendered.source_text == Path("vibecomfy/nodes/comfy_extras.py").read_text(encoding="utf-8")
    assert render_pack_stub(PACK, specs, out_dir=Path("vibecomfy/nodes")).startswith("# vibecomfy:generated")
