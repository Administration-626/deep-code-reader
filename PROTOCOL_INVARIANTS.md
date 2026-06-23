# Deep Code Reader v2: Protocol Invariants

**CRITICAL WARNING TO FUTURE MAINTAINERS AND AI AGENTS:**
This document defines the unbendable, structural invariants of the `deep-code-read` protocol. This protocol is designed as a **Stateful Cognition Infrastructure** (a "Cognitive Bazel" / "Cognitive Database"), NOT a simple prompt framework. 

Do **NOT** attempt to "optimize" or "simplify" the protocol by violating any of the invariants below. The primary failure mode of incremental cognition systems is **silent decay** (stale cognition silently accumulating), not execution cost.

---

## 1. Correctness Invariant: Stale Cognition Is Worse Than Over-Invalidation

This protocol intentionally over-reruns rather than risk preserving stale cognition. 
- **Forbidden Optimization:** Do NOT introduce heuristic "smart-skip" logic (e.g., "if only docs changed, skip verification"). 
- **Rationale:** Stale semantic residue is a silent failure that will eventually cause the AI's understanding to permanently diverge from the codebase truth.

## 2. Replacement Semantics: Verification State Is Replaced, Never Merged

When a dirty module is rerun during Phase 0, its resulting state (`verification_pass_rate`, `open_gaps`, `knowledge_confidence`, `verified_at`, `module_hash`) must be **atomically regenerated and replaced**.
- **Forbidden Optimization:** Never append, merge, or patch historical verification state (e.g., do not "merge" old gaps with new gaps).
- **Rationale:** Merging introduces "ghost gaps" (resolved issues that never disappear) and "stale summaries", irreversibly poisoning the metadata cache.

## 3. Orchestration Authority: Agents Analyze, Protocol Decides

The control flow, loop limits (`max_rounds`), stop conditions (`plateau`), and invalidation logic must remain strictly inside the external **Protocol layer**, NOT inside the Agent prompts.
- **Forbidden Optimization:** Do not allow LLM Agents to decide whether a module is "dirty enough" to require a rebuild, or whether they "feel" they have finished verification. 

## 4. Confidence Semantics: 100% Pass Rate != Global Understanding

The `knowledge_confidence` metric in an incremental run only represents **Local Verification Confidence** (i.e., "Did it pass the test for the current small diff?"). 
- **Warning:** Do not confuse this with **Historical Coverage Confidence**. A trivial typo fix can yield a 100% local pass rate, but that does not mean the agent understands the complex internals of the module. Beware of "Confidence Inflation."

## 5. Phase 5 Warning: Phase 5 Is Not String Concatenation

Phase 5 (Global Index Generation) acts as the **Cognition Synthesis Layer**. It must dynamically re-evaluate the cross-module scenarios and dependency topologies by analyzing the newly merged `.metadata.json` and the fresh/frozen `SKILL.md` files.
- **Forbidden Optimization:** Do not simply `cat` module files together.
- **Rationale:** Cross-module mechanics and architectural dependency reasoning will drift and become silently obsolete if Phase 5 is bypassed to save tokens.

## 6. Maintenance Rule: Benchmark-Before-Feature

Before introducing any new invalidation heuristic, optimization logic, or "Semantic Incremental" feature:
1. Add coverage to the Continuous Cognition Benchmark Matrix (e.g., testing `types.rs` shared contract avalanche).
2. Define regression expectations.
3. Measure false-negative risk (False Negative > False Positive).
4. Verify metadata byte-determinism.
**Do not merge optimization-first protocol changes without proving state integrity across time.**
