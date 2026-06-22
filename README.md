# Deep Code Reader

[中文版](README_CN.md)

**Turn any codebase into verified, reusable AI skills — not summaries, not RAG, but genuine comprehension.**

---

## The Problem

When LLMs read code, they default to skimming and summarizing. Ask them to "understand" a repo, and you'll get a high-level overview that falls apart the moment you ask a specific question. Next time you ask, they go back to searching from scratch.

## The Solution

Deep Code Reader produces **verified cognitive skills** — structured knowledge documents that an AI can load and immediately operate at the level of someone who has actually read the code.

### Why Deep Code Reader?

- **Massive Token Savings at Query Time**: While the initial generation (the ABC loop) consumes a fair amount of compute (perfect for utilizing idle overnight quota), your day-to-day development becomes extremely cheap. Instead of dumping a massive 100k+ line codebase into context every time you ask a question, the AI only reads the highly compressed `SKILL.md` documents. "Compile once, query infinitely at 10% of the cost."
- **Zero-Dependency & Universal**: Outputs standard plain-text Markdown and YAML. No need to install third-party plugins. Natively cross-compatible with Codex, Gemini CLI, Claude Code, and other major AI agents.
- **Auto-Generated Visual Architecture**: Automatically forces the generation of ASCII/Mermaid diagrams for complex state machines and data flows, making logic instantly comprehensible.
- **Eliminates AI Hallucinations**: The pioneering ABC closed-book exam loop ensures the generated knowledge base is genuinely comprehensive, because Agent C must pass difficult questions from Agent B without looking at the source code.

### How it works

```
Scan repo → identify modules & dependencies → you pick what to read
                          ↓
         For each module: deep read → generate skill
                          ↓
              Closed-book exam verification (ABC loop)
                          ↓
         Agent B (reads code, no skill) → exam questions + answer keys
         Agent C (reads skill, no code) → takes the exam
                          ↓
              Pass? → Next module / Fail? → improve skill → re-exam
                          ↓
              Global index + Q&A acceptance with you
```

The tool first scans the repo structure to map out modules and their dependencies, then lets you choose which modules to deep-read. Each module goes through a thorough reading phase followed by a **closed-book exam** — if Agent C can answer detailed questions using ONLY the generated skills, without touching source code, the skills are genuinely comprehensive. If not, they get improved until they are.

## Let Your Tokens Learn While You Sleep

Most subscription plans include ~5 hours of daily AI compute. Much of it goes unused overnight. Deep Code Reader turns that idle quota into accumulated knowledge.

Fire it off before bed, wake up to a fully analyzed repo with verified skills ready to load. The more repos you run, the more your AI knows — compounding overnight, zero extra cost.

## Quick Start

### Install

Add `deep-code-read` to your agent's skills directory. We recommend the universal cross-agent `~/.agents/` directory:

```bash
git clone https://github.com/Administration-626/deep-code-reader.git

# Recommended: Universal cross-agent path (supports Codex, Copilot CLI, Gemini, etc.)
cp -r deep-code-reader/deep-code-read ~/.agents/skills/

# Or, if you prefer specific assistant directories:
# cp -r deep-code-reader/deep-code-read ~/.gemini/skills/
# cp -r deep-code-reader/deep-code-read ~/.claude/skills/
```



### Use

```bash
# From a GitHub URL (output to system's plugins directory)
# Note: We recommend outputting to ~/.agents/plugins/ for cross-agent compatibility
/deep-code-read https://github.com/example/project ~/.agents/plugins/

# From a local repo
/deep-code-read ./path/to/project ~/.agents/plugins/
```

That's it. The tool handles everything automatically, pausing only twice for your input:

1. **Confirm version** — which tag/branch to analyze
2. **Select modules** — which parts to deep-read

### Uninstall

Since skills are entirely based on plain-text directory structures and involve no system-level processes or background agents, uninstalling is as simple as deleting the folders:

```bash
# Uninstall the core deep-code-read skill
rm -rf ~/.agents/skills/deep-code-read/

# Uninstall any auto-generated project knowledge base plugin
rm -rf ~/.agents/plugins/project-dr/
```

## What You Get

```text
~/.agents/plugins/              # Universal plugin location
  project-dr/                   # Auto-generated knowledge base plugin
    plugin.json                 # Plugin config
    skills/
      index/                    # Global architecture & router
        SKILL.md
      auth/                     # Module cognitive skill
        SKILL.md
        reference.md            # Optional for complex modules
      routing/
        SKILL.md
  ...
```

### Each module skill covers 5 dimensions:

| Dimension | What it captures |
|---|---|
| **Purpose & Capabilities** | What the module does, its public API, function signatures |
| **Core Design Logic** | WHY it's built this way, key architectural decisions |
| **Data Structures** | Key types, interfaces, and their relationships |
| **State Flow** | How data flows, entry points, error paths, and ASCII/Mermaid diagrams |
| **Modification Guide** | "To change X, modify these files" |

### The global index skill includes:

- Repo source, version, tracked branch
- All modules with one-line descriptions
- Inter-module dependency map
- Cross-module scenario guides

## The ABC Verification Loop

This is what makes deep-code-reader different from "just another code summarizer":

- **Agent A** (primary model): reads source code, generates skill files
- **Agent B** (lightweight model): reads source code WITHOUT seeing skills, generates exam questions with answer keys and required facts
- **Agent C** (primary model): reads ONLY skill files, takes the exam without source code access

Each iteration, B adds **new questions** covering untested areas — so A can't just "teach to the test". Max 3 rounds per module; unresolved gaps are surfaced to you for judgment.

## After Generation

The tool enters a **Q&A acceptance phase**:

- Ask anything about the codebase — AI answers using ONLY the generated skills
- Recommended deep questions from Agent B are provided if you're not sure what to ask
- If the AI can't answer from skills alone, that's an honest signal of a gap

## Platform Support

Deep Code Reader is platform-agnostic. It works with any AI coding agent that supports:

- Skill/instruction file loading
- Subagent dispatching
- File system read/write

Tested with Claude Code. Should work with Codex, Gemini CLI, and other skill-compatible agents.

## License

MIT
