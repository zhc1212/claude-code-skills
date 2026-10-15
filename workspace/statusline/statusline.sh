#!/bin/bash
# Keep writing the quota snapshot for the host-side sync job, then render with ccstatusline.
# ccstatusline renders untruncated; statusline-fit.py lays it out for the terminal width.
set -o pipefail
input=$(cat)
fallback=$(printf '%s' "$input" | /usr/bin/python3 "$HOME/huicheng/config/claude-usage-statusline.py")
printf '%s' "$input" | CCSTATUSLINE_WIDTH=9999 ccstatusline 2>/dev/null \
  | /usr/bin/python3 "$HOME/.claude/statusline-fit.py" || printf '%s\n' "$fallback"
