# Passes 3989–3996 — physical incidence photon processor and exact orbit closure

## Promoted status

```text
PASS_PHYSICAL_INCIDENCE_PHOTON_AND_THREE_MAXCODE_ORBITS
2223d77032d8b748cfeb32ec2ef6f2c68f43312a38b9b8c85b5e045d140404e9
852db084763db441845f0ef082a28b30c90a0f6eccd0aff32cc57fde7fa46757
16680f46b3768c71fe133d0a62985d2d10ad1d19c96afc899d733c2a7d17f615
```

This packet executes five frontier tasks and three additional photon constructions. It preserves the invariant-vacuum-speed firewall: all processor rates below are engineered Hamiltonian rates, while `c` remains the propagation-front speed.

## Pass 3989 — degree-four physical lift of the W33 processor

Let `N` be the point-line incidence matrix of `W(3,3)`. There are 40 points and 40 totally isotropic lines; every point lies on four lines and every line contains four points. Exact enumeration gives

\[
\boxed{NN^T=4I+A_{W33}}.
\]

Thus the dense 12-neighbor point graph has an 80-mode bipartite lift with

\[
40\text{ point modes}+40\text{ line-bus modes},
\]

\[
\boxed{160\text{ couplings},\quad\text{degree }4,\quad\text{girth }8}.
\]

The Gram spectrum is

\[
\operatorname{Spec}(NN^T)=16^1,6^{24},0^{15},
\]

so the bipartite incidence Hamiltonian has spectrum

\[
\boxed{-4^1,-\sqrt6^{24},0^{30},\sqrt6^{24},4^1}.
\]

With uniform point-line coupling `g` and bus detuning `Delta`, adiabatic elimination gives

\[
H_{\rm eff}=-\frac{g^2}{\Delta}NN^T
=-\frac{g^2}{\Delta}(A+4I)+O(g^4/\Delta^3).
\]

At

\[
t=\frac{\pi\Delta}{2g^2},
\]

the point sector approaches the exact W33 half-period reflection. This is an analytic architecture and detuning certificate, not a fabricated device.

## Pass 3990 — exact dual-geometry echo and three-moment tomography

Let

\[
B=J-I-A,\qquad D=A-B.
\]

Then

\[
A+B=J-I
\]

is geometry-blind on the 39-dimensional nonuniform sector, whereas

\[
\operatorname{Spec}(D)=-15^1,5^{24},-7^{15}.
\]

The exact projector formulas are

\[
E_{-15}=\frac{(D-5I)(D+7I)}{160}=\frac{J}{40},
\]

\[
E_5=\frac{(D+15I)(D+7I)}{240},
\qquad
E_{-7}=-\frac{(D+15I)(D-5I)}{96}.
\]

Therefore only the first two moments of `D` are needed to reconstruct sector populations:

\[
p_{-15}=\frac{\langle D^2\rangle+2\langle D\rangle-35}{160},
\]

\[
p_5=\frac{\langle D^2\rangle+22\langle D\rangle+105}{240},
\qquad
p_{-7}=\frac{-\langle D^2\rangle-10\langle D\rangle+75}{96}.
\]

On the nonuniform sector,

\[
e^{-i\pi D/12}
\]

is a global phase times `E_5-E_-7`. If identical commuting error `C` enters both arms,

\[
e^{-it(A+C)}e^{+it(B+C)}=e^{-it(A-B)},
\]

so common error cancels exactly. A symmetric echo cancels first-order common error beyond the commuting case.

## Pass 3991 — exact maximum-code orbit census

The fixed-parent compatibility graph has 945 vertices, degree 624, and maximum clique size 57. The parent-preserving group has order 51,840 and two weight-four vertex orbits of sizes 135 and 810.

Fixing one vertex in the 135-orbit yields exactly 57 maximum cliques:

\[
12\text{ of composition }3+54,
\qquad
45\text{ of composition }15+42.
\]

Orbit-stabilizer and explicit orbit traversal produce exactly

\[
\boxed{945=540+270+135}
\]

maximum codes in three parent-group orbits. Their stabilizers have orders

\[
\boxed{96,192,384}.
\]

This corrects the earlier use of a full coordinate stabilizer as though it necessarily preserved the fixed parent. Maximum-code uniqueness is false in the fixed-parent problem: there are exactly three orbits.

## Pass 3992 — complete central fusion lattice

