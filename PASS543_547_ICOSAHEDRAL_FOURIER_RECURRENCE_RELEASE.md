# Passes 543–547 — icosahedral image, switch fibre, antiunitary triality, Z/9 Fourier, and q=5 recurrences

This release executes the five directions opened after Pass 542. All statements below are finite exact certificates or explicitly delimited recurrence theorems.

## Pass 543 — the q=5 association-scheme image begins with all four A5 irreducibles

The 12-vertex icosahedral permutation module has adjacency polynomial

\[
(x-5)(x+1)^5(x^2-5)^3,
\]

hence decomposes as

\[
\mathbf 1\oplus \mathbf 3\oplus\mathbf 3'\oplus\mathbf 5.
\]

Let `L_i` be the first-order Heisenberg difference block produced by changing the section coordinate at the `i`-th antipodal class. Exact cyclotomic arithmetic gives

\[
\operatorname{tr}(L_iL_j)=-10\delta_{ij}.
\]

Therefore the linearized block map is injective on all 12 section directions. No A5 irreducible is missing: q=5 spectral collisions are nonlinear invariant collisions, not a representation-kernel effect.

The finite quadratic coefficient is even more rigid. Pair contributions are trace-orthogonal for distinct coordinates, and

\[
\operatorname{tr}N_c^2=
\begin{cases}
20-10t,&c=\pm1,\\
30+10t,&c=\pm2,
\end{cases}
\qquad t=\zeta_5+\zeta_5^{-1}.
\]

Thus `e_2=-tr(D^2)/2` depends only on the coordinate square-class histogram. This explains the first layer of blindness for the Pass-540 pair, whose coordinates are square-identical.

## Pass 544 — the fixed-magnitude spectral fibre is nonlinear

Fix the Pass-540 magnitude word and scan all `2^12=4096` vertex sign switches using exact cyclotomic characteristic polynomials. The result is:

- `98` distinct characteristic polynomials;
- exactly `80` sign words retain the original polynomial;
- the 80-word fibre is closed under global complement but is **not** closed under XOR;
- under the order-20 automorphism stabilizer of the magnitude pattern, enlarged by global complement, it splits into `18` orbits.

The Pass-540 weight-five switch belongs to an eight-word orbit. The target fibre has weight distribution

`1,2,3,4,4,14,24,14,4,4,3,2,1`

for weights `0,...,12`.

Cohomologically, vertex switching maps `F_2^12` onto the icosahedral cut space of dimension `11`; the graph cycle space has dimension `19`. Every closed-cycle sign observable is blind to the entire 12-cube, while the exact spectrum retains only 80 words. Hence “spectral switch kernel” is a nonlinear fibre, not a binary code.

## Pass 545 — half-spin fusion lifts antiunitarily

For q=3 representatives `D_+` and `D_-` of the two half-spin section orbits, let

\[
W_{jk}=\omega^{jk},\qquad \omega=\zeta_3.
\]

Exact Eisenstein arithmetic gives

\[
WW^*=3I,
\qquad
W\overline{D_+}W^*=3D_-.
\]

Therefore the normalized qutrit Fourier transform followed by complex conjugation is an antiunitary Clifford intertwiner between the two half-spin blocks. Plain unitary Fourier conjugation does not work.

Their characteristic polynomials agree,

\[
x^3-36x-81,
\]

whereas the vector orbit has

\[
x^3-9x.
\]

This gives the exact representation-level reason that the half-spin pair fuses spectrally while the vector member of the D4 triality triple does not. The order-three section-space triality remains outer and is not a single similarity of all three qutrit blocks.

## Pass 546 — exact C3^3 Fourier decomposition over Z/9

The reduction kernel

\[
K=\ker\bigl(SL(2,\mathbb Z/9)\to SL(2,3)\bigr)\cong C_3^3
\]

acts on the 40 antipodal coordinates. Fourier decomposition of that permutation module gives:

- trivial character with multiplicity `8`;
- `12` nontrivial characters with multiplicity `2`;
- `8` nontrivial characters with multiplicity `1`;
- `6` characters absent.

The dimensions sum to `40`. The first-order Z/9 Heisenberg map has exact Gram matrix

\[
-18I_{40},
\]

so every coordinate/Fourier mode that occurs survives in the linearized block image.

A nonlinear exact slice was also completed. Set deep anchors to zero and make the primitive offset constant on each of the four tetrahedral fibres, with values in `{0,3,6}`. The resulting 81 sections have **13** exact characteristic polynomials. The seven naive q=3 signed orbits split into characteristic-polynomial counts

\[
1,2,2,2,2,3,3.
\]

Thus the obvious constant-fibre embedding of the q=3 orbit table is not equivariant for the Z/9 characteristic image; Hjelmslev lifting already creates additional spectral classes.

## Pass 547 — an all-exponent q=5 theorem for the one-pair orbit

For a section with one nonzero antipodal coordinate, the difference block has

\[
\chi_D(x)=x\bigl(x^4-5\pi x^2+25u\bigr),
\]

where

\[
t=\zeta_5+\zeta_5^{-1},\qquad \pi=2-t,\qquad u=1-t,
\qquad \pi^2=5u.
\]

All odd traces vanish. Put `R_r=tr(D^(2r))` and `S_r=R_r/pi^(2r)`. Then

\[
R_r=5\pi R_{r-1}-25uR_{r-2}
\]

and direct recurrence induction gives

\[
S_r=2\bigl(F_{2r+1}+1\bigr)+2F_{2r}t.
\]

Its real norm is

\[
N(S_r)=
\begin{cases}
4L_r^2,&r\text{ even},\\
20F_r^2,&r\text{ odd}.
\end{cases}
\]

Using `v_5(F_r)=v_5(r)`, the complete valuation law is

\[
v_\lambda(\operatorname{tr}D^m)=\infty\quad(m\text{ odd}),
\]

and, for `m=2r`,

\[
\boxed{
v_\lambda(\operatorname{tr}D^{2r})=
\begin{cases}
4r,&r\text{ even},\\
4r+2+4v_5(r),&r\text{ odd}.
\end{cases}}
\]

The constant sections `c=1` and `c=2` have Galois-conjugate degree-five recurrences and therefore identical lambda-valuation sequences. The Pass-540 odd-switch pair has one identical exact degree-five recurrence for every exponent. No closed valuation formula is claimed for those two larger families yet.

## Validation boundary

All five scripts emit one immutable combined JSON certificate and pass 46 exact checks; the focused test suite has six tests. The release does not classify all 2,034,735 q=5 symplectic orbits, the full Z/9 image, or all recurrence families.
