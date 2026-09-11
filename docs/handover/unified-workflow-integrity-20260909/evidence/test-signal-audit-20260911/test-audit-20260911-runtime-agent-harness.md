# Test quality audit: runtime-agent-harness

Planning-only audit of the 143 manifest-assigned files. No tests were run or
collected. No product/test files were changed. The inventory below is based on
reading test names, fixtures, setup, and assertion bodies; `S` means shallow
inventory (names/assertion shape, not every branch), and `D` means deeper
inspection of representative/high-risk assertions. Method labels are the
dominant oracle, not a claim that every test in a file has one method.

The relevant direction is the 2026-09-11 canonical pair: readable generated
Python owns values/topology/inputs/output; sibling `.vibe.json` owns closed,
non-executable custody and presentation; loading/editing/publication must be
fail-closed and atomic. The audit therefore weights tests that prove readable
Python plus sibling JSON remains the authority through the Comfy Node edit
pipeline, while retaining harness, security, provenance, and runtime boundary
protections.

## Complete assigned-file inventory

| file | behavior / invariant | method | relevance to readable Python + sibling JSON and edit pipeline | disposition | depth |
|---|---|---|---|---|---|
| `tests/characterization/test_agent_edit_roundtrips.py` | ingress snapshot/commit roundtrip preserves expected graph | mocked integration | Direct edit-kernel compatibility; useful baseline for Python-derived graph | keep | D |
| `tests/intent/smoke/test_judge_calibration.py` | six calibration panels map to expected pass verdicts | live | Indirect assessor confidence, not custody | defer | S |
| `tests/intent/smoke/test_render_diff_runpod.py` | changed render differs; unchanged render matches | live | Output-level signal for value edits, weak topology authority | keep | S |
| `tests/intent/test_falsification.py` | faithful-but-wrong fixtures are allowed by refusal spine | unit | Protects honest distinction between edit validity and visual correctness | keep | S |
| `tests/intent/test_judge_text_offline.py` | text judge criteria, prompt shape, iff aggregation | mocked integration | Assessor only; must not become publication authority | keep | D |
| `tests/intent/test_panel_aggregation.py` | text/vision conjunction and sub-verdict retention | unit | Preserves independent assessment signals | keep | S |
| `tests/intent/test_phash.py` | calibration separates near/different pairs | unit/property | Useful output regression, not readable-source custody | keep | S |
| `tests/intent/test_render_diff_structural.py` | structural hash and seed mutation behavior | unit | Detects value/topology deltas without runtime; complementary oracle | keep | D |
| `tests/intent/test_static_lowering.py` | loop discovery, cloning, links, atomic failures, deterministic layout | unit/property | High relevance to readable constructors and graph edit lowering | keep | D |
| `tests/intent/test_tripwire.py` | forbidden imports stay out of judge/render-diff one-hop closure | static source | Prevents assessor from acquiring execution authority | keep | S |
| `tests/security/test_agent_context_boundary.py` | untrusted text is tainted while schema/agent-authored fields stay usable | unit | Protects hostile readable source/context handling | keep | D |
| `tests/security/test_agent_generated_loader.py` | scan-before-exec, gate, provenance, hostile source rejection | mocked integration/static source | Direct source loading boundary; extend for required sibling JSON | keep | D |
| `tests/security/test_runtime_code_policy.py` | forbidden calls rejected before subprocess; JSON subset remains | static source/unit | Runtime sandbox boundary for generated Python | keep | S |
| `tests/smoke/test_layer2_runpod_dropped.py` | remote dropped-template output is empty and exits cleanly | live | Real Comfy boundary smoke; low diagnostic specificity | defer | S |
| `tests/smoke/test_layer2_runpod_matrix.py` | remote family matrix completes without failures | live | Broad node/runtime compatibility signal | defer | S |
| `tests/smoke/test_layer2_runpod_ops.py` | remote layer2 ops produce declared output marker | live | Real execution transport protection | keep | S |
| `tests/smoke/test_p1_runpod.py` | typed-handle image workflow runs remotely | live | Strong end-to-end constructor/handle smoke | keep | S |
| `tests/structural_harness/test_runner_exit_code.py` | fake/no-op and assessment outcomes map to exit codes | mocked integration | Prevents harness from declaring fake success | keep | D |
| `tests/test_additive_witness_oracle.py` | broken/wrong/decoy graphs rejected; valid additive and exact cases accepted | unit/property | Independent graph oracle for edit candidate integrity | keep | D |
| `tests/test_admission_witness_artifact_transport.py` | witness/envelope lineage survives child copy and rejects tampering | mocked integration | Direct custody/admission chain protection | keep | D |
| `tests/test_agent_acceptance.py` | indexed discovery, inspect/compile, dry-run and metadata artifact shape | mocked integration | Pipeline admission and readable workflow evidence | keep | D |
| `tests/test_agent_contract_codegen.py` | generated JS matches generator; no golden fixture dependency | static source | Source-generation contract, peripheral to Python pair | keep | S |
| `tests/test_agent_edit_artifact_replay.py` | canonical ops, identity, schema envelope, replay parity and rejection | unit/property | Core edit pipeline; high-value identity and fail-closed coverage | keep | D |
| `tests/test_agent_edit_compatibility_ledger.py` | retained aliases are allowlisted and bounded to backend | static source | Prevents legacy compatibility from overriding canonical source | keep | D |
| `tests/test_agent_edit_parameter_tweak_fallback.py` | advisory ranking requires explicit agent call and bounded enums | unit | Protects explicit edit intent and readable values | keep | S |
| `tests/test_agent_edit_provenance_evidence.py` | deleted research/prefetch contracts stay deleted; active shape agent-owned | static source | Keeps source authority clean; indirect | keep | S |
| `tests/test_agent_edit_safety.py` | agentic edit preserves invariants and deterministic output | mocked integration | Broad edit safety regression | keep | S |
| `tests/test_agent_edit_settings_contract.py` | schema-derived seven settings, enum validation, batch edits/rollback | unit | Direct readable control edit coverage; preserve unique fields | consolidate candidate | D |
| `tests/test_agent_execution_plan_hydration.py` | nested plan hydration/provenance/artifact persistence | mocked integration | Runtime plan continuity after source edits | keep | S |
| `tests/test_agent_executor_durable.py` | durable module boundaries, idempotency and artifact delegation | mocked integration/static source | Durable edit response and no duplicate turns | keep | D |
| `tests/test_agent_executor_response.py` | serializers strip authority from non-applyable responses | unit | Prevents response payload becoming source/custody authority | keep | D |
| `tests/test_agent_executor_routes.py` | intent route truth tables, detector, authority parity | unit/mocked integration | Entry routing to inspect/revise/adapt/research | consolidate candidate | S |
| `tests/test_agent_headless_import_boundaries.py` | headless imports avoid forbidden/UI modules | static source | Keeps runtime loading separable from UI | keep | S |
| `tests/test_agent_layout_reorganisation.py` | layout-only reorganize and presentation identity | mocked integration | JSON presentation projection, must not alter Python semantics | keep | S |
| `tests/test_agent_obligation_ledger.py` | obligations/claims require evidence and bounded statuses | unit | Admission/publication evidence discipline | keep | S |
| `tests/test_agent_research_contribution_settings.py` | research contribution settings shape and fields | unit | Peripheral metadata; no runtime authority | defer | S |
| `tests/test_agent_research_shadow.py` | research shadow routing, provenance, fallback and isolation | mocked integration | Keeps research advisory and separate from edit authority | consolidate candidate | S |
| `tests/test_agent_route_families.py` | route-family canonicalization and research/edit families | unit | Entry-point behavior; preserve unique route boundaries | consolidate candidate | S |
| `tests/test_agent_runtime_adapter.py` | runtime adapter lifecycle, metadata, errors, output handling | mocked integration | Runtime execution boundary for readable workflow | keep | S |
| `tests/test_agent_runtime_probe_gate.py` | runtime probe gate decisions and failure diagnostics | mocked integration | Preflight before Comfy execution | keep | S |
| `tests/test_agent_skill_sync.py` | skill synchronization/manifest shape | static source | Tooling metadata only | defer | S |
| `tests/test_agent_tool_surface.py` | tool registration, schemas, route/authority exposure | static source/unit | API surface for edit pipeline | consolidate candidate | S |
| `tests/test_agentic_harness_live.py` | live harness actor/run basic contract | live | Real agent boundary, expensive and low local determinism | defer | S |
| `tests/test_agentic_reorganise_layout.py` | agentic layout reorganization result shape | mocked integration | Presentation-only pipeline | consolidate candidate | S |
| `tests/test_agentic_replay_routes.py` | replay route selection and response handling | mocked integration | Replay must use retained authority | keep | S |
| `tests/test_artifact_lineage_manifest.py` | artifact lineage manifest fields and consistency | unit | Publication custody/provenance | keep | D |
| `tests/test_authority_nonapply_terminal.py` | non-apply authority terminal states are explicit | unit | Fail-closed response boundary | keep | S |
| `tests/test_authority_receipts.py` | receipt identity, evidence, and terminal transitions | mocked integration | Publication/admission custody | keep | D |
| `tests/test_authority_replay_name_domain.py` | replay names/domains remain bound and reject foreign values | unit | Prevents cross-publication replay | keep | S |
| `tests/test_authority_replay_sequential.py` | sequential replay authority and order | unit | Edit ordering and retained authority | keep | S |
| `tests/test_b02_rich_preservation.py` | rich graph fields survive transformations | unit | Preserves readable graph semantics through edits | keep | S |
| `tests/test_b11b_execution_projection.py` | execution projection maps graph/outputs/metadata | mocked integration | Python semantic graph to Comfy API | keep | D |
| `tests/test_b14_clone_lifecycle.py` | clone lifecycle and identity preservation | unit | Lowering/edit graph integrity | keep | S |
| `tests/test_b18_browser_contract.py` | browser contract fields exist | static source | Peripheral transport contract | defer | S |
| `tests/test_conftest_runpod_markers.py` | runpod markers/configuration are present | static source | Test selection hygiene only | defer | S |
| `tests/test_demo_factory_structural_baseline.py` | demo factory structural baseline remains stable | snapshot/static source | Representative readable graph baseline | keep | S |
| `tests/test_execution_plan_contracts.py` | execution plan schemas and serialization contracts | unit | Runtime plan survives edits/publication | keep | S |
| `tests/test_execution_plan_evaluator.py` | evaluator classifies plan outcomes | unit | Execution decision boundary | keep | S |
| `tests/test_execution_plan_runtime.py` | runtime plan execution and failures | mocked integration | Comfy execution plan boundary | keep | S |
| `tests/test_execution_spine_shim_disposition.py` | legacy spine shim disposition and boundaries | static source | Prevents old authority path re-entry | keep | S |
| `tests/test_executor_classify_only.py` | classify-only responses have no apply side effects | unit | Explicit non-mutating route | keep | S |
| `tests/test_executor_compare_pipeline_retry.py` | compare pipeline retry/terminal result semantics | mocked integration | Assessor retry must not mutate source | keep | S |
| `tests/test_executor_contracts.py` | executor stage/request/result contracts | unit | Broad orchestration contract; overlapping with flows | consolidate candidate | S |
| `tests/test_executor_edit_suggestion_tools.py` | suggestion tools and bounded edit payloads | mocked integration | Explicit readable value edit surface | keep | S |
| `tests/test_executor_flows.py` | end-to-end executor flow families and error paths | mocked integration | Broad pipeline coverage; likely duplicate contract assertions | consolidate candidate | S |
| `tests/test_executor_hivemind_messages.py` | research message serialization | unit | Advisory research only | defer | S |
| `tests/test_executor_hivemind_tools.py` | research tool calls and result handling | mocked integration | Advisory path isolation | consolidate candidate | S |
| `tests/test_executor_host_boundary.py` | host boundary rejects/contains invalid calls | unit | External execution boundary | keep | S |
| `tests/test_executor_inventory_feedback.py` | inventory feedback and missing-node outcomes | mocked integration | Node availability informs edit planning | keep | S |
| `tests/test_executor_layout_hints.py` | layout hints remain presentation metadata | unit | Sibling JSON presentation relevance | keep | S |
| `tests/test_executor_lookup_tools.py` | lookup tool routing/results/errors | mocked integration | Advisory node/schema lookup; no source authority | consolidate candidate | S |
| `tests/test_executor_profiles.py` | executor profile selection/configuration | unit | Runtime policy | defer | S |
| `tests/test_executor_research_identity.py` | research identity/provenance remains stable | unit | Provenance support, non-semantic | keep | S |
| `tests/test_executor_stage_contracts.py` | stage contract/result invariants | unit | Orchestration correctness | consolidate candidate | S |
| `tests/test_executor_threaded_contracts.py` | threaded executor request/response contracts | unit | Durable agent pipeline | keep | S |
| `tests/test_executor_threaded_edits.py` | threaded edit lifecycle and authority | mocked integration | Direct edit path | keep | S |
| `tests/test_executor_threaded_mode.py` | threaded mode routing and persistence | mocked integration | Runtime agent mode boundary | keep | S |
| `tests/test_executor_threaded_sessions.py` | threaded session state transitions | mocked integration | Durable execution state | keep | S |
| `tests/test_executor_verbatim_query.py` | user query preserved verbatim | unit | Readable intent fidelity | keep | S |
| `tests/test_executor_web_tools.py` | web tool routing and bounded responses | mocked integration | Advisory external lookup; not custody | defer | S |
| `tests/test_headless_agent_artifacts.py` | headless artifacts, reports, provenance and files | mocked integration | Publication and restricted loading evidence | keep | D |
| `tests/test_headless_agent_astrid_subprocess_smoke.py` | subprocess headless smoke | live | Real boundary smoke | defer | S |
| `tests/test_headless_agent_cli.py` | CLI options, errors, artifact output | unit/mocked integration | Operational entrypoint | keep | S |
| `tests/test_headless_agent_contracts.py` | headless request/result contracts | unit | Source loading/execution contract | keep | S |
| `tests/test_headless_agent_service.py` | service lifecycle and response failures | mocked integration | Agent runtime boundary | keep | S |
| `tests/test_headless_harness_contract.py` | harness scenario/adapter/evidence contracts | static source/unit | Evidence boundary for agent claims | keep | S |
| `tests/test_headless_harness_runner_contract.py` | runner contract, exit and persistence | unit/mocked integration | Harness result integrity | keep | S |
| `tests/test_headless_harness_scenarios_contract.py` | scenario descriptor contracts | static source | Harness coverage selection | defer | S |
| `tests/test_intent_judge_delta_replay_canon.py` | judge replay canonicalization and delta interpretation | unit | Independent assessment of edit delta | keep | S |
| `tests/test_intent_nodes.py` | intent node fixture/semantic operations | mocked integration | Node-level edit intent | keep | S |
| `tests/test_live_agentic_assessor.py` | live assessor output/contract | live | Real model boundary; expensive | defer | S |
| `tests/test_live_agentic_assessor_score_honesty.py` | assessor score honesty and evidence grounding | live | Protects evidence-vs-narrative honesty | keep | S |
| `tests/test_live_agentic_failure_analysis.py` | live failure analysis classification | live | Diagnostics only | defer | S |
| `tests/test_live_agentic_harness.py` | live harness basic execution | live | Real agent boundary | defer | S |
| `tests/test_live_agentic_harness_corpus_manifest.py` | live corpus manifest completeness | static source | Scenario coverage metadata | keep | S |
| `tests/test_live_agentic_harness_guard_contract.py` | guard rejects fake/live/category and evidence mismatches | static source/mocked integration | Strong anti-fake evidence gate | keep | D |
| `tests/test_live_agentic_harness_runner.py` | runner dispatch and result shape | mocked integration | Harness orchestration | consolidate candidate | S |
| `tests/test_live_agentic_harness_runner_persistence.py` | persistence placeholder/no substantive assertions | unit | No meaningful current protection | replace candidate | D |
| `tests/test_live_agentic_harness_runner_timeout.py` | timeout cleanup/bounds and result persistence | mocked integration | Runtime safety and durable terminal state | keep | S |
| `tests/test_live_agentic_output_containment.py` | output remains inside declared evidence roots | unit | Publication/artifact custody | keep | S |
| `tests/test_live_agentic_runner_persistence.py` | persistence, resume, corruption, atomic writes | mocked integration | Durable harness evidence | keep | S |
| `tests/test_live_agentic_source_layouts.py` | source layout discovery variants | static source | Readable Python layout support | keep | S |
| `tests/test_live_agentic_split_finale.py` | split finale/terminal evidence | mocked integration | End-state evidence integrity | keep | S |
| `tests/test_live_agentic_threaded_comparison.py` | threaded comparison and consensus | mocked integration | Independent oracles around edits | keep | S |
| `tests/test_live_agentic_watchdog.py` | watchdog timeout/termination | mocked integration | Runtime boundary | keep | S |
| `tests/test_p1_replay_domain.py` | replay domain restrictions | unit | Cross-publication edit safety | keep | S |
| `tests/test_p3_signature_literals.py` | signature/source literal contract | static source | Generated/readable source shape | keep | S |
| `tests/test_p5_accepted_batch_terminal.py` | accepted batch terminal evidence | mocked integration | Publication terminal state | keep | D |
| `tests/test_p6_corpus_orphan.py` | orphan corpus detection | static source | Harness fixture hygiene | defer | S |
| `tests/test_p7_lineage_evidence_abort.py` | lineage abort paths fail closed | mocked integration | Direct custody safety | keep | D |
| `tests/test_p7_lineage_evidence_digest.py` | lineage digest consistency | unit | Publication identity | keep | S |
| `tests/test_runpod_acceptance.py` | remote acceptance marker/output contract | live | Real Comfy boundary | defer | S |
| `tests/test_runpod_bundle_adapter.py` | RunPod bundle/config adapter | mocked integration | Transport of readable workflow artifacts | keep | S |
| `tests/test_runpod_matrix.py` | remote route/family matrix and output evidence | live | Broad compatibility, low local diagnostic value | defer | S |
| `tests/test_runpod_runner.py` | remote runner lifecycle/retry/cleanup | mocked integration | Real transport orchestration | keep | S |
| `tests/test_runpod_setup.py` | remote setup/warmup and credentials | mocked integration | Boundary setup and secret hygiene | keep | S |
| `tests/test_runtime_b09_config.py` | B09 runtime configuration fields | unit | Runtime configuration, not source custody | defer | S |
| `tests/test_runtime_code_modes.py` | allowed/rejected runtime code modes | static source/unit | Generated Python execution policy | keep | S |
| `tests/test_runtime_doctor.py` | doctor diagnoses environment/config | unit | Operational preflight | defer | S |
| `tests/test_runtime_ensure_env.py` | environment/model/node ensuring and rollback | mocked integration | Runtime prerequisites for Comfy edit execution | keep | S |
| `tests/test_runtime_eval.py` | safe runtime evaluation and result handling | mocked integration | Readable Python execution boundary | keep | S |
| `tests/test_runtime_eval_absence.py` | absent runtime evaluator fails/omits correctly | unit | Fail-closed runtime path | keep | S |
| `tests/test_runtime_execution.py` | execution success/error mapping | mocked integration | Comfy execution result boundary | keep | S |
| `tests/test_runtime_integration_matrix.py` | runtime mode/config matrix | mocked integration | Cross-mode coverage | consolidate candidate | S |
| `tests/test_runtime_model_policy.py` | model policy allow/deny | unit | Runtime safety | keep | S |
| `tests/test_runtime_run.py` | run lifecycle, artifacts, metadata, prompt identity | mocked integration | High-risk runtime/publication boundary | keep | S |
| `tests/test_runtime_session_config.py` | config precedence, profiles, metadata, model fingerprints | unit | Runtime config; fingerprints support custody evidence | keep | S |
| `tests/test_runtime_session_embedded.py` | embedded lifecycle, acceptance, flush/reload, concurrency | mocked integration | Comfy embedded boundary and terminal evidence | keep | D |
| `tests/test_runtime_session_run_untracked.py` | one-shot and ensure packs/models resolution | mocked integration | Runtime preparation for readable workflow | keep | S |
| `tests/test_runtime_session_server.py` | server lifecycle, queue/history, cancellation, evidence | mocked integration | Comfy server boundary and terminal custody | keep | D |
| `tests/test_runtime_session_validation.py` | schema cache/live validation/off-ramp parity | mocked integration | Direct schema authority gate before queue | keep | S |
| `tests/test_runtime_spawn_contract.py` | child readiness, timeout, cleanup, credentials | mocked integration | Process boundary and fail-closed startup | keep | S |
| `tests/test_runtime_worker_retry.py` | typed retry policy, budgets, attempt evidence | mocked integration | Runtime retry must not duplicate accepted edits | keep | S |
| `tests/test_structural_evidence_builders.py` | evidence packs, lineage, fake/real distinctions | mocked integration | Strong evidence/publication oracle | keep | D |
| `tests/test_structural_golden_m4.py` | M4 builders/scenarios emit complete evidence | snapshot/static source | Golden harness coverage | keep | S |
| `tests/test_structural_golden_m5.py` | M5 category sets and evidence packs | snapshot/static source | Anti-fake evidence classification | keep | S |
| `tests/test_structural_harness_adapter.py` | workspace isolation, evidence capture, fake/agent classification | mocked integration | Strong harness custody and honesty boundary | keep | D |
| `tests/test_structural_harness_contract.py` | adapter/runner/ABC/readme/source-introspection contracts | static source/unit | Harness architecture and evidence semantics | keep | D |
| `tests/test_structural_harness_runner.py` | CLI filters, modes, actor rejection, bounded assessor retry | mocked integration | Harness orchestration and anti-live leakage | keep | S |
| `tests/test_t20_evaluator_architecture.py` | typed lowering, retained snapshot authority, no-op semantics | unit/property | Direct custody-v2 architecture protection | keep | D |
| `tests/test_t20_publication_custody.py` | publication requires retained pair and preserves destination on refusal | mocked integration | Direct canonical Python/JSON atomic publication | keep | D |
| `tests/test_t20_response_custody.py` | response/republication uses frozen authority; rejects stale/missing lock | mocked integration | Direct custody-v2 response/edit path | keep | D |
| `tests/test_t20_snapshot_witness_binding.py` | retained workflow/schema pair, digest, lineage, detached replay | unit/property | Direct independent authority oracle | keep | D |

