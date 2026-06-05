# Recovery Matrix

Diagnose failures before retrying. Different failure types need different
actions — blind retrying wastes attempts and can introduce new issues.

## Diagnosis → Action

### 1. Syntax / Import Errors

**Signal**: ImportError, SyntaxError, ModuleNotFoundError in test or impl output.

**Diagnosis**: Codex used wrong import paths, missing dependencies, or
incompatible Python syntax.

**Action**:
- Check which imports failed against the project's actual module structure
- Update the spec with correct import paths and module structure
- Retry the same phase (A or B) with the corrected spec

**Typical cause**: Spec didn't include enough project context (import patterns,
module locations). Prevent by including the project context capsule.

### 2. Weak / Tautological Tests

**Signal**: Gate checks #4 or #7 fail — tests pass for wrong implementations,
or Claude can't name a non-trivial wrong behavior that would fail.

**Diagnosis**: Tests check types/shapes but not values, or assert the
implementation's actual behavior rather than the spec's required behavior.

**Action**:
- Send specific feedback to Codex-A: "Test X passes for any tensor of shape
  (d, r). Add `assert_close` against known expected values."
- Include a concrete wrong implementation that currently passes
- Retry Phase A

**Typical cause**: Spec's acceptance criteria are too vague ("returns correct
result" instead of "returns tensor within 1e-5 of expected values X, Y, Z").

### 3. Spec Ambiguity

**Signal**: Codex asks clarifying questions in its output, tests miss the
intent (cover something different from what was meant), or Phase B implements
something technically correct but wrong.

**Diagnosis**: The spec was underspecified, ambiguous, or Claude misunderstood
the user's intent.

**Action**:
- Revise the spec — add concrete examples, tighten acceptance criteria
- Show revised spec to the user for confirmation
- Restart from Phase A (new tests needed for new spec)

**Typical cause**: User's request was high-level ("add caching") and Claude
didn't decompose it into specific behavioral requirements.

### 4. Environment Failures

**Signal**: MCP timeout (>15 min), git conflicts, permission errors,
dependency issues, CUDA errors in CPU-only tests.

**Diagnosis**: Infrastructure problem, not code logic problem.

**Action**:
- Check `git status` for partial changes from interrupted sessions
- Verify MCP connectivity
- Clean up any partial state (targeted revert of specific files)
- Retry the same phase once

**Typical cause**: Network issues, Codex session timeout, git state corruption
from interrupted operations.

### 5. Incomplete Implementation

**Signal**: Some tests pass, some fail. Phase B's implementation is on the
right track but doesn't cover all cases.

**Diagnosis**: Codex-B understood the contract but didn't finish implementing
all edge cases, or hit a tricky case it couldn't solve.

**Action**:
- Send the failing test output (not the passing tests) to Codex-B via
  `mcp__codex__codex-reply` with the Phase B threadId
- Include the specific assertion failures and expected values
- Retry Phase B

**Typical cause**: Complex acceptance criteria that Codex partially addresses.
Often resolves in 1 retry with targeted error messages.

## Reclassification

After one failed targeted retry:
1. Re-read the spec, test diff, RED/GREEN logs, and changed files
2. Consider whether the diagnosis was correct
3. Choose a different diagnosis category if the evidence points elsewhere
4. If the same diagnosis still seems right but retry failed, escalate

## Escalation Rules

- 2 same-diagnosis failures → escalate to user
- 3 total retries in any single phase → escalate to user
- Environment retries (MCP timeout, git conflict) don't count toward phase
  retry budget — they're infrastructure issues, not code issues
- Tell the user: what was attempted, what failed, which diagnosis was used
- Offer: Claude takes over implementation, or user adjusts the spec/approach
