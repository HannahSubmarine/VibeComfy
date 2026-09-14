"""Structural actor: splice a model-optimization node UPSTREAM of the LoRA loader.

Base template: ``video/wanvideo_wrapper_21_14b_t2v``. The real model chain is

    WanVideoModelLoader(22) -> WanVideoSetLoRAs(58) -> WanVideoSetBlockSwap(56) -> WanVideoSampler(27)

The user wants a model-optimization node (a torch-compile / model-modifier) spliced
onto the BASE model, BEFORE the LoRA loader, so the optimization wraps the full
model+lora stack rather than sitting between the loras and the sampler.

The canonical correct edit attaches ``WanVideoTorchCompileSettings`` to the base
model loader's ``compile_args`` input. This is the node's current schema: it emits
compile settings, and the model loader applies them before emitting the model
consumed by the LoRA loader. The downstream block-swap + sampler chain is left
intact, so the sampler still receives the post-lora model.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from tests.structural_harness.actors import _write_actions, _write_placeholder, _write_workflow_evidence
from vibecomfy import load_workflow_any


def build_m4_wan_t2v_splice_modelpatch_before_loras_evidence(
    report_dir: Path,
) -> dict[str, Any]:
    """Compile-only evidence for splicing a model-patch upstream of the loras."""
    root = report_dir.resolve()
    root.mkdir(parents=True, exist_ok=True)

    workflow = load_workflow_any("video/wanvideo_wrapper_21_14b_t2v")

    # Attach compile settings to the base model loader. The loader applies them
    # before its output enters the LoRA chain (node 58).
    optimization = workflow.node("WanVideoTorchCompileSettings")
    workflow.connect(f"{optimization.id}.0", "22.compile_args")
    workflow.finalize_metadata()

    output_path = root / "outputs" / "video.mp4"
    _write_placeholder(output_path, "structural video placeholder\n")

    evidence = _write_workflow_evidence(
        root=root,
        run_id="m4-wan-t2v-splice-modelpatch-before-loras",
        workflow=workflow,
        output_path=output_path,
        origin=(
            "agentic",
            "tests/structural_harness/actors_m4/wan_t2v_splice_modelpatch_before_loras.py:"
            "build_m4_wan_t2v_splice_modelpatch_before_loras_evidence",
        ),
    )
    _write_actions(
        root / "actions.jsonl",
        [
            {
                "op": "add_node",
                "class_type": "WanVideoTorchCompileSettings",
                "node_id": optimization.id,
                "run_id": evidence.run_id,
                "status": "completed",
            },
            {
                "op": "splice",
                "position": "model_loader_compile_args_before_loras",
                "base_model_node": "22",
                "lora_loader_node": "58",
                "optimization_node": optimization.id,
                "run_id": evidence.run_id,
                "status": "completed",
            },
            {
                "op": "finalize_metadata",
                "run_id": evidence.run_id,
                "status": "completed",
            },
        ],
    )
    (root / "stdout.txt").write_text("", encoding="utf-8")
    (root / "stderr.txt").write_text("", encoding="utf-8")
    (root / "report.md").write_text(
        "Spliced WanVideoTorchCompileSettings onto the base WanVideoModelLoader, "
        "upstream of the LoRA loader, so the optimization wraps the full model+lora "
        "stack while the sampler still receives the post-lora model.\n",
        encoding="utf-8",
    )
    return {
        "scenario": "wan-t2v-splice-modelpatch-before-loras",
        "run_id": evidence.run_id,
        "compiled_api_path": evidence.compiled_api_path,
        "metadata_path": evidence.metadata_path,
        "actions_path": str(root / "actions.jsonl"),
        "output_path": str(output_path),
        "report_path": str(root / "report.md"),
    }
