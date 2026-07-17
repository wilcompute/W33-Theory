# The 27-fold way of W(3,3)

### One parity law, one torsor, one impossibility, one quantum reading

*Self-contained capstone of Passes 368–371. Every claim is machine-verified
(witness files listed at the end) or cited to its owner. Four results, none
long, that assemble into one statement.*

---

## 1. The parity law (Pass 368)

Over `F4` every nonzero element cubes to 1, so a traced rank-`n` Hermitian form
has `Q(x) =` Hamming weight mod 2, giving isotropic count

> `(4ⁿ + (−2)ⁿ)/2 = 2^{2n−1} + (−1)ⁿ 2^{n−1}` — **type = (−1)^{Eisenstein rank}.**

One line. Its instances are the exceptional series: `A2` (rank 1, minus,
`O⁻(2,2)=W(A2)`), `E6` (rank 3, minus, `O⁻(6,2)=W(E6)`), `E8` (rank 4, plus,
`O⁺(8,2)=W(E8)/±`), `K12` (rank 6, plus, 2080 — verified on a from-scratch
hexacode construction, Pass 369). The `[[137m,m,21]]` QR tower's "exceptional
boundary" (Passes 363–367, GAP track) is this parity, and the rank-5 minus/plus
flip of the lattice-leaf story (Pass 347) is its fourth appearance.

## 2. The torsor (Passes 369–370)

`E6/2E6` splits `1+27+36`: the 36 nonsingular classes are the root pairs (and,
by the GAP track's own spread bijection, **the 36 W(3,3) spreads**); the 27
isotropic classes are *the* 27 of the cubic surface.

Fix any point `p0` of W(3,3): the 40 points split `1+12+27`, and the elation
group of the generalized quadrangle — order 27, exponent 3, nonabelian: the
**Kantor–Sahoo–Sastry Heisenberg group**, i.e. the single-qutrit Pauli group
`⟨X,Z,ωI⟩` — acts **regularly** on the 27 opposite points.

The same group acts regularly on the E6 27, and an explicit isomorphism plus
base-point bijection `φ(h·b₁) = iso(h)·b₂` is **machine-checked equivariant at
all 27 points**:

> **The bulk of W(3,3) and the 27 of E6 are one torsor.**

## 3. The impossibility (Pass 370)

Could the torsor have been commutative? **No — and this is refuted, not
unfound.** Any order-27 subgroup lies in a Sylow-3 (order 81), whose order-27
subgroups are *exactly* the four Frattini-hyperplane preimages — a complete
enumeration. On both sides:

| order-27 subgroup | regular on the 27? |
|---|---|
| exponent-3 extraspecial (qutrit Pauli) | **yes** |
| exponent-9 extraspecials | yes |
| elementary abelian `F₃³` | **no — fixed points** |

The abelian group *exists* at order 27 and *fails*. Since the regular groups
are exactly the ones whose two translation directions do not commute
(`ZX = ωXZ`):

> **Noncommutativity is required to make the 27 a torsor. The uncertainty
> principle is load-bearing.**

Among the regular options, the geometry itself selects exponent 3: elations
have order 3, and the exponent-9 groups contain order-9 elements, so the
elation-generated regular group is uniquely the Pauli one (Pass 371).

## 4. The Clifford match (Pass 371)

Naturality holds. On the W(3,3) side the normalizer of the elation group is the
point stabilizer, order 648; on the E6 side the normalizer of the regular Pauli
group has order 648; **both have point stabilizers `SL(2,3)`** (order 24, one
involution) acting faithfully on `F₃²` — i.e. both are

> `3^{1+2} : SL(2,3)` — **the one-qutrit Clifford group** —

and both 27-actions are its coset action on an `SL(2,3)` complement, hence
permutation-isomorphic. The identification of the two 27s extends from the
Pauli level to the Clifford level.

## The statement it assembles into

The substrate's bulk is a *quantum register cell*: 27 states forming a torsor
under the qutrit Pauli group, with the qutrit Clifford group as its full
symmetry, identified — entry by entry — with the 27 of E6 carried on the minus
side of the Eisenstein parity. The commutative version of this object is
provably impossible. And, per the torsor no-go (Passes 346–354), the substrate
can present this cell but cannot select a state of it: the choices the Standard
Model actually makes (a chirality, a vacuum) enter as sections from outside.

## What is *not* claimed

No mass, coupling, or measured quantity is derived. "Qutrit Pauli/Clifford"
names finite groups, not hardware. The m=6 Coxeter–Todd rung of the QR tower
remains a prediction (necessary divisibility verified; sufficiency handed to
the GAP track, `data/m6_handoff_k12.json`).

## Witnesses and owners

| result | witness | owner |
|---|---|---|
| parity law, E6/E8 identifications | `w33_pass368_eisenstein_rank_parity_law.py` (35/35) | this track |
| K12 from the hexacode; 2080; kill of d=21↔√21 | `w33_pass369_the_27_is_a_heisenberg_torsor.py` (22/22) | this track |
| elation torsor; complete Sylow decision; equivariant bijection | `w33_pass370_the_two_27s_are_one_torsor.py` (30/30) | this track |
| naturality; Clifford match; exponent selector | `w33_pass371_naturality_and_the_clifford_match.py` (23/23) | this track |
| QR tower, spread bijection, refinement counts | Passes 363–367 | GAP track |
| KSS representation of W(3,3) in `3^{1+2}` | `docs/new_connections_research.md` (Kantor–Sahoo–Sastry) | literature |
| torsor no-go | Passes 346/348/354 | this track (+ BT857's argument form) |
