# User-level snapshot — 2026-10-01

Update 2026-10-08 (v1.0.17): unlike the snapshot below, this sync follows an upgrade of 23 installed
third-party skills to their current upstream; the README lists them. The installed files remain the source of truth.

Version 1.0.15 snapshots the user's active `~/.claude/CLAUDE.md` and all 158
readable top-level skills in `~/.claude/skills/`. The existing repository-only
`run-pipeline` remains, giving 159 packaged skills. The installed files are the
source of truth: this update does not upgrade skills from upstream or modify the
active installation.

## Layout and restoration

- `USER_CLAUDE.md` is an exact copy of the user-level `CLAUDE.md`, including its
  routing table and machine-specific paths. Review those paths before use on
  another machine. References to local memory describe files outside this snapshot.
- `../skills/` contains skill instructions, references, scripts, tests, templates,
  and assets. Copy the desired directories into `~/.claude/skills/`, or install
  the repository as a plugin. Avoid exposing both copies under the same names.
- To restore the user configuration, review `USER_CLAUDE.md` against the existing
  `~/.claude/CLAUDE.md`, back up that file, then copy the snapshot into its place.
  The older `CLAUDE.md` in this directory is the preserved project-level example.
- `USER_SKILLS_MANIFEST.json` lists every installed skill, its SKILL.md SHA-256,
  available source evidence, and exclusions. `user-skills-lock.json` is the
  unchanged installed lockfile. Its slide-maker hash was already stale according
  to local update records; use the manifest's installed SHA-256 for this snapshot.

## Deliberate exceptions

- `slide-maker` was a link into `~/.claude/skills/.agents/skills/slide-maker`.
  Its contents are materialized in `../skills/slide-maker/`; the hidden installer
  layout and redundant `.claude/skills/slide-maker` link are not duplicated.
- `run-baseline` is a broken link into a QIprover worktree. No readable content
  exists at its target, so it cannot be included. No replacement is invented.
- Nested `.git` directories, Python caches, generated `evals/results/` outputs,
  and unpublished `oral-paragraph-audit` fixtures 08–13 are excluded. Two `.env`
  files in neat-freak's evaluation fixtures are upstream synthetic examples,
  not live user configuration, and are retained with the fixtures.
- `deai-latex/SKILL.md` encodes its unchanged description as a YAML folded
  scalar to repair the installed copy's unquoted colon. The installed file is
  unchanged.
- Citation-verification keeps the existing three documented EOF whitespace
  normalizations and its original license/provenance files.
- Plugin installations, parked skills, credentials, settings, local memory, and
  projects referenced by skills are outside the requested config/skills snapshot.
  Referenced external programs and dependencies still need separate installation.

## Attribution and licenses

Third-party skills retain their own licenses. Copies of available upstream
license and notice files are in `third-party-licenses/`, and installed per-skill
licenses remain in their directories. This includes MIT, Apache-2.0, and
CC BY-NC-SA-4.0 material; the plugin manifests no longer label the entire bundle
MIT. In particular, the Supervisor-Skills copies (`deep-research`,
`drawio-reconstruction`, `paper-polish`, and `paper-writer`) are attributed to
[HKUSTDial/Supervisor-Skills](https://github.com/HKUSTDial/Supervisor-Skills);
its CC BY-NC-SA-4.0 license is retained, along with any per-skill notices.

An observed source clone HEAD records the clone available at snapshot time, not
necessarily the installed version. `skill_md_matches_clone` explicitly records
whether the installed SKILL.md matches that clone; it does not assert that every
supporting file matches. Installed local modifications and skills removed from
current upstream trees remain intact. Existing per-skill provenance takes
precedence over the aggregate inventory. No upstream authorship is reassigned.

This is a file and packaging snapshot, not evidence that every skill has been
executed successfully or that external API/model integrations have been tested.

The snapshot preserves pre-existing trailing whitespace and blank EOF lines in
30 imported files. A full `git diff --cached --check` reports these source
formatting issues; they are not silently normalized during synchronization.
