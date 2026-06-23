# Deep Code Reader

[English](README.md)

**把任何代码库转化为经过验证的、可复用的 AI 认知型 skills —— 不是摘要，不是 RAG，而是真正的深度理解。**

---

## 问题

LLM 阅读代码时的默认行为是浏览和概括。让它"理解"一个仓库，你只会得到一份泛泛的概述，一旦问到具体问题就露馅。下次再问，又得从头搜索。

## 解决方案

Deep Code Reader 产出的是**经过验证的认知技能** —— 结构化的知识文档，AI 加载后就能像真正读过代码的人一样工作。

### 核心优势 (Why Deep Code Reader?)

- **日常查询时极致的 Token 节省**：虽然初始生成（ABC循环）会消耗一定的算力（建议利用夜间闲置配额），但在日常开发中，你不再需要每次提问都把庞大的代码库硬塞进上下文。AI 只需要读取极其精简的 `SKILL.md`（高浓度认知压缩），日常对话的 Token 消耗和等待延迟降低 90% 以上，实现“一次编译，无限次低成本查询”。
- **零依赖与跨生态兼容**：纯原生 Markdown 与 YAML 结构，不依赖任何第三方运行时插件，天生兼容 Codex、Gemini CLI、Claude Code 等主流智能体。
- **自动绘制架构图**：在梳理状态流转和核心控制逻辑时，强制自动生成 ASCII / Mermaid 可视化架构图，让晦涩的代码一目了然。
- **彻底杜绝“幻觉”**：首创的 ABC 闭卷考试验证循环（Agent C 必须在不看源码的情况下，仅凭文档答出 Agent B 提出的细节考题），确保生成的知识库 100% 详实可靠。

### 工作流程

```
扫描仓库 → 识别模块和依赖关系 → 你选择要读的模块
                          ↓
            逐模块：精读源码 → 生成 skill
                          ↓
                 闭卷考试验证（ABC 循环）
                          ↓
         Agent B（读代码，不看 skill）→ 出考题 + 标准答案
         Agent C（看 skill，不读代码）→ 闭卷答题
                          ↓
              通过？→ 下一模块 / 不通过？→ 改进 skill → 重考
                          ↓
              生成全局索引 + 与你进行问答验收
```

工具首先扫描仓库结构，梳理出模块划分和依赖关系，然后让你选择要深读哪些模块。每个模块都会经过一轮彻底的精读，随后进入**闭卷考试** —— 如果 Agent C 仅凭生成的 skill 文件就能回答细节问题、完全不接触源码，那说明这些 skill 确实够全面。如果答不出来，就继续完善直到能答出来。

## 让你的 Token 在你睡觉时学习

大多数订阅套餐包含约 5 小时的每日 AI 算力额度，夜间大量闲置。Deep Code Reader 把这些空闲额度变成积累的知识。

睡前启动，醒来就有一整套经过验证的技能可以加载。跑的仓库越多，你的 AI 懂的就越多 —— 利用夜间额度，零额外成本持续积累。

## 快速开始

### 安装

把 `deep-code-read` 目录添加到你的 agent 技能目录。建议使用跨助手通用的 `~/.agents/` 目录：

```bash
git clone https://github.com/Administration-626/deep-code-reader.git

# 推荐：通用跨助手路径（支持 Codex, Copilot CLI, Gemini 等）
cp -r deep-code-reader/deep-code-read ~/.agents/skills/

# 或者，如果你更喜欢特定助手的专属目录：
# cp -r deep-code-reader/deep-code-read ~/.gemini/skills/
# cp -r deep-code-reader/deep-code-read ~/.claude/skills/
```



### 使用

```bash
# 输出到跨平台 skills 目录（Codex、Gemini CLI、Copilot CLI 均可用）
/deep-code-read https://github.com/example/project ~/.agents/skills/

# 从本地仓库深读
/deep-code-read ./path/to/project ~/.agents/skills/
```

> **仅使用 Antigravity 的情况：** 如果你只用 Antigravity 且希望 skills 隔离在单个项目内，
> 可以改用工作区路径：`/your/project/.agents/skills/`

就这么简单。工具全自动运行，只在两个地方暂停等你确认：

1. **确认版本** — 要分析的 tag/分支
2. **选择模块** — 要深读的模块

### 卸载

由于技能完全是基于纯文本目录结构的，不涉及任何系统级进程或环境变量，卸载极其简单，只需删除对应的文件夹即可：

```bash
# 卸载 deep-code-read 核心技能
rm -rf ~/.agents/skills/deep-code-read/

# 卸载某个项目的知识库
rm -rf ~/.agents/skills/project-dr/
# 若已复制到 Claude Code，一并删除：
rm -rf ~/.claude/skills/project-dr/
```

## 产出物

```text
~/.agents/skills/               # 跨平台 skills 目录（Codex, Gemini CLI, Copilot CLI 均可读取）
  project-dr/                   # 唯一顶层条目 —— 索引技能
    SKILL.md                    # 全局架构与模块路由
    auth/                       # 模块技能（通过索引按需读取）
      SKILL.md
      reference.md              # 复杂模块可选
    routing/                    # 模块技能
      SKILL.md
    ...
```

> **Claude Code 用户：** Claude Code 只读取 `~/.claude/skills/`，不读取 `~/.agents/skills/`。生成完成后，运行：
> ```bash
> cp -r ~/.agents/skills/project-dr ~/.claude/skills/
> ```

### 每个模块技能覆盖 5 个维度：

| 维度 | 内容 |
|---|---|
| **职责与能力** | 模块做什么，公开 API，函数签名 |
| **核心设计逻辑** | 为什么这样设计，关键架构决策 |
| **数据结构** | 核心类型、接口及其关系 |
| **状态流转** | 数据如何流动，入口点，错误处理路径，并强制生成 ASCII/Mermaid 架构图 |
| **修改指南** | "要改 X 功能，需要动这些文件" |

### 全局索引技能包含：

- 仓库来源、版本号、跟踪分支
- 所有模块及一句话描述
- 模块间依赖关系图
- 跨模块场景指南

## ABC 验证循环

这就是 deep-code-reader 区别于"又一个代码摘要工具"的核心：

- **Agent A**（主模型）：读源码，生成技能文件
- **Agent B**（轻量模型）：读源码但不看技能，出考题并附带答案和必要事实点
- **Agent C**（主模型）：只看技能文件，闭卷答题

每轮迭代，B 都会追加**新题目**覆盖未测试的领域 —— 所以 A 不能只针对考过的题补课。每个模块最多 3 轮；未解决的差距会呈现给你判断。

## 生成完成后

工具进入**问答验收阶段**：

- 随意提问，AI 仅凭生成的技能回答
- 如果不知道问什么，Agent B 生成的推荐深度问题可供参考
- 如果仅凭技能答不出来，这就是一个诚实的差距信号

## 平台支持

Deep Code Reader 不绑定特定平台。只要 AI 编程 agent 支持以下特性即可使用：

- 技能/指令文件加载
- 子代理调度
- 文件系统读写

已在 Claude Code 上测试通过。理论上兼容 Codex、Gemini CLI 及其他支持 skill 的 agent。

## License

MIT
