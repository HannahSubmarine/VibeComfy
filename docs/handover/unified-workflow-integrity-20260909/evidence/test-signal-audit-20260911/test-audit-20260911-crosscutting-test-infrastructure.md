# Crosscutting test-infrastructure quality audit

Planning-only audit of the 159 files in the assigned manifest. No tests were
executed. No product or test files were changed. No `AGENTS.md` exists under
the project tree. The canonical-source-cleanliness direction dated 2026-09-11
is the governing reference: readable generated Python owns runtime values and
topology; a closed v2 `.vibe.json` sibling owns custody and presentation;
legacy embedded-custody expectations are not acceptance criteria for the new
surface.

## Scope and notation

The inventory is assertion-aware but intentionally bounded. I deep-read the
representative/high-risk files called out in the findings and sampled assertion
bodies in the surrounding boundary, emitter, bundle, security, layout, and
test-infrastructure families. The remaining rows are a filename/import/
assertion-pattern inventory, explicitly marked `shallow inventory`; they are
not claims that every assertion in those files was semantically reviewed.

Method: `U` unit, `M` mocked integration, `R` real filesystem/subprocess or
other boundary, `T` static source/AST, `S` snapshot/fixture, `P` property or
law-style, `L` live/native boundary. Relevance: `H` directly exercises the
readable-Python + sibling-JSON + Comfy Node edit pipeline, `A` adjacent
workflow/runtime infrastructure, `I` indirect/low relevance. Depth is `deep`
or `shallow inventory`.

Disposition counts: keep 86; consolidate candidate 32; replace candidate 8;
defer 33. “Replace candidate” means replacement coverage must be landed before
removal or weakening; no deletion is recommended by this audit.

## File-by-file disposition

