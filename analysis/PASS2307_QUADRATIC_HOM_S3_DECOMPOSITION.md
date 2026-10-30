# Pass 2307 — the complete quadratic map space is an exact \(S_3\)-module

## Result

Pass 2301 constructed all fifty \(PSp(4,3)\)-equivariant quadratic maps from
the signed-edge \(90\) into the targets \(15,24,30,81\), together with the
simultaneous phase action and outer involution on every multiplicity space.
Pass 2307 identifies the representation those data form:

\[
\boxed{
\mathcal H_{\mathrm{quad}}
\cong16\,\mathbf1\oplus16\,\mathrm{sgn}\oplus9\,\mathrm{std}
}
\]

as a module for

\[
C_3:C_2\cong S_3.
\]

The symmetric and alternating halves refine this to

\[
\boxed{
\mathcal H_{\mathrm{Sym}}
\cong13\,\mathbf1\oplus3\,\mathrm{sgn}\oplus5\,\mathrm{std}
}
\]

and

\[
\boxed{
\mathcal H_{\Lambda}
\cong3\,\mathbf1\oplus13\,\mathrm{sgn}\oplus4\,\mathrm{std}.
}
\]

This is the structural explanation of two numerical splits in the Pass-2301
certificate:

\[
50=25_{\mathrm{outer}+}+25_{\mathrm{outer}-}
   =32_{C_3\text{-fixed}}+18_{C_3\text{-rotating}}.
\]

The exact witness is
[`analysis/w33_pass2307_quadratic_hom_s3_decomposition.g`](analysis/w33_pass2307_quadratic_hom_s3_decomposition.g),
the frozen certificate is
[`data/w33_pass2307_quadratic_hom_s3_decomposition.json`](data/w33_pass2307_quadratic_hom_s3_decomposition.json),
and the focused regression is
[`tests/test_w33_pass2307_quadratic_hom_s3_decomposition.py`](tests/test_w33_pass2307_quadratic_hom_s3_decomposition.py).

## 1. Why the acting group is \(S_3\)

Let \(r\) be the simultaneous phase action on the two inputs of a quadratic
map and let \(s\) be the geometric outer involution.  Pass 2301 proves

\[
r^3=s^2=1,
\qquad
srs=r^{-1}.
\]

Thus \(\langle r,s\rangle=C_3:C_2\cong S_3\).  The original phase on the
\(90\)-carrier has order six, but its central sign acts twice on a bilinear
input and disappears.  The quadratic map layer therefore sees the order-three
phase quotient.  This is an exact logic-level reduction, not an assertion that
the order-48, order-24, and arithmetic controllers of Pass 2306 are the same
object.

## 2. Recovering an \(S_3\) character from four integers

For one target multiplicity space, let

- \(n\) be its dimension;
- \(f\) be the dimension fixed by \(C_3\);
- \(e_+\) and \(e_-\) be the outer-involution eigenspace dimensions.

Write its \(S_3\)-decomposition as

\[
a\,\mathbf1\oplus b\,\mathrm{sgn}\oplus c\,\mathrm{std}.
\]

Restriction to \(C_3\), and then to a reflection, gives

\[
n=a+b+2c,
\qquad
f=a+b,
\qquad
e_+-e_-=a-b.
\]

Hence the multiplicities are forced:

\[
a=\frac{f+e_+-e_-}{2},
\qquad
b=\frac{f-e_++e_-}{2},
\qquad
c=\frac{n-f}{2}.
\]

GAP applies these equations to every Pass-2301 target and independently asks
the ordinary character table of \(S_3\) to recognize the resulting class
functions as genuine characters.

## 3. Target-by-target decomposition

The entries below are \((\mathbf1,\mathrm{sgn},\mathrm{std})\):

\[
\begin{array}{c|rrrr|c}
&15&24&30&81&\text{total}\\ \hline
\mathrm{Sym}^2(90)
 &(3,0,0)&(4,0,1)&(2,1,1)&(4,2,3)&(13,3,5)\\
\Lambda^2(90)
 &(0,3,0)&(0,4,0)&(1,2,1)&(2,4,3)&(3,13,4)
\end{array}
\]

The corresponding characters on the GAP class order
\((1),(123),(12)\) are

\[
\chi_{\mathrm{Sym}}=(26,11,10),
\qquad
\chi_{\Lambda}=(24,12,-10),
\]

and therefore

\[
\chi_{\mathrm{quad}}=(50,23,0).
\]

The zero reflection trace is not an accidental cancellation.  It is equivalent
to the equality of the total trivial and sign multiplicities, both sixteen.

## 4. Why the outer split is exactly \(25+25\)

A reflection acts by \(+1\) on \(\mathbf1\), by \(-1\) on
\(\mathrm{sgn}\), and with one eigenvalue of each sign on every standard
two-dimensional copy.  Consequently

\[
\dim\mathcal H_{+}=16+9=25,
\qquad
\dim\mathcal H_{-}=16+9=25.
\]

Similarly, both one-dimensional representations restrict trivially to
\(C_3\), while each standard copy restricts as the two nontrivial cubic phase
characters.  Therefore

\[
\dim\mathcal H^{C_3}=16+16=32,
\qquad
\dim\mathcal H_{\mathrm{rot}}=2\cdot9=18.
\]

Thus one irreducible decomposition simultaneously explains both independent
Pass-2301 dimension ledgers.

The symmetric/alternating asymmetry is also exact in the representation ring:

\[
[\mathcal H_{\mathrm{Sym}}]-[\mathcal H_{\Lambda}]
=10\,\mathbf1-10\,\mathrm{sgn}+\mathrm{std}.
\]

No canonical operator exchanging the symmetric and alternating spaces is
claimed here; this identity records their characters only.

## 5. Scope and ownership

- Pass 2301 owns the fifty explicit orbit-tensor basis maps, their
  surjectivity, the full Hom dimensions, and the exact phase/outer matrices.
- Pass 2306 owns the separation of the abstract order-48 controller, canonical
  order-24 quotient, and infinite rank-three arithmetic carrier.
- Pass 2307 owns the induced \(S_3\)-character decomposition and the structural
  explanations of the \(25+25\) and \(32+18\) splits.

The integers \(16\) and \(9\) also occur elsewhere in the W33 corpus.  This
pass does **not** identify these representation multiplicities with an adjacency
rank, a generation count, or any other carrier merely because the integers
match.  The fifty maps are exact equivariant maps, not physical couplings.

The calculation uses the ordinary-character operations documented in the
[GAP Reference Manual](https://docs.gap-system.org/doc/ref/manual.pdf).

## Reproduce

```bash
gap -q analysis/w33_pass2307_quadratic_hom_s3_decomposition.g
python3 -m pytest -q tests/test_w33_pass2307_quadratic_hom_s3_decomposition.py
```

Expected GAP summary:

```text
Pass2307 status=PASS
Symmetric [trivial,sign,standard]=[ 13, 3, 5 ]
Alternating [trivial,sign,standard]=[ 3, 13, 4 ]
Combined [trivial,sign,standard]=[ 16, 16, 9 ]
outer_even_odd=[25,25] phase_fixed_rotating=[32,18]
```
