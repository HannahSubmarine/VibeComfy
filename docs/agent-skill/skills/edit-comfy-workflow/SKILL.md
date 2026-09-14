---
name: edit-comfy-workflow
description: Edit an existing VibeComfy or ComfyUI workflow, ready template, recipe, scratchpad, or target graph. Use when the user asks to tweak prompts/seeds/steps/resolution, alter nodes, splice a pattern into a workflow, convert JSON to editable Python, or make a graph change without necessarily running it.
---

# Edit Comfy Workflow

Use this when the graph needs to change. Follow the same shape as the agentic tests: identify the target, inspect it, materialize an editable Python surface if needed, make the smallest graph change, then validate.

## Shared Edit Spine

Use the same spine as the Comfy app agent edit path and the structural/live agentic tests:

```text
target graph -> inspect/research -> Python editable surface -> VibeWorkflow edit -> finalize_metadata -> validate/doctor -> candidate or run
```

For package-side edits, the editable surface is a recipe, scratchpad, or ready template. For the Comfy app, the same idea returns a candidate UI graph plus apply eligibility. Do not treat an edit candidate as an executed result; execution belongs to `run-comfy-workflow`.

## Fast Path

```bash
vibecomfy inspect <target>
vibecomfy analyze info <target>
```

If the target is raw JSON, load it only as import evidence and materialize Python before editing:

```bash
vibecomfy import <workflow.json>
vibecomfy inspect workflows/<source-stem> --json
vibecomfy analyze info workflows/<source-stem>
vibecomfy validate workflows/<source-stem> --json
```

The import folder contains editable `workflow.py`, its canonical
`workflow.vibe.json` companion, and byte-identical `source.json`; provenance
stays in the bundle metadata. Edit the existing node arguments in Python for
simple changes. If you use a recipe that loads the imported folder as a
`VibeWorkflow`, common supported controls are `set_prompt`, `set_seed`,
`set_steps`, and `set_input`; first check available fields with
`vibecomfy inspect <folder> --field <field>`. For unfamiliar node parameters,
use `vibecomfy nodes spec <ClassType>` and visible graph evidence. Validate and
diagnose the folder before handing it off.

Use `vibecomfy port check` and `vibecomfy port convert` when you need advanced
preflight, a standalone scratchpad, or the intentional ready-template
conversion path; import does not promote a template.

If the target is a ready template and the edit is user-specific:

```bash
vibecomfy copy-to-recipe <ready_id> --out recipes/<name>.py
```

Then edit the Python recipe, scratchpad, or template.

## Edit Shape

Use the lightest public API that fits:

```python
from vibecomfy.cli_loader import load_bundle

def build():
    wf = load_bundle("image/z_image").workflow
    wf.set_prompt("a glass teapot on basalt")
    wf.set_seed(42)
    wf.set_steps(20)
    return wf.finalize_metadata()
```

Reach for patches when decorating an existing graph. Reach for blocks or direct `VibeWorkflow` methods only when the edit changes handles, splices nodes, or rewires topology.

Never invent node fields, sockets, or class names. Use `vibecomfy nodes spec <ClassType>`, visible graph data, local precedents, or `search-comfy-workflows`.

## Validate

```bash
vibecomfy validate <edited.py>
vibecomfy doctor <edited.py> --json
```

For converted source workflows:

```bash
vibecomfy port doctor-all <source_or_edited_workflow> --json
```

If the edit adds custom nodes:

```bash
vibecomfy nodes install-plan <edited.py>
```

## Return Shape

For package-side edits, return the edited file path and validation evidence:

- recipe/scratchpad/template path
- changed intent in plain language
- `vibecomfy validate` / `vibecomfy doctor` status
- any node/model install plan

For Comfy app style edits, the returned object is a candidate envelope: `outcome.kind`, `candidate.graph`, `apply_eligibility`, graph hashes, change details, and artifact paths such as `candidate.ui.json` / `response.json`. The user still has to Apply or run it.

## Boundaries

- Do not run GPU work unless the user asked to execute or validation requires it.
- Do not promote a one-off composition to `ready_templates`; use `recipes/`.
- Keep upstream JSON close to upstream. Put local edits in Python.
- If the environment is missing, hand off to `vibecomfy-setup`; if execution fails, hand off to `debug-comfy-workflow`.