| File | Behavior/invariant | Method | Relevance | Disposition | Inspection depth |
|---|---|---:|:---:|---|---|
| `tests/characterization/test_compile_api_snapshots.py` | Compiled class types and widget values stay equal to committed sidecars | S/R | H | replace candidate | deep |
| `tests/characterization/test_known_failures_audit.py` | Stale quarantine entries are reported without mutating source files | R | I | keep | deep |
| `tests/pi_transition/bakeoff/test_pi_bakeoff.py` | PI bakeoff scenario comparison and outcome floor | M/R | A | defer | shallow inventory |
| `tests/pi_transition/integration/test_pi_worker_fixtures.py` | Worker fixture lifecycle, transport, and failure receipts | M/R | A | keep | shallow inventory |
| `tests/pi_transition/system/test_pi_edge_cases.py` | System-level PI edge-case terminal states and diagnostics | R | A | defer | shallow inventory |
| `tests/security/test_add_node_gate.py` | Add-node capability decisions and audit records | U | A | keep | shallow inventory |
| `tests/security/test_add_node_provenance.py` | Provenance required for add-node authorization | U | A | keep | shallow inventory |
| `tests/security/test_capabilities.py` | Capability classification and policy defaults | U | A | keep | shallow inventory |
| `tests/security/test_gate.py` | Headless/TTY gate decisions, structured denial, CLI flag parsing | U/R | A | keep | deep |
| `tests/security/test_integration.py` | Security gate integration across commands and side effects | M/R | A | keep | shallow inventory |
| `tests/security/test_loader_gates.py` | Resolved trusted paths, traversal refusal, loader provenance | M/R | H | keep | deep |
| `tests/security/test_no_cross_layer_import.py` | Layer import direction remains clean | T | H | keep | shallow inventory |
| `tests/security/test_provenance.py` | Provenance stamping, validation, and refusal rules | U/T | H | keep | shallow inventory |
| `tests/smoke/test_z_image_only.py` | Minimal z-image workflow smoke and output shape | R/S | H | defer | shallow inventory |
| `tests/test_acceptance.py` | Small acceptance marker/entry-point contract | U | A | consolidate candidate | shallow inventory |
| `tests/test_act1_reply_floor.py` | Agent reply floor and required response fields | U | I | defer | shallow inventory |
| `tests/test_act2_name_domain.py` | Name-domain validation for agent outputs | U | I | defer | shallow inventory |
| `tests/test_act4_emit_ingest.py` | Emit/ingest behavior across authored edit cases | M/R/T | H | keep | shallow inventory |
| `tests/test_adherence_reply_parse.py` | Reply parser adherence and malformed response diagnostics | U | I | defer | shallow inventory |
| `tests/test_analysis.py` | Analysis/diagnostic result shape and classification | U | A | consolidate candidate | shallow inventory |
| `tests/test_api_surface.py` | Public API exports and callable surface | T/U | H | keep | shallow inventory |
| `tests/test_artifact_failed_turn_synthesis.py` | Failed-turn artifact synthesis and safe terminal reporting | U/M | A | defer | shallow inventory |
| `tests/test_batch_e_e2e.py` | Batch edit end-to-end application and receipts | M/R | H | keep | shallow inventory |
| `tests/test_blocks.py` | Block parsing/validation and response boundaries | U | I | consolidate candidate | shallow inventory |
| `tests/test_build_demo_scenario_assets.py` | Demo scenario asset construction | U/R | A | defer | shallow inventory |
| `tests/test_cache_busting.py` | Cache invalidation and stale artifact avoidance | M/R | H | keep | shallow inventory |
| `tests/test_check.py` | Check command result and diagnostics | U/R | A | consolidate candidate | shallow inventory |
| `tests/test_class_inventory_audit.py` | Class inventory completeness and fixture audit | T/R | H | keep | shallow inventory |
| `tests/test_cleanup_surface_manifest.py` | Cleanup surface manifest and allowed residues | T/S | H | keep | shallow inventory |
| `tests/test_cli_affordances.py` | CLI help/options and user-facing affordances | R | A | consolidate candidate | shallow inventory |
| `tests/test_cli_analyze.py` | Analyze CLI output and error contract | R | A | consolidate candidate | shallow inventory |
| `tests/test_cli_debug.py` | Debug CLI routing and output | R/M | A | consolidate candidate | shallow inventory |
| `tests/test_cli_debug_contract.py` | Debug command structured contract | R/T | A | keep | shallow inventory |
| `tests/test_cli_doctor_contract_validate.py` | Doctor contract validation and failure payloads | R/M | A | keep | shallow inventory |
| `tests/test_cli_loader.py` | CLI recipe loading, isolation, and loader failures | R/M | H | keep | shallow inventory |
| `tests/test_cli_misc.py` | Miscellaneous CLI commands and exit/output contracts | R/M | A | consolidate candidate | shallow inventory |
| `tests/test_cli_models_fetch.py` | Model-fetch CLI and request/error behavior | M/R | A | defer | shallow inventory |
| `tests/test_cli_port.py` | Port CLI conversion/edit/export/refusal behavior | M/R/T | H | keep | shallow inventory |
| `tests/test_cli_reorganise.py` | CLI reorganization and layout persistence | R/M | H | consolidate candidate | shallow inventory |
| `tests/test_codemod_hypothesis.py` | Codemod transformations across generated variants | P | H | keep | shallow inventory |
| `tests/test_comfy_backend.py` | Comfy backend adapter and API conversion boundary | M/R | H | keep | shallow inventory |
| `tests/test_comfy_roundtrip_route.py` | Comfy route round-trip and endpoint semantics | R | H | keep | deep |
| `tests/test_comfy_version_compat.py` | Version compatibility and unsupported-version behavior | U/S | H | keep | shallow inventory |
| `tests/test_comparison_leg_isolation.py` | Comparison legs do not contaminate one another | M | A | keep | shallow inventory |
| `tests/test_compile_invariance.py` | Compile parity despite UID/furniture metadata differences | R/S | H | replace candidate | deep |
| `tests/test_contract.py` | Core contract schema and validation | U | H | keep | shallow inventory |
| `tests/test_contract_ir.py` | Contract-to-IR conversion invariants | U | H | keep | shallow inventory |
| `tests/test_contracts_reexport.py` | Contract symbols remain re-exported | T/U | A | consolidate candidate | shallow inventory |
| `tests/test_controlnet_patch.py` | ControlNet patch/edit behavior | M | H | keep | shallow inventory |
| `tests/test_cookbook_imports.py` | Cookbook/example imports remain loadable | R | A | defer | shallow inventory |
| `tests/test_corrective_gate.py` | Corrective gate diagnoses and blocks unsafe changes | U | A | keep | shallow inventory |
| `tests/test_coverage_policy.py` | Coverage policy parsing and enforcement | U/T | I | consolidate candidate | shallow inventory |
| `tests/test_demo_factory_cli.py` | Demo factory CLI creates expected artifacts | M/R | A | defer | shallow inventory |
| `tests/test_demo_factory_creative.py` | Creative demo factory graph shape | U | A | defer | shallow inventory |
| `tests/test_demo_factory_multinode.py` | Multinode demo graph construction | U/M | A | defer | shallow inventory |
| `tests/test_demo_scenarios_routes.py` | Demo route matrices and response contracts | M/R | A | defer | shallow inventory |
| `tests/test_diagnostics.py` | Diagnostic codes and stable detail fields | U | H | keep | shallow inventory |
| `tests/test_doctor_diagnostics.py` | Doctor diagnostics aggregation and rendering | M | A | consolidate candidate | shallow inventory |
| `tests/test_doctor_lockfile.py` | Lockfile doctor checks and repair boundaries | M/R | I | defer | shallow inventory |
| `tests/test_doctor_models.py` | Model doctor discovery and status results | M/R | A | defer | shallow inventory |
| `tests/test_edge_primitives.py` | Edge primitive normalization and types | U | H | keep | shallow inventory |
| `tests/test_embedded_comfy_model_paths.py` | Embedded Comfy model path extraction | T/S | A | keep | shallow inventory |
| `tests/test_ensure_capture.py` | Capture/ensure lifecycle and failure recovery | M/R | H | keep | shallow inventory |
| `tests/test_env_parsing.py` | Environment configuration parsing/defaults | U/M | A | consolidate candidate | shallow inventory |
| `tests/test_environment_diagnostics.py` | Environment diagnostic minimum contract | U | A | consolidate candidate | shallow inventory |
| `tests/test_errors.py` | Error hierarchy, serialization, and messages | U | A | consolidate candidate | shallow inventory |
| `tests/test_exec_normalize.py` | Execution result normalization | U/M | A | keep | shallow inventory |
| `tests/test_exec_spine_failure_kind_classification.py` | Failure-kind classification in execution spine | U | A | keep | shallow inventory |
| `tests/test_felt_fidelity_gate.py` | Felt-fidelity gate protects expected user-visible behavior | M/R | H | keep | shallow inventory |
| `tests/test_fetch.py` | Fetch/cache behavior and failure handling | M/R | A | defer | shallow inventory |
| `tests/test_fix_validation_iter2.py` | Fix validation iteration diagnostics | U/M | A | defer | shallow inventory |
| `tests/test_fixture_provider.py` | Fixture provider resolution, caching, and schema inputs | M/R | H | keep | shallow inventory |
| `tests/test_fixtures.py` | Shared fixture construction and isolation | U/M | H | keep | shallow inventory |
| `tests/test_foundation_utils.py` | Foundation utility invariants | U | A | consolidate candidate | shallow inventory |
| `tests/test_graph_facts.py` | Graph fact extraction and stable facts | U | H | keep | shallow inventory |
| `tests/test_graph_inspection.py` | Graph inspection, links, widgets, and diagnostics | U/S | H | consolidate candidate | shallow inventory |
| `tests/test_h3_generated_editability.py` | H3 public controls, effective wires, and source cleanliness | R/T/S | H | replace candidate | deep |
| `tests/test_handle.py` | Handle construction, outputs, and connection semantics | U | H | keep | shallow inventory |
| `tests/test_harness_common.py` | Harness helper contracts | U | A | consolidate candidate | shallow inventory |
| `tests/test_hivemind_lean_shape.py` | Hivemind lean response shape | M | I | defer | shallow inventory |
| `tests/test_http_security.py` | HTTP security, sanitization, and request boundaries | M/R | A | keep | shallow inventory |
| `tests/test_import_errors.py` | Import failure diagnostics | U/R | A | consolidate candidate | shallow inventory |
| `tests/test_improvement_rc_fixes.py` | Release-candidate regression fixes | M/R/S | H | keep | shallow inventory |
| `tests/test_ir_boundary_kpi.py` | IR boundary KPI measurements and thresholds | U/S | H | keep | shallow inventory |
| `tests/test_ir_laws.py` | IR algebraic/law invariants | P | H | keep | shallow inventory |
| `tests/test_lane_exemption.py` | Lane exemption policy and refusal reasons | U | A | keep | shallow inventory |
| `tests/test_layer4_smoke.py` | Layer-4 smoke path | R | H | defer | shallow inventory |
| `tests/test_local_library.py` | Local library discovery and load behavior | M/R | H | keep | shallow inventory |
| `tests/test_luna_b15_durable_turn.py` | Durable turn persistence/recovery | M/R | A | defer | shallow inventory |
| `tests/test_m1_contracts.py` | M1 contract matrix and source/bundle rules | T/S | H | replace candidate | shallow inventory |
| `tests/test_materialize_filtering.py` | Materialization filtering decisions | U | H | keep | shallow inventory |
| `tests/test_megaplan_chain_spec.py` | Megaplan chain specification shape | U/T | I | defer | shallow inventory |
| `tests/test_memory_profile.py` | Memory profile envelope | R | I | defer | shallow inventory |
| `tests/test_metadata_registration.py` | Metadata registration and lookup | U/M | H | keep | shallow inventory |
| `tests/test_model_assets.py` | Model asset declarations/resolution | M/R | H | keep | shallow inventory |
| `tests/test_native_h3_boundary_mapping.py` | H3 native boundary mapping and ports | S/U | H | keep | shallow inventory |
| `tests/test_node_corpus_builder.py` | Corpus node fixture construction | M/R | H | keep | shallow inventory |
| `tests/test_node_coverage.py` | Node corpus coverage accounting | T/S | H | consolidate candidate | shallow inventory |
| `tests/test_node_shims.py` | Node shim compatibility behavior | U | H | keep | shallow inventory |
| `tests/test_op_validate_known_output.py` | Known output operation validation | U | H | keep | shallow inventory |
| `tests/test_ops.py` | Edit operation primitives | U | H | keep | shallow inventory |
| `tests/test_origin_stamping.py` | Origin/provenance stamping | U/M | H | keep | shallow inventory |
| `tests/test_packaging.py` | Package/build artifact contracts | R/T | A | defer | shallow inventory |
| `tests/test_patches.py` | Patch application and diagnostics | U/M | A | keep | shallow inventory |
| `tests/test_pipeline_health.py` | Pipeline health summary | U | A | consolidate candidate | shallow inventory |
| `tests/test_pipeline_mode_surface.py` | Pipeline mode availability and behavior | M/R | H | keep | shallow inventory |
| `tests/test_pipeline_orchestrate.py` | Pipeline orchestration dispatch | M | A | consolidate candidate | shallow inventory |
| `tests/test_plugin_discovery.py` | Plugin discovery and isolation | M/R | A | defer | shallow inventory |
| `tests/test_port_simulate.py` | Port simulation, preview, and refusal paths | M/R/S | H | keep | shallow inventory |
| `tests/test_position_fidelity.py` | Layout/UID/virtual-wire preservation through edits | U/S/R | H | keep | deep |
| `tests/test_pr_e_validation_repair.py` | PR validation/repair diagnostics | M/R | A | defer | shallow inventory |
| `tests/test_preserve_convergence.py` | Repeated preservation converges | R/S | H | keep | shallow inventory |
| `tests/test_pristine_architecture_guardrails.py` | Architecture/source guardrails and forbidden patterns | T | H | replace candidate | shallow inventory |
| `tests/test_profile_smoke_report.py` | Profile smoke report shape | R | A | defer | shallow inventory |
| `tests/test_provenance.py` | Workflow provenance semantics | U/S | H | keep | shallow inventory |
| `tests/test_quarantine_loader.py` | Quarantine loading and scoped entries | M/R | I | consolidate candidate | shallow inventory |
| `tests/test_quarantine_policy.py` | Quarantine policy decisions | U | I | consolidate candidate | shallow inventory |
| `tests/test_r12_cow_counter_truth.py` | Copy-on-write counter truth and receipts | U/R | A | keep | shallow inventory |
| `tests/test_r9_representation_fidelity.py` | Representation fidelity across conversion | S/R | H | keep | shallow inventory |
| `tests/test_rc_preexisting_unknown_classes.py` | Unknown-class release handling | S/R | H | keep | shallow inventory |
| `tests/test_reconcile.py` | UID/layout reconciliation and edit convergence | U/S | H | keep | shallow inventory |
| `tests/test_recursive_live_contract.py` | Nested native scopes and explicit unsupported live operations | S | H | replace candidate | deep |
| `tests/test_refuse.py` | Refusal diagnostics for unsupported shapes | U/M/R | H | keep | shallow inventory |
| `tests/test_release_guard_four_category.py` | Four-category release guard | T/S | H | keep | shallow inventory |
| `tests/test_research_hivemind_outage.py` | Research-provider outage behavior | M | I | defer | shallow inventory |
| `tests/test_resolution_backends.py` | Resolution backend selection | U/M | H | keep | shallow inventory |
| `tests/test_router.py` | Router dispatch and route errors | U | A | consolidate candidate | shallow inventory |
| `tests/test_routes_session_sanitization.py` | Session route sanitization and isolation | M/R | A | keep | shallow inventory |
| `tests/test_run_command.py` | Run-command subprocess/result contract | M/R | A | keep | shallow inventory |
| `tests/test_s1_persist_landed_delta.py` | Authority receipt rejects false landed edits fail-closed | U | A | keep | deep |
| `tests/test_s2_named_field_emit.py` | Named widget fields replace positional aliases in emitted edits | R/T | H | replace candidate | deep |
| `tests/test_s4_fence_extract.py` | Fence extraction and typed malformed-response classification | U | I | consolidate candidate | deep |
| `tests/test_s5_reroute_leftover_judge.py` | Reroute slots, leftover links, and judge input vocabulary | U/S | H | keep | deep |
| `tests/test_scenario_obligation_preflight.py` | Scenario preflight obligations and refusal evidence | M/R | H | keep | shallow inventory |
| `tests/test_scope.py` | Scope/path containment and scope metadata | U | H | keep | shallow inventory |
| `tests/test_search.py` | Search routing/results and failure handling | M/R | A | defer | shallow inventory |
| `tests/test_semantic_assessor.py` | Semantic assessment and mismatch classification | U/S | H | keep | shallow inventory |
| `tests/test_session_cli.py` | Session CLI lifecycle and edit persistence | M/R | H | keep | shallow inventory |
| `tests/test_sisypy_integration.py` | SisyPy integration boundary | R | A | defer | shallow inventory |
| `tests/test_store_from_ui_json.py` | UI JSON to stable UID/layout store projection | U/R/S | H | keep | deep |
| `tests/test_strict_ready.py` | Strict-ready template contract | T/S | H | keep | shallow inventory |
| `tests/test_strict_ready_gate.py` | Strict-ready gate and diagnostics | U/T | H | keep | shallow inventory |
| `tests/test_success_rate_cli.py` | Success-rate CLI aggregation/report | R | I | defer | shallow inventory |
| `tests/test_terminal_checkpoint.py` | Terminal checkpoint and durable state | M/R | A | keep | shallow inventory |
| `tests/test_testing_api.py` | Testing API public assertions | U | I | keep | shallow inventory |
| `tests/test_testing_assertions.py` | Positive and negative workflow assertion helpers | U | H | keep | deep |
| `tests/test_testing_dry_run.py` | Dry-run command contract | R | I | consolidate candidate | shallow inventory |
| `tests/test_testing_import_cost.py` | Import-cost budget | R | I | defer | shallow inventory |
| `tests/test_testing_pytest_plugin.py` | Pytest plugin registration | U | I | consolidate candidate | shallow inventory |
| `tests/test_testing_snapshot.py` | Snapshot/verify CLI, recipe isolation, and cleanup | R/M/S | H | replace candidate | deep |
| `tests/test_threaded_final_answer_contract.py` | Threaded final answer contract | U | I | defer | shallow inventory |
| `tests/test_ui_layout.py` | UI layout/store/reconcile behavior | U/S/R | H | consolidate candidate | shallow inventory |
| `tests/test_uid_contract.py` | UID creation and contract invariants | U | H | keep | shallow inventory |
| `tests/test_utils.py` | Utility behavior | U | A | consolidate candidate | shallow inventory |
| `tests/test_v24_surface_coverage.py` | v2.4 surface coverage marker | T/S | H | consolidate candidate | shallow inventory |
| `tests/test_vendor_custom_nodes_yaml.py` | Vendor custom-node YAML parsing | T/S | H | keep | shallow inventory |
| `tests/test_walking_skeleton.py` | Walking-skeleton end-to-end workflow | R/S | H | keep | shallow inventory |
| `tests/test_watchdog.py` | Watchdog timeout/retry/terminal behavior | M/R | A | keep | shallow inventory |
| `tests/test_with_import.py` | Import-only smoke module with no test functions | T | I | consolidate candidate | shallow inventory |

