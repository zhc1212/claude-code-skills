---
name: citation-verification
description: Verify academic citations for correctness — detect fabricated references, metadata errors, claim-citation mismatches, and retracted papers. Use before submission or after AI-assisted writing. Triggers on "检查引用", "verify citations", "citation check", "引用核验", "check references", "cite verify".
---

# Citation Verification Workflow

AI language models frequently fabricate ("hallucinate") citations. Every AI-generated reference must be verified before inclusion in a manuscript.

**Rule: Never trust an AI-generated citation without independent verification.**

## Common AI Citation Fabrication Patterns

| Pattern | Example | Detection |
|---------|---------|-----------|
| **Plausible but nonexistent paper** | Real author + real journal + fabricated title | Search by title |
| **Wrong author combination** | Author A's topic + Author B's name | Verify author list |
| **Incorrect year** | Correct paper but wrong publication year | Cross-check with DOI |
| **Fabricated DOI** | DOI format correct but resolves to nothing | Check doi.org |
| **Journal mismatch** | Real paper published in different journal | Verify journal name |
| **Volume/page errors** | Correct paper but wrong bibliographic details | Check against database |
| **Merged citations** | Elements from 2+ real papers combined | Search each element separately |
| **Retracted papers cited as valid** | Paper exists but was retracted | Check Retraction Watch |
| **Preprint cited as published** | On arXiv/medRxiv but not peer-reviewed | Verify publication status |
| **Outdated version cited** | Guideline or meta-analysis updated | Check for latest version |

## Step-by-Step Verification

### Step 1: Title Search (Primary)

Search the exact title in multiple databases:

- **PubMed**: `https://pubmed.ncbi.nlm.nih.gov/` — use quotes for exact match
- **Google Scholar**: `allintitle: [key words]` — discovery only, not authoritative
- **Semantic Scholar**: `https://www.semanticscholar.org/` — good for CS/AI papers

**If title not found**: The paper likely does not exist. Do NOT proceed to use it.

### Step 2: DOI Verification

```bash
# Direct resolution
https://doi.org/[DOI]

# CrossRef API lookup
curl -s "https://api.crossref.org/works/[DOI]" | python -m json.tool
```

**Check**: Does the resolved page match the claimed title, authors, and journal?

### Step 3: Author Verification

- PubMed author search: `[LastName FirstInitial][au]`
- ORCID lookup: `https://orcid.org/[ORCID-ID]`
- Google Scholar author profile

**Check**: Has this author actually published in this topic area?

### Step 4: Journal Verification

- NLM Catalog: `https://www.ncbi.nlm.nih.gov/nlmcatalog/`
- Check journal website table of contents for the specific volume/issue

### Step 5: Content Verification (Critical)

Even if the paper exists, verify:
- [ ] The claims attributed to the paper are actually in the paper
- [ ] The data/statistics cited match what the paper reports
- [ ] The conclusions drawn are consistent with the paper's actual findings
- [ ] The paper is not being cited out of context

## Batch Verification

### Phase 1: Rapid Triage (2-3 min per reference)

```
For each reference:
1. Copy exact title → PubMed search (with quotes)
2. Mark as: ✅ Found | ❌ Not found | ⚠️ Partial match
```

### Phase 2: Detail Check

```
For each ✅ Found:
1. Compare: authors, year, journal, volume, pages
2. Verify DOI resolves correctly
3. Mark as: ✅ Verified | ⚠️ Details wrong
```

### Phase 3: Resolution

```
❌ Not found → Find replacement or remove
⚠️ Partial match → Correct bibliographic details
⚠️ Details wrong → Update with correct information
```

### Programmatic Batch Verification

```bash
# CrossRef batch DOI check
while IFS= read -r doi; do
  response=$(curl -s "https://api.crossref.org/works/${doi}" 2>/dev/null)
  status=$(echo "$response" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    title = data['message']['title'][0] if data['message']['title'] else 'NO TITLE'
    print(f'OK: {title}')
except:
    print('FAILED: DOI not found')
" 2>/dev/null)
  echo "${doi} -> ${status}"
done < doi_list.txt
```