Inventory count: 143 files. Depth: 32 deep, 111 shallow. The table uses mixed
method labels where appropriate: 56 mocked-integration, 39 unit, 14 static
source, 6 unit/property, 5 static-source/unit, 3 snapshot/static-source, 3
unit/mocked-integration, 2 mocked-integration/static-source, 1
static-source/mocked-integration, and 14 live entries (some files contain
multiple methods, so these method counts are intentionally non-exclusive).
Disposition count: keep 108, consolidate candidate 13, replace candidate 1,
defer 21; these primary dispositions sum to 143.

## Specific findings and evidence

1. The strongest direct protections are the T20 custody trio. At
`tests/test_t20_snapshot_witness_binding.py:77-90`, explicit retained authority
is exercised with a poison provider and `poison.calls == 0`; the malformed and
cross-lineage cases around lines 118-213 and detached nested replay at line 366
protect the actual authority split. `tests/test_t20_publication_custody.py:79-89`
also proves rejection leaves candidate, lock, and destination untouched. These
are not redundant count checks and should anchor the custody-v2 regression set.

2. There is assertion duplication inside
`tests/test_agent_edit_settings_contract.py`: the seven-field aggregate at
line 87 is followed by individual seed/steps/control/CFG/sampler/scheduler/
denoise tests (for example lines 90-114), and the batch-success tests repeat
the same `result.ok`/statement-shape assertions at lines 372-436 and 605-639.
The unique protections are schema-origin at lines 230-246, enum choice detail
at 452-470, unknown-field diagnostics at 498-535, and mixed-batch rollback at
626-639. Consolidate only the repeated happy-path field assertions into a
parameterized contract; retain one field-specific test per semantic type and
the rollback/diagnostic cases.

