# Passes 5603–5610 — fusion closure, exact code distance, dynamical no-go theorems, and the old `s12` phase layer

This packet executes the five open targets after Pass5595–5602 and three additional outside-the-box probes. The user's `index.html` hint materially changed the search: `docs/index.html` still contains historical `s12` cards that route into the February ternary-Golay/Heisenberg program. In this report **`S_12` means the symmetric group on twelve letters; `s12` means the older 728-dimensional ternary-Golay construction.**

## Pass 5603 — the PSL2 fixed-point fusion closes symbolically

For odd prime powers `q>3`, let `G=PSL(2,q)` act on `P1(q)` and define relations on `G` by whether `g^{-1}h` fixes 0, 1, or 2 projective points. Pass5599 measured the valencies

\[
k_0=\frac{q(q-1)^2}{4},\qquad k_1=q^2-1,\qquad k_2=\frac{q(q+1)(q-3)}4.
\]

The standard projective-line character classification now yields the joint eigenmatrix

\[
\boxed{
P=\begin{pmatrix}
1&k_0&k_1&k_2\\
1&0&q-1&-q\\
1&-(q-1)^2/4&0&(q-3)(q+1)/4\\
1&q&-(q+1)&0
\end{pmatrix}}
\]

with multiplicities

\[
\boxed{1,\quad \frac{(q-3)(q+1)^2}{4},\quad q^2,\quad \frac{(q-1)^3}{4}.}
\]

The symbolic verifier proves

\[
P^{T}\operatorname{diag}(m)P=|G|\operatorname{diag}(1,k_0,k_1,k_2)
\]

identically and reconstructs every intersection number by

\[
p_{ij}^k=\frac1{|G|k_k}\sum_hm_hP_{hi}P_{hj}P_{hk}.
\]

Those expressions are exactly the polynomial intersection matrices measured in Pass5599. Thus the 0/1/2 fixed-point fusion is a symmetric 3-class Bose–Mesner algebra for every odd `q>3`.

The `q=3` specialization is stronger than the previous valency observation:

\[
\boxed{k_2=0,\qquad m_1=0.}
\]

So the generic algebra loses both one adjacency relation and one primitive idempotent. The surviving relations are the already identified `3K4` and `K4,4,4`. This is a genuine algebra degeneration at `q=3`, not a repeated integer.

Primary character-table background: Long–Plaza–Sin–Xiang, *Characterization of intersecting families of maximum size in PSL(2,q)*, arXiv:1608.07304, especially the projective-line action and character families in Section 2.

## Pass 5604 — exact all-odd minimum distance

Let `C+` be the binary projectivity code from the square determinant class and `C-` the opposite determinant class. Pass5601 proved

\[
C_-=C_+^\perp.
\]

Fix a support cell `c`. Exactly

\[
r=\frac{q(q-1)}2
\]

opposite-coset projectivity graphs pass through `c`. A second compatible cell lies with it on exactly

\[
\lambda=\frac{q-1}2
\]

such graphs; an incompatible cell lies with it on none. If a nonzero `C+` support `S` had size `s<=q`, then at least

\[
r-(s-1)\lambda
=\frac{q-1}{2}(q-s+1)>0
\]

opposite graphs would meet `S` exactly once, contradicting orthogonality to `C-`. Hence every nonzero word has weight at least `q+1`, and a generator projectivity row has weight exactly `q+1`.

Therefore

\[
\boxed{d(C_+)=d(C_-)=q+1}
\]

for every odd prime power `q`, so both sectors have parameters

\[
\boxed{[(q+1)^2,(q+1)^2/2,q+1]_2.}
\]

Independent symmetry-fixed HiGHS MILPs certify `d=8` at `q=7` and `d=10` at `q=9`. Equality in the counting bound also forces every minimum support to use distinct first and second coordinates, so every minimum support is a permutation graph. Which permutation graphs occur as codewords is a sharper remaining classification problem.

## Pass 5605 — Hodge and Hashimoto do not acquire a Weyl continuum in the maximally symmetric all-q family

Pass5388–5392 gives the exact Levi flag Hodge spectrum `L1=D^T D`:

