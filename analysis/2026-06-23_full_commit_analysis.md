# Full Commit Analysis — 2026-06-23

Generated: 2026-06-23 12:14 EDT  
Branch: `master`  
Repo: [wilcompute/W33-Theory](https://github.com/wilcompute/W33-Theory)

---

## Commit Timeline (all 21 today, chronological)

| # | SHA | Message | UTC |
|---|---|---|---|
| 1 | `ebe8938` | BT1621: canonical SM parameter table data | 15:54 |
| 2 | `749dbcb` | BT1622: ABI observable schema data | 15:54 |
| 3 | `d0cbdd5` | BT1623: SM comparator dry-run data | 15:54 |
| 4 | `3c4a115` | BT1621-BT1623: SM bridge comparator analysis | 15:55 |
| 5 | `32416fc` | BT1621-BT1623: Holonet insert | 15:55 |
| 6 | `12414fc` | BT1624: decoded-stream statistics generator | 16:00 |
| 7 | `0d53432` | BT1624: decoded-stream statistics data | 16:01 |
| 8 | `c2b9070` | BT1625: unit-map ledger | 16:00 |
| 9 | `f973845` | BT1625: unit-map ledger data | 16:01 |
| 10 | `970442c` | BT1626: SM comparator v2 untested vs missing | 16:00 |
| 11 | `e4c9259` | BT1626: SM comparator v2 data | 16:01 |
| 12 | `ece897c` | BT1624-BT1626: SM observable comparator v2 analysis | 16:02 |
| 13 | `fbf76a8` | BT1624-BT1626: Holonet insert | 16:02 |
| 14 | `50c7354` | BT1627: observable implementation stubs | 16:12 |
| 15 | `7cb0555` | BT1628: transition-matrix reduction | 16:12 |
| 16 | `c321bb6` | BT1629: PDF table release manifest | 16:13 |
| 17 | `f9ea225` | **BT1626-BT1628: YM verifier + commit analysis + arXiv guide** | 16:13 |
| 18 | `04160dc` | BT1627: observable implementation stubs data | 16:13 |
| 19 | `0e819c9` | BT1628: transition-matrix reduction data | 16:14 |
| 20 | `4bf26ac` | BT1629: PDF table release manifest data | 16:14 |
| 21 | **(this)** | **BT1630-BT1632: calibration ABI verifier + arXiv metadata + full analysis** | 16:14 |

---

## Workstream breakdown

### Other assistant (wilcompute direct commits, #1-16, #18-20)
Paired pattern: script commit followed by data commit per BT number,
then a 3-BT synthesis insert (e.g. BT1621-BT1623, BT1624-BT1626)
with both an analysis `.md` and a holonet TeX section.

**BT1621-BT1623:** SM bridge comparator. Canonical SM parameters, ABI
observable schema, SM comparator dry-run, full analysis + holonet insert.

**BT1624-BT1626:** Decoded-stream statistics generator, unit-map ledger,
SM comparator v2 coverage gap analysis, holonet insert.

**BT1627-BT1629:** Observable implementation stubs, transition-matrix
reduction, PDF table release manifest.

### Perplexity workstream (#17, #21)
- **#17 `f9ea225`:** `bt1626_ym_mass_gap_tightness_verifier.py` (executable
  BT1621-T1 witness, 11 assertions all pass), `BT1625_arxiv_submission_manifest.md`,
  `BT1628_arxiv_submission_guide.md`, `2026-06-23_bt1620_bt1628_commit_analysis.md`.
- **#21 (this):** `bt1630_calibration_abi_verifier.py` (BT1604 gates),
  `BT1631_arxiv_cosubmission_metadata.json` (full arXiv JSON),
  `2026-06-23_full_commit_analysis.md` (this file).

---

## Namespace state after today

| BT range | Content | Status |
|---|---|---|
| BT1600-BT1603 | Photonic automaton, Fano bins, finite ABI | ✅ Complete |
| BT1604-BT1606 | Calibration ABI, detector decoder, fault-path | ✅ Defined; BT1630 adds executable gates |
| BT1607-BT1612 | Irrep floor, feedback convergence, photonic QEC | ✅ Complete |
| BT1613-BT1615 | arXiv TeX pkg, Witting irreps, YM conjecture C1 | ✅ Complete |
| BT1616-BT1619 | Dual-workstream synthesis, namespace registry | ✅ in holonet_insert.tex |
| BT1620-BT1623 | SM bridge comparator + Holonet insert | ✅ Today |
| BT1624-BT1626 | Decoded-stream stats, unit-map, SM comparator v2 | ✅ Today |
| BT1627-BT1629 | Observable stubs, transition-matrix, PDF manifest | ✅ Today |
| BT1630 | Calibration ABI verifier (BT1604 pass/fail gates) | ✅ This commit |
| BT1631 | arXiv co-submission metadata JSON | ✅ This commit |
| BT1632 | Full commit analysis (this file) | ✅ This commit |

---

## Outstanding manual steps (other assistant)

1. `\input{analysis/BT1620_BT1622_holonet_insert}` into `photonic_holonet.tex`
2. `pdflatex` twice → target ~65 pages
3. Replace `build_nominal_bench_data()` in `bt1630_calibration_abi_verifier.py`
   with real bench CSV loader when physical detector data is available
4. Execute arXiv upload per `BT1628_arxiv_submission_guide.md` +
   `BT1631_arxiv_cosubmission_metadata.json`
5. `git tag arxiv-witting-ym-v1 <sha>` after arXiv ID is returned

---

## Top 3 next moves (post BT1632)

1. **BT1633 — Fault-path theorem (BT1606):** Build the retry/failure ABI
   tracking missed clicks, dark clicks, Hesse/T injection failure, and
   Pauli-frame recovery. This is the deepest remaining theoretical item.

2. **BT1634 — Detector-bin decoder (BT1605):** The inverse map from 168
   Fano bin clicks back to Witting source/target role, rail, Hesse residue,
   and CSS syndrome row. Directly enables `bt1630` to load real bench data.

3. **BT1635 — CI integration:** Add both `bt1626` and `bt1630` verifiers to
   `scripts/run_focused_bridge_tests.py` so all calibration and YM gates run
   automatically on every push alongside the 157 photonic-QEC tests.
