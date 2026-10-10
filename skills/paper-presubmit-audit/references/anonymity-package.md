# Anonymity sweep for supplementary and code packages (Check 4)

Venues apply double-blind rules to everything uploaded or linked, and a leak in the code
package is a desk reject like a leak in the PDF. Audit the artifact a reviewer receives: the
uploaded archive, or the live anonymous link opened in a private browser window, not the
working repository.

## Where packages leak

- **Version control**: a `.git/` directory carries every commit's author, email, and
  timezone. Ship from `git archive` or a fresh export; a rewritten history still leaks
  through merge-commit messages and old objects.
- **Notebooks**: saved outputs print home paths, hostnames, stack traces, and run links;
  `metadata.kernelspec` names a personal environment. Strip outputs and metadata.
- **Experiment trackers**: `wandb.init(entity=...)`, logged run URLs
  (`wandb.ai/<entity>/...`), a committed `wandb/` settings directory, Hydra/Lightning
  output folders and `debug.log`.
- **Hub and download identifiers**: Hugging Face `username/model` IDs, checkpoint URLs on
  personal or institutional servers, Docker image names.
- **Paths and configs**: `/home/<user>`, `/Users/<user>`, cluster hostnames in configs and
  SLURM scripts, `prefix:` lines in conda `environment.yml`.
- **Authorship fields**: `LICENSE` copyright lines, `author=` in `setup.py` or
  `pyproject.toml`, file header comments, `CITATION.cff`.
- **Binary files**: PDF metadata and image EXIF (`exiftool`), plots showing a tracker
  workspace or a file path, editor folders (`.idea/`, `.vscode/`), `.DS_Store`.
- **LaTeX source uploads**: comments and commented-out text survive in the source even when
  the PDF is clean.

## Anonymizing hosts

anonymous.4open.science redacts only the terms it is given: the repository owner and name
automatically, everything else (names, institution, tracker entity, hostnames) through a
custom term list. Images, PDFs, and binaries are served unchanged. Redaction inside code can
change program behaviour, and can itself identify: redacting an institution that also names
the licence turns "MIT License" into "XXX License". Cached copies outlive edits to the
source repository, so check the live link after every change.

## Sweep

1. Build the package exactly as it will be uploaded.
2. Search every file, binaries included, for author names, emails, institution, account
   handles (GitHub, tracker, Hugging Face), `/home/`, `/Users/`, and hostnames.
3. Run `exiftool` on images and PDFs; list archive contents for `.git/`, notebooks with
   outputs, and tracker directories.
4. Open the anonymous link or archive as a reviewer would and browse it.

Report each leak with its file and line; a third-party tool's URL is not a leak.
