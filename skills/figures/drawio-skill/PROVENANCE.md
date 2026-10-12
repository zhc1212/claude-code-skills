# drawio-skill provenance

Third-party skill installed by user request on 2026-10-12 for editable draw.io paper diagrams.

- Upstream: [Agents365-ai/drawio-skill](https://github.com/Agents365-ai/drawio-skill), commit `57270820d3cd71cbdf4fb6b2f7091d4fb37bb019`
  (skill v3.4.3), path `skills/drawio-skill/`.
- Copyright: (c) 2026 Agents365-ai. License: MIT, in [LICENSE](LICENSE).

Unmodified; this file is the only addition. `disable-model-invocation: true`: it runs only when the user
invokes `/drawio-skill`. Native PNG/SVG/PDF export uses the draw.io desktop CLI (installed 2026-10-12, run
headless through Xvfb); for a paper PDF add `--crop`, since `-f pdf` alone gives a Letter page. Authoring
`.drawio` XML, the Diagram IR and `validate.py` need only Python 3.
