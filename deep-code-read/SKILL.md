---
name: deep-code-read
description: Use when you want to deeply understand an unfamiliar codebase and generate reusable cognitive skills from it, by providing a local path or GitHub URL
---

# Deep Code Reader

Systematically read and understand a codebase, producing a set of verified cognitive skills that capture deep knowledge — module capabilities, design logic, data structures, state flow, and modification guides.

The core mechanism: a closed-book exam verification loop ensures generated skills are genuinely comprehensive, not shallow summaries.

## Usage

```
/deep-code-read <source> <output-dir>
```

- **source**: local path (e.g., `./path/to/repo`) or GitHub URL (e.g., `https://github.com/org/repo`)
- **output-dir**: where generated skills are written (e.g., `~/.claude/skills/`)

## Full Flow

You MUST follow these phases in order. Use TaskList to track progress across modules.

### Phase 1: Prepare

1. Determine the project name:
   - Local path → directory name
   - GitHub URL → repo name
2. If source is a URL:
   - Clone to `{output-dir}/{project-name}/`
   - If the directory already exists, skip cloning and use it
3. If source is a local path:
   - Verify the path exists and is a git repo
   - Use it directly (read-only — do NOT modify any files in the source repo)
4. Detect version:
   - Run `git tag --list` in the source repo
   - If tags exist, sort with semver-aware ordering (handle `v` prefix), recommend the latest
   - If no reasonable tags, recommend `main` or `master` branch
5. **PAUSE — present recommendation to user:**
   > "Detected the following tags/branches: [list]. I recommend tracking `{recommended}`. Confirm or specify a different target."
6. Checkout the confirmed ref

### Phase 2: Scan

1. Scan the source repo directory structure
2. Identify module boundaries using heuristics:
   - Top-level directories under `src/`, `lib/`, `pkg/`, `packages/`, or project root
   - Language-specific patterns: Python packages (`__init__.py`), Go packages, Node packages (`package.json`), etc.
   - Look for existing module documentation or manifest files
3. Analyze import/dependency relationships between modules
4. **PAUSE — present module list and dependency graph to user:**
   > "Found the following modules: [list with one-line descriptions]. Select which modules to deep-read (or 'all')."
5. Record the user's selection in TaskList — one task per selected module

### Phase 3: Deep Read (Agent A)

For each selected module, dispatch an Agent with the prompt template from `agent-a-prompt.md`.

**Agent dispatch parameters:**
- `prompt`: rendered `agent-a-prompt.md` with variables filled in
- `description`: "Deep read {module-name}"

**Variables to fill in the prompt:**
- `{source-dir}`: path to the source repo
- `{module-dir}`: path to the specific module within the source repo
- `{output-dir}`: the skill output directory
- `{project-name}`: extracted project name
- `{module-name}`: the module name
- `{ref}`: the tracked tag/branch

After Agent A completes, verify the skill files were written to `{output-dir}/{project-name}-dr-{module-name}/`. Update the module's task status.

### Phase 4: Verify (ABC Loop)

For each module that has generated skills, run the verification cycle:

**Step 1 — Agent B (question generation):**

Dispatch an Agent with `agent-b-prompt.md`, using `model: "haiku"`.

**Agent dispatch parameters:**
- `prompt`: rendered `agent-b-prompt.md`
- `model`: `"haiku"`
- `description`: "Generate questions for {module-name}"

**Variables:**
- `{source-dir}`, `{module-dir}`, `{module-name}`
- `{previous_questions}`: empty string for the first round

Agent B returns two sets:
- Verification questions with answer keys (JSON array)
- Recommended questions for user (JSON array)

Save the recommended questions (keep in context for Phase 6). Accumulate all verification questions asked so far across rounds.

**Step 2 — Agent C (closed-book answer):**

Dispatch an Agent with `agent-c-prompt.md`.

**Agent dispatch parameters:**
- `prompt`: rendered `agent-c-prompt.md` with verification questions embedded
- `description`: "Verify skills for {module-name}"

**Variables:**
- `{skill-dir}`: `{output-dir}/{project-name}-dr-{module-name}/`
- `{questions}`: the verification questions from Agent B (without answer keys)

Agent C returns answers to each question.

**Step 3 — Evaluate:**

For each question, check Agent C's answer against Agent B's `required_facts` list:
- An answer PASSES if it covers ALL required facts (exact match or semantic equivalent)
- An answer FAILS if it misses any required fact
- This is an objective check, not a subjective judgment

**Step 4 — Loop or proceed:**

- All questions pass → module verified, update task, move to next module
- Some questions fail → collect failed questions with: the question, B's answer key, C's failed answer
- Feed these back to Agent A: dispatch again with supplementary instructions to improve the skill based on the gaps
- Then re-run Agent B and Agent C, passing ALL previous questions (from all rounds) as `{previous_questions}` so B generates new questions instead of repeating old ones
- **Max 3 iterations** — after 3 rounds, show unresolved questions to the user for judgment

### Phase 5: Generate Global Index

After all modules are verified, generate `{output-dir}/{project-name}-dr/SKILL.md`:

```yaml
---
name: {project-name}-dr
description: Use when working with {project-name} codebase — provides comprehensive module knowledge, design logic, and modification guides (generated from {ref})
---
```

Content must include:
- Repo source (GitHub URL if applicable, or local path)
- Version: tag or commit hash
- Tracked branch
- Generation timestamp
- Each module's one-line purpose (from the module skills)
- Inter-module dependency relationships (from Phase 2 scan)
- Cross-module scenario entry guides: for common operations that span multiple modules, describe which modules are involved and in what order

To generate cross-module scenarios, read ALL the module skills and synthesize typical user workflows.

### Phase 6: User Acceptance

Present the recommended questions collected from Phase 4:

> "Skills generated and verified. Here are some questions you might want to test:
> [list recommended questions]
>
> Feel free to ask any question about {project-name}. I'll answer using ONLY the generated skills."

When answering user questions in this phase:
- Read ONLY the generated skill files in `{output-dir}/{project-name}-dr*/`
- Do NOT read source code
- If you cannot answer a question from the skills alone, say so honestly — this indicates a gap

Continue until the user is satisfied or decides to end the session.

## Key Rules

- **Never modify source code** — the source repo is read-only throughout
- **Agent isolation is critical** — each agent's prompt strictly defines what it can read
- **Skills must be self-sufficient** — the verification loop exists to ensure this
- **Progress via TaskList** — every module is a task, updated as it progresses through phases
- **Format via writing-skills** — Agent A follows `superpowers:writing-skills` formatting conventions (frontmatter, CSO description, directory structure) but does NOT run the full writing-skills TDD cycle
