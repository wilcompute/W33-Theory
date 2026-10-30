# Pass 174 — Dual Discriminant Fixed Rail and the Route-Hull E8 Shadow

## Result

Pass 174 continues Pass 173 on the two dark-lattice discriminant modules
and corrects the recent v4 cohomology interpretation.

For an order-eight generator (h) and the outer involution (	au), write

\[
\tau(h)=c h+u_c,
\qquad c\in\{1,3,5,7\}.
\]

The v4 address calculation used (c=5) and correctly found

\[
[u_5]=[4h]\ne0
\quad\text{in}\quad
H^1(C_2,A[2]).
\]

Its stated conclusion was wrong: this does **not** obstruct a fixed
order-eight rail.  Since

\[
u_1=\tau(h)-h=u_5+4h,
\]

the same equality implies ([u_1]=0).  Therefore an order-two shift
(h'=h+v) exists with

\[
\boxed{\tau(h')=h'.}
\]

The nonzero class obstructs only a *pure scalar-5 normal form*
(	au(h')=5h'), not a scalar-1 fixed generator.

## Exact address/route comparison

The complete computation gives:

| invariant | address dark lattice | route dark lattice |
|---|---:|---:|
| (A_2(L)) | ((\mathbb Z/2)^{14}\oplus\mathbb Z/8) | ((\mathbb Z/2)^8\oplus\mathbb Z/8) |
| actual coefficient of (h) in (	au(h)) | (5) | (1) |
| (dim\ker(1+\tau)) on (A[2]) | (9) | (5) |
| (dim\operatorname{im}(1+\tau)) | (6) | (4) |
| (dim H^1(C_2,A[2])) | (3) | (1) |
| shifts making (h+v) fixed | (512) | (32) |
| fixed shifts preserving (q=11/8) | (256) | (16) |

On both sides,

\[
[u_1]=0,
\qquad
[u_5]=[4h]\ne0.
\]

The verifier exhibits explicit fixed generators preserving (q=11/8).
Exactly half of all fixed shifts preserve (11/8); the other half give
(3/8).  Thus the celebrated (11/8) is a genuine value on one quadratic
orbit, but it is not invariant under arbitrary choice of order-eight
generator.

## The route quotient that Pass 173 had not yet named

Let

\[
R=\ker_{\mathbb F_2}N^{\mathsf T}=[40,15,10].
\]

Because (R\not\subset R^\perp), the address construction
(R^\perp/R) is undefined.  But the canonical hull

\[
H=R\cap R^\perp
\]

exists and is much stronger than a consolation quotient:

\[
\boxed{H=[40,9,16]}
\]

with exact enumerator

\[
1+135z^{16}+240z^{20}+135z^{24}+z^{40}.
\]

The all-ones word spans a fixed radical line.  The quotient

\[
\overline H=H/\langle\mathbf1\rangle\cong\mathbb F_2^8
\]

carries the nondegenerate quadratic form

\[
q([x])=\frac{\operatorname{wt}(x)}4\pmod2.
\]

It has (136) isotropic and (120) anisotropic vectors, so it is plus
type.  The native actions are faithful:

\[
|\PSp(4,3)|=25920,
\qquad
|\PSp(4,3){:}2|=51840,
\]

and both have the exact orbit split

\[
\boxed{1+135+120}
\]

on (overline H).  The nonzero stabilizers have orders (192) and
(216).

The same (136/120) quotient appears directly in the route discriminant:
(A_2(L_{\rm route})[2]) has (272) quadratic zeros and (240) ones,
and division by the fixed radical (langle4h\rangle) halves those counts.
This is an objectwise identification, not a count match: for every one of
the (512) hull words, the verifier expresses it in the integral route
lattice basis and proves

\[
\frac{c^{\mathsf T}G c}{4}
\equiv\frac{\operatorname{wt}(x)}4\pmod2.
\]

The all-ones word has lattice coefficient mask `0x7fff` and Smith
coordinate exactly ((0^8,4)=4h).

## The entire 255-vector capstone from one route code

On the (255) nonzero vectors of (overline H), polar-orthogonality
reconstructs

\[
\operatorname{SRG}(255,126,61,63).
\]

The quadratic split induces exactly

\[
\operatorname{SRG}(135,70,37,35)
\quad\sqcup\quad
\operatorname{SRG}(120,63,30,36).
\]

These are the full Pass-124 symplectic capstone and its isotropic and
anisotropic orthogonal subconstituents.  Therefore the single route code
([40,15,10]) now carries all three layers:

\[
\begin{array}{ccl}
R&:&432\text{ signed minima }\to216\text{ pentad cores},\\
H=R\cap R^\perp&:&[40,9,16]\text{ hull},\\
H/\langle\mathbf1\rangle&:&255=135+120\text{ plus-type capstone}.
\end{array}
\]

This is a second intrinsic route-side realization of the abstract
(E_8/2E_8) quadratic space.  It does not yet supply a chosen equivariant
isomorphism to every earlier (E_8/2E_8) realization; what is proved is
the exact quadratic form, native group orders and orbits, and all three
strongly regular graphs.

## Reproduction

```bash
python analysis/w33_pass174_dual_discriminant_fixed_rail.py
pytest -q tests/test_pass174_dual_discriminant_fixed_rail.py
```

Artifacts:

- `analysis/w33_pass174_dual_discriminant_fixed_rail.py`
- `data/w33_pass174_dual_discriminant_fixed_rail.json`
- `tests/test_pass174_dual_discriminant_fixed_rail.py`

The witness reports `PASS (66/66)`.  It uses exact Smith decomposition,
binary linear algebra, exhaustive finite orbit/coset censuses, and exact
strongly regular common-neighbor counts.  Its scope is finite lattice,
code, group-action, and cohomology mathematics; no continuum gauge field
or physical transport channel is inferred.
