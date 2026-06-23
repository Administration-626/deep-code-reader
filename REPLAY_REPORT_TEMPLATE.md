# Cognition Replay Report: [Target Repo Name]

**Date of Execution:** [YYYY-MM-DD]
**Engine Version:** [Protocol Version / Git Hash]
**Target Repository:** [URL or Path]
**Commit Range:** [Oldest Commit] -> [Newest Commit]
**Replay Count:** [N commits]

## 1. Execution Parameters
- `mode`: deterministic
- `llm`: disabled
- `metadata_replace_only`: true
- `phase5_always_rerun`: true

## 2. Failure Distribution (Risk Summary)
| Metric | Count | Acceptable? | Severity |
| :--- | :--- | :--- | :--- |
| **`false_negative_count`** | [Count] | ❌ NO (Must be 0) | P0 (Data Corruption) |
| **`orphan_metadata_count`** | [Count] | ❌ NO (Must be 0) | P1 (Ghost State) |
| **`byte_instability_count`** | [Count] | ❌ NO (Must be 0) | P1 (Nondeterminism) |
| **`over_invalidation_count`** | [Count] | ✅ YES | P2 (Economic Cost) |

## 3. Incident Logs
*(Log specific commits where an incident occurred. If none, write "None")*

### P0 Incidents (Catastrophic)
- **Commit `[hash]`:** [Description of false negative or silent corruption]

### P1 Incidents (State Degradation)
- **Commit `[hash]`:** [Description of ghost state, orphan manifest, or metadata drift]

### P2 Incidents (Economic Inefficiency)
- **Commit `[hash]`:** [Description of significant over-invalidation / avalanche events]

## 4. Key Protocol Health Events

### Avalanche Interceptions
*(Times when modifying a shared contract successfully invalidated large portions of the dependency graph, proving the False Negative Firewall works)*
- **Commit `[hash]`:** Modified `[shared_file]`. Cascaded invalidation to `[N]` dependent modules.

### Cognition Garbage Collection Events
*(Times when modules were deleted/renamed, and the system successfully purged their metadata)*
- **Commit `[hash]`:** Deleted `[directory]`. Purged `[module]` from manifest successfully.

## 5. Final Verdict
**Replay Determinism Status:** [PASS / FAIL]
*(Does the incrementally evolved metadata state at Commit N structurally match a cold-start generation at Commit N?)*

**Conclusion:**
[Brief summary of whether the protocol maintained ACID health across the replay time-dimension.]
