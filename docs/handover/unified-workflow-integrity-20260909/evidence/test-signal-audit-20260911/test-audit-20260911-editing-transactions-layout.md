# Test quality audit: editing / transactions / layout

Planning-only audit of the 44 files in the assigned manifest. No tests were
executed and no product or test files were changed. `AGENTS.md` was not found
under the assigned worktree. The audit uses the current canonical-source
cleanliness direction as the governing target: readable generated Python owns
runtime values/topology; a closed deterministic sibling `.vibe.json` owns
non-derivable custody and presentation; `.layout.json` remains legacy layout
storage; mixed/malformed pairs fail closed and publication is recoverable.

Inspection depth: **deep** means assertions and representative setup/body were
read; **sampled** means assertions were read for representative sections and
the remainder was inventoried by test names/assertion patterns; **shallow**
means bounded inventory only (not a claim of behavioral verification).

## File inventory

| file | behavior / invariant | method | relevance to readable Python + sibling JSON and edit pipeline | disposition | inspection depth |
|---|---|---|---|---|---|
| `tests/intent/smoke/test_edit_correctness_full_runpod.py` | Live judge rejects wrong-but-faithful fixtures; at least one fixture per family | live | Intent oracle is downstream of a rebuilt editable artifact, but this is not custody/pair coverage | defer | shallow |
| `tests/intent/test_edit_correctness.py` | Structural refusal spine allows corpus while intent judge returns zero | mocked integration | Useful edit correctness gate; fixture-derived judge weakens independence | replace candidate | deep |
| `tests/test_batch_rollback_journal.py` | Failed writes/unlinks, symlink swaps, fd/root replacement, recovery blocker | real boundary | Directly supports fail-closed pair publication and unchanged destination guarantees | keep | deep |
| `tests/test_candidate_transaction_layout_contract.py` | Versioned layout authority, schema custody, candidate issuance and explicit identity | mocked integration | Transaction envelope is adjacent to sibling presentation publication, but not `.vibe.json` v2 | keep | deep |
| `tests/test_edit_batch_repl_dependencies.py` | Invocation-time dependency resolution; no singleton/imported package snapshot | static source / unit | Protects readable edit façade from hidden stale authority | keep | deep |
| `tests/test_edit_lint_noop_delta.py` | No-op writes disappear; real writes retain canonical history and replay | unit / mocked integration | Essential value-edit/no-op behavior; independent replay oracle still needed | keep | deep |
| `tests/test_edit_narrative.py` | Structured outcome, fallback, artifact writes, and truthful user message | mocked integration | Pipeline reporting only; should not be used as evidence of Python/JSON fidelity | consolidate candidate | sampled |
| `tests/test_edit_renderer_alias_resolver.py` | Typed/rendered output aliases resolve to frozen slots and reject bad indices | unit | Protects handle/output mapping needed when Python owns topology and bundle stores witnesses | keep | deep |
| `tests/test_edit_schema_known_field.py` | Known linked field accepted; unknown field rejected with diagnostics | mocked integration | Direct editable-value/schema authority coverage | keep | deep |
| `tests/test_inverse_relation_v1.py` | Inverse operations bind exact rewires, prior state, and digest witness | static source / golden | Useful transaction undo invariant; contract version is v1, separate from custody v2 | keep | deep |
| `tests/test_layout_delta.py` | Detect widget/rewire/node changes while ignoring unchanged/lowered/helper-only cases; deterministic topo order | unit | Layout delta must remain presentation-only and not become semantic custody authority | keep | sampled |
| `tests/test_layout_operation_v1.py` | Closed operation envelope, canonical numeric encoding, golden digests and rejection | static source / golden | Legacy layout contract remains separate; protects presentation operation integrity | keep | deep |
| `tests/test_layout_oracle.py` | Position/size drift and uid/display-id fallback are reported | unit | Useful layout-only oracle; no Python/JSON pair semantics | keep | deep |
| `tests/test_layout_store.py` | `.layout.json` naming, v1 migration/v2 envelope, furniture/uid GC and nested entries | unit / fixture integration | Directly guards legacy layout separation and preservation during readable-Python edits | keep | sampled |
| `tests/test_mutation_materialization_v1.py` | Add-node materialization, rebind detection, closed envelope and cross-language numeric parity | static source / golden | Transaction materialization is relevant, but v1 payload must not be mistaken for v2 custody | keep | deep |
| `tests/test_porting_edit_apply.py` | Interpret/apply edits, frozen schema enrichment, guards, atomic replay, subgraph and layout furniture | mocked integration | Highest-signal current edit pipeline; needs external-custody/load-before-constructor cases | keep | sampled |
| `tests/test_porting_edit_apply_values.py` | Asset enum warnings, constrained enum rejection, scalar type discipline | unit / mocked integration | Protects runtime constructor values remaining editable and type-safe | keep | deep |
| `tests/test_porting_edit_corpus.py` | Flat corpus prompt/seed/add/remove/mode edits preserve untouched nodes and atomicity | fixture integration | Strong value-edit regression surface; add canonical Python + sibling JSON corpus cases | keep | deep |
| `tests/test_porting_edit_delta_contract.py` | Six-op canonical delta round trips, strictness, minimal diff, inverse and unknown widgets | unit / fixture integration | Canonical edit record must survive reconstruction independent of presentation bundle | keep | sampled |
| `tests/test_porting_edit_kernel.py` | Python and typed doors converge; claims bind positional carriers; stale/invalid batches mutate nothing | unit / mocked integration | Core readable-Python edit contract and oracle convergence | keep | deep |
| `tests/test_porting_edit_lint.py` | Admission rejects unknown/legacy/unsafe ops, resolves aliases, preserves frozen schema, keeps aggregate atomicity | unit / mocked integration | Strong lint gate; broad overlap with apply and session lifecycle assertions | consolidate candidate | sampled |
| `tests/test_porting_edit_ops.py` | Operation parsing/normalization and field/link/node operation behavior | unit | Lower-level canonical delta contract; retain unique malformed-shape protections | keep | shallow |
| `tests/test_porting_edit_provisional_carveout.py` | Narrow provisional exception/carve-out remains explicit | unit | Policy guard, low direct pair relevance | defer | shallow |
| `tests/test_porting_edit_recursive.py` | Depth-two scopes, typed refs, fanout, boundaries, COW, cycles and rollback fail closed | unit / mocked integration | Highest-risk nested custody binding and Python handle interface coverage | keep | deep |
| `tests/test_porting_edit_report_immutability.py` | Results, ops, diagnostics and nested payloads are detached/immutable | unit | Prevents post-publication mutation of pair/revision evidence | keep | deep |
| `tests/test_porting_edit_resolve.py` | Research/source resolution is fail-closed and does not resurrect prohibited engines | unit | Adjacent policy, not canonical edit/pair fidelity | defer | shallow |
| `tests/test_porting_edit_revision_lifecycle.py` | Explicit revision/bundle/journal identity, approval invalidation, rollback and publication failure preservation | real boundary / mocked integration | Direct transaction/pair publication evidence; strongest candidate for v2 mixed-generation extensions | keep | sampled |
| `tests/test_porting_edit_session.py` | Large end-to-end session harness for fixture conversion, edits, replay, commit and rollback | mocked integration / fixture integration | Broadest pipeline surface, but substantial overlap and fixture-coupled setup | consolidate candidate | shallow |
| `tests/test_porting_edit_session_harness.py` | Flat/subgraph real fixture sessions, byte identity, isomorphism, atomic rollback, provenance and scope gates | fixture integration | Strong representative edit pipeline and nested boundary protections | keep | sampled |
| `tests/test_reorganise_assess.py` | Assessment metrics/issues are ordered and read-only over UI, sidecar, links and topology | unit | Confirms planning does not mutate executable/readable source authority | keep | deep |
| `tests/test_reorganise_classify.py` | Role classification across samplers, loaders, helpers, notes, unknowns and branches | unit | Supports presentation projection while keeping runtime graph semantics distinct | keep | sampled |
| `tests/test_reorganise_compile.py` | Deterministic placement, group ownership, collision/pinned gates, fixed points, hashes and patch shape | unit / mocked integration | High-value presentation compiler; current assertions do not validate sibling `.vibe.json` custody separation | consolidate candidate | sampled |
| `tests/test_reorganise_existing_groups.py` | Existing group preservation/dissolution policy and pinned-node behavior | unit | Layout-only policy; preserve unique ownership/pinned protections | keep | shallow |
| `tests/test_reorganise_goldens.py` | Fixture matrix preserves topology, thresholds, layout metrics, helpers and idempotent coordinates | fixture integration / snapshot-like golden | Valuable layout regression oracle; thresholds/counts can pass despite semantically wrong placement | keep | deep |
| `tests/test_reorganise_graph_facts.py` | Scoped refs, furniture, helper/virtual-wire facts, effective topology and SCC feedback | unit / fixture integration | Critical projection facts; must prove annotations/notes are typed presentation, not hidden custody | keep | sampled |
| `tests/test_reorganise_multiple_samplers.py` | Sequential/parallel/mixed sampler topology ranking and section placement | unit / fixture integration | Representative complex layout; useful non-regression for editable topology projection | keep | shallow |
| `tests/test_reorganise_orchestrate.py` | Offline deterministic preview, sanitized planner input, second-stage gating, patch application and nested scopes | mocked integration | Orchestration boundary; useful for pair presentation path, but planner output is not independent semantic oracle | keep | deep |
| `tests/test_reorganise_plan_parse.py` | Closed plan schema, unknown/backend-owned fields, refs and policy refusal | static source / unit | Protects planning payload from becoming executable/custody authority | keep | deep |
| `tests/test_reorganise_projection.py` | Stable human-readable reasoning projection, scoped refs, helper facts and no executable Python | snapshot-like static source | Directly reinforces readable-source boundary; add explicit “no custody / no JSON loader” assertions for generated source | keep | deep |
| `tests/test_reorganise_skill.py` | Durable skill route, candidate lifecycle, sanitized metrics and layout structural drift refusal | mocked integration | Candidate transaction boundary relevant; not a canonical pair test | keep | sampled |
| `tests/test_reorganise_validate.py` | Ownership, scope, helper placement, forbidden topology/coordinate payloads and SCC rules | unit | Important fail-closed plan validation and presentation/semantic separation | keep | deep |
| `tests/test_reorganise_visualize.py` | Rendering preserves authored UI and emits non-empty PNG/detail band | real boundary / snapshot-like | Visual presentation smoke only; does not establish source/bundle fidelity | defer | shallow |
| `tests/test_revision_evidence.py` | Scoped semantic/layout diff, output/socket/readiness facts, blockers and serializable prompt evidence | unit / mocked integration | Strong revision oracle for semantic vs presentation edits; should include custody digest/revision cases | keep | deep |
| `tests/test_s3_rollback_scope.py` | Add persists while downstream missing schema is typed; readonly missing edge skipped; pure missing target typed | mocked integration | Useful refusal/rollback boundary, but narrow and partly overlaps apply/session | consolidate candidate | shallow |

