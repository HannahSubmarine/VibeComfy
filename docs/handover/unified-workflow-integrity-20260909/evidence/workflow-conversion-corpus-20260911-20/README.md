# VibeComfy 20-workflow conversion corpus

This is the 20-workflow validation corpus for the canonical-workflow-integrity
plan. Each source was run through the current v2 `vibecomfy port convert` path
on 2026-09-11. The authoritative rerun is
`../workflow-corpus-v2-20260911-final2/`; each positive result contains a
same-basename Python/`.vibe.json` pair, while an expected refusal contains no
partial pair. The raw command receipt is the matching `stdout.json` and
`stderr.txt` in that directory.

The canonical pair keeps readable constructors/topology in Python and
identity, provenance, custody, and presentation annotations in the validated
companion JSON. Markdown-note text is typed presentation data with exact
content; it is not runtime Python or custody. A legacy `.layout.json` is not
emitted by this canonical path.

## Results

| # | Source | Coverage | Outcome | Triage |
|---:|---|---|---|---|
| 01 | `official/image/flux2_klein_4b_t2i.json` | Note-bearing official image; primitive input | Refused: `primitive_literal_invalid` for `PrimitiveInt` node `75::68` | Importer/source type normalization defect; preserve as a regression fixture |
| 02 | `official/edit/qwen_image_edit.json` | Official edit; native recursive boundary markers | Refused: `unsupported_boundary_encoding` | Boundary mapping/explicit-refusal policy; must be covered by subgraph tests |
| 03 | `official/audio/ace_step_1_5_t2a_song.json` | Official audio; 10 API nodes | v2 pair materialized; `parity_ok=true` | Positive baseline |
| 04 | `official/video/wan_i2v.json` | Official video I2V; MarkdownNote | v2 pair materialized; `parity_ok=true` | Positive note-bearing baseline |
| 05 | `official/video/wan_t2v.json` | Official video T2V; 11 API nodes | v2 pair materialized; `parity_ok=true` | Positive baseline |
| 06 | `custom_nodes/qwen_tts/1038lab/qwen3_tts_custom_voice.json` | Custom audio; 2 API nodes | v2 pair materialized; `parity_ok=true` | Positive custom-node baseline |
| 07 | `custom_nodes/ltxvideo/iamccs/IAMCCS_LTX23_BEST_3SEG_AUDIOEXT_30S_FREE_LOW_RAM.json` | Helper/note-heavy custom video/audio; 74 API nodes | v2 pair materialized; `parity_ok=true` | Positive large-graph baseline |
| 08 | `custom_nodes/ltxvideo/lightricks_2_3/LTX-2.3_ICLoRA_HDR_Distilled.json` | Model-heavy custom video; 24 API nodes | v2 pair materialized; `parity_ok=true` | Positive model/control baseline |
| 09 | `custom_nodes/qwen_tts/1038lab/qwen3_tts_voice_clone.json` | Custom audio; 3 API nodes | v2 pair materialized; `parity_ok=true` | Positive small custom baseline |
| 10 | `tests/fixtures/recursive_live_contract/depth2.json` | Depth-two/edge fixture | Refused: `Unsupported workflow shape: unknown` | Fixture-shape/diagnostic contract gap; keep as malformed-input test |
| 11 | `official/image/flux2_klein_9b_t2i.json` | Official image; native recursive boundary markers | Refused: `unsupported_boundary_encoding` | Same boundary coverage as 02 |
| 12 | `official/image/qwen_image_2512.json` | Official image; switch widgets | v2 pair materialized; `parity_ok=true` | Fixed: preserve authored switch values and scoped links |
| 13 | `official/video/ltx2_3_t2v.json` | Official video; native recursive boundary markers | Refused: `unsupported_boundary_encoding` | Same boundary coverage as 02 |
| 14 | `custom_nodes/ltxvideo/runexx/LTX-2.3_Talking_Avatar_Qwen_TTS.json` | Large custom audio/video; native recursive boundary markers | Refused: `unsupported_boundary_encoding` | Boundary coverage plus custom-node preservation |
| 15 | `custom_nodes/ltxvideo/runexx/LTX-2.3_V2V_Extend_Any_Video.json` | Custom V2V; native recursive boundary markers | Refused: `unsupported_boundary_encoding` | Boundary coverage plus edit/rebuild proof |
| 16 | `custom_nodes/ltxvideo/lightricks_2_3/LTX-2.3_ICLoRA_Motion_Track_Distilled.json` | Custom control workflow; stale endpoint | Refused: UI link 2 references unknown endpoint `2004`/`2653` | Source endpoint validation/repair or explicit refusal |
| 17 | `custom_nodes/ltxvideo/lightricks_2_3/LTX-2.3_ICLoRA_Union_Control_Distilled.json` | Custom control workflow; stale endpoint | Refused: UI link 2 references unknown endpoint `2004`/`2653` | Same endpoint-validation coverage as 16 |
| 18 | `custom_nodes/wanvideo_wrapper/kijai/wan21_14b_flf2v.json` | Custom FLF2V; virtual-wire output | Refused: `unknown_virtual_wire_port` for `end_image` | Virtual-wire/native-roster preservation defect or explicit refusal |
| 19 | `custom_nodes/wanvideo_wrapper/kijai/wan22_5b_i2v.json` | Custom I2V; output arity and model paths | v2 pair materialized; `parity_ok=true` | Fixed: preserve authored model paths and output mapping |
| 20 | `custom_nodes/ltxvideo/iamccs/IAMCCS_LTX2_AU_IMG2V.json` | Large custom audio/I2V; audio fan-in | v2 pair materialized; `parity_ok=true` | Fixed: retain authored audio fan-in topology |

