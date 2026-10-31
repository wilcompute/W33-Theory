# Passes 12498–12505: three information-physics tests — the constants claims fail a fair null, field-reduced grids are contextual only at two qubits, and the site's Kramers–Wannier temperature has no derivation

Claude track. Producer: `analysis/w33_pass12498_to_12505_information_physics_audits.py`. Drivers in
`analysis/search_drivers_12466`:

- `alphabet_null.py`, `constants_information_audit.py` and `mdl_fair_null.py` (12498);
- `field_reduction_parity.py` and `pauli_rank_sign.py` (12499);
- `w33_plaquette_thermo.py` (12500).

All three ideas treat physics as information: bits gained against bits spent (12498), contextuality as a parity obstruction (12499),
and the code enumerator as a partition function (12500).

**Prior art in the corpus, read before running.** Each pass builds on, and in two places corrects, earlier corpus material:

- `w33_alphabet_pool.py` (Pass 20/21) and `w33_mdl_shortest.py` cover the look-elsewhere and minimum-description analysis.
- Pass 4479 (`PASS4472_4479_*`) already uses a code's weight enumerator as a partition function, with MacWilliams as thermal duality.
- Pass 173 owns the route code [40,15,10] and its enumerator.
- BT1707 summarises the multi-qubit contextuality literature.
- `analysis/w33_doily_mermin.py` has the Mermin–Peres square in the doily.

## 12498: the constants claims, priced in bits

**(a) Random-alphabet control under the corpus's own grammar.** `w33_alphabet_pool.py` prices the look-elsewhere effect of the q = 3
alphabet {2,3,4,7,10,12,13,15,18,24,27,30,40} with a fixed depth-2 grammar. It never varies the alphabet. Run with that same grammar
and the same windows:

- the q = 3 alphabet reaches **1 of 5** headline windows;
- 2,000 random alphabets (13 distinct integers from [2,40]) reach 2.2 on average, and only 7 reach none;
- **99.65% do at least as well** as q = 3, and 73% beat it in bits.

The claimed precision matches (m_p/m_e = 1836, 1/α = 137) are not in that grammar at all, so the tool never actually priced them.

**(b) Per-claim information audit** (PDG/CODATA values; "baseline" is the chance that a number drawn log-uniformly within ±20% lies at
least as close to some integer, or to a fraction with denominator at most the claimed one):

| claim | prediction | tension | bits claimed | baseline | net bits |
|---|---|---|---|---|---|
| m_p/m_e | 1836 | 1.4 × 10⁶ σ | 12.6 | 0.31 | 1.7 |
| 1/α | 137 | 1.7 × 10⁶ σ | 10.9 | 0.07 | 3.8 |
| M_Z | 91 GeV | 89 σ | 7.9 | 0.38 | 1.4 |
| m_H | 125 GeV | **1.8 σ** | 8.3 | 0.40 | 1.3 |
| sin²θ_W | 3/13 | 11 σ | 8.0 | 0.05 | 4.2 |
| α_s | 9/76 | **0.5 σ** | 7.1 | 0.88 | 0.2 |

- **Only m_H and α_s agree with experiment.** The others are approximations, not predictions at experimental precision.
- **The bits mostly vanish.** Of the **54.8** bits the matches nominally claim, **12.6** survive the near-a-simple-number baseline,
  and that is before paying for the formulas. Each formula drawn from a 13-letter alphabet costs roughly 9 bits or more.

**(c) The MDL tool's null used unequal tolerances.** `w33_mdl_shortest.py` matches the 10 substrate observables within **1.5%** but
its random targets within their **tight achieved δ**, which inflates the gap (0.70 against 0.38). With one rule applied to both:

| rule | substrate cost ≤ 2 | random targets | random alphabets (mean) | P(random alphabet ≥ q = 3) |
|---|---|---|---|---|
| loose (1.5%) | 0.70 | 0.52 | 0.51 | 0.154 |
| tight (each δ) | 0.50 | 0.38 | 0.34 | 0.156 |

> **About one random alphabet in six matches the constants as well as the q = 3 alphabet (p ≈ 0.15).** Under the corpus's own
> methods, fairly applied, the constants carry no statistically significant trace of the q = 3 alphabet.

This corrects the conclusions of `w33_alphabet_pool.py` (a 10⁻⁵–10⁻⁶ coincidence) and `w33_mdl_shortest.py` (substrate observables
"anomalously short"). It says nothing against the geometry itself. It says that **numerical coincidences with constants are not
evidence for it at the precision claimed.**

## 12499: contextuality from even line sets — only at two qubits

Field reduction F_q⁴ → F₂^{4h}, with q = 2^h and ω₂ = Tr(ω_q), maps:

- a line of W(3,q) to a maximal commuting set of 2^{2h} − 1 two-h-qubit Paulis;
- a grid, the minimal even line set at even q, to a context family covering each Pauli exactly twice.

With Hermitian Paulis i^{x·z}XˣZᶻ, a state-independent parity proof exists iff the product of the context signs is −1.