## Strongest findings

1. **The intent correctness oracle is not independent.**
   `tests/intent/test_edit_correctness.py:67-80` resolves the expected verdict
   from fixture JSON, then `:117-131` asserts the judge fraction against that
   fixture-derived result. This verifies plumbing and corpus accounting, not
   correctness against an independent semantic/UI oracle. Keep the refusal
   spine protection; replace the verdict oracle with an independently authored
   expected semantic delta plus a rebuilt artifact or a deliberately mutated
   wrong output. The live Runpod test at
   `tests/intent/smoke/test_edit_correctness_full_runpod.py:24-44` should remain
   deferred until the expensive boundary is authorized.

2. **Atomicity is valuable but repeated across layers without one named oracle.**
   `tests/test_porting_edit_apply.py` contains separate batch/ops/empty-delta
   atomicity families (for example its `test_apply_batch_replay_rejection_is_atomic`
   and `test_apply_ops_replay_rejection_is_atomic`), while
   `tests/test_porting_edit_kernel.py:217-239` independently checks a typed
   invalid batch and `tests/test_porting_edit_session_harness.py:718-790`
   checks exception/validation rollback. These are not noise: they protect
   different doors. Consolidation should extract a shared oracle contract
   (workflow signature, UI bytes, history, revision, name maps, destination
   files unchanged) and retain one representative per door plus the unique
   exception/symlink/publication cases.