## Failure taxonomy and plan extension

The 20-case run identifies six distinct classes to handle in the implementation
and test plan. Three supported-input fidelity defects were fixed and rerun:
case 12 (switch values/scoped links), case 19 (authored model path spelling and
output mapping), and case 20 (audio fan-in topology). The remaining failures
are intentional, source-backed refusals:

- 01 rejects an invalid `PrimitiveInt` literal (`75::68`).
- 02, 11, 13, 14, and 15 reject unsupported native recursive-boundary encoding.
- 10 rejects the malformed unknown workflow shape.
- 16 and 17 reject links to absent endpoints (`2004`/`2653`).
- 18 rejects the unproven `end_image` virtual-wire port.

The six diagnostic classes remain:

1. **Primitive coercion** — validate and normalize typed literal values before
   graph construction; never stringify or silently clamp an invalid integer.
2. **Native recursive boundaries** — detect `inputNode`/`outputNode` markers in
   preflight, resolve them to explicit Python-owned interfaces when supported,
   and otherwise refuse with a stable diagnostic before any output is written.
3. **Unknown UI endpoints** — validate every link endpoint against the source
   node table and report the exact link/node IDs; do not fabricate a node.
4. **Virtual-wire/native-port mismatch** — preserve named virtual-wire legs only
   when the native roster proves the port; otherwise produce a precise refusal.
5. **Parity drift** — compare canonical widget values, model paths, output
   arity, and topology after import and before publication. A failed parity
   check must leave no partial Python/JSON pair.
6. **Unknown workflow shape** — schema/shape preflight must identify malformed
   fixtures and return a structured diagnostic rather than a raw `ValueError`.

These classes are implementation work only where the source is a supported
workflow shape or the agreed plan requires explicit boundary preservation. A
stale/malformed source may remain refused, but the refusal must be intentional,
stable, actionable, and tested. No failure is a PASS merely because the report
contains `build_ok: true`. The final2 receipt records the exact diagnostics and
confirms no pair was written for every refusal.

## Required validation phase

The plan now includes a named validation phase between implementation and
completion:

### V0 — corpus preflight

Run source-shape checks on all 20 inputs: JSON/schema shape, node/link endpoint
integrity, native boundary markers, primitive types, output declarations,
virtual-wire ports, and note classification. Record the source hash and the
expected result (`convert` or `refuse`) before materialization.

### V1 — conversion and atomicity

