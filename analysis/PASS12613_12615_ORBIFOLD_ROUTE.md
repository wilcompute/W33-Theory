# Passes 12613–12615: why Model A's fragments are light, and the problem that creates

Claude track. Continues `PASS12609_12611_PQ_TESTS.md`. Producer: `analysis/w33_pass12613_to_12615_orbifold_route.py`. Test: `tests/test_w33_pass12613_to_12615.py`.

**Not a theory of everything.** Model A ((3,1,−⅓) + 2×(3,2,⅙) at the PQ scale) needs a reason for its fragments to be light while their SU(5) partners are heavy. That is Di Luzio et al's main objection.

## 12613: no missing partner in 4D SU(5)

`missing_partner_search.py`. Every SU(5) irrep up to dimension 220 is branched into SM pieces from semistandard tableaux. A fragment is protected if its SU(5) partner multiplet R contains conjugates of all the heavy fragments and none of the light one, with a 24, 75 or 200 Higgs in F × R.

**Controls [E]:** 5, 10, 24, 45, 50, 75 reproduce their textbook decompositions. The search finds the standard doublet-triplet missing partner, 50 with 75. (A first run missed it because I wrote the 75 as shape (2,2,1,1) instead of (2,2,1). Fixed.)

**Result [N]:** for Model A's 10 (light (3,2,⅙)) and 5 (light (3,1,−⅓)), **no representation up to dimension 220 qualifies, at the content level alone**, before any Higgs condition. In 4D SU(5) these fragments are as tuned as the Higgs doublet in minimal SU(5). Larger representations and accidental zero Clebsches are not covered.

## 12614: the orbifold gives them exactly

`orbifold_gut.py`. SU(5) on S¹/(ℤ₂×ℤ₂′) (Kawamura; Hall–Nomura), P′ = diag(+,+,+,−,−):

| Bulk field | η′ | Massless fragment | at 1/R |
|---|---:|---|---|
| 5 | +1 | **(3,1,−⅓)** | (1,2,½) |
| 10 | −1 | **(3,2,⅙)** | (3̄,1,−⅔), (1,1,1) |
| 5_H | −1 | doublet | triplet |

**[E]** Exactly Model A's content, by boundary conditions, the same mechanism that splits the Higgs.

KK unification at one loop, matching at the cutoff Λ, brane kinetic terms neglected. **Control:** ΛR = 1 returns the 4D one-loop result exactly.

| ΛR | M_X | 1/R | 1/α_U | τ, matter on the SU(5) brane |
|---:|---:|---:|---:|---:|
| 1 | 6.6×10⁹ | 8.4×10¹⁵ | 36.8 | 7×10³⁵ |
| 3 | 3.2×10⁹ | 5.5×10¹⁵ | 37.8 | 1.2×10³⁵ |
| 10 | 1.5×10⁹ | 3.2×10¹⁵ | 41.9 | 1.2×10³⁴ |
| 30 | 8.7×10⁸ | 1.8×10¹⁵ | 54.3 | 7×10³² |

These are one loop; in 4D, two-loop running raised M_X about 4 times. With matter on the SM brane, tree-level X exchange is absent and the proton prediction weakens.

## 12615: the problem, from prior art

Agrawal, Nee, Reig, arXiv:2511.21830 (2025), which I read for this: in orbifold GUTs with apparent unification, any axion coupled to photons satisfies g_aγ/m_a at or below the line set by E/N = 8/3. Their argument is that an axion whose couplings to the SM factors are not GUT-related must live on the SM brane. Apparent unification needs the brane kinetic terms small, so the brane gauge couplings are strong and UV brane instantons give it a large potential, V ≈ K l₅⁻⁴ e^(−S), with S = 8π²/g²_brane.

Model A's E/N = ⅔ gives |E/N − 1.92| = 1.25, above the 0.75 of E/N = 8/3. **So the orbifold that explains Model A's fragments also puts its axion in conflict with their bound.** The PQ solution needs the extra potential below about 10⁻¹⁰ χ_QCD, about 3×10⁻¹⁵ GeV⁴. With l₅⁻¹ ≈ 5×10¹⁵ GeV that requires K e^(−S) ≲ 10⁻⁷⁷.

My rough estimate, not a calculation: SM fermion zero modes on an SU(2) brane instanton closed by Yukawa loops give K ~ 10⁻⁴⁸. That would need S ≳ 68, i.e. brane α⁻¹ ≳ 11, against a unified 1/α ≈ 38. Brane terms that large must then be universal to about 10 percent to keep unification. That is a tuning condition, not a refutation. Their paper treats chiral suppression only from added brane fermions, as I read it, so the SM-zero-mode estimate is mine and unchecked.

**Outcomes, stated plainly:**
- If an axion is found with E/N = ⅔, it contradicts orbifold GUTs with apparent unification by their result, but not Model A in 4D with tuned splitting.
- Model A has no natural fragment splitting in 4D SU(5) up to dimension 220, and the natural orbifold splitting meets this axion-quality condition.

## Sources

arXiv:2511.21830, hep-ph/9902423 (Kawamura), hep-ph/0103125 (Hall–Nomura), hep-ph/0112094, 1705.05370. Missing partner: Masiero, Nanopoulos, Tamvakis, Yanagida 1982 (from memory, not re-read).
