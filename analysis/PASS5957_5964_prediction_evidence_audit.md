# Passes 5957–5964 — prediction-evidence audit and claim-tier correction

## Verdict

The physical-derivation claims introduced in Pass5913–5932 and Pass5933–5956 are **not established by their producer scripts**. The scripts contain useful exact arithmetic and combinatorics, but the map from those finite quantities to masses, inflationary observables or spacetime volume is either assumed, circular, target-back-solved, or repaired after comparison with the target.

Accordingly these items are retained only as **ansätze / comparison tables** until an independent dynamics theorem derives the observable map.

This audit does not depend on whether a numerical value happens to agree with experiment. It asks the logically prior question: was the observable forced without using its target value, assuming the desired scaling exponent, or inserting an unproved conversion rule?

## Pass5957 — L-infinity mass ratios: not a computed Maurer-Cartan solution

The producer claims an L-infinity interpretation, but internally it records

- `mc_residual = K - LA = 10`, not zero;
- `mc_sum_formal = Y1 + Y2 + Y3`, explicitly noting that this is not zero;
- `m_c/m_t = 1/(k^2-2mu)` and the up/top ratio are imported as denominator formulas and then *named* `l_2` and `l_3` evaluations.

No explicit transferred L-infinity structure, graded vector space with verified brackets, higher Jacobi identities, or actual evaluation of `l_2(alpha,alpha)` and `l_3(alpha,alpha,alpha)` produces the quoted Yukawa ratios.

**Retain:** exact integer/rational formulas as an ansatz table.

**Withdraw:** “Maurer-Cartan equation verified” and “L-infinity derivation of quark masses.”

## Pass5958 — Weyl-law dimension/volume: circular refinement definition

The producer defines

```python
N_n_count(n,Lambda) = n**4 * N1
```

and explains that multiplicities are “scaled by n^4 (4D volume scaling).” It then uses the resulting `N~n^4` to infer `d=4`.

That is circular: the exponent to be discovered is inserted in the definition of the refined counting function.

The finite spectrum itself also gives `N(4)=362` and `N(16)=440`, while `C_W=480` is introduced separately as `v*k`. The script therefore does not exhibit an asymptotic spectral counting sequence converging to 480.

The conversion to `V_4=30*pi^2 l_P^4` is likewise an assumed normalization, not a consequence of a verified manifold/metric Weyl law.

**Retain:** the finite D^2 spectrum and any independently computed refinement census.

**Withdraw:** discovery of spacetime dimension from this script and physical 4-volume derivation.

## Pass5959 — electron packet: exact factorization, unproved mass map

The identity

\[
2\cdot49\cdot17\cdot16\cdot13=346528
\]

is exact. What is not derived is why the electron/top Yukawa ratio must equal the reciprocal of that product.

No mass matrix, Yukawa operator, renormalization flow or representation-theoretic eigenvalue theorem in the producer forces those factors to multiply into a fermion mass ratio.

The reported “sigma” is especially non-statistical: the code defines it as `deviation_pct/0.87` without an uncertainty model or propagated experimental/theory errors.

**Retain:** integer factorization and comparison-only table.

**Withdraw:** prediction status and sigma language.

## Pass5960 — Yang-Mills 1818 MeV: explicit target back-solving

The Yang-Mills producer is self-diagnosing. After trying several formulas it states:

> `Solve for Lambda_QCD_eff that gives exactly 1818 MeV`

and executes

```python
delta_ym_target = 1818.0
lambda_eff = delta_ym_target / coeff
```

This algebraically guarantees the target. The external QCD scale is dimensionful input, and the script does not derive a pure-Yang-Mills Hamiltonian spectrum or a rigorous mass gap.

**Retain:** the dimensionless coefficient `12*sqrt(13/40)` as an ansatz if useful.

**Withdraw:** “1818 MeV derived/predicted” and any identification with a mathematical Yang-Mills mass-gap proof.

## Pass5961 — neutrino 0.0500 eV: target factor repaired after mismatch

The initial claimed factorization

\[
24\cdot480\cdot13\cdot273
\]

equals `40,884,480`, four times the desired `10,221,120`. The producer notices this in its own comments and replaces `24` by `6`, writing that this fixes the target.

The dimensionful scale is then supplied by the measured electron mass.

Thus

\[
6\cdot480\cdot13\cdot273=10,221,120
\]

is an exact integer identity, but no neutrino mass operator or seesaw theorem forces `m_e/m_nu3` to equal that integer.

**Retain:** integer identity as an ansatz.

**Withdraw:** Leech-derived neutrino mass prediction.

## Pass5962 — inflation r=1/45: count is real, observable map is assumed

The classical count of 45 tritangent planes may be retained where independently certified. The inflation script then simply sets

```python
r = Fraction(1, N_TRITANGENT_PLANES)
```

and narrates that 45 saddle directions imply a slow-roll suppression `1/45`.

No inflationary action, canonical scalar field, potential, background solution or perturbation calculation derives this map.

The script itself computes a single-field consistency value of `n_s` that is incompatible with the comparison value it quotes, and then says `n_s` needs an independent mechanism. That further demonstrates that `r=1/45` is not yet a closed inflationary model.

**Retain:** 45-count.

**Withdraw:** r prediction.

## Pass5963 — 3.2 TeV scalar: exact spanning-tree count, arbitrary mass multiplier

The octahedron graph `K_{2,2,2}` indeed has

\[
\tau(K_{2,2,2})=384.
\]

The producer then defines

\[
m_{\rm scalar}=m_H\frac{384}{15}.
\]

There is no Hamiltonian, mass matrix, propagator pole, coupling or self-energy theorem connecting an octahedron spanning-tree count divided by 15 to a scalar pole mass.

**Retain:** `tau=384` and the arithmetic ratio `384/15`.

**Withdraw:** 3.215 TeV prediction.

## Pass5964 — release policy

A physical result remains at **ANSATZ / COMPARISON-ONLY** tier if its producer does any of the following:

1. inserts `n^d` into a refinement rule and then claims to discover dimension `d`;
2. solves an input scale from the desired output;
3. repairs a factor after observing a target mismatch;
4. defines a physical observable as a reciprocal/product of a finite count without deriving the observable map from dynamics;
5. labels an arithmetic discrepancy in “sigma” units without a statistical uncertainty model.

Promotion requires a separate theorem that supplies the physical map independently of the target value.

## Net effect

The correction does **not** discard the useful finite mathematics. It separates it cleanly:

- exact W33 invariants remain exact;
- `346528`, `10,221,120`, `45`, and `384` remain reproducible arithmetic/combinatorial objects;
- none are currently certified as electron mass, neutrino mass, inflationary `r`, scalar pole mass, physical four-volume, or Yang-Mills gap.

That is the strongest version of the project: the combinatorics stays, while the physics layer has to earn its conversion map.
