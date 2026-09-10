from __future__ import annotations

import tempfile
from pathlib import Path
from PIL import Image

from vibecomfy.porting.reorganise.visualize import _detail_lines, _node_rect, render_layout_png


def test_render_detail_preserves_authored_geometry_and_input() -> None:
    node = {
        "id": 171,
        "type": "MiniMaxH3ImageToVideo",
        "pos": [520, 0],
        "size": [320, 52],
        "inputs": [{"name": "clip"}, {"name": "vae"}],
        "outputs": [{"name": "IMAGE"}],
    }
    authored = {key: value.copy() if isinstance(value, list) else value for key, value in node.items()}

    assert _node_rect(node) == (520.0, 0.0, 320.0, 52.0)
    assert _detail_lines(node) == (
        "[171] MiniMaxH3ImageToVideo",
        "in: clip, vae",
        "out: IMAGE",
    )
    assert node == authored


def test_render_layout_png_draws_link_titles_and_ports() -> None:
    ui_json = {
        "nodes": [
            {"id": 1, "type": "SourceNode", "pos": [0, 0], "size": [180, 100],
             "outputs": [{"name": "IMAGE", "links": [7]}]},
            {"id": 2, "type": "SinkNode", "pos": [320, 0], "size": [180, 100],
             "inputs": [{"name": "image", "link": 7}]},
        ],
        "links": [[7, 1, 0, 2, 0, "IMAGE"]],
        "groups": [],
    }
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "linked.png"
        render_layout_png(ui_json, path)
        image = Image.open(path).convert("RGB")
        colors = set(image.getdata())
        assert len(colors) > 20
        # The dark edge is behind the cards and therefore survives between them.
        assert any(sum(pixel) < 260 for pixel in colors)


def test_render_layout_png_draws_link_titles_and_ports() -> None:
    ui_json = {"nodes": [
        {"id": 1, "type": "SourceNode", "pos": [0, 0], "size": [180, 100],
         "outputs": [{"name": "IMAGE", "links": [7]}]},
        {"id": 2, "type": "SinkNode", "pos": [320, 0], "size": [180, 100],
         "inputs": [{"name": "image", "link": 7}]},
    ], "links": [[7, 1, 0, 2, 0, "IMAGE"]], "groups": []}
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "linked.png"
        render_layout_png(ui_json, path)
        from vibecomfy.porting.reorganise.visualize import _node_rect
        assert _node_rect(ui_json["nodes"][1])[3] >= 80
        assert _node_rect(ui_json["nodes"][0])[3] >= 80
        colors = set(Image.open(path).convert("RGB").getdata())
        assert len(colors) > 20
        assert any(sum(pixel) < 260 for pixel in colors)


def test_render_layout_png_produces_non_empty_png_from_minimal_ui_json() -> None:
    """Smoke test: render_layout_png writes a non-empty PNG file for a minimal UI JSON."""
    ui_json: dict = {
        "nodes": [
            {
                "id": 1,
                "type": "CheckpointLoaderSimple",
                "pos": [100.0, 200.0],
                "size": [300.0, 120.0],
            },
            {
                "id": 2,
                "type": "CLIPTextEncode",
                "pos": [450.0, 200.0],
                "size": [280.0, 140.0],
            },
        ],
        "groups": [
            {
                "title": "Loaders",
                "bounding": [80.0, 160.0, 340.0, 200.0],
            },
            {
                "title": "Conditioning",
                "bounding": [430.0, 160.0, 320.0, 220.0],
            },
        ],
    }

    with tempfile.TemporaryDirectory() as tmpdir:
        png_path = Path(tmpdir) / "layout.png"
        render_layout_png(ui_json, png_path)

        assert png_path.exists(), "PNG file must be created"
        assert png_path.stat().st_size > 0, "PNG file must be non-empty"
        assert Image.open(png_path).height > 220, "detail band must be appended below the overview"


def test_render_layout_png_produces_non_empty_png_from_fixture_json() -> None:
    """Smoke test: render_layout_png handles a real fixture-based UI JSON and writes a non-empty PNG."""
    fixture_path = (
        Path(__file__).resolve().parent
        / "fixtures"
        / "reorganise"
        / "simple_text_to_image.json"
    )
    ui_json_raw = fixture_path.read_text(encoding="utf-8")
    import json

    ui_json = json.loads(ui_json_raw)

    with tempfile.TemporaryDirectory() as tmpdir:
        png_path = Path(tmpdir) / "layout_fixture.png"
        render_layout_png(ui_json, png_path)

        assert png_path.exists(), "PNG file must be created from fixture"
        assert png_path.stat().st_size > 0, "PNG file must be non-empty from fixture"
