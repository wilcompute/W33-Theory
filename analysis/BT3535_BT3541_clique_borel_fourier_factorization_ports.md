# Passes 3535–3541 — independent star-clique recertification, the four Borel–M57 archetypes, Perkel Fourier projectors, and nonseparable Moore factorization

## Status

The exact lightweight verifier reports

```text
PASS_7_FRONTS 34ea459ab6acea3a2b5624ba6523016cfb914ffb54220ed64230f74f78a1fb6b
```

This packet executes the five continuations from Passes 3528–3534 and two additional high-risk directions. It distinguishes completed finite theorems from the separately heavy 3,720-instance maximum-clique rerun. The degree-57 Moore graph remains open.

---

## 3535 — an independent exact compatibility-clique recertifier

The previous packet independently regenerated the 3,720 candidate 19-vertex star complements but retained the published Cliquer histogram as a source-locked boundary. The new companion source

```text
analysis/bt3535_star_clique_recertify.py
```

implements the missing second route.

For every candidate adjacency matrix `C`, it constructs

\[
M=2I-C
\]

and computes \(M^{-1}\) exactly. A reconstruction column \(b\in\{0,1\}^{19}\) must satisfy

\[
b^{\mathsf T}M^{-1}b=2.
\]

Because the seed contains the closed neighbourhood of its windmill centre, every omitted graph vertex has centre coordinate zero and exactly four selected windmill leaves. The implementation exhausts these choices together with all subsets of the four outside coordinates, rejecting vectors that already violate the \(\lambda=1\), \(\mu=4\) common-neighbour bounds inside the star complement.

Two surviving columns are compatible exactly when

\[
b^{\mathsf T}M^{-1}c\in\{-1,0\},
\]

with the corresponding adjacent/nonadjacent common-neighbour bound also enforced.

The resulting graph is solved by a deterministic bitset maximum-clique engine with greedy-colour upper bounds. Each instance emits:

- its compatibility-graph order;
- an exact maximum-clique witness;
- the search-node count;
- a deterministic proof-row digest.

The complete job fails closed unless all 3,720 maxima reproduce the published histogram and the compatibility-graph size range is exactly 4 through 265.

The clique engine itself is regression-tested on \(K_9\), \(C_5\), and \(K_{5,7}\). The complete 3,720-instance result is **not promoted in this packet before an observed heavy-workflow artifact**.

---

## 3536 — prime fixed sets in a hypothetical M57 are Moore graphs again

Let an automorphism of prime order \(p\) act on a hypothetical Moore graph

\[
\operatorname{SRG}(3250,57,0,1).
\]

At a fixed vertex, its fixed neighbours occur in orbits of size one while all other neighbours occur in \(p\)-cycles, so the fixed degree is congruent to 57 modulo \(p\). The fixed set is closed under the unique common neighbour of every nonadjacent fixed pair.

If the fixed set has more than one vertex, the induced graph is connected, has diameter at most two, and has girth at least five. Writing its adjacency matrix as \(A_F\), the Moore law gives

\[
A_F^2\mathbf1=(|F|-1)\mathbf1.
\]

Connectivity and the girth constraint force regularity; hence the nontrivial fixed graph is itself a Moore graph.

The admissible Moore degrees are

\[
2,3,7,57.
\]

Therefore:

- for \(p=19\), the fixed degree is zero and every order-19 automorphism fixes exactly one vertex;
- for \(p=3\), the fixed graph is either one vertex or the Petersen graph on ten vertices.

This fixed-subgraph recursion is independent of the Perkel graph. It applies conditionally to automorphisms of a hypothetical M57.

---

## 3537 BONKERS — a hypothetical `19:9` action collapses to four archetypes

Assume

\[
B=C_{19}\rtimes C_9
\]

acts on a hypothetical M57. The normal \(C_{19}\) fixes a unique vertex \(x\), so the full Borel group fixes \(x\).

