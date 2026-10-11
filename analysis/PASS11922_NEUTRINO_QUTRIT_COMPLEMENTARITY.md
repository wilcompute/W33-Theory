# Pass 11922: neutrinos are the qutrit-2 mirror of the up quarks, and CKM and PMNS are marginals of one theta state — but not complementary

Producer: `analysis/w33_pass11922_neutrino_qutrit_complementarity.py`
Certificates:
* `data/w33_pass11922_neutrino_qutrit_complementarity.json`
* `data/w33_pass11922_complementarity_scan_frozen.json`

Regression: `tests/test_w33_pass11922.py`
Track: Claude. Continues Pass 11921: the flux factorises W(3,3) into flavour qutrits, 10 = qutrit 1 and 5̄ = qutrit 2.

## 1. The neutrino mirror

**Setup.** The Weinberg operator L L H_u H_u runs through the L × L channel, with flux 2N₅. Its 3-torsion translation
group is K₅, so it is the qutrit-2 mirror of the up sector.

**What holds.** Checked for all 12 det-3 fluxes:
* **Monomial.** Every single-mode L·L Yukawa is monomial.
* **The Higgs pair is a flavour qutrit.** The top-Yukawa Gram space is exactly 3-dimensional (to 2·10⁻¹⁵ at grid
  G = 16).
  * At G = 10 the degeneracy is only 3·10⁻⁶ for the larger fluxes.
  * That is a grid artefact: G = 14 and 18 give 5·10⁻¹² and 2·10⁻¹⁵.
* **An exactly degenerate pair.** Both L carry the same Wilson line and the same hypercharge. So the 2-cycle entries are
  always equal, and every single-class neutrino mass matrix has an **exactly degenerate pair** (to 7·10⁻¹⁵).
* **The closed form.** In the qutrit space,

    **M_ν(h)_{bb′} = h_{b+b′} g′_{b−b′},  with g′₊ = g′₋,**

  which is automatically symmetric, as a Majorana matrix must be.

**Physical reading.** At leading order, one class gives the pattern (M, m, m). That is a large atmospheric splitting,
with the solar splitting needing a correction such as Higgs-pair mixing across classes. It suits normal ordering with a
quasi-degenerate light pair.

## 2. CKM and PMNS are two marginals of one state

**Two kinds of sector.**

| sector | lives on | structure |
|---|---|---|
| up quarks, neutrinos | one qutrit each | monomial, flavour-qutrit Higgs |
| down quarks, charged leptons | across the factorisation | one two-qutrit theta state |

**The mixing matrices.**
* The CKM is the theta state's qutrit-1 (left) Schmidt basis, read in the up basis.
* The PMNS is the qutrit-2 (right) Schmidt basis of the charged-lepton theta state, read in the neutrino basis.
* In this geometry, quark and lepton mixing are the two marginals of a single two-qutrit state. With SU(5), the charged
  lepton state is the down state at a relative Wilson line shifted by (5m/18)w (Pass 11918).

## 3. Complementarity test: negative

**Hypothesis.** Anisotropy of the modulus between the two qutrit directions localises the 10 and spreads the 5̄. That
would give a small CKM and a large PMNS, the familiar "hierarchical 10 / anarchic 5̄" pattern.

**Setup.**
* The A₂ model, with Ω = it(1 + βJ) plus real parts.
* A hypercharge Wilson line and a radiative H_d.
* 240 moduli.
* Proxy distances: the best-assignment log-distance of each Schmidt basis to |V_CKM| and to |U_PMNS|.

**Results.**

| | value |
|---|---|
| corr(CKM distance, PMNS distance) | **+0.47** (no complementarity) |
| median distances for β ∈ [0.4, 0.85] | CKM 2.04, PMNS 1.02 |
| median distances for β ∈ [−0.85, −0.4] | CKM 2.12, PMNS 3.24 |
| best joint point | t = 1.29, β = 0.81: PMNS distance 0.50, but V_us = 0.38, V_cb = 0.033, V_ub = 0.028 |

* β > 0 does favour PMNS-like lepton mixing, but the quark mixing is then large too.
* The left and right Schmidt bases of the theta state are localised together. Anisotropy alone does not decouple them.

## Reading

**What is new and structural.**
* The flavour sectors of SU(5) on the W(3,3) factorisation split into single-qutrit sectors (up quarks, neutrinos) and
  two-qutrit sectors (down quarks, charged leptons).
* Neutrinos inherit the up sector's monomial selection, and their degenerate pair is exact.
* Both mixing matrices are marginals of one theta state.

**What fails.** The quantitative hope: the mixing pattern is not reproduced. This confirms Pass 11921. The quark-flavour
obstruction lives in the theta state itself, not in which basis it is read in.

## Prior art

* SU(5) "hierarchical 10 / anarchic 5̄": Sato–Yanagida; Altarelli–Feruglio–Masina. That is the target pattern here, not
  a result.
* Corpus: TM₁ from the W(3,3) line stabiliser (Passes 11225, 11230, 11254) is a symmetry route to the PMNS, independent
  of this geometric one. Also Passes 11917–11921.
