# H3 correction evidence — 2026-09-10

The exact input was `assets/h3/MiniMax_H3_AV_EncodeDecode_Inpaint.json` with
SHA-256 `2dd64fe26c42281962e434841c458cc935b1d1858e83093b882bbaeb02dc3121`.

Draft conversion through `vibecomfy port convert` completed with `build_ok`,
`compile_ok`, and `parity_ok`; the generated artifact has 20 runtime nodes and
25 effective edges. The edited artifact is
`MiniMax_H3_AV_EncodeDecode_Inpaint.edited.py`, SHA-256
`c3d3d18ab5980a7a0bc021cede9061e98caf4c84a4c781ed479ec76ba722043b`.

The generated source sets `DEFAULT_SEED = 123`. Restricted import and build
inspection passed with the seed retained on the `RandomNoise` node; the source
contains no `wf.connect` calls. The normal offline path reports unresolved
LanPaint/MiniMax schema providers, so strict-ready promotion, GPU execution,
and video-quality claims remain intentionally unmade.

Presentation-sidecar/render inspection is not claimed here: no valid edited
sidecar was produced by the draft conversion path, and no GPU/runtime viewer
was available. This is a residual H3 evidence blocker for final Astra review.
