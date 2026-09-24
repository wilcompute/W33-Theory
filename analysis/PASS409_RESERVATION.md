# Pass 409 — compact E8, cubic Jacobi control, triality routing, and minimal root support

Pass 409 replaces its reservation marker with an executed theorem packet.  The
main result is a finite Lie-control switch with four independently replayable
layers:

1. a compact-real two-control theorem for the diagonal H27 weld;
2. an exact classification of the nondiagnonal 24-dimensional residual algebra;
3. a unique local-qutrit-to-global-constraint transducer;
4. a rank-optimal eight-root control frame for full compact E8.

No statement below derives a continuum action, Standard-Model spectrum, measured
coupling, or laboratory energy scale.

## 1. The diagonal H27 weld generates compact E8 with two fixed controls

On the committed Chevalley basis define the anti-linear compact conjugation by
[
sigma_c(h_i)=-h_i,qquad
sigma_c(e_alpha)=c_alpha e_{-alpha},qquad
c_alpha=-operatorname{sgn}K(e_alpha,e_{-alpha}).
]

All 30,628 unordered basis bracket identities pass exactly. The fixed root
planes have Killing value \(-120\), while the split Cartan Killing matrix is
positive definite; hence the fixed real algebra has negative-definite Killing
form and is the compact real form.

For either diagonal plus or minus H27 background \(x\), the exact compact
partner \(\sigma_c(x)\) closes to all 248 dimensions over \(\mathbb Q\), with
grading \(86+81+81\). Therefore
\[
A=x+\sigma_c(x),\qquad B=i(x-\sigma_c(x))
\]
are two fixed compact-real controls whose generated real Lie algebra is
\[
\boxed{\mathfrak e_{8(-248)}}.
\]

Executable: analysis/w33_20260923_compact_e8_two_control.py.
Frozen data: data/w33_20260923_compact_e8_two_control.json.

## 2. Eight root channels are necessary and sufficient

A compact-conjugate two-control architecture supported on \(k\) roots can only
generate roots in their root-lattice span. Its Cartan rank is therefore at most
\(k\). Since \(E_8\) has rank eight, \(k\ge8\).

An exact rational witness with support
\[
\{16,19,23,31,153,190,216,228\}
\]
and amplitudes \((3,2,1,2,1,3,1,1)\) generates all 248 dimensions.

The selected roots have determinant \(-1\) in the simple-root basis, so they
form an integral basis of the \(E_8\) root lattice. Four additional independently
found eight-root witnesses also have determinant \(\pm1\) and close at both
primes 103 and 109.

Thus, for this architecture,
\[
\boxed{k_{\min}=8}.
\]
Unimodularity is a necessary prefilter for an eight-root full-control frame; it
is not asserted that every unimodular root basis generates under every amplitude
assignment.

Executable: analysis/w33_20260923_compact_e8_sparse8.py.
Frozen data: data/w33_20260923_compact_e8_sparse8.json.

## 3. The 24D nondiagnonal branch is cubic Jacobi, not trinification

The residual closure \(L_{24}\) is perfect with one-dimensional center and has
a nested ideal flag
\[
0\subset I_9\subset I_{15}\subset L_{24}.
\]
Both proper ideals are Heisenberg:
\[
I_9\cong\mathfrak h_4,\qquad I_{15}\cong\mathfrak h_7,
\]
with commutator-form ranks 8 and 14 respectively.

The quotient \(S_9=L_{24}/I_{15}\) has nondegenerate Killing form and a
three-dimensional centroid over \(\mathbb Q\).

An exact centroid generator satisfies
\[
\boxed{\theta^3-\theta^2-53\theta-120=0},
\]
and PARI reduces the field to the same polynomial with discriminant
\[
\boxed{94557=3\cdot43\cdot733}.
\]
The field is totally real. An exact nilpotent in the three-dimensional
centroid-linear form has adjoint ranks \(6,3,0\), certifying the split
\(A_1\) form over its centroid field \(K\). Hence
\[
S_9\cong\operatorname{Res}_{K/\mathbb Q}\mathfrak{sl}_2(K).
\]

