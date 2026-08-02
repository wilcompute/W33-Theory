# Pass 2314 — one pair of local orders, two incompatible controllers

Reduce the overlapping arithmetic generators \(R_4,U_6\) modulo two. Their
orders become \(2\) and \(3\), while their product has order \(7\). Exact closure
contains 168 matrices:

\[
\boxed{\langle\bar R_4,\bar U_6\rangle=GL(3,2)\cong PSL(2,7)}.
\]

The executable witness also checks simplicity by showing that the normal closure
of every nonidentity conjugacy class is the full 168-element group.

The quadratic Hom multiplicity controller has the same local generator orders
\(2,3\), but the product has order \(2\):

\[
\boxed{S_3=(2,3,2)}.
\]

Therefore the controller fork is

\[
(2,3,7)\quad\text{Fano routing/diagnostic mode},
\qquad
(2,3,2)\quad\text{quadratic phase-demodulation mode}.
\]

There is no quotient \(PSL(2,7)\twoheadrightarrow S_3\). These are different
closures of similar local ports, not the same controller at two resolutions.

For computer engineering this is a strong type-safety rule: a controller ABI
must record the product relation, not only the orders of its named generators.
