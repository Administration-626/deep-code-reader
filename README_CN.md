# Deep Code Reader v2: 认知事务引擎

[English](README.md)

**把任何代码库转化为经过验证的、长期稳定的 AI 技能。它不是简单的代码摘要，也不是 RAG，而是一个具有 ACID 特性、永远不会随时间发生“静默腐烂”的认知事务引擎（Cognitive Transaction Engine）。**

---

## 我们面临的问题

现有的 LLM 工具在阅读代码时的默认行为是浏览和概括。让它"理解"一个仓库，你只会得到一份泛泛的概述，一旦问到具体细节就会产生幻觉。

更可怕的是，随着代码库的持续演进，AI 的知识库会发生**“静默腐烂（Silent Rot）”**。被删除的模块变成了“幽灵状态（Ghost State）”；被修改的共享接口会悄无声息地污染其他依赖它的模块的认知。大多数工具试图用“智能后台驻留（Smart Background Watchers）”或“语义对比”来解决这个问题，但这不可避免地引入了非确定性（Nondeterministic behavior），并最终导致最致命的**漏杀（False Negatives）**—— AI 会非常自信地基于过期的旧知识给你提供错误的答案。

## 解决方案：认知事务语义

Deep Code Reader v2 已经从一个普通的“AI 读代码工具”进化成了一个 **确定性的有状态认知基础设施（Deterministic Stateful Cognition Infrastructure）**。

它依然产出**经过验证的认知技能**，但在状态维护上，它采用了类似于“增量编译器（Incremental Compiler）”或“数据库引擎（Database Engine）”的严格事务语义。

### 核心协议不变量
- **漏杀（False Negative）是致命灾难**：过度计算（浪费 Token）是可以接受的经济成本；但漏更新依赖节点（认知过期）则是绝对不可容忍的结构性数据损坏（P0 级灾难）。
- **显式触发，拒绝后台魔法**：当代码发生变更时，**必须由你显式地触发认知同步事务**。系统内没有任何在后台悄悄修改 `.metadata.json` 的监听器，以此保证认知状态的绝对可审计性与确定性。
- **只做全量替换，绝不合并**：为了彻底消灭幽灵节点和过期缺口，脏模块的元数据永远只会被原子级重建，绝不使用 Append 或 Merge 操作。
- **评测先行（Benchmark-Before-Feature）**：该协议的稳定性已经通过在真实开源仓库（TypeScript、Rust）上连续几十次的 Git Commit 回放压测，确保了零幽灵状态残留和绝对的字节级确定性。

### 工作流程一：初始冷启动（Cold Start）
1. **扫描与拓扑提取**：工具扫描并构建整个仓库的模块与依赖关系图。
2. **源码精读**：Agent A 精读代码并生成知识库（Skill）。
3. **闭卷考试验证（ABC 循环）**：
   - Agent B（看源码）提出高难度考题。
   - Agent C（只看知识库，不看源码）进行闭卷答题。
   - 答错则强迫 Agent A 回炉重造，补充缺失的认知。
4. **合成（Synthesis）**：生成跨模块的全局路由树。

### 工作流程二：增量认知同步事务（Incremental Updates）
代码变了？AI 的认知状态也必须同步进化。

1. **Phase 0 (检测与雪崩标记)**：严格对比当前文件系统与 `.metadata.json`。只要检测到共享层或模糊依赖发生变动，系统会立刻触发防卫性的雪崩标记，将大量模块标为脏数据，宁可错杀绝不漏过。
2. **Phase 4 (验证与重塑)**：被标记的脏模块会被原子化抹除，重新打入 ABC 循环进行知识重塑。
3. **Phase 5 (认知垃圾回收)**：孤儿模块和作废的路由路径会被无情地从全局清单中彻底清除。

## 快速开始

### 安装

将 `deep-code-read` 添加到你的跨平台 agent 技能目录：

```bash
git clone https://github.com/Administration-626/deep-code-reader.git
cp -r deep-code-reader/deep-code-read ~/.agents/skills/
```

### 首次初始化一个项目

```bash
/deep-code-read ./path/to/project ~/.agents/skills/
```

### 保持状态同步（显式增量事务）

**极其关键的铁律：** 本系统**不在后台自动运行**。当你完成了重大的代码重构，或从主干拉取了大量更新后，你必须像执行数据库 Commit 一样，主动触发认知同步：

```bash
/deep-code-incremental ./path/to/project ~/.agents/skills/
```
*注：该指令会严格执行 Diff 并安全地在依赖树上传导失效（Invalidation），最终刷新全局认知元数据。它能在保证 ACID 级别认知健康度的前提下，为你最大程度地节省 Token。*

## 为什么不采用后台自动同步？

我们刻意封杀了类似于传统 IDE Language Server 那样的后台自动更新机制。

在一个“认知事务系统”里，每一次状态变更都极其昂贵（无论是 Token 成本还是系统熵增）。如果允许一个后台脚本在你重构写了一半、代码还处在破碎状态时，就自作聪明地修改 `.metadata.json`，它会轻易引入非确定性的幽灵状态和缓存投毒（Cache Poisoning）。

我们将状态更新设计成一个**显式发起的、确定性的事务动作**，从而保证 AI 的认知永远死死锁定在某一个稳定的 Git Commit 上。这才是真正经得起时间考验的工程学。
