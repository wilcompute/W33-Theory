# Pass 4938 — Adjoint root compiler and symmetry firewall

## Result

Pass 4938 turns the ten-dimensional adjoint offset register of Pass 4937 into
an exact additive compiler.  Native GAP proves that its smallest nonzero
`PGSp(4,3)` orbit is the set of all 80 rank-one elements of
`sp4(F3)`.  Every such element satisfies

\[
X^2=0,\qquad T_X=I+X\in Sp(4,3),\qquad |T_X|=3.
\]

The 80 elements are the two nonidentity members of the 40 long-root `C3`
subgroups already owned by BT881.  Their span is all of `sp4(F3)`.  Thus this
pass does not rediscover the 80 transvections: it identifies them exactly with
the primitive differences in the Pass-4937 adjoint offset register and derives
the resulting compiler geometry.

The theorem owner is
[`w33_pass4938_adjoint_root_compiler.g`](w33_pass4938_adjoint_root_compiler.g).
It uses exact arithmetic in GAP 4.12.1 and emits the deterministic certificate
[`PART_W33_PASS4938_ADJOINT_ROOT_COMPILER.json`](../data/PART_W33_PASS4938_ADJOINT_ROOT_COMPILER.json).

## 1. Literal bridge to symmetric forms

Let `J` be GAP's invariant symplectic form.  The map

\[
\Phi:sp_4(\mathbb F_3)\longrightarrow Sym_4(\mathbb F_3),
\qquad X\longmapsto JX
\]

is a linear bijection.  GAP constructs both ten-dimensional spaces and checks
the bridge has rank 10.  The trace pairing

\[
\langle X,Y\rangle=\operatorname{Tr}(XY)
\]

has rank 10 and determinant 1 modulo 3, and is invariant under the transported
`PGSp(4,3)` action.  This makes the Fourier calculation below intrinsic to the
adjoint carrier rather than a coordinate guess.

## 2. Signed-root compiler

Use all 80 rank-one roots as additive opcodes on `F3^10`.  The resulting
undirected Cayley graph has

| invariant | exact value |
|---|---:|
| vertices | `3^10 = 59049` |
| degree | `80` |
| diameter | `4` |
| distance distribution from zero | `[1, 80, 2340, 18720, 37908]` |

Exhaustive breadth-first search proves, for every pair of offsets,

\[
d(X,Y)=\operatorname{rank}(X-Y)
      =\operatorname{rank}\!\bigl(J(X-Y)\bigr).
\]

Consequently every offset has an optimal program of at most four signed-root
instructions.  This is an exact finite compiler theorem, not a heuristic
diameter estimate.

The Fourier spectrum is

\[
80^1,\quad 26^{1560},\quad 8^{21060},\quad
(-1)^{18800},\quad (-10)^{16848},\quad (-28)^{780}.
\]

GAP also freezes the full `17 x 17` equitable transition matrix on the Pass-4937
`PGSp` orbit classes.  Its characteristic polynomial is

\[
(t-80)(t-26)^2(t-8)^5(t+1)^4(t+10)^3(t+28)^2.
\]

Every row sums to 80 and the matrix satisfies detailed balance against the
exact orbit sizes.  The 17 orbitwise Fourier values are recorded in the JSON.

## 3. Constant-time orbit classifier

For an offset `X`, the following tuple separates all 17 `PGSp` classes:

\[
\left(
\operatorname{rank}X,
\chi_X(t),
m_X(t),
\delta(JX)\ \text{for even rank}
\right).
\]

Here `delta` is the square class in `F3` of a nonsingular maximal principal
minor of the symmetric form; the last entry is set to zero in odd rank.  The
certificate gives a canonical least-base-three representative, orbit size,
and stabilizer order for every class.

This locates the one collision left by characteristic and minimal polynomials:
the square-zero rank-two orbits of sizes 240 and 480 have identical polynomial
data but discriminants 1 and 2, respectively.

## 4. Chirality and the forward-only ISA

Restricting the frame group from `PGSp(4,3)` to `PSp(4,3)` refines the 17
classes to 21.  GAP proves that exactly the four odd-rank `PGSp` classes split,
and that every split is a negative pair:

