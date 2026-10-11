# Pass 11902: across all 104 A8 SO(16)×SO(16) Standard Models, no Kähler modulus lifts the up-sector degeneracy

Producer: `analysis/w33_pass11902_a8_census_kahler_independent_degeneracy.py`
Frozen scan: `data/w33_pass11902_census_frozen.json`. Rescan with the Pass 11095 dumps: WSL
`~/orb/p1109x/a8/a8_sm_all_our_m0_v2.dump`, `a8_sm_all_theirs.dump`.
Certificate: `data/w33_pass11902_a8_census_kahler_independent_degeneracy.json`
Regression: `tests/test_w33_pass11902.py`
Track: Claude.

## Result

The quark doublets of the 104 models come in exactly two kinds.

| kind | models | renormalisable up sector | Kähler-moduli dependence |
|---|---|---|---|
| untwisted Q (families = the three planes) | **73** | every coupling, for all 219 Higgs rows, is the E₈ cubic g ε_ijk: antisymmetric, spectrum **(1, 1, 0)**, so top = charm and m_u = 0 | none: the untwisted matter metric (T + T†)⁻¹ normalises by congruence A M Aᵀ, which preserves antisymmetry. Checked for random Hermitian T to 10⁻¹⁵; a non-antisymmetric control moves |
| Q at the three fixed points of one Wilson-line-free torus | **31** | every up triangle is single-pointed on both Wilson-line tori, giving **m_c = m_u** | none: equal by θ evenness for all nine moduli (Pass 11901) |

Only one model, **56**, has down-sector triangles that are not single-pointed on its Wilson-line tori: (0,1,1) and
(1,1,1). Only there could the off-diagonal Kähler moduli split m_s from m_d, and the price would be a bottom suppressed
on both tori.

## Reading

In this class the up-quark hierarchy cannot come from any Kähler modulus at the renormalisable level. That includes
the off-diagonal moduli that carry the W(3,3) structure (Passes 11897–11900).

This extends three corpus results:
* Pass 11103 (scalar-vacuum alignments);
* Pass 11108 (untwisted ×3 gives top = charm);
* Pass 11109 (diagonal moduli).

The remaining levers are non-renormalisable couplings with a reflection-breaking vacuum (closed for the up sector by
Pass 11103), non-perturbative effects, Higgs mixing across family-torus points (the Hesse states of Pass 11114), or a
different model class. For a different class, the Pass 11901 criterion applies: a quark triangle that is not
single-pointed on a Wilson-line torus.

## Not established

* **Scope.** Renormalisable couplings only.
* **Which Higgs stays light.** Every Higgs row is examined individually; the light-Higgs mixing matrix is not computed.
* **Untwisted metric.** The untwisted matter metric is taken in the standard form (T + T†)⁻¹, common to Q and u^c, as
  for untwisted fields of one E₈.

## Prior art

* Corpus: 11095 (scan), 11098 (ε textures), 11103, 11105, 11108, 11109, 11114, 11900, 11901.
* Ferrara–Lüst–Shapere–Theisen; hep-th/9204040: the untwisted Z3 Kähler potential, −log det(T + T† − C C†).
