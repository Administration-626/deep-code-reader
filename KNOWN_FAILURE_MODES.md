# Deep Code Reader v2: Known Failure Modes

This document records the institutional "failure memory" of the Deep Code Reader protocol. 
Mature engineering systems (databases, compilers, distributed systems) are stable because they institutionalize the pitfalls they have encountered. We record the symptoms and causes of "cognition corruption" here to prevent future agents or maintainers from repeating history.

## 1. Confidence Inflation (The "Fake 100%" Trap)
- **Symptom:** A module's `knowledge_confidence` and `verification_pass_rate` suddenly jump to 100%, silently erasing dozens of previously hard-fought `open_gaps`.
- **Cause:** A trivial local change (e.g., adding a single boolean field) triggers an incremental rerun. The verification loop only tests this tiny delta, easily scoring 100%. The global, historical complexity of the module is not re-verified, but the local score overwrites the global confidence.
- **Prevention:** Differentiate between `local_verification_confidence` (this run) and `historical_coverage_confidence` (long-term). Do not let a local 100% pass rate blind the system to underlying historical gaps.

## 2. Ghost Gaps (Zombie State)
- **Symptom:** Unresolved facts (`open_gaps`) from old versions of the codebase remain in the `.metadata.json` forever, even after the underlying code has been entirely rewritten or deleted.
- **Cause:** Using "append" or "merge" logic when updating verification state instead of strict "atomic replacement".
- **Prevention:** Always enforce **Replacement Semantics**. When a module is dirty, its entire verification state must be wiped and reconstructed from scratch.

## 3. Stale Routing & Topology Drift
- **Symptom:** The global index (`SKILL.md`) routes agents to the wrong module, or describes "Cross-Module Scenarios" that no longer match the reality of the codebase's architecture.
- **Cause:** Treating Phase 5 (Global Index Generation) as simple string concatenation, or skipping it entirely to "save tokens" when only a leaf module changed.
- **Prevention:** Phase 5 must be an active synthesis layer that regenerates the dependency graph and cross-module workflows by analyzing the latest merged `.metadata.json` and module `SKILL.md`s.

## 4. Cognition Cache Poisoning (Stale Skill)
- **Symptom:** The AI confidently answers architectural questions using obsolete schemas or deleted data structures, causing cascading hallucinations in downstream coding tasks.
- **Cause:** Missed invalidation (False Negative) during Phase 0 incremental detection. Usually happens when a shared contract/type is changed, but the protocol fails to propagate the `dirty` flag to the modules that import it.
- **Prevention:** Over-invalidation is always preferred over under-invalidation. `module_public_interface_hash` and dependency topologies must be strictly monitored to trigger avalanche invalidations when shared APIs change.
