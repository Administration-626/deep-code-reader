# Deep Code Reader v2: Replay Metrics Schema

**Status:** Final / Frozen
**Date:** 2026-06-23

## The Primary Directive
This schema governs the **Longitudinal Cognition Stability Test (Scaling Validation v1)**. It is designed to track the stability of the protocol's state management over 50-200 sequential Git commits on real-world repositories (e.g., `cac`, `clap`, `fd`).

To prevent "changing the benchmark to hide corruption," these four metrics and their acceptable thresholds are **absolutely frozen**. No protocol optimizations may be merged if they compromise these strict thresholds.

---

## 1. False Negative Count (`false_negative_count`)
*Did a module that was functionally impacted by a change fail to be marked dirty?*
- **Severity:** **P0** (Catastrophic Data Corruption)
- **Description:** This occurs when a shared contract or dependency changes, but the protocol fails to avalanche the invalidation to the importing modules. The system will confidently interpret the new codebase using stale schemas.
- **Acceptable Threshold:** **0** (Absolute zero tolerance).
- **Enforcement:** If `false_negative_count > 0` at any point during a 50-commit replay, the protocol is considered structurally broken.

## 2. Orphan Metadata Count (`orphan_metadata_count`)
*Did deleted/renamed modules leave ghost states in the `.metadata.json`?*
- **Severity:** **P1** (Cognition Leak / Ghost State)
- **Description:** This happens when metadata relies on `append` or partial merge semantics rather than strict replacement. It leads to zombie facts, stale gaps, and dead routing paths permanently accumulating in the system's memory.
- **Acceptable Threshold:** **0** (Absolute zero tolerance).
- **Enforcement:** After every commit replay (Phase 5), the symmetric difference between physical modules on disk and logical modules in metadata MUST be exactly zero.

## 3. Byte Instability Count (`byte_instability_count`)
*Did untouched modules suffer from non-deterministic metadata drift?*
- **Severity:** **P1** (Nondeterminism / Metadata Drift)
- **Description:** Modules outside the dirty set must remain strictly byte-identical across the replay cycle. Any change in their timestamps, JSON formatting, or hash values destroys the system's ability to be audited over long timeframes.
- **Acceptable Threshold:** **0** (Absolute zero tolerance).
- **Enforcement:** `diff` between unchanged sections of the metadata before and after the incremental cycle must be completely empty.

## 4. Over-Invalidation Count (`over_invalidation_count`)
*Did the system invalidate more modules than strictly necessary?*
- **Severity:** **P2** (Economic Inefficiency)
- **Description:** Occurs when a trivial change (e.g., modifying comments in a shared file) triggers a massive dependency avalanche.
- **Acceptable Threshold:** **Allowed** (Monitored for efficiency).
- **Enforcement:** Over-invalidation is explicitly permitted and expected. **We gladly accept wasting tokens to guarantee we never waste the integrity of the state.** We monitor this metric purely to measure the token cost of verification, but we will never attempt to artificially reduce it if there is even a 0.01% risk of increasing the `false_negative_count`.

## 5. Dependency Graph Instability Count (`dependency_graph_instability_count`)
*Did the module topology (edges/dependencies) drift non-deterministically across replay cycles?*
- **Severity:** **P1** (Nondeterminism / Graph Drift)
- **Description:** Especially in languages with macros or re-exports (like Rust), identical code checkouts must yield identical dependency graphs. If running the replay twice produces different graphs, we have implicit compiler-level nondeterminism.
- **Acceptable Threshold:** **0** (Absolute zero tolerance).
- **Enforcement:** Comparing the final metadata dependency graph against a cold-start generation must show zero edge differences.
