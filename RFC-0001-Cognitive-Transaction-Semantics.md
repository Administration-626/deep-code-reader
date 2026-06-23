# RFC-0001: Cognitive Transaction Semantics

**Status:** Final / Frozen
**Date:** 2026-06-23

## 1. System Positioning
`deep-code-reader v2` is **NOT** an AI code summarization tool.
It is a **Cognitive Transaction Engine** designed to maintain long-lived, incrementally updated, verifiable cognition state. Its architecture is structurally isomorphic to distributed databases and build systems like Bazel. The primary goal is preventing **"silent cognition rot"** as the codebase evolves over time.

## 2. Non-Negotiable Invariants
To prevent protocol drift and catastrophic "optimizations", the following invariants are absolute:
1. **Stale Cognition is Worse Than Over-Invalidation:** False Positives (over-rerunning) only waste tokens. False Negatives (under-invalidation) silently poison the AI's understanding.
2. **Verification is Replaced, Never Merged:** To prevent ghost gaps and stale states, dirty module metadata must be atomically regenerated. Never append.
3. **Agents Analyze, Protocol Decides:** Invalidation routing and plateau limits are deterministic. They must never be delegated to heuristic AI decision-making.
4. **100% Local Pass != Global Understanding:** A trivial patch yielding 100% pass rate must not overwrite the module's historical complexity confidence.
5. **Phase 5 is Synthesis, Not Concatenation:** Global manifests and cross-module scenarios must be semantically regenerated from fresh metadata, not string-concatenated.
6. **Benchmark-Before-Feature:** No "smart" skips or heuristic optimizations may be merged without first passing the deterministic state integrity benchmark.

## 3. Failure Taxonomy
Not all failures are equal. We classify cognition degradation into three severity levels:

| Failure Mode | Severity | Description |
| :--- | :--- | :--- |
| `false_negative` | **P0** | A dirty dependency was missed, allowing stale knowledge to survive. |
| `stale_manifest` | **P0** | The global index points to renamed/deleted files. |
| `cognition_poisoning` | **P0** | The AI utilizes hallucinated schemas from skipped updates. |
| `ghost_state` | **P1** | Deprecated arrays (e.g. `open_gaps`) accumulate via append. |
| `stale_routing` | **P1** | Cross-module architectural scenarios fall out of sync. |
| `orphan_manifest` | **P1** | Deleted modules leave dangling metadata references. |
| `over_invalidation` | **P2** | An isolated file triggered an unnecessary avalanche (token waste). |
| `unnecessary_phase5` | **P2** | Global manifest regenerated without cross-module impact. |

## 4. Transaction Lifecycle (Cognitive ACID Pipeline)
Every incremental update must strictly follow this atomic pipeline:
1. **Detect:** Diff the file system against `.metadata.json` (Phase 0).
2. **Invalidate:** Trace the dependency graph and mark affected nodes dirty.
3. **Regenerate:** Atomically wipe verification states for dirty modules.
4. **Verify:** Execute the Agent A/B/C reading loops (Phases 1-4).
5. **Synthesize:** Regenerate the global cross-module manifest (Phase 5).
6. **Commit:** Persist the byte-stable `.metadata.json`.

## 5. State Integrity vs. AI Intelligence
We validate this protocol through **Deterministic Benchmarks** rather than LLM benchmarks. We measure *State Integrity* (Does the system cleanly propagate invalidations and purge ghosts?) rather than *AI Intelligence* (Did the AI write good code?). Mixing LLM non-determinism into protocol testing makes it impossible to isolate state corruption bugs from prompt fluctuations.

## 6. Explicitly NOT IMPLEMENTED (And Why)
The following features are highly requested but explicitly frozen and excluded from the current protocol until scaling correctness is proven:
- **Semantic Incremental:** (e.g., AST-level diffing)
- **Smart Skip:** (e.g., skipping tests if only documentation changed)
- **Confidence-based Skipping:** (e.g., skipping rerun because past confidence was 100%)
- **Heuristic Invalidation Reduction:** (e.g., Agent guessing if an import change matters)

**Reason:** The correctness guarantees of these optimizations have not yet been benchmark-proven. Introducing them now would compromise the transaction integrity of the system.
