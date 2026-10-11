# Pass 11908: the split-10 scan beyond A8 — the local-10 lock holds in every ℤ₃ shift class (0/600)

Producer: `analysis/w33_pass11908_split_ten_scan_beyond_a8.py`
Frozen census: `data/w33_pass11908_split10_census_frozen.json`
Model definitions (provenance): `data/w33_pass11908_model_definitions.json`
Scan inputs: `analysis/orbifolder_n0_drivers/split10_bases/base_*.txt` and `split10_v0enum.py`
Regression: `tests/test_w33_pass11908.py`
Track: Claude.

## Question

Pass 11903 found the up-quark lock in all 491 A8 SO(16)² models: Q, u^c and e^c sit at one Wilson-line point (a local
SU(5) 10). That forces the up Higgs to the same point, so m_c = m_u for every Kähler modulus. Does the lock persist
beyond the A8 Kac shift?

## Scan

**Shift classes.** Three further ℤ₃ shift classes V₁ of the SO(16)×SO(16) (ℤ₂W×ℤ₃) string:
* E₆×SU(3) × E₈ (the standard embedding);
* E₆×SU(3) × E₆×SU(3);
* E₇×U(1) × SO(14)×U(1).

**Witten shifts.** All admissible Witten shifts V₀ were enumerated: 894,240, 804,006 and 1,020,852 respectively. One per
4D gauge group was kept, giving 9 bases. Three of them do not load (orbifold group ill-defined).

**Draws.** 20,000 random Wilson-line draws on each loadable base gave **109 inequivalent SM-like, tachyon-free
models**.

**Dumps.** Produced with the byte-verified pipeline of Pass 11903 (levdump2 + nsosm).

## Results (109 new models)

| class (local gauge groups) | untwisted | twisted (all with local 10) |
|---|---|---|
| E₆SU₃ × E₈ (D₅A₂ \| D₈) | 1 | 66 |
| E₆SU₃ × E₈ (A₅A₁A₁ \| D₈) | 0 | 1 |
| E₆SU₃ × E₆SU₃ (D₅A₂ \| A₅A₁A₁) | 4 | 0 |
| E₆SU₃ × E₆SU₃ (A₅A₁A₁ \| A₅A₁A₁) | 23 | 0 |
| E₇U₁ × SO₁₄U₁ (D₆A₁ \| D₄A₃) | 6 | 2 |
| E₇U₁ × SO₁₄U₁ (A₇ \| A₆) | 2 | 4 |

* **Twisted families: all 73 carry a complete local 10.**
* **Untwisted families:** in all 36, every up coupling (105 Higgs rows) is the antisymmetric E₈ cubic, so top = charm.
* **Up-sector escape: 0/109.** Down-sector escape: 9/109.

**Combined with Pass 11903: 0/600 models in four ℤ₃ shift classes** can split charm from up through any Kähler modulus
at tree level. In these scans the local 10 is universal.

## Provenance

The parallel track's TOE48 reported that the 491 models' gauge shifts and Wilson lines were absent from the frozen
corpus. They are now frozen. `data/w33_pass11908_model_definitions.json` holds the shift and Wilson-line rows of all 600
models (V₀, V₁, W₁…W₆, and the space group), together with the SHA-256 of each source file:

| source file | contents | SHA-256 prefix |
|---|---|---|
| `a8_sm_all.txt` | the 104 of Pass 11095 | 9ed6c9ad… |
| rescan `r_*_SM.txt` | the 387 of Pass 11108 | 4dfe22e7… |
| split-10 output | the 109 here | 0de82043… |

## Reading

In heterotic ℤ₃ orbifolds of the SO(16)² string, the up-quark hierarchy cannot be a tree-level Kähler effect in any of
the four shift classes scanned. The magnetized home (Passes 11904–11907) remains the place where the W(3,3) structure
can carry it.

## Not established

* **Scope.** Only the SO(16)×SO(16) ℤ₂W×ℤ₃ string, and one V₀ per gauge group.
* **Supersymmetric case.** The supersymmetric E₈×E₈ ℤ₃ orbifolds, where the literature has MSSM-like models, are not
  scanned here.
* **Why universal.** Why the local 10 appears in every model is observed, not proved.

## Prior art

* Corpus: 11095, 11108, 11903.
* TOE48 (provenance).
* Ibáñez–Kim–Nilles–Quevedo: three generations in ℤ₃.
* Local grand unification: Buchmüller–Hamaguchi–Lebedev–Ratz.
