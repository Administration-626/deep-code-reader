# Deep Code Reader v2: The Cognitive Transaction Engine

[中文版](README_CN.md)

**Turn any codebase into verified, long-lived AI skills. Not summaries, not RAG, but an ACID-compliant Cognitive Transaction Engine that never rots over time.**

---

## The Problem

When LLMs read code, they default to skimming and summarizing. Ask them to "understand" a repo, and you'll get a high-level overview that falls apart the moment you ask a specific question. 

Worse, as your codebase evolves, AI knowledge bases silently rot. A deleted module leaves a "ghost state." A changed shared interface silently poisons the dependent understanding. Most tools try to solve this with "smart background heuristics" or "semantic diffing," which inevitably leads to nondeterministic behavior and fatal false negatives where the AI confidently gives you wrong answers based on stale data.

## The Solution: Cognitive Transaction Semantics

Deep Code Reader v2 has evolved from an "AI Coding Agent" into a **Deterministic Stateful Cognition Infrastructure**. 

It produces **verified cognitive skills** (structured knowledge documents) that an AI can load and immediately operate at the level of a senior maintainer. But crucially, it maintains this state using strict transaction semantics structurally akin to an Incremental Compiler or a Database MVCC Engine.

### Core Protocol Invariants
- **False Negatives are Fatal:** Over-invalidation (wasting tokens) is an acceptable economic cost; under-invalidation (stale knowledge) is a catastrophic data corruption.
- **Explicit Transactions over Background Magic:** When code changes, you explicitly trigger an update. There are no silent background watchers. This guarantees auditable, deterministic state management.
- **Verification is Replaced, Never Merged:** To prevent ghost gaps and stale states, dirty module metadata is atomically regenerated.
- **Benchmark-Before-Feature:** The protocol's stability is validated through thousands of long-term Git commit replays on real repositories (TypeScript, Rust), ensuring zero "ghost states" and absolute metadata byte-stability.

### How it works: The Initial Cold Start
1. **Scan**: The tool maps modules and dependencies.
2. **Deep Read**: Agent A generates a skill document for each module.
3. **The ABC Loop (Verification)**: 
   - Agent B (reads source) generates difficult exam questions.
   - Agent C (reads ONLY the skill) takes the exam.
   - Failures force Agent A to improve the skill.
4. **Synthesis**: A global index and cross-module routing map is generated.

### How it works: Incremental Updates (Time-Dimension Engineering)
Code changes? The cognition state must evolve. 

1. **Phase 0 (Detect & Invalidate):** Strict diffing against `.metadata.json` identifies changed files and avalanches invalidation across the dependency graph. Ambiguous ownership causes conservative over-invalidation to prevent poisoning.
2. **Phase 4 (Re-verify):** Dirty modules are atomically wiped and re-sent through the ABC Loop.
3. **Phase 5 (Garbage Collection):** Orphan modules and deprecated routing paths are ruthlessly purged from the global manifest.

## Quick Start

### Install

Add `deep-code-read` to your agent's skills directory:

```bash
git clone https://github.com/Administration-626/deep-code-reader.git
cp -r deep-code-reader/deep-code-read ~/.agents/skills/
```

### Initializing a Project

```bash
/deep-code-read ./path/to/project ~/.agents/skills/
```

### Keeping State in Sync (Incremental Update)

**Crucial Rule:** The system does NOT run in the background. When your codebase undergoes significant changes (e.g., after completing a feature branch, pulling latest `main`), you must actively synchronize the cognition state:

```bash
/deep-code-incremental ./path/to/project ~/.agents/skills/
```
*Note: This command will safely calculate the diff, invalidate only the necessary modules, and update the global manifest, preserving your tokens while guaranteeing absolute ACID integrity.*

## Why Not Background Auto-Updates?

We explicitly rejected silent background watchers (like traditional IDE language servers). 

In a Cognitive Transaction System, state changes are expensive (both in tokens and cognitive entropy). If a background script constantly rewrites `.metadata.json` based on heuristic diffs while you are mid-refactoring with broken code, it introduces non-deterministic "ghost states" and cache poisoning. By making the update an explicit, deliberate action, we guarantee that the AI's understanding is always locked to a known, stable Git commit, providing 100% replay determinism.
