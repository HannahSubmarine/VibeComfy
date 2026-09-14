# Import and edit a ComfyUI workflow

Import turns a saved ComfyUI JSON workflow into Python that you or a coding
agent can read and edit. Start in the directory where you want to keep your
workflows. These examples assume VibeComfy is installed; in an editable
checkout, `python -m vibecomfy.cli` is equivalent to `vibecomfy`.

## 1. Import the source

```bash
vibecomfy import path/to/my_workflow.json
```

This creates a folder relative to your current directory:

```text
workflows/my_workflow/
  workflow.py
  workflow.vibe.json
  source.json
```

| File | What it is for |
| --- | --- |
| `workflow.py` | Your editable workflow: node calls, values, and connections. |
| `workflow.vibe.json` | VibeComfy's companion data for identity, source bookkeeping, and visual layout. Keep it beside the Python file. |
| `source.json` | The unchanged original JSON, for comparison or a fresh import. Editing it does not change `workflow.py`. |

Source hashes and conversion provenance use the existing bundle metadata.
There is no separate import manifest. Move or share the whole folder to keep
these files together; importing preserves the graph, not the models or custom
node packages it depends on.

The folder name comes from the source filename, with unusual characters
sanitized. Use the path printed by the command. To choose a destination:

```bash
vibecomfy import path/to/my_workflow.json --out workflows/my_variant
```

`--out` names a **directory**, not a Python file. Existing destinations are
refused so an import cannot replace your edits. `--dry-run` previews the
conversion without creating the output folder; `--json` returns the result
and diagnostics for scripts or agents.

## 2. Find what you want to change

The import result prints the file paths and follow-up commands. You can open
`workflow.py` immediately. When you want help understanding it, these optional
commands describe the workflow built from that code:

```bash
vibecomfy inspect workflows/my_workflow
vibecomfy analyze info workflows/my_workflow
```

`inspect` summarizes node and edge counts, public inputs and outputs, and
declared model and custom-node requirements. It loads the Python and companion
and performs compilation checks; it does not just print the source file.
`analyze info` provides the graph details. Use those node classes and input
names to locate the corresponding calls in `workflow.py`.

To understand a node's parameters and sockets, ask for
its class specification. For example, for an image-saving node:

```bash
vibecomfy nodes spec SaveImage
```

`nodes spec` already returns JSON: `inputs` contains parameter types, required
flags, defaults, and choices where known; `outputs` lists the output sockets.
It also records where the schema came from. This describes the node interface,
not its implementation code. A schema's `source_path` may be absent when it
came from cached ComfyUI metadata.

For a focused view, if you have `jq` installed:

```bash
vibecomfy nodes spec SaveImage | jq '.inputs'
vibecomfy nodes spec SaveImage | jq '.outputs'
```

There are currently no `--inputs`, `--outputs`, or source-code display options
on this command.

Some workflows also expose named public controls. `analyze info` lists their
inputs; `inspect --field <name>` traces an existing public control to its node
and field. A workflow need not expose every prompt, seed, or step count as a
public control: you can still edit its existing Python node arguments.

Inspection can report missing schemas. If that prevents it from describing
the graph, use `doctor` as described below and read the generated Python in
the meantime.

## 3. Edit the Python file

Open `workflows/my_workflow/workflow.py`. Change the existing argument that
controls the behavior you want. For example, if a `SaveImage` call contains:

```python
filename_prefix='out/port'
```

change that argument to:

```python
filename_prefix='out/edited'
```

This changes the output filename prefix when the workflow is eventually run.
Keep the surrounding node call and its image connection intact. Prompts,
seeds, and step counts can be adjusted at their corresponding calls in the
same way. Confirm unfamiliar argument names with `nodes spec`.

For graph changes, use the Python node calls and supported `VibeWorkflow`
methods such as `add_node`, `connect`, and `remove_node`. The
[editing skill](../agent-skill/skills/edit-comfy-workflow/SKILL.md) explains the
agent workflow; [Authoring](../authoring.md) covers Python composition.
The companion JSON is maintained by VibeComfy: do not repair validation
errors by manually changing its identity or binding fields.

## 4. Validate the edited workflow

After saving your edit, run:

```bash
vibecomfy validate workflows/my_workflow
```

A successful check prints `ok`. Validation reloads the Python and companion,
checks their relationship, and checks compilation against the available node
schemas. It does not queue generation. An error should be fixed in the
workflow or its dependencies, then checked again.

Read warnings as well as the exit status: a schema-less fallback means some
node details could not be checked, even if the command completed successfully.

To investigate missing node schemas, models, or other dependency findings:

```bash
vibecomfy doctor workflows/my_workflow
```

`doctor` uses local information. Model-presence checks depend on a configured
`VIBECOMFY_MODELS_ROOT`; it cannot inventory an unconfigured remote server.

A successful import means an editable bundle was created. A successful
validation means the available checks passed. Neither establishes that a
particular ComfyUI server has all the dependencies or that generation will
succeed.

Both commands accept `workflow.py` directly as well as the folder. Always
validate the file or folder you actually edited. Add `--json` for structured
results and use the exit status to detect failures in automation.

## If something needs attention

| Situation | Next step |
| --- | --- |
| The destination already exists | Open that folder to continue editing, or import to a different `--out` directory. |
| A class schema is missing | Run `doctor` on the imported folder. `vibecomfy schemas ensure workflows/my_workflow/workflow.py` is the schema-recovery entry point; follow its diagnostics for your environment. |
| You want a limited structural check while schemas are missing | Use `vibecomfy validate workflows/my_workflow --no-schema`. This is a weaker check, not full schema validation. |
| Import reports `unsupported_boundary_encoding` | The source contains a native subgraph boundary the importer cannot safely represent. No completed folder is published. Keep the source and the diagnostic when reporting the problem. |
| A load asks for confirmation | Loading authored Python follows the existing capability policy. In intentional unattended use, `--yes` accepts those prompts; `--non-interactive` refuses actions that require confirmation. |

## Make a separate variation with Python

Directly editing the imported Python is the shortest path. If you want a
separate recipe that loads it and changes public controls, save the following
as **`recipes/workflow_variation.py`**, not as the imported `workflow.py`:

```python
from vibecomfy.cli_loader import load_bundle


def build():
    wf = load_bundle("workflows/my_workflow").workflow
    wf.set_prompt("a glass teapot on basalt")
    wf.set_seed(42)
    wf.set_steps(20)
    return wf.finalize_metadata()
```

This example requires the loaded workflow to expose those public controls.
Run from the project directory so its relative path resolves, and validate
**the variation**:

```bash
vibecomfy validate recipes/workflow_variation.py
```

The variation depends on the imported folder. Keep both when moving it to
another project.

## Next steps

- **Run the edited workflow:** follow the [run-workflow skill](../agent-skill/skills/run-comfy-workflow/SKILL.md) to choose a runtime and check its dependencies.
- **Export back to ComfyUI:** see [Emitting a UI view](../authoring.md#emitting-a-ui-view).
- **Add a reusable library template:** follow [Adding templates and models](../templates/adding_templates_models.md).
- **Use advanced conversion controls:** the [porting workbench](../templates/porting_workbench.md) documents `port check`, `port convert`, and strict-ready promotion. `workflows onboard` prints a multi-step plan; it does not execute an import.
