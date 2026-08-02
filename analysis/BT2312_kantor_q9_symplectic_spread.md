# Pass 2312 — the first non-Desarguesian control breaks the two-intersection law

Using the Ball–Zieve coordinate model over

\[
\mathbb F_9=\mathbb F_3[u]/(u^2+1),
\]

take the nonsquare \(n=1+u\). The regular spread uses

\[
g(x,y)=-nx,
\]

while the Kantor spread uses

\[
g(x,y)=-nx^3.
\]

The executable witness constructs all 82 lines in each spread, verifies that
each partitions all 820 points of \(PG(3,9)\), and checks total isotropy for the
same symplectic form.

The two spreads share exactly

\[
\boxed{28}
\]

lines. The reason is exact: equality of the affine lines requires \(x^3=x\),
whose solutions are the three elements of the fixed subfield \(\mathbb F_3\).
There are nine choices of \(y\), giving 27 affine common lines, plus the common
line at infinity.

Thus \(28\notin\{1,10\}\). The regular-orbit \(1\)-or-\((q+1)\) law is not a
universal law for all symplectic spreads.