3. Replay fixtures repeat `test_fixture_exists_and_is_synthetic` four times in
`tests/test_agent_edit_artifact_replay.py:185,277,422,607`. This is useful
fixture hygiene but is a consolidation candidate, not deletion: move the
fixture provenance check to one parametrized registry test while preserving
the unique canonicalization, missing-identity, schema-rejection, and replay
parity assertions (including the roundtrip at lines 733 and 1106).

4. Embedded and server session suites intentionally repeat lifecycle invariants
but have a narrow overlap. Both assert approved artifact cardinality in
`tests/test_runtime_session_embedded.py:107-112` and
`tests/test_runtime_session_server.py:62-67`; both also assert exactly one
queue/prompt in selected failure paths. This is not noise: embedded/server
parity is a meaningful independent boundary. Consolidate only shared fixture
builders and a small parity matrix; preserve server-specific history/prompt
identity and embedded-specific context reuse (`embedded.py:132-150`) plus
server-exclusive roots (`server.py:209-239`).

5. `tests/test_live_agentic_harness_runner_persistence.py` is a three-line file
with no substantive assertion body. It is a replace candidate, not a deletion
recommendation. Replacement criterion: add an isolated persistence test that
writes a partial run, resumes it, rejects corrupt/mixed-generation state, and
proves atomic destination behavior; otherwise remove the file only after the
replacement coverage is present in `test_live_agentic_runner_persistence.py`.

