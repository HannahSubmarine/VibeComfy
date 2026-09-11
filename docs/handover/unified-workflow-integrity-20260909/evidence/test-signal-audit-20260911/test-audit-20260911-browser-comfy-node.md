# Test quality audit: browser-comfy-node

Planning-only audit of the 76 files in the assigned manifest. No tests were
executed or collected. Inspection is source-based: assertions and fixtures were
read in the central/high-risk files; small adjacent files were inventoried from
their tests and assertion sites. “Shallow” means this is an inventory, not a
claim that every assertion in that file is redundant.

Method abbreviations: unit = isolated function/contract; mocked integration =
browser harness, fake transport, or fixture-backed backend; real boundary =
cross-language/filesystem/live adapter boundary; static source = import/owner/
AST/text inspection; snapshot = structural/render projection comparison;
property = invariant across generated cases; live = Playwright/ComfyUI. Depth is
deep (representative assertions read), medium (main assertions/fixtures read),
or shallow (inventory only).

## File-by-file disposition

| file | behavior / invariant | method | relevance to readable Python + sibling JSON and Comfy Node edit pipeline | disposition | inspection depth |
|---|---|---|---|---|---|
| `tests/browser/active_row_rendering.test.mjs` | Activity/outcome labels and DOM phase rows remain canonical and safe | unit + mocked integration | Adjacent UI projection; no pair or Comfy reconstruction | keep; separate concern | medium |
| `tests/browser/agent_candidate_actions.test.mjs` | Candidate eligibility/action payloads preserve durable authority and stale blocking | unit | Apply gate protects edit pipeline, but not Python/JSON fidelity | keep | medium |
| `tests/browser/agent_edit_lifecycle.test.mjs` | 70-field lifecycle state, delta normalization, apply/rebaseline cleanup | unit + mocked integration | Important editor state boundary; little canonical pair coverage | consolidate candidate with response/commit lifecycle only if field-level oracle retained | deep |
| `tests/browser/agent_edit_lifecycle_transcript.test.mjs` | Rehydrate atomically replaces optimistic transcript without duplication/leakage | unit | Chat safety around edits; not source/bundle semantics | keep | medium |
| `tests/browser/agent_edit_node_pack_installer.test.mjs` | Installer request, CSRF path, and failure dispatch | mocked integration | Custom-node availability prerequisite; no schema provenance or pair | keep | medium |
| `tests/browser/agent_edit_response_contract.test.mjs` | Public outcome/candidate/legacy adapter selectors stay closed and canonical | unit | Candidate contract feeds edit pipeline; not generated-source authority | consolidate candidate with malformed response if distinct negative matrix retained | deep |
| `tests/browser/agent_edit_response_malformed.test.mjs` | Missing identity/graph/turn and stale/rebaseline responses fail closed | unit + mocked integration | High-value negative edit safety; no Python/JSON validation | keep; pair with contract matrix | deep |
| `tests/browser/agent_edit_transaction.test.mjs` | V2 authority, provenance order, layout verification, and bounded errors | unit | Transaction gate protects Comfy apply; does not inspect readable source | keep | medium |
| `tests/browser/agent_lifecycle_commit.test.mjs` | Commit response selectors and outcome normalization preserve canonical fields | unit | Server/browser lifecycle bridge; no bundle reconstruction | consolidate candidate with response contract after unique field inventory | medium |
| `tests/browser/agent_lifecycle_parity.test.mjs` | Production/preview/replay adapters project identical lifecycle fields and safe payloads | unit + snapshot | Strong pipeline parity; no Python/sibling JSON oracle | keep; do not collapse to count assertions | deep |
| `tests/browser/agent_status_poller.test.mjs` | URL/status/retry/credential rendering and failure states | unit + mocked integration | Operational prerequisite only; unrelated to source cleanliness | defer from this amendment | medium |
| `tests/browser/agentic_replay.test.mjs` | Replay is opt-in, isolated from production, deep-cloned, and navigable | mocked integration + property | Replay safety; risks alternative graph authority but not canonical pair itself | keep; check against v2 source-container rule | deep |
| `tests/browser/b18_lifecycle_contract.test.mjs` | Storage-disabled scope, snapshot cloning, HTTP/terminal status contracts | unit + mocked integration | Lifecycle guard, not pair fidelity | defer | medium |
| `tests/browser/canonical_bundle_queue.test.mjs` | Canonical record publication, custody mismatch rejection, exact queue projection, stale/replaced hooks | mocked integration + real boundary | Directly high-signal for canonical custody, publication atomicity, and queue/edit handoff; fixtures are record-shaped, not readable generated Python + v2 sibling JSON | keep as boundary suite; add v2 pair fixtures and interleaving rollback oracle | deep |
| `tests/browser/canonical_delta.test.mjs` | Seven delta ops, schema version, strict shapes, diagnostics, round trips | unit + property | Edit mutation envelope, not Python/JSON source fidelity | keep | deep |
| `tests/browser/canonical_hash.test.mjs` | Browser/Python canonical hash and UTF-8/key-order authority | real boundary + property | Useful independent oracle for pair digests and revision identity | keep; extend to v2 custody/presentation digest exclusions | deep |
| `tests/browser/chat_boundaries.test.mjs` | Ownership of transport and canonical ingestion remains in declared modules | static source | Prevents adapter drift, but not source/bundle behavior | keep as ownership guard | shallow |
| `tests/browser/chat_rehydration.test.mjs` | Snake/camel normalization and precedence at transport boundary | unit | Adjacent lifecycle compatibility | defer or consolidate with response boundary only with exact alias oracle | medium |
| `tests/browser/comfy_adapter_ownership.test.mjs` | Adapter owns intent/exec normalization; roundtrip delegates | static source | Directly protects Comfy Node adapter ownership | keep | medium |
| `tests/browser/deep_plain.test.mjs` | Recursive plain-object/array clone and prototype handling | unit + property | Snapshot isolation used by edit/replay; not pair semantics | keep | medium |
| `tests/browser/dependency_isolation.test.mjs` | Independent diagnostic consumers do not overwrite dependencies | mocked integration | Harness isolation; low source/bundle relevance | defer | shallow |
| `tests/browser/dynamic_io_smoke.test.mjs` | Dangling/duplicate links sanitize; dynamic exec IO survives refresh | mocked integration + snapshot | Direct Comfy Node graph/link protection; no readable Python sidecar | keep; add typed native-port/pair fixture | deep |
| `tests/browser/frontend_browser_boundary.test.mjs` | Shipped frontend modules are browser-resolvable | real boundary | Build prerequisite only | defer | shallow |
| `tests/browser/frontend_ownership_regression.test.mjs` | Roundtrip does not re-own status/settings/provider behavior | static source | Prevents wrong owner from becoming source authority | keep | medium |
| `tests/browser/graph_projection.test.mjs` | Browser structural projection equals Python session fixture | real boundary + snapshot | Independent parity for graph identity; not generated workflow pair | keep; broaden to v2 presentation projection | medium |
| `tests/browser/harness_dependency_closure.test.mjs` | Staged web manifest is closed and dependencies are reachable | static source | Harness integrity, not workflow source cleanliness | defer | shallow |
| `tests/browser/hermes_cli_provider.test.mjs` | Provider alias and browser provider contract normalize correctly | unit | Provider selection may affect edit flow; no pair | defer | shallow |
| `tests/browser/http_security.test.mjs` | Mutations bootstrap CSRF once, sanitize responses, reject unsafe requests | mocked integration | Protects edit transport, not source/bundle fidelity | keep | medium |
| `tests/browser/intent_graph_adapter.test.mjs` | Intent/exec graph adapter contracts, normalization, repaint and output behavior | unit + mocked integration | Comfy Node graph projection and edit surface; no readable-source authority | keep | deep |
| `tests/browser/intent_graph_adapter_ownership_static.test.mjs` | Only adapter acquires live graph/repaints and forbidden imports stay absent | static source | Important ownership boundary for Comfy canvas edits | keep | deep |
| `tests/browser/intent_graph_receipt_core.test.mjs` | Prepared authority receipt preflight/currentness and diagnostics | mocked integration | Edit admission gate; not pair loading | keep | medium |
| `tests/browser/inverse_relation_v1.test.mjs` | Inverse relation golden structural cases and digest | property + snapshot | Graph relation primitive; low direct source relevance | defer unless v2 uses it | shallow |
| `tests/browser/layout_operation_v1.test.mjs` | Layout operation positives and pinned digests | property + snapshot | Presentation-only edit semantics; useful to keep separate from runtime authority | keep | medium |
| `tests/browser/legacy_authority_migration.test.mjs` | Legacy v0 authority explicitly migrates and invalid inputs refuse | unit + mocked integration | Compatibility boundary; must remain explicit under v2 direction | keep; add unmarked-legacy/no-companion cases | deep |
| `tests/browser/lifecycle_ownership_static.test.mjs` | Preview picker avoids state overwrite and ownership violations | static source | UI lifecycle safety, not pair | defer | shallow |
| `tests/browser/m1_contracts.test.mjs` | Browser/Python consume one golden projection corpus | real boundary + snapshot | Strong cross-language oracle; should become a home for pair projection parity | keep; extend to v2 custody/presentation | medium |
| `tests/browser/markdown.test.mjs` | Markdown rendering, escaping, links, and safe text behavior | unit + snapshot | Relevant only to typed presentation annotations; no exact note round trip | keep; add annotation identity/text cases under v2 | medium |
| `tests/browser/mutation_materialization_v1.test.mjs` | Mutation materialization golden positives and digests | property + snapshot | Edit operation materialization; not Python regeneration | keep | medium |
| `tests/browser/ownership_contract.test.mjs` | Roundtrip does not declare status-poller ownership | static source | Narrow ownership guard | consolidate candidate with other ownership static tests if each owner remains named | shallow |
| `tests/browser/panel_runtime_scoped.test.mjs` | Scope snapshot excludes canvas-affine state; scoped panel isolation | unit + mocked integration | Protects live Comfy edit scope; no source/bundle | keep | medium |
| `tests/browser/panel_scheduler_activation_fence.test.mjs` | Replaced panel cannot accept late frame or satisfy replacement flush | mocked integration | Prevents stale live edit application | keep | medium |
| `tests/browser/panel_thread_rating.test.mjs` | Rating/detail UI uses canonical field-change selectors and safe payloads | mocked integration | Adjacent audit UX; no pair | defer | medium |
| `tests/browser/payload_contracts.test.mjs` | Large public payload/progress/error contract corpus and redaction rules | unit + snapshot | Supports safe edit transport; overlaps response/lifecycle contracts but preserves broad public shape oracle | consolidate candidate only after partitioning unique fixtures and forbidden-field checks | deep |
| `tests/browser/pipeline_mode_surface.test.mjs` | Mode aliases remain boundary-only and canonical mode surface is closed | unit | Pipeline routing prerequisite | defer | medium |
| `tests/browser/prepared_plan_builder_ownership_static.test.mjs` | Builder import closure excludes runtime/native/adapter modules | static source | Important authority isolation; not readable Python pair | keep | medium |
| `tests/browser/prepared_plan_builder_v1.test.mjs` | Prepared authority builds frozen zero-native plan and rejects invalid structure | unit + mocked integration | Edit admission protection; no generated-source fidelity | keep | medium |
| `tests/browser/preview_diff_core.test.mjs` | Registry owns native-locator UID recovery and diff classification | unit + snapshot | Identity preservation in Comfy edit preview; not pair loading | keep | medium |
| `tests/browser/preview_overlay_ownership_static.test.mjs` | Overlay owns implementation details and does not leak to other owners | static source | Canvas edit ownership only | defer | shallow |
| `tests/browser/preview_picker.test.mjs` | Picker disabled/preview/apply selection and no-network behavior | mocked integration | Review UX gate; no pair | keep | medium |
| `tests/browser/projection_boundary_helpers.test.mjs` | Safe TranscriptMessage/ResponseDetail projection allowlist | unit | Payload safety around editor | defer | shallow |
| `tests/browser/render_section_safety.test.mjs` | Renderer section allowlist excludes candidate/raw fields | static source + unit | Safe UI projection, not source/bundle | defer | shallow |
| `tests/browser/roundtrip_smoke.test.mjs` | Broad browser roundtrip, hashing, graph projection, agent submit, panel render and forbidden leakage | mocked integration + snapshot | Directly adjacent to Comfy round-trip/edit pipeline, but much of the 25k-line corpus is UI/transport fixture coverage rather than readable Python + sibling JSON | keep as smoke boundary; split focused canonical-pair suite before any consolidation | deep |
| `tests/browser/scope_resolver.test.mjs` | Scope fingerprint/resolution and nested graph identity remain stable | unit + property | Relevant to nested workflow custody binding and edit scope | keep; add v2 scope-path/label cases | medium |
| `tests/browser/scoped_session_persistence.test.mjs` | Session storage wrappers and scoped persistence round trip | unit + mocked integration | Session support, not pair | defer | shallow |
| `tests/browser/submit_flow_ownership.test.mjs` | Submit factory owns exactly its consumer state and dependency object | static source | Prevents live edit state cross-talk | keep | medium |
| `tests/e2e/run.test.mjs` | Launcher diagnostics, sanitization, fixture preflight, and Playwright artifacts | mocked integration + real boundary | Test harness reliability; no source/bundle oracle | defer | medium |
| `tests/e2e/specs/agent_panel_layout.spec.mjs` | Launcher/sidebar open, viewport bounds, panel regions and layout | live | Canvas/panel shell only | defer | medium |
| `tests/e2e/specs/agent_panel_lifecycle.spec.mjs` | Session rehydrate/reopen, scroll anchoring, pending-to-complete lifecycle | live | End-user edit lifecycle; no readable Python/JSON | keep as acceptance smoke | medium |
| `tests/e2e/specs/agent_panel_overlay.spec.mjs` | Overlay anchors to live canvas/widgets and updates after edits | live + snapshot | High-value Comfy canvas edit visualization; not source pair | keep | medium |
| `tests/e2e/specs/agent_panel_reorganise.spec.mjs` | Layout-only candidate is applyable and changes live positions | live | Presentation edit path; useful proof that layout does not imply runtime mutation | keep | medium |
| `tests/e2e/specs/agent_panel_turn.spec.mjs` | Fixture-backed turn, audit affordances, apply, and live widget change | live | Highest end-to-end edit smoke; no readable-source regeneration or sidecar | keep; add pair load/edit/reload scenario | medium |
| `tests/e2e/specs/demo_preview_visual.spec.mjs` | Demo scenario manifest and visual review states render without failures | live + snapshot | Visual regression only; no canonical source authority | defer | medium |
| `tests/e2e/specs/extension_boot.spec.mjs` | Extension boots, launcher/panel visible, no browser failures | live | Deployment smoke only | defer | shallow |
| `tests/e2e/specs/test_dynamic_exec_refresh.spec.mjs` | Agent-create/apply/refresh preserves typed exec IO, links, properties, pool-free serialization | live + snapshot | Direct Comfy Node edit/refresh protection; no readable Python sidecar | keep; add custody/presentation pair assertion | deep |
| `tests/test_comfy_exec_node.py` | Exec IO parsing, exact outputs, recursive input cloning, tensor/mask handling | unit | Direct Comfy Node runtime primitive; no pair | keep | medium |
| `tests/test_comfy_nodes.py` | Conditioning cleanup and code-intent flag preserves legacy/default IO surfaces | unit | Node API compatibility; low canonical-pair relevance | defer | medium |
| `tests/test_comfy_nodes_agent_backend_spine.py` | Backend session/idempotency, authority receipts, schema snapshot freezing, canonical actions, rollback and live-plan gates | unit + mocked integration + real filesystem boundary | Core backend edit spine; strong custody/transaction evidence, but existing snapshots are backend/session artifacts rather than v2 sibling JSON loaded before constructors | keep; add explicit readable-Python/v2-pair fixtures at bundle boundary | deep |
| `tests/test_comfy_nodes_agent_contracts.py` | Frozen public dataclasses, snake-case serialization, failure redaction, gate/rebaseline contracts | unit + property | Strong public edit contract; not pair fidelity | keep; consolidate only duplicate projection assertions with browser payload corpus | deep |
| `tests/test_comfy_nodes_agent_edit.py` | Schema-less edits, frozen schema providers, node/value/layout mutation, batch/replay, output and safety diagnostics | unit + mocked integration + snapshot | Core Comfy edit pipeline and schema provenance; broad and high-signal, but fixture-heavy and not yet v2 external-custody oriented | keep; carve focused conversion/pair regression module | deep |
| `tests/test_comfy_nodes_agent_hivemind_feedback.py` | Config validation, sanitized metadata-only feedback, bounded upload/error behavior | unit + mocked integration | Feedback side path; not source/bundle | defer | medium |
| `tests/test_comfy_nodes_agent_session.py` | Session IDs/paths, persistence, locks, turn allocation and state normalization | unit + real filesystem boundary | Required transaction/session substrate; not Python/JSON fidelity | keep | medium |
| `tests/test_comfy_nodes_agent_transaction_storage.py` | Append-only lifecycle log, receipt/index persistence, recovery and derived snapshots | real filesystem boundary | Supports atomic edit evidence; distinct from canonical pair publication | keep | medium |
| `tests/test_comfy_nodes_browser.py` | Browser harness plus JS/Python canonical and structural hash parity | real boundary | Direct independent oracle for cross-language canonical identity | keep; extend to v2 pair digest | medium |
| `tests/test_comfy_nodes_entrypoint.py` | Comfy entrypoint, mappings, web directory, route-safe stubs | unit + mocked integration | Node/plugin integration prerequisite; no pair | defer | medium |
| `tests/test_comfy_nodes_info.py` | Stable source/dist content identity, dirty/missing Git metadata, secret exclusion | unit | Provenance identity useful to bundle publication; not pair reconstruction | keep | medium |
| `tests/test_comfy_nodes_live_smoke.py` | Live ComfyUI panel open, mocked routes, submit/accept and applied graph safety | live + mocked integration | Strong end-user Comfy edit smoke; currently no generated Python/sibling JSON assertion | keep; add canonical-pair lifecycle only if environment can inspect artifacts | medium |

