#!/usr/bin/env bash
# Eval runner for oral-paragraph-audit.
#
# Invokes the skill the real way: `claude -p "/oral-paragraph-audit ..."` in
# headless mode — the installed zhc-skills plugin supplies the skill, exactly
# as in an interactive session. No system-prompt injection.
#
# One command, auto mode:
#   bash evals/run_tests.sh          # regenerates a test only if its saved
#                                    # output is missing or older than
#                                    # SKILL.md / the test YAML; then runs
#                                    # deterministic marker checks (the gate)
# Options:
#   bash evals/run_tests.sh 03       # single test
#   bash evals/run_tests.sh --fresh  # force regeneration of all
#   bash evals/run_tests.sh --judge  # + advisory LLM judging (not in exit code)

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SKILL_FILE="$SKILL_DIR/SKILL.md"
EVALS_DIR="$SKILL_DIR/evals"
RESULTS_DIR="$EVALS_DIR/results"
mkdir -p "$RESULTS_DIR"

GREEN='\033[0;32m'; RED='\033[0;31m'; YELLOW='\033[0;33m'; NC='\033[0m'

FRESH=0; JUDGE=0; TEST_ID=""
for arg in "$@"; do
    case "$arg" in
        --fresh) FRESH=1 ;;
        --judge) JUDGE=1 ;;
        *) TEST_ID="$arg" ;;
    esac
done

det_pass=0; det_fail=0; gen_err=0
adv_pass=0; adv_fail=0; adv_skip=0

extract_claude_response() {
    python3 -c "
import sys, json
for line in sys.stdin:
    line = line.strip()
    if not line: continue
    try:
        d = json.loads(line)
        if d.get('type') == 'result':
            print(d.get('result',''))
            break
    except: pass
"
}

yaml_get() {
    python3 -c "
import yaml
d = yaml.safe_load(open('$1'))
v = d.get('$2') or []
if isinstance(v, str): print(v)
else:
    for x in v: print(x)
"
}

check_markers() {
    python3 - "$1" "$2" <<'PYEOF'
import sys, re, yaml
out = open(sys.argv[1], encoding='utf-8', errors='ignore').read()
d = yaml.safe_load(open(sys.argv[2]))
fails = 0
for pat in d.get('required_markers') or []:
    if re.search(pat, out, re.IGNORECASE | re.MULTILINE):
        print(f"PASS required {pat}")
    else:
        print(f"FAIL required {pat}")
        fails += 1
for pat in d.get('forbidden_markers') or []:
    if re.search(pat, out, re.IGNORECASE | re.MULTILINE):
        print(f"FAIL forbidden {pat}")
        fails += 1
    else:
        print(f"PASS forbidden-absent {pat}")
sys.exit(0 if fails == 0 else 1)
PYEOF
}

