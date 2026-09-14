"""Source-backed corpus contracts for D-CORPUS-20260912.

These assertions deliberately read the authored UI bytes directly.  They do
not compare an importer with its own output, and the required-positive lane
also attempts canonical admission so current importer barriers remain visible.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import pytest


ROOT = Path("ready_templates/sources")

CASES = {
    "01": ("official/image/flux2_klein_4b_t2i.json", "237b436e577cdd2a97527766637e87af162b4c14fb293c9c269b470b7a2d0166"),
    "02": ("official/edit/qwen_image_edit.json", "34d4a94e9a60c9e60ccd96b965834eee92d0428288cbe000cea6837d9b2f9a94"),
    "11": ("official/image/flux2_klein_9b_t2i.json", "ac7513756f3bf72b49292a334c48315aa40e6c0e4ff8dd152773bb55dac17fff"),
    "13": ("official/video/ltx2_3_t2v.json", "0d6ea69dc57324ce3f53e3d69f81ecac19c7f71af977fe32506b50c82c03cbfa"),
    "15": ("custom_nodes/ltxvideo/runexx/LTX-2.3_V2V_Extend_Any_Video.json", "2d63f545d1cfc6e47f55682094dae29fa0177751eb513e934744fd2a30a1126b"),
    "18": ("custom_nodes/wanvideo_wrapper/kijai/wan21_14b_flf2v.json", "6a7b43e9091d9ba19b07f8e200d6d217d5b3ed8faa3353089d1ca4620fceff7d"),
}


def _load(case: str) -> tuple[Path, dict[str, Any]]:
    relative, expected_sha = CASES[case]
    path = ROOT / relative
    data = path.read_bytes()
    assert hashlib.sha256(data).hexdigest() == expected_sha
    return path, json.loads(data)


def _nodes(graph: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(node["id"]): node for node in graph.get("nodes", []) if isinstance(node, dict)}


def _links(graph: dict[str, Any]) -> dict[int, list[Any]]:
    result: dict[int, list[Any]] = {}
    for link in graph.get("links", []):
        if isinstance(link, list):
            result[int(link[0])] = link
        elif isinstance(link, dict) and "id" in link:
            result[int(link["id"])] = [
                link["id"], link.get("origin_id"), link.get("origin_slot"),
                link.get("target_id"), link.get("target_slot"), link.get("type"),
            ]
    return result


def _definitions(graph: dict[str, Any]) -> list[dict[str, Any]]:
    return list((graph.get("definitions") or {}).get("subgraphs") or [])


def _definition_links(definition: dict[str, Any]) -> dict[int, list[Any]]:
    return _links({"links": definition.get("links", [])})


@pytest.mark.parametrize("case", sorted(CASES))
def test_frozen_source_identity(case: str) -> None:
    path, _raw = _load(case)
    assert path.is_file()


def test_case_01_proxy_identity_values_edges_and_output_slot() -> None:
    _path, raw = _load("01")
    nodes, links = _nodes(raw), _links(raw)
    assert {nodes["75"]["type"], nodes["77"]["type"]} == {
        "7b34ab90-36f9-45ba-a665-71d418f0df18",
        "a67caa28-5f85-4917-8396-36004960dd30",
    }
    assert nodes["75"]["widgets_values"][1:3] == [1024, 1024]
    assert nodes["77"]["widgets_values"][1:3] == [1024, 1024]
    assert links[154][1:5] == [75, 0, 9, 0]
    assert links[156][1:5] == [77, 0, 78, 0]
    definition = next(item for item in _definitions(raw) if item["id"] == nodes["75"]["type"])
    assert _definition_links(definition)[153][1:5] == [65, 0, -20, 0]
    assert [item["name"] for item in definition["inputs"]] == [
        "value", "value_1", "unet_name", "clip_name", "vae_name", "text"
    ]
    assert [item["name"] for item in definition["outputs"]] == ["IMAGE"]


def test_case_02_empty_outer_override_and_image_fanout_are_source_facts() -> None:
    _path, raw = _load("02")
    nodes, links = _nodes(raw), _links(raw)
    assert nodes["102"]["widgets_values"] == []
    assert links[177][1:5] == [78, 0, 93, 0]
    assert links[189][1:5] == [78, 0, 102, 0]
    assert links[190][1:5] == [102, 0, 60, 0]
    definition = next(item for item in _definitions(raw) if item["id"] == nodes["102"]["type"])
    image = next(item for item in definition["inputs"] if item["name"] == "image")
    assert image["linkIds"] == [180, 178, 179]


def test_case_11_absent_outer_values_preserve_inner_model_and_dimensions() -> None:
    _path, raw = _load("11")
    nodes = _nodes(raw)
    assert nodes["75"]["widgets_values"] == []
    definition = _definitions(raw)[0]
    inner = _nodes(definition)
    assert inner["68"]["widgets_values"] == [1024, "fixed"]
    assert inner["69"]["widgets_values"] == [1024, "fixed"]
    assert inner["70"]["widgets_values"][0] == "flux-2-klein-base-9b-fp8.safetensors"
    assert inner["71"]["widgets_values"][0] == "qwen_3_8b_fp8mixed.safetensors"
    assert inner["72"]["widgets_values"] == ["full_encoder_small_decoder.safetensors"]


def test_case_13_repeated_checkpoint_references_are_agreeing_fanout() -> None:
    _path, raw = _load("13")
    nodes = _nodes(raw)
    definition = _definitions(raw)[0]
    assert nodes["267"]["type"] == definition["id"]
    assert [item["name"] for item in definition["inputs"]][:5] == [
        "value", "value_2", "value_3", "value_4", "ckpt_name"
    ]
    checkpoint_links = next(item for item in definition["inputs"] if item["name"] == "ckpt_name")["linkIds"]
    assert checkpoint_links == [601, 604, 605]
    assert _links(definition)[601][1:5] == [-10, 4, 236, 0]
    assert _links(definition)[604][1:5] == [-10, 4, 221, 0]
    assert _links(definition)[605][1:5] == [-10, 4, 243, 1]


def test_case_15_proxy_widget_and_linked_value_fanout_are_source_facts() -> None:
    _path, raw = _load("15")
    nodes, links = _nodes(raw), _links(raw)
    instance = nodes["599"]
    assert instance["widgets_values"] == []
    assert instance["properties"]["proxyWidgets"] == [["482", "string_b"]]
    assert links[1082][1:5] == [508, 0, 599, 1]
    assert links[1083][1:5] == [487, 0, 599, 2]
    assert links[1085][1:5] == [599, 0, 592, 1]
    assert links[1086][1:5] == [599, 0, 597, 0]


def test_case_18_end_image_channel_preserves_virtual_leg_and_nonzero_ports() -> None:
    _path, raw = _load("18")
    nodes, links = _nodes(raw), _links(raw)
    assert nodes["92"]["type"] == "SetNode"
    assert nodes["92"]["widgets_values"] == ["end_image"]
    assert nodes["94"]["type"] == "GetNode"
    assert nodes["94"]["widgets_values"] == ["end_image"]
    assert links[184][1:5] == [108, 0, 92, 0]
    assert links[149][1:5] == [94, 0, 96, 0]
    assert links[176][1:5] == [92, 0, 88, 2]
    assert links[188][1:5] == [108, 1, 89, 8]
    assert links[189][1:5] == [108, 2, 89, 9]
    assert nodes["89"]["inputs"][3]["name"] == "end_image"


def test_case_18_virtual_leg_compiles_to_the_named_source_output() -> None:
    path, raw = _load("18")
    from vibecomfy.ingest.normalize import from_ui

    workflow = from_ui(raw, source_path=str(path), use_comfy_converter=False)
    assert workflow.virtual_wires["end_image"]["legs"][0]["from_output"] == "IMAGE"
    compiled = workflow.compile("api")
    assert compiled["96"]["inputs"]["image"] == ["108", 0]
    assert compiled["89"]["inputs"]["end_image"] == ["108", 0]


@pytest.mark.parametrize("case", sorted(CASES))
def test_required_positive_canonical_admission(case: str) -> None:
    """Required positives must be admitted from these exact authored bytes."""
    path, raw = _load(case)
    from vibecomfy.ingest.normalize import from_ui

    try:
        workflow = from_ui(raw, source_path=str(path), use_comfy_converter=False)
    except Exception as exc:  # retain the failing regression for E1/T1 handoff
        pytest.fail(f"required-positive case {case} is not canonically admitted: {type(exc).__name__}: {exc}")
    assert workflow.nodes, f"case {case}: canonical admission produced no nodes"


def test_case_14_one_repeated_reference_has_one_source_link_record() -> None:
    path = ROOT / "custom_nodes/ltxvideo/runexx/LTX-2.3_Talking_Avatar_Qwen_TTS.json"
    raw = json.loads(path.read_text())
    matching = [
        definition for definition in _definitions(raw)
        if any(3485 in (item.get("linkIds") or []) for item in definition.get("outputs", []))
    ]
    assert len(matching) == 1
    definition = matching[0]
    repeated = next(item for item in definition["outputs"] if 3485 in item["linkIds"])
    records = [link for link in definition.get("links", []) if link.get("id") == 3485]
    assert repeated["linkIds"] == [3485, 3485]
    assert len(records) == 1
    assert records[0]["origin_id"] == 1928
    assert records[0]["target_id"] == -20
    pytest.skip("frontend LGraph serialization/deserialization package is unavailable in this worktree; no minimal load/export authority")


def test_case_14_route_fanout_is_admitted_by_the_canonical_importer() -> None:
    path = ROOT / "custom_nodes/ltxvideo/runexx/LTX-2.3_Talking_Avatar_Qwen_TTS.json"
    raw = json.loads(path.read_text())
    from vibecomfy.ingest.normalize import from_ui

    workflow = from_ui(raw, source_path=str(path), use_comfy_converter=False)
    assert workflow.nodes
    assert workflow.compile("api")


def test_exact_negative_case_10_is_descriptive_not_a_graph() -> None:
    path = Path("tests/fixtures/recursive_live_contract/depth2.json")
    raw = json.loads(path.read_text())
    assert raw["capture_status"] == "undetermined"
    assert "could be captured" in raw["capture_note"]
    assert "nodes" not in raw


@pytest.mark.parametrize(
    ("case", "relative", "missing_targets"),
    [
        ("16", "custom_nodes/ltxvideo/lightricks_2_3/LTX-2.3_ICLoRA_Motion_Track_Distilled.json", {2653}),
        ("17", "custom_nodes/ltxvideo/lightricks_2_3/LTX-2.3_ICLoRA_Union_Control_Distilled.json", {2653, 4979}),
    ],
)
def test_exact_negative_cases_retain_missing_source_targets(case: str, relative: str, missing_targets: set[int]) -> None:
    path = ROOT / relative
    raw = json.loads(path.read_text())
    node_ids = {int(node["id"]) for node in raw.get("nodes", []) if isinstance(node, dict) and str(node.get("id")).isdigit()}
    observed = {int(link[3]) for link in raw.get("links", []) if isinstance(link, list) and int(link[3]) in missing_targets}
    assert observed == missing_targets, case
    assert not (observed & node_ids)


def test_native_depth_two_positive_fixture_is_real_nested_graph() -> None:
    path = Path("tests/fixtures/recursive_live_contract/depth2_native.json")
    raw = json.loads(path.read_text())
    outer = raw["definitions"]["subgraphs"][0]
    inner = outer["definitions"]["subgraphs"][0]
    assert raw["nodes"][0]["type"] == outer["id"]
    assert outer["nodes"][0]["type"] == inner["id"]
    assert outer["links"] == [[101, -10, 0, 11, 0, "INT"], [102, 11, 0, -20, 0, "INT"]]
    assert inner["links"] == [[201, -10, 0, 21, 0, "INT"], [202, 21, 0, -20, 0, "INT"]]
    assert inner["nodes"][0]["widgets_values"] == [1024, "fixed"]
