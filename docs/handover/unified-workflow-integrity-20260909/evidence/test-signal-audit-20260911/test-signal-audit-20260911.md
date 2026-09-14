# Test-signal audit — 2026-09-11

Status: planning only; static inspection, not test collection or execution.

User authorized Luna swarms to categorize current tests and one Astra high planning adjudication. No product/test cleanup authorized in this planning turn. Preserve existing exhausted execution-review history and S90 overrun; this is a separate supplemental planning decision, not a new delivery review stage.

Baseline: isolated worktree HEAD c43e870d6c15ac9a31c0141d3212ae3a032d86ac. Existing planning modifications preserved.

## Inventory and delegated coverage

Completed decision: [single Astra high ruling](test-signal-astra-20260911.md),
adopted in the source handover test-signal-cleanup-plan.md. One explicit
supplemental planning call charged 1/1; no execution review or historical reset.

541 conventionally named test-bearing files under tests, assigned exactly once by filename routing. This is not 541 collected tests: parameters, dynamically registered cases, helpers, fixtures and tests outside tests require separate accounting. Each slice must state deep versus shallow inspection and actual behavioral category.

- [browser-comfy-node](./test-audit-20260911-browser-comfy-node.md): 76 files; Luna medium 01a09045-0846-7973-b0b3-35f29c657775.
- [editing-transactions-layout](./test-audit-20260911-editing-transactions-layout.md): 44 files; Luna medium 01a09045-0891-7fd2-a973-ce582a75b0dd.
- [schema-registry-naming](./test-audit-20260911-schema-registry-naming.md): 49 files; Luna medium 01a09045-08d5-70b0-8409-d575292cd106.
- [workflow-format-roundtrip](./test-audit-20260911-workflow-format-roundtrip.md): 70 files; Luna medium 01a09045-0928-7591-ab02-a881782c2867.
- [runtime-agent-harness](./test-audit-20260911-runtime-agent-harness.md): 143 files; Luna medium 01a09045-097d-7593-b760-b6b6dd98dba0.
- [crosscutting-test-infrastructure](./test-audit-20260911-crosscutting-test-infrastructure.md): 159 files; Luna medium 01a09045-09b4-7a03-b629-b3ee6e953f1a.

## Coordinator CI/context inspection

All six Luna reports completed. Coordinator checked each table against its manifest: 76 + 44 + 49 + 70 + 143 + 159 = 541 rows, no missing or extra assigned paths. This verifies inventory coverage, not full assertion-by-assertion review. Individual disposition totals are advisory and are not a deletion quota. An agent's final-message claim about dirty schema/validate.py refers to the protected receiving checkout, not evidence of a source change in this isolated worktree; coordinator git status showed planning documents only.

Do not adopt suggestions to quarantine low-relevance suites merely to shrink acceptance. Defer means retain unchanged in their existing lanes, not suppress failures or weaken final configured coverage. Existing compatibility placeholders may be intentional shims; inspect their consumers before treating them as missing tests.

- Existing tiers already exist: Makefile fast/ci, broad-pytest, browser-smoke, browser-contracts, e2e-browser, parity, snapshots, oracle and corrective trust gate. Reuse and clarify rather than introduce another framework.
- .github/workflows/ci.yml runs make ci; a separate real-browser job runs extension_boot only. Browser boot is not complete edit/apply/save/reload validation.
- .github/workflows/broad-python.yml runs broad-pytest on schedule/manual, explicitly non-required. A fast PR pass is not whole-suite evidence. Do not silently change branch protection or CI policy during cleanup.
- tests/README.md already distinguishes live-model, structural agentic, mocked executor contracts and browser e2e. Extend this taxonomy, don't create competing definitions. Its claim of baseline failures is documentation, not freshly reproduced status.
- tests/conftest.py:189 defaults on-demand schemas off; tests must deliberately exercise production-on acquisition separately. :203 resets workflow context between tests; failure-followed-by-success state tests must stay within one test to reveal leakage.
- pyproject defaults exclude GPU; live/RunPod opt-ins and skipped/xfail/quarantine reports must remain explicit. Current timing, flakiness and warning rates are unknown without execution; historical counts cannot certify the planned candidate.

## Decision criteria

Additional verified correction: tests/test_live_agentic_harness_runner_persistence.py is a documented D13 compatibility path that imports all tests from tests.test_live_agentic_runner_persistence; it is NOT an empty no-assertion test hole. Broad collection may duplicate imported tests, which is a future collection/consumer-mapping question, not justification for invented new persistence requirements. The runtime slice's finding 5 is superseded by this source check. Also, tests/edgecases/test_determinism.py's purported API-hash test actually hashes result.text, repeating the text-equality invariant; this is a well-supported focused consolidation/rename candidate.

Coordinator spot-check: the bare SHA hexdigest assertion in test_wrapper_codegen.py:40 is tautological, but preceding assertions prove cross-timestamp source/hash determinism. Strengthen that individual assertion; do not classify the entire test as valueless. The sentinel tests at test_nodes_install.py:598–633 pair count checks with explicit result status, commit SHA and sentinel removal, so they are not count-only tests. Preserve those protections. Slice recommendations to add concurrency machinery or blanket structural-edit refusal are not automatically adopted: the existing direction owns supported edits, direct binding compatibility and pair publication guarantees. Do not extend those contracts through a test-cleanup recommendation.

Optimize distinct defect detection, actionable diagnosis and maintenance cost—not a numerical deletion quota. Retirement requires a concrete equivalent or stronger replacement and preservation of independent expected semantics, failure/refusal, security, identity, revision and rollback guarantees. Shared roundtrip helpers alone are not independent oracles. Preserve parametrization where cases cover distinct boundaries. Scope cross-product testing to demonstrated interactions.