\[
0^{q^4},\quad
(q+1-\sqrt{2q})^{q(q+1)^2/2},\quad
(q+1)^{q(q^2+1)},\quad
(q+1+\sqrt{2q})^{q(q+1)^2/2},\quad
(2q+2)^1.
\]

The total flag dimension is `(q+1)^2(q^2+1)`. Thus the full normalized spectral measure tends `delta_0`, because the `q^4` cycle sector asymptotically occupies the whole space. If that topological kernel is removed and the nonzero eigenvalues are divided by `q+1`, all macroscopic bands collapse to `1`; the reduced measure tends `delta_1`. There is no Weyl-law tower.

For a `k`-regular graph the nonbacktracking matrix `B` has an even stronger exact obstruction. Ordering incoming and outgoing directed edges vertex-by-vertex makes the local block `J_k-I_k`, so the singular values are

\[
k-1\quad(v\text{ times}),\qquad 1\quad(v(k-1)\text{ times}).
\]

Hence `BB^T` is always two-band. For the `W(3,q)` point graph, Ihara–Bass roots from adjacency eigenvalues `q-1` and `-(q+1)` converge, after `sqrt(k-1)` normalization, to finitely many unit-circle atoms, while the much larger extra `±1` Bass sector collapses to zero.

So neither maximally symmetric Hodge nor Hashimoto scaling yields a continuum spectral dimension. This does **not** rule out those operators after defects, phase twists, multiscale refinement, disorder, or transport symmetry breaking.

## Pass 5606 — selected 13-cover to F4 object map: fail-closed extraction gate

The previous action-level GAP test was still queued, so this packet does not infer an object map from the common abstract group. Instead it commits a stronger exact gate:

- `analysis/w33_pass5606_cover12_explicit_conjugator.g` rebuilds the exact 325-vertex Pass5417 graph and selected 13-cover, restricts to the moving twelve points, constructs the Klein-V4 Latin action independently, and asks GAP for an explicit conjugating permutation in `S_12`.
- `analysis/w33_pass5606_cover_to_f4_rootpair_map.py` composes that witness with the already proved `F4-short-root-pairs -> Latin` conjugator and emits a twelve-row object-level table.

The Python composer deliberately refuses to emit anything unless the GAP certificate says `conjugate_in_S12=true`. Until that replay finishes, the exact cover-to-root-pair bijection remains pending rather than silently promoted.

## Pass 5607 — a canonical finite d'Alembertian exists, but full projective symmetry kills dispersion

Let `X=P1(q)xP1(q)` and `n=q+1`. Because `PSL2(q)` is 2-transitive on each projective line,

\[
\operatorname{End}_{PSL_2(q)}\mathbb R[P^1(q)]
=\operatorname{span}\{I,J\}.
\]

Therefore the full product commutant on `X` has dimension four. Every completely `PSL2 x PSL2` invariant linear event operator has at most four joint spectral sectors.

The direct indefinite two-ruling analogue is

\[
\boxed{\square_q=(nI-J)\otimes I-I\otimes(nI-J).}
\]

Its spectrum is

\[
\boxed{0^{q^2+1}\oplus(+n)^q\oplus(-n)^q.}
\]

The mixed derivative `(nI-J) tensor (nI-J)` is even flatter: only `0` and `n^2`. Thus exact full projective symmetry is too restrictive to generate a dispersive wave equation. A physical operator must introduce phase/holonomy, directed transport, chart order, defects, or some other symmetry-breaking/refinement data.

## Pass 5608 — outside the box: the old s12 Golay 12-set is M12, not the new 576 action

The `docs/index.html` audit led back to `exploration/w33_s12_klein_projective_bridge.py`, where the 728 nonzero ternary Golay labels projectivize to 364 lines with Hamming-weight distribution

\[
132+220+\boxed{12}.
\]

That final twelve looked dangerous because the recent Reye/Latin/F4 action also has degree 12. The new verifier rebuilds the natural ATLAS `M12` generators, transports the Steiner `S(5,6,12)` design into the repo's Golay coordinates, finds the necessary monomial sign lifts, and acts on the twelve projective weight-12 Golay lines.

The induced group is

\[
\boxed{|M_{12}|=95,040}
\]

