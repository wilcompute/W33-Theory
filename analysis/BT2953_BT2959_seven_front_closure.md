# Passes 2953–2959 — conjugacy, chirality, Bayesian diagnosis, three-copy CSS, and two outside-box closures

## Executive result

This packet executes the five continuations left open by Passes 2917–2923 and follows two independent structural probes until they close or fail exactly.

1. The 188 directed-diameter-19 affine transformations meet **12 genuine conjugacy classes** of `ASp(4,3)`, not the 25 algebraic profiles previously used as a safe over-refinement.
2. The two middle 12-ray magic classes are impossible to distinguish class-blind on one copy: both uniform ensembles equal `I_4/4`. With the conjugate pair known, a one-bit selector between the two local probes `YI` and `IY` covers all twelve pairs without an entangling gate.
3. Exact finite-horizon posterior optimization under a coordinate-asymmetric detector model reduces aggregate observer error from `5.869%` to `1.689%` while slightly reducing expected action cost.
4. The earlier three-copy set-cover test used a shallow ray and imposed a condition stronger than necessary. Exhausting all `43,617` CSS `[[6,2]]` stabilizer subspaces and all sixteen syndromes finds `54` projectors that route every accepted single fault into the clean logical line, but all such logical lines are stabilizer. Among `67,023` deep-magic-closed branches the minimum first-order output slope is exactly `1`: no three-copy CSS branch improves the deep resource.
5. The seven-bit rank engine remains a storage theorem and source-complete hardware candidate. Its replacement-versus-context-memory decision remains blocked on an observed same-harness place-and-route report; no silicon result is inferred from the queued workflows.
6. **Outside-box I:** the fixed-point incidence of the 188 hard compiler transformations has ternary Fourier support `79/81`. Exactly the two nontrivial pure-`z_p` characters vanish, giving a perfect `60+60+60` incidence split across the three `z_p` slices and refuting a sparse Hodge/code-module identification.
7. **Outside-box II:** the middle-class label `s=mu+nu mod 3` is exchanged by conjugation through `s -> -s`. That is precisely the reflection action already carried by the machine's `D_12` mirror on its `C_3` phase subgroup. The resulting metadata transform is reversible, but it is not a physical antiunitary gate on an unknown state.

## Pass 2953 — actual conjugacy closure of the terminal compiler shell

A forward breadth-first search of the full four-operation affine group again gives

```text
|ASp(4,3)| = 4,199,040
directed diameter = 19
terminal shell = 188
```

Conjugating each unclassified shell element by the four affine generators and their inverses, and closing the orbit in the full group, produces twelve classes intersecting the shell. Their shell intersections are

```text
2, 22, 6, 6, 4, 6, 6, 4, 2, 8, 12, 110
```

and their full class sizes sum to `2,730,348`. The dominant shell contribution is one order-four class of full size `43,740`, centralizer order `96`, and shell intersection `110`.

The inverse relation is also class-level rather than profile-level: two order-12 pairs exchange under inversion, four classes are self-inverse, and two inverse classes do not meet the terminal shell at all.

**Correction.** The Pass 2923 count of 25 algebraic profiles was not false—it was explicitly bounded as a profile partition rather than a conjugacy theorem—but it strictly over-refines the true answer.

## Pass 2954 — what the minimal chirality detector can and cannot do

For the two middle classes `A` and `B`,

```text
rho_A = (1/12) sum_{psi in A} |psi><psi| = I_4/4
rho_B = (1/12) sum_{psi in B} |psi><psi| = I_4/4.
```

Their trace distance is zero. Therefore no one-copy POVM can identify an unknown uniformly drawn class label.

Complex conjugation nevertheless pairs every `A` ray with one `B` ray, and every pair has squared overlap `1/3`. Perfect one-shot pair discrimination is impossible, but the Helstrom success probability is

```text
p_success = (1 + 1/sqrt(3))/2 = 0.7886751345948129.
```

No single fixed Pauli separates all twelve conjugate pairs. The minimum local cover is exactly

```text
{Y tensor I, I tensor Y}.
```

A one-bit classical selector chooses the qubit; physically the selected local `Y` measurement is `S^dagger`, then `H`, then ordinary `Z` readout. No entangler is required. Majority repetition raises success to `0.884900`, `0.933013`, `0.959742`, and `0.975334` at 3, 5, 7, and 9 copies.

## Pass 2955 — Bayes-optimal noisy observer policy

The existing depth-four noise-free policy was evaluated under the same channel and action costs used by the new posterior dynamic program:

