"""Focused contracts for the pinned LanPaint wrapper set."""
from __future__ import annotations

import inspect
from pathlib import Path

from vibecomfy.porting.wrappers.codegen import render_pack, render_pack_stub
from vibecomfy.porting.wrappers.discovery import discover_pack
from vibecomfy.schema.provider import ObjectInfoIndexSchemaProvider
from vibecomfy.workflow import VibeWorkflow, WorkflowSource

PACK = "LanPaint"
CLASSES = (
    "LanPaint_AVDecode",
    "LanPaint_AVEncode",
    "LanPaint_SamplerCustomAdvanced",
    "LanPaint_VideoMaskEditor",
)


def test_pinned_discovery_has_exact_classes_fields_outputs_and_provenance() -> None:
    specs = discover_pack(PACK, sources=("cache",))
    assert tuple(spec.class_type for spec in specs) == CLASSES
    assert all(spec.source_provenance.startswith("object_info cache LanPaint@2.1.0.json") for spec in specs)

    by_name = {spec.class_type: spec for spec in specs}
    assert tuple(by_name[CLASSES[0]].inputs) == (
        "samples", "video", "vae", "audio_vae", "mask", "audio_mask",
        "blend_overlap", "audio_crossfade",
    )
    assert by_name["LanPaint_AVDecode"].outputs == ("video", "audio")
    assert by_name["LanPaint_AVDecode"].output_types == ("VIDEO", "AUDIO")
    assert by_name["LanPaint_AVEncode"].outputs == ("latent",)
    assert by_name["LanPaint_SamplerCustomAdvanced"].inputs["LanPaint_PromptMode"].options == (
        "Image First", "Prompt First"
    )
    assert by_name["LanPaint_VideoMaskEditor"].inputs["video"].options is None


def test_pinned_schema_index_uses_same_source_and_output_roster() -> None:
    provider = ObjectInfoIndexSchemaProvider("vibecomfy/porting/cache/object_info")
    schema = provider.get_schema("LanPaint_AVDecode")
    assert schema is not None
    assert schema.source_package == PACK
    assert schema.source_version == "2.1.0"
    assert set(schema.inputs) == {
        "samples", "video", "vae", "audio_vae", "mask", "audio_mask",
        "blend_overlap", "audio_crossfade",
    }
    assert [(output.name, output.type) for output in schema.outputs] == [
        ("video", "VIDEO"), ("audio", "AUDIO")
    ]


def test_importable_wrappers_forward_only_present_values_and_keep_outputs() -> None:
    import vibecomfy.nodes.lanpaint as lanpaint

    wf = VibeWorkflow("lanpaint-test", WorkflowSource(id="lanpaint-test", path="test.py", source_type="inline"))
    result = lanpaint.LanPaint_AVDecode(
        wf, samples="samples", video="video", vae="vae", audio_vae="audio-vae",
        mask="mask", audio_mask="audio-mask", blend_overlap=11,
    )
    node = result.node
    assert node.class_type == "LanPaint_AVDecode"
    assert node.inputs == {
        "samples": "samples", "video": "video", "vae": "vae", "audio_vae": "audio-vae",
        "mask": "mask", "audio_mask": "audio-mask", "blend_overlap": 11,
    }
    assert tuple(node.native_output_names or ()) == ("VIDEO", "AUDIO")
    assert "audio_crossfade" not in node.inputs

    signature = inspect.signature(lanpaint.LanPaint_SamplerCustomAdvanced)
    assert signature.parameters["LanPaint_PromptMode"].annotation == "Literal['Image First', 'Prompt First'] | _Omitted"


def test_generated_pair_is_deterministic_and_registered() -> None:
    import vibecomfy.nodes as nodes
    import vibecomfy.nodes.lanpaint as lanpaint

    assert "lanpaint" in nodes.MODULES
    assert set(lanpaint.__all__) == set(CLASSES)
    specs = discover_pack(PACK, sources=("cache",))
    result = render_pack(PACK, specs, out_dir=Path("vibecomfy/nodes"))
    assert result.source_text == Path("vibecomfy/nodes/lanpaint.py").read_text(encoding="utf-8")
    assert render_pack_stub(PACK, specs, out_dir=Path("vibecomfy/nodes")) == Path(
        "vibecomfy/nodes/lanpaint.pyi"
    ).read_text(encoding="utf-8")
