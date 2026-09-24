# Pass 409 — compact E8 control, cubic Jacobi algebra, and trialitarian descent

Pass 409 executes the reserved finite-algebra and virtual-hardware packet. Its
main result is a phase-controlled switch between a cubic-Jacobi boundary algebra
and full compact \(E_8\), with exact control, representation, arithmetic, and
scheduling witnesses.

No result below derives a continuum action, Standard-Model spectrum, measured
coupling, or laboratory energy scale.

## 1. A diagonal H27 weld generates compact E8 with two controls

On the committed Chevalley basis, define the anti-linear compact conjugation

\[
\sigma_c(h_i)=-h_i,\qquad
\sigma_c(e_\alpha)=
-\operatorname{sgn}K(e_\alpha,e_{-\alpha})e_{-\alpha}.
\]

All 30,628 unordered basis-bracket identities pass exactly. The fixed root
planes have Killing value \(-120\), while the split Cartan Killing matrix is
positive definite. The fixed real algebra therefore has negative-definite
Killing form and is \(\mathfrak e_{8(-248)}\).

For either diagonal H27 background \(x\), the compact pair

\[
A=x+\sigma_c(x),\qquad B=i(x-\sigma_c(x))
\]

generates all 248 directions. The equivalent complex pair
\(x,\sigma_c(x)\) closes exactly over \(\mathbb Q\), and independent
finite-field replays give the same \(86+81+81\) grading.

Executables:

- `analysis/w33_20260923_compact_e8_two_control.py`
- `analysis/w33_pass409_compact_e8_control.py`

## 2. Eight root channels are necessary and sufficient

A compact-conjugate control frame supported on \(k\) roots can generate Cartan
rank at most \(k\), so rank eight forces \(k\geq8\). The support

\[
\{16,19,23,31,153,190,216,228\}
\]

with amplitudes \((3,2,1,2,1,3,1,1)\) closes exactly to all 248 dimensions.
The selected-root matrix has determinant \(-1\), so these roots form an
integral basis of the \(E_8\) root lattice. Four independently found
eight-root witnesses also have determinant \(\pm1\) and close at both test
primes. Thus this architecture has the sharp support bound

\[
\boxed{k_{\min}=8}.
\]

Unimodularity is a necessary prefilter at the lower bound; it is not claimed
that every unimodular root basis works for every amplitude assignment.

Executable: `analysis/w33_20260923_compact_e8_sparse8.py`

## 3. The 24D branch is cubic Jacobi

The non-diagonal center/external closure \(L_{24}\) is perfect, has a
one-dimensional center, and has a nested ideal flag

\[
0\subset I_9\subset I_{15}\subset L_{24},
\qquad
I_9\cong\mathfrak h_4,\quad I_{15}\cong\mathfrak h_7.
\]

Its nine-dimensional Levi quotient has a three-dimensional centroid generated
by a root of

\[
\theta^3-\theta^2-53\theta-120,
\qquad
\operatorname{Disc}(K)=94557=3\cdot43\cdot733.
\]

Exact centroid and nilpotent witnesses identify

\[
S_9=L_{24}/I_{15}
\cong\operatorname{Res}_{K/\mathbb Q}\mathfrak{sl}_2(K),
\qquad
L_{24}\cong S_9\ltimes\mathfrak h_7.
\]

A GAP Levi-Malcev replay independently returns dimensions \(9+15\), Levi
derived dimension 9, and radical derived dimension 1. This rules out the
previously tempting \(A_2^3\) or trinification reading.

Executables:

- `analysis/w33_20260923_cubic_jacobi_residual.py`
- `analysis/w33_20260923_cubic_jacobi_centroid_exact.py`
- `analysis/w33_20260923_cubic_jacobi_levi.g`

## 4. The rational modules are restricted standard plus Asai cube

Let

\[
W_8=I_9/Z,\qquad U_6=I_{15}/I_9.
\]

Exact characteristic-zero linear algebra gives

\[
\operatorname{End}_{S_9}(U_6)=K,\qquad
\operatorname{Alg}(S_9|_{U_6})=M_2(K),
\]

and hence

\[
U_6\cong\operatorname{Res}_{K/\mathbb Q}(K^2).
\]

For the eight-dimensional module,

\[
\operatorname{End}_{S_9}(W_8)=\mathbb Q,\qquad
\operatorname{Alg}(S_9|_{W_8})=M_8(\mathbb Q),
\]

so it is absolutely irreducible. The irreducible cubic has nonsquare
discriminant, giving Galois group \(S_3\) on the three split \(A_1\) factors.
Among every dimension-eight highest-weight triple for
\(\mathfrak{sl}_2^3\), the only \(S_3\)-fixed one is \((1,1,1)\). Therefore

\[
\boxed{
W_8\cong\operatorname{TensorInd}_{K/\mathbb Q}(K^2)
}
\]

—the cubic tensor-induction representation conventionally called the Asai
cube.

The actual Heisenberg bracket form constructs the rational symplectic splitting

\[
I_{15}/Z
\cong
\operatorname{TensorInd}_{K/\mathbb Q}(K^2)
\;\widehat\oplus\;
\operatorname{Res}_{K/\mathbb Q}(K^2).
\]

The cross-pairing vanishes after exact orthogonalization; the two summands have
alternating ranks eight and six.

All 54 Levi actions preserve the six-dimensional complement exactly, with no
central leakage, and every cross-bracket with \(W_8\) is zero. A pivot minor
for the resulting 15-vector phase basis has determinant \(-1\). Thus

