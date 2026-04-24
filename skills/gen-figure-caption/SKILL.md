---
name: gen-figure-caption
description: Use when user needs to generate English figure captions from Chinese descriptions for academic papers. Triggers on "生成图标题", "figure caption", "图的标题", "生成配图文字", or when user has a figure and needs its caption written in conference-standard English.
---

# 生成图的标题: English Figure Caption from Chinese Description

## When to Use
- User has a figure and a Chinese description, needs English caption
- Keywords: "生成图标题", "figure caption", "图的标题", "Fig. caption"
- Target: conference-standard format (Title Case for noun phrases, Sentence case for full sentences)

## Instructions

If user hasn't provided description yet, ask: **"请粘贴对图的中文描述"**

Apply the following prompt to the user's Chinese description:

---

**Role**: 经验丰富的学术编辑，擅长撰写精准、规范的论文插图标题。

**Task**: 将【中文描述】转化为符合顶级会议规范的【英文图标题】。

**Constraints**:

1. 格式规范:
   - 若翻译结果是名词性短语: 用 **Title Case**（所有实词首字母大写），末尾不加句号
   - 若翻译结果是完整句子: 用 **Sentence case**（仅第一个词首字母大写，专有名词除外），末尾必须加句号
2. 写作风格:
   - 极简原则: 去除 "The figure shows" / "This diagram illustrates" 等冗余开头，直接以 Architecture / Performance comparison / Visualization 开头
   - 去 AI 味: 避免复杂生僻词，保持平实准确
3. 输出格式:
   - 只输出翻译后的英文标题文本
   - 不包含 "Figure 1:" 前缀，只输出内容本身
   - 特殊字符转义（`%`, `_`, `&`）
   - 数学公式保留 `$` 符号

## Examples

| Chinese | English (Title Case) |
|---------|----------------------|
| 我们方法的整体架构 | Overall Architecture of Our Method |
| 在 WikiText-2 上的困惑度对比 | Perplexity Comparison on WikiText-2 |

| Chinese | English (Sentence case) |
|---------|-------------------------|
| 提升的压缩比使得精度显著下降 | Higher compression ratios lead to significant accuracy degradation. |
