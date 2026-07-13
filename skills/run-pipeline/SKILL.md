---
name: run-pipeline
description: "Run the proving pipeline on a Lean theorem (Putnam, IMO, QIT, etc). Use when user says 'run pipeline', 'prove', 'run-pipeline', 'run-qit', names a problem (A1-A6, B1-B6, P1-P6, traceDistance, fuchs), or specifies a .lean file."
---

# Run Pipeline

## Pipeline Flow

```
theorem.lean (theorem statement — sorry 由 Stage 1 / archon 自动生成)
  │
  ▼ cleanup_prior_injection (清理上次残留)
  │
  ├─ Stage 0 (可选, 需显式启用): Rethlas / LLM → 非形式化证明 blueprint
  │    ┌─ 输入: 自然语言题目 (从 /-! ... -/ docstring 自动提取)
  │    │   ⚠ Rethlas 是非形式化推理 agent, 期望 NL 数学问题, 不是 Lean 代码
  │    │   例: "Consider a 2025×2025 grid..." 而不是 "import Mathlib..."
  │    │
  │    ├─ Rethlas 输出: blueprint_verified.md (verified markdown proof)
  │    │   包含: 证明策略、关键引理、子目标分解、arXiv 引用
  │    │
  │    └─ 注入 (三层, 不是 blind dump):
  │         references/informal_proof.md ← 完整 blueprint (无截断, Plan Agent 直接读)
  │         references/summary.md ← 摘要 (≤3000 chars, reference-retriever 索引)
  │         .archon/USER_HINTS.md ← 精华摘要 (≤1500 chars):
  │           仅 lemma inventory + proof outline + critical claims
  │           不包含完整证明文本 (避免 over-anchor prover)
  │
  ├─ Stage 1: none(默认) / archon-dag / legacy-blueprint
  │    → [archon-dag] .tex 带 \lean{}/\uses{} + dag.json
  │    → [legacy-blueprint] sorry_using scaffold (消融用)
  │    → [none] 跳过, archon loop 自己 bootstrap
  │
  ├─ Stage 2: archon loop (N iterations)
  │    内部 phases (archon 控制, pipeline 不可观测):
  │      Plan → Validate → Prover → sync_leanok → Doctor → Review → Finalize
  │    ┌─ 有 blueprint (archon-dag / competition):
  │    │    compute_gaps() 每轮从 .tex+.lean 重算 DAG
  │    │    plan agent 读 frontier → 选 objective files
  │    └─ 无 blueprint (none / quick, 默认):
  │         DAG/frontier 休眠 (无 .tex → _blueprint_frontier_block 返回空)
  │         plan agent 直接按 PROGRESS.md objective 证明
  │    critics (需在 .archon/config.json 启用,archon init 默认关):
  │      progress-critic, strategy-critic, blueprint-reviewer
  │
  ├─ P0 Sealed Verdict (0 sorry 时触发, 4-gate)
  │    Gate 1: statement identity (kernel defeq, 自动解析 namespace FQN)
  │    Gate 2: compile + sorry-free (lake env lean)
  │    Gate 3: axiom audit (仅 propext/choice/Quot.sound)
  │    Gate 4: kernel recheck (lean4checker/leanchecker 独立验证)
  │
  └─ dependency_audit (非阻塞警告)
       refs ⊆ declared \uses{}

  → result.status: SOLVED / VERDICT_FAILED / PENDING
  → result.verdict: {gates: {statement_identity, compile_no_sorry, axiom_allowlist, kernel_recheck}}
```

### Rethlas vs Archon 职责边界

| | Rethlas (Stage 0) | Archon (Stage 2) |
|---|---|---|
| **输入** | 自然语言数学题目 | .lean 文件 (带 sorry) |
| **输出** | verified markdown proof blueprint | compiled .lean (0 sorry) |
| **语言** | 数学散文 (LaTeX/prose) | Lean 4 tactics |
| **角色** | 非形式化推理 + 文献检索 | 形式化证明 |
| **关系** | 产生 hints 给 Archon (不是替代) | 消费 hints, 独立证明 |

## Step 0: Preflight

