---
name: gen-table-caption
description: Use when user needs to generate English table captions from Chinese descriptions for academic papers. Triggers on "生成表标题", "table caption", "表的标题", "Tab. caption", or when user has a table and needs its caption written in conference-standard English.
---

# 生成表的标题: English Table Caption from Chinese Description

## When to Use
- User has a table and a Chinese description, needs English caption
- Keywords: "生成表标题", "table caption", "表的标题", "Tab. caption"
- Target: conference-standard format (Title Case for noun phrases, Sentence case for full sentences)

## Instructions

If user hasn't provided description yet, ask: **"请粘贴对表格的中文描述"**

Apply the following prompt to the user's Chinese description:

---

**Role**: 经验丰富的学术编辑，擅长撰写精准、规范的论文表格标题。

**Task**: 将【中文描述】转化为符合顶级会议规范的【英文表标题】。

**Constraints**:

1. 格式规范:
   - 若翻译结果是名词性短语: 用 **Title Case**（所有实词首字母大写），末尾不加句号
   - 若翻译结果是完整句子: 用 **Sentence case**（仅第一个词首字母大写，专有名词除外），末尾必须加句号
2. 写作风格:
   - 常用句式: `Comparison with ...`, `Ablation study on ...`, `Results on ...`
   - 去 AI 味: 避免 `showcase`, `depict`；直接用 `show`, `compare`, `present`
3. 输出格式:
   - 只输出翻译后的英文标题文本
   - 不包含 "Table 1:" 前缀，只输出内容本身
   - 特殊字符转义（`%`, `_`, `&`）
   - 数学公式保留 `$` 符号

## Examples

| Chinese | English |
|---------|---------|
| 与SOTA方法在 WikiText-2 上的困惑度对比 | Comparison with SOTA Methods on WikiText-2 Perplexity |
| 关于混合比例 λ 的消融实验 | Ablation Study on Mixing Ratio $\lambda$ |
| 在 GSM8K 上的下游任务结果 | Results on GSM8K Downstream Task |
