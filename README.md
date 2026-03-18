# Deep Code Reader

**Turn any codebase into verified, reusable AI skills — not summaries, not RAG, but genuine comprehension.**

**把任何代码库转化为经过验证的、可复用的 AI 认知技能 —— 不是摘要，不是 RAG，而是真正的深度理解。**

---

## The Problem / 问题

When LLMs read code, they default to skimming and summarizing. Ask them to "understand" a repo, and you'll get a high-level overview that falls apart the moment you ask a specific question. Next time you ask, they go back to searching from scratch.

LLM 阅读代码时的默认行为是浏览和概括。让它"理解"一个仓库，你只会得到一份泛泛的概述，一旦问到具体问题就露馅。下次再问，又得从头搜索。

## The Solution / 解决方案

Deep Code Reader produces **verified cognitive skills** — structured knowledge documents that an AI can load and immediately operate at the level of someone who has actually read the code.

Deep Code Reader 产出的是**经过验证的认知技能** —— 结构化的知识文档，AI 加载后就能像真正读过代码的人一样工作。

The key innovation: a **closed-book exam** verification loop.

核心创新：**闭卷考试**验证循环。

```
Agent A (reads code) → generates skill
Agent B (reads code, no skill) → generates exam questions + answer keys
Agent C (reads skill, no code) → takes the exam
                                     ↓
                          Pass? → Next module
                          Fail? → A improves skill → re-exam
```

If Agent C can answer detailed questions about the code using ONLY the generated skills — without touching source code — then the skills are genuinely comprehensive. If not, they get improved until they are.

如果 Agent C 仅凭生成的 skill 文件就能回答关于代码的细节问题 —— 完全不接触源码 —— 那说明这些 skill 确实够全面。如果答不出来，就继续完善直到能答出来。

## Quick Start / 快速开始

### Install / 安装

Add `deep-code-read` to your agent's skills directory:

把 `deep-code-read` 目录添加到你的 agent 技能目录：

```bash
# Example for Claude Code / Claude Code 示例
git clone https://github.com/CiferaTeam/deep-code-reader.git
cp -r deep-code-reader/deep-code-read ~/.claude/skills/
```

**Dependency / 依赖:** [superpowers](https://github.com/obra/superpowers) must be installed for skill formatting conventions.

### Use / 使用

```bash
# From a GitHub URL / 从 GitHub URL
/deep-code-read https://github.com/example/project ~/.claude/skills/

# From a local repo / 从本地仓库
/deep-code-read ./path/to/project ~/.claude/skills/
```

That's it. The tool handles everything automatically, pausing only twice for your input:

就这么简单。工具全自动运行，只在两个地方暂停等你确认：

1. **Confirm version** — which tag/branch to analyze / 确认要分析的版本（tag/分支）
2. **Select modules** — which parts to deep-read / 选择要深读的模块

## What You Get / 产出物

```
~/.claude/skills/
  project/                      # Cloned source (URL only) / 克隆的源码（仅 URL 模式）
  project-dr/                   # Global index skill / 全局索引技能
    SKILL.md
  project-dr-auth/              # Module skill / 模块技能
    SKILL.md
    reference.md                # Optional for complex modules / 复杂模块可选
  project-dr-routing/
    SKILL.md
  ...
```

### Each module skill covers 5 dimensions / 每个模块技能覆盖 5 个维度：

| Dimension / 维度 | What it captures / 内容 |
|---|---|
| **Purpose & Capabilities** / 职责与能力 | What the module does, its public API, function signatures | 模块做什么，公开 API，函数签名 |
| **Core Design Logic** / 核心设计逻辑 | WHY it's built this way, key architectural decisions | 为什么这样设计，关键架构决策 |
| **Data Structures** / 数据结构 | Key types, interfaces, and their relationships | 核心类型、接口及其关系 |
| **State Flow** / 状态流转 | How data flows, entry points, error paths | 数据如何流动，入口点，错误处理路径 |
| **Modification Guide** / 修改指南 | "To change X, modify these files" | "要改 X 功能，需要动这些文件" |

### The global index skill includes / 全局索引技能包含：

- Repo source, version, tracked branch / 仓库来源、版本号、跟踪分支
- All modules with one-line descriptions / 所有模块及一句话描述
- Inter-module dependency map / 模块间依赖关系图
- Cross-module scenario guides / 跨模块场景指南

## Let Your Tokens Learn While You Sleep / 让你的 Token 在你睡觉时学习

Most subscription plans include ~5 hours of daily AI compute. Much of it goes unused overnight. Deep Code Reader turns that idle quota into accumulated knowledge.

大多数订阅套餐包含约 5 小时的每日 AI 算力额度，夜间大量闲置。Deep Code Reader 把这些空闲额度变成积累的知识。

Fire it off before bed, wake up to a fully analyzed repo with verified skills ready to load. The more repos you run, the more your AI knows — compounding overnight, zero extra cost.

睡前启动，醒来就有一整套经过验证的技能可以加载。跑的仓库越多，你的 AI 懂的就越多 —— 利用夜间额度，零额外成本持续积累。

## The ABC Verification Loop / ABC 验证循环

This is what makes deep-code-reader different from "just another code summarizer":

这就是 deep-code-reader 区别于"又一个代码摘要工具"的核心：

- **Agent A** (primary model): reads source code, generates skill files / 读源码，生成技能文件
- **Agent B** (lightweight model): reads source code WITHOUT seeing skills, generates exam questions with answer keys and required facts / 读源码但不看技能，出考题并附带答案和必要事实点
- **Agent C** (primary model): reads ONLY skill files, takes the exam without source code access / 只看技能文件，闭卷答题

Each iteration, B adds **new questions** covering untested areas — so A can't just "teach to the test". Max 3 rounds per module; unresolved gaps are surfaced to you for judgment.

每轮迭代，B 都会追加**新题目**覆盖未测试的领域 —— 所以 A 不能只针对考过的题补课。每个模块最多 3 轮；未解决的差距会呈现给你判断。

## After Generation / 生成完成后

The tool enters a **Q&A acceptance phase**:

工具进入**问答验收阶段**：

- Ask anything about the codebase — AI answers using ONLY the generated skills / 随意提问，AI 仅凭生成的技能回答
- Recommended deep questions from Agent B are provided if you're not sure what to ask / 如果不知道问什么，Agent B 生成的推荐深度问题可供参考
- If the AI can't answer from skills alone, that's an honest signal of a gap / 如果仅凭技能答不出来，这就是一个诚实的差距信号

## Platform Support / 平台支持

Deep Code Reader is platform-agnostic. It works with any AI coding agent that supports:

Deep Code Reader 不绑定特定平台。只要 AI 编程 agent 支持以下特性即可使用：

- Skill/instruction file loading / 技能/指令文件加载
- Subagent dispatching / 子代理调度
- File system read/write / 文件系统读写

Tested with Claude Code. Should work with Codex, Gemini CLI, and other skill-compatible agents.

已在 Claude Code 上测试通过。理论上兼容 Codex、Gemini CLI 及其他支持 skill 的 agent。

## License

MIT
