from __future__ import annotations

import ast
import importlib
import sys
import types
from pathlib import Path

import pytest

from vibecomfy.porting.emit import emit_constants
from vibecomfy.porting.emit.emit_ready import _v2_output_args
from vibecomfy.porting.convert import port_convert_workflow
from vibecomfy.porting.emitter import emit_canonical_python
from vibecomfy.porting.workbench import load_port_source
from vibecomfy.schema.provider import ObjectInfoIndexSchemaProvider
from vibecomfy.security.provenance import Provenance
from vibecomfy.workflow import VibeNode, VibeOutput, VibeWorkflow, WorkflowSource
from vibecomfy.workflow_bundle import emit_bundle, load_bundle


def _reset_wrapper_registry(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(emit_constants, "_WRAPPER_CLASS_TO_MODULE", None)
    monkeypatch.setattr(emit_constants, "_WRAPPER_CLASS_TO_SYMBOL", None)
    monkeypatch.setattr(emit_constants, "_WRAPPER_MODULE_SIGNATURE", None)


def test_registered_wrapper_import_failure_is_not_raw_fallback(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _reset_wrapper_registry(monkeypatch)
    monkeypatch.setattr(
        emit_constants,
        "_wrapper_modules",
        lambda: ("missing_registered_pack",),
    )
    real_import = importlib.import_module

    def import_module(name: str, package: str | None = None):
        if name == "vibecomfy.nodes.missing_registered_pack":
            raise ImportError("fixture import failure", name=name)
        return real_import(name, package)

    monkeypatch.setattr(emit_constants.importlib, "import_module", import_module)

    with pytest.raises(RuntimeError, match="registered_wrapper_import_failed"):
        emit_constants._wrapper_module_for_class("ProvenNode")


def test_wrapper_registry_refreshes_after_a_new_module_is_registered(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import vibecomfy.nodes as nodes

    _reset_wrapper_registry(monkeypatch)
    emit_constants._wrapper_class_to_module()

    module_name = "_emitter_registered_wrapper_fixture"
    qualified_name = f"vibecomfy.nodes.{module_name}"
    module = types.ModuleType(qualified_name)

    def ProvenNode() -> None:
        return None

    module.ProvenNode = ProvenNode
    module.__all__ = ["ProvenNode"]
    module.__vibecomfy_class_types__ = {"ProvenNode": "Proven Class"}
    monkeypatch.setitem(sys.modules, qualified_name, module)
    monkeypatch.setattr(nodes, "MODULES", [*nodes.MODULES, module_name])

    assert emit_constants._wrapper_module_for_class("Proven Class") == module_name
    assert emit_constants._wrapper_symbol_for_class("Proven Class") == "ProvenNode"


def _typed_multi_output_workflow() -> VibeWorkflow:
    workflow = VibeWorkflow("typed-slots", WorkflowSource("typed-slots"))
    workflow.nodes["1"] = VibeNode(
        "1",
        "SimpleCalculatorKJ",
        inputs={"expression": "a + b", "variables": {"a": 2, "b": 5}},
        uid="calculator-uid",
        native_input_names=["expression", "variables"],
        native_output_names=["FLOAT", "INT", "BOOLEAN"],
        native_input_types=["STRING", "DICT"],
        native_output_types=["FLOAT", "INT", "BOOLEAN"],
        native_input_optional=[False, True],
    )
    workflow.nodes["2"] = VibeNode(
        "2",
        "SaveImage",
        inputs={"images": None, "filename_prefix": "typed-slots"},
        uid="consumer-uid",
        native_input_names=["images", "filename_prefix"],
        native_output_names=[],
        native_input_types=["IMAGE", "STRING"],
        native_output_types=[],
        native_input_optional=[False, False],
    )
    workflow.connect("1.1", "2.images")
    workflow.outputs = [
        VibeOutput(
            "2",
            "SaveImage",
            artifact_kind="image",
            filename_prefix="typed-slots",
        )
    ]
    return workflow


def test_registered_wrapper_preserves_nonzero_slot_identity_and_native_ports(
    tmp_path: Path,
) -> None:
    workflow = _typed_multi_output_workflow()
    source = emit_canonical_python(workflow)
    tree = ast.parse(source)

    imports = {
        (node.module, alias.name)
        for node in tree.body
        if isinstance(node, ast.ImportFrom)
        for alias in node.names
    }
    assert ("vibecomfy.nodes.kjnodes", "SimpleCalculatorKJ") in imports
    assert ("vibecomfy.nodes.core", "SaveImage") in imports
    assert "raw_call('SimpleCalculatorKJ'" not in source
    assert "images=simplecalculatorkj.out('INT')" in source

    output = tmp_path / "typed_slots.py"
    emit_bundle(workflow, output, {"operation": "authored"})
    rebuilt = load_bundle(output, trust=Provenance.USER_CONFIRMED).workflow

    assert rebuilt.semantic_digest() == workflow.semantic_digest()
    assert rebuilt.nodes["1"].uid == "calculator-uid"
    assert rebuilt.nodes["2"].uid == "consumer-uid"
    assert rebuilt.nodes["1"].native_output_names == ["FLOAT", "INT", "BOOLEAN"]
    assert rebuilt.nodes["1"].native_output_types == ["FLOAT", "INT", "BOOLEAN"]
    assert rebuilt.edges[0].from_output == "1"


def test_exact_h3_uses_lanpaint_wrappers_with_only_minimax_raw() -> None:
    source_path = Path(
        "docs/handover/unified-workflow-integrity-20260909/assets/h3/"
        "MiniMax_H3_AV_EncodeDecode_Inpaint.json"
    )
    provider = ObjectInfoIndexSchemaProvider("vibecomfy/porting/cache/object_info")
    loaded = load_port_source(
        str(source_path),
        schema_provider=provider,
        use_comfy_converter=False,
    )
    assert loaded.source_hash == (
        "sha256:2dd64fe26c42281962e434841c458cc935b1d1858e83093b882bbaeb02dc3121"
    )

    # load_port_source has already expanded the native definition. Passing its
    # raw UI payload again would ask the converter to ingest that boundary a
    # second time rather than exercise the shared emitter.
    result = port_convert_workflow(
        loaded.workflow,
        source_path=loaded.source_path,
        source_hash=loaded.source_hash,
        raw_workflow=None,
        schema_provider=provider,
        validate=True,
        prune_dead_branches=False,
    )
    assert result.validation is not None
    assert result.validation.import_ok
    assert result.validation.build_ok
    assert result.validation.compile_ok
    assert result.validation.parity_ok

    tree = ast.parse(result.text)
    lanpaint_classes = {
        "LanPaint_AVDecode",
        "LanPaint_AVEncode",
        "LanPaint_SamplerCustomAdvanced",
        "LanPaint_VideoMaskEditor",
    }
    imports = {
        alias.name
        for node in tree.body
        if isinstance(node, ast.ImportFrom)
        and node.module == "vibecomfy.nodes.lanpaint"
        for alias in node.names
    }
    calls = {
        call.func.id
        for call in ast.walk(tree)
        if isinstance(call, ast.Call)
        and isinstance(call.func, ast.Name)
        and call.func.id in lanpaint_classes
    }
    raw_calls = {
        call.args[0].value
        for call in ast.walk(tree)
        if isinstance(call, ast.Call)
        and isinstance(call.func, ast.Name)
        and call.func.id == "raw_call"
        and call.args
        and isinstance(call.args[0], ast.Constant)
        and isinstance(call.args[0].value, str)
    }
    assert imports == lanpaint_classes
    assert calls == lanpaint_classes
    assert raw_calls == {"MiniMaxH3ImageToVideo"}

    unresolved = [
        issue
        for issue in result.validation.issues
        if issue.code == "unknown_class_type"
    ]
    assert len(unresolved) == 1
    assert unresolved[0].detail["class_type"] == "MiniMaxH3ImageToVideo"
    assert provider.get_schema("MiniMaxH3ImageToVideo") is None

    sampler_call = next(
        call
        for call in ast.walk(tree)
        if isinstance(call, ast.Call)
        and isinstance(call.func, ast.Name)
        and call.func.id == "LanPaint_SamplerCustomAdvanced"
    )
    sampler_kwargs = {keyword.arg for keyword in sampler_call.keywords}
    assert sampler_kwargs == {
        "LanPaint_NumSteps",
        "LanPaint_Lambda",
        "LanPaint_StepSize",
        "LanPaint_PromptMode",
        "LanPaint_Info",
        "guider",
        "latent_image",
        "noise",
        "sampler",
        "sigmas",
    }
    assert "audio_mask=lanpaint_videomaskeditor.out('AUDIO_MASK')" in result.text
    assert "wf.connect(" not in result.text
    assert "_native_ports=" not in result.text
    assert "wf = wf.finalize(PUBLIC_INPUT_METADATA, outputs=[OutputSpec(node=savevideo)])" in result.text


def _output_workflow(output: VibeOutput | None) -> VibeWorkflow:
    workflow = VibeWorkflow("finalizers", WorkflowSource("finalizers"))
    workflow.nodes["1"] = VibeNode("1", "SaveImage")
    workflow.outputs = [] if output is None else [output]
    return workflow


def test_compact_output_node_requires_exactly_inferable_metadata() -> None:
    inferable = VibeOutput(
        "1",
        "SaveImage",
        artifact_kind="image",
        filename_prefix="finalizers",
    )
    assert _v2_output_args(
        _output_workflow(inferable),
        {"1": "save_image"},
        {"output_prefix": "finalizers"},
    ) == ", output_node=save_image"

    explicit_null_prefix = VibeOutput(
        "1",
        "SaveImage",
        artifact_kind="image",
        filename_prefix=None,
    )
    assert _v2_output_args(
        _output_workflow(explicit_null_prefix),
        {"1": "save_image"},
        {"output_prefix": "finalizers"},
    ) == ", outputs=[OutputSpec(node=save_image, output_type='SaveImage', artifact_kind='image')]"


def test_finalizer_preserves_explicit_null_empty_and_ordered_multi_outputs() -> None:
    explicit_null = VibeOutput("1", "SaveImage")
    assert _v2_output_args(
        _output_workflow(explicit_null), {"1": "save_image"}, {}
    ) == ", outputs=[OutputSpec(node=save_image)]"

    assert _v2_output_args(
        _output_workflow(None), {"1": "save_image"}, {}
    ) == ", outputs=[]"

    workflow = _output_workflow(None)
    workflow.outputs = [
        VibeOutput("1", "PreviewImage"),
        VibeOutput("1", "SaveImage"),
    ]
    assert _v2_output_args(workflow, {"1": "save_image"}, {}) == (
        ", outputs=[\n"
        "        OutputSpec(node=save_image, output_type='PreviewImage'),\n"
        "        OutputSpec(node=save_image, output_type='SaveImage'),\n"
        "    ]"
    )