```text
p01 = [0.002, 0.006, 0.002, 0.006]
p10 = [0.020, 0.050, 0.020, 0.050]
cost(F_p) = cost(Z_p) = 1
cost(CX_p->f) = cost(CX_f->p) = 2
```

The initial support is known exactly, the horizon is four actions, and stopping is allowed at every posterior.

| terminal-error weight | aggregate error | expected action cost |
|---:|---:|---:|
| 20 | 0.0285396 | 4.48013 |
| 50 | 0.0210285 | 4.67179 |
| 100 | **0.0168892** | **4.92667** |
| 200 | 0.0159274 | 5.05915 |

The old minimum-depth tree under the same noisy channel gives error `0.0586948` and cost `4.96316`. At weight 100 the fully re-optimized policy therefore cuts error by about 71% while slightly lowering expected action cost. This is not repetition on the old tree: posterior stopping, root actions, and later actions are re-optimized.

## Pass 2956 — complete three-copy CSS closure

The earlier Pass 2910 factor-wise set-cover test has two corrected boundaries:

1. it instantiated ray `0`, a shallow-class state, rather than the deep engineering target ray `5`;
2. rejecting all nine single-error vectors is sufficient for quadratic suppression but not necessary. An accepted fault may instead land collinearly on the accepted clean logical ray.

The new search enumerates every six-qubit CSS rank-four stabilizer subspace:

```text
43,617 CSS subspaces
16 syndromes each
697,872 projectors per Clifford class
```

Fifty-four deep-class projectors—27 all-X and 27 all-Z—make every accepted single-error vector collinear with the accepted clean vector. This proves that the former rejection criterion was too strong. However, all 54 clean logical lines are stabilizer lines, and none is a closed deep-magic branch.

The full deep-closed CSS census contains `67,023` branches. The minimum first-order output parameter slope is

```text
min dp_out/dp at p=0 = 1,
```

attained by `3,087` branches. The best clean success probability among those branches is `1/4`, hence twelve raw inputs per accepted output at the pure fixed point. An explicit identity branch has

```text
q(p) = (2-p)^2/16,
F_out = 1 - 3p/4,
p_out = p.
```

So three-copy CSS processing does not improve the deep M36 resource even to first order. This is exhaustive for CSS `[[6,2]]` projectors, not for all `213,648,435` general isotropic six-qubit stabilizer subspaces.

## Pass 2957 — rank-engine role gate

The exact seven-bit storage theorem and exhaustive transition model remain valid. What remains unavailable is an observed same-harness placement report: the Pass 2856 and Pass 2917 jobs are still queued in the repository-wide Actions backlog.

The release therefore encodes a mechanical decision rule rather than manufacturing a result:

1. replace the arithmetic execution core only if rank coding wins area without violating timing;
2. if it saves storage but loses execution area or timing, use it only for compressed context memory;
3. if it loses both, reject the hardware encoding while retaining the information-theoretic theorem.

## Pass 2958 — hard-shell fixed-point Fourier law

Let `h(x)` count terminal-shell transformations fixing frame `x in F_3^4`. The 188 elements contribute 180 total fixed incidences. The per-frame count histogram is

```text
h=0:15, h=1:18, h=2:13, h=3:12, h=4:15, h=5:8.
```

The ternary Fourier transform of `h` has 79 nonzero coefficients. Its only zeros are

```text
(0,1,0,0), (0,2,0,0),
```

the two nontrivial pure-`z_p` characters. Equivalently, the fixed-incidence totals by `z_p` are exactly

```text
60, 60, 60.
```

The hoped-for sparse `15/24/40/81` Hodge or code duality is therefore refuted. What survives is a sharper compiler symmetry: terminal difficulty is perfectly balanced across past-phase translations and not across the other three coordinates.

## Pass 2959 — mirror-assisted reversible chirality metadata

Write a ray's phase label as

```text
s = mu + nu mod 3.
```

The two middle classes are `s=1` and `s=2`. Complex conjugation sends `s -> -s`, exchanging them. The existing `D_12` mirror relation sends rotation `r` to `r^{-1}`; on its `C_3` phase subgroup this is exactly the same inversion.

The reversible metadata map is therefore

```text
(s, mirror) -> ((-1)^mirror s, mirror).
```

Keeping the mirror bit makes the transform bijective and gives zero logical-erasure cost. This is a controller-level identification of two structures already in the architecture. It does not implement complex conjugation of an unknown quantum state, which is antiunitary and not a physical deterministic gate.
