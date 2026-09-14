# M6 Public API Surface

This artifact records the code-level public import surface settled for M6.
It is intentionally limited to API facts; broader narrative documentation belongs
to the M7 documentation pass.

## API Export Path

Use `VibeWorkflow.compile("api")` to export a workflow to the ComfyUI API JSON
shape accepted by runtime execution.

Do not add or document a separate `export_to_json` public method for M6. Existing
source and test code does not require it, and `compile("api")` is the supported
single export path.

`compile("api")` is a projection, not a persistence operation. For a loaded
canonical candidate, `load_bundle()`/`WorkflowBundle.compile()` provide the
identity- and revision-bound approval path; the returned record contains the
API projection, UI projection, input binding, revision, and API digest. A
legacy `.layout.json` sidecar is layout evidence only and is never the
semantic/API authority. Canonical converted Python is paired with a validated
same-basename `.vibe.json` companion; that companion carries identity,
provenance, custody, and presentation annotations without changing the
`compile("api")` projection contract.

## Import, drafts, and native subgraphs

`load_workflow_any` and the CLI onboarding path may ingest a source workflow
with unresolved class schema as a draft. Schema diagnostics remain attached to
the report; conversion must not invent widget meanings. Strict-ready checks
and ready-template promotion are separate gates and refuse unresolved
schema-backed requirements until provider evidence is available.

Native ComfyUI definitions are materialized before canonical IR construction
when they contain both `inputNode` and `outputNode` plus an unambiguous,
supported boundary mapping. Instances become namespaced node identities and
their boundary/fan-out links become ordinary `VibeEdge` handles. Expansion
records source provenance and diagnostics. Missing/ambiguous markers,
unsupported nesting, malformed links, contradictory backlinks, or unmapped
native edges fail closed with `unsupported_boundary_encoding`; no partial
canonical candidate is published.

## Top-Level Imports

The following names are public from `vibecomfy` and are present in
`vibecomfy.__all__`.

### Loaders

- `load_workflow_any`
- `load_workflow_json`
- `workflow_from_file`
- `workflow_from_id`
- `workflow_from_ready`
- `ready_template_ids`

### Template Compatibility Aliases

- `workflow_from_template`
- `load_template`

### Runtime Helpers

- `run`
- `run_sync`
- `run_embedded`
- `run_embedded_sync`

### Ops Namespaces

- `image`
- `video`

### Core IR Types

- `VibeWorkflow`
- `VibeNode`
- `VibeEdge`
- `VibeInput`
- `VibeOutput`
- `WorkflowRequirements`
- `WorkflowSource`
- `ValidationIssue`
- `ValidationReport`

### Handles

- `Handle`

Handles are the source-level wiring authority. Emitted constructor kwargs use
named handles/output attributes; raw numeric API link pairs and native boundary
payloads are derived at the projection doors, not duplicated as ordinary
runtime values. Stable node UID/source identity and provenance are retained
alongside the semantic graph so save/reload/export can verify the same
candidate.

### Layer-2 Namespaces

- `blocks`
- `patches`
- `router`

### Artifact Result Types

- `Artifact`
- `Image`
- `Video`
- `Audio`
- `Latent`
- `Mask`

### Plugin Hook

- `ensure_plugins_loaded`