```bash
REPO_ROOT=$(cd "$(git rev-parse --show-toplevel)" && pwd)
# PY, LEAN_PROJECT, ARCHON_PROJECT are defined in CLAUDE.md Development Environment.
# LEAN_PROJECT must be a Lean project dir with lakefile.toml + .lake/ cache.
# For QIT problems: the project must have `require QIT` in lakefile.toml.
```

### Workspace Isolation (自动, 无需手动 cleanup)

`run_pipeline()` 默认启用 `isolate_workspace=True`：为每个定理创建隔离工作目录。
Archon 只看到目标 .lean 文件，不会被其他题目分心。

**隔离目录结构**:
```
results/<theorem>/<timestamp>/_workspace/
├── .lake → (symlink to shared 8GB Mathlib cache)
├── lakefile.toml, lean-toolchain, lake-manifest.json  (copied)
├── <theorem_dir>/<theorem>.lean                        (唯一的目标文件)
├── Leanproblems/, .claude/                             (copied)
├── .mcp.json                                           (qit-search MCP server config)
│   └── qit-search: command + env (QIT_PREMISE_INDEX, QIT_DENSE_INDEX, QIT_EMBED_MODEL, QIT_EMBED_DEVICE)
└── .archon/  (fresh via archon init + post-init config seed)
```

**QIT Search MCP**：workspace 自动注入 `qit-search` MCP server。如果配置了 `qit_dense_index_path`，MCP server 启动时加载 Qwen3-Embedding-8B（~10s, ~16GB VRAM），查询时自动 embed query → hybrid search。未配置则纯 lexical。

**解决的问题**:
- ~~dag.json 混入其他题~~ → 隔离目录没有其他 .tex/.lean
- ~~旧 logs 锚定 agent~~ → fresh .archon/, 无旧 logs
- ~~PROGRESS.md 被改写~~ → pipeline 每次覆写
- ~~P6 文件被之前 run 修改~~ → 隔离目录里是原题 copy
- ~~Plan agent 给其他题 dispatch~~ → 目录里只有目标题

**手动 pre-flight cleanup 不再需要。** 如需禁用隔离（调试用）：`isolate_workspace=False`。

### Known Issues & Mitigations

| Issue | Symptom | Mitigation |
|-------|---------|------------|
| **Rethlas 收到 Lean 代码** | Codex 写 Lean tactics 而不是 markdown proof | `extract_nl_problem()` 自动提取 `/-! ... -/` docstring |
| **Blueprint blind dump** | USER_HINTS 被 12KB proof 塞满, over-anchor prover | 完整版 → `references/informal_proof.md` (Plan Agent 读), 精华 → `USER_HINTS.md` ≤1500 chars |
| **Rethlas verify 循环过长** | 33+ min 还在修 staircase lemma | 设 timeout, 用当前 blueprint.md 即使 verification 未通过 |

**Check availability** (report before asking questions):
- `archon --version` → Archon CLI
- `codex --version` → Codex CLI (ChatGPT login)
- `claude --version` → Claude CLI
- `curl -sf http://127.0.0.1:8091/health` → Rethlas verification service (**optional** — inline fallback exists)
- `env | grep -E "OPENAI|DEEPSEEK"` → API keys
- `ls /tmp/qit-dense-qwen3.npy` → QIT dense vector cache (**optional** — lexical fallback if missing)
- `ls ~/.cache/modelscope/Qwen/Qwen3-Embedding-8B/` → Qwen3-Embedding-8B model (**optional** — needed for dense search)

**QIT Dense Search setup** (one-time per QIT-Dev revision, skip if `.npy` exists):
```bash
# Build premise index (QIT_DEV_ROOT = path to Lean-QIT-Dev checkout)
$PY -m lean_qit_agent.cli qit-index build --qit-root $QIT_DEV_ROOT --out /tmp/qit-premises.jsonl
# Embed declarations + build dense cache (~74s on A800)
# MODEL_PATH = HuggingFace model ID or local path (e.g. ~/.cache/modelscope/Qwen/Qwen3-Embedding-8B)
CUDA_VISIBLE_DEVICES=1 $PY -m lean_qit_agent.cli qit-index embed-build \
  --index /tmp/qit-premises.jsonl --out /tmp/qit-dense-qwen3.npy \
  --model $MODEL_PATH --device cuda
```

