# Test quality audit: schema-registry-naming

Scope is the 49 files in the assigned manifest. This is a static audit only:
tests were not collected or executed. No product/test deletion is recommended
by this report. “Consolidate candidate” means overlapping coverage should be
made canonical before any removal; “replace candidate” means replacement
coverage is required first. Inspection depth is `deep` where assertions and
representative setup were read, and `shallow` where the inventory was limited
to test names, assertion census, and targeted searches.

The governing direction is `canonical-source-cleanliness-direction.md`:
readable generated Python owns values/topology/public inputs/output; sibling
`.vibe.json` owns closed custody and presentation; the pair loader/publication
must be deterministic, paired, and fail closed. Relevance below means direct
or indirect protection of that Python + sibling JSON edit pipeline.

## File-by-file inventory

| file | behavior / invariant | method | relevance to readable Python + sibling JSON / Comfy Node edit pipeline | disposition | inspection depth |
|---|---|---|---|---|---|
| `tests/acceptance/node_resolution/test_acceptance.py` | A1–C12 node resolution, schema/version pinning, provenance, snapshots, install/compile outcomes | mocked integration + static fixtures | Broad end-to-end evidence for node discovery and authored-version fidelity; does not directly exercise the new v2 pair contract | keep, but split if ownership remains unclear | shallow |
| `tests/edgecases/test_pack_drift.py` | Pack metadata survives conversion; empty drift is safe | unit | Protects provenance/drift inputs to schema custody, not Python/JSON publication itself | keep | shallow |
| `tests/security/test_install_pack_gate.py` | Headless/user-confirmed install gates and audit bypass rules | mocked integration | Protects safe acquisition of node packs that supply schemas; outside canonical source editing | defer to install/security owner | shallow |
| `tests/test_b14_object_info_publication.py` | Atomic generations, marker/hash failure, symlink/path rejection, warm consumer refresh | mocked integration / real filesystem boundary | High-value source-of-schema publication boundary; analogous oracle for atomic Python+JSON publication | keep | deep |
| `tests/test_compact_widget_resolver.py` | Compact widget aliases, hidden padding, duplicate names, schema-provider authority, fail-closed apply | unit / mocked integration | Directly protects readable constructor edits from widget/schema drift; no sibling JSON pair assertions | keep | shallow |
| `tests/test_custom_node_ref_backfill.py` | Backfills generated/strict-ready pack refs and reports unknown/manual buckets | unit / mocked integration | Preserves pack provenance needed for schema witnesses and custody identity | keep | shallow |
| `tests/test_custom_node_refs.py` | Structured refs normalize and lock compatibility distinguishes pinned/unpinned cases | unit | Protects registry/schema identity; indirect to pair loading | keep | shallow |
| `tests/test_emitter_object_info_validation.py` | Object-info validation gate, known classes, CI inclusion, swapped widget order detection | static source + mocked integration | Strong naming/schema witness protection for generated Python; sibling JSON not directly checked | keep | shallow |
| `tests/test_extract_embedded.py` | Embedded schema extraction ladder, timeouts, import preference, allow flag propagation | mocked integration / real filesystem boundary | Protects schema acquisition feeding constructor validation; not canonical pair publication | keep | shallow |
| `tests/test_generated_node_wrappers.py` | Wrapper workflow context, explicit workflow, sentinel rejection, extras/raw, annotations/stubs | unit | Direct readable Python constructor/edit surface protection | keep | shallow |
| `tests/test_h3_schema_widgets.py` | H3 widget slots retain core/lanpaint values; dotted autogrow accepted | unit | Narrow regression for constructor/widget mapping in readable workflows | keep | shallow |
| `tests/test_imagebatch_widget_lens.py` | Link inputs are not mistaken for named widgets; inspect/emit round trip keeps shape | unit / mocked integration | Directly protects Python semantic topology versus UI/widget lens confusion | keep | shallow |
| `tests/test_live_agentic_intent_judge_schema_context.py` | Judge parses verdicts and recomputes/grounds schema/UI context | mocked integration | Indirect evaluator context; not a source/registry oracle and mostly unrelated to sibling JSON authority | defer | shallow |
| `tests/test_models_registry.py` | Registry validation, aliases, pins, path/symlink safety, rollback, cache, phase filtering | unit / mocked integration / real filesystem boundary | High-value model identity and file-boundary protection; supports editable Python model values but not pair custody | keep | deep |
| `tests/test_models_registry_node_packs.py` | Canonical node-pack aliases/gaps and deterministic typo/entry validation | unit | Direct registry naming contract; indirect schema availability | keep | shallow |
| `tests/test_node_packs_compat.py` | Rich lock overrides static seeds; bootstrap fallback; cache invalidation | mocked integration | Protects schema/node-pack resolution used by Python constructors | keep | shallow |
| `tests/test_node_packs_git.py` | Install root/ref matching and sentinel ownership/recovery/quarantine | mocked integration / real filesystem boundary | Install provenance and atomicity support; overlaps `test_nodes_install.py` sentinel behavior | consolidate candidate | shallow |
| `tests/test_nodes_index.py` | Runtime node index fallback to module command/object-info cache | mocked integration | Discovery fallback for readable generated wrappers; no v2 companion checks | keep | shallow |
| `tests/test_nodes_install.py` | Clone/pip/lock transactions, sentinels, dirty trees, ref verification, rollback | mocked integration / real filesystem boundary | Important upstream integrity for node schema availability; sentinel cases overlap `test_node_packs_git.py` | consolidate candidate | shallow |
| `tests/test_nodes_lock.py` | Lock parsing/validation, pins, duplicate/invalid entries, deterministic writes | unit / mocked integration | Direct registry identity/provenance protection | keep | shallow |
| `tests/test_nodes_reconcile.py` | Reconcile installed packs, lock updates, drift and removal behavior | mocked integration / real filesystem boundary | Supports reproducible schema registry inputs; not pair publication | keep | shallow |
| `tests/test_object_info_schema.py` | Object-info source shapes map to schema inputs/outputs and widget metadata | unit | Direct schema oracle for readable node construction | keep | shallow |
| `tests/test_on_demand_resolver.py` | Resolver chooses/loads schema lazily, caches, bounds, and types failures | unit / mocked integration | Directly affects edited Python resolution and fail-closed behavior | keep | shallow |
| `tests/test_p0_widget_canon.py` | Canonical widget names/order and link-vs-widget protections | unit / static fixtures | Direct Python edit semantics; should remain an independent widget oracle | keep | shallow |
| `tests/test_p4_objectinfo_caches.py` | Cache identity, freshness, integrity, fallback, and rebuild behavior | mocked integration / real filesystem boundary | Upstream schema custody and cache trust; adjacent to publication tests | keep | shallow |
| `tests/test_pack_provenance.py` | Pack provenance survives schema/lock transformations and rejects ambiguity | unit | Direct identity evidence for registry and custody metadata | keep | shallow |
| `tests/test_pack_resolver.py` | Pack resolution precedence, lock/cache/source fallback, ambiguity and provenance | mocked integration | High relevance to schema registry naming and constructor authority | keep | shallow |
| `tests/test_porting_corpus_schema_adapter.py` | Corpus/object-info adapter normalizes schema shapes and evidence | unit / static fixtures | Schema oracle for ported readable Python | keep | shallow |
| `tests/test_porting_emitter_widgets.py` | Porting emitter preserves widget names/order and links | mocked integration | Direct Python constructor/emit edit protection; JSON only as UI-adjacent projection | keep | shallow |
| `tests/test_porting_object_info.py` | Object-info serializer/consumer, cache identity, widget-order reconciliation, corruption paths | mocked integration / real filesystem boundary | High-signal schema source and edit round-trip boundary; likely overlaps cache/publication suites | consolidate candidate | shallow |
| `tests/test_rc_primitive_widget_alias.py` | Primitive widget aliases resolve without positional drift | unit | Narrow readable Python edit protection | keep | shallow |
| `tests/test_runtime_schema_probe.py` | Runtime probe capture, bounded materialization, malformed/error typing, provenance | mocked integration / real filesystem boundary | Direct schema registry boundary; important independent real-ish probe oracle | keep | shallow |
| `tests/test_runtime_schema_reuse.py` | Runtime schema reuse preserves captured schema and avoids unnecessary work | unit / mocked integration | Useful cache/reuse invariant for edits; tiny suite | keep | shallow |
| `tests/test_schema.py` | Core provider/index loading, snapshots, refresh, provenance, schema validation and fail-closed transitions | unit + mocked integration / real filesystem boundary | Very high: schema authority for readable constructors and registry resolution; not yet a v2 pair oracle | keep, split by owner before growth | deep |
| `tests/test_schema_alias_authority.py` | Alias precedence and authoritative schema source rules | unit / mocked integration | Directly protects names from being silently remapped during Python edits | keep | shallow |
| `tests/test_schema_availability_admission.py` | Frozen catalog/schema admission, tamper rejection, atomic unavailable/mismatch paths | mocked integration | High-signal fail-closed admission for editable workflows; sibling JSON pairing absent | keep | shallow |
| `tests/test_schema_provisioning_r9.py` | Unknown bounds omission, publish-time races, exact schema witness requirement | mocked integration / real filesystem boundary | Strong schema witness and atomic publication-adjacent coverage | keep | shallow |
| `tests/test_schema_refresh_path.py` | Capture ingest, authority attestation, pruning, replacement and stale-authority prevention | mocked integration / real filesystem boundary | High-value registry/source freshness; no readable Python + `.vibe.json` pair | keep | shallow |
| `tests/test_schema_validate.py` | Required/unknown/range/enum/type validation, normalization approval, links, advisory conversion | unit / mocked integration / snapshot | Direct Python edit contract and independent validation oracle; duplicate basic cases with `test_schema.py` | consolidate candidate for shared primitives only | deep |
| `tests/test_schemas_ensure.py` | AST class extraction, cache coverage, source import fallback, registry mapping, command workflow | static source + mocked integration / real filesystem boundary | Direct generated-Python class naming/discovery and schema registry completeness | keep | deep |
| `tests/test_ui_emitter_widget_shape_verdict.py` | Pinned/dynamic/overflow widget and link verdicts, nested scopes, ghost edges, output identity | mocked integration / snapshot | Very high for preserving semantic Python topology while projecting UI JSON; no custody-v2 envelope assertions | keep | deep |
| `tests/test_widget_aliases.py` | IR-neutral aliases and precedence avoid object-info fallback/positional drift | unit / static source | Direct readable Python edit semantics | keep | shallow |
| `tests/test_widget_row_preservation.py` | Named writes preserve captured rows/None and fail before landing when unresolved | unit / mocked integration | Direct edit/replay invariant; independent oracle for value edits | keep | shallow |
| `tests/test_widget_shape_evidence.py` | Candidate/raw/schema widget counts and overflow evidence | unit / snapshot | Direct UI projection evidence; complements verdict suite | keep | shallow |
| `tests/test_widget_shape_fence.py` | Regeneration/pinning/refusal fence for dynamic/overflow and collateral nodes | unit / snapshot | Direct semantic-vs-presentation boundary protection | consolidate candidate with verdict suite only after scenario matrix is preserved | shallow |
| `tests/test_wrapper_allowance_enforce.py` | Read/mutate allowance, commit ownership, child result and exit enforcement | mocked integration / real filesystem boundary | Process safety around generated artifacts; indirect to canonical pair | defer | shallow |
| `tests/test_wrapper_class_discovery.py` | AST literal extraction, import order, known-error policy, parity and sticky caches | static source + mocked integration | Direct generated wrapper naming/discovery and schema coverage | keep | shallow |
| `tests/test_wrapper_codegen.py` | Deterministic wrapper source/hash, safe identifiers, collisions, annotations, no private ABI | unit / static source + real filesystem boundary | Very high for readable generated Python; lacks sibling JSON generation/pair oracle | keep | deep |
| `tests/test_wrapper_discovery.py` | Snapshot/cache/live/source precedence, pack filtering, lock parsing and stable hashing | mocked integration / static source | High registry naming/discovery coverage; should gain canonical source-vs-companion checks | keep | deep |