The possible nontrivial Borel orbit sizes are

\[
19,57,171.
\]

Combining the 3,250-vertex census with the order-three and order-nine fixed-set theorem leaves exactly two orbit profiles:

\[
\boxed{P_{19}:\quad1+9\cdot19+18\cdot171,}
\]

and

\[
\boxed{P_{57}:\quad1+3\cdot57+18\cdot171.}
\]

The invariant neighbourhood \(N(x)\) is correspondingly either three 19-orbits or one 57-orbit.

For an order-19 element, the permutation module has one fixed point and 171 regular \(C_{19}\)-orbits. Decomposing the \(7^{1729}\) and \((-8)^{1520}\) eigenspaces and applying the adjacency trace gives the raw displacement possibilities

\[
g\in\{57,342,627,912,1197\},
\]

where \(g\) counts vertices mapped to adjacent vertices.

On one nonfixed \(C_{19}\)-orbit, the induced graph is a circulant. Girth at least five permits at most one undirected step class. Equality of the displacement count for all nontrivial powers balances the nine step classes, so

\[
9\frac g{19}\le171.
\]

Only

\[
\boxed{g=57\quad\text{or}\quad g=342}
\]

survive. Thus every hypothetical Borel action belongs to exactly one of four necessary archetypes:

\[
P_{19}^{\rm low},\ P_{19}^{\rm high},\ P_{57}^{\rm low},\ P_{57}^{\rm high}.
\]

The low cases have three edge-bearing regular Borel orbits; the high cases have eighteen. This is a severe conditional reduction, not a construction or nonexistence proof.

If the current oddness and odd-order automorphism bound are assumed, the presence of this Borel subgroup would additionally force

\[
\operatorname{Aut}(M57)=C_{19}\rtimes C_9.
\]

---

## 3538 — exact Perkel Fourier projectors with denominator 171

The Perkel vertex module was previously decomposed rationally as

\[
\mathbb Q^{57}=\mathbf1\oplus3V_{18}\oplus V_2.
\]

This pass produces the projectors themselves.

Let \(A\) be the Perkel adjacency matrix, \(J\) the all-ones matrix, and \(B_{19}\) the block-diagonal matrix with three \(J_{19}\) blocks. Define

\[
N=-A^3+9A^2-19A+6I=171E_{-3}.
\]

The four integer projector numerators are

\[
P_1=3J,
\]

\[
P_2=9B_{19}-3J,
\]

\[
P_{18}=N-9B_{19}+3J,
\]

\[
P_{36}=171I-3J-N.
\]

They have exact ranks

\[
\boxed{1,2,18,36}
\]

and satisfy

\[
P_iP_j=171\delta_{ij}P_i,
\qquad
P_1+P_2+P_{18}+P_{36}=171I.
\]

The adjacency actions are

\[
AP_1=6P_1,
\qquad
AP_2=AP_{18}=-3P_2,-3P_{18},
\]

and

\[
(A^2-3A+I)P_{36}=0.
\]

The complete conductor-19 projector is especially simple:

\[
\boxed{P_{54}=P_{18}+P_{36}=171I-9B_{19}.}
\]

On this 54-space,

\[
(A^3-8A+3I)P_{54}=0.
\]

Therefore every Perkel adjacency polynomial has the exact Fourier normal form

\[
p(A)=p(6)E_1+p(-3)E_2+
(c_0I+c_1A+c_2A^2)E_{54},
\]

where \(p(x)\) is reduced modulo

\[
x^3-8x+3.
\]

For example,

\[
x^{19}\equiv
-69{,}144{,}384+201{,}730{,}265x-54{,}214{,}032x^2.
\]

---

## 3539 — factorization-first M57 search and the separable no-go

Inside the declared involutive Moore branch, every residual row pencil is a one-factorization of \(K_n\). At \(n=56\), this means:

- 56 row pencils;
- 55 perfect matchings per pencil;
- 28 edges per matching;
- all \(\binom{56}{2}=1540\) symbol pairs covered once per pencil.

The most aggressive compression would reuse one global symbol factorization and one row-edge factorization, coupling them by a colour bijection. This separable ansatz was exhausted on the exact Hoffman–Singleton control.

For \(K_6\), there are exactly

\[
15\text{ perfect matchings}
\]

and

\[
6\text{ labelled one-factorizations}.
\]

Fixing one row factorization and one symbol factorization gives \(5!=120\) colour identifications. Across all

\[
120\cdot\binom63=2400
\]

triangle tests, every holonomy has exactly two fixed points. Thus

\[
\boxed{\text{every globally separable factorization ansatz fails every HS triangle}.}
\]

The M57 involutive lane must therefore use genuinely row-dependent, reciprocity-coupled one-factorizations.

---

## 3540 BONKERS — Hoffman–Singleton is the complete `K6` factorization atlas

The six residual rows of one exact Hoffman–Singleton edge chart were classified against all labelled one-factorizations of \(K_6\).

Their factorization indices are

\[
(4,5,2,0,1,3).
\]

Hence each of the six one-factorizations occurs exactly once:

\[
\boxed{\text{the HS edge chart realizes the complete labelled }K_6\text{ factorization atlas}.}
\]

All twenty triangle holonomies have cycle type

\[
2^3.
\]

The smallest nontrivial Moore control is therefore maximally nonseparable at the factorization level. This changes the search philosophy for M57: the primary object is not one factorization with relabelings, but a field of mutually coupled factorizations.

---

## 3541 — every genuinely polynomial W33 theorem is now ported to Gewirtz

Both graphs were regenerated objectwise:

\[
W33=\operatorname{SRG}(40,12,2,4),
\]

\[
\mathrm{Gewirtz}=\operatorname{SRG}(56,10,0,2).
\]

Their restricted spectra are

\[
2^{24},(-4)^{15}
\]

and

\[
2^{35},(-4)^{20},
\]

respectively. For either graph, with degree \(k\), order \(v\), and \(P=J/v\),

\[
(A-2I)(A+4I)=(k-2)(k+4)P.
\]

Let \(Q=I-P\). The exact centered-complement reflection is

\[
R=\frac{(k+1)P-I-A}{3},
\qquad
R^2=Q.
\]

The restricted projectors are

\[
E_2=\frac{Q-R}{2},
\qquad
E_{-4}=\frac{Q+R}{2}.
\]

Every polynomial reduces on augmentation modulo

\[
x^2+2x-8.
\]

If

\[
p(x)\equiv ax+b,
\]

then the full graph formula is

\[
\boxed{p(A)=p(k)P+(aA+bI)Q.}
\]

Equivalently,

\[
p(A)=aA+bI+[p(k)-ak-b]P.
\]

The typed package also emits exact trace, determinant, and inverse formulas after supplying the graph-specific multiplicities. Incidence, lines, codes, automorphisms, Smith forms, descendant maps, and intertwiners remain geometry-sensitive and are not auto-ported.

---

## Reproduction

```bash
python analysis/bt3535_3541_clique_borel_fourier_factorization_ports.py
pytest -q tests/test_bt3535_bt3541_clique_borel_fourier_factorization_ports.py
python analysis/bt3535_star_clique_recertify.py --self-test
```

The independent complete clique rerun is intentionally isolated:

```bash
python analysis/bt3535_star_clique_recertify.py \
  --json evidence/pass3535_3541/star_clique_full.json
```

## Claim boundaries

- M57 remains open.
- The four Borel archetypes are conditional necessary forms.
- No complete independent 3,720-instance clique histogram is promoted until its heavy artifact is observed.
- No W33–Gewirtz incidence, code, group, or objectwise equivalence is asserted.
- No hardware, laboratory, particle, or spacetime claim is made.
