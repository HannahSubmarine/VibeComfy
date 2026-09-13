from __future__ import annotations

import json
from pathlib import Path

import pytest

from vibecomfy._compile._resolve import HelperResolveError, resolve_helpers
from vibecomfy.ingest.normalize import from_envelope
from vibecomfy.workflow import VibeEdge, VibeNode


FIXTURE = Path(__file__).parent / "fixtures/live_agentic_corpus/corpus/0070184c5f1c8ca2.json"


def test_real_corpus_linked_multiline_passes_source_and_preserves_fanout() -> None:
    workflow = from_envelope(json.loads(FIXTURE.read_text()))
    workflow.nodes["fanout"] = VibeNode("fanout", "StringSink")
    workflow.edges.append(VibeEdge("281", "0", "fanout", "value"))

    resolve_helpers(workflow.nodes, workflow.edges, {})

    assert "281" not in workflow.nodes
    assert {(edge.from_node, edge.from_output, edge.to_node) for edge in workflow.edges} >= {
        ("259", "0", "263"),
        ("259", "0", "fanout"),
    }
    assert workflow.nodes["263"].inputs["negative"] == (
        "bad hands, extra fingers, missing fingers, fused fingers, broken hands, "
        "mutant hands, twisted limbs, extra limbs, missing limbs, dimple "
    )


def test_multiline_zero_inbound_still_folds_literal() -> None:
    nodes = {
        "source": VibeNode("source", "Source"),
        "target": VibeNode("target", "Target"),
        "primitive": VibeNode(
            "primitive", "PrimitiveStringMultiline", inputs={"value": "literal"}
        ),
    }
    edges = [VibeEdge("primitive", "0", "target", "text")]

    resolve_helpers(nodes, edges, {})

    assert nodes["target"].inputs["text"] == "literal"
    assert "primitive" not in nodes
    assert edges == []


def test_multiline_multiple_inbound_fails_closed() -> None:
    nodes = {
        "a": VibeNode("a", "Source"),
        "b": VibeNode("b", "Source"),
        "primitive": VibeNode(
            "primitive", "PrimitiveStringMultiline", inputs={"value": "literal"}
        ),
        "target": VibeNode("target", "Target"),
    }
    edges = [
        VibeEdge("a", "0", "primitive", "value"),
        VibeEdge("b", "0", "primitive", "value"),
        VibeEdge("primitive", "0", "target", "text"),
    ]

    with pytest.raises(HelperResolveError, match="multiple inbound"):
        resolve_helpers(nodes, edges, {})


def test_multiline_known_type_mismatch_fails_closed() -> None:
    nodes = {
        "source": VibeNode(
            "source", "Source", native_output_names=["out"], native_output_types=["IMAGE"]
        ),
        "primitive": VibeNode("primitive", "PrimitiveStringMultiline"),
        "target": VibeNode("target", "Target"),
    }
    edges = [
        VibeEdge("source", "out", "primitive", "value"),
        VibeEdge("primitive", "0", "target", "text"),
    ]

    with pytest.raises(HelperResolveError, match="not STRING"):
        resolve_helpers(nodes, edges, {})


def test_multiline_helper_cycle_fails_closed() -> None:
    nodes = {
        "a": VibeNode("a", "PrimitiveStringMultiline"),
        "b": VibeNode("b", "PrimitiveStringMultiline"),
    }
    edges = [VibeEdge("a", "0", "b", "value"), VibeEdge("b", "0", "a", "value")]

    with pytest.raises(HelperResolveError, match="cycle"):
        resolve_helpers(nodes, edges, {})