run_test() {
    local test_file="$1"
    local test_name; test_name=$(basename "$test_file" .yaml)
    local output_file="$RESULTS_DIR/${test_name}.output.md"

    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  Test: $test_name"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    if ! python3 -c "
import yaml, sys
d = yaml.safe_load(open('$test_file'))
sys.exit(0 if d.get('prompt') and d.get('required_markers') else 1)"; then
        echo -e "  ${RED}SCHEMA ERROR: missing prompt or required_markers${NC}"
        gen_err=$((gen_err + 1)); return
    fi

    # regenerate only when stale (or --fresh): output missing, SKILL.md newer,
    # or the test prompt changed (hash) — marker-only edits never force regen
    local hash_file="$RESULTS_DIR/${test_name}.prompt.md5"
    local cur_hash
    cur_hash=$(yaml_get "$test_file" prompt | md5sum | cut -d' ' -f1)
    local need_gen=0
    if [ "$FRESH" -eq 1 ] || [ ! -s "$output_file" ] \
       || [ "$SKILL_FILE" -nt "$output_file" ] \
       || [ ! -f "$hash_file" ] || [ "$(cat "$hash_file")" != "$cur_hash" ]; then
        need_gen=1
    fi

    if [ "$need_gen" -eq 1 ]; then
        local prompt; prompt=$(yaml_get "$test_file" prompt)
        echo "  Generating via real skill invocation (claude -p, model=sonnet)..."
        local raw_file="$RESULTS_DIR/${test_name}.raw.jsonl"
        local exit_code=0
        CLAUDE_WRAPPER_ASSUME_Y=Y timeout 300 claude -p --model sonnet --output-format json "$prompt" > "$raw_file" 2>/dev/null || exit_code=$?
        extract_claude_response < "$raw_file" > "$output_file" 2>/dev/null || true
        if [ $exit_code -ne 0 ] || [ ! -s "$output_file" ]; then
            echo -e "  ${RED}GENERATION ERROR (exit=$exit_code, output empty)${NC}"
            gen_err=$((gen_err + 1)); return
        fi
        echo "$cur_hash" > "$hash_file"
        echo "  Response: $(wc -c < "$output_file") chars → $output_file"
    else
        echo "  Saved output is current — validating without regeneration"
    fi

    # deterministic gate
    local marker_report
    if marker_report=$(check_markers "$output_file" "$test_file"); then
        local n; n=$(echo "$marker_report" | grep -c '^PASS')
        det_pass=$((det_pass + n))
        echo -e "  ${GREEN}✓ markers: ${n}/${n} pass${NC}"
    else
        while IFS= read -r line; do
            case "$line" in
                PASS*) det_pass=$((det_pass + 1)); echo -e "  ${GREEN}✓ ${line}${NC}" ;;
                FAIL*) det_fail=$((det_fail + 1)); echo -e "  ${RED}✗ ${line}${NC}" ;;
            esac
        done <<< "$marker_report"
    fi

    # advisory judge (opt-in)
    if [ "$JUDGE" -eq 1 ]; then
        local output; output=$(cat "$output_file")
        while IFS= read -r behavior; do
            [ -z "$behavior" ] && continue
            local judge_result
            judge_result=$(CLAUDE_WRAPPER_ASSUME_Y=Y timeout 60 claude -p --model haiku --output-format json "You are a test judge. Given a skill output and an expected behavior criterion, determine if the output satisfies the criterion.

Answer ONLY 'PASS' or 'FAIL' on the first line, then one sentence of evidence.

Expected behavior: $behavior

Skill output (truncated):
${output:0:12000}" 2>/dev/null | extract_claude_response || echo "SKIP: judge failed")
            local first_line; first_line=$(echo "$judge_result" | head -1)
            if echo "$first_line" | grep -qi "PASS"; then
                adv_pass=$((adv_pass + 1)); echo -e "  ${GREEN}~ advisory PASS${NC}: $behavior"
            elif echo "$first_line" | grep -qi "FAIL"; then
                adv_fail=$((adv_fail + 1)); echo -e "  ${YELLOW}~ advisory FAIL${NC}: $behavior"
            else
                adv_skip=$((adv_skip + 1)); echo -e "  ${YELLOW}~ advisory SKIP${NC}: $behavior"
            fi
        done < <(yaml_get "$test_file" expected_behavior)
    fi
}

echo "╔══════════════════════════════════════════╗"
echo "║  oral-paragraph-audit Skill Eval Suite   ║"
echo "╚══════════════════════════════════════════╝"
[ "$FRESH" -eq 1 ] && echo "  Mode: forced regeneration"
[ "$JUDGE" -eq 1 ] && echo "  Advisory LLM judge: enabled"

if [ -n "$TEST_ID" ]; then
    test_file=$(ls "$EVALS_DIR"/${TEST_ID}*.yaml 2>/dev/null | head -1)
    [ -z "$test_file" ] && { echo "Test not found: $TEST_ID"; exit 1; }
    run_test "$test_file"
else
    for test_file in "$EVALS_DIR"/*.yaml; do
        run_test "$test_file"
    done
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "  Deterministic: ${GREEN}${det_pass} pass${NC} / ${RED}${det_fail} fail${NC} / ${YELLOW}${gen_err} generation errors${NC}"
[ "$JUDGE" -eq 1 ] && echo -e "  Advisory:      ${adv_pass} pass / ${adv_fail} fail / ${adv_skip} skip (not counted)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

[ $det_fail -eq 0 ] && [ $gen_err -eq 0 ] && exit 0 || exit 1