3. **Readable-Python / sibling-JSON v2 coverage is presently an omission, not a
   reason to delete layout tests.** Existing layout tests explicitly preserve
   legacy separation (`tests/test_layout_store.py:86-99`) and compile tests
   reject semantic fields from layout entries (`tests/test_reorganise_compile.py`
   around the patch-key assertions). Add focused v2 tests for: load/validate
   companion before the first constructor; no custody declarations, loaders,
   raw links, or giant finalizer in the complete Python file; closed custody and
   typed presentation annotations in JSON; deterministic pair regeneration;
   value edits without JSON regeneration; mixed-generation/missing/malformed
   refusal before replacement; and copy-to-recipe/registry/restricted-loader
   pair resolution. No current file proves this complete contract.

4. **Golden layout checks are high-signal but partly threshold/count based.**
   `tests/test_reorganise_goldens.py:389-425` checks metric bounds, helper
   counts, scope counts, and minimum group counts; the matrix also calls a
   second-preview idempotence helper at `:290` and separately tests deterministic
   coordinates at `:510-549`. Preserve topology/idempotence protections, but
   add an independent expected placement/ownership oracle for representative
   nested, multi-sampler, note, virtual-wire, and pinned cases. A threshold
   pass must not be accepted as proof that the presentation bundle retained the
   correct scope-qualified identities.