GAP independently constructs a rational Levi-Malcev decomposition with
dimensions \(9+15\), Levi derived dimension 9, and radical derived dimension 1:
\[
\boxed{L_{24}\cong S_9\ltimes\mathfrak h_7}.
\]
The tempting \(A_2^3\) / trinification identification is therefore false.

Executables:
analysis/w33_20260923_cubic_jacobi_residual.py,
analysis/w33_20260923_cubic_jacobi_centroid_exact.py,
analysis/w33_20260923_cubic_jacobi_levi.g.

## 4. After the cubic field splits, a three-qubit/STU invariant package appears

At the completely split primes 107 and 151, the centroid projectors separate
\(S_9\) into three commuting perfect 3D ideals. On
\[
W_8=I_9/Z,\qquad U_6=I_{15}/I_9,
\]
the action is exactly
\[
W_8\cong(2,2,2),\qquad
U_6\cong(2,1,1)\oplus(1,2,1)\oplus(1,1,2).
\]

Each \(A_1\) factor generates a four-dimensional associative algebra on
\(W_8\), while all three together generate dimension 64, the full matrix
algebra on eight dimensions. On \(U_6\), the three two-dimensional moved
subspaces are disjoint and the full associative algebra has dimension 12.

The polynomial invariant census on \(W_8\) is
\[
\dim \mathbb F[W_8]^{A_1^3}_d=(0,0,0,1),\qquad d=1,2,3,4,
\]
at both split primes. Since \((2,2,2)\) is the standard three-doublet tensor
representation, the unique quartic is the Cayley \(2\times2\times2\)
hyperdeterminant up to scale after scalar splitting.

This representation package is the familiar mathematical core used in the
three-qubit/STU literature; see M. J. Duff, arXiv:hep-th/0601134, and
L. Borsten et al., arXiv:0809.4685. The repo result is the appearance of that
package inside this residual control algebra, not a derivation of a black-hole
solution or entropy formula.

Executables:
analysis/w33_20260923_cubic_jacobi_char0_modules.py,
analysis/w33_20260923_cubic_jacobi_split107.py,
analysis/w33_20260923_cubic_jacobi_stu_split.py.

## 5. The qutrit fibre has one global edge channel, and it lands in constraints

Let \(H=3_+^{1+2}{:}GL(2,3)\) be the W33 point stabilizer and
\(\rho_6\) the corrected canonical Weil carrier. GAP gives
\[
\operatorname{Ind}_H^{W(E_6)}\rho_6
  =10\oplus60\oplus80\oplus90,
\]
while the signed 240-edge module is
\[
C_1^{\mathrm{signed}}=15\oplus24\oplus30\oplus81\oplus90.
\]

Therefore
\[
\boxed{\dim\operatorname{Hom}_{W(E_6)}
 (\operatorname{Ind}_H^{W(E_6)}\rho_6,C_1^{\mathrm{signed}})=1},
\]
and every nonzero map has image the unique degree-90 constituent.

Earlier exact repo work identifies this degree-90 block as the fused constraint
sector: its restriction to \(PSp(4,3)\) is the conjugate \(45+45\) pair,
whereas the harmonic logical block is degree 81. Thus the local qutrit Weil
carrier routes canonically to the global constraint sector, not directly to the
harmonic logical sector.

The three rational local 6D characters form one actual
\(\operatorname{Out}(H)\cong C_3\) orbit. The global 6D Weyl characters select
one local phase frame, while the 90D constraint representation contains the
other two. This is an exact 1+2 phase-frame routing law.

Executable: analysis/w33_20260923_qutrit_edge_triality_transducer.g.


## 6. The 18D core has the exact D4 contact-grading fingerprint

