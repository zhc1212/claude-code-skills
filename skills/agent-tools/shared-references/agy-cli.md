# Calling Carbon through the agy CLI

The Antigravity CLI `agy` (1.5.14) has no MCP server mode, so skills call Gemini 4 Carbon through Bash.
Use one call form for every call, first and follow-up. `--settings` applies to a single invocation, so a
call without it runs with write and shell access: headless agy runs in Auto mode, and `--mode plan` does
not stop writes.

```bash
AGY_RO='{"permissions":{"deny":["write_file(*)","command(*)","mcp(*)"]}}'
cd <repository root or exchange> && agy --model gemini-4-carbon --effort high \
  --disable-slash-commands --settings "$AGY_RO" --output-format json --print-timeout 1200s \
  [--conversation <conversation_id>] \
  -p "$(cat <prompt file>)" > <reply>.json 2> <reply>.err
```

- Run from the repository root for a code topic. Otherwise run from the exchange directory.
- A denied write or command comes back to Carbon as a tool error, and the turn continues.
- **Evidence access.** With the shell denied, Carbon has no tool for listing or searching files. It opens files
  only by exact path, and a search request stalls for minutes before it gives up.
  - Give every cited file as an absolute path beside its excerpt.
  - Paste any web page Carbon needs: fetching a page goes through the denied shell. Web search still works.
  - Put this line in every prompt:

  ```
  Read-only session: shell commands and file writes are disabled. Open files only by the exact paths given; if you need anything else, name it in your reply instead of searching.
  ```

- Start each call with `run_in_background`. Read the files when the task finishes; a call took 369–553 s in
  testing.
- `-p` passes the prompt as a single argument, which Linux caps at 128 KB. Trim excerpts to fit.
- After the first call, save `jq -r .conversation_id` to a file. A call without `--conversation` starts a new
  conversation with no memory of earlier turns.
- **Checking that a reply completed.** A reply is complete when
  `jq -e '.status=="SUCCESS" and (.response|length>0) and .denied_actions==null'` passes; then
  `jq -r .response` gives the text. Otherwise read the `.err` file:
  - A tool that needed approval ends the turn with an empty response.
  - A timeout returns `"status":"ERROR"`.
  - In either case, resume the same conversation with a narrower request, and say that the previous turn ended
    before replying.
- If `agy` fails (not signed in, network), say so and follow the skill's fallback for an unreachable model.
  A sign-in error means Dr.Z runs `agy` once in a host terminal.