## Findings with file:line evidence

### 1. Embedded-custody expectations must be replaced, not simply deleted

`tests/test_h3_generated_editability.py:63-87` parses one generated fixture and
only forbids `_native_subgraph_source`, `_ui_door`, `nodes`, `links`, and
`boundary` in `ReadyMetadata`; it explicitly permits
`_native_subgraph_provenance` and `_native_subgraph_diagnostics`. More
importantly, `:55-60` documents and asserts legacy importer-shaped input pairs,
`len(workflow.edges) == 19`, and `len(references) >= 20`. That is useful
compatibility evidence, but it is not proof of the new whole-file cleanliness
contract or v2 pair loading. The replacement criterion is an AST/declaration
content test over the complete generated module plus a staged
`workflow.py`/`workflow.vibe.json` load: reject renamed/disguised custody,
inline loaders, raw replay links, duplicate runtime authority, and sibling
wrapper files while proving exact semantic edges and editable controls.

`tests/characterization/test_compile_api_snapshots.py:28-49` protects only two
compiled projections (class types and widget values). It preserves useful
characterization drift detection, but cannot certify deterministic v2 JSON,
custody closure, topology, provenance, outputs, or presentation. Keep the
unique sidecar drift oracle as a lower-level snapshot and replace its role as a
canonical acceptance gate with semantic/identity/pair assertions.

