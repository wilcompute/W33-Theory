# Passes 405–409 — Universal Critical Group, Full Qutrit Control, Sandpile Memory, Full Automorphisms, and the Sealed Hardware Falsifier

**Status: certified by executable witnesses, with physical claims explicitly excluded.**

This release executes the five orthogonal moves queued after Passes 400–404.

## Pass 405 — complete critical group for every odd prime

Let `Gamma_p` be the `p^3`-vertex Heisenberg bulk graph for an odd prime `p`.
Its critical group is now determined completely.

### The theorem

The characteristic-primary component is

\[
K(\Gamma_p)_{(p)}\cong
(\mathbb Z/p)^{(p^2-1)(2p-3)/3}
\oplus
(\mathbb Z/p^2)^{\binom p3}
\oplus
(\mathbb Z/p^3)^{p^2-2}.
\]

Write

\[
a=v_2(p-1),\qquad b=v_2(p+1).
\]

Then

\[
K(\Gamma_p)_{(2)}\cong
(\mathbb Z/2^a)^{p(p-1)}
\oplus
(\mathbb Z/2^{a+b})^{p(p-1)^2/2}.
\]

For an odd prime `ell != p`, semisimple Fourier separation gives

\[
\ell\mid p-1:
\quad
K(\Gamma_p)_{(\ell)}
\cong
(\mathbb Z/\ell^{v_\ell(p-1)})^{p(p^2-1)/2},
\]

and

\[
\ell\mid p+1:
\quad
K(\Gamma_p)_{(\ell)}
\cong
(\mathbb Z/\ell^{v_\ell(p+1)})^{p(p-1)^2/2}.
\]

These factors reconstruct the exact matrix-tree order

\[
p^{p^3+p^2-5}
(p-1)^{p(p^2-1)/2}
(p+1)^{p(p-1)^2/2}.
\]

### Integral Fourier proof

Set `R=Z_p[zeta_p]` and `pi=zeta_p-1`. Successive finite differences in
rows and columns transform the `p x p` Fourier matrix into Smith form

\[
\operatorname{diag}(1,\pi,\pi^2,\ldots,\pi^{p-1}).
\]

The nontrivial-central symplectic Fourier block is permutation-equivalent to
`F_p tensor F_p`. Its `pi`-exponent `s` therefore occurs with triangular
multiplicity

\[
m_s=
\begin{cases}
s+1,&0\le s<p,\\2p-1-s,&p\le s\le2p-2.
\end{cases}
\]

Before conductor gluing, this yields

\[
\frac{p(p-1)(2p-1)}3
\]

`p`-level generators and

\[
\binom{p+1}{3}
\]

`p^2`-level generators, while the trivial-central sector contributes
`p^2-2` additional `p^2` factors.

The normalization

\[
\mathbb Z_p[C_p]\hookrightarrow \mathbb Z_p\oplus R
\]

is a fibre product along the residue field. Its conductor matching removes
`p-1` first-level generators and `C(p,2)` second-level generators, promotes
the `p^2-2` trivial-sector factors by one `p`-adic level, and has index `p`.
The result is exactly the displayed `p`, `p^2`, and `p^3` multiplicities.

The witness checks every polynomial identity symbolically and agrees with the
full Smith forms/Bockstein certificates at `p=3,5,7`. It also emits the first
new closed instance at `p=11`:

\[
K(\Gamma_{11})_{(11)}
\cong
(\mathbb Z/11)^{760}
\oplus
(\mathbb Z/121)^{165}
\oplus
(\mathbb Z/1331)^{119}.
\]

## Pass 406 — minimally supported non-Abelian control and all 216 qutrit Cliffords

The commuting magnetic triangle of Pass 400 solves the central shift but does
not provide full local control. Pass 406 adds two fibre-local Hamiltonians:

\[
D=\operatorname{diag}(-4,-1,5),
\]

and

\[
K=|0\rangle\langle1|+|1\rangle\langle0|
 +|1\rangle\langle2|+|2\rangle\langle1|.
\]

Exact commutator closure gives

\[
\operatorname{Lie}_{\mathbb R}(iD,iK)=\mathfrak{su}(3),
\qquad \dim=8.
\]

This support is minimal in two independent senses:

1. one Hamiltonian generates only an Abelian one-parameter group;
2. a connected coupling graph on three modes requires at least two edges, and
   `K` uses exactly those two path edges.

The discrete compiler uses the projective Clifford model

\[
\mathbb F_3^2\rtimes SL(2,3),
\]

with hardware generators `X,Z,F,P`. Breadth-first enumeration produces all

\[
9\cdot24=216
\]

projective qutrit Cliffords. Every element has a shortest hardware word of
length at most seven. The exact length distribution is

| length | count |
|---:|---:|
| 0 | 1 |
| 1 | 4 |
| 2 | 13 |
| 3 | 32 |
| 4 | 56 |
| 5 | 65 |
| 6 | 40 |
| 7 | 5 |