| q | qubits | contexts | observables | sign product | parity proof |
|---|---|---|---|---|---|
| 2 | 2 | 6 | 9 | −1 | **yes**: the Mermin–Peres square (control) |
| 4 | 4 | 10 | 75 | +1 | no |
| 8 | 6 | 18 | 567 | +1 | no |

Every context at q = 4 and q = 8 multiplies to +I.

**Reason.** Write H = K ∪ gK with P(g)P(k) = ε(g,k)P(g + k). Then ∏_H P(h) = ∏_{k∈K} ε(g,k). That is (−1) to the number of ones of a
quadratic function on K, which is even once dim K ≥ 3.

> **A commuting Hermitian Pauli group of rank ≥ 4 always multiplies to +I.** Ranks 2 and 3 can give −I: 42/132 and 36/92 random
> samples did, against 0/52 and 0/12 at ranks 4 and 5 (`pauli_rank_sign.py`).

Field-reduced contexts have rank 2h ≥ 4, so grids give parity proofs only at q = 2. For odd q, stabiliser qudits are noncontextual
(Gross; Howard–Wallman–Veitch–Emerson), so the binary even sets cannot be contextuality proofs either. The minimal even line sets
carry state-independent contextuality **only at the two-qubit point**. The rank argument is a proof sketch checked on random samples;
multi-qubit contextual configurations in general are an active literature (BT1707), and this is one structural case of it.

## 12500: the W(3,3) plaquette model — the site's critical temperature has no derivation

Put Ising spins on the 40 points with a 4-spin coupling on each line: H = −J Σ_L Π_{p∈L} s_p. Its high-temperature series sums over
line sets covering every point evenly, so Z = 2⁴⁰ cosh⁴⁰K · W_route(tanh K). Here W_route is the enumerator of **Pass 173's route code
[40,15,10]**, recomputed independently and matching exactly: 216, 270, 1080, 3375, 7920, 7044 at weights 10–20.

The Wegner/Kramers–Wannier dual puts spins on lines and has the **address code [40,15,8]** (45 minimum words). The enumerators differ:
W(3,q) is self-dual only for even q, so **there is no self-dual point.**

The exact specific-heat maxima of the two 40-spin models are at **K ≈ 0.595 and 0.598**.

`docs/index.html` (and its copies) state: "W(3,3) as a statistical system: critical temperature β_c = log(1+√q) from Kramers–Wannier"
(Checks 1150–1163). Three things are wrong with that statement:

- log(1+√3) ≈ 1.005 is the self-dual point of the **square-lattice** 3-state Potts model;
- its "check" in `archive/root_scripts/SOLVE_OPEN.py:4940` is tautological: it asserts log(1+√3) = log(1+√3);
- a 40-spin system has no sharp phase transition in the first place.

The 2026-10-09 firewall (`w33_20261009_selector_potts_dimension_firewall.py`) already labels the formula a square-lattice result "NOT
proved here". **The site sentence should be read as unsupported.** The method (enumerator as partition function, MacWilliams as
thermal duality) is Pass 4479's; the new content here is the exact computation for the W(3,3) plaquette model and the audit of the site
claim.

## Sources

- PDG 2024 and CODATA 2018 values, as listed in `constants_information_audit.py`.
- D. Gross, *Hudson's theorem for finite-dimensional quantum systems*, J. Math. Phys. 47 (2006); M. Howard, J. Wallman, V. Veitch,
  J. Emerson, *Contextuality supplies the "magic" for quantum computation*, Nature 510 (2014).
- N. D. Mermin, Phys. Rev. Lett. 65 (1990); A. Peres, Phys. Lett. A 151 (1990).
- F. Y. Wu, *The Potts model*, Rev. Mod. Phys. 54 (1982) (the square-lattice β_c), as cited by the corpus's own firewall.

## 12501: the q = 9 48-line set is an icosahedral orbit

The 48-line even set of W(3,9) found in 12496 is identified exactly.

- **Its 12 "free" lines** (lines missing every covered point) form K₂,₁₀: a disjoint isotropic pair X, Y and the regulus
  {X, Y}^⊥ of their 10 transversals. The set misses the whole hyperbolic quadric Q⁺(3,9) swept by that regulus (100 points). It lies
  among the 288 W-lines missing the quadric, on which H = Stab({X, Y}) = GL(2,9).2 acts transitively (`passant_orbits.py`).
- **Its stabiliser lies in H**, because X and Y are determined by the set. Enumerating all 11,520 elements of H (`stab48.py`) gives a
  stabiliser of **order 480** as a group of line permutations. It is **transitive on all 48 lines**, half its elements swap the two
  24-line halves, and the element orders are 1, 2, 3, 4, 5, 6, 10, 12, 20.
- **Its image in PGL(2,9) is A₅**: order 60, element orders 1¹ 2¹⁵ 3²⁰ 5²⁴ (`stab48_pgl_image.json`). The kernel is the scalar group
  F₉*.

> **The 48-set is a single orbit of F₉* · 2.A₅ · 2**, the binary icosahedral group acting on X ⊕ Y as (M, M⁻ᵀ), together with the
> swap, with A₅ ⊂ PSL(2,9) ≅ A₆.

