# BT1340–BT1344: Cartan, Atlas-standard, selector, and p-adic closure

## Scope

This packet contains exact finite-dimensional algebra and finite permutation computations. It does not promote a continuum, particle-physics, or hardware claim.

## BT1340 — Modular decomposition and Cartan data

Let \(\mathcal H_{\mathbb Z}\) be the primitive integral form of the literal 26-dimensional \(W(E_6)/S_5\) Hecke algebra. For each bad prime, the decomposition matrix is uniquely determined row-by-row by ordinary-to-modular trace congruences and simple dimensions. Independently, primitive idempotents are lifted inside \(\mathcal H_{\mathbb F_p}\), and the corner dimensions reproduce
\[
C_p=D_p^{\mathsf T}D_p.
\]

The Cartan matrices are
\[
C_2=\begin{pmatrix}1&0\\0&22\end{pmatrix},
\]
\[
C_3=\begin{pmatrix}
5&1&3&0\\
1&3&2&0\\
3&2&5&0\\
0&0&0&1
\end{pmatrix},
\]
and
\[
C_5=I_6\oplus
\begin{pmatrix}
2&1&1\\
1&1&0\\
1&0&2
\end{pmatrix}.
\]
The projective indecomposable dimensions are respectively
\[
(2,22),\qquad (9,6,10,1),\qquad (3,2,1,1,1,1,4,2,3).
\]
Thus the modular block algebra dimensions are \((4,22)\) at \(p=2\), \((25,1)\) at \(p=3\), and \((9,4,1,1,1,1,9)\) at \(p=5\).

## BT1341 — Exact Atlas-standard 20-dimensional model

Inside the literal 480-dimensional directed-edge carrier, the central character projector
\[
N_{20}=20\sum_{g\in W(E_6)}\chi_{20}(g)\rho(g)
\]
has rank 20 and satisfies
\[
N_{20}^2=51840N_{20}.
\]
A deterministic pivot basis produces exact rational matrices \(C,D\in\mathrm{GL}_{20}(\mathbb Q)\) for the Atlas standard generators with
\[
C^2=D^9=(CD)^{10}=I.
\]
Their class-trace vector is
\[
(20,4,4,2,5,-1,0,0,0,-2,1,1,1,-1,0,10,2,2,2,1,1,-1,0,0,-1),
\]
which is the frozen degree-20 row used by the literal carrier computation. The matrices are committed in machine-readable form under SHA-256
\[
\texttt{8d0c52cf1f962471be1ab6dc4d98af5bc397fe003cbf9660a819ac0572689deb}.
\]
The representation is faithful because the character takes its full degree only on the identity class. A GAP/AtlasRep comparison program is retained as an independent runtime surface; this packet does not call a queued job “passed.”

## BT1342 — Minimal cycle–idempotent selector

Literal dihedral cycle enumeration through length six gives a unique smallest nontrivial cycle orbit: the length-four orbit represented by
\[
(0,1,2,3),
\]
of size 120 and stabilizer order 432. Length-seven and length-eight representatives retain the exact Pass-1332 stabilizers 2 and 1.

Every directed-edge cycle operator transports to the three species-20 copies as \(C\otimes I_3\). Therefore a cycle does not itself choose a multiplicity coordinate; one must also choose a primitive idempotent in the internal \(M_3\) block. Such idempotents form an \(S_3\)-orbit of size three. Hence the smallest combined selector orbit under \(W(E_6)\times S_3\) is
\[
3\cdot120=\boxed{360},
\]
with stabilizer order
\[
432\cdot2=\boxed{864}.
\]
Any additional cycle constraints only shrink the stabilizer, so this is minimal within the literal length-three through length-eight frontier.

## BT1343 — p-adic lifting and filtration separation

Complete orthogonal primitive idempotent systems lift by Newton–Hensel to precision \(p^6\) for all three bad primes:
\[
2^6=64,\qquad3^6=729,\qquad5^6=15625.
\]
There is therefore no primitive-idempotent lifting obstruction. The actual obstruction is block splitting: characteristic-zero species fuse according to the decomposition matrices above.

The Smith saturation and Loewy radical filtrations are distinct. Their cumulative dimensions are
\[
\begin{array}{c|l|l}
p&\text{Smith cumulative ranks}&\dim(\mathcal H/J^k)\\\hline
2&(5,12,17,20,22,25,25,25,26)&(5,9,13,19,24,26)\\
3&(13,21,23,26)&(4,10,16,22,26)\\
5&(24,26)&(20,24,26).
\end{array}
\]
At \(p=5\), the Smith ranks agree with the shifted stages \(\mathcal H/J^2\) and \(\mathcal H/J^3\), but the raw filtrations are not indexwise identical.

## BT1344 — Manuscript closure

The theorem insert is compile-ready and has an idempotent integrator for both `w33_paper.tex` and `photonic_holonet.tex`. The current repository input closure was audited; the earlier missing-input report came from a stale local paper snapshot, while the referenced BT1480–BT1494 inserts are present on current `master`.

Local gates:

- four isolated exact component generators: PASS;
- merged deterministic certificate: PASS;
- focused tests: PASS;
- minimal theorem-insert LaTeX compile: PASS.

Full historical-paper builds and the independent GAP/AtlasRep comparison remain explicit GitHub Actions surfaces until their runs are observed.
