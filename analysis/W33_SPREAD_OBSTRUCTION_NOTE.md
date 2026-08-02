# The spread obstruction in `W(q,q)` — a standalone note

**Scope.** This note collects the results of Passes 1612–1975 concerning the
frame graph and signed edge module of `W(3,3)` and related `W(q,q)` examples.
Passes 1971 and 1974 corrected two scope errors: the spread 45-set is not maximal
independent, and a linewise involution alone supplies a candidate subfamily but
does not automatically prove that no additional candidates exist.

The controlling current-status document is
`analysis/W33_CLAIM_STATUS_LEDGER.md`.

---

## 0. Ownership and withdrawal boundary

The general character-theoretic facts about non-real symplectic characters and
twisted Frobenius–Schur indicators belong to Gow and Vinroot and were already
represented in-repository by Passes 353/355. Passes 1900, 1907 and 1914 are
therefore retracted as novel, though their module-specific computations remain
useful.

The following readings are retired:

- the internal `C6` is electric charge;
- the internal `C6` is a Dirac or homological flux quantum;
- the spread 45-set is a maximal independent set;
- orbit-volume reduction is evidence of solver-tree reduction;
- a linewise involution by itself proves exhaustiveness of the candidate set.

---

## 1. The frame graph is 240 edge-indexed `K9`s

Let `H` have the 540 frames—unordered pairs of disjoint totally isotropic
lines—as vertices, adjacent when their canonical cross-matchings share an edge.

**Proposition.** Each of the 240 edges of `W(3,3)` lies in exactly 9 frames, all
mutually adjacent; `H` is 32-regular; and adjacent frames share exactly one
matching edge. Hence `H` is exactly the union of 240 edge-indexed, edge-disjoint
`K9`s.

The 240 cliques cover `240 C(9,2)=8640` graph edges, equal to `540·32/2`.

**Corollary.** `chi(H)=9` iff 540 variables in `1..9` satisfy 240 rainbow
`AllDifferent(9)` constraints.

---

## 2. A spread is a completion trap, not a maximal independent set

Let `S` be a spread of `W(q,q)`. Its `q^2+1` lines partition the points.

**Theorem.** The `C(q^2+1,2)` pairs of spread lines are frames and form an
independent set of `H`. Their matchings cover exactly the collinear point pairs
whose endpoints lie on different spread lines. The residual set consists
precisely of the edges lying inside the spread lines and has size

`(q^2+1) C(q+1,2) = (q^2+1)q(q+1)/2`.

For `q=3`, the seed has 45 frames, covers 180 edges, and leaves 60. Exactly 15
candidate frames have all four matching edges in that residual set.
Consequently the 45-frame seed is **not maximal independent**: any one of those
15 candidates can be adjoined.

What is exact—and is the actual obstruction—is that the 15 candidates
collectively touch only 20 of the 60 residual edges. Forty residual edges occur
in no candidate frame. Therefore no choice of 15 candidates can complete the
spread seed to a 60-frame exact cover. This was verified for all 36 spreads of
`W(3,3)`.

---

## 3. The involution-generated candidate subfamily

Assume a spread `S` carries a projective involution `sigma_S` which fixes each
spread line setwise, has no fixed point, and fixes no outside line setwise.

For every outside line `A`, the frame `{A,sigma_S(A)}` is residual: its canonical
matching is `{x,sigma_S(x):x in A}`, lying inside the spread lines. Thus the
involution supplies a candidate subfamily consisting of the two-element line
orbits.

Counting those orbits gives:

- involution-generated candidates: `q(q^2+1)/2`;
- distinct supported edges: `(q^2+1)(q+1)/2`;
- residual edges: `(q^2+1)q(q+1)/2`;
- support fraction of this subfamily: `1/q`;
- multiplicity of every supported edge in this subfamily: `q`.

The **candidate-orbit property** is the additional assertion that every residual
candidate frame is one of these line orbits. When it holds, the formulas above
are the exact complete-candidate census and the exact `1/q` law.

The property is verified by literal enumeration for the repository's `q=3,5,7`
examples, giving `20/60`, `78/390`, and `200/1400`. It is not promoted as a
uniform theorem for all spreads without a separate converse proof.

When `q` is even, `q+1` is odd, so a fixed-point-free involution cannot partition
a spread line into 2-cycles. This rules out the involution mechanism and is
consistent with the measured zero-candidate `q=2` case; it does not by itself
classify every even-characteristic spread.

---

