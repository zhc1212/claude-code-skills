#!/usr/bin/env python3
"""Trigger smoke test for skill routing: python3 evals/run_triggers.py [model].

Runs each prompt in triggers.yaml once with `claude -p --max-turns 1` and checks
which Skill the first assistant turn calls. One run per prompt is a smoke test,
not a trigger-rate measurement.
"""
import json, os, subprocess, sys, yaml

here = os.path.dirname(os.path.abspath(__file__))
model = sys.argv[1] if len(sys.argv) > 1 else "sonnet"
fails = 0
for t in yaml.safe_load(open(os.path.join(here, "triggers", "triggers.yaml"))):
    proc = subprocess.run(
        ["claude", "-p", "--model", model, "--max-turns", "1", "--verbose",
         "--output-format", "stream-json", t["prompt"]],
        stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=300,
        env={**os.environ, "CLAUDE_WRAPPER_ASSUME_Y": "Y"}, cwd="/tmp")
    skills = []
    for line in proc.stdout.splitlines():
        try:
            d = json.loads(line)
        except ValueError:
            continue
        if d.get("type") == "assistant":
            for c in d["message"].get("content", []):
                if c.get("type") == "tool_use" and c.get("name") == "Skill":
                    skills.append(c["input"].get("skill", ""))
    ok = True
    if "expect" in t and (not skills or skills[0] != t["expect"]):
        ok = False
    if "forbid" in t and t["forbid"] in skills:
        ok = False
    fails += not ok
    print(f"{'PASS' if ok else 'FAIL'} {t['id']}: skills={skills or ['(none)']}")
print(f"{fails} fail")
sys.exit(1 if fails else 0)