A complete 216-entry hardware schedule is frozen in
`data/w33_pass406_qutrit_clifford_schedule.json`.

## Pass 407 — the critical group is an exact calibration memory

For the qutrit cell, take one mode as the reduced-Laplacian root. A unit pulse
moved from source mode `j` to target mode `i` defines the divisor

\[
e_i-e_j.
\]

Its persistent sandpile syndrome is

\[
L_{\rm root}^{-1}(e_i-e_j)\pmod{\mathbb Z^{26}}.
\]

Using the critical-group exponent `216`, the witness stores each coordinate as
an integer residue modulo `216`.

There are

\[
27\cdot26=702
\]

oriented single-slip errors, and **all 702 syndromes are distinct**. Therefore
a single unit pulse relocation can be decoded exactly, including its source
and target mode.

The minimum pairwise torus `L_infinity` separation is

\[
\frac{23}{216}.
\]

Consequently, every integer syndrome perturbation satisfying

\[
|\delta_k|\le11
\]

for every coordinate remains uniquely decodable.

The single-slip classes have only two orders:

| class | count |
|---|---:|
| order 72 | 54 |
| order 216 | 648 |

Thus a repeated uncompensated slip acts as a finite torsion clock. Applying the
inverse slip cancels the class exactly. This supplies a mathematically exact
persistent calibration-memory model; it does not assert that a fabricated
chip's analog errors automatically satisfy the eleven-tick bound.

## Pass 408 — the full unoriented automorphism group

For every odd prime power `q=p^f`, the full graph automorphism group is

\[
\boxed{
\operatorname{Aut}(\Gamma_q)
=H_q\rtimes\Gamma L(2,q)
}
\]

and therefore

\[
\boxed{
|\operatorname{Aut}(\Gamma_q)|
=q^3(q^2-1)(q^2-q)f.
}
\]

For a prime field, the explicit action is

\[
(u,z)\longmapsto
\left(Mu+a,
\det(M)z-\omega(Mu,a)+c\right).
\]

The proof is intrinsic to the graph:

1. distance three recovers the antipodal fibres;
2. triangle voltage vanishes exactly on collinear base triples;
3. every graph automorphism therefore induces an affine-plane collineation;
4. the fundamental theorem of affine geometry makes that map semilinear;
5. matching conjugacy forces the displayed common fibre multiplier and
   cocycle, leaving exactly `H_q semidirect GammaL(2,q)`.

At `q=3`, all `9!` base permutations were exhaustively tested: exactly `432`
preserve the affine lines, all are affine, and their three central lifts give
exactly `1296` graph automorphisms. There are no extras.

The crucial orientation result is

\[
\operatorname{Aut}(\Gamma_q)/
\operatorname{Aut}_{\det=1}(\Gamma_q)
\cong\mathbb F_q^\times.
\]

Hence the unoriented extension is only `C2` at `q=3`. At `q=5` its index is
four, not two; all nonzero central multipliers occur. The certified orders are

| q | full order |
|---:|---:|
| 3 | 1,296 |
| 5 | 60,000 |
| 9 | 8,398,080 |

## Pass 409 — vendor-neutral sealed hardware falsifier

The Pass-404 schedule has been converted into a vendor-neutral bill of
materials with explicit acceptance tests and empty cost/specification fields
for real engineering input. Its logical minimum includes:

- one heralded source;
- 27 phase-stable modes;
- 12 reusable programmable native couplers;
- nine magnetic triangles, equivalent to 27 directed couplers;
- nine balanced qutrit tritters;
- 27 independent phase channels;
- nine delay registers;
- 27 detector channels;
- one deterministic schedule controller.

The frozen physical protocol tests the four blinded gates

\[
I,\quad X,\quad Z,\quad F_3
\]

with target Choi visibilities

\[
1,\quad0,\quad0,\quad\frac13.
\]

The minimum preregistered design is eight replicates per gate, 3,000 shots per
phase, and the four phases `0,pi/2,pi,3pi/2`. Every gate must satisfy

\[
|\widehat V-V_{\rm target}|\le0.08,
\qquad
|\widehat Q|\le0.08,
\]

with calibrated visibility dilution at least `0.85`. All conditions must pass
simultaneously; no gate-specific post-hoc relaxation is allowed.

Distribution-free Hoeffding bounds certify the planned design's power against
both a stuck-identity device and a half-control device. A deterministic
nonclaim fixture is passed through the same file formats and is rejected by
production mode. The dedicated workflow also runs the existing Pass-397
`seal -> analyze -> unblind` pipeline in explicit test mode.

**No genuine laboratory counts were supplied. No physical experiment is
claimed.** The next physical action is to replace the fixture with externally
acquired counts and run Pass 397 without `--test-mode`.

## Validation surface

The release contains:

- five executable witnesses;
- seven primary certificates/artifacts plus the complete Clifford and slip
  decoder tables;
- a JSON Schema for the preregistered physical protocol;
- six cross-pass regression tests;
- a dedicated GitHub Actions release gate;
- strict no-physical-claim boundaries in every experimental artifact.
