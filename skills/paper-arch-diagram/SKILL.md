---
name: paper-arch-diagram
description: Use when user wants to generate a paper architecture diagram prompt for image generation tools (nano-banana, DALL-E, Midjourney, Gemini Imagen). Triggers on "画架构图", "论文架构图", "architecture diagram", "method figure", or requests to visualize a paper's method pipeline.
---

# 论文架构图: Paper Architecture Diagram Prompt

## When to Use
- User has method description and wants an image-gen prompt for architecture figure
- Keywords: "画架构图", "架构图", "architecture diagram", "method figure", "框架图"
- Target tools: nano-banana (Gemini Imagen), DALL-E, Midjourney, Stable Diffusion

## Instructions

If user hasn't provided methodology yet, ask: **"请粘贴你的论文摘要 (Abstract) 和方法描述 (Method section)"**

Then offer two prompt versions (Chinese for Chinese-tuned models, English for nano-banana). Output BOTH versions so user can pick.

### English Version (recommended for nano-banana)

```
You are an expert Scientific Illustrator for top-tier AI conferences (NeurIPS/CVPR/ICML).
Your task is to generate a professional "Illustration" (main figure for the paper) based on a research paper abstract and methodology.

**Abstract:**
{abstract}

**Methodology:**
{methodology}

**Visual Style Requirements:**
1.  **Style:** Flat vector illustration, clean lines, academic aesthetic. Similar to figures in DeepMind or OpenAI papers.
2.  **Layout:** Organized flow (Left-to-Right, Top-to-Bottom, Circular and other shapes). Group related components logically.
3.  **Color Palette:** Professional pastel tones. White background.
4.  **Text Rendering:** You MUST include legible text labels for key modules or equations mentioned in the methodology (e.g., "Encoder", "Loss", "Transformer").
5.  **Negative Constraints:** NO photorealistic photos, NO messy sketches, NO unreadable text, NO 3D shading artifacts.

**Generation Instruction:**
Highlight the core novelty. Ensure the connection logic makes sense.
```

### Chinese Version (for Chinese-tuned image models)

```
# Role
你是世界顶尖的学术插画专家，专注于为 CVPR, NeurIPS, ICLR 绘制高质量、直观、美观的论文架构图。

# Task
先深刻理解【论文方法描述】的核心机制、模块组成、数据流向，然后设计并绘制专业学术架构图。

# Visual Constraints
1. 风格基调: 专业、干净、现代、极简主义；扁平化矢量插画风格；参考 DeepMind / OpenAI 论文；纯白背景、无纹理阴影。
2. 色彩体系: 淡色系/柔和色调；严禁鲜艳饱和或过度暗沉；用深浅变化区分模块类型。
3. 内容与布局: 理解方法论并转化为清晰模块和数据流箭头；可嵌入简洁矢量图标增强直观性。
4. 文字规范: 所有文字用英文；为关键模块/方程加清晰标签；禁止长句子/公式/描述性段落。
5. 禁止事项: 不用逼真照片感、杂乱草图、难辨文本、廉价 3D 阴影。

# Input Methodology
{论文摘要 + 方法部分描述}
```

## Post-Processing

告诉用户：
1. 两个版本都可尝试（nano-banana 对英文 prompt 训练更好）
2. 把 `{abstract}` 和 `{methodology}` 占位符替换成实际内容
3. 粘到目标图像生成工具（推荐 nano-banana / Gemini）