## Findings and evidence

1. The strongest existing protections are real boundary oracles, not call
counts. `test_b14_object_info_publication.py:44-92,137-196` verifies committed
generation selection, failed publication preservation, hash failure, path
escape, and symlink rejection. `test_models_registry.py:876-964,991-1185`
similarly verifies rollback and safe materialization. Preserve these kinds of
assertions when consolidating; they model the required “stage/validate together,
leave destination unchanged” rule for the canonical pair.

2. Basic schema validation is duplicated at the public and workflow layers.
`test_schema_validate.py:103-132` separately checks missing required and
unknown inputs with full issue details, while `test_schema.py:447-490`
repeats unknown-class/missing-required behavior through `_only_issue` and
message/severity checks. This is not noise: the former protects detailed
workflow reporting and the latter protects the public validator API. A safe
consolidation would retain one parameterized error-detail matrix plus one API
adapter test; do not delete either file until both contracts are represented.

3. Install sentinel behavior is repeated across owners. The low-level
`test_node_packs_git.py:383-445` covers fresh/live/dead-owner sentinel states,
while `test_nodes_install.py:584-650` covers legacy/corrupt quarantine and
continued install, with similar assertions at `test_nodes_install.py:1044-1072`.
These are meaningful state-machine protections, but the ownership boundary is
unclear. Consolidate around a shared sentinel transition matrix and leave
installer tests for orchestration/lock atomicity; replacement must retain live
owner refusal, corrupt quarantine, retry safety, and no false refresh.