`tests/test_compile_invariance.py:53-95,144-194` is valuable for compile
equivalence and metadata stripping, but its current contract compares API
outputs and explicitly drops `_meta`; it does not establish external custody,
preconstruction sidecar validation, or mixed-generation refusal. Retain the
compile law, add the v2 pair oracle, and do not treat API equality as sufficient
for identity/provenance/presentation fidelity.

### 2. Several source assertions are string-window heuristics with weak or
duplicated oracles

`tests/test_s2_named_field_emit.py:36-59` searches emitted source by a line
containing a class name and inspects a fixed ten-to-twelve-line window. The
UltraShape assertion at `:47` is especially weak (`"guidance_scale=5" in
snippet or "guidance_scale" in snippet`), and the suite mostly proves that a
`widget_N` token is absent rather than that the named field maps to the correct
node/input/value and survives a rebuild. Preserve the unique named-field and
range-vocabulary protections, but replace source-window checks with AST calls
and an independent reconstructed-graph oracle, including ambiguous frontend
positions and frozen resolver evidence.

The same principle applies to `tests/test_h3_generated_editability.py:76-87`:
negative substring checks are useful mutation probes, but they need declaration
content traversal and structural reasons. Do not consolidate these into a
generic “no widget_N” count; field-name mapping is a distinct protection.

