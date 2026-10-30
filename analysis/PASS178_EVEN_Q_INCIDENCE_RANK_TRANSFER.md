# Pass 178 — Exact Even-(q) Incidence-Rank Transfer

Pass 171 computed

\[
\operatorname{rank}_2 M_q=10,50,298,1890
\quad(q=2,4,8,16)
\]

and used the fourth value to reject a cubic fit.  Four values still do
not determine a structural law: an earlier local draft interpolated them
with characteristic roots (1,6,13), but that expression is false at
(q=32).

The exact result is Theorem 1 of N. S. Narasimha Sastry and Peter Sin,
[“The Code of a Regular Generalized Quadrangle of Even
Order”](https://people.clas.ufl.edu/sin/files/the-code-of-a-regular-generalized-quadrangle-of-even-order.pdf).
For (q=2^n),

\[
r_n:=\operatorname{rank}_2M(2^n)
=1+\left(\frac{1+\sqrt{17}}2\right)^{2n}
 +\left(\frac{1-\sqrt{17}}2\right)^{2n}.
\]

## Integral transfer form

Set

\[
B=\begin{pmatrix}4&2\\2&5\end{pmatrix}.
\]

Its eigenvalues are

\[
\frac{9\pm\sqrt{17}}2
=\left(\frac{1\pm\sqrt{17}}2\right)^2,
\]

so the theorem has the exact integer form

\[
\boxed{r_n=1+\operatorname{tr}(B^n)}.
\]

Because (operatorname{tr}B=9) and (det B=16), Cayley–Hamilton gives

\[
r_n=9r_{n-1}-16r_{n-2}+8,
\]

or, after adjoining the constant root,

\[
r_n=10r_{n-1}-25r_{n-2}+16r_{n-3}.
\]

The exact continuation is

| (q) | (2) | (4) | (8) | (16) | (32) | (64) | (128) | (256) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| (operatorname{rank}_2M_q) | 10 | 50 | 298 | 1,890 | **12,250** | 80,018 | 524,170 | 3,437,250 |

The rejected four-anchor interpolation gives (12,794) at (q=32),
already (544) too large.  The transfer matrix therefore supplies both
the correct closure of Pass 171 and the first exact falsifier of the
numerological fit.

## Reproducibility and scope

- Witness: `analysis/w33_pass178_even_q_closed_form.py`
- Certificate: `data/w33_pass178_even_q_closed_form.json`
- Test: `tests/test_pass178_even_q_closed_form.py`

The repo witness rederives the (q=2,4,8) ranks from the finite
geometries, reads the independently computed (q=16) anchor from Pass
171, and then checks the theorem’s integral transfer and both recurrences.
It packages and regression-tests Sastry–Sin’s theorem; it is not claimed
as a new proof of that theorem.
