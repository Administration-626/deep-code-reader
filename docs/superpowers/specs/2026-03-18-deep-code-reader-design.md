# Deep Code Reader — V1 Design Spec

## Overview

deep-code-reader is a Claude Code skill that helps people unfamiliar with a codebase (and their AI assistant) rapidly build deep understanding of it, producing a set of reusable cognitive skills.

The core insight: instead of the default LLM behavior of skimming and summarizing, this skill enforces deep reading through a "closed-book exam" verification mechanism — if an AI can answer detailed questions about code using ONLY the generated skills (without access to source code), then the skills are genuinely comprehensive.

## User Experience

### Input

```bash
# Local codebase
/deep-read ./path/to/openclaw ~/.claude/skills/

# Remote codebase
/deep-read https://github.com/example/openclaw ~/.claude/skills/
```

Two arguments:
1. **Code source**: local path or GitHub URL
2. **Output directory**: where skills (and cloned code if URL) are placed

### Output

All artifacts are placed flat in the output directory:

```
~/.claude/skills/
  openclaw/                  # Cloned source (URL case only)
  openclaw-dr/               # Global index skill
    SKILL.md
  openclaw-dr-hooks/         # Module skill
    SKILL.md
    reference.md             # Optional, for complex modules
  openclaw-dr-routing/
    SKILL.md
  ...
```

### Naming Convention

- Project name: extracted from directory name (local) or repo name (URL)
- Global index skill: `{project}-dr/`
- Module skills: `{project}-dr-{module}/`

## Full Flow

One command triggers the entire flow. Only two points pause for user confirmation.

### Phase 1: Prepare

- **URL input**: clone repo to `{output-dir}/{project-name}/`
- **Local input**: use the path directly
- Detect tags (prefer latest by semver-aware sorting; fall back to lexicographic for non-semver tags) and branches, recommend a target version
- **PAUSE**: wait for user to confirm target tag/branch

### Phase 2: Scan

- Scan directory structure, identify module boundaries and dependency relationships
- Display module list + dependency graph
- **PAUSE**: wait for user to select which modules to deep-read

### Phase 3: Deep Read (Agent A)

For each selected module, the primary model reads source code and generates skill files, written directly to the output directory.

**Required output constraints for each module skill:**

1. **Module purpose & capabilities**: what this module does, what capabilities it exposes externally (key function signatures + input/output descriptions)
2. **Core design logic**: why it's designed this way, the reasoning and key decisions behind processing core functionality (e.g., "why event-driven instead of direct calls")
3. **Core data structures**: key types, interface definitions
4. **State flow**: how data/state flows within the module
5. **Common modification scenarios → affected files**: if you want to change X, what files need to be touched

Three dimensions of coverage: **what it can do** (capabilities), **why it does it that way** (design logic), **how to change it** (modification guide).

Agent A MUST follow the formatting and structural conventions from `superpowers:writing-skills` (frontmatter format, CSO description rules, directory structure). Agent A does NOT run the full writing-skills TDD cycle — the ABC verification loop in Phase 4 serves as the quality gate instead.

Progress tracked via TaskList.

### Phase 4: Verify (ABC Loop)

For each module, run a closed-book verification cycle:

### Agent Orchestration

All agents are dispatched via the Claude Code `Agent` tool from the main SKILL.md orchestrator. Access isolation is enforced through prompt instructions — each agent's prompt explicitly specifies which files/directories it may read.

**Agent A** (primary model, dispatched via `Agent` tool):
- Prompt specifies: read source code in `{module-dir}`, write skill files to `{output-dir}/{project}-dr-{module}/`
- Follows `superpowers:writing-skills` formatting conventions

**Agent B** (Haiku model, dispatched via `Agent` tool with `model: "haiku"`):
- Prompt specifies: read ONLY source code in `{module-dir}`, do NOT read any `*-dr-*` directories
- Generates two separate sets of questions:
  - **Verification questions** (with answer keys): for Agent C's closed-book test, focused on specific details. Each question includes a brief expected answer derived from the source code.
  - **Recommended questions**: saved for user acceptance phase, focused on usage and modification perspectives. Kept in context window for Phase 6.
- The two sets must not overlap

**Agent C** (primary model, dispatched via `Agent` tool):
- Prompt specifies: read ONLY files in `{output-dir}/{project}-dr-{module}/`, do NOT read any source code
- Answers verification questions in closed-book mode
- Every answer must be specific (function names, file paths, processing flows) — no vague summaries allowed

### Answer Evaluation

The orchestrator compares Agent C's answers against Agent B's answer keys. An answer is considered failing if it contradicts the answer key, is substantially incomplete, or resorts to vague generalization where the answer key provides specifics.

### Loop Logic

1. A generates skill → B generates questions with answer keys → C answers → orchestrator evaluates
2. Questions C fails → orchestrator feeds back to A specifying what's missing (the question + B's answer key + C's failed answer)
3. A supplements skill → B regenerates questions → C re-answers → orchestrator evaluates
4. All verification questions pass → module complete, move to next
5. **Max 3 iterations** — if still failing after 3 rounds, show unresolved questions to user for judgment

### Phase 5: Generate Global Index

Generate `{project}-dr/SKILL.md` containing:
- Repo GitHub URL (if applicable)
- Version (tag or commit hash)
- Tracked branch
- Generation timestamp
- Each module's one-line purpose
- Inter-module dependency relationships
- Cross-module scenario entry guides

### Phase 6: User Acceptance

- User can freely ask questions; AI answers using ONLY the generated skills (no source code access)
- Recommended questions from Phase 4 (generated by Agent B) are presented if user doesn't know what to ask
- User judges answer quality and decides if any module needs re-reading

## Implementation Shape

### deep-code-reader Skill Directory Structure

```
deep-code-reader/
  SKILL.md                    # Main skill: defines /deep-read command and full flow
  agent-a-prompt.md           # Agent A (deep read + generate skill) prompt template
  agent-b-prompt.md           # Agent B (Haiku question generation) prompt template
  agent-c-prompt.md           # Agent C (closed-book answer) prompt template
```

### Dependencies

- **REQUIRED SUB-SKILL**: `superpowers:writing-skills` (invoked by Agent A when generating skills)

### SKILL.md Frontmatter

```yaml
---
name: deep-read
description: Use when you want to deeply understand an unfamiliar codebase and generate reusable cognitive skills from it
---
```

## Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Target user | People unfamiliar with a repo | Familiar users don't need generated skills |
| Scope control | Auto-discover + user selection | Full scan is too expensive; manual specification requires prior knowledge |
| Skill granularity | Per-module + global index | Natural boundary, automatable; global index covers cross-module understanding |
| Verification | ABC closed-book exam | Prevents AI laziness; skills must be good enough to replace reading code |
| Agent B model | Haiku | Weaker model catching gaps = those gaps are definitely important |
| State management | Context window + TaskList | v1 simplicity; no intermediate files needed |
| Skill format | superpowers convention via writing-skills | Ecosystem consistency |
| Naming | `{project}-dr-{module}` | Avoids collision, clear provenance |
| Storage | Flat in user-specified output directory | Simple, no hidden directories, immediate usability |
| Flow control | v1 one-shot full flow | Staged commands deferred to v2 when state persistence is designed |

## Future Considerations (Not in V1)

- Staged commands (`/deep-read scan`, `/deep-read read`, etc.) with state persistence
- Incremental re-reading when repo updates
- Cross-repo skill comparison
- Custom question templates for domain-specific codebases