with orbitals

\[
\boxed{12,132.}
\]

So it is the natural 2-transitive Mathieu action, not the rank-3 order-576 action with orbitals `12,36,96`. ATLAS independently supplies a stronger group-theoretic firewall: none of the maximal subgroups of `M12` has order divisible by 576, hence `M12` contains no subgroup of order 576.

The two distinguished twelve-point objects therefore coexist at different symmetry layers and should not be identified.

## Pass 5609 — outside the box: the old s12 Heisenberg cocycle produces the spectral complexity we were missing

The old `s12` algebra work learned that grade-only coefficients fail Jacobi and that a symplectic/Weyl–Heisenberg phase restores associative closure. Apply that lesson directly to the `q=3` Segre event carrier.

On the 16 Segre events, join two cells exactly when both ruling coordinates differ. The untwisted rook-complement adjacency has only three eigenvalues:

\[
9^1\oplus1^9\oplus(-3)^6.
\]

Now use the W33 symplectic form

\[
B(x,y)=x_0y_1-x_1y_0+x_2y_3-x_3y_2\pmod3
\]

and weight an allowed edge by `omega^{B(x,y)}`, `omega^3=1`. Alternation makes the matrix Hermitian. Exact arithmetic in `Z[omega]` gives

\[
\chi(x)=(x+2)^2\bigl(x^{14}-4x^{13}-60x^{12}+244x^{11}+1292x^{10}-5517x^9-12212x^8+58256x^7+46617x^6-296670x^5-16992x^4+667170x^3-219780x^2-511272x+260496\bigr).
\]

It has 15 distinct real eigenvalues numerically; only `-2` is double. More importantly, the phase is not a gauge artifact: among the 96 event triangles,

\[
\boxed{60}
\]

carry nonzero `Z3` Wilson flux. The old `s12` cocycle therefore turns a 3-band maximally symmetric event operator into a genuinely multiscale magnetic/holonomy operator.

This is still finite kinematics, not a derived Lorentzian Hamiltonian. But it is the first result in this thread that explicitly repairs the spectral-flatness no-go by importing the old phase layer rather than adding another count.

## Pass 5610 — outside the box: explicit W33 -> old s12 Heisenberg phase embedding, plus a canonicity firewall

The older `s12/Klein` script proves real cardinality statements:

\[
728/2=364=|PG(5,3)|,
\]

and the projective Golay weight split `132+220+12`. It does **not** construct a canonical Pluecker/Klein isometry or canonically select the forty W33 points inside those 364 lines. The old Heisenberg script itself explicitly chooses a nondegenerate symplectic form on the systematic `F3^6` labels.

We can nevertheless make one exact chosen bridge. Embed the W33 four-coordinate symplectic space into the old three-qutrit phase space by

\[
\boxed{E(x_0,x_1,x_2,x_3)=(x_0,x_2,0,-x_1,-x_3,0).}
\]

For the old convention

\[
\langle(p,q),(p',q')\rangle=q\cdot p'-p\cdot q',
\]

one has identically

\[
\boxed{\langle E(x),E(y)\rangle=B(x,y)}
\]

for all `3^4 x 3^4 = 6561` pairs. Thus the Pass5609 phase is literally the restriction of the old `s12` Weyl–Heisenberg cocycle.

The important qualifier is **chosen**: this establishes compatibility, not uniqueness. A physical selection principle would still have to explain why this symplectic four-subspace and embedding are preferred.

## What this changes in the TOE program

The five requested attacks split the problem more sharply. The finite geometry now has a closed fixed-point Bose–Mesner sector and an exact half-rate code with exact distance, but the maximally symmetric Hodge, Hashimoto, and Segre wave operators all fail the same continuum test: too few spectral scales. The old `s12` work supplies the first concrete mechanism that repairs that defect—nontrivial Heisenberg holonomy—while simultaneously teaching us not to collapse every twelve-point object into the same symmetry class.

The next serious physical problem is therefore not another finite count. It is to determine whether a **phase-twisted, transport-sensitive tower** has a controlled large-scale dispersion/heat-kernel limit and whether its symmetry breaking can be derived rather than chosen.
