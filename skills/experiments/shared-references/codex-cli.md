# Calling Codex through the CLI

Codex CLI 0.154.0 removed `codex mcp-server`, so skills call Codex through Bash.
A skill step written as `codex exec` (with `model`, `config`, `prompt`) starts a
new thread; one written as `codex exec resume` (with `threadId`, `prompt`)
continues an existing thread.

New thread. It prints the `threadId`, and Codex's reply goes to the `-o` file:

```bash
LEAN="--disable multi_agent --disable apps --disable plugins --disable browser_use \
  --disable computer_use --disable image_generation --disable goals --disable tool_suggest \
  --disable skill_search --disable in_app_browser"
codex -c model_reasoning_effort=xhigh -c skills.include_instructions=false \
  exec $LEAN --json --skip-git-repo-check -m gpt-6.2-astra \
  -o /tmp/codex-reply.md - <<'PROMPT' | jq -r 'select(.type=="thread.started").thread_id'
<prompt>
PROMPT
```

Follow-up in the same thread:

```bash
codex -c skills.include_instructions=false exec resume <threadId> $LEAN --json --skip-git-repo-check \
  -o /tmp/codex-reply.md - <<'PROMPT' >/dev/null
<prompt>
PROMPT
```

Then read `/tmp/codex-reply.md`.

- Map `model: X` to `-m X`, `cwd: D` to `-C D`, and each `config` key to
  `-c key=value` placed before `exec`. A `-c` after `exec` replaces every earlier
  `-c`, including the wrapper's sandbox default below.
- Keep `$LEAN` and `skills.include_instructions=false` on every call: they stop
  Codex from spawning sub-agents and drop its skill listing and app/browser tools,
  which every request otherwise resends (first request 29.6K → 17.3K input tokens,
  CLI 0.167.0, 2026-11-20). Shell, `apply_patch`, `view_image` and web search stay.
  `--disable` takes effect only after `exec`; placed before it, `spawn_agent` stays.
- Pass the prompt on stdin through a quoted heredoc so the shell expands nothing.
- An xhigh call can run past the 10-minute Bash limit. Start long calls with
  `run_in_background` and read the `-o` file when the task finishes.
- Concurrent calls need distinct `-o` files.
- Do not pass `-s`. On the host, Codex keeps its own read-only sandbox. Inside the
  Claude sandbox, Codex's bubblewrap cannot nest, so the `codex` wrapper defaults to
  `danger-full-access` there; the outer sandbox still applies.
- If `codex` fails (not installed, not logged in, network), say so and follow the
  skill's fallback for an unavailable Codex.