6. Static source contracts are valuable but can be weak or drift-prone when
they assert token presence. `tests/test_structural_harness_contract.py:129-158`
checks source strings such as `run_all` and enum names. Preserve the architectural
guard, but pair it with the behavioral runner tests at
`tests/test_structural_harness_runner.py:37-124`, and prefer AST/signature
assertions over substring-only checks where practical. The README/evidence
claims at lines 421-443 should remain because they guard the falsification
contract, not implementation details.

## Recommended focused high-signal additions

- Add a canonical-pair fixture test that emits readable `workflow.py` plus
  `workflow.vibe.json`, edits prompt/model/seed/mask/duration in Python, and
  proves the unchanged custody/presentation bundle still loads while the
  reconstructed graph takes the Python values. Add a second case changing
  topology/constructor class/order and require a regeneration diagnostic.
- Add closed-schema mutation/property cases for unknown keys, duplicate JSON
  keys, non-finite numbers, mixed generation, stale digest, foreign labels,
  presentation edges attempting semantic authority, and missing companion.
  The oracle should assert fail-closed behavior and unchanged destination bytes.
- Add a real-boundary contract at the loader/first-constructor seam: malformed,
  missing, and valid sibling capsules must be distinguished before any node is
  instantiated; prove helper custody cannot instantiate nodes or restore edges.
