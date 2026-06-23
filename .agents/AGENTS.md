# Deep Code Reader v2: Cognitive Transaction System Engineering Rules

> **Context:** This project has officially evolved from an "AI Coding Agent" into a **Deterministic Stateful Cognition Infrastructure**. Any AI Agent operating within this workspace must strictly adhere to the following philosophical and architectural rules.

## 1. The Separation of Prompt and Protocol (Skill vs Transaction)
- **Do not patch time-dimensional bugs with Prompt tweaks.** The AI Agent's Prompts (`SKILL.md`) are solely responsible for generating high-density cognition for a single snapshot in time. 
- All lifecycle management (invalidation, garbage collection, handling renames, avoiding ghost states) is the exclusive domain of the **deterministic code-based protocol** (Phases 0 and 5). 
- If the system leaks state over time, fix the protocol mechanics, NEVER try to make the Prompt "smarter" about state.

## 2. P0: False Negatives are Fatal Data Corruption
- **Over-invalidation** (wasting tokens to re-read unchanged modules due to shared dependencies) is an expected and acceptable economic cost (P2).
- **Under-invalidation / False Negative** (failing to invalidate a module when its dependency changes) is catastrophic.
- *Rule:* Always err on the side of absolute avalanche invalidation. A clean, fresh state is always prioritized over token savings.

## 3. Strict Replay Determinism & The Benchmark Taboo
- The metrics frozen in `REPLAY_METRICS_SCHEMA.md` (`false_negative_count`, `orphan_metadata_count`, `byte_instability_count`) have a strict 0-tolerance threshold.
- *Rule:* **Do not change the benchmark to hide corruption.** Do not introduce any "smart heuristics", "semantic diffing", or "confidence-based skipping" that might break absolute byte-for-byte replay determinism across time.

## 4. Time-Dimension Validation over Point-in-Time AI Quality
- A feature is not considered successful just because "the AI output looks good on a single file."
- A feature is only successful if it can survive **50+ consecutive commits** in a real-world repository replay without introducing a single `ghost state`, `orphan metadata`, or `stale routing` path.

## 5. Stabilization Era Directive
- We are currently in the **Stabilization Era (v1 Protocol Complete)**.
- Do not propose sweeping new intelligent features.
- Focus exclusively on: Evidence Accumulation, Cross-language pathology discovery, and strict ACID-health maintenance.
