# E2 regression batch receipt

Date: 2026-09-10

The regression batch covered the shared native-link classifier, scoped IDs, draft/strict CLI gating, H3 boundary mapping, and generated-source edge authority. The one stale fixture expectation was updated to assert canonical edge materialization while preserving valid importer-shaped draft pairs.

Verification:

- `git diff --check` — passed.
- `PYTHONPYCACHEPREFIX=/tmp/vibecomfy-pyc /usr/bin/python3 -m py_compile vibecomfy/commands/port/_convert.py vibecomfy/porting/emit/emit_prepare.py` — passed (2 files).
- Focused H3/native/emitter/foundation gate: **169 passed**, 0 failed.
- Required Q5 workflow-integrity/edit/revision matrix: **617 passed, 2 skipped**, 0 failed/errors.
- Expanded affected matrix including CLI/native/UI-emitter, foundation, edge-case, and codemod coverage: **941 passed, 11 skipped**, 0 failed/errors.
- `git diff --check`: passed.
- Exact H3 CLI conversion, edit → rebuild → reload → deterministic export: passed; see `.otto/runs/unified-workflow-integrity-20260909/evidence/h3/`.
- CLI, SDK, and canvas valid-input parity plus malformed-input refusal: passed; see `.otto/runs/unified-workflow-integrity-20260909/evidence/entrypoint-parity/parity-report.json`.

Known non-failure notes: pytest reports 28 warnings from the repository's disabled-plugin/headless configuration and schema-less fixture paths. Strict-ready H3 promotion remains blocked by absent local custom-node/schema providers, as recorded in the H3 evidence; draft conversion and source editability are complete.