## Specific duplication and weakness findings

1. The clearest overlap is lifecycle response projection: `agent_edit_response_contract.test.mjs`
   has the closed public/outcome and selector matrix (for example lines 85–190),
   `agent_edit_response_malformed.test.mjs` repeats the same normalizer boundary
   for malformed/missing fields (lines 40–188), `agent_lifecycle_commit.test.mjs`
   reprojects the same identity/candidate/outcome fields (lines 58–276), and
   `payload_contracts.test.mjs` carries another large public payload/progress
   corpus (for example lines 690–698 and 1328–1365). These are consolidation
   candidates, not deletion targets: preserve the unique malformed fail-closed
   cases, legacy-adapter cases, redaction/forbidden-field oracle, and commit
   selector ownership. A replacement needs a matrix showing each field, source
   shape, negative shape, and consumer adapter.

2. Ownership guards overlap narrowly: `ownership_contract.test.mjs:1–8`,
   `chat_boundaries.test.mjs` (the first ownership assertions),
   `frontend_ownership_regression.test.mjs`, and
   `lifecycle_ownership_static.test.mjs` each inspect module ownership/import or
   state-write prohibitions. Keep the distinct owner assertions, but a single
   ownership inventory could replace duplicated harness setup. It must report
   the exact forbidden declaration/import/write and retain a per-owner failure
   message; a line-count or “module imports” count is insufficient.

