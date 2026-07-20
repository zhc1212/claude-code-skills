# Research Workspace — Project-Level Claude Code Rules

This file is a portable version of the `CLAUDE.md` used in the author’s research workspace. Replace angle-bracket values before use.

## Scope

Keep Claude Code configuration project-scoped: `.claude/skills/`, `.claude/agents/`, and project `settings.local.json` load only beneath this workspace. Do not create global symlinks or global plugin configuration unless every project should inherit it.

## Remote Execution

| Host | SSH alias | Remote path |
|---|---|---|
| GPU worker | `<gpu-host>` | `<remote-root>/<project>` |

If remote access depends on a VPN or proxy, report a connectivity failure and wait; do not silently change routes.

## Code Workflow — Git First

**Local checkout is the sole code authority. Remote machines execute experiments only.**

```
local edit → commit → push → deploy → remote experiment
```

- Never edit code on the remote. An emergency patch must be exported as a diff, applied and committed locally, then redeployed.
- Never use `rsync` for code. Use it only to pull declared experiment artifacts, with an exclude list.
- Deploy between runs only, and record the commit SHA for every experiment.
- Keep heavy models, datasets, logs, and results on the execution host unless they are intentionally curated artifacts.

Maintain a project router table (local path, upstream repository, remote path, default branch) and update it whenever a project moves.

## Repository Documentation

Each project maintains:

- `CLAUDE.md`: environment, run commands, and current status. Update it when workflow-relevant code changes.
- `README.md`: directory map, including every script’s purpose and usage.

For organisation-owned repositories, keep personal workflow rules in an untracked `CLAUDE.local.md` rather than committing them upstream.

## Skills and Plugins

- This plugin contains original skills only. Third-party skills remain in their upstream plugin or clone; never copy them into this repository.
- On capability overlap, name a single owner and document the routing rule.
- Keep one source per upstream repository: do not install and clone the same skill collection simultaneously.
- After updating a source clone, check its exposed symlinks for renamed or new skills.
- After changing this plugin, bump all four manifest version fields before pushing.

The active third-party sources and symlink exposure list are in [`SKILL_SOURCES.md`](SKILL_SOURCES.md).

## Engineering Conventions

- Use the issue tracker as the work queue; define canonical triage labels once.
- Keep `CONTEXT.md` for domain language and ambiguities, and write architecture decisions as they are made under `docs/adr/`.
- Keep one agent-instruction file per repository. Do not maintain contradictory `CLAUDE.md` and `AGENTS.md` files.
- Use concise imperative commit messages.

## Working Rules

- State material assumptions and ask before designing an experiment when its goal or metric is unclear.
- Make the smallest change that directly satisfies the request; avoid speculative configuration and unrelated refactors.
- Define a verifiable outcome before implementation. For multi-step work, plan each step with its verification.
- Preserve decisions worth revisiting in a dated decision record.
