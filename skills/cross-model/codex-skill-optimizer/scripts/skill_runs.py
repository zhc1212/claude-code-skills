#!/usr/bin/env python3
"""Summarize past invocations of a Claude Code skill from local transcripts.

usage: python3 skill_runs.py <skill-name> [--final N]

Scans ~/.claude/projects/*/*.jsonl for Skill tool calls and slash commands
naming the skill. Per invocation it prints the request before it, the
arguments, Codex CLI calls and errors (when there are any), the start of the
last assistant text before the next user message (--final N characters,
default 300), and the next user messages. Transcripts older than
cleanupPeriodDays (default 30) have been deleted.
"""
import glob
import json
import os
import re
import sys

CODEX_ERROR = re.compile(r'(?i)(timed out|timeout|HTTP 4\d\d|error[:\]]|exit[= ]?[1-9]|not logged in|stream disconnected)')


def text_of(rec):
    content = rec.get('message', {}).get('content')
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return ' '.join(b.get('text', '') for b in content if isinstance(b, dict) and b.get('type') == 'text')
    return ''


def is_real_user(rec):
    if rec.get('type') != 'user':
        return False
    text = text_of(rec).strip()
    harness = text.startswith(('<', '(Re-invocation of /')) or 'Base directory for this skill' in text
    return bool(text) and not harness


def invocation_args(rec, skill):
    """Return the arguments if rec invokes the skill, else None."""
    content = rec.get('message', {}).get('content')
    if isinstance(content, list):
        for b in content:
            if (isinstance(b, dict) and b.get('type') == 'tool_use' and b.get('name') == 'Skill'
                    and b.get('input', {}).get('skill') == skill):
                return b['input'].get('args', '')
    if rec.get('type') == 'user':
        text = text_of(rec)
        if f'<command-name>/{skill}</command-name>' in text:
            m = re.search(r'<command-args>(.*?)</command-args>', text, re.S)
            return m.group(1) if m else ''
    return None


def one_line(text, n):
    return text[:n].replace('\n', ' / ')


def summarize(recs, i, args, final_n):
    before = next((text_of(r) for r in reversed(recs[:i]) if is_real_user(r)), '')
    end = next((j for j in range(i + 1, len(recs)) if is_real_user(recs[j])), len(recs))
    execs = resumes = 0
    errors, texts, codex_ids = [], [], set()
    for rec in recs[i + 1:end]:
        content = rec.get('message', {}).get('content')
        if not isinstance(content, list):
            continue
        for b in content:
            if not isinstance(b, dict):
                continue
            if b.get('type') == 'tool_use' and b.get('name') == 'Bash':
                cmd = b.get('input', {}).get('command', '')
                if 'codex exec resume' in cmd:
                    resumes += 1
                    codex_ids.add(b.get('id'))
                elif re.search(r'\bcodex\b.*\bexec\b', cmd):
                    execs += 1
                    codex_ids.add(b.get('id'))
            elif b.get('type') == 'tool_result' and b.get('tool_use_id') in codex_ids:
                m = CODEX_ERROR.search(json.dumps(b.get('content'))[:3000])
                if m:
                    errors.append(m.group(1))
            elif b.get('type') == 'text' and rec.get('type') == 'assistant':
                texts.append(b['text'])
    after = [one_line(text_of(r), 160) for r in recs[end:end + 40] if is_real_user(r)][:3]
    lines = []
    if execs or resumes:
        lines.append(f'CODEX : exec={execs} resume={resumes} errors={errors[:4]}')
    lines.append('ARGS  : ' + one_line(args, 220))
    lines.append('BEFORE: ' + one_line(before, 200))
    lines.append('FINAL : ' + one_line(texts[-1] if texts else '', final_n))
    lines += ['AFTER : ' + a for a in after]
    return lines


def main():
    if len(sys.argv) < 2 or sys.argv[1].startswith('-'):
        sys.exit(__doc__)
    skill = sys.argv[1]
    final_n = int(sys.argv[sys.argv.index('--final') + 1]) if '--final' in sys.argv else 300
    runs = 0
    for path in sorted(glob.glob(os.path.expanduser('~/.claude/projects/*/*.jsonl'))):
        try:
            with open(path) as fh:
                recs = [json.loads(line) for line in fh if line.strip()]
        except (OSError, ValueError):
            continue
        for i, rec in enumerate(recs):
            args = invocation_args(rec, skill)
            if args is None:
                continue
            runs += 1
            project = os.path.basename(os.path.dirname(path))[-40:]
            print('=' * 100)
            print(f"{rec.get('timestamp', '')[:16]} {project} {os.path.basename(path)[:8]}")
            print('\n'.join(summarize(recs, i, args, final_n)))
    print(f'\n{runs} invocation(s) of {skill} in the retained transcripts.')


if __name__ == '__main__':
    main()