3. `agent_lifecycle_parity.test.mjs:422–460` compares adapter snapshots field by
   field, while `roundtrip_smoke.test.mjs` contains many similar safe projection,
   graph hash, and UI state assertions. This is not noise: parity has a valuable
   three-adapter oracle and roundtrip has transport/canvas integration. The
   focused improvement is to share canonical fixture builders while retaining
   independent expected values for at least one adapter and one browser-to-
   Python boundary.

4. Some assertions are weak when isolated: E2E overlay helpers assert generic
   geometry and `recordCount > 0` (`agent_panel_overlay.spec.mjs:547–577`), the
   visual demo mostly asserts manifest/scenario non-emptiness
   (`demo_preview_visual.spec.mjs:277–334`), and boot only asserts visibility and
   an empty failure list (`extension_boot.spec.mjs:34–40`). These are appropriate
   smoke sentinels, not evidence of source fidelity. Do not replace them with
   more counts; add semantic identity/attachment assertions where the behavior
   matters.

5. The strongest current boundary evidence is in
   `canonical_bundle_queue.test.mjs:480–635` (real-shaped publication and exact
   decoded queue projection), its changed-custody matrix at `:643–705`, and
   cross-language fixture construction near `:35–164`. The weakness is that the
   fixture is an approved canonical record, not a generated readable
   `workflow.py` plus validated `workflow.vibe.json`; it cannot catch embedded
   custody, duplicate runtime values, a mixed-generation companion, or a
   constructor-before-companion-load bug.

