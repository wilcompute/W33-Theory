# 2026-09-24 frontier — trialitarian D4 and cubic tensor induction

The Pass 409 cubic-Jacobi residual algebra has a sharper rational
identification than its split-prime STU fingerprint alone supplied. Let

\[
K=\mathbb Q(\theta),\qquad
\theta^3-\theta^2-53\theta-120=0,
\qquad \operatorname{Disc}(K)=94557,
\]

and let

\[
S_9\cong \operatorname{Res}_{K/\mathbb Q}\mathfrak{sl}_2(K)
\]

be the exact Pass 409 Levi quotient. The new certificate identifies both
noncentral Heisenberg modules over \(\mathbb Q\), rather than only after
reduction at split primes.

## 1. The six-dimensional companion is the restricted standard module

For \(U_6=I_{15}/I_9\), the exact commutant of the \(S_9\)-action has dimension
three. An explicit commutant matrix \(\Theta\) satisfies

\[
\Theta^3-\Theta^2-53\Theta-120I_6=0
\]

and has characteristic polynomial

\[
(\lambda^3-\lambda^2-53\lambda-120)^2.
\]

The action is faithful, and its associative envelope has rational dimension

\[
12=\dim_{\mathbb Q}M_2(K).
\]

Consequently

\[
\boxed{U_6\cong \operatorname{Res}_{K/\mathbb Q}(K^2)}
\]

as the restricted standard module, with
\(\operatorname{End}_{S_9}(U_6)\cong K\).

## 2. The eight-dimensional module is cubic tensor induction

For \(W_8=I_9/Z\), exact rational linear algebra gives

\[
\operatorname{End}_{S_9}(W_8)=\mathbb Q,
\qquad
\operatorname{Alg}(S_9|_{W_8})=M_8(\mathbb Q).
\]

Thus \(W_8\) is absolutely irreducible. The defining cubic is irreducible
with nonsquare discriminant, so its normal closure has Galois group \(S_3\).
After base change to that normal closure,

\[
S_9\otimes\overline{\mathbb Q}\cong\mathfrak{sl}_2^3,
\]

with \(S_3\) permuting the three factors. The executable enumerates every
highest-weight triple \((a,b,c)\) with
\((a+1)(b+1)(c+1)=8\). The only triple fixed by all of \(S_3\) is
\((1,1,1)\). Therefore

\[
\boxed{W_8\cong\operatorname{TensorInd}_{K/\mathbb Q}(K^2)}.
\]

At the algebraic-group or L-group level, this cubic tensor-induction
representation is conventionally called the Asai cube.

## 3. The Heisenberg phase space splits symplectically

The actual bracket form on \(W_8\subset I_{15}/Z\) has rank eight. Its
symplectic orthogonal complement has dimension six and maps isomorphically to
\(U_6\). The certificate constructs that complement exactly and verifies that
the cross-pairing has rank zero while the complementary alternating form has
rank six. Hence

\[
\boxed{
I_{15}/Z
\cong
\operatorname{TensorInd}_{K/\mathbb Q}(K^2)
\;\widehat\oplus\;
\operatorname{Res}_{K/\mathbb Q}(K^2)
}
\]

as a symplectic \(S_9\)-module. The hat denotes symplectic orthogonal direct
sum. The invariant alternating form on \(W_8\) is unique up to scale, so the
Heisenberg extension \(S_9\ltimes I_9\) is fixed up to central normalization by
the trialitarian tensor module.

The split is objectwise, not only an isomorphism of quotients. All 54 actions
of the nine rational Levi basis elements on the six complement vectors stay in
that complement with no central leakage, every cross-bracket with \(W_8\)
vanishes, and a 15-coordinate pivot minor for
\(W_8\oplus U_6^\perp\oplus Z\) has determinant \(-1\). Therefore

\[
\boxed{\mathfrak h_7\cong\mathfrak h_4*_{Z}\mathfrak h_3}.
\]

This gives an exact virtual-hardware ABI: an eight-coordinate tensor-induction
data lane and a six-coordinate restricted-standard control lane commute while
sharing one central phase register.

## 4. The 18D core is the rational trialitarian D4 contact parabolic

Henniart and Lomelí describe the standard trialitarian \(D_4\) construction
attached to a separable cubic extension \(E/F\): its relevant Levi has derived
group \(\operatorname{Res}_{E/F}SL_2\), and its eight-dimensional representation
is tensor induction from \(E\) to \(F\). The repo's exact finite algebra has
precisely these data:

\[
\operatorname{Res}_{K/\mathbb Q}\mathfrak{sl}_2(K)
\quad\text{acting on}\quad
\operatorname{TensorInd}_{K/\mathbb Q}(K^2),
\]

with the unique invariant alternating form furnishing the Heisenberg center.
The 18-dimensional core

\[
S_9\ltimes I_9
\]

is therefore the derived contact-parabolic Lie algebra of the trialitarian
\(D_4\) form attached to \(K\). This closes the rational descent that the
earlier split-prime root census left open; it does not yet freeze a
basis-conjugating matrix to a chosen rational Chevalley model.

Because the normal closure of \(K/\mathbb Q\) has Galois group \(S_3\), the
three split \(A_1\) factors are welded by the full outer triality group, rather
than by a chosen cyclic permutation.

## 5. Quartic and arithmetic consequences

Over a splitting field, \(W_8\cong(2,2,2)\) for \(SL_2^3\). Its first
nonconstant invariant is the quartic Cayley hyperdeterminant. The independent
split-prime replays at 107 and 151 recover invariant dimensions

\[
(0,0,0,1)
\]

in degrees \(1,2,3,4\). The primes \(3,43,733\) are exactly the bad-reduction
locus of this cubic triality descent, matching the previously certified
discriminant and dual-number degenerations.

## Literature anchors

- G. Henniart and L. Lomelí, [*Asai cube L-functions and the local Langlands
  conjecture*](https://arxiv.org/abs/1701.01516).
- M.-A. Knus and J.-P. Tignol, [*Triality and étale
  algebras*](https://arxiv.org/abs/0912.3405).
- M. Bremner, M. Bickis, and M. Soltanifar, [*Cayley's hyperdeterminant: a
  combinatorial approach via representation
  theory*](https://arxiv.org/abs/1106.5068).

## Evidence boundary

This is an exact finite/rational Lie-module descent theorem. “Asai cube” names
the representation-theoretic cubic tensor induction. It does not assert that
an automorphic L-function is physically realized, nor derive spacetime,
particle generations, couplings, black-hole entropy, or laboratory dynamics.

Executable: `analysis/w33_20260924_trialitarian_asai_cube_descent.py`  
Frozen data: `data/w33_20260924_trialitarian_asai_cube_descent.json`
