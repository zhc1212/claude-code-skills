# Staging, Capture and Promote

Commands for Stages 1, 3 and 5. `REPO` is the repository root (the top of everything the
generators read), `PY` the project's interpreter, `GUARD` this skill's `scripts/figure_guard.py`,
and `GEN` the generator path relative to `REPO` (for example `paper/figures/src/make_figures.py`).

## 1. Stage

```bash
RUN=/tmp/figure-pipeline-$(date +%Y%m%d-%H%M%S); TREE=$RUN/tree; mkdir -p $TREE
cd $REPO && rsync -aR --exclude '*.aux' --exclude '*.log' paper/ $(dirname $GEN)/ $TREE/
```

Copy the paper directory and the generator directory with `rsync -aR`, which keeps the
repository-relative paths that generators resolve from their own location. Repositories holding
large datasets need only the files the generator reads, found next.

Capture once, in the fresh tree: the reproduction check compares each output with the file the
tree held before the run, so a second baseline capture after any regeneration proves nothing. To
redo the baseline, stage again. Each missing input stops the generator; this loop copies it in
from the repository at the same relative path and retries:

```bash
for i in $(seq 20); do
  out=$(cd $TREE && $PY $GUARD capture $RUN/cap0 --root $TREE -- $GEN 2>&1) && break
  missing=$(echo "$out" | grep -o "No such file or directory: '[^']*'" | head -1 | sed "s/.*: '//; s/'$//")
  [ -z "$missing" ] && { echo "$out" | tail -5; break; }    # a real failure: read it
  (cd $REPO && rsync -aR "${missing#$TREE/}" $TREE/)
done
```

- Every saved file name in `$RUN/cap0/*.json` must be relative. An absolute name means the
  generator writes outside the tree, into the live repository: stop and point it at the tree.
- The comparison flags any output the capture did not reproduce:
  `$PY $GUARD compare $RUN/cap0 $RUN/cap0`.

Freeze the inputs: the repository must hold the bytes the capture read.

```bash
jq -r 'to_entries[] | "\(.value)  \(.key)"' $RUN/cap0/reads.json > $RUN/inputs.sha256
cd $REPO && sha256sum -c --quiet $RUN/inputs.sha256
```

Compile with the project's own command (here latexmk) and compare the measurements with the
report's Measurements table:

```bash
cd $TREE/paper && latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex > $RUN/build0.log 2>&1
cp main.pdf $RUN/baseline.pdf
python3 <figure-audit>/scripts/figure_text_audit.py $RUN/baseline.pdf
```

Record the write-back candidates, every generator output and source, in the repository state:

```bash
cd $REPO && sha256sum $GEN <style helpers> <outputs from cap0> > $RUN/baseline.sha256
cd $REPO && sha256sum <main.tex and every file it inputs> > $RUN/text.sha256   # read by the Recheck only
```

## 3. Capture after each edit

```bash
cd $TREE && $PY $GUARD capture $RUN/cap1 --root $TREE -- $GEN && $PY $GUARD compare $RUN/cap0 $RUN/cap1
```

Keep `cap0` as the reference for every round, so each comparison shows the cumulative change.
`--json` gives the same result for scripting. `git diff --no-index` between the repository file
and its tree copy shows the source edit for the report.

## 5. Promote

```bash
cd $REPO && sha256sum -c --quiet $RUN/baseline.sha256 || echo "BLOCKED: changed since staging"
cd $REPO && sha256sum -c --quiet $RUN/text.sha256 || echo "TEXT MOVED: re-verify captions and citing sentences"
for f in <edited sources and regenerated outputs>; do cp $TREE/$f $REPO/$f; done
```

Run the check immediately before copying. It detects a concurrent change; it is not a lock, so
keep the gap between check and copy to one command. Files outside the list stay untouched.

A moved text does not block: the promoted figures are the verified bytes, but the Recheck judged
them against the old captions and citing sentences. Compare those of every changed figure with the
live TeX, then compile a copy of the live paper with the promoted files, outside the live directory
since another session may be building there:

```bash
rsync -a --exclude 'main.pdf' $REPO/paper/ $RUN/live/paper/ && (cd $RUN/live/paper && latexmk -pdf main.tex)
python3 <figure-audit>/scripts/figure_text_audit.py $RUN/live/paper/main.pdf
```

Each changed figure's row (width, scale, text sizes) must equal the staged PDF's; page and figure
numbers may move.

## Evidence crops

Crop the same figure from both PDFs for each repaired finding (figure-audit's viewing protocol).
Take page `P` and `rect_pt` from each PDF's own `figure_text_audit.py --json`, since a repair can
move a figure; pixels = points × 300/72:

```bash
pdftoppm -cropbox -r 300 -f P -l P -x X -y Y -W W -H H -png $RUN/baseline.pdf $RUN/<id>-before
pdftoppm -cropbox -r 300 -f P -l P -x X -y Y -W W -H H -png $TREE/paper/main.pdf $RUN/<id>-after
```