6. `test_comfy_nodes_agent_backend_spine.py` and
   `test_comfy_nodes_agent_edit.py` preserve unique protections for frozen schema
   authority (for example backend-spine `:14372–14425` and edit helpers around
   `:216–362`), schema-less safety, idempotency, rollback, and scoped mutation.
   Their broad fixture construction is a maintainability risk, but matching
   snapshots or mocks are not intrinsically weak: they are the independent
   inputs needed to prove no ambient schema/provider mutation. Replace only
   when smaller fixtures retain the same mutation and negative-path oracle.

## Focused high-signal recommendations

Priority 1 — add a dedicated v2 canonical-pair boundary suite, preferably
adjacent to `canonical_bundle_queue.test.mjs` but not embedded in the 25k-line
roundtrip smoke file. Use actual generated readable Python and sibling
`workflow.vibe.json` fixtures. Assert whole-file cleanliness (renamed/hidden
custody, giant finalizer, replay assignment, duplicate runtime value,
`vibe.py` sibling), closed JSON schema, deterministic pair generation, and
pre-constructor companion validation. The oracle must parse/check Python AST and
the v2 JSON independently, then compare reconstructed semantic IR, IDs/UIDs,
native ports, helper provenance, outputs, and presentation foreign keys.

Priority 1 — add value-edit and structural-edit contrasts: prompt/model/seed/
mask/duration/audio interval changes must load with unchanged custody; changed
scope/label/class/order/native-port/output arity must refuse with a structured
diagnostic. Include repeated nodes, handle aliases/output unpacking, and
depth-two nested scopes. Reuse the Python hash oracle from
`canonical_hash.test.mjs`/`test_comfy_nodes_browser.py`, but do not use the
same serializer as both subject and oracle.