**If Stage 0 = rethlas**, verification service is **optional**:
- HTTP endpoint (`http://127.0.0.1:8091/verify`) is tried first
- If unavailable, pipeline **automatically falls back to inline CLI verification** (`codex exec` / `claude -p`) using the full AGENTS.md workflow including reference-checking
- Inline fallback inherits env (proxy, API keys, model, effort) from the pipeline process

To start the HTTP service (optional, for faster verification):
```bash
cd $REPO_ROOT/vendor/rethlas/agents/verification
nohup $PY -m uvicorn api.server:app --host 127.0.0.1 --port 8091 > /tmp/rethlas_verifier.log 2>&1 &
```
If `/verify` returns HTTP 500, the inline fallback will handle it automatically. To debug the HTTP service:
- Check `/tmp/rethlas_verifier.log` for errors
- Codex CLI connection failure → run `codex exec "echo test"` to verify
- Missing `jsonschema` → `$PY -m pip install jsonschema`

## Step 1: Collect Parameters

Parse shorthand from user args first, then **always ask** for missing parameters
(one AskUserQuestion with up to 4 questions).

### Shorthand parsing

Shorthand 只解析 **theorem, backend, effort, profile**。Stage 0 和 Stage 1
**不从 shorthand 解析**——必须通过 Round 2 AskUserQuestion 让用户选择。

| User says | Theorem | Backend | Model ID | Effort | Profile |
|-----------|---------|---------|----------|--------|---------|
| `B5 gpt-5.5 high competition` | putnam_2025_b5 | codex | gpt-5.5 | high | competition |
| `A2 opus max` | putnam_2025_a2 | claude_code | claude-opus-4-8 | max | — |
| `B1 sonnet quick` | putnam_2025_b1 | claude_code | claude-sonnet-4-6 | — | quick |
| `IMO2025 P2 codex` | imo_2025_p2 | codex | gpt-5.5 | — | — |
| `traceDistance_comm codex quick` | QIT problem | codex | gpt-5.5 | — | quick |

Shorthand aliases:
- `sonnet` → claude_code, claude-sonnet-4-6
- `opus` → claude_code, claude-opus-4-8
- `codex`, `gpt-5.5` → codex, gpt-5.5
- `deepseek` → api, deepseek-v4-flash

Problem shorthand:
- Putnam: A1-A6, B1-B6 → `$LEAN_PROJECT/Putnam2025/putnam_2025_<lower>.lean`
- IMO: P1-P6 → `$LEAN_PROJECT/IMO2025/imo_2025_p<N>.lean`
- QIT: name or partial → `$REPO_ROOT/problems/QIT/<name>.lean`
  - `traceDistance_comm`, `fuchs_van_de_graaf_lower`, etc.
  - QIT problems auto-set `require_qit=True` in PipelineOptions

### Ask missing parameters

Use **TWO rounds** of AskUserQuestion:

**Round 1** — core params (skip questions already parsed from shorthand):

| Question | Options |
|----------|---------|
| **Theorem** (skip if parsed) | Problem list / custom .lean path |
| **Backend + Model** (skip if parsed) | Codex+GPT-5.5 (Recommended), Claude+Opus 4.8, Claude+Sonnet 4.6, API+DeepSeek |
| **Iterations** (skip if parsed) | quick=10 iter, balanced=16 iter, competition=30 iter, custom |
| **Effort** (skip if parsed or backend=API) | high (Recommended), max, medium |

**Round 2** — **ALWAYS ask Stage 0 and Stage 1**, even if shorthand provided other params.
These are the two most impactful choices and the user must decide each run:

| Question | Options |
|----------|---------|
| **Stage 0 (非形式化推理)** | rethlas (Recommended — Rethlas 生成 informal proof blueprint), llm (单次 LLM sketch), none (跳过) |
| **Stage 1 (DAG 生成)** | archon-dag (Recommended — leandag blueprint 指导 prover), none (Archon 自己 bootstrap) |

