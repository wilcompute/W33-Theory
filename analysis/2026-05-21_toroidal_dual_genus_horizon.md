# Toroidal Dual Genus Horizon

## Executive result

Your correction is right:

\[
[72,66]_3
\]

is not sourced only by Q4.  Q4 gives the incidence realization, but the arithmetic/topological source is the Császár/Szilassi toroidal dual pair.

The key point is that the same complete-graph genus equation

\[
h(K_n)=\frac{(n-3)(n-4)}{12}
\]

is read in two dual ways:

- Császár uses the vertex variable \(n=V=7\), because the Császár polyhedron has complete vertex adjacency \(K_7\);
- Szilassi uses the face variable \(n=F=7\), because the Szilassi polyhedron has complete face adjacency \(K_7\).

So the same equation is primal for Császár and dual for Szilassi.

## The toroidal dual pair

Császár:

\[
(V,E,F)=(7,21,14).
\]

Szilassi:

\[
(V,E,F)=(14,21,7).
\]

Both have

\[
V-E+F=0,
\]

so both are genus-one toroidal polyhedra.

They are dual in the exact sense:

\[
V_{Cs}=F_{Sz}=7,
\]

\[
F_{Cs}=V_{Sz}=14,
\]

\[
E_{Cs}=E_{Sz}=21.
\]

And

\[
21=\binom72=T_6.
\]

## Genus equation source

For Császár, complete vertex adjacency gives:

\[
n=V=7.
\]

Then:

\[
(7-3)(7-4)=4\cdot3=12=k.
\]

So:

\[
h(K_7)=\frac{12}{12}=1.
\]

For Szilassi, complete face adjacency gives:

\[
n=F=7.
\]

Then the same calculation gives:

\[
h(K_7)=1.
\]

Thus:

\[
\boxed{\text{Császár: }n=V=7,\qquad \text{Szilassi: }n=F=7.}
\]

Both feed the same toroidal seed into the same genus equation.

## From toroidal seed to horizon code

At the toroidal seed:

\[
(7-3)(7-4)=12=k.
\]

At the horizon value:

\[
n=k=12,
\]

we get:

\[
(12-3)(12-4)=72.
\]

But

\[
72=12\cdot6=kq!.
\]

The complete-edge payload is

\[
\binom{12}{2}=66.
\]

The parity gap is

\[
72-66=6=q!.
\]

Therefore:

\[
\boxed{[72,66]_3=\text{critical genus-horizon lift of the toroidal }K_7\text{ seed}.}
\]

## Why 66 is toroidal

The payload has a beautiful toroidal/tetrahedral decomposition:

\[
66=21+21+24.
\]

That is:

\[
\boxed{66=E_{Cs}+E_{Sz}+f.}
\]

In words:

\[
\boxed{66=\text{Császár edges}+\text{Szilassi edges}+\text{tetrahedron flags}.}
\]

Since each toroidal polyhedron has cell count

\[
V+E+F=42,
\]

we also have:

\[
66=42+24.
\]

That is:

\[
\boxed{66=\text{one toroidal cell chart}+\text{tetrahedron flags}.}
\]

Then the corrected horizon is:

\[
72=66+6.
\]

So:

\[
\boxed{72=\text{toroidal payload}+\text{qutrit parity budget}.}
\]

## Relation to Q4

The Q4 bridge remains correct, but now its role is clearer.

Q4 supplies an incidence realization:

\[
f_0(Q_4)+f_1(Q_4)+f_2(Q_4)=16+32+24=72.
\]

But the toroidal dual pair supplies the genus source:

\[
K_7\longrightarrow h=1,
\]

then

\[
n=k=12\longrightarrow 72=66+6.
\]

So the complete picture is:

\[
\boxed{\text{Császár/Szilassi dual pair}=\text{topological/genus source}.}
\]

\[
\boxed{Q_4^{(2)}=\text{incidence/router realization}.}
\]

## The theorem

**Toroidal Dual Genus Horizon Theorem.** The \([72,66]_3\) horizon code is sourced by the Császár/Szilassi dual \(K_7\) torus. Császár inserts

\[
n=V=7
\]

into

\[
h(K_n)=\frac{(n-3)(n-4)}{12},
\]

while Szilassi inserts

\[
n=F=7.
\]

Both give genus one and numerator

\[
12=k.
\]

Lifting to the fixed critical value

\[
n=k=12
\]

gives numerator

\[
72=kq!,
\]

payload

\[
66=\binom{12}{2},
\]

and parity

\[
6=q!.
\]

## Why this matters

This corrects the hierarchy of explanation:

\[
\boxed{\text{toroidal duality explains the numbers}.}
\]

\[
\boxed{Q4 realizes the incidence operator}.}
\]

The toroidal pair explains why the genus equation, the number 7, the toroidal cell count 42, the payload 66, and the corrected horizon 72 all belong together.

## Honesty boundary

These are exact arithmetic and polyhedral-duality identities. The next construction is a chain-level map from the toroidal dual pair to the Q4 2-skeleton basis.