**Reconstruction (control).** Building that group from scratch and minimising over its invariant even sets (`icosa_even.py`)
returns **48** for one class of A₅ in PSL(2,9) and **80** for the other. 80 = q² − 1, the known transitive family.

**It does not generalise.** The same construction gives 100 and 240 at q = 11 (worse than 84) and 720 at q = 19. The value 48 depends
on q = 9 specifically.

**Observation [I].** Every exceptional optimum found so far comes from an exceptional subgroup of PSL(2,q):

| q | structure | group |
|---|---|---|
| 5 | Petersen | A₅ (PSL(2,5) ≅ A₅) |
| 7 | cube | S₄ ⊂ PSL(2,7) |
| 9 | the 48-set | A₅ ⊂ PSL(2,9) ≅ A₆ |
| 11 | icosahedron | A₅ ⊂ PSL(2,11) |

These are the field orders of Galois's theorem and of the exceptional isomorphisms. This is an observed pattern, not a theorem.

## 12502: is 48 the minimum at q = 9?

`q9_le46.py` asks CP-SAT for an even line set of W(3,9) with at most 46 lines. It uses the line-pair symmetry break of 12474, which is
valid because some chosen line meets another and PSp(4,q) is transitive on meeting line pairs. Even sets have even size, so
**INFEASIBLE would prove the minimum is 48**. UNKNOWN proves nothing. The result is recorded in `q9_le46.json` when the 3-hour run
finishes; until then, the status of record is: minimum ∈ [32, 48] (lower bound from the other track's
`w33_20261031_even_set_bounds.py`).

## 12503: the exceptional-subgroup pattern, tested

`poly_even.py` generalises 12501's construction to every polyhedral group F_q* · L · 2 on a hyperbolic pair: L = A₄, S₄ or A₅,
presented as s² = t³ = (st)ᵐ = 1 with m = 3, 4, 5. Each is tried at every q where it embeds in PSL(2,q).

| q | best polyhedral (group) | best known | reading |
|---|---|---|---|
| 5 | **20** (A₄) | 20 | the Petersen set is A₄-invariant |
| 7 | 68 (A₄), 72 (S₄) | 40 (cube, a regulus construction) | |
| 9 | **48** (A₄, A₅) | 48 | A₄ ⊂ A₅ already suffices |
| 11 | 100 (A₄, A₅) | 84 | |
| 13 | 168 (A₄) | 168 = q² − 1 | the classical transitive family |
| 17 | 288 (A₄, S₄) | 288 = q² − 1 (new upper bound; lower bound 72) | |
| 19 | 720 (A₄, A₅) | 360 = q² − 1 | |

**The pattern survives.** Below the classical q² − 1 family, small even line sets have been found only at q = 5, 7, 9, 11, each with
an exceptional PSL(2,q) symmetry. Polyhedral subgroups at q = 13, 17, 19 give nothing smaller. That is an observed pattern [I]; no
theorem is claimed.

## 12504: the site's PMNS claims, tested fairly

The site's "all within 0.5σ" neutrino triple is sin²θ₁₂ = 4/13, sin²θ₁₃ = 2/91 and sin²θ₂₃ = 7/13. `pmns_null.py` counts how often a
random 13-integer alphabet (plus the leaf 1) reaches each angle within 1σ, using NuFIT 6.0 values and the site's own:

| expression cost | q = 3 hits | random: θ₁₂ / θ₁₃ / θ₂₃ | P(random ≥ q = 3) |
|---|---|---|---|
| ≤ 2 (e.g. 4/13, 7/13) | θ₁₂, θ₂₃ | 88–90% / 0% / 95–98% | 0.83–0.88 |
| ≤ 3 (e.g. 2/91) | all three | 100% / 100% / 100% | 1.00 |

**The PMNS matches carry no evidence.** Small rationals with three integer leaves are so dense that every random alphabet reaches
every angle.

**Site corrections in `docs/index.html`:**

- the "All within 0.5σ of experiment!" sentence;
- the Higgs row, already withdrawn by Pass 1010 but still shown as a success;
- the m_p/m_e row, which is 1.4 × 10⁶ σ, the nearest integer rather than a derivation;
- the solar PMNS row.

The README's Pass 1010 table was already honest; the site had not caught up with it.

## 12505: a checker for future constant claims, and the literature

- **`scripts/check_constant_claim.py`.** Give it `--measured --sigma --predicted --cost` and it reports the experimental tension,
  the window, the fraction of random alphabets reaching the target at that cost, and a verdict: excluded, consistent but not
  evidence, or rare. On the headline claims: 4/13 is "consistent, not evidence"; 3/13 is "excluded" (11σ); 9/76 is "consistent,
  not evidence".
- **Literature.** Transitive hyperovals of Q(4,q), q odd, are known in sizes (q+1)², q(q+1) and q² − 1, with dihedral-product
  stabilisers. Searches (Pepe–Storme–Van de Voorde, the Bayens thesis, the transitive pseudo-hyperoval literature, three web
  searches) found **no hyperoval of Q(4,9) of size 48**, and no icosahedral hyperoval. That is a negative search.