4. Several count/presence assertions are weak when used alone. Examples are
`test_wrapper_codegen.py:34-40` (`assert hashlib.sha256(...)`, whose truth is
not an oracle), `test_nodes_install.py:607-608` and `632-633` (`>= 1` calls and
quarantine entries without asserting the exact command/state transition), and
`test_schemas_ensure.py:509-510` (dedupe plus `len == 1`, which does not test
ordering or extraction provenance). Keep them only when paired with semantic
assertions; otherwise replace with exact output/command/marker and unchanged-
destination assertions. The `len` assertions in wrapper discovery and the
count checks in widget verdicts are not automatically weak because they are
paired with full field/graph assertions.

5. The manifest contains substantial schema/widget coverage but no clearly
identified canonical v2 pair oracle. The deep wrapper tests assert generated
Python text and importability (`test_wrapper_codegen.py:34-155`), and the deep
publication tests assert atomic cache generations, but neither proves that a
readable Python file and sibling `.vibe.json` share deterministic generation,
custody digest, complete scoped bindings, and presentation-only JSON. Add a
focused pair contract suite before any old custody-oriented tests are
considered replaceable.

## Focused high-signal recommendations

Prioritize independent tests in this order:

* Tier 1 — canonical pair publication/load: generate `workflow.py` and
  `workflow.vibe.json`; assert Python owns edited prompt/model/seed values and
  topology, JSON contains only closed custody/presentation, generation and
  custody digest are deterministic, duplicate/unknown keys and mixed
  companions fail closed, and staged publication leaves both prior files
  unchanged on any failure.