⚠ **Stage 0 和 Stage 1 永远让用户选择，不从 shorthand 解析，不由 profile 自动决定。**
Profile（quick/balanced/competition）只控制 **Archon 迭代次数**。

💡 推荐组合: Stage 0 = rethlas + Stage 1 = archon-dag（informal proof → blueprint → 结构化 DAG → prover 有方向感）。
但两者独立有效，用户可以任意搭配。

### Confirmation

```
Pipeline config for <theorem_name>:
  Backend:       <backend> (<model_id>, effort=<effort>)
  Iterations:    <10 / 16 / 30 / custom>
  Stage 0:       <rethlas / llm / none>
  Stage 1:       <archon-dag / none / legacy-blueprint>
  Archon iter:   <N>
  Rethlas:       <verification service UP/DOWN> (only if Stage 0 = rethlas)
  ──────────────────────────────
  Time est:      Rethlas ~5-15min + Archon ~2-3min/iter
```

AskUserQuestion: **Proceed** / **Change config** / **Cancel**.

## Step 2: Execute Pipeline

**Run via `run_pipeline()` API** (one call, stages are automatic):

```python
import json, sys, time, logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)-7s %(name)s: %(message)s")
sys.path.insert(0, "<REPO_ROOT>")

from lean_qit_agent.blueprint.pipeline import run_pipeline
from lean_qit_agent.blueprint.pipeline_options import PipelineOptions

LEAN_PROJECT = Path("<LEAN_PROJECT>")  # from CLAUDE.md Development Environment

TIMESTAMP = time.strftime("%Y%m%d_%H%M%S")
RESULT_DIR = Path("<REPO_ROOT>/results/<theorem_name>") / TIMESTAMP

theorem_source = Path("<theorem_file>").read_text()

opts = PipelineOptions(
    stage0_provider="<none|llm|rethlas>",
    stage1="<none|archon-dag|legacy-blueprint>",
    archon_max_iterations=<N>,
    archon_model="<model_id>",
    archon_max_parallel=4,
    archon_dag_max_iterations=6,       # varies by profile: quick=4, balanced=6, competition=10
    rethlas_backend="auto",            # codex/claude/api/auto
    rethlas_effort="xhigh",            # reasoning effort for Rethlas
    rethlas_verify_url="http://127.0.0.1:8091",
    # QIT workspace (set for QIT problems, skip for Putnam/IMO)
    require_qit=True,                          # pin workspace to QIT + mathlib v4.30.0
    qit_index_path="<qit-index.jsonl>",        # QIT premise index for lexical search (None to skip)
    # QIT dense embedding search (optional — lexical fallback if omitted or deps missing)
    qit_dense_index_path="<dense_cache.npy>",  # .npy from embed-build (None to skip)
    qit_embed_model="Qwen/Qwen3-Embedding-8B", # HF model ID or local path
    qit_embed_device="cuda",                    # GPU for query embedding
)

t0 = time.time()
result = run_pipeline(
    theorem_source,
    LEAN_PROJECT,
    RESULT_DIR,
    opts=opts,
    backend="<codex|claude_code|api>",  # resolved from "auto" internally
    model="<model_id>",                 # for Stage 0 + legacy Stage 1
    effort="<medium|high|max>",
)
elapsed = time.time() - t0

print(f"STATUS:  {result.status}")
print(f"SUCCESS: {result.success}")
print(f"VERDICT: {json.dumps(result.verdict, indent=2, default=str)}")
print(f"ELAPSED: {elapsed:.0f}s")
print(f"ERRORS:  {result.errors}")
print(f"STAGES:  {result.stage_times}")

(RESULT_DIR / "result.json").write_text(json.dumps({
    "status": result.status,
    "success": result.success,
    "verdict": result.verdict,
    "elapsed": elapsed,
    "errors": result.errors,
    "stage_times": result.stage_times,
    "proved_len": len(result.proved_lean),
}, indent=2, default=str))
```

### Alternative: `run-qit` CLI (batch benchmark)

For running multiple QIT problems with pass@k scoring:

```bash
$PY -m lean_qit_agent.cli run-qit \
  --bench-jsonl <qit-bench.jsonl> \
  --lean-project-dir $LEAN_PROJECT \
  --out results/qit-bench/ \
  --k 1 \
  --backend codex \
  --model gpt-5.5 \
  --profile quick \
  --stage0-provider none \
  --stage1 none \
  --require-qit \
  --qit-index <qit-index.jsonl> \
  --qit-dense-index <dense.npy> \
  --qit-embed-model Qwen/Qwen3-Embedding-8B
```

This runs each problem through the pipeline with P0 verdict and writes a scorecard.

### What happens inside `run_pipeline()`

1. **Workspace isolation** (default on): creates isolated workspace with only target .lean + symlinked .lake
2. **Cleanup**: removes prior-run `references/summary.md` + `USER_HINTS.md` sentinel block
3. **Stage 0** (if `stage0_provider != "none"`):
   - `rethlas`: codex exec → Rethlas Generation Agent → `blueprint_verified.md` → inject
   - `llm`: single LLM call → NL sketch → inject
   - Injection targets: `references/informal_proof.md` (full) + `references/summary.md` (≤3000 chars) + `.archon/USER_HINTS.md` persistent section (≤1500 chars)
4. **Stage 1** (if `stage1 != "none"`):
   - `archon-dag`: `archon dag -M <model> -m <max_iter>` → leandag-native `.tex`
   - `legacy-blueprint`: LLM → sorry_using scaffold + DAG validate (no Lean compilation)
5. **Stage 2**: `archon loop` with configured harness/model/effort/critics
   - Pipeline monitors sorry count every 30s; kills archon early on 0 sorry
   - Runs inside isolated workspace (only target .lean visible)
6. **P0 Verdict** (if 0 sorry, 4-gate):
   - Gate 1: `statement_identity` — kernel defeq check (auto-resolves namespace FQN)
   - Gate 2: `compile_no_sorry` — `lean_compile_source`
   - Gate 3: `axiom_allowlist` — `#print axioms`, whitelist check
   - Gate 4: `kernel_recheck` — independent lean4checker/leanchecker verification
   - All 4 pass → `status = "SOLVED"`; any fail → `status = "VERDICT_FAILED"`
7. **dependency_audit** (after verdict, non-blocking):
   - Reads proved file + DAG → checks refs ⊆ declared parents
   - Warnings only, does not block SOLVED

### Monitoring

`run_pipeline()` is a single blocking Python call that runs all stages sequentially.
Run the entire pipeline script in the background and monitor its log output.

```bash
# Write the pipeline script (from Step 2 template) to $RESULT_DIR/run.py, then:
nohup $PY -u $RESULT_DIR/run.py > $RESULT_DIR/pipeline.log 2>&1 &

# Monitor — filter key events across all stages
tail -f $RESULT_DIR/pipeline.log | \
  grep -E --line-buffered "Stage|Rethlas|blueprint|archon|iteration|sorry|STUCK|CHURNING|verdict|SOLVED|FAILED|Error|elapsed"
```

**关键日志信号**:
- `Stage 0` — Rethlas input/output, blueprint chars, verification pass/fail
- `Stage 1` — DAG node count, archon dag result
- `Stage 2` — iteration number, sorry count, `STUCK`/`CHURNING` (需干预), `0 sorry` (early kill)
- `P0` — gate results (statement/compile/axioms), `SOLVED` or `VERDICT_FAILED`
- `dependency_audit` — conforms or warnings

### Checkpoints (interactive mode)

After each stage completes, show summary + AskUserQuestion:

**Stage 0**: Rethlas blueprint length + key ideas extracted → Continue / Retry / Skip
**Stage 1**: DAG node count + dependency graph → Continue / Retry / Abort
**Stage 2**: Sorry count + iterations used + critics verdicts → Continue to P0 / Retry / Abort
**P0**: Gate results (statement/compile/axioms) → Accept / Investigate / Re-run

AskUserQuestion: **Accept result** / **Write USER_HINTS and retry** / **Abort**

## Step 3: Final Report

