# Deep Code Reader v2: Failure Severity Matrix

Not all failures in a Cognitive Transaction Engine are equal. To ensure the long-term stability of the system, every test scenario is classified by its severity.

The primary rule of this engine: **Over-invalidation is an economic inefficiency. Under-invalidation is a catastrophic data corruption.**

## P0: Catastrophic Protocol Corruption
These failures result in the system permanently diverging from reality without the user or the AI realizing it. A single P0 failure invalidates the entire protocol run.

- **`false_negative`**: A module should have been marked dirty (e.g., a shared dependency changed) but was skipped.
- **`stale_manifest`**: The global index or dependency graph points to deleted/renamed modules, using the "old world" to explain the "new world".
- **`cognition_poisoning`**: The AI confidently uses obsolete schemas or hallucinations derived from skipped invalidation steps.

## P1: Persistent State Degradation
These failures cause "ghosts" in the system. They don't immediately crash the system, but they accumulate entropy over time.

- **`ghost_state`**: Unresolved facts, old metadata fields, or stale gap arrays are merged or appended instead of being atomically replaced.
- **`stale_routing`**: The cross-module routing scenarios are out of sync with the physical layout, causing the Agent to get lost or loop infinitely.
- **`orphan_manifest`**: Deleted modules still have dangling metadata references.

## P2: Economic Inefficiency
These are safe failures. They cost tokens and time, but they preserve the absolute correctness of the AI's understanding. We optimize these only AFTER P0 and P1 are mathematically proven stable.

- **`over_invalidation`**: A module was marked dirty even though the change didn't functionally affect it (e.g., whitespace in a shared file).
- **`unnecessary_phase5`**: Regenerating the global index when no cross-module boundaries were altered.
- **`false_positive`**: Running verification on a file that didn't need it.
