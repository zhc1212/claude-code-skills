# Audit Output Format

The Audit shape (SKILL.md, Output Format). The Rewrite shape does not use this file.

## Template

```
¶ [section / heading]

Section role: [section type, structure] — this ¶ serves as [role]. [OK / BLOCKING: role mismatch]
Strengths: [what works well]

Sentence ledger:
| S | Job in the ¶ (relation to S1) | Info | → next: relation; linking words | Wording |
|---|---|---|---|---|
| S1 | [what this sentence does for the ¶'s message, in plain words; S2 onward add the Check 2 label of its relation to S1] | [+new / =echo / ~filler] | [relation; "phrase" that links] | [gap N words; stress; referent; premise; wording / OK] |
| ... | | | | |

 1. Sentence level: largest subject→verb gap S_ ("[head]" … "[verb]", N words); [OK / MINOR (F_) at S_] — rows in ledger
 2. Transitions: [OK / MAJOR (F_) at S_→S_] — pairs in ledger
3a. Structure:  organization: [claim→support / progressive / parallel / setup→derivation]; S1 message: "[quote]"; last sentence: [advances / MAJOR: empty]; [OK / MAJOR: S_ off-topic]
3b. Density:    [OK / MAJOR (F_): S_ echo/filler] — tags in ledger
 4. ¶ bridge:   [relation to previous ¶ / skipped (no adjacent ¶)] [OK / MAJOR]
5a. Consistency: within view: [OK / MINOR (F_)]; cross-section: [OK / skipped (single ¶, no other section) / MAJOR: terminology drift]
5b. First use:  [TERM → spelled out / defined in §_ / never / skipped (no other part of the paper)]
5c. Placement:  [OK / S_ belongs in {Experiments/Setup/...} / S_ repeats §_]
 6. De-AI:      [PASS / MINOR: isolated hits / MAJOR: hits cluster in one sentence]; baseline: [type and file / none]; findings: ["phrase" (family), …]; dismissed: ["phrase" — reason, …]
 7. Section:    [OK / MAJOR: ...]
 8. Claims:     [OK / MAJOR: "X" unsupported / scope missing / boundary "Y" defensive]
 9. Formulas:   [OK / skipped / BLOCKING: symbol X undefined]

F1 [BLOCKING / MAJOR / MINOR] (Checks _, _): [the defect, one line]
   [Original / Revised / Why, for Blocking and Major]
F2 ...

Finding summary: N Blocking / N Major / N Minor

Added facts: [none / each statement a Revised text adds]
```


## Sentence ledger

The ledger carries the per-sentence content of Checks 1, 2, 3a Step B, and
3b, one row per sentence and the last row's link pointing to the next ¶ or
"—". Lines 1, 2, 3a, and 3b then give one-line verdicts that cite rows and
F-numbers ("see ledger; MAJOR (F2) at S2→S3") instead of repeating the rows;
3a still names the organization and quotes the S1 message.

## Labels

In the Audit shape, emit every labelled line of the template verbatim,
including 3a–3b, 5a–5c, and `Added facts:`, each on its own line, with the
colon immediately after the label. A skipped line still appears, with its
reason. Put commentary after the colon, never between label and colon; the
labels are parsed by downstream tooling.

Severity labels BLOCKING/MAJOR/MINOR are valid in any check line; the bracketed
options in the template are examples, not exhaustive.

## F-line contents

Under each Blocking or Major F-line, provide:
- **Original**: the problematic text
- **Revised**: the replacement, built as Procedure step 3 says
- **Why**: one-sentence reasoning