* Tier 1 — construction compatibility: compare ordered scoped labels/classes
  and schema witnesses against live constructed nodes; cover constructor
  alias/output unpacking, nested scopes, repeated instances, explicit output,
  value-only edits, swapped companion, missing companion, and unsupported
  structural edits. The oracle should inspect reconstructed semantic nodes,
  not merely emitted text or mock call counts.
* Tier 1 — registry/discovery: one independent fixture matrix for canonical
  names, aliases, lock/source/cache precedence, exact pack/version provenance,
  duplicate labels/classes, and restricted pair discovery. Keep existing
  wrapper-discovery and schema-provider tests as lower-level oracles.
* Tier 2 — Python/UI boundary: retain the widget row/shape/verdict protections
  and add assertions that presentation links may decorate Python-derived edges
  but cannot create edges, overwrite constructor values, or instantiate helper
  records. Include a readable edit followed by copy-to-recipe and reload.
* Tier 3 — upstream acquisition/operations: consolidate sentinel and cache
  matrices, preserve filesystem rollback/symlink/path protections, and defer
  judge, allowance, and broad acceptance suites unless they gain a named
  canonical-pair scenario.

## Omissions and triage

The main omission is direct v2 custody/presentation schema coverage: closed
keys, duplicate JSON keys, finite numbers, scope-local unique labels, complete
one-to-one bindings, native-port carrier restrictions, helper non-instantiation,
presentation foreign-key validation, digest/generation derivation, and
copy-to-recipe pair association. Also missing from this slice is a focused
independent oracle proving that a value-only edit remains loadable while a
topology/class/output edit refuses with a regeneration diagnostic.

Recommended triage is 12 Tier-1 keep/add areas (publication/pair contract,
construction compatibility, registry/discovery, and semantic/UI authority),
20 Tier-2 keep areas (schema, widget, provenance, cache, and wrapper support),
10 Tier-3 consolidate/defer areas (install/cache/state orchestration), and 7
low-relevance/defer files (judge, allowance, and broad operational suites).
These are triage areas, not file deletion instructions.

## Final state

* Assigned: 49 files; categorized: 49/49.
* Deep inspection: 10 files; shallow inventory: 39 files.
* Disposition counts (normalized across qualified labels): keep 41;
  consolidate candidate 5; defer 3; replace candidate 0. No file is recommended for deletion, so no replacement
  criterion is being waived.
* Strongest findings: atomic filesystem boundaries are high-signal and should
  be preserved; public/workflow schema validation and install sentinels overlap
  but protect distinct layers; several bare count/presence checks need stronger
  semantic oracles; and the assigned slice lacks a direct canonical v2 Python +
  sibling JSON contract test.