- Add an independent semantic oracle comparing constructed Python handles and
  ordered custody records (scope, label, class, order, schema witnesses), then
  separately compare presentation foreign keys. Do not use the JSON graph as
  the oracle for Python topology.
- Add one end-to-end Comfy Node edit case covering readable source load,
  explicit parameter edit, finalize, queue, accepted witness, and publication;
  assert output handles/values, not merely queue count or an output marker.

## Omissions and triage

Tier 1 (must retain/extend): T20 custody trio; agent generated loader/security;
artifact admission/lineage; static lowering; runtime embedded/server validation
and terminal evidence; structural adapter anti-fake guards. These protect
fail-closed authority, readable-source semantics, and real Comfy boundaries.

Tier 2 (consolidate carefully): settings happy paths; executor contracts/flows/
routes/families; research/lookup tool families; repeated replay fixture hygiene;
embedded/server shared setup. Refactor toward shared factories and a compact
truth-table while preserving independent oracles and failure-specific details.

Tier 3 (defer or replace): RunPod matrices, calibration, live assessor/harness
happy paths, doctor/profile/config-only checks, and the empty persistence
placeholder. Keep a small scheduled real-boundary smoke; replace broad low-
diagnostic suites only with targeted evidence assertions and bounded reports.

Not covered: unassigned product code, unlisted tests, test execution/collection,
full repository dependency graph, and implementation of the canonical pair.