Priority 1 — test publication interleavings and rollback: missing sidecar,
malformed JSON, stale/mixed-generation pair, digest mismatch, replacement
failure, and concurrent read between the two filesystem replacements must leave
the prior destination intact. `canonical_bundle_queue.test.mjs` already proves
many queue-side fail-closed cases; the missing oracle is filesystem pair
atomicity and mixed companion identity.

Priority 2 — add presentation annotation cases for ordinary Markdown/Note,
including empty/Unicode/whitespace text, nested definition-vs-instance scope,
stable qualified identity, edit-save-reload, and semantic invariance. The
existing `markdown.test.mjs` proves renderer behavior, not exact annotation
round trip.

Priority 2 — add the known corpus regressions from the direction: absent switch
value/channel semantics, authored model-path preservation, explicit output
arity, and the `VHS_VideoCombine.audio` edge. These should be source-pair
fixtures with negative refusal cases where fidelity is not proven.

Priority 3 — consolidate only after a field/negative-path inventory: response
contract + malformed + commit + payload projection; narrow ownership guards;
and shared fixture builders across browser/Python parity. Preserve independent
oracles rather than merging all assertions into one implementation-shaped
snapshot.

## Omissions and triage

The assigned slice has no convincing coverage of the adopted external-custody
v2 shape itself: no direct assertion that generated Python has no custody
declarations across the whole module, no closed-schema `custody`/`presentation`
parser matrix, no deterministic generation excluding marker fields, no
constructor-before-load refusal, no mixed-generation pair rollback, and no
exact typed annotation round trip. It also lacks focused proof that valid
runtime value edits remain loadable without regenerating custody and that
explicit zero-output/multi-output declarations are not autodetected away.

