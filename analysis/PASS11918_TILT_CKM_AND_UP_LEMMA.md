# Pass 11918: the frame tilt gives a realistic down-quark mass but not the CKM — an exact up-sector selection rule of magnetized SU(5)

Producer: `analysis/w33_pass11918_tilt_ckm_and_up_lemma.py`
Sampler: `analysis/w33_pass11918_hypercharge_wilson_scan.py`
Certificates:
* `data/w33_pass11918_tilt_ckm_and_up_lemma.json`
* `data/w33_pass11918_tilt_scan_frozen.json`

Regression: `tests/test_w33_pass11918.py`
Track: Claude. Route 1 of the plan after Pass 11917: the CKM from the tilt.

## 1. The up lemma, and a correction

**Setup.** In SU(5), Q, u^c and e^c sit on one brane (the 10).

**Lemma.** A single-Higgs-mode 10·10 Yukawa is **monomial**.
* Its support is the permutation matrix of the involution a ↦ c − a on ℤ₃, which has exactly one fixed point.
* This holds for every modulus and every Wilson line.
* Checked on all 12 det-3 fluxes, with and without a hypercharge Wilson line.

**Consequence with a common Wilson line.** If SU(5) is unbroken, the two entries of the 2-cycle are equal, by theta
evenness. So the up spectrum **always has a degenerate pair** (to 3·10⁻¹⁵). This is the matrix-flux form of the corpus's
charm–up lock (Passes 11903 and 11905).

**Correction.** The CKM samples of Pass 11915 (`ckm_wl.py`) and the GST test of Pass 11916 were not SU(5)-consistent.
They gave Q and u^c independent Wilson lines, with no source for the difference.

## 2. The consistent source: a hypercharge Wilson line

**The model.** SU(5) → SM is broken by a hypercharge Wilson line w, a flat direction in the Hosotani sense. Each field
sits at

  ζ_X = ζ_rep + Y_X N_rep⁻¹ w,

with hypercharges Q 1/6, u^c −2/3, e^c 1, d^c 1/3, L −1/2.

**What w does.**
* **It lifts the up degeneracy:** the minimum gap is 6·10⁻⁴ over the 12 fluxes.
* **The up Yukawa stays monomial.** So the up mass basis is **exactly** the magnetic-translation basis of the 10. The
  CKM is then just the down sector's left rotation in that basis.
* **The H_d position is consistent:** N₁₀(ζ_e − ζ_Q) + N₅(ζ_L − ζ_d) = (5/6)w − (5/6)w = 0.
* **The lepton Yukawa equals the down Yukawa at a shifted relative Wilson line.** The shift is the scalar (5m/18)w, and
  this was checked on the spectra. So down and lepton spectra have identical distributions, and there is no
  Georgi–Jarlskog factor (the median of (m_μ/m_τ)/(m_s/m_b) is 0.98).

## 3. The tilt model scanned

**Scope.** The model is the (1,1,4) pair, with
* 279 random compatible moduli;
* random 10, 5̄ and hypercharge Wilson lines;
* all 25 × 12 down and up Higgs modes;
* 83 700 rows in total.

**Results.**

| question | result |
|---|---|
| does the tilt make m_d/m_s realistic? | **yes**: m_d/m_s > 0.01 in 17% of rows; 90th percentile 0.047 |
| does Gatto–Sartori–Tonin emerge? | **no**: corr(log V_us, log √(m_d/m_s)) = 0.11 over 14 595 hierarchical rows; median V_us/√(m_d/m_s) = 0.065 |
| what does the CKM look like? | 82% of rows near-permutation (an off-diagonal entry > 0.9); of the 12 712 aligned rows, 87% have V_cb = 0 exactly |
| realistic quark masses and CKM together? | **0 of 222** rows with m_s/m_b, m_u/m_c, m_c/m_t within ×3 have a hierarchical CKM with all three angles nonzero |

**Numerical note.** The 11915 module truncates the theta series at |n_i| ≤ 4. That is accurate to about 10⁻⁷ of the
largest singular value at large Wilson-line offsets. The frozen scans use it, and are reproducible bit for bit. Exact
zeros are certified with |n_i| ≤ 7 (Pass 11920).

## Reading

**What works.** The tilt solves the first-generation mass *size* problem: m_d/m_s ≈ 0.05 is generic.

**What does not.** It does not solve flavour mixing, and the obstruction is exact. The single-mode up Yukawa is monomial,
so the up basis is pinned to the magnetic-translation basis. The down rotation in that basis is unrelated to the down
masses.

**The way out.** The up sector must be non-monomial, i.e. its Higgs must be a superposition of modes. That is the
fourth time the corpus lands on the Higgs profile as the flavour lever (Passes 11914, 11915, 11916, 11918).

## Prior art

* Abe–Choi–Kobayashi–Ohki 2010 (arXiv:1001.1788): magnetized flavour with Wilson lines.
* Choi et al. 2009 (arXiv:0908.0395): GUT-breaking Wilson lines deform the GUT flavour structure.
* Hosotani: Wilson-line symmetry breaking.
* Corpus: Passes 11903, 11905, 11914–11917.
