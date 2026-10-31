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