Triage tiers:

- P1: v2 pair boundary, whole-file cleanliness, preconstruction load, semantic
  parity, value-vs-structure edit matrix, and publication rollback.
- P2: nested scopes, widget-name provenance/frozen resolution, presentation
  annotations, known corpus regressions, and pair coverage through registry,
  restricted loader, and copy-to-recipe.
- P3: response/ownership consolidation, ancillary UI smoke pruning, and
  deferral of status/feedback/harness-only files from this amendment.

No deletion is recommended. Any future replacement must first name the retained
coverage criterion, carry the unique negative cases and independent oracle, and
show an explicit mapping from the old file's protections to the replacement.

## Final state

| state | count |
|---|---:|
| assigned files audited | 76 |
| keep / keep with focused extension | 48 |
| consolidation candidate (no deletion) | 8 |
| defer from this amendment | 20 |
| replace candidate | 0 |
| execution / collection performed | 0 |

The 3–5 strongest findings are: (1) the slice has substantial transaction and
Comfy edit safety but lacks direct readable-Python + sibling-JSON v2 evidence;
(2) canonical queue tests prove record publication/queue custody, not
pre-constructor pair loading or filesystem mixed-generation rollback; (3)
response/payload/commit suites overlap but each retains distinct malformed,
legacy, redaction, or adapter protections; (4) large backend/edit suites have
valuable frozen-schema, rollback, and scoped-mutation oracles that should be
refactored only with protection mapping; and (5) current E2E/count/visual smoke
assertions are useful health checks but must not be mistaken for semantic source
fidelity.
