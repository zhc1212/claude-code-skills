---
name: shorten-latex
description: Use when user needs to slightly shorten an English LaTeX paragraph to fit page limits (paragraph-level, NOT model compression). Triggers on "缩写", "shorten", "tighten", "trim words", "精简这段", "削减字数", or requests to reduce length by 5-15 words while preserving all technical details. Do NOT trigger on "compress" alone (reserved for SVD model compression).
---

# 缩写: Shorten English LaTeX Passage

## When to Use
- User has LaTeX passage slightly over page limit / word budget
- Keywords: "缩写", "shorten", "tighten", "trim", "精简这段", "削减字数", "reduce word count"
- Need to trim 5-15 words while preserving all technical content

## When NOT to Use
- "compress" / "压缩模型" → that's `/compress` (SVD model compression), not this skill
- Paragraph needs rewriting / restructuring → use `polish-english-paper`

## Instructions

If user hasn't provided LaTeX yet, ask: **"请粘贴你的英文 LaTeX 代码"**

Apply the following prompt to the user's LaTeX input:

---

**Role**: 专注于简洁性的顶级学术编辑。特长是在不损失任何信息量的前提下，通过句法优化压缩文本长度。

**Task**: 将【英文 LaTeX 代码片段】进行微幅缩减。

**Constraints**:

1. 调整幅度:
   - 目标: 减少约 5-15 个单词
   - 严禁大删大改，必须保留所有核心信息、技术细节、实验参数
2. 缩减手段:
   - 句法压缩: 从句→短语；被动→主动（如果更简练）
   - 剔除冗余: 如 "in order to" → "to"
3. 视觉与风格:
   - 保持 LaTeX 源码纯净，不使用加粗/斜体/引号
   - 不用破折号（—）
   - 拒绝列表格式（Itemization），保持连贯段落
4. 输出格式:
   - **Part 1 [LaTeX]**: 缩减后的英文 LaTeX
     * 全英文
     * 特殊字符转义（`%`, `_`, `&`）
     * 保持数学公式原样（保留 `$`）
   - **Part 2 [Translation]**: 中文直译（核对核心信息是否完整）
   - **Part 3 [Modification Log]**: 中文说明调整点（例如：删除冗余词 "XXX"，合并 "YYY" 从句）

**Execution Protocol**:
输出前自查：
1. 信息完整性: 是否不小心删除了某个实验参数或限定条件？（如有，放回去）
2. 字数检查: 是否缩减过度？（目标只是微调）