```
======================================================
 PIPELINE RESULT: <theorem_name>
======================================================
 Backend:     <backend> (<model_id>, effort=<effort>)
 Profile:     <profile>
 Stage 0:     <provider, chars, time>
 Stage 1:     <backend, nodes, time>
 Stage 2:     <iterations, sorry count, time>
 P0 Verdict:
   Gate 1 (statement): <PASS/FAIL>
   Gate 2 (compile):   <PASS/FAIL>
   Gate 3 (axioms):    <PASS/FAIL/SKIPPED>
   Overall:            <SOLVED/FAILED>
 Dep Audit:   <conforms/warnings>
 Total time:  <wall time>
 Results:     $RESULT_DIR/
======================================================
```

## Reference Tables

### Iteration Presets (profile controls iterations + DAG budget)

| Preset | DAG Iterations | Archon Iterations | Time per iter |
|--------|---------------|-------------------|---------------|
| **quick** | 4 | 10 | ~2-3min |
| balanced | 6 | 16 | ~2-3min |
| competition | 10 | 30 | ~2-3min |

DAG iterations 有早停：agent 写 `## Status: COMPLETE` → loop 提前结束。
Stage 0 和 Stage 1 由用户 **每次独立选择**，不绑定 preset。
Subagents: `enabled: "*"` (全部 14 个, 包括 critics + decomposition + construction)。

### Backend + Model

| Option | Backend | Model ID | Use |
|--------|---------|----------|-----|
| **Codex CLI + GPT-5.5** | codex | gpt-5.5 | Hard interactive proving |
| Codex CLI + GPT-5.4 | codex | gpt-5.4 | Stable fallback |
| Claude CLI + Sonnet 4.6 | claude_code | claude-sonnet-4-6 | Fast daily proving |
| Claude CLI + Opus 4.8 | claude_code | claude-opus-4-8 | Hardest theorems |
| API + DeepSeek V4 Flash | api | deepseek-v4-flash | Cheapest Stage 1 |

### Effort Mapping

| User | Archon codex | Archon claude | Rethlas codex | Rethlas claude |
|------|-------------|---------------|---------------|----------------|
| medium | medium | ignored | medium | medium |
| **high** | high | ignored | high | high |
| max | xhigh | ignored | xhigh | max |

### Verdict Result Structure

```json
{
  "solved": true,
  "reason": "ok",
  "gates": {
    "statement_identity": "pass",
    "compile_no_sorry": "pass",
    "axiom_allowlist": "pass",
    "kernel_recheck": "pass"
  },
  "theorem": "QIT.conditionalRenyi_valueSet_bddAbove",
  "artifact": {
    "schema": "verdict-v2/verification-artifact/1",
    "proof_sha256": "...",
    "toolchain": "Lean (version 4.31.0, ...)",
    "checker": "leanchecker"
  }
}
```

## Error Handling

- **Stage 0 fails**: retry once; skip and proceed
- **Stage 1 fails**: retry; suggest higher model/effort
- **archon dag fails**: check `.archon/logs/`; retry with more iterations
- **Stage 2 timeout**: offer continue / accept partial / abort
- **Stage 2 STUCK** (progress-critic): try higher effort, different model, or USER_HINTS
- **G1 fail (statement drift)**: prover changed theorem signature. Check namespace — `--name` must be FQN (auto-resolved since 2127b92).
- **G2 fail (sorry/compile)**: proving incomplete.
- **G3 fail (axiom cheat)**: soundness issue — investigate.
- **G4 fail (kernel recheck)**: independent checker disagrees — investigate olean build.
- **Dep audit violation**: warning only — graph debt, not soundness.

## Results Directory

```
results/<theorem_name>/<timestamp>/
├── result.json              (caller writes after run_pipeline returns)
├── nl_sketch.md             (if stage0_provider != "none")
├── .leandag/dag.json        (if stage1 != "none")
├── archon_stdout.log        (Archon loop stdout)
├── archon_stderr.log        (Archon loop stderr, if any)
├── archon_logs/             (Archon internal logs from .archon/logs/)
├── proved.lean              (if proved — copied from isolated workspace)
└── _workspace/              (isolated workspace dir, kept on failure for debugging)
```

Note: `scaffold.lean` is written to `lean_project_dir/Problems/` (inside workspace), not to results.
`result.json` is not generated by `run_pipeline()` — the caller serializes `PipelineResult`.
