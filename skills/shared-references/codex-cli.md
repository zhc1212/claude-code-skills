# Calling Codex through the CLI

Codex CLI 0.154.0 removed `codex mcp-server`, so skills call Codex through Bash.
A skill step written as `codex exec` (with `model`, `config`, `prompt`) starts a
new thread; one written as `codex exec resume` (with `threadId`, `prompt`)
continues an existing thread.

New thread. It prints the `threadId`, and Codex's reply goes to the `-o` file:

```bash
codex -c model_reasoning_effort=xhigh exec --json --skip-git-repo-check -m gpt-6-astra \
  -o /tmp/codex-reply.md - <<'PROMPT' | jq -r 'select(.type=="thread.started").thread_id'
<prompt>
PROMPT
```

Follow-up in the same thread:

```bash
codex exec resume <threadId> --json --skip-git-repo-check \
  -o /tmp/codex-reply.md - <<'PROMPT' >/dev/null
<prompt>
PROMPT
```

Then read `/tmp/codex-reply.md`.

- Map `model: X` to `-m X`, `cwd: D` to `-C D`, and each `config` key to
  `-c key=value` placed before `exec`. A `-c` after `exec` replaces every earlier
  `-c`, including the wrapper's sandbox default below.
- Pass the prompt on stdin through a quoted heredoc so the shell expands nothing.
- An xhigh call can run past the 10-minute Bash limit. Start long calls with
  `run_in_background` and read the `-o` file when the task finishes.
- Concurrent calls need distinct `-o` files.
- Do not pass `-s`. On the host, Codex keeps its own read-only sandbox. Inside the
  Claude sandbox, Codex's bubblewrap cannot nest, so the `codex` wrapper defaults to
  `danger-full-access` there; the outer sandbox still applies.
- If `codex` fails (not installed, not logged in, network), say so and follow the
  skill's fallback for an unavailable Codex.
