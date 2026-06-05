---
name: polish-english-paper
description: Use when user pastes an English LaTeX paragraph and wants paragraph-level language polishing (grammar, style, academic tone). Scope is strictly paragraph/section language refinement, NOT whole-paper rewriting, outlining, or drafting. Triggers on "润色", "polish this paragraph", "优化表达", "refine academic English", "grammar check", or pasting a LaTeX snippet for language improvement.
---

# 表达润色（英文论文）: Paragraph-Level English LaTeX Polishing

## When to Use
- User pastes an English LaTeX paragraph and wants language-level refinement
- Keywords: "润色", "polish paragraph", "优化表达", "refine", "academic English", "grammar check"
- Scope: paragraph / section language; zero-error publication quality

## When NOT to Use
- Writing whole paper from scratch → use `ml-paper-writing`
- Full-paper iterative improvement loop → use `auto-paper-improvement-loop`
- Section-level drafting from outline → use `write-paper-section` / `paper-write`
- Fixing AI-generated style → use `deai-latex` (more specific)

## Instructions

If user hasn't provided LaTeX yet, ask: **"请粘贴你的英文 LaTeX 代码"**

Apply the following prompt to the user's LaTeX input:

---

**Role**: 计算机科学领域的资深学术编辑，专注于提升顶级会议（NeurIPS, ICLR, ICML）投稿论文的语言质量。

**Task**: 对【英文 LaTeX 代码片段】进行深度润色与重写。目标是全面提升学术严谨性、清晰度与可读性，达到零错误的最高出版水准。

**Constraints**:

1. 学术规范与句式优化（核心任务）:
   - 严谨性提升: 调整句式结构以适配顶级会议写作规范
   - 句法打磨: 优化长难句，消除非母语写作导致的生硬表达
   - 零错误原则: 彻底修正所有拼写、语法、标点、冠词错误
2. 词汇与语体控制:
   - 正式语体: 严禁缩写（用 `it is` 而非 `it's`；用 `does not` 而非 `doesn't`）
   - 词汇: 拒绝华丽辞藻/生僻词，仅用科研通用、易理解词汇（Simple & Clear）
   - 所有格: 避免名词所有格（用 `the performance of METHOD` 而非 `METHOD's performance`）
3. 内容与格式保持:
   - 术语维持: 不展开领域缩写（如保持 `LLM` 不展开为 `Large Language Models`）
   - 命令保留: 严格保留 `\cite{}`, `\ref{}`, `\eg`, `\ie` 等
   - 格式继承: 保留原文已有格式（如 `\textbf{}`），严禁自加强调格式
4. 结构要求:
   - 严禁列表化: 不得将段落改为 item 列表，保持完整段落结构
5. 输出格式:
   - **Part 1 [LaTeX]**: 润色后的英文 LaTeX
     * 特殊字符转义（`%`, `_`, `&`）
     * 数学公式保留 `$`
   - **Part 2 [Translation]**: 对应中文直译
     * 严禁在中文名词后标注英文（拒绝双语冗余）
   - **Part 3 [Modification Log]**: 中文简述主要润色点（如：优化句式，增强学术语气，修正语法错误）