### 3. Positive infrastructure exists, but live/boundary coverage is visibly
missing in the exact places the direction calls high risk

`tests/test_recursive_live_contract.py:30-57` validates a checked-in fixture
whose `capture_status` is explicitly `"undetermined"`, then
`:60-81` proves an unsupported inner mutation refuses without changing the
fixture. `:84-92` records that serialize/reload is not captured without a live
graph export. This is honest and should remain as an intentional-refusal
oracle, but it is not nested live-boundary coverage. Add a fixture-backed
native/frontend boundary test for definition discovery, depth-two construction,
interface/fanout/output slots, and reload; retain the refusal test for absent
live bytes.

`tests/test_store_from_ui_json.py:223-235` calls its corpus check a
“round_trip” but asserts only that top-level values have the expected types and
keys. The detailed UID, group, virtual-wire, and unresolved-endpoint assertions
at `:53-202` are real protections and should be preserved. Replace the weak
corpus smoke with exact canonicalized envelope equality (including authored
notes/annotations once v2 supports them), deterministic regeneration, and
malformed-reference refusal.

`tests/test_testing_snapshot.py:42-79` mostly asserts subprocess return code and
that two snapshot payloads agree; `:92-168` does add meaningful same-stem
isolation, cleanup, neutral-CWD, and directive checks. The return-code-only
checks should be consolidated around a small command contract helper, while
the recipe/sibling-pair cases become v2 pair tests. Preserve the unique module
cleanup assertion at `:125-135` and uncatalogued-template refusal at
`:172-198`.