```bash
# Semantic Scholar title lookup
curl -s "https://api.semanticscholar.org/graph/v1/paper/search?query=<title>&limit=1&fields=title,authors,year,venue,externalIds" | python -m json.tool
```

```bash
# arXiv metadata
curl -s "http://export.arxiv.org/api/query?id_list=<arxiv-id>" | grep -E "<title>|<author>|<published>"
```

## Handling Specific Scenarios

### Paper Exists but Details Wrong
1. Use PubMed/CrossRef record as authoritative source
2. Update all bibliographic fields
3. Re-check that the paper's content still supports the citation context

### Paper Does Not Exist
1. Search for the topic described in the fabricated title
2. Find a real paper making the same point
3. Read the real paper to confirm it supports the claim
4. Replace the fabricated citation

### Paper Is Retracted
1. Check Retraction Watch: `http://retractiondatabase.org/`
2. Check PubMed for retraction notice
3. **Do NOT cite retracted papers** unless discussing the retraction itself
4. Find alternative supporting evidence

### Preprint Not Yet Published
1. Check if a published version now exists
2. If published: cite published version, not preprint
3. If still preprint: cite as preprint with clear labeling
4. Consider whether the journal accepts preprint citations

### Multiple Versions Exist
- Always cite the most recent/final version
- Note the version/edition if relevant

## Per-Reference Checklist

```
- [ ] Title verified: Found in database
- [ ] Authors verified: Author list matches
- [ ] Year verified: Publication year correct
- [ ] Journal verified: Published in stated journal
- [ ] Volume/Issue/Pages verified: Bibliographic details correct
- [ ] DOI verified: Resolves to correct paper
- [ ] Not retracted: Checked Retraction Watch / PubMed
- [ ] Content verified: Paper actually supports the claim made
- [ ] Citation context accurate: Not cited out of context

Status: ✅ Verified / ⚠️ Needs correction / ❌ Replace
```

## Quick Decision Tree

```
AI generated a citation
├── Search title (exact match)
│   ├── FOUND → Verify all details (author, year, journal, DOI)
│   │   ├── All correct → ✅ Use (check content too)
│   │   ├── Minor errors → ⚠️ Correct from database
│   │   └── Major discrepancies → ⚠️ Re-read paper
│   └── NOT FOUND → Search Google Scholar
│       ├── FOUND → Verify details
│       └── NOT FOUND → ❌ Fabricated → Find real replacement
└── DOI provided?
    └── Resolve at doi.org
        ├── Resolves → Check if matches claimed paper
        └── Does not resolve → ❌ DOI fabricated
```

## Tools Reference

| Tool | URL | Best For |
|------|-----|----------|
| DOI resolver | https://doi.org/ | Canonical resolution |
| CrossRef API | https://api.crossref.org/works/ | Programmatic metadata |
| Semantic Scholar | https://www.semanticscholar.org/ | CS/AI papers, API |
| PubMed | https://pubmed.ncbi.nlm.nih.gov/ | Biomedical literature |
| arXiv | https://arxiv.org/ | Preprints |
| Retraction Watch | http://retractiondatabase.org/ | Retraction checking |
| ORCID | https://orcid.org/ | Author identity |
| NLM Catalog | https://www.ncbi.nlm.nih.gov/nlmcatalog/ | Journal verification |

## Output Format

For each citation, produce:

```
[PASS]  \cite{key} — Author (Year). "Title". Venue.
[WARN]  \cite{key} — Issue description (fixable).
[CHECK] \cite{key} — Claim-support alignment unclear (needs human review).
[FAIL]  \cite{key} — DOI does not resolve / not found. Likely fabricated.
```

---

*Source: [kgraph57/paper-writer-skill](https://github.com/kgraph57/paper-writer-skill) — citation-verification reference guide*
