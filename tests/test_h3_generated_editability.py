"""Acceptance checks for the generated H3 Python review artifact."""
from __future__ import annotations

import ast
import importlib.util
from pathlib import Path


PATH = Path(__file__).parent / "fixtures/h3_generated_editability.py"


def _module():
    spec = importlib.util.spec_from_file_location("generated_h3_review", PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_generated_h3_build_accepts_and_retains_every_public_control() -> None:
    module = _module()
    workflow = module.build(
        model="override-unet.safetensors",
        steps=31,
        prompt="override prompt",
        duration=7,
        seed=123,
        lp_steps=9,
        source_video="override.mp4",
        mask_keyframes="override-keyframes.json",
        audio_intervals="override-intervals.json",
    )

    assert workflow.nodes["105::6"].inputs["unet_name"] == "override-unet.safetensors"
    assert workflow.nodes["105::9"].inputs["steps"] == 31
    assert workflow.nodes["105::104"].inputs["prompt"] == "override prompt"
    assert workflow.nodes["105::111"].inputs["value"] == 7
    assert workflow.nodes["171"].inputs["value"] == 123
    assert workflow.nodes["105::159"].inputs["LanPaint_NumSteps"] == 9
    assert workflow.nodes["164"].inputs["video"] == "override.mp4"
    assert workflow.nodes["164"].inputs["keyframes"] == "override-keyframes.json"
    assert workflow.nodes["164"].inputs["audio_mask"] == "override-intervals.json"
    assert workflow.nodes["164"].widgets == {}


def test_generated_h3_build_retains_effective_wire_references() -> None:
    module = _module()
    workflow = module.build()
    references = [
        (node.id, field, value)
        for node in workflow.nodes.values()
        for field, value in node.inputs.items()
        if isinstance(value, (list, tuple)) and len(value) == 2
    ]
    # The expanded source has 28 links; nine are root-to-inner effective
    # connections and the remaining internal links are retained as references.
    assert len(workflow.edges) == 9
    assert len(references) >= 20
    assert workflow.nodes["92"].inputs["video"] == ["105::168", 0]


def test_generated_h3_source_has_controls_and_compact_custody_only() -> None:
    source = PATH.read_text(encoding="utf-8")
    tree = ast.parse(source)
    metadata_call = next(
        node for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "build"
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == "ReadyMetadata"
    )
    metadata_keys = {keyword.arg for keyword in metadata_call.keywords if keyword.arg is not None}

    assert "_native_subgraph_source" not in metadata_keys
    assert "_ui_door" not in metadata_keys
    assert {"_native_subgraph_provenance", "_native_subgraph_diagnostics"} <= metadata_keys
    # These are meaningful user controls, not serialized graph structure.
    assert "DEFAULT_PROMPT =" in source
    assert "MASK_KEYFRAMES =" in source
    assert "AUDIO_INTERVALS =" in source
    metadata_text = ast.get_source_segment(source, metadata_call)
    assert metadata_text is not None
    assert "'nodes':" not in metadata_text
    assert "'links':" not in metadata_text
    assert "'boundary':" not in metadata_text
