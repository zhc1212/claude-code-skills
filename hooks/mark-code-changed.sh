#!/bin/bash
# PostToolUse hook: mark code files changed during this response.

set -euo pipefail

INPUT=$(cat)
CWD=$(printf '%s' "$INPUT" | python3 -c 'import json, sys; print(json.load(sys.stdin).get("cwd", "."))')

if [ ! -d "$CWD" ]; then
    exit 0
fi

FILE_PATH=$(printf '%s' "$INPUT" | python3 -c 'import json, sys; data=json.load(sys.stdin); print(data.get("tool_input", {}).get("file_path", ""))')
if [ -z "$FILE_PATH" ]; then
    exit 0
fi

case "$FILE_PATH" in
    *.py|*.js|*.ts|*.jsx|*.tsx|*.java|*.c|*.cpp|*.h|*.go|*.rs|*.rb|*.sh|*.yaml|*.yml)
        ;;
    *)
        exit 0
        ;;
esac

MARKER_DIR="$CWD/.claude/hooks/state"
mkdir -p "$MARKER_DIR"
printf '%s\n' "$FILE_PATH" >> "$MARKER_DIR/changed_files.txt"
