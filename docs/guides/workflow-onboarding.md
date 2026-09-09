# Workflow onboarding

Use this path when you have a workflow from ComfyUI or an upstream repository and want a local, editable VibeComfy surface.

## 1. Save the source and provenance

Keep the upstream file unchanged under a stable source path, and record its URL, upstream commit or release, local path, and SHA-256. For example, the MiniMax H3 AV inpainting source used by the Matrix experiment is:

- upstream: [LanPaint `MiniMax_H3_AV_EncodeDecode_Inpaint.json`](https://github.com/scraed/LanPaint/blob/32cf848e93971da380d868936e007f5611218bee/example_workflows/MiniMax_H3_AV_EncodeDecode_Inpaint.json)
- local: `planning/comfy-inspection/MiniMax_H3_AV_EncodeDecode_Inpaint.json`
- SHA-256: `2dd64fe26c42281962e434841c458cc935b1d1858e83093b882bbaeb02dc3121`

Keep source JSON as evidence. Put hand edits in a recipe or scratchpad so the upstream graph can still be compared with the candidate.

## 2. Preflight, then understand the graph

From the VibeComfy repository root, use the console entrypoint (or replace `vibecomfy` with `python -m vibecomfy.cli` in an editable checkout):

```bash
vibecomfy port check path/to/workflow.json --json
vibecomfy inspect path/to/workflow.json --json
vibecomfy analyze info path/to/workflow.json
```

For a ready template, discovery and inspection use its id:

```bash
vibecomfy workflows list --ready
vibecomfy inspect image/z_image --json
```

`inspect` and `analyze info` describe the graph and public inputs; they do not prove that models, custom nodes, a ComfyUI checkout, or a server are available. If a class schema is missing, `doctor` identifies the gap and the supported recovery command is `vibecomfy schemas ensure <workflow>`; provisioning is an environment change and should be treated separately. A missing schema does not by itself prevent a draft scratchpad from being emitted.

## 3. Materialize the editable Python candidate

For a supported source workflow, convert it to a scratchpad and keep the emitted path as the canonical edit surface:

```bash
vibecomfy port convert path/to/workflow.json \
  --out out/scratchpads/my_workflow.py --json
vibecomfy inspect out/scratchpads/my_workflow.py --json
```

For a curated ready template, copy a user-specific recipe instead:

```bash
vibecomfy copy-to-recipe image/z_image --out recipes/my_run.py
```

Load the candidate through `load_bundle()` before editing or running. A minimal recipe looks like this:

```python
from vibecomfy.cli_loader import load_bundle


def build():
    wf = load_bundle("image/z_image").workflow
    wf.set_prompt("a glass teapot on basalt")
    wf.set_seed(42)
    wf.set_steps(20)
    return wf.finalize_metadata()
```

Use `vibecomfy inspect <candidate> --field <PUBLIC_INPUTS field>` when you need to resolve one public handle. Use `vibecomfy nodes spec <ClassType>` before relying on a custom node's sockets or widgets.

### Native subgraphs

Native ComfyUI definitions with a complete `inputNode`/`outputNode` boundary are
supported on the normal import path. VibeComfy materializes each instance into
namespaced nodes (for example, `105::6`), maps boundary inputs/outputs and
fan-out into ordinary named edges, and carries a source hash and expansion
diagnostics as provenance. The expanded graph then uses the same canonical
normalizer and Python emitter as any other workflow.

The expansion is deliberately fail-closed. Missing or ambiguous boundary
rosters, unsupported nesting, contradictory socket backlinks, malformed links,
or unmapped native edges produce `unsupported_boundary_encoding` and do not
write a candidate. Preserve the original JSON and provenance when this occurs.

## 4. Edit, validate, and inspect readiness

Make the smallest change in the Python candidate, then run structural and dependency checks:

```bash
vibecomfy validate out/scratchpads/my_workflow.py --json
vibecomfy doctor out/scratchpads/my_workflow.py --json
vibecomfy runtime doctor --json
```

`validate`/`doctor` describe the candidate. `runtime doctor` reports local runtime findings; configured `models` or `custom_nodes` directories alone do not make embedded execution ready, and an external server remains unverified until a URL is supplied to a run.

Only after the candidate and runtime are ready should execution be attempted, for example:

```bash
vibecomfy run out/scratchpads/my_workflow.py \
  --runtime server --server-url http://127.0.0.1:8188
```

## Evidence and blockers

There are four distinct claims:

1. **Source evidence:** the saved JSON, provenance, and inspection output show what the upstream graph contains.
2. **Draft candidate:** conversion produced a structurally valid Python scratchpad. Unresolved class schemas remain visible in the report and may make fields unavailable; this is not a claim of strict readiness or runtime execution.
3. **Strict readiness:** `port check --strict-ready-template`, `port convert --strict-ready-template`, or ready-template promotion with `--ready-id` passed the provider-backed gates, including required schema/widget resolution.
4. **Runtime readiness:** the selected ComfyUI runtime, custom nodes, models, and server or embedded environment were checked.

Do not promote one claim into another. The H3 example's supported native
recursive boundary is expanded during conversion; unresolved schemas can still
leave the result as a draft, and strict-ready promotion can still refuse it
until schema evidence is available. A malformed or unsupported boundary still
reports `unsupported_boundary_encoding` and writes no candidate. That is an
import representation blocker, not proof that the upstream graph or models are
invalid.

For a durable authored candidate, `load_bundle()` binds the Python source to a
workflow identity, semantic digest, provenance, revision, and optional UI
sidecar. `emit_bundle()` publishes the Python and canonical `.vibe.json` pair
atomically; reload validates that identity and revision before approval. The
legacy `.layout.json` sidecar is presentation-only and optional: `port export
--to ui` uses it for layout preservation, persists it on the canonical output
path, and does not update it for an explicit `--out` unless
`--persist-sidecar` is supplied. Use `--from` for an explicit prior UI source,
`--fresh` to discard preservation evidence, and `--dry-run` for a no-write
preview.