The literal 48-orbital algebra has seven primitive central blocks of simple degrees

\[
\boxed{1,1,2,2,2,3,5}.
\]

All central coarse-grainings are set partitions of these seven blocks. Hence

\[
\boxed{B_7=877}
\]

central fusions exist. By central dimension their census is

\[
1,63,301,350,140,21,1.
\]

Quotienting the interchangeable degree-one pair and degree-two triple by

\[
S_2\times S_3
\]

leaves

\[
\boxed{198}
\]

inequivalent types, distributed as

\[
1,23,68,66,31,8,1.
\]

These are exact unital subalgebras of the center. They are not automatically combinatorial fusions of the 48 orbital relations. The heavy symbolic job separately freezes the seven primitive orbital-basis idempotents and the `7 x 48` character table.

## Pass 3993 — explicit Monster maximal-overgroup acquisition

The Monster gate now searches through explicit maximal overgroups rather than blind ambient words.

1. GAP/CTblLib enumerates direct class fusions `U4(2) -> M`.
2. It composes every available `U4(2) -> H -> M` fusion through Monster maximal-subgroup character tables.
3. The workflow clones the published `mmgroup` maximal-subgroup generator database.
4. Only compatible explicit overgroups are inventoried and searched.
5. A deterministic bounded word pool tests order-three quadruples against the exact pair-order, triple-order, and order-25,920 closure signatures.

No embedding is promoted without four portable Monster words. The default status remains

```text
PENDING_EXPLICIT_MONSTER_U42_WORDS
```

until the strict existing object-action and class-fusion firewall passes.

# Three additional photon constructions

## Pass 3994 — a 30-dimensional dark-memory sector

Since `rank(N)=25`, both point and line spaces contain 15-dimensional kernels. The 80-mode incidence Hamiltonian therefore has

\[
\boxed{30\text{ exact zero modes}}.
\]

The remaining bright sectors have dimensions 1 and 24 on each side. This supplies an exact separation between stationary dark coordinates and bright processing coordinates. Relative dark/bright phase can encode clock-referenced memory, but this is an engineered Hamiltonian memory—not the claim that physical time is literal RAM.

## Pass 3995 — exact four-step Floquet clock

For

\[
L=12I-A,
\]

the exact dimensionless period is `pi`. Define

\[
V=e^{-i\pi L/4}=I-(1+i)E_{10}.
\]

Then

\[
\boxed{V^2=U,\qquad V^4=I},
\]

with cycle

\[
I\to V\to U\to V^\dagger\to I.
\]

This gives an exact four-phase internal graph clock. The physical clock frequency is set by the engineered coupling multiplying `L`; it is not set by, and does not modify, vacuum light speed.

## Pass 3996 — tensor incidence tower and asymptotic dark fraction

For a genuine `m`-fold independent carrier,

\[
\operatorname{rank}(N^{\otimes m})=25^m,
\]

\[
\dim\ker(N^{\otimes m})=40^m-25^m.
\]

Thus the one-side dark fraction is

\[
\boxed{1-\left(\frac58\right)^m}.
\]

Only `m+1` nonzero singular shells occur. If `r` tensor factors lie in the `sqrt(6)` sector, then

\[
\operatorname{mult}(m,r)=\binom mr24^r,
\qquad
\sigma^2(m,r)=16^{m-r}6^r.
\]

At level eight the dark fraction is approximately 0.9767169356. This is exact spectral/control compression; the physical carrier still grows as `40^m`.

## Evidence boundary

### Exact and promoted

- the 80-mode, 160-edge, degree-four, girth-eight incidence lift;
- `NN^T=4I+A` and the complete incidence spectrum;
- exact dual-geometry projectors, moment tomography, and commuting-error echo;
- all 945 maximum codes and their three parent-group orbits;
- the 877-element central partition lattice and 198 inequivalent types;
- the 30-dimensional dark sector, order-four Floquet clock, and tensor dark-fraction law.

### Executable but externally pending

- the full orbital-basis primitive idempotent/character-table freeze;
- the Monster maximal-overgroup fusion and bounded explicit-word search;
- three manuscript PDF builds and remote workflow completion.

### Not claimed

- a fabricated photonic device or measured fidelity;
- literal hidden photon nodes or a mode-dependent vacuum `c`;
- global optimality of a physical layout;
- a Monster embedding without four explicit words;
- relation-level fusion classification from the central lattice alone.