A self-contained D4 root census, using the standard roots
\(\pm e_i\pm e_j\) and grading by the central simple root, gives
root counts
\[
1,8,6,8,1
\]
in grades \(-2,-1,0,1,2\).  The grade-zero semisimple root subsystem is
\(A_1^3\), the eight grade-minus-one weights are all sign triples
\((\pm1,\pm1,\pm1)\), and they pair into four opposite-weight pairs
whose brackets land in the unique grade-minus-two root.

Hence the derived contact parabolic is
\[
\boxed{\mathfrak{sl}_2^3\ltimes\mathfrak h_4}
\]
of dimension \(9+8+1=18\), exactly matching the split fingerprint of the
repo core \(S_9\ltimes I_9\).  This proves the abstract graded fingerprint;
a single basis-conjugating matrix to a conventional D4 Chevalley basis remains
open.

Executable: analysis/w33_pass409_d4_contact_root_census.py.

## 7. The cubic descent has an exact three-prime branch locus

The centroid polynomial has squarefree discriminant
\[
94557=3\cdot43\cdot733,
\]
so \(\mathbb Z[\theta]\) is the maximal order and the Galois closure is
\(S_3\).  At each of the three ramified primes the centroid reduction is
\[
\mathbb F_p[\epsilon]/(\epsilon^2)\times\mathbb F_p,
\]
with a canonical nonzero square-zero \(\epsilon\).  Consequently the
nine-dimensional Levi reduction acquires the ideal
\[
\epsilon\mathfrak{sl}_2,
\]
of dimension three, and its Killing rank drops from nine to six.  The good
control primes 103, 107, 109, and 151 remain etale.

This makes \(3,43,733\) the exact arithmetic branch locus of the cubic
descent.  No particle, anomaly, resonance, or energy interpretation is inferred
from these primes.

Executable: analysis/w33_pass409_cubic_ramification_audit.py.

## 8. The transducer is an actual matrix, and the minimal control compiles in six microframes

The degree-90 overlap is not merely character-theoretic.  Over \(\mathrm{GF}(103)\),
MeatAxe constructs 90-dimensional submodules in the induced qutrit module and
the signed-edge module and an invertible \(90\times90\) matrix \(T\) such that
\[
M_{\rm ind}(g)T=T M_{\rm edge}(g)
\]
for all three frozen generators of \(W(E_6)\).  Thus the local qutrit fibre and
the global constraint lane share an explicit equivariant transducer.  A
characteristic-zero integral lift remains open.

The minimum eight-root compact-E8 frame has the same conflict graph for
controls A and B.  Each graph contains a 3-clique and admits an explicit
3-coloring, so the exact chromatic number is three.  Therefore one full AB
cycle needs exactly
\[
\boxed{3+3=6\text{ microframes}=432\text{ ticks}}.
\]
The existing 30-microframe / 2160-tick E8 Coxeter bus therefore carries exactly
five complete minimal AB cycles, and the 51840-tick global window carries 120.

Executables:
analysis/w33_pass409_qutrit_edge_intertwiner.g,
analysis/w33_pass409_qutrit_edge_intertwiner.py,
analysis/w33_pass409_sparse8_holonet_schedule.py.

## Synthesis

The exact finite structure now supports a phase-controlled hierarchy:
\[
\boxed{
\text{cubic-Jacobi boundary algebra}
\xrightarrow{\text{diagonal H27 phase weld}}
\mathfrak e_{8(-248)}
}
\]
with a rank-optimal eight-root compact control frame, while the local qutrit
point-stabilizer fibre has a unique equivariant route into the global 90D
constraint block.

That is a substantial algebraic/control bridge. It is not yet a theory of
spacetime dynamics or observed particle parameters. The remaining physical work
is to derive a Hamiltonian/action and experimentally normalized control map that
selects this finite structure rather than merely realizing it.