\[
80=40+40,\qquad
4320=2160+2160,\qquad
5760=2880+2880,\qquad
8640=4320+4320.
\]

Choose the 40-root class with least coordinate code as the forward opcode
alphabet.  Its negative is the other 40-class, the two alphabets are disjoint,
and the forward class still spans all ten dimensions.  The directed Cayley
compiler has diameter 5 and distance distribution

\[
[1,40,820,10920,30420,16848].
\]

Let `r=rank(JX)`, let `delta_0=2` be the discriminant of a forward root, and
let `delta(JX)` be the discriminant of the nonsingular part.  Exhaustive GAP
evaluation of all 59,049 offsets proves

\[
\ell_+(0)=0,\qquad
\ell_+(X)=
\begin{cases}
r,&\delta(JX)=\delta_0^r,\\
r+1,&\delta(JX)\ne\delta_0^r.
\end{cases}
\]

Because the field has characteristic three, two repeats implement the inverse:
`X+X=2X=-X`.  The extra compiler step is therefore exactly the chirality
correction detected by the discriminant, not an unexplained BFS residue.

## 5. The symmetry firewall

Rank distance alone forgets most of the controller.  On symmetric forms GAP
constructs the linear group

\[
S\longmapsto aP^{\mathsf T}SP,
\qquad P\in GL_4(3),\quad a\in\mathbb F_3^\times.
\]

Its image on `Sym4(F3)` has order `24,261,120`.  GAP transports the actual
`PGSp` action through `X -> JX`, proves subgroup containment, and obtains the
exact index

\[
[G_{\mathrm{rank}}:PGSp(4,3)]=468.
\]

The larger group has only seven offset orbits, with sizes

\[
[1,80,780,1560,16848,18720,21060].
\]

The certified information-loss chain is therefore

\[
21\ \text{PSp classes}
\longrightarrow17\ \text{PGSp classes}
\longrightarrow7\ \text{rank/type classes}
\longrightarrow6\ \text{Cayley eigenvalues}.
\]

This is a firewall against a tempting over-read: the rank graph does **not**
recover the W33 controller.  It admits a constructed linear symmetry group
468 times larger.  The transported Lie bracket and similitude-frame data are
the structure that selects `PGSp` inside that larger rank-metric symmetry.
This pass does not claim that the constructed rank group is the full abstract
graph automorphism group.

## Prior-art boundary

- **BT881** owns the 40 long-root `C3` subgroups and their 80 nonidentity
  transvections.
- **Pass 3966** owns the earlier finite transvection compiler and its
  four-generator `PSp` closure.
- **Pass 4864** owns the explicit `Q10 ~= sp4(F3)` adjoint Lie algebra.
- **Pass 4937** owns the affine `PGSp` controller and its 17 offset orbit sizes.
- Kai-Uwe Schmidt's
  [*Symmetric bilinear forms over finite fields with applications to coding theory*](https://arxiv.org/abs/1410.7184)
  owns the odd-characteristic symmetric-form translation association scheme,
  its `GL`-orbit partition, and the general rank-distance framework.

The scoped contribution of Pass 4938 is their exact composition on the W33
adjoint carrier: the orbit-level transvection identification, complete
17-class classifier and transition quotient, exhaustive signed and forward
compiler laws, `PSp` chirality refinement, and the 468-index symmetry
firewall.

## Reproduction and boundary

```bash
gap -q -b analysis/w33_pass4938_adjoint_root_compiler.g
python3 -m pytest -q tests/test_w33_pass4938_adjoint_root_compiler.py
```

The witness reports `44/44 checks; status=PASS`.  The regression executes GAP
in a clean temporary directory, rejects syntax warnings, and requires the
rebuilt JSON to match the frozen certificate byte for byte.

This is an exact finite characteristic-three matrix, orbit, Cayley, and
compiler theorem.  It does not construct a HoloBox hardware opcode or timing
model, a security or isolation theorem, a continuum gauge field, a particle,
a mass, or a coupling.
