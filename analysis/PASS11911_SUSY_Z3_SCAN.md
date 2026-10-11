# Pass 11911: supersymmetric E₈×E₈ ℤ₃ orbifolds — no Standard-Model-like vacuum in four shift classes

Producer: `analysis/w33_pass11911_susy_z3_scan.py`
Frozen logs: `data/w33_pass11911_susy_scan_logs.json`
Scan inputs: `analysis/orbifolder_n0_drivers/susy_z3_bases/`
New dumper: `analysis/orbifolder_n0_drivers/smlocdump.cpp`, which prints the SM label, twist, lattice vector and
dimensions of every field; it was compiled against the orbifolder objects in WSL `~/orb/build`.
Regression: `tests/test_w33_pass11911.py`
Track: Claude.

## Question

Does the local-10 lock of Passes 11903 and 11908 also hold in the supersymmetric E₈×E₈ ℤ₃ orbifolds?

## Scan

**Tool.** Orbifolder 1.2.1 random-model scan on T⁶/ℤ₃ (SU(3)³ lattice), with the shifts kept and all six Wilson lines
random. 20,000 draws per class:

| shift class | inequivalent spectra | SM-like |
|---|---|---|
| E₆×SU(3) × E₈ (standard embedding) | 717, saturated (682 → 717 over the last 6,600 draws) | 0 |
| E₆×SU(3) × E₆×SU(3) | 1591 | 0 |
| E₇×U(1) × SO(14)×U(1) | 1902 | 0 |
| SU(9) × SO(14)×U(1) (the W(3,3) A8 Kac shift) | 1986 | 0 |

**Criterion.** "SM-like" means the orbifolder test: the SM gauge group, three net generations, Higgs doublets, and
vector-like exotics. `scan` and `smlocdump` use the same CAnalyseModel test.

**Positive control.** `smlocdump` recognises the known ℤ₆-II Standard Model SM_1_55 (from
`~/orb/build/bhlr_sm_scan.txt`) as SM.

**Earlier corpus scan.** The supersymmetric ℤ₃ A8 scan (WSL `~/orb/scan/z3`: 8 bases × 8,000 draws) also found 0
SM-like models.

## Result

**0 SM-like models in 80,000 draws.** The standard-embedding space is essentially exhausted.

So, by this criterion, the supersymmetric ℤ₃ orbifolds have no Standard-Model-like vacuum, and the local-10 question is
empty there. The programme's three-generation ℤ₃ Standard Models live in the non-supersymmetric SO(16)×SO(16) class
(Passes 11095, 11108, 11908), where the lock holds in all 600 models.

## Not established

* **Coverage.** Only the four shift classes above. Not every ℤ₃ shift class is covered.
* **Other model types.** Three-generation ℤ₃ models with chiral exotics or extra U(1) structure, as studied by
  Ibáñez–Kim–Nilles–Quevedo, Casas–Muñoz and Giedt, are not counted as SM-like by the vector-like-exotics criterion.

## Prior art

* Ibáñez–Kim–Nilles–Quevedo (1987); Casas–Muñoz (1988); Giedt (2001): ℤ₃ three-generation models.
* Orbifolder: Nilles–Ramos-Sánchez–Vaudrevange–Wingerter.
* Corpus: the supersymmetric ℤ₃ A8 scan; 11095; 11108; 11903; 11908.
