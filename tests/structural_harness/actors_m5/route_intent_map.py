"""M5 route-intent map evidence builder.

Runs the canonical four-route taxonomy deterministically through the executor
with fake classifications and freezes the resulting executor envelopes so the
rubric can verify route → phase gates → Apply eligibility.
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any
from unittest import mock

from tests.structural_harness.actors import _write_command_log_jsonl
from vibecomfy.executor.agent_research_stage import AgentResearchTrace
from vibecomfy.executor.contracts import (
    ClassifyDecision,
    ExecutorRequest,
    ExecutorHostPorts,
    ImplementationResult,
)
from vibecomfy.executor.core import run_executor
from vibecomfy.executor.evidence_pack import EvidencePack


def _fake_classify_for_route(expected_route: str, intent: str, task: str) -> Any:
    """Return a fake classify side effect for the given canonical route."""
    def _classify(
        query: str,
        *,
        route: str = "",
        model: str = "",
        has_graph: bool = False,
        graph_summary: str | None = None,
        **kwargs: Any,
    ) -> ClassifyDecision:
        return ClassifyDecision(
            research=expected_route == "adapt",
            implement=expected_route in {"revise", "adapt"},
            reply=True,
            effort="low" if expected_route in {"clarify", "revise"} else "medium",
            plan_summary=f"{expected_route} plan",
            intent=intent,
            route=expected_route,
            task=task,
        )
    return _classify


def _fake_reply(
    *_args: Any,
    plan: ClassifyDecision | None = None,
    **_kwargs: Any,
) -> str:
    return f"reply for {plan.route if plan else 'unknown'}"


def _fake_handle_agent_edit(payload: dict[str, Any], **kwargs: Any) -> dict[str, Any]:
    return {
        "graph": payload.get("graph"),
        "message": "Edited graph.",
    }


def _fake_agent_research(
    *,
    route: str,
    question: str,
    spec: Any | None = None,
    **_kwargs: Any,
) -> tuple[AgentResearchTrace, EvidencePack]:
    """Stub the ACTIVE C1 research seam with a minimal inert trace + pack."""
    return (
        AgentResearchTrace(
            route=route,
            question=question,
            iterations=(),
            final_verdict="enough",
            summary="Synthetic route-intent research.",
            citations=(),
            uncertainty="",
            status="ok",
            elapsed_seconds=0.0,
        ),
        EvidencePack(),
    )


def _fake_implementation(
    request: ExecutorRequest,
    *_args: Any,
    **_kwargs: Any,
) -> ImplementationResult:
    return ImplementationResult(message="Edited graph.", graph=request.graph)


def _structural_host_ports() -> ExecutorHostPorts:
    """Return deterministic host seams for this fully synthetic actor.

    The route map patches every model/implementation seam.  It must therefore
    not lazily construct the production ComfyUI adapter: that adapter owns
    process-wide capture and session state which unrelated tests may have
    replaced.  Keeping the synthetic actor on the neutral host contract makes
    the evidence builder repeatable in the full suite as well as in isolation.
    """
    def unused(*_args: Any, **_kwargs: Any) -> Any:
        raise AssertionError("unused synthetic host operation")

    return ExecutorHostPorts(
        handle_agent_edit=unused,
        payload_hash=lambda _payload: "synthetic-route-intent-hash",
        classify_failure=unused,
        failure_envelope=unused,
        begin_deepseek_usage_capture=lambda: "synthetic-usage",
        snapshot_deepseek_usage_capture=lambda: ({}, True),
        end_deepseek_usage_capture=lambda _token: None,
        begin_model_attempt_capture=lambda: "synthetic-attempts",
        snapshot_model_attempt_capture=lambda: (),
        end_model_attempt_capture=lambda _token: None,
    )


def build_m5_route_intent_map_evidence(report_dir: Path) -> dict[str, Any]:
    """Freeze executor envelopes for all four canonical routes."""
    root = report_dir.resolve()
    root.mkdir(parents=True, exist_ok=True)

    cases = [
        ("clarify", "respond", "respond", "make it more cinematic"),
        ("inspect", "explain_graph", "inspect_graph", "what does this workflow do?"),
        ("revise", "edit", "edit_graph", "change the seed to 42"),
        ("adapt", "edit", "research_precedent", "add the Wan control LoRA chain"),
    ]

    records: list[dict[str, Any]] = []
    for route, intent, task, query in cases:
        classify_fn = _fake_classify_for_route(route, intent, task)
        request = ExecutorRequest(
            query=query,
            graph={"nodes": [{"id": 1, "class_type": "KSampler"}]},
            profile="default",
            # This actor patches the staged executor seams below.  Declare the
            # matching mode at the request boundary so evidence is independent
            # of any ambient pipeline-mode setting left by another scenario.
            pipeline_mode="staged",
        )
        # Patch the globals used by the imported ``run_executor`` function,
        # rather than resolving a possibly reloaded module by import path.
        # Some preceding contract tests deliberately reload executor modules;
        # path-based patches can then miss the function's original globals and
        # accidentally dispatch a real provider from this synthetic actor.
        with mock.patch.dict(
            run_executor.__globals__,
            {
                "run_classify_turn": mock.Mock(side_effect=classify_fn),
                "run_reply_turn": mock.Mock(side_effect=_fake_reply),
                "run_agent_research_stage": mock.Mock(side_effect=_fake_agent_research),
                "_run_implement": mock.Mock(side_effect=_fake_implementation),
            },
        ):
            result = run_executor(request, host_ports=_structural_host_ports())

        records.append({
            "expected_route": route,
            "query": query,
            "result_route": result.turn.route,
            "research": result.report.plan.research,
            "implement": result.report.plan.implement,
            "apply_eligible": result.turn.apply_eligible,
            "no_candidate_reason": result.turn.no_candidate_reason,
            "ok": result.ok,
        })

    route_map_path = root / "route_intent_map.json"
    route_map_path.write_text(json.dumps(records, indent=2), encoding="utf-8")

    actions_path = root / "actions.jsonl"
    actions_path.write_text(
        "\n".join(
            json.dumps({
                "op": "route_intent_map",
                "route": r["expected_route"],
                "result_route": r["result_route"],
                "apply_eligible": r["apply_eligible"],
            })
            for r in records
        )
        + "\n"
        + json.dumps({"op": "finalize_metadata", "status": "completed"})
        + "\n",
        encoding="utf-8",
    )

    ts = time.time()
    _write_command_log_jsonl(
        root / "command_log.jsonl",
        [
            {
                "ts": ts + index * 0.1,
                "command": "executor",
                "argv": ["executor", "route-intent", record["expected_route"]],
                "exit_code": 0,
                "summary": (
                    "Synthetic: executor produced "
                    f"{record['result_route']} with apply_eligible={record['apply_eligible']}"
                ),
            }
            for index, record in enumerate(records)
        ],
    )

    (root / "report.md").write_text(
        "Deterministic route-intent map for clarify/inspect/revise/adapt.\n",
        encoding="utf-8",
    )

    return {
        "scenario": "route-intent-map",
        "route_map_path": str(route_map_path),
        "actions_path": str(actions_path),
        "command_log_path": str(root / "command_log.jsonl"),
        "report_path": str(root / "report.md"),
    }