Run the canonical converter over the corpus. Positive cases must materialize a
Python/partner-JSON pair; negative cases must return the declared diagnostic,
write no partial pair, and leave an existing destination unchanged. The batch
must be deterministic on a second run.

### V2 — artifact cleanliness and closed-schema checks

For every positive pair, parse the whole Python file and JSON partner, inspect
declaration contents (not just names), assert no embedded custody/helper replay
payloads or duplicate runtime values, and verify deterministic hashes. Markdown
annotations must be explicit typed presentation records with exact text and
scope-qualified identity. The final2 positive pairs pass this v2 cleanliness
check.

### V3 — semantic, identity, and parity validation

Compare source and rebuilt IR for topology, public inputs/outputs, subgraph
interfaces, node IDs/UIDs, native ports, helper identity, provenance, model
assets, output slots/arity, and widget values. Require exact named diagnostics
for each of the six failure classes above.

### V4 — editing and regeneration

On representative positive workflows, edit runtime controls (prompt, seed,
model, mask, duration, audio interval), save, reload, export, and regenerate.
Presentation-only note edits must change bundle/presentation evidence without
changing runtime semantics. Rebuilds must not need custody regeneration to
preserve valid drafts.

### V5 — CLI/SDK/canvas parity and final gate

Exercise CLI, SDK, and canvas import/export paths with the same pair. Verify
MarkdownNote/Note/Label text, whitespace, Unicode, empty strings, scope, and
attachment round-trip exactly, including nested definition/instance notes.
The phase exits only when required positive cases pass, malformed/unsupported
cases refuse intentionally, no partial writes occur, the affected programmatic
suite is green, and the broad suite is run once on the integrated candidate.

## Astra adjudication

**Disposition: change approach.** Retain external custody v2 and extend the
existing implementation/validation plan; the corpus does not justify a new
architecture or a requirement that arbitrary malformed input convert.

The definite in-scope fidelity defects are:

- **12:** `ComfySwitchNode` values are inserted or moved during reconstruction;
  preserve authored values and absent/channel distinctions.
- **19:** authored backslash-containing model paths are changed during parity;
  preserve runtime strings explicitly. Separately prove the WanVideo output
  arity mapping; the warning alone does not establish that arity caused the
  parity failure.
- **20:** the `VHS_VideoCombine.audio` edge from `IAMCCS_MultiSwitch:0` is lost;
  preserve it through import, construction, reload, and export.

Trace **01, 16, 17, and 18** against exact source membership and pinned schemas
before classifying them. Fix valid data lost by the importer; retain a
contextual refusal when the source is genuinely invalid or ambiguous. The
native-boundary cases **02, 11, 13, 14, and 15** are valid refusals under the
current explicit-boundary policy; add supported explicit-boundary counterparts
for positive nesting coverage. Case **10** remains a malformed-shape negative
fixture and must be paired with a correctly packaged supported depth-two graph.

### Minimum acceptance

All 20 original outcomes must match evidence-backed expectations with zero
unexplained discrepancies. Each supported input must materialize a validated
v2 pair and pass fidelity/cleanliness/editing checks. Each expected refusal must
emit its exact contextual diagnostic, materialize nothing, and preserve any
existing destination. Preserve the seven baseline successes, but do not count
their current embedded-custody output as v2 acceptance.

The validation phase enters after v2 loading/publication and clean emission are
implemented, known fidelity defects are fixed, corpus expectations are
established, and focused regressions pass. It exits only after the 20-case rule,
the full regression matrix, H3 edit/save/reload/export evidence, artifact
inspection, deterministic regeneration, and the complete required suite all
pass. This is validation within the existing plan, not an extra review gate.

## Raw artifacts

- The final v2 run and all 20 command receipts are in
  `../workflow-corpus-v2-20260911-final2/`.
- Positive pairs are in cases 03–09, 12, 19, and 20 there; refusal cases have
  only their exact `stderr.txt` diagnostic and empty `stdout.json`.
- Three exploratory refusal receipts from nearby alternatives are under the
  earlier `workflow-review-set-20260911/exploratory-failures/` directory.
- The quick-view folder with ten selected files is
  `../workflow-review-outputs-10-20260911/`.
