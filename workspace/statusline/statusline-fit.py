#!/usr/bin/env python3
"""Fit ccstatusline output to the terminal width.

One line when everything fits; otherwise keep the configured lines and
re-wrap each one at its "│" separators instead of letting it be cut off.
"""
import os
import re
import sys

ANSI = re.compile(r'\x1b\[[0-9;]*m|\x1b\]8;;[^\x07]*\x07')
SEP = re.compile(r'(?:\x1b\[[0-9;]*m)?[\xa0 ]+│[\xa0 ]+(?:\x1b\[39m)?')
MARGIN = 6  # same right margin ccstatusline reserves in "full" mode


def term_cols():
    # The status line runs on pipes; the nearest ancestor holding a tty is Claude Code.
    pid = os.getppid()
    for _ in range(8):
        for fd in (1, 2, 0):
            path = f'/proc/{pid}/fd/{fd}'
            try:
                if os.readlink(path).startswith(('/dev/pts/', '/dev/tty')):
                    f = os.open(path, os.O_RDONLY | os.O_NOCTTY)
                    try:
                        return os.get_terminal_size(f).columns
                    finally:
                        os.close(f)
            except OSError:
                pass
        try:
            with open(f'/proc/{pid}/stat') as f:
                pid = int(f.read().rsplit(')', 1)[1].split()[1])
        except (OSError, ValueError, IndexError):
            return None
        if pid <= 1:
            return None
    return None


def width(s):
    return len(ANSI.sub('', s))


lines = [l for l in sys.stdin.read().split('\n') if l]
if not lines:
    sys.exit()
cols = term_cols()
if not cols:
    print('\n'.join(lines))
    sys.exit()
limit = cols - MARGIN
joiner = next((m.group() for m in map(SEP.search, lines) if m), None)
segs = [SEP.split(l) for l in lines]

if joiner:
    one = joiner.join(s for ss in segs for s in ss)
    if width(one) <= limit:
        print(one)
        sys.exit()

out = []
for ss in segs:
    cur = ss[0]
    for s in ss[1:]:
        if width(cur) + width(joiner) + width(s) <= limit:
            cur += joiner + s
        else:
            out.append(cur)
            cur = s
    out.append(cur)
print('\n'.join(out))