## 4. `sigma_S` from a nonsquare similitude

Let `q` be odd, choose a nonsquare `mu in F_q`, and set
`K=F_q(alpha)` with `alpha^2=mu`. Regard the four-dimensional `F_q` space as a
two-dimensional `K` space. Multiplication by `alpha` gives an `F_q`-linear
symplectic similitude `g` with `g^2=mu I`.

Projectively, `g` has order two. A fixed projective point would require an
`F_q` eigenvalue `lambda` with `lambda^2=mu`, impossible. The one-dimensional
`K`-subspaces form the associated Desarguesian symplectic spread and are fixed
linewise by the induced involution.

This proves existence of the linewise involution for the associated spread for
every odd `q`. It does not, by itself, prove the candidate-orbit property.

At `q=3`, exhaustive computation proves more: all 36 spreads carry the unique
nontrivial linewise stabiliser, central in the spread stabiliser of order 1440.
The 72 nonsquare-multiplier similitudes give 36 projective involutions; the
square-multiplier branch gives 270 inner involutions. The exact `36/270` split is
a certified finite result for which no literature reference has been located.

---

## 5. The signed edge module

Over `PGSp(4,3)` the orientation-signed 240-edge module is multiplicity-free:

```text
V = 15 + 24  |  81  |  30 + 90
    exact       harmonic  coexact
      39          81       120
```

- `15+24` is the nonconstant part of the 40-point permutation module.
- `Res_PSp(90)=45+conjugate(45)` and the real endomorphism algebra on the 90 is
  `C`; invariant complex structures are `±J`.
- The 15 and 81 are odd-dimensional and cannot admit a real `J` with `J^2=-1`.
- The 90 is the only non-rational block, with field `Q(omega)` and integral phase
  units `C6`.
- The finite equivariant centralizer torsion is `(C2)^4 x C6`; its unique odd
  subgroup `C3=<mu6^2>` acts faithfully only on the coexact 90.
- The outer involution inverts `mu6`, giving `C6 semidirect C2 = D12` on the
  phase label.
- Multiplicity-freeness gives `Hom_PSp(90,X)=0` for
  `X in {15,24,30,81}`. The phase is linearly confined to the 90 in the ideal
  equivariant model.

### What the phase is not

| reading | status |
|---|---|
| electric charge from a Gauss-law sector | withdrawn: the phase is coexact, not exact/source-like |
| Dirac or homological flux quantum | withdrawn: the integral boundary complex has no supporting `Z/3` or `Z/6` torsion |
| QCD colour, generation, or neutrino label | not derived and not promoted |
| internal cyclotomic sector marker | supported representation-theoretically |

The `E8` Coxeter six-cycle action is not the same `C6`; the two full-carrier
character multiplicities are incompatible.

---

## 6. Solver status

`chi(H)=9` remains undecided. Frozen branch counts are:

```text
plain                              2,127,575
spread-variable branching            60,909
geometric lex, 8 generators          198,352
spread + lex, 8 generators           451,460
spread + lex, 40 generators          512,714
```

The exact spread-signature orbit reduction `25,920 -> 807` remains valid, but it
did not improve the tested fixed-search tree. The combined encodings are 7.4 and
8.4 times worse than spread branching alone. The current diagnosis is a
propagation-horizon mismatch: spread variables are fixed early while the lex
constraints become informative mainly on later frame variables.

Full-scale constraint auditing no longer uses truncated enumeration. Version 5
of `scripts/constraint_audit.py` uses named feasible witnesses or explicit finite
feasible orbits; such certificates prove only their stated scope.

---

## 7. Open problems

- Decide `chi(H)=9`.
- Decide whether `max |class intersection K10|=13`; 13 is attained and 14 is not
  excluded.
- Prove the candidate-orbit property uniformly for the associated Desarguesian
  spread, or find a counterexample beyond `q=3,5,7`.
- Determine which non-Desarguesian symplectic spreads carry a linewise
  fixed-point-free involution.
- Prove or refute uniform uniqueness of the linewise stabiliser beyond `q=3`.
- Locate prior art for the exact `36/270` multiplier split.
- Classify nonlinear invariant couplings involving the phase-bearing 90 without
  importing a physical label.

---

*Primary reconciliation: Passes 1971–1975. Relevant background includes Gow,
Vinroot, Thas–Payne, De Bruyn, in-repository Passes 227/346/353/355, BT790/795,
and the exact certificates cited in the claim-status ledger.*
