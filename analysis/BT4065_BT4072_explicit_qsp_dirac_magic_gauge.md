# Passes 4065–4072 — explicit QSP, adaptive magic, Lorentzian Dirac dynamics, robust H1 control, gauge obstruction, and three outside-box probes

## Status

```text
PASS_EXPLICIT_QSP_ADAPTIVE_MAGIC_DIRAC_SK1_GAUGE_OBSTRUCTION_AND_THREE_BONKERS
342e8e7ae8f3ef06750716a1d3bdb25f2db432ee55e3ca35482086e16d6544ed
```

## Pass 4065 — explicit six-phase QSP sequence

Use the `Wx` convention

\[
W(x)=\begin{pmatrix}x&i\sqrt{1-x^2}\\i\sqrt{1-x^2}&x\end{pmatrix},
\]

\[
U_{\boldsymbol\phi}(x)=e^{i\phi_0Z}\prod_{j=1}^{5}\left[W(x)e^{i\phi_jZ}\right].
\]

For the exact bounded quintic from Pass 4049, one extracted phase vector is

\[
\boxed{
\boldsymbol\phi=(-2.8067951015434964,-2.042810210594929,-2.419664116537273,
2.419664116537273,-1.0987824429948638,-0.3347975520462967).
}
\]

It obeys

\[
\phi_0+\phi_5=-\pi,\qquad
\phi_1+\phi_4=-\pi,\qquad
\phi_2+\phi_3=0.
\]

On 20,001 uniformly spaced points in \([-1,1]\),

\[
\max_x |(U_{\boldsymbol\phi})_{00}-p_5(x)|
=1.1872\times10^{-15}.
\]

The maximum unitarity residual is below \(1.17\times10^{-15}\). Thus the compiler requires five signal queries and six phase gates in this convention.

A direct telescoping bound gives

\[
\boxed{\|\delta U\|\le6\delta_\phi+5\eta_W}
\]

when every phase error is at most \(\delta_\phi\) and every signal-query operator error is at most \(\eta_W\).

This is an explicit numerical phase certificate, not a fabricated block encoding or hardware calibration.

## Pass 4066 — adaptive irrational-magic correction and its exact resource law

The M36 reduction produces

\[
e^{i\phi}=\frac{-4+3i}{5},\qquad \phi/\pi\notin\mathbb Q.
\]

Ordinary injection applies either \(+\phi\) or \(-\phi\). If the undesired branch occurs, inject \(|A_{2\phi}\rangle\). A second failure is corrected with \(|A_{4\phi}\rangle\), and so on.

Two copies of \(|A_\theta\rangle\), an even \(Z\otimes Z\) parity result, and a CNOT produce \(|A_{2\theta}\rangle\) with probability \(1/2\).

After \(K\) correction levels,

\[
\boxed{p_{\rm fail}=2^{-(K+1)}}
\]

and the accepted deterministic channel satisfies

\[
\boxed{\|\mathcal E_K-\mathcal U_\phi\|_\diamond\le2^{-K}}.
\]

If the doubled-angle resources are available directly, the expected number of injected resources is

\[
2-2^{-K}<2.
\]

If every doubled-angle resource is recursively manufactured from the original M36 resource, the expected raw cost is

\[
\boxed{N_{\rm raw}=2^{K+1}-1.}
\]

For \(K=10\),

\[
p_{\rm fail}=\frac1{2048},\qquad
\|\mathcal E-\mathcal U_\phi\|_\diamond\le\frac1{1024},
\qquad N_{\rm raw}=2047.
\]

After all \(K\) corrections fail, the accumulated angle is

\[
-(2^{K+1}-1)\phi.
\]

Its difference from the target \(+\phi\) is \(-2^{K+1}\phi\), which is never a Clifford angle because \(\phi/\pi\) is irrational. Hence the doubling tree has no finite exact deterministic termination.

The infinite ladder succeeds almost surely and consumes fewer than two angle-labelled injections on average, but naïve recursive raw-resource production has divergent expected cost. This sharply separates angle-resource complexity from raw M36 complexity.

## Pass 4067 — a causal W33-fibered Dirac walk in 3+1 dimensions

Use three spatial lattice directions and discrete time. Let

\[
\beta=Z\otimes I,
\qquad
\alpha_j=X\otimes\sigma_j,
\]

so

\[
\{\alpha_i,\alpha_j\}=2\delta_{ij}I,
\qquad
\{\alpha_j,\beta\}=0.
\]

For W33 sector \(r\), define

\[
m_r=\sqrt{m_0^2+g\lambda_r},
\qquad
\lambda_r\in\{0,10,16\},
\]

with multiplicities \(1,24,15\). The exact momentum-space walk is

\[
\boxed{
U_a(p,r)=e^{-iam_r\beta}
 e^{-iap_1\alpha_1}
 e^{-iap_2\alpha_2}
 e^{-iap_3\alpha_3}.
}
\]

Each spatial exponential is a conditional nearest-neighbour shift. One macrostep therefore has finite support inside

\[
|\Delta x_j|\le1.
\]

For fixed physical momentum,

\[
\boxed{
\frac{U_a-I}{-ia}
=m_r\beta+\sum_{j=1}^{3}p_j\alpha_j+O(a).
}
\]

The verifier checks exact Clifford anticommutation and linear convergence for all three W33 mass sectors. This supplies a local unitary \(3+1\)-dimensional continuation. It does not derive the physical speed of light, curved geometry, interactions, or quantum gravity.

## Pass 4068 — SK1-protected H1 pulse words

Inside any calibrated logical two-level subspace of \(H_1\), let

\[
R_\chi(\theta)=\exp\left[-\frac{i\theta}{2}
(\cos\chi\,X+\sin\chi\,Y)\right].
\]

