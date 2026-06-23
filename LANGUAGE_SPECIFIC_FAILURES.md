# Cognition Transaction Semantics: Language-Specific Failure Modes

**Status:** Draft
**Goal:** Document failure modes that are structurally tied to a specific language's syntax, build system, or dependency resolution model.

As we scale the Cognitive Transaction Engine across the polyglot ecosystem, we recognize that the protocol's invalidation rules must map cleanly to language-specific constructs. What causes an avalanche in TypeScript might be perfectly safe in Rust, and vice-versa.

## TypeScript / Node.js
- **Soft Module Boundaries:** Modules often don't have explicit visibility modifiers, making it easy to create "hidden" dependencies through relative paths.
- **`index.ts` Barrels:** Re-exporting huge numbers of symbols from single entry points causes massive `over_invalidation` avalanches if not correctly fingerprinted.
- **Dynamic Imports:** Runtime-resolved dependencies defeat static AST invalidation.

## Rust
- **Macro-induced Ambiguity:** Macros like `include_bytes!` or custom procedural macros generate implicit AST nodes that are invisible to pure text-based or basic tree-sitter invalidation.
- **Crate Graph Drift:** Modifying `Cargo.toml` without touching `src/` can change feature flags, altering the entire conditional compilation graph.
- **Public API Re-exports (`pub use`):** Extremely common in Rust. Changing a deeply nested private struct impacts the top-level crate interface if it is re-exported, requiring deep propagation rules to prevent false negatives.
