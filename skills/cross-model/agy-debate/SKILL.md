---
name: agy-debate
description: Structured multi-round debate between Claude and Gemini 4 Carbon through the Antigravity CLI (`agy`), run on codex-debate's protocol (blind openings, crux ledger, steel-manned rounds, synthesis). Use when the user names agy, Gemini or Carbon as the other side — "agy debate", "和agy讨论", "让gemini和你辩", "carbon debate". A two-model debate that names no model stays with codex-debate.
---

# agy Debate

1. Read [`../codex-debate/SKILL.md`](../codex-debate/SKILL.md) and run its whole protocol (evidence
   tiers, Phases 1–7, behavioral rules) with its templates and
   [`../codex-debate/references/consensus-template.md`](../codex-debate/references/consensus-template.md).
2. Apply the substitutions below everywhere, including inside the prompt templates. Every
   Codex step becomes an agy step; the debate runs without any `codex` command.
3. Apply the two Carbon rules below on top of the protocol. Where the two files differ, this
   file wins.

## Substitutions

| codex-debate | agy-debate |
|---|---|
| Codex (the opponent) | Carbon (Gemini 4 Carbon High via `agy`) |
| `codex exec` with `model`, `config`, `cwd` | the call form below, without `--conversation` |
| `codex exec resume` with `threadId` | the same call form with `--conversation <conversation_id>` |
| `../shared-references/codex-cli.md`, section "Codex CLI" | section "agy CLI" here |
| `thread_id` file | `conversation_id` file |
| `r{N}-codex.md` (the `-o` file) | `r{N}-agy.json`, then its `.response` saved as `r{N}-agy.md` |
| template line `Codex: {model}, {effort}, thread {threadId}` | `agy: gemini-4-carbon, high, conversation {conversation_id}` |
| confidence label `X:` in the crux ledger | `G:` (`C:` stays Claude) |
| Codex opens the repository through `cwd` | Carbon opens files only by exact path; see "Evidence access" |

## Carbon rules

- **Verify on arrival.** Each round, open every checkable claim from Carbon that bears on a
  crux (file:line, quoted code, citation, number, API name) before it enters the crux ledger.
  Until opened it is `unverified`, and an unverified claim leaves every crux status unchanged.
  A `code-inspected` tag on a path outside the packet counts as `inference` until you open it.
- **Widen the option space.** Add this section to the blind-opening request, after `## Risks`:

  ```
  ## Alternatives Outside the Framing
  [at least one option the question does not list, with its strongest case]
  ```

  Treat a surviving alternative as a new crux.

## Evidence access

Carbon has no directory-listing or search tool: with the shell denied it opens files only by
exact path, and a search request stalls for minutes before it gives up.

- Run each call from the repository root for a code topic, otherwise from the exchange
  directory.
- In the packet, give every cited file as an absolute path beside its excerpt, and paste any web
  page Carbon needs: fetching a page goes through the denied shell, though web search still works.
- In every prompt, first and follow-up, replace codex-debate's read-only line with this line:

  ```
  Read-only session: shell commands and file writes are disabled. Open files only by the exact paths given; if you need anything else, name it in your reply instead of searching.
  ```

## agy CLI

One call form for every call, first and follow-up. `--settings` lasts one invocation, so a call
without it runs with write and shell access:

```bash
AGY_RO='{"permissions":{"deny":["write_file(*)","command(*)","mcp(*)"]}}'
cd <repository root or exchange> && agy --model gemini-4-carbon --effort high \
  --disable-slash-commands --settings "$AGY_RO" --output-format json --print-timeout 1200s \
  [--conversation <conversation_id>] \
  -p "$(cat <exchange>/r{N}-prompt.md)" > <exchange>/r{N}-agy.json 2> <exchange>/r{N}-agy.err
```

A denied write or command comes back to Carbon as a tool error and the turn continues.

- Run each call with `run_in_background` and read the files when the task finishes; a blind
  opening took 553 s in testing.
- `-p` passes the prompt as one argument, which Linux caps at 128 KB; trim excerpts to fit.
- After the first call, save `jq -r .conversation_id` to `<exchange>/conversation_id`.
- A round is complete when
  `jq -e '.status=="SUCCESS" and (.response|length>0) and .denied_actions==null'` passes on
  `r{N}-agy.json`; then save `jq -r .response` as `r{N}-agy.md`. Otherwise read
  `r{N}-agy.err`: a tool that needed approval ends the turn with an empty response, and a
  timeout returns `"status":"ERROR"`. Resume the same conversation with the request narrowed,
  and say in the prompt that the previous turn ended before replying.
- A call without `--conversation` starts a new conversation with no memory of earlier rounds.
- If `agy` fails (not signed in, network), follow codex-debate's fallback for an unreachable
  Codex. A sign-in error means Dr.Z runs `agy` once in a host terminal.