For a common fractional amplitude error \(\epsilon\), use

\[
\boxed{
U_{\rm SK1}=R_{-\chi}(2\pi(1+\epsilon))
R_{\chi}(2\pi(1+\epsilon))
R_x(\theta(1+\epsilon)),
}
\]

with

\[
\boxed{\chi=\arccos\left(-\frac{\theta}{4\pi}\right).}
\]

The first derivative of the error frame vanishes exactly at \(\epsilon=0\).

For a logical \(\pi\) pulse,

\[
\chi=\arccos(-1/4)
\]

and

\[
\boxed{
R_x(\pi)^\dagger U_{\rm SK1}
=I-i\frac{\sqrt{15}\pi^2}{8}\epsilon^2Z+O(\epsilon^3).
}
\]

Thus

\[
\|\delta U\|=rac{\sqrt{15}\pi^2}{8}\epsilon^2+O(\epsilon^3)
\]

and

\[
1-F_e=\frac{15\pi^4}{64}\epsilon^4+O(\epsilon^5).
\]

This is a projected-subspace amplitude-error theorem. Leakage, decoherence, bandwidth, and global 81-dimensional scheduling remain open.

## Pass 4069 — exact W33 gauge-commutant obstruction

The W33 permutation module decomposes as

\[
\mathbb C^{40}=\mathbf1\oplus V_{24}\oplus V_{15}.
\]

The full automorphism commutant is

\[
\boxed{
\operatorname{End}_{\operatorname{Aut}(W33)}(\mathbb C^{40})
=\operatorname{span}\{E_{12},E_2,E_{-4}\}
=\operatorname{span}\{I,A,J\}.
}
\]

It is commutative. Its unitary group is therefore

\[
\boxed{U(1)^3.}
\]

The most general invariant charge is

\[
Q=q_{12}E_{12}+q_2E_2+q_{-4}E_{-4}.
\]

A lattice link may transform covariantly under

\[
\psi_x\mapsto e^{i\alpha_xQ}\psi_x,
\qquad
U_{x\mu}\mapsto e^{i\alpha_xQ}U_{x\mu}e^{-i\alpha_{x+\mu}Q}.
\]

But the untouched W33 commutant cannot generate non-Abelian \(SU(2)\) or \(SU(3)\), nor can it mix the \(1,24,15\) sectors. A Standard Model gauge group therefore requires symmetry breaking, additional multiplicity spaces, or a larger noncommutative algebra. This is a no-go theorem, not a Standard Model construction.

## Pass 4070 — outside box I: anti-thermalization theorem

The exact reflection is

\[
U=I-2E_6,
\qquad U^2=I.
\]

Repeated applications generate an orbit of dimension at most two. For any initial density matrix,

\[
\overline\rho=P_+\rho P_++P_-\rho P_-.
\]

For a pure input, the time-averaged entropy is at most one bit. A localized vertex has weights

\[
p_+=\frac25,\qquad p_-=\frac35,
\]

so

\[
\boxed{S(\overline\rho)=H_2(3/5)=0.9709505944546686\text{ bits}.}
\]

The reflection by itself cannot generate a Page curve, Haar scrambling, or thermalization. Rich driven sequences or interacting dynamics are not covered by this no-go.

## Pass 4071 — outside box II: H1 frame metrology

A local projected perturbation has generator

\[
A_e=P|e\rangle\langle e|P
=\frac{81}{160}|u_e\rangle\langle u_e|.
\]

Its maximum single-site quantum Fisher information is

\[
\boxed{F_e^{\max}=\left(\frac{81}{160}\right)^2t^2.}
\]

Since

\[
\sum_eA_e=I_{H_1},
\]

for any pure probe

\[
\boxed{
\sum_eF_e=4t^2\left[\frac{81}{160}-\sum_e\mu_e^2\right],
\qquad \mu_e=\langle A_e\rangle,
\quad\sum_e\mu_e=1.
}
\]

Therefore

\[
\boxed{\sum_eF_e\le2t^2}
\]

and the maximum uniform-prior average is

\[
\boxed{\overline F\le\frac{t^2}{80}.}
\]

The bound is attainable: because the Levi graph is four-regular, it admits an Eulerian orientation with two incoming and two outgoing links per vertex. The corresponding equal-magnitude divergence-free flow belongs to \(H_1\) and has \(\mu_e=1/160\).

## Pass 4072 — outside box III: exact Kirchhoff tree entropy

The W33 Laplacian spectrum is

\[
0^1+10^{24}+16^{15}.
\]

The matrix-tree theorem gives

\[
\boxed{
\tau(W33)=\frac{10^{24}16^{15}}{40}=2^{81}5^{23}.
}
\]

The Levi Laplacian spectrum is

\[
0^1+(4-\sqrt6)^{24}+4^{30}+(4+\sqrt6)^{24}+8^1.
\]

Hence

\[
\boxed{
\tau(L)=\frac{8\,4^{30}\,10^{24}}{80}=2^{83}5^{23}.
}
\]

Therefore

\[
\boxed{\frac{\tau(L)}{\tau(W33)}=4.}
\]

The point-line incidence lift doubles the number of vertices but increases Kirchhoff complexity by exactly two bits. This is graph complexity, not gravitational entropy or physical microstate counting.

## Evidence boundary

The phase sequence, correction tree, Dirac walk, composite pulse, commutant obstruction, anti-thermalization bound, metrological budget, and tree counts are exact or deterministically certified in their stated models. No fabricated device, finite-cost exact deterministic irrational injection, logical fault-tolerance threshold, Standard Model, gravity, cosmology, or theory of everything is claimed.
