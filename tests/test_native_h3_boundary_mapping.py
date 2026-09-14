"""Regression fixtures for the MiniMax H3 native subgraph boundary.

These tests intentionally inspect the source artifact without starting
ComfyUI.  They pin the mapping an eventual native-to-Python adapter must
preserve, including outer subgraph-instance overrides.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from vibecomfy.ingest.normalize import from_ui
from vibecomfy.ingest.native_subgraph import NativeSubgraphError, expand_native_subgraphs
from vibecomfy.porting.emitter import emit_canonical_python
from vibecomfy.porting.emit.ui import emit_ui_json
from vibecomfy.security.agent_generated_loader import load_agent_generated_scratchpad


SOURCE = (
    Path(__file__).parent / "fixtures/native_h3_minimal.json"
)


def _source() -> dict:
    return json.loads(SOURCE.read_text())


def test_h3_fixture_retains_upstream_provenance() -> None:
    provenance = _source()["_source_provenance"]
    assert provenance["upstream_commit"] == "32cf848e93971da380d868936e007f5611218bee"
    assert provenance["source_sha256"] == "2dd64fe26c42281962e434841c458cc935b1d1858e83093b882bbaeb02dc3121"


def _graph_parts() -> tuple[dict, dict]:
    raw = _source()
    outer = next(node for node in raw["nodes"] if node["id"] == 105)
    definition = raw["definitions"]["subgraphs"][0]
    return outer, definition


def test_h3_native_input_slots_preserve_loader_fanout_and_instance_overrides() -> None:
    outer, definition = _graph_parts()
    assert [item["name"] for item in definition["inputs"]] == [
        "first_frame",
        "last_frame",
        "prompt",
        "width",
        "height",
        "value_1",
        "noise_seed",
        "unet_name",
        "clip_name",
        "vae_name",
        "vae_name_1",
        "video",
        "mask",
        "mask_1",
        "LanPaint_NumSteps",
    ]

    native_targets = [
        link for link in definition["links"] if link["origin_id"] == -10
    ]
    by_slot = {}
    for link in native_targets:
        by_slot.setdefault(link["origin_slot"], []).append(link)

    assert {(item["target_id"], item["target_slot"]) for item in by_slot[7]} == {(6, 0)}
    assert {(item["target_id"], item["target_slot"]) for item in by_slot[8]} == {(13, 0)}
    assert {(item["target_id"], item["target_slot"]) for item in by_slot[9]} == {(11, 0)}
    assert {(item["target_id"], item["target_slot"]) for item in by_slot[10]} == {(24, 0)}
    assert {(item["target_id"], item["target_slot"]) for item in by_slot[11]} == {(166, 0), (168, 1)}
    assert {(item["target_id"], item["target_slot"]) for item in by_slot[12]} == {(166, 3), (168, 4)}
    assert {(item["target_id"], item["target_slot"]) for item in by_slot[13]} == {(166, 4), (168, 5)}

    # The effective values are on the outer instance.  They intentionally
    # differ from the nested loader defaults in this source graph.
    assert outer["widgets_values"][5:9] == [
        "minimax_h3_fl2va_pruned_fp8_scaled.safetensors",
        "qwen3vl_32b_minimax_h3_int8_convrot.safetensors",
        "minimax_h3_video_vae_fp16.safetensors",
        "minimax_h3_audio_vae_fp32.safetensors",
    ]
    inner = {node["id"]: node for node in definition["nodes"]}
    assert inner[6]["widgets_values"][0] != outer["widgets_values"][5]
    assert inner[13]["widgets_values"][0] != outer["widgets_values"][6]


def test_h3_native_output_is_video_decode_slot_zero() -> None:
    _outer, definition = _graph_parts()
    outputs = [
        link
        for link in definition["links"]
        if link["target_id"] == -20
    ]
    assert outputs == [
        {"id": 323, "origin_id": 168, "origin_slot": 0, "target_id": -20, "target_slot": 0, "type": "VIDEO"}
    ]


def test_native_boundary_missing_or_ambiguous_inputs_fail_closed() -> None:
    raw = _source()
    definition = raw["definitions"]["subgraphs"][0]
    definition["links"] = [link for link in definition["links"] if link["origin_slot"] != 8 or link["origin_id"] != -10]
    with pytest.raises(ValueError, match="unsupported_boundary_encoding"):
        from_ui(raw, source_path="h3-missing-boundary.json", use_comfy_converter=False)

    ambiguous = _source()
    links = ambiguous["definitions"]["subgraphs"][0]["links"]
    duplicate = copy.deepcopy(next(link for link in links if link["origin_id"] == -10 and link["origin_slot"] == 8))
    duplicate["id"] = 99999
    links.append(duplicate)
    with pytest.raises(ValueError, match="unsupported_boundary_encoding"):
        from_ui(ambiguous, source_path="h3-ambiguous-boundary.json", use_comfy_converter=False)


def test_native_h3_expansion_preserves_instance_values_fanout_and_save_output() -> None:
    expanded = expand_native_subgraphs(_source())
    nodes = {str(node["id"]): node for node in expanded["nodes"]}
    assert "105" not in nodes
    assert expanded.get("definitions") is None

    assert nodes["105::6"]["widgets_values"][0] == "minimax_h3_fl2va_pruned_fp8_scaled.safetensors"
    assert nodes["105::13"]["widgets_values"][0] == "qwen3vl_32b_minimax_h3_int8_convrot.safetensors"
    assert nodes["105::11"]["widgets_values"][0] == "minimax_h3_video_vae_fp16.safetensors"
    assert nodes["105::24"]["widgets_values"][0] == "minimax_h3_audio_vae_fp32.safetensors"

    links = expanded["links"]
    assert [link for link in links if link[3] == "105::166" and link[4] == 0] == [
        [300, "164", 0, "105::166", 0, "VIDEO"]
    ]
    assert [
        (link[1], link[2], link[3], link[4], link[5])
        for link in links
        if link[3] == "105::168" and link[4] == 1
    ] == [("164", 0, "105::168", 1, "VIDEO")]
    assert [link for link in links if link[3] == "92" and link[4] == 0] == [
        [194, "105::168", 0, "92", 0, "VIDEO"]
    ]


def test_native_h3_expansion_rejects_boolean_slots_and_contradictory_target_backlinks() -> None:
    boolean_slot = _source()
    native_link = next(
        link
        for link in boolean_slot["definitions"]["subgraphs"][0]["links"]
        if link["origin_id"] == -10
    )
    native_link["origin_slot"] = True
    with pytest.raises(NativeSubgraphError, match="native_subgraph_expansion"):
        expand_native_subgraphs(boolean_slot)

    contradictory = _source()
    inner = contradictory["definitions"]["subgraphs"][0]["nodes"]
    target = next(node for node in inner if node["id"] == 104)
    target["inputs"][2]["link"] = 999999
    with pytest.raises(NativeSubgraphError, match="backlink|link"):
        expand_native_subgraphs(contradictory)


def test_native_h3_expansion_is_accepted_by_canonical_ui_ingest() -> None:
    workflow = from_ui(
        expand_native_subgraphs(_source()),
        source_path="native_h3_minimal.json",
        use_comfy_converter=False,
    )
    assert "105" not in workflow.nodes
    assert "105::168" in workflow.nodes
    assert "video" not in workflow.nodes["92"].inputs
    assert any(
        edge.from_node == "105::168"
        and edge.from_output == "0"
        and edge.to_node == "92"
        and edge.to_input == "video"
        for edge in workflow.edges
    )


def _math_expression_ui(*, linked: bool) -> dict:
    math_inputs = [
        {"name": "expression", "type": "STRING", "link": None, "widget": {"name": "expression"}},
        {
            "name": "values.a",
            "type": "FLOAT,INT,BOOLEAN",
            "link": 1 if linked else None,
            "widget": {"name": "values.a"},
        },
    ]
    nodes = [{
        "id": 1,
        "type": "ComfyMathExpression",
        "inputs": math_inputs,
        "outputs": [],
        "widgets_values": ["a + 1", 5] if not linked else ["a + 1"],
    }]
    links = []
    if linked:
        nodes.insert(0, {
            "id": 2,
            "type": "PrimitiveFloat",
            "inputs": [],
            "outputs": [{"name": "value", "type": "FLOAT", "links": [1]}],
            "widgets_values": [3.0],
        })
        links.append([1, 2, 0, 1, 1, "FLOAT"])
    return {"workflow_id": "math-expression", "nodes": nodes, "links": links, "groups": []}


def test_math_expression_unlinked_dynamic_literal_survives_ui_export_and_reload() -> None:
    workflow = from_ui(_math_expression_ui(linked=False), source_path="h3-edit.json", use_comfy_converter=False)
    workflow.nodes["1"].inputs["values.a"] = 6

    exported = emit_ui_json(workflow)
    node = next(item for item in exported["nodes"] if item["id"] == 1)
    assert node["widgets_values"] == ["a + 1", 6]
    assert [item["name"] for item in node["inputs"]] == ["expression", "values.a"]
    assert node["inputs"][1]["widget"] == {"name": "values.a"}

    reloaded = from_ui(exported, source_path="h3-edit-reload.json", use_comfy_converter=False)
    assert reloaded.nodes["1"].inputs["values.a"] == 6
    assert reloaded.compile("api")["1"]["inputs"]["values.a"] == 6


def test_math_expression_linked_dynamic_input_keeps_descriptor_and_no_literal_duplicate() -> None:
    workflow = from_ui(_math_expression_ui(linked=True), source_path="h3-linked.json", use_comfy_converter=False)

    exported = emit_ui_json(workflow)
    node = next(item for item in exported["nodes"] if item["id"] == 1)
    descriptor = next(item for item in node["inputs"] if item["name"] == "values.a")
    assert descriptor["widget"] == {"name": "values.a"}
    assert descriptor["link"] == 1
    assert node["widgets_values"] == ["a + 1"]
    assert len([item for item in exported["nodes"] if item["type"] == "PrimitiveFloat"]) == 1

    reloaded = from_ui(exported, source_path="h3-linked-reload.json", use_comfy_converter=False)
    assert reloaded.nodes["1"].inputs == {"expression": "a + 1"}
    assert [(edge.from_node, edge.to_node, edge.to_input) for edge in reloaded.edges] == [("2", "1", "values.a")]
