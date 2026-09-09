# E0 baseline — unified workflow integrity

Recorded 2026-09-09 from candidate `0d731926779112e1dfcf7d8f22b59550ceff66b7` in the isolated worktree:

`/Users/hannahomalley/Documents/Codex/2026-09-08/goal-continue-the-existing-megado-plan/VibeComfy-integrity/.otto/worktrees/unified-workflow-integrity-20260909`

The worktree was clean before the E0 test-only change. The explicit repository environment was:

```text
/Users/hannahomalley/Documents/Codex/2026-09-08/goal-continue-the-existing-megado-plan/VibeComfy-integrity/.venv/bin/python
Python 3.11.16
pytest 9.1.1
vibecomfy.__file__ = <worktree>/vibecomfy/__init__.py
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1
```

## Existing Q6 baseline

Exact command:

```sh
VENV=/Users/hannahomalley/Documents/Codex/2026-09-08/goal-continue-the-existing-megado-plan/VibeComfy-integrity/.venv
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 "$VENV/bin/python" -m pytest -q \
  tests/test_porting_emitter.py \
  tests/test_h3_generated_editability.py \
  tests/test_native_subgraph_expansion.py \
  tests/test_native_h3_boundary_mapping.py \
  tests/test_h3_schema_widgets.py
```

Result: `140 passed, 0 failed, 0 errors, 0 skipped, 0 xfailed, 0 xpassed` in 25.60s. This is a passing preservation/native-boundary baseline, not I8/I9 proof: the pre-existing assertions accept importer-shaped emitted source.

## Added E0 characterization

Added to `tests/test_porting_emitter.py`:

- AST inspection of ordinary constructor calls for `_id`, `_uid`, and `_native_ports` leakage.
- Whole-source check for `wf.connect` and post-construction `wf.nodes[...]` replay assignments.
- Edit/rebuild check proving an edited constructor default is not overwritten later.
- H3 fixture check that resolver-owned `Reroute` nodes are lowered before emission.

Exact command:

```sh
VENV=/Users/hannahomalley/Documents/Codex/2026-09-08/goal-continue-the-existing-megado-plan/VibeComfy-integrity/.venv
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 "$VENV/bin/python" -m pytest -q tests/test_porting_emitter.py -k 'e0_'
```

Result: `0 passed, 4 failed, 0 errors, 126 deselected`; all four are new, unquarantined failures:

1. `test_e0_canonical_source_uses_handles_without_importer_identity_or_native_payloads`: current calls contain `_id`, `_uid`, and `_native_ports`.
2. `test_e0_canonical_source_has_no_replay_topology_tail`: current source contains `wf.connect(...)` and `wf.nodes[...]` restoration.
3. `test_e0_constructor_edit_survives_rebuild_without_later_replay`: changing the emitted `filename_prefix` constructor value is overwritten; rebuilt value remains `out/sample`.
4. `test_e0_h3_source_lowers_resolver_owned_reroutes`: the H3 review fixture contains `raw_call('Reroute', ...)`.

These assertions intentionally remain failing for E1; no quarantine or implementation workaround was added.

## Current owner map

- CLI port conversion loads through `vibecomfy/commands/port/_convert.py` → `vibecomfy/porting/workbench.py:load_port_source` → existing ingest normalization (`vibecomfy/ingest/normalize.py:from_ui/from_api/normalize_to_api`) → `vibecomfy/porting/convert.py:port_convert_workflow`.
- SDK/canonical emission uses `vibecomfy/porting/emit/entrypoints.py` and delegates canonical, ready, and scratchpad surfaces to the shared emitter implementation in `vibecomfy/porting/emitter.py`.
- Canvas/public capture uses `vibecomfy/workflow_bundle.py:capture_bundle`; layout/presentation persistence remains in `vibecomfy/commands/port/_export.py` and `vibecomfy/porting/layout_store.py`.
- Existing native subgraph expansion and malformed-boundary refusal are owned by the ingest/native expansion path exercised by `tests/test_native_subgraph_expansion.py` and `tests/test_native_h3_boundary_mapping.py`.

The baseline shows the emission seam is the demonstrated E1 defect; it does not justify a second emitter, a global ingest rewrite, or a new custody framework.