### 4. Large suites contain unique high-signal protections but are
consolidation candidates by responsibility, not by assertion count

`tests/test_position_fidelity.py` is 1,129 lines, yet its exact UID/position/
size/virtual-wire and no-inheritance assertions (for example `:250-287`,
`:343-391`, `:468-497`, and `:648-726`) protect layout semantics that should
not be dismissed as “mock/count noise.” Consolidate only shared setup and
duplicate round-trip scaffolding; retain independent edit-invariance,
JSON-only collaboration, duplicate/twin identity, note preservation, and
fresh-layout protections.

Likewise, `tests/test_ir_laws.py` (law-style), `tests/test_graph_inspection.py`,
`tests/test_ui_layout.py`, `tests/test_cli_port.py`, `tests/test_fixture_provider.py`,
and `tests/test_improvement_rc_fixes.py` are broad ownership suites. Their
potential consolidation is about moving cases to focused owners and reducing
fixture duplication, not deleting assertions merely because they use mocks,
counts, or repeated setup.

### 5. Security and authority tests have strong independent protections

`tests/security/test_loader_gates.py:59-112` proves resolved trusted-dir
classification and traversal refusal, while `:118-177` exercises trusted and
attacker-controlled loader paths under a headless gate. The explicit string
prefix counterexample at `:88-96` is a good independent oracle, not noise.
`tests/test_s1_persist_landed_delta.py:58-148` checks that gate/debug claims
cannot override a replay mismatch and that candidate/graph data is removed on
authority rejection. Keep these tests and reuse their fail-closed style for
missing/malformed/stale/mixed-generation v2 companions.