5. **Nested and evidence suites protect important unique invariants but need
   custody-specific assertions.** `tests/test_porting_edit_recursive.py:239-437`
   covers depth-two references, fanout, cycles and qualified-endpoint refusal;
   `tests/test_revision_evidence.py:243-330` distinguishes layout-only from
   semantic changes and marks order-only candidates unrepresentable. Extend
   these focused fixtures to assert ordered custody records, complete scoped
   one-to-one bindings, custody digest participation in revision identity, and
   presentation-only annotation changes leaving semantic IR unchanged.

## Focused recommendations and triage

**Tier 1 — required for the adopted direction.** Add a compact canonical-pair
fixture matrix (H3 plus flat, unknown-schema, multi-output, depth-two nested)
covering preconstruction sidecar validation, closed-schema rejection, binding
coverage/order, deterministic generation, readable whole-file cleanliness,
runtime value edits, output arity, helper/provenance fidelity, and mixed-pair
rollback. Use independent semantic IR/topology/identity oracles, not hashes or
counts alone. Add exact note/annotation identity-text round trips and a test
that `.layout.json` cannot supply custody.

**Tier 2 — retain and sharpen.** Keep transaction journal, recursive, alias,
delta, revision evidence, layout delta/store, graph-facts, plan validation,
orchestration, and golden protections. Extract shared assertion helpers only
where the invariant is genuinely identical; keep separate Python-door,
typed-door, replay, filesystem, and candidate-publication tests.

**Tier 3 — consolidate or defer after replacement exists.** Consolidate
narrative/report/session-wide repetitions around a shared lifecycle oracle;
retain unique user-facing fallback and immutability cases. Defer live Runpod,
visual PNG, provisional carve-out, and research-resolution checks from the
canonical cleanliness gate. Do not delete any listed test solely because it
uses mocks, counts, or snapshots: removal is justified only after the Tier 1
replacement proves the same invariant at the appropriate boundary and the
unique negative/refusal case is preserved.

## Disposition counts

| disposition | count |
|---|---:|
| keep | 34 |
| consolidate candidate | 5 |
| replace candidate | 1 |
| defer | 4 |
| total | 44 |

The counts reflect planning dispositions, not test quality scores or execution
results.
