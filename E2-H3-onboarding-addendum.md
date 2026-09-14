# H3 onboarding evidence — 2026-09-10

- Implementation checkout: `otto/unified-workflow-integrity-20260909`, based on current `main` (`0d731926779112e1dfcf7d8f22b59550ceff66b7`).
- Exact source: `docs/handover/unified-workflow-integrity-20260909/assets/h3/MiniMax_H3_AV_EncodeDecode_Inpaint.json`
- Source SHA-256: `2dd64fe26c42281962e434841c458cc935b1d1858e83093b882bbaeb02dc3121`.
- The shared native-subgraph owner expands the supported H3 definitions before normalizing through the same SDK/CLI/canvas path. Malformed or unsupported boundary encodings fail closed as `unsupported_boundary_encoding`.
- Exact CLI conversion produced an editable Python artifact with 24 expanded source nodes / 29 source edges, 20 emitted runtime nodes / 25 edges, and no `wf.connect` replay tail or native/UI evidence payload in the source. The artifact parses and reloads.
- The expected local schema/custom-node limitation remains accurately represented as draft validation diagnostics: `LanPaint_*`, `MiniMaxH3ImageToVideo`, and the stale `CLIPLoader` enum are not installed in this headless environment. This blocks strict-ready promotion/runtime execution, not draft conversion or editability.
- Edit/rebuild evidence changed model, steps, prompt, duration, seed, LanPaint steps, source video, keyframes, and audio intervals. Reload preserved the edits; exact UI export was deterministic at 20 nodes / 25 links.
- Inspectable artifacts are under `.otto/runs/unified-workflow-integrity-20260909/evidence/h3/`: `MiniMax_H3_AV_EncodeDecode_Inpaint.generated.py`, `MiniMax_H3_AV_EncodeDecode_Inpaint.edited.py`, `MiniMax_H3_AV_EncodeDecode_Inpaint.edited.exported.json`, `MiniMax_H3_AV_EncodeDecode_Inpaint.edited.layout.json`, the PNG layout, and the `inspect-*.json` / `graph-inspection.md` reports.
- No GPU, network, or video-quality claim is made.
