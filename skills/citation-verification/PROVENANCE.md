# citation-verification provenance

This third-party skill is vendored by explicit user request to preserve the active
user-level installation in this repository.

- Upstream: [Galaxy-Dawn/claude-scholar](https://github.com/Galaxy-Dawn/claude-scholar).
- Upstream commit: [`6ed46dac03191c7a734f49ed48b41195012098ff`](https://github.com/Galaxy-Dawn/claude-scholar/tree/6ed46dac03191c7a734f49ed48b41195012098ff/skills/citation-verification).
- Upstream path: `skills/citation-verification/`.
- Source installation: `~/.claude/skills/citation-verification/`.
- Imported on: 2026-09-10, in zhc-skills v1.0.12.
- Copyright: (c) 2026 Gaorui Zhang.
- License: MIT; the upstream license is reproduced in [LICENSE](LICENSE).

All nine source files match both the active installation and the pinned upstream
commit byte for byte. Packaging removes the extra blank line at EOF in
`references/api-usage.md`, `references/common-errors.md`, and
`references/verification-rules.md` so Git whitespace checks pass; all other
imported bytes are unchanged. `LICENSE` and this `PROVENANCE.md` are the only
packaging additions. This replaces the older adapted
citation-verification skill bundled through v1.0.11.

## Source file hashes (SHA-256)

| File | SHA-256 |
|---|---|
| `SKILL.md` | `c98a1be776ee4301425e01e4ed46488aba293487c8b572de8963cadf805f929a` |
| `references/README.md` | `72a1c6c93a200cfe138d520b08f7ac04148a9c7385d465f06880c49b9dc40140` |
| `references/api-usage.md` | `8272cf78b68eb7e3f9f45d47cdd9dedcfc9ee6903ff2ba34d8974f0b59f14a81` |
| `references/common-errors.md` | `f3e8fe91edc22d5d8ba798c9fecaf68ddb9ff327873b4b6f5aec7630f1819d2a` |
| `references/verification-rules.md` | `f5781c3d5d47d194a68228256909e73b2e15495426e089bfacb9cbcee7aaeb1f` |
| `scripts/README.md` | `8b70a6d4c48cc5876fd43b2e2cbb63c99c389d7a74b972371df5e29f71702479` |
| `scripts/api-clients.py` | `522e6cd132bb85bf57a75f72576e2836b312cce140eac481be7373cd64e6ecc0` |
| `scripts/format-checker.py` | `33329dc03a4573af4166b254b809787d07d884808aacd196a5f89d3812971cc9` |
| `scripts/verify-citations.py` | `f2ab99b2ed19b4ff3ab66885294485a2bf13d5318ff5c673198779a924561038` |

## Packaged hashes after EOF normalization

| File | SHA-256 |
|---|---|
| `references/api-usage.md` | `2848134370634a5e28b7edaf50b854224c52cd662105bc2a86b6591ea9828455` |
| `references/common-errors.md` | `7fb2a9473c50c978e7a0a08a97e5314f145a82a7d7df8f07ecc4478d8e21adab` |
| `references/verification-rules.md` | `74806a925c7176d7b5db737b853ecb13cf5ab7e8d1dbecaf629ce062aa0235be` |

## Updating this copy

Compare the installed files with a specific upstream commit before syncing. Preserve
the upstream license and attribution, update the commit and file hashes here, and
bump all four plugin/marketplace manifests. Record any local modifications explicitly.
Do not include caches, credentials, generated reports, or private bibliography files.

The Python scripts remain upstream reference implementations; see
[scripts/README.md](scripts/README.md) for their intended use and optional dependencies.
Their syntax and source identity are checked during packaging; live scholarly API
behavior and semantic citation verification are not certified by that check.
