"""Checks for audit_style.py. Run: python3 scripts/test_audit_style.py (stdlib only)."""
import os, sys, unittest
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from audit_style import allowance, features, new_words, protected, protected_diff

def counts(text):
    return features(text)["counts"]

class Masking(unittest.TestCase):
    def test_comments_math_and_keys_are_not_prose(self):
        f = features("We fit the model~\\cite{smith24} on $x---y$ data. % a note---here\n"
                     "\\begin{equation} a: b; c \\end{equation}\nThe loss is small.")
        self.assertEqual(f["counts"]["em dash"], 0)
        self.assertEqual(f["counts"]["elab colon"], 0)
        self.assertEqual(f["counts"]["semicolon (clause)"], 0)
        self.assertEqual(f["words"], 11)  # We fit the model on SYM data The loss is small

    def test_em_dash_in_prose_counts(self):
        self.assertEqual(counts("The cache---rebuilt nightly---is small. It is — as expected — fast.")["em dash"], 4)

    def test_plain_text_percent_is_not_a_comment(self):
        f = features("The method improves speed by 7.7% over the baseline on every run. However, it uses more memory.")
        self.assertEqual((f["sentences"], f["counts"]["conn initial"]), (2, 1))
        self.assertEqual(protected("It gains 7.7% over the baseline.")[("number", "7.7")], 1)

    def test_run_in_heading_is_not_a_sentence(self):
        f = features("\\textbf{Hardware-aware optimization surface.} A full unitary has many entries for each qubit.")
        self.assertEqual(f["sentences"], 1)

class Colons(unittest.TestCase):
    def test_elaborating_colon(self):
        self.assertEqual(counts("The two losses are coupled: lowering one raises the other.")["elab colon"], 1)

    def test_label_list_and_display_colons(self):
        text = ("Stage 1: we train the model once. Our contributions are as follows: \\begin{itemize} "
                "\\item A new loss. \\end{itemize} The checker requires the following:\n"
                "\\begin{equation} U = V \\end{equation}")
        self.assertEqual(counts(text)["elab colon"], 0)

class Semicolons(unittest.TestCase):
    def test_clause_semicolon_counts_and_list_semicolon_does_not(self):
        self.assertEqual(counts("The cache is rebuilt after each change; stale entries are never served.")["semicolon (clause)"], 1)
        self.assertEqual(counts("We test three settings: small, fast; large, slow; and mixed, medium.")["semicolon (clause)"], 0)
        self.assertEqual(counts("We test three settings: small, fast; large, slow; and mixed, medium.")["elab colon"], 0)

    def test_colon_then_clause_semicolon_is_not_a_list(self):
        c = counts("The two losses are coupled: lowering one raises the other; the gap stays.")
        self.assertEqual((c["elab colon"], c["semicolon (clause)"]), (1, 1))

class TailsAndConnectives(unittest.TestCase):
    def test_tails(self):
        c = counts("The profiler runs once per build, so its cost is shared. We keep the loss, which is stable, "
                   "rather than the old one. We prune layers, rather than heads.")
        self.assertEqual(c["tail"], 4)

    def test_initial_and_mid_connectives(self):
        c = counts("However, the loss rises. Instead of pruning, we merge heads. Together with the cache, it is fast. "
                   "Additionally, we test it. The loss thus falls quickly.")
        self.assertEqual(c["conn initial"], 2)
        self.assertEqual(c["conn mid (step 6)"], 1)

class Sentences(unittest.TestCase):
    def test_fragments_and_abbreviations(self):
        f = features("\\textbf{Setup.} We follow prior work, e.g. the ASVD setup, for all runs. "
                     "Results are in Fig. 2 and match the earlier report closely.")
        self.assertEqual(f["sentences"], 2)
        self.assertEqual(f["short"], 2)

class Allowance(unittest.TestCase):
    def test_skill_example(self):
        # 2.0 colons per 1,000 words allow one colon in a 355-word passage.
        self.assertEqual(allowance(2, 1000, 355), 1)
        self.assertEqual(allowance(0, 1000, 355), 0)
        self.assertEqual(allowance(3, 1000, 1000), 3)

class Compare(unittest.TestCase):
    SRC = "We leverage the tuning of $\\alpha$ from 42.1 to 19.3~\\cite{a,b} (see Table~\\ref{t})."

    def test_protected_spans_equal_when_only_words_change(self):
        rw = "We use the tuning of $\\alpha$ from 42.1 to 19.3~\\cite{a,b} (see Table~\\ref{t})."
        self.assertEqual(protected_diff(protected(self.SRC), protected(rw)), [])

    def test_lost_number_citation_and_math_are_reported(self):
        rw = "We use the tuning of $\\beta$ from 42 to 19.3~\\cite{a} (see Table~\\ref{t})."
        diff = {(kind, value) for kind, value, _, _ in protected_diff(protected(self.SRC), protected(rw))}
        self.assertEqual(diff, {("number", "42.1"), ("number", "42"), ("cite", "b"),
                                ("math", "\\alpha"), ("math", "\\beta")})

    def test_new_words_ignore_form_changes(self):
        rw = "We use the tuned $\\alpha$ from 42.1 to 19.3 for long inputs~\\cite{a,b}."
        flagged = {w for w, _ in new_words(self.SRC, rw)}
        self.assertEqual(flagged, {"use", "long", "inputs"})

    def test_past_tense_is_a_form_change(self):
        self.assertEqual(new_words("We use the cache.", "We used the cache."), [])

    def test_earlier_version_counts_as_source(self):
        rw = "We use the tuned $\\alpha$ from 42.1 to 19.3."
        self.assertEqual({w for w, _ in new_words(self.SRC, rw, earlier="We use it.")}, set())

if __name__ == "__main__":
    unittest.main()
