# Corpus completeness amendment — 2026-09-12

## Decision

Decision ID: `D-CORPUS-20260912`.

The latest user requirement is that every workflow in the 20-workflow corpus
must work through the canonical path unless its source is genuinely malformed
or semantically unresolved. The previous `10 successful / 10 intentional
refusals` result is therefore not a completion result. It remains preserved as
historical evidence, but the affected refusal expectations are superseded by
this amendment.

A bounded Astra high adjudication classified the cases from their source bytes
and the existing importer owners. This document extends the existing E0/E1/
T1/T2/T3/E2/T4 tasks; it does not create a new stage, review process, budget,
representation or compatibility layer.

## Corpus disposition

| Cases | Current required outcome | Reason / acceptance condition |
| --- | --- | --- |
| 03–09, 12, 19, 20 | Positive | Existing positive corpus coverage remains required. |
| 01 | Positive | Proxy-widget order must bind by declared identity, not encounter order; preserve the inner `PrimitiveInt` value `1024`. |
| 02 | Positive | Empty outer instance values are absent overrides when explicit inner proxy references supply the values; preserve recoverable image fanout. |
| 11 | Positive | Same absent-override/default precedence as 02; preserve inner width/height and model values. |
| 13 | Positive | Repeated edges with agreeing checkpoint values are proven fanout, not ambiguity; preserve all destinations. |
| 15 | Positive | A linked value may feed multiple native targets, including a widget-backed target, when the source proves one value and compatible fanout. |
| 18 | Positive | Preserve the source-proven virtual leg `108:0 → 96:image` through the `end_image` channel; do not confuse a numeric slot with a port name. |
| 14 | Investigate, then support if source-proven | The source repeats one link ID (`[3485, 3485]`) while the link table has one record. Inspect the matching frontend serialization/deserialization and run one minimal load/export experiment before normalizing it. |
| 10 | Refusal for these bytes | `depth2.json` is a descriptive contract document with `capture_status: undetermined`, not a workflow graph. Improve the diagnostic and add a separate real native depth-two positive fixture. |
| 16 | Refusal for these bytes | Link target `2653` is absent and no source evidence identifies a replacement. Refuse contextually; never fabricate, retarget or silently drop it. |
| 17 | Refusal for these bytes | Targets `2653` and `4979` are absent. Refuse contextually with the missing node/link identity; never fabricate, retarget or silently drop them. |

The minimum success target is 16 original positive conversions plus the three
justified atomic refusals. If case 14 is proven to be a recoverable redundant
reference, the target becomes 17 positives. No remaining refusal may be
explained only by the presence of native boundary markers.

## Megado dispatch

### E0/T3 — freeze source contracts (Luna medium)

- Pin the exact source hashes and relevant schema/frontend identities.
- Turn 01, 02, 11, 13, 15 and 18 into source-backed required-positive
  regressions, with expected values, edges, output slots and virtual channels.
- Verify proxy default/override precedence against the matching frontend code.
- Bound case 14 to a half-day source-format experiment: inspect matching
  serialization/deserialization and perform one minimal load/export.
- Preserve 10, 16 and 17 as negative fixtures and add a real native depth-two
  positive workflow beside the descriptive case-10 document.

### E1 — fix widget and boundary binding (Luna medium)

Fix only the demonstrated owners in `vibecomfy/ingest/native_subgraph.py`,
the existing widget-resolution path and the existing recursive boundary path.
The implementation must:

- resolve proxy widgets by declared identity and preserve declaration order;
- distinguish absent overrides from explicit `""`, `0` and `false`;
- use inner defaults when an outer override is absent;
- use source-proven linked widget/non-widget fanout and agreeing repeated
  edges without weakening contradictory-mapping checks;
- preserve model strings, control-after-generate positions, nonzero output
  slots, repeated instances, sibling isolation, unused definitions, notes and
  authored presentation;
- treat case 14 only according to the bounded source experiment.

### E1 — recursive preservation kernel (Sol high XHARD)

