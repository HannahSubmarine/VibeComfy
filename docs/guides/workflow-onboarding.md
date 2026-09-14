# Workflow onboarding

Use this path when you have a ComfyUI workflow and want an editable local copy.

## Import and inspect

Import the JSON into a self-contained folder. The default destination is
`./workflows/<source-stem>/`; `--out` selects a different destination
directory. The destination must not already exist.

```bash
vibecomfy import path/to/my_workflow.json
vibecomfy inspect workflows/my_workflow --json
vibecomfy analyze info workflows/my_workflow
vibecomfy validate workflows/my_workflow --json
vibecomfy doctor workflows/my_workflow --json
```

The imported folder contains `workflow.py` (the editable authoring surface),
`workflow.vibe.json` (the canonical bundle companion), and `source.json` (a
byte-identical copy of the input). The source hash and existing conversion
provenance remain in the bundle metadata; no separate import manifest is
needed. Use `--dry-run` to preview without writing, or `--json` for
machine-readable output.

Import converts the graph for authoring; it does not install nodes or models,
configure a runtime, or run the workflow.

If you need to examine a source before creating a bundle, the advanced porting
commands remain available:

```bash
vibecomfy port check path/to/workflow.json --json
vibecomfy port convert path/to/workflow.json --out out/scratchpads/my_workflow.py --json
```

`port convert` is still useful when you want a standalone scratchpad, a
preflight report, or the advanced ready-template conversion path. For a
reusable curated template, follow [Adding templates and models](../templates/adding_templates_models.md).

## Make a small edit

Open `workflows/my_workflow/workflow.py` and change the existing node argument
that represents the desired value. Use `inspect` or `analyze info` to find
the relevant node and field first. If you want a separate recipe instead of
editing the imported bundle directly, save it as `recipes/workflow_variation.py`.
For example, common `VibeWorkflow` controls are:

```python
from vibecomfy.cli_loader import load_bundle


def build():
    wf = load_bundle("workflows/my_workflow").workflow
    wf.set_prompt("a glass teapot on basalt")
    wf.set_seed(42)
    wf.set_steps(20)
    return wf.finalize_metadata()
```

Only call a setter when the imported graph exposes that input. Use
`vibecomfy inspect workflows/my_workflow --field <field>` to resolve a public
handle, and `vibecomfy nodes spec <ClassType>` before relying on a node's
sockets or widgets. For structural edits, follow the [edit-comfy-workflow
agent skill](../agent-skill/skills/edit-comfy-workflow/SKILL.md); use supported
`VibeWorkflow` methods, patches, or blocks rather than editing compiled API
JSON.

Validate and review the result before execution:

```bash
vibecomfy validate workflows/my_workflow --json
vibecomfy doctor workflows/my_workflow --json
vibecomfy runtime doctor --json
```

Validation checks the candidate; `doctor` reports graph and dependency
findings. Neither installs missing dependencies nor proves runtime readiness.
Only run after the candidate and selected runtime are ready, for example:

```bash
vibecomfy run workflows/my_workflow --runtime server --server-url http://127.0.0.1:8188
```

`inspect` and `analyze info` describe the graph and public inputs; they do not
prove that models, custom nodes, a ComfyUI checkout, or a server are available.
If a class schema is missing, `doctor` identifies the gap and the supported
recovery command is `vibecomfy schemas ensure <workflow>`; provisioning is an
environment change and should be treated separately.

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

## Evidence and blockers

There are four distinct claims:

1. **Source evidence:** the saved JSON, provenance, and inspection output show what the upstream graph contains.
2. **Imported candidate:** import produced the Python and canonical companion bundle, preserving the input as `source.json`. Unresolved class schemas can leave fields unavailable; this is not a claim of runtime readiness or execution.
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
sidecar. The imported folder carries this bundle alongside the original JSON;
`emit_bundle()` publishes the Python and canonical `.vibe.json` pair
atomically; reload validates that identity and revision before approval. The
legacy `.layout.json` sidecar is presentation-only and optional: `port export
--to ui` uses it for layout preservation, persists it on the canonical output
path, and does not update it for an explicit `--out` unless
`--persist-sidecar` is supplied. Use `--from` for an explicit prior UI source,
`--fresh` to discard preservation evidence, and `--dry-run` for a no-write
preview.
