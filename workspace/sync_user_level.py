#!/usr/bin/env python3
"""Copy the installed user-level Claude config into this repository and check upstream skills.

    python3 workspace/sync_user_level.py            # ~/.claude -> repo, refresh manifest hashes
    python3 workspace/sync_user_level.py --verify   # also compare upstream skills with their upstream

The installed files are the source of truth. The manifest's `origin`, `source`, `upstream_path`,
`derived_from` and `known_deviations` fields are maintained by hand; this script refreshes
`installed_skill_sha256` and, with --verify, `upstream_commit`.
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

HOME = Path.home()
LIVE = HOME / '.claude/skills'
REPO = Path(__file__).resolve().parent.parent
WS = REPO / 'workspace'
MANIFEST = WS / 'USER_SKILLS_MANIFEST.json'
CACHE = HOME / '.cache/zhc-skill-upstreams'
SKIP = {'.git', '__pycache__', '.pytest_cache', 'node_modules'}
FILES = {
    HOME / '.claude/CLAUDE.md': WS / 'USER_CLAUDE.md',
    HOME / '.claude/statusline.sh': WS / 'statusline/statusline.sh',
    HOME / '.claude/statusline-fit.py': WS / 'statusline/statusline-fit.py',
    HOME / '.config/ccstatusline/settings.json': WS / 'statusline/ccstatusline-settings.json',
    HOME / 'huicheng/config/claude-usage-statusline.py': WS / 'statusline/claude-usage-statusline.py',
}


def rsync(src, dst):
    subprocess.run(['rsync', '-a', '-c', '--delete', *(f'--exclude={s}' for s in SKIP), '--exclude=*.pyc',
                    f'{src}/', f'{dst}/'], check=True)


def blob(path):
    data = path.read_bytes()
    return hashlib.sha1(b'blob %d\0' % len(data) + data).hexdigest()


def live_files(skill):
    for p in sorted((LIVE / skill).rglob('*')):
        rel = p.relative_to(LIVE / skill)
        if p.is_file() and not SKIP & set(rel.parts) and not any(x.startswith('results') for x in rel.parts[:-1]):
            yield rel.as_posix(), p


def sync(manifest):
    for src, dst in FILES.items():
        dst.write_bytes(src.read_bytes())
    settings = json.loads((HOME / '.claude/settings.json').read_text())
    (WS / 'statusline/settings-statusLine.json').write_text(
        json.dumps({'statusLine': settings['statusLine']}, indent=2) + '\n')
    for shared in REPO.glob('skills/*/shared-references'):
        rsync(LIVE / 'shared-references', shared)

    entries = {e['name']: e for e in manifest['skills']}
    folders = {p.name: p for p in REPO.glob('skills/*/*') if p.is_dir()}
    live = {p.name for p in LIVE.iterdir() if (p / 'SKILL.md').is_file()}
    problems = [f'{n}: installed but has no skills/<scenario>/{n}/ folder' for n in sorted(live - folders.keys())]
    problems += [f'{n}: installed but has no manifest entry (add one with its origin)' for n in sorted(live - entries.keys())]
    problems += [f'{n}: in the manifest but no longer installed (git rm its folder, drop the entry)'
                 for n in sorted(entries.keys() - live)]
    for n in sorted(live & folders.keys() & entries.keys()):
        rsync(LIVE / n, folders[n])
        entries[n]['installed_skill_sha256'] = hashlib.sha256((LIVE / n / 'SKILL.md').read_bytes()).hexdigest()
    manifest['active_skill_count'] = len(live)
    return problems


def git(repo, *args):
    return subprocess.run(['git', '-C', str(repo), *args], capture_output=True, text=True, check=True).stdout


def upstream_clone(source):
    slug = source.removeprefix('https://github.com/').strip('/')
    repo = CACHE / slug.replace('/', '__', 1)
    if repo.exists():
        git(repo, 'fetch', '-q')
    else:
        CACHE.mkdir(parents=True, exist_ok=True)
        subprocess.run(['git', 'clone', '-q', '--filter=blob:none', '--no-checkout', source, str(repo)], check=True)
    return repo


def verify(entry, repo):
    """Return (status, details); updates entry['upstream_commit'] when SKILL.md matches a commit."""
    base = entry['upstream_path'].strip('/')
    prefix = f'{base}/' if base else ''
    head = {}
    for line in git(repo, 'ls-tree', '-r', 'origin/HEAD', '--', base or '.').splitlines():
        meta, path = line.split('\t', 1)
        head[path.removeprefix(prefix)] = meta.split()[2]
    if 'SKILL.md' not in head:
        moved = [p[:-len('/SKILL.md')] for p in git(repo, 'ls-tree', '-r', '--name-only', 'origin/HEAD').split()
                 if p.endswith(f"/{entry['name']}/SKILL.md")]
        return ('MOVED upstream: set upstream_path', moved) if moved else ('REMOVED upstream: retire it', [])
    history, first_commit = {}, {}
    commit = None
    for line in git(repo, 'log', '--all', '--no-renames', '--format=C %h', '--raw', '--no-abbrev',
                    '--', base or '.').splitlines():
        if line.startswith('C '):
            commit = line[2:]
        elif line.startswith(':'):
            meta, path = line.split('\t', 1)
            rel, (old, new) = path.removeprefix(prefix), meta.split()[2:4]
            history.setdefault(rel, set()).update((old, new))  # old side covers blobs introduced by merges
            first_commit.setdefault((rel, new), commit)
    allowed = set(entry.get('known_deviations', []))
    modified, behind = [], []
    local = dict(live_files(entry['name']))
    for rel, path in local.items():
        h = blob(path)
        if head.get(rel) == h or rel in allowed or (rel not in history and rel not in head):
            continue  # identical, registered deviation, or a local-only addition (PROVENANCE, LICENSE)
        (behind if h in history.get(rel, ()) else modified).append(rel)
    skill_md = blob(LIVE / entry['name'] / 'SKILL.md')
    if ('SKILL.md', skill_md) in first_commit:
        entry['upstream_commit'] = first_commit[('SKILL.md', skill_md)]
    elif head['SKILL.md'] == skill_md:  # introduced by a merge commit
        entry['upstream_commit'] = git(repo, 'rev-parse', 'origin/HEAD').strip()
    if modified:
        return 'MODIFIED locally', modified
    return ('behind upstream', behind) if behind else ('current', [])


def main():
    manifest = json.loads(MANIFEST.read_text())
    problems = sync(manifest)
    if '--verify' in sys.argv:
        repos = {}
        for e in manifest['skills']:
            if e.get('origin') != 'upstream' or not (LIVE / e['name']).is_dir():
                continue
            if e['source'] not in repos:
                repos[e['source']] = upstream_clone(e['source'])
            status, details = verify(e, repos[e['source']])
            if status != 'current':
                print(f"{e['name']}: {status}" + (f" ({', '.join(details[:5])})" if details else ''))
            if status.split()[0].isupper():
                problems.append(f"{e['name']}: {status}")
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n')
    for p in problems:
        print('PROBLEM', p)
    sys.exit(1 if problems else 0)


if __name__ == '__main__':
    main()
