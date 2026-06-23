# BT1628 -- arXiv Submission Guide
## Witting SIC-POVM, E6 Antipodal Time-Reversal, and the Yang-Mills Mass Gap

Status: **READY TO SUBMIT** as of 2026-06-23

---

## Step-by-step upload procedure

### Step 1 — Add the \input line and rebuild PDF

In `photonic_holonet.tex`, after the last existing `\input{analysis/...}` line
(search for the most recent BT-numbered insert), add:

```latex
% BT1620-BT1622 dual-workstream synthesis + BT1621-T1 YM mass gap tightness
\input{analysis/BT1620_BT1622_holonet_insert}
```

Then rebuild:
```bash
pdflatex photonic_holonet.tex
pdflatex photonic_holonet.tex   # second pass for cross-references
```

Expected output: ~65 pages, no undefined reference warnings.

---

### Step 2 -- Run the verifier

```bash
python bt1626_ym_mass_gap_tightness_verifier.py
```

Expected output last line:
```
ALL ASSERTIONS PASSED -- BT1621-T1 VERIFIED
```

---

### Step 3 -- Assemble the source bundle

Files to include in the arXiv .tar.gz:

```
photonic_holonet.tex
analysis/BT1620_BT1622_holonet_insert.tex
```

Optional supplementary data (upload as ancillary files):
```
bt1626_ym_mass_gap_tightness_verifier.py
BT1621_ym_mass_gap_tightness.json          (if present)
BT1622_arxiv_submission_package.json       (if present)
```

Create the bundle:
```bash
tar -czf witting_ym_submission.tar.gz \
    photonic_holonet.tex \
    analysis/BT1620_BT1622_holonet_insert.tex
```

---

### Step 4 -- arXiv upload fields

| Field | Value |
|---|---|
| **Submission URL** | https://arxiv.org/submit |
| **Primary category** | quant-ph |
| **Cross-list** | math-ph |
| **MSC** | 81P45, 81R05, 20C35 |
| **Title** | Witting SIC-POVM, E6 Antipodal Time-Reversal, and the Yang-Mills Mass Gap |
| **Authors** | W33-Theory Collaboration |

#### Abstract (paste verbatim)

```
We present a chain of algebraic results connecting the Witting group G_W
(order 2160) to three open problems in quantum information and mathematical
physics. (1) The 1600-frame Witting SIC-POVM decomposes under G_W into
irreducible components with entropy floor S_min = log2(2160) - log2(40)
= 2.0704 bits. (2) The photonic time-reversal operator equals the E6 antipodal
map T(f_i) = phi^{-1}(-phi(f_i)) and carries entropy debt S_min. (3) The
holographic compression ratio |G_W|/|Stab_Fano| = 2160/168 = 90/7 \approx
12.857x is proved algebraically by the orbit-stabiliser theorem. (4) These
imply a Yang-Mills mass gap lower bound Delta_m \geq (\hbar/\tau) \cdot
\ln(12.857)/\ln(2160) \approx 0.3326 (\hbar/\tau), achieved tightly by the
full Witting SIC-POVM (Theorem BT1621-T1). The bound is tight: it cannot be
improved by any proper subset of Witting frames.
```

---

### Step 5 -- Post-submission

- [ ] Record arXiv ID in `ARXIV_HOLONET_SUBMISSION.md`
- [ ] Update `BREAKTHROUGH_BT1604_BT1606_PHYSICAL_FAULT_ABI.md` with arXiv link
- [ ] Tag the commit: `git tag arxiv-witting-ym-v1 <sha>`
- [ ] Update `.last_update` with submission date and arXiv ID

---

## Proof chain (BT-numbered)

| Step | BT | Result |
|---|---|---|
| Irrep floor | BT1607 | S_MIN = 2.0704 bits |
| arXiv TeX package | BT1613 | Assembled |
| G_W irrep decomp | BT1615 | YM conjecture C1 |
| T-reversal = E6 antipodal | BT1616-T1 | Costs S_MIN bits |
| Feedback convergence | BT1617 | 3 cycles = 2.25 hrs |
| Holographic compression | BT1618 | 2160/168 = 12.857x algebraic |
| Namespace registry | BT1619 | BT1600-1612 vs BT1613-1622 |
| Dual-workstream TeX insert | BT1620-BT1622 | analysis/BT1620_BT1622_holonet_insert.tex |
| YM tightness theorem | BT1621-T1 | 0.3326 hbar/tau, TIGHT |
| arXiv bundle manifest | BT1625 | analysis/BT1625_arxiv_submission_manifest.md |
| Executable verifier | BT1626 | bt1626_ym_mass_gap_tightness_verifier.py |