## Focused high-signal replacement plan

Tier 1 — required before the amendment can be accepted:

1. Whole-file generated-source AST checker: declarations, nested definitions,
   metadata, finalizer, imports, raw IDs/links, inline loaders, disguised
   custody dictionaries, duplicate runtime values, and executable sibling
   wrappers. Each mutation must fail for a structural reason.
2. Closed v2 bundle parser/property matrix: unknown keys/version, duplicate JSON
   keys, non-finite numbers, duplicate labels, scope-local one-to-one coverage,
   invalid native ports, presentation foreign keys, digest/generation mismatch.
   Use an independent canonical JSON oracle rather than only round-tripping the
   implementation's own serializer.
3. Pair boundary matrix through direct bundle load, registry/restricted load,
   and copy-to-recipe: missing sidecar, malformed sidecar, stale/mixed
   generation, and failed second replacement must leave destinations unchanged.
4. Editable-value regression: H3 prompt/model/seed/mask/duration/audio edits
   rebuild with unchanged custody; compare semantic IR, IDs/UIDs, native ports,
   provenance, public inputs, outputs, helpers, and presentation separately.
5. Output contract matrix: explicit one-output, zero-output, and ordered
   multi-output; prove no silent autodetection for explicit no-output.

Tier 2 — high-value fidelity and resolver coverage:

1. Flat, unknown-schema, multi-output, and depth-two nested representative
   workflows with a source-vs-importer trace and intentional refusals.
2. Fixture-backed widget-position resolution with exact pack/class/revision
   provenance, frontend-added controls, ambiguous/conflicting evidence, and a
   frozen no-network rebuild.
3. Presentation annotations: exact authored Markdown/Unicode/empty text,
   scope-qualified identity, definition-vs-instance isolation, edit/save/reload,
   deterministic regeneration, malformed references, and semantic invariance.
4. Independent Comfy boundary parity: compare reconstructed workflow semantics
   to a separately normalized API/UI oracle; do not compare serializer output to
   itself.

Tier 3 — consolidation and maintenance:

1. Move repeated CLI exit/payload assertions to one contract helper while
   retaining command-specific routing assertions.
2. Share fixture builders and canonicalization utilities across layout,
   snapshot, port, and graph suites; retain distinct ownership and negative
   cases.
3. Quarantine/defer low-relevance agent-reply, research-provider, performance,
   and demo-only suites from the v2 acceptance gate, without deleting them.

## Omitted/under-covered invariants

- Whole-file cleanliness against renamed/disguised custody and nested replay;
  current checks are mostly names/substrings or a single H3 fixture.
- Required companion resolution before the first constructor and fail-closed
  no-mutation behavior for malformed, stale, or mixed-generation pairs.
- Deterministic generation identity and custody digest semantics independent of
  current editable Python bytes.
- Atomic/recoverable two-file replacement interleavings and rollback failure.
- Exact v2 closed-schema validation, duplicate JSON-key rejection, and
  complete scope-local binding coverage.
- Explicit zero-output versus unspecified output and ordered multi-output slots.
- Independent parity of semantic graph, IDs/UIDs, native ports, provenance,
  helpers, model assets, and presentation; API snapshots cover only projections.
- Depth-two live native boundary capture/reload and nested annotation identity.
- Proven widget position/name mapping with pinned source/schema evidence and
  no-network frozen rebuilds; “widget_N absent” is not enough.
- Exact note/annotation content and role separation from runtime note nodes.
- Registry, restricted loader, and copy-to-recipe exercising the same canonical
  pair owner.

## Final state

All 159 assigned manifest files are categorized. Counts are: 86 keep, 32
consolidate candidates, 8 replace candidates, and 33 defer. The strongest
recommendation is not broad test deletion: preserve the unique semantic,
security, UID/layout, refusal, and law protections; replace only stale
embedded-custody acceptance with a v2 pair/cleanliness matrix; consolidate
shared scaffolding and low-signal command repetition after replacement coverage
exists.
