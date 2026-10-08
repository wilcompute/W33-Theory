# Pass 11766 — compact-real reality firewall for the Hesse/E8 and Spin(10) selectors

Reservation: \`analysis/PASS11766_RESERVATION.md\`, commit \`7a8a13721\`.

This pass audits the **reality condition** implicit in Passes 11607 and 11609 against the physical compact-real E8 adjoint and the existing real Clifford-10 matrices. It distinguishes a valid complex spectral projector from a projection of the **original real carrier**. It provides a minimal real-linear repair with its added-field cost. All results are exact finite-dimensional linear algebra.

## 1. What the earlier passes proved

The external-A2 center acts on the complexified E8 adjoint as

\[
248_{\mathbb C}=86_{1}\oplus 81_{\omega}\oplus81_{\bar\omega}.
\]

The prior Hesse shell filter uses \(C=(U-U^\dagger)/(i\sqrt3)\), \(M=C^2\), and the supplied vacuum value \(W=\pm c\rho^6\), \(c=15/343\):

\[
H_{\rm shell}=\lambda(c\rho^6 M+WC)^2.
\]

Over \(\mathbb C\), one of the two matter 81s has a zero eigenvalue, while the other is penalized. That algebraic statement remains valid.

## 2. New compact-real firewall

An order-3 orthogonal action with nontrivial eigenvalues \(\omega,\bar\omega\) acts on a real two-plane in canonical form

\[
U=-\frac12 I+\frac{\sqrt3}{2}J,\qquad
J=\begin{pmatrix}0&-1\\1&0\end{pmatrix},\quad J^2=-I.
\]

Here \(C=-iJ\). Thus complex conjugation interchanges \(P_\pm=(I\pm C)/2\). A real vector in a single complex eigenspace must be zero: if \(P_+v=0\), conjugation forces \(P_-v=0\), and \(P_++P_-=I\).

Consequently **no nonzero compact-real E8 adjoint matter vector can be kept solely in one complex 81**. At a fixed nonzero real \(W\), the Hermitian complex filter fails to preserve the compact real 248. The actual 86+81+81 eigenmultiplicities are inherited from the previously certified external-A2 center. This producer checks their canonical real rotation-plane normal form, not all 248 E8 matrices anew.

The obstruction has a second proof: the real commutant of this irreducible rotation plane is \(\mathbb R[I,J]\), whose symmetric part is only scalar multiples of \(I\). It has no nontrivial real symmetric rank-one projector.

## 3. Independent exact check on the committed Spin(10) carrier

We reconstruct the **actual** ten 32×32 real gamma matrices from the committed \`w33_pass10961_albert_clifford9_gammas.json\`. Their volume element \(V=\Gamma_1\cdots\Gamma_{10}\) is real skew, \(V^2=-I\), and commutes with all 45 bivectors. The chirality involution \(\chi=iV\) is Hermitian but imaginary.

Ordinary compact-real conjugation sends \(\chi\mapsto-\chi\); it exchanges the two complex Weyl-16 eigenspaces. Thus neither projector \((I\pm\chi)/2\) preserves the original 32-real-dimensional carrier. This **does not** invalidate Weyl spinors as intrinsically complex physical fields.

## 4. Minimal real-linear repair and its price

Introduce a *second* real two-plane with \(J_{\rm aux}^2=-I\). Then \(S=J_{\rm carrier}\otimes J_{\rm aux}\) is a **real symmetric involution** and commutes with the relevant grading centralizer. The CP/reflection coset negates \(S\). The positive real filter

\[
H_{\rm real}=\lambda[c\rho^6(M\otimes I)+WS]^2
\]

is a real-linear operator. At the two Hesse vacua it has the same exact gap \(4c^2\lambda\rho^{12}=900\lambda\rho^{12}/117649\).

In the doubled E8 carrier \(248\otimes_{\mathbb R}\mathbb R^2\) (real dimension 496), the original 86 becomes 172 neutral real dimensions; the 324-dimensional real matter block splits into **162 real light +162 real heavy**. Supplying the auxiliary complex structure interprets the light matter as 81 complex dimensions. For the doubled Spin(10) carrier \(\mathbb R^{32}\otimes\mathbb R^2\), the corresponding split is **32 real light +32 real heavy**, equivalent to 16 complex light components *given* that auxiliary complex structure.

**This repair is an additional assumption.** It is not a projection of the original undoubled compact-real E8 adjoint, does not extend automatically to a full unbroken-E8 gauge-invariant mass, and does not produce a Lorentzian chiral fermion measure, anomaly inflow, a protected Higgs sector, four-dimensional gravity, or observed particle spectra. The relevant physical direction is to realize the extra complex structure through a genuine spin-c/bundle zero-mode construction, rather than inserting it by hand.

## Relation to literature and provenance

The reality and chirality warnings are consonant with Distler and Garibaldi, *There is no "Theory of Everything" inside E8*, [arXiv:0905.2658](https://arxiv.org/abs/0905.2658), although the present statement is narrower: it addresses these exact projectors on the **compact-real adjoint** and does not assert their general no-go theorem applies to every proposed larger architecture.

Source-bound producer: \`analysis/w33_pass11766_compact_real_selector.py\`; frozen certificate: \`data/PART_W33_PASS11766_COMPACT_REAL_SELECTOR.json\`; focused tests: \`tests/test_w33_pass11766_compact_real_selector.py\`.
