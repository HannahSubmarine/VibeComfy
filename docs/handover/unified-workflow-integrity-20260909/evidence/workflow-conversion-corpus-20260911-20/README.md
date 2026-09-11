# VibeComfy 20-workflow conversion corpus

This is a diagnostic corpus for the canonical-workflow-integrity plan. Each
source was run through the current `vibecomfy port convert` path on 2026-09-11.
The raw command receipt is the matching `*.convert.json` file. A Python file is
present only when conversion completed with exit status 0 and materialized an
output. Reports that contain build/compile fields but have no Python output are
parity failures, not successes.

This corpus is deliberately not v2 acceptance evidence. The external custody
boundary and exact Markdown-note sidecar support are documented in the
[canonical cleanliness direction](../../canonical-source-cleanliness-direction.md),
but are not implemented in this checkout yet. The seven materialized files may
therefore still contain the legacy embedded custody representation.

## Results

| # | Source | Coverage | Outcome | Triage |
|---:|---|---|---|---|
| 01 | `official/image/flux2_klein_4b_t2i.json` | Note-bearing official image; primitive input | Refused: `primitive_literal_invalid` for `PrimitiveInt` node `75::68` | Importer/source type normalization defect; preserve as a regression fixture |
| 02 | `official/edit/qwen_image_edit.json` | Official edit; native recursive boundary markers | Refused: `unsupported_boundary_encoding` | Boundary mapping/explicit-refusal policy; must be covered by subgraph tests |
| 03 | `official/audio/ace_step_1_5_t2a_song.json` | Official audio; 10 API nodes | Materialized `03_ace_step_1_5_t2a_song.py` plus layout JSON | Positive baseline |
| 04 | `official/video/wan_i2v.json` | Official video I2V; MarkdownNote | Materialized `04_wan_i2v.py` plus layout JSON | Positive note-bearing baseline |
| 05 | `official/video/wan_t2v.json` | Official video T2V; 11 API nodes | Materialized `05_wan_t2v.py` plus layout JSON | Positive baseline |
| 06 | `custom_nodes/qwen_tts/1038lab/qwen3_tts_custom_voice.json` | Custom audio; 2 API nodes | Materialized `06_qwen3_tts_custom_voice.py` plus layout JSON | Positive custom-node baseline |
| 07 | `custom_nodes/ltxvideo/iamccs/IAMCCS_LTX23_BEST_3SEG_AUDIOEXT_30S_FREE_LOW_RAM.json` | Helper/note-heavy custom video/audio; 74 API nodes | Materialized `07_ltx23_best_3seg_audioext_low_ram.py` plus layout JSON | Positive large-graph baseline |
| 08 | `custom_nodes/ltxvideo/lightricks_2_3/LTX-2.3_ICLoRA_HDR_Distilled.json` | Model-heavy custom video; 24 API nodes | Materialized `08_ltx2_3_iclora_hdr.py` plus layout JSON | Positive model/control baseline |
| 09 | `custom_nodes/qwen_tts/1038lab/qwen3_tts_voice_clone.json` | Custom audio; 3 API nodes | Materialized `09_qwen3_tts_voice_clone.py` plus layout JSON | Positive small custom baseline |
| 10 | `tests/fixtures/recursive_live_contract/depth2.json` | Depth-two/edge fixture | Refused: `Unsupported workflow shape: unknown` | Fixture-shape/diagnostic contract gap; keep as malformed-input test |
| 11 | `official/image/flux2_klein_9b_t2i.json` | Official image; native recursive boundary markers | Refused: `unsupported_boundary_encoding` | Same boundary coverage as 02 |
| 12 | `official/image/qwen_image_2512.json` | Official image; switch widgets | Refused after parity: `ComfySwitchNode` widget values differ | In-scope parity defect or explicit source compatibility rule; needs regression |
| 13 | `official/video/ltx2_3_t2v.json` | Official video; native recursive boundary markers | Refused: `unsupported_boundary_encoding` | Same boundary coverage as 02 |
| 14 | `custom_nodes/ltxvideo/runexx/LTX-2.3_Talking_Avatar_Qwen_TTS.json` | Large custom audio/video; native recursive boundary markers | Refused: `unsupported_boundary_encoding` | Boundary coverage plus custom-node preservation |
| 15 | `custom_nodes/ltxvideo/runexx/LTX-2.3_V2V_Extend_Any_Video.json` | Custom V2V; native recursive boundary markers | Refused: `unsupported_boundary_encoding` | Boundary coverage plus edit/rebuild proof |
| 16 | `custom_nodes/ltxvideo/lightricks_2_3/LTX-2.3_ICLoRA_Motion_Track_Distilled.json` | Custom control workflow; stale endpoint | Refused: UI link 2 references unknown endpoint `2004`/`2653` | Source endpoint validation/repair or explicit refusal |
| 17 | `custom_nodes/ltxvideo/lightricks_2_3/LTX-2.3_ICLoRA_Union_Control_Distilled.json` | Custom control workflow; stale endpoint | Refused: UI link 2 references unknown endpoint `2004`/`2653` | Same endpoint-validation coverage as 16 |
| 18 | `custom_nodes/wanvideo_wrapper/kijai/wan21_14b_flf2v.json` | Custom FLF2V; virtual-wire output | Refused: `unknown_virtual_wire_port` for `end_image` | Virtual-wire/native-roster preservation defect or explicit refusal |
| 19 | `custom_nodes/wanvideo_wrapper/kijai/wan22_5b_i2v.json` | Custom I2V; output arity and model paths | Refused after parity: WanVideo output/model representation differs | Output-arity/model canonicalization defect; must not silently emit |
| 20 | `custom_nodes/ltxvideo/iamccs/IAMCCS_LTX2_AU_IMG2V.json` | Large custom audio/I2V; audio fan-in | Refused after parity: missing `VHS_VideoCombine.audio` topology | Topology/parity defect; must be a regression fixture |

## Failure taxonomy and plan extension

The 20-case run identifies six distinct classes to handle in the implementation
and test plan:

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
contains `build_ok: true`.

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
scope-qualified identity. The current corpus is a baseline for this check; it
cannot pass the v2 cleanliness assertions until the planned emitter changes land.

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

- Seven positive Python outputs and their generated layout JSON are in this
  directory.
- All 20 command receipts are in this directory.
- Three exploratory refusal receipts from nearby alternatives are under the
  earlier `workflow-review-set-20260911/exploratory-failures/` directory.
- The quick-view folder with ten selected files is
  `../workflow-review-outputs-10-20260911/`.