\[
\mathfrak h_7\cong\mathfrak h_4*_{Z}\mathfrak h_3.
\]

This is an exact virtual-machine ABI: an eight-coordinate Asai-cube data lane
and a six-coordinate restricted-standard control lane commute while sharing a
single central phase register.

Executable: `analysis/w33_20260924_trialitarian_asai_cube_descent.py`

## 5. The 18D core is the trialitarian D4 contact parabolic

Over a splitting field, the Levi becomes \(\mathfrak{sl}_2^3\) and \(W_8\)
becomes \((2,2,2)\). A direct \(D_4\) root census gives contact grades

\[
1,8,6,8,1
\]

and grade-zero semisimple part \(A_1^3\). The eight grade-minus-one weights are
all sign triples \((\pm1,\pm1,\pm1)\), with opposite triples pairing into
the unique Heisenberg center.

Henniart and Lomelí's trialitarian \(D_4\) construction supplies the rational
descent criterion: a cubic extension gives a Levi with derived group
\(\operatorname{Res}SL_2\), acting through cubic tensor induction. Our exact
Levi, module, and invariant alternating form meet that criterion. Hence

\[
S_9\ltimes I_9
\]

is abstractly the derived contact-parabolic Lie algebra of the trialitarian
\(D_4\) form attached to \(K\). The normal closure's \(S_3\) is the full
outer triality action. A coordinate conjugating matrix to one chosen rational
Chevalley presentation remains open.

Literature anchors:

- G. Henniart and L. Lomelí, [Asai cube L-functions and the local Langlands
  conjecture](https://arxiv.org/abs/1701.01516).
- M.-A. Knus and J.-P. Tignol, [Triality and étale
  algebras](https://arxiv.org/abs/0912.3405).

## 6. The quartic and ramified-prime structures agree with the descent

At the completely split primes 107 and 151,

\[
W_8\cong(2,2,2),\qquad
U_6\cong(2,1,1)\oplus(1,2,1)\oplus(1,1,2).
\]

The invariant dimensions on \(W_8\) in degrees \(1,2,3,4\) are

\[
(0,0,0,1),
\]

so the first nonconstant invariant is the Cayley
\(2\times2\times2\) hyperdeterminant after splitting.

The squarefree field discriminant makes \(\mathbb Z[\theta]\) the maximal
order and isolates exactly three ramified primes:

\[
\boxed{3,43,733}.
\]

At each one the centroid reduction has a
\(\mathbb F_p[\epsilon]/(\epsilon^2)\) factor. The reduced Levi acquires the
three-dimensional square-zero ideal \(\epsilon\mathfrak{sl}_2\), and its
Killing rank drops from nine to six. The control primes 103, 107, 109, and 151
remain étale. No particle, anomaly, resonance, or energy interpretation is
assigned to these primes.

Executables:

- `analysis/w33_20260923_cubic_jacobi_stu_split.py`
- `analysis/w33_pass409_cubic_ramification_audit.py`

## 7. The qutrit fibre has one explicit global constraint channel

For the corrected local six-dimensional Weil carrier \(\rho_6\) of the W33
point stabilizer \(H\),

\[
\operatorname{Ind}_{H}^{W(E_6)}\rho_6
=10\oplus60\oplus80\oplus90,
\]

while the orientation-signed edge module is

\[
15\oplus24\oplus30\oplus81\oplus90.
\]

Thus the equivariant Hom space is one-dimensional, and every nonzero map lands
in the unique degree-90 constraint constituent rather than the harmonic
degree-81 logical sector.

This is an actual matrix map: over \(\mathrm{GF}(103)\), MeatAxe constructs
an invertible \(90\times90\) matrix \(T\) satisfying

\[
M_{\rm ind}(g)T=T M_{\rm edge}(g)
\]

for all three frozen \(W(E_6)\) generators. The certificate freezes only
basis-invariant dimensions, rank, and equations; it deliberately omits
basis-dependent MeatAxe stdout.

Executables:

- `analysis/w33_20260923_qutrit_edge_triality_transducer.g`
- `analysis/w33_pass409_qutrit_edge_intertwiner.g`
- `analysis/w33_pass409_qutrit_edge_intertwiner.py`

## 8. The minimal frame compiles to six microframes

The rank-optimal eight-root compact frame has identical A/B conflict graphs.
Each graph contains a 3-clique and admits a 3-coloring, so its exact chromatic
number is three. One complete control cycle therefore needs

\[
\boxed{3A+3B=6\text{ microframes}=432\text{ ticks}}.
\]

Five cycles exactly fill the existing 30-microframe, 2160-tick \(E_8\)
Coxeter bus, and 120 cycles fill the 51,840-tick global window. Every batch is
a commuting root-plane macro. Analog pulse amplitude, bandwidth, loss,
crosstalk, and wall-clock calibration remain outside the certificate.

Executable: `analysis/w33_pass409_sparse8_holonet_schedule.py`

## Synthesis and boundary

The exact finite hierarchy is now

\[
\boxed{
\text{trialitarian cubic-Jacobi boundary algebra}
\xrightarrow{\text{diagonal H27 phase weld}}
\mathfrak e_{8(-248)}
}
\]

with a sharp eight-root control frame and a unique qutrit-to-constraint
transducer. This closes an arithmetic, representation-theoretic, and scheduling
bridge. It does not derive spacetime dynamics or measured physics. The next
physical theorem must add a normalized Hamiltonian or action that selects this
finite structure and survives a stated experimental falsifier.
