#!/usr/bin/env bash
# Lightweight skill eval runner for oral-paragraph-audit
# Usage: bash evals/run_tests.sh [test_id]
# Runs all tests if no test_id given, or a specific test (01, 02, etc.)

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SKILL_FILE="$SKILL_DIR/SKILL.md"
EVALS_DIR="$SKILL_DIR/evals"
RESULTS_DIR="$EVALS_DIR/results"
mkdir -p "$RESULTS_DIR"

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m'

total_pass=0
total_fail=0
total_skip=0

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

run_test() {
    local test_file="$1"
    local test_name
    test_name=$(basename "$test_file" .yaml)

    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  Test: $test_name"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    local prompt
    prompt=$(python3 -c "
import yaml, sys
with open('$test_file') as f:
    d = yaml.safe_load(f)
print(d['prompt'])
")

    local -a behaviors=()
    mapfile -t behaviors < <(python3 -c "
import yaml
with open('$test_file') as f:
    d = yaml.safe_load(f)
for b in d['expected_behavior']:
    print(b)
")

    local sys_prompt
    sys_prompt="You are executing the oral-paragraph-audit skill. Follow every check precisely and produce the full output format as specified.

$(cat "$SKILL_FILE")"

    echo "  Running claude -p (system=SKILL.md, prompt=test case)..."
    local output_file="$RESULTS_DIR/${test_name}.output.md"
    local raw_file="$RESULTS_DIR/${test_name}.raw.jsonl"
    local exit_code=0
    CLAUDE_WRAPPER_ASSUME_Y=Y timeout 300 claude -p --model sonnet --output-format json --append-system-prompt "$sys_prompt" "$prompt" > "$raw_file" 2>/dev/null || exit_code=$?
    # Extract result from JSONL (ignore non-zero exit from wrapper cleanup)
    extract_claude_response < "$raw_file" > "$output_file" 2>/dev/null || true

    if [ $exit_code -ne 0 ] || [ ! -s "$output_file" ]; then
        echo -e "  ${RED}ERROR: claude -p returned empty or failed (exit=$exit_code)${NC}"
        total_skip=$((total_skip + ${#behaviors[@]}))
        return
    fi

    local output
    output=$(cat "$output_file")
    local output_len=${#output}
    echo "  Response: ${output_len} chars → $output_file"

    local pass=0
    local fail=0

    for behavior in "${behaviors[@]}"; do
        local judge_result
        judge_result=$(CLAUDE_WRAPPER_ASSUME_Y=Y timeout 60 claude -p --model haiku --output-format json "You are a test judge. Given a skill output and an expected behavior criterion, determine if the output satisfies the criterion.

Answer ONLY 'PASS' or 'FAIL' on the first line, then one sentence of evidence.

Expected behavior: $behavior

Skill output (first 4000 chars):
${output:0:12000}" 2>/dev/null | extract_claude_response || echo "SKIP: judge failed")

        local first_line
        first_line=$(echo "$judge_result" | head -1)

        if echo "$first_line" | grep -qi "PASS"; then
            pass=$((pass + 1))
            total_pass=$((total_pass + 1))
            echo -e "  ${GREEN}✓ PASS${NC}: $behavior"
        elif echo "$first_line" | grep -qi "FAIL"; then
            fail=$((fail + 1))
            total_fail=$((total_fail + 1))
            local reason
            reason=$(echo "$judge_result" | sed -n '2p')
            echo -e "  ${RED}✗ FAIL${NC}: $behavior"
            [ -n "${reason:-}" ] && echo -e "         ${YELLOW}→ $reason${NC}"
        else
            total_skip=$((total_skip + 1))
            echo -e "  ${YELLOW}? SKIP${NC}: $behavior (judge: ${first_line:0:60})"
        fi
    done

    echo "  Result: ${pass}/${#behaviors[@]} passed"
}

echo "╔══════════════════════════════════════════╗"
echo "║  oral-paragraph-audit Skill Eval Suite   ║"
echo "╚══════════════════════════════════════════╝"

if [ -n "${1:-}" ]; then
    test_file=$(ls "$EVALS_DIR"/${1}*.yaml 2>/dev/null | head -1)
    if [ -z "$test_file" ]; then
        echo "Test not found: $1"
        exit 1
    fi
    run_test "$test_file"
else
    for test_file in "$EVALS_DIR"/*.yaml; do
        run_test "$test_file"
    done
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "  Total: ${GREEN}${total_pass} pass${NC} / ${RED}${total_fail} fail${NC} / ${YELLOW}${total_skip} skip${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

[ $total_fail -eq 0 ] && [ $total_skip -eq 0 ] && exit 0 || exit 1