Use the existing recursive IR, interfaces and boundary-port representation.
Compose nested boundary bindings, instance overrides and identity across
import/rebuild/export. Reuse the existing recursive emitter and execution
owners. Do not flatten all subgraphs, delete unused definitions or add a new
compatibility framework. Ordinary fixtures and integration remain Luna work;
Sol owns only the irreducible non-local composition kernel.

### T1/T2/T3 — virtual wires, diagnostics and publication (Luna medium)

- Fix case 18 at the existing capture/port-resolution owner, retaining missing,
  empty, invented-roster, numeric-looking-name and scope-isolation refusals.
- Add contextual diagnostics for genuine malformed/refused sources.
- Keep source admission, normalization, semantic comparison and publication
  on the existing shared owners; serialize overlapping importer/bundle edits.
- Prove equivalent CLI, SDK and canvas ingress/export outcomes under one frozen
  authority, allowing only documented report/presentation differences.

### E2/T4 — complete validation (Luna medium)

After integration, rerun all 20 original inputs and all new focused fixtures.
For every positive case, perform conversion, edit, save, reload, export and
deterministic regeneration. Inspect the whole generated Python and the exact
exported graph. For every negative case, prove contextual refusal, no partial
output and byte-for-byte preservation of any existing destination pair. Update
the acceptance ledger, status, receipts and review packet inputs.

## Required proof

Programmatic tests must be source-backed rather than producer-versus-producer
comparisons. Cover:

- positional and proxy-backed widgets, absent versus explicit overrides,
  linked widget/non-widget fanout, repeated instances, nested depth-two
  definitions, sibling/global references, nonzero outputs, notes and unused
  definitions;
- contradictory mappings, missing targets, duplicate conflicting links,
  cycles and invalid slots as stable negative cases;
- case 14's one-link repeated-reference distinction from multiple producers;
- case 18's `108:0 → 96:image` path, both channels, direct SetNode consumers,
  nonzero slots, numeric-looking names, sparse/empty rosters and scope;
- atomic refusal, unchanged source objects, no output files and untouched
  existing destination pairs;
- real CLI, SDK and canvas capture/edit/persist/reopen flows, plus the exact H3
  rehearsal, without treating mocked providers or browser boot as lifecycle
  proof.

### Astra follow-up: admission is not lifecycle closure

The source-contract regressions are only the first rung: an admitted workflow
is not successful until its independently expected values, fanout, output slots,
public outputs, identity, recursive structure, notes and presentation survive
Python/companion generation, rebuild, a meaningful edit, save/reload, UI export
and deterministic regeneration. Replay each original positive after its
minimized fix. The depth-two fixture must exercise repeated instances,
local/global lookup, absent versus explicit `""`/`0`/`false` overrides, sibling
isolation, unused definitions and nonzero outputs through that lifecycle.

Also extend the existing owners' tests for frozen schema/registry/copy-to-recipe
consumers, control-after-generate, aliases, model-string edits, helper/reroute
and note preservation, wrong-value/wrong-target/omitted-fanout/cross-sibling
counterexamples, and full-file cleanliness. These are deterministic test
oracles, not extra model-oracle calls. The selected Python 3.11.16 environment
is authoritative; the worktree Python 3.9 environment is invalid. Case 14's
skipped frontend experiment is an evidence blocker, not an accepted refusal;
the prior `MISSING_COMFYUI` lifecycle receipt likewise cannot close T2/E2.

Retain the existing full offline suite, focused source-shape/semantic/identity
checks, H3 inspection and configured review contract. A required unavailable
boundary remains an evidence gap. The acceptance target is behavior and
identity/provenance fidelity, not importer-shaped syntax.

## Stop conditions and non-goals

Return to the coordinator only when case 14's bounded experiment cannot
establish semantics, preserving supported recursive structure requires changing
the agreed representation, or an existing resource/budget boundary prevents
the required proof. Continue ordinary in-scope fixes otherwise.

Do not repair arbitrary broken JSON, infer missing nodes or semantics, broaden
custom-node/schema coverage, provision models/GPU/runtime, deploy, merge or add
a second review process. Preserve all historical evidence and counters; the
existing run remains the sole Megado authority.

This is a planning amendment. No implementation or test result is claimed by
this document.
