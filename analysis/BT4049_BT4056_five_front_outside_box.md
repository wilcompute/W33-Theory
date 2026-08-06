# Passes 4049–4056 — five physical closures and three outside-box probes

## Status

```text
PASS_EXACT_FIVE_FRONT_THREE_OUTSIDE_BOX_IDEAL_POSTSELECTED_UNIVERSALITY_CONTINUUM_AND_FT_PENDING
5f99f47f1a899b76c5e3e464a56440a63f51396a94c5d1ba9978ca65303b6946
```

This packet executes the five next steps listed after Passes 4025–4032 while respecting the independent Passes 4033–4040 and the reserved Passes 4041–4048. In particular, it does not duplicate the full 81-channel swap compiler or the proof that calibrated projected detunings generate \(\mathfrak u(81)\). It refines those results into a minimal bounded spectral compiler and an explicit pulse alphabet, then constructs a scaling family, a postselected non-Clifford reduction, and a finite-to-observable free-field dictionary.

The final three passes are deliberately orthogonal to the existing holonomy, interaction, refrigeration, refinement, supersymmetry, Floquet, and perfect-transfer tracks.

## Pass 4049 — the exact polar transform has a minimal degree-five QSVT compiler

Normalize the sparse Levi Hamiltonian by

\[
X=\frac{H_L}{4}.
\]

Its spectrum is

\[
\operatorname{spec}X=
\left\{-1,-\frac{\sqrt6}{4},0,
\frac{\sqrt6}{4},1\right\}.
\]

The target polar operator is \(\operatorname{sign}(X)\) on the four nonzero sectors and zero on the kernel.

### Why the exact cubic is not physically admissible as a QSVT polynomial

The unique odd cubic satisfying

\[
p_3(1)=1,
\qquad
p_3\!\left(\frac{\sqrt6}{4}\right)=1
\]

is

\[
\boxed{
p_3(x)=
\left(-\frac35+\frac{16\sqrt6}{15}\right)x+
\left(\frac85-\frac{16\sqrt6}{15}\right)x^3.
}
\]

It implements the exact sign values on the W33 spectrum, but it is not bounded by one on the complete block-encoding interval. Its maximum is

\[
\max_{x\in[-1,1]}p_3(x)
\simeq1.0921593487432213
\]

at

\[
x\simeq0.8139149086761249.
\]

Thus the cubic identity from Pass 4026 is an exact matrix polynomial, but it is not directly an admissible unit-normalized QSVT target.

### Exact bounded quintic

The minimal bounded odd solution is

\[
\boxed{
\begin{aligned}
p_5(x)={}&
\left(\frac9{25}+\frac{24\sqrt6}{25}\right)x\\
&+\left(-\frac{48}{25}-\frac{152\sqrt6}{225}\right)x^3\\
&+\left(\frac{64}{25}-\frac{64\sqrt6}{225}\right)x^5.
\end{aligned}
}
\]

It obeys

\[
p_5(0)=0,
\qquad
p_5(\pm1)=\pm1,
\qquad
p_5\!\left(\pm\frac{\sqrt6}{4}\right)=\pm1,
\]

and the interior spectral points are stationary:

\[
p'_5\!\left(\pm\frac{\sqrt6}{4}\right)=0.
\]

The exact boundedness certificate is

\[
\boxed{
1-p_5(x)^2=
\frac{4096(29-6\sqrt6)}{16875}
(1-x^2)\left(x^2-\frac38\right)^2q_+(x)q_-(x),
}
\]

where

\[
q_\pm(x)=x^2\pm\left(1+\frac{\sqrt6}{2}\right)x+
\frac{9+\sqrt6}{8}.
\]

Both quadratics are strictly positive because their discriminant is

\[
-2+\frac{\sqrt6}{2}<0.
\]

Therefore

\[
|p_5(x)|\le1
\qquad(-1\le x\le1).
\]

The polynomial is minimal among real odd QSVT targets. Degree one cannot take value one at both distinct positive spectral points. Degree three is uniquely fixed and overshoots. Hence the exact sign compiler has:

\[
\boxed{\text{query degree }5}
\]

and admits a six-phase QSP/QSVT realization once a block encoding of \(H_L/4\) is supplied.

This is stronger than the earlier cubic identity: it is an exact, globally bounded spectral transformation. The remaining engineering tasks are the actual block encoding, phase extraction under a selected QSP convention, and optical or microwave realization.

Quantum singular-value transformation guarantees polynomial transformations of a block-encoded operator subject to parity and boundedness conditions. The W33 result is the exact minimal polynomial specialized to this five-point spectrum; it is not a general QSVT theorem.

## Pass 4050 — exact local \(H_1\) phase gates and the four-angle pulse alphabet

Let

\[
P=P_{H_1}.
\]

The exact projector entries belong to

\[
\left\{
\frac{81}{160},
-\frac{27}{160},
\frac9{160},
-\frac3{160},
\frac1{160}
\right\}.
\]

For each physical link \(e\), define the normalized projected ray

\[
|u_e\rangle=
\sqrt{\frac{160}{81}}P|e\rangle.
\]

Every ray has unit norm. Relative to a fixed link, the other 159 rays have overlap distribution

\[
\begin{array}{c|cccc}
\langle u_e|u_f\rangle&-1/3&1/9&-1/27&1/81\\
\hline
\text{count}&6&18&54&81.
\end{array}
\]

A local projected detuning is

\[
A_e=P|e\rangle\!\langle e|P
=\frac{81}{160}|u_e\rangle\!\langle u_e|.
\]

Holding a physical detuning amplitude \(\delta_e\) for duration

\[
\boxed{
t_\phi=\frac{160\phi}{81\delta_e}}
\]

produces the exact protected-space phase gate

\[
\boxed{
U_e(\phi)=I+(e^{-i\phi}-1)
|u_e\rangle\!\langle u_e|.
}
\]

At \(\phi=\pi\), this becomes the Householder reflection

\[
\boxed{
R_e=I-2|u_e\rangle\!\langle u_e|.
}
\]

A product of two such reflections acts as a plane rotation. The exact primitive angle alphabet is

\[
2\arccos\frac13,
\qquad
2\arccos\frac19,
\qquad
2\arccos\frac1{27},
\qquad
2\arccos\frac1{81}.
\]

Pass 4034 already proved that the projected local controls generate

\[
\mathfrak u(81).
\]

The present pass supplies the missing pulse-level primitives: explicit duration, phase action, reflection gates, overlap classes, and two-pulse rotation angles. Consequently, calibrated piecewise-constant link detunings are an executable ideal control alphabet for the entire protected memory.

No optimal word compiler, bounded-amplitude schedule, leakage-canceling waveform, or fault-tolerance threshold is claimed.

## Pass 4051 — an explicit local four-dimensional scaling family

A fixed W33 cell has no continuum spectral dimension. To construct an actual scaling family without pretending dimension four emerges automatically, use the Cartesian-product graph

\[
\boxed{
G_n=W33\,\square\,C_n\,\square\,C_n\,
\square\,C_n\,\square\,C_n.
}
\]

It has

\[
|V(G_n)|=40n^4
\]

and constant degree

\[
\deg G_n=12+4\cdot2=20.
\]

Let \(L\) be the physical side length of each periodic base direction and \(M\) the internal W33 gap scale. Define

\[
\boxed{
\mathcal L_n=
M^2L_{W33}\otimes I+
I\otimes\left(\frac nL\right)^2
\sum_{\mu=1}^4 L_{C_n}^{(\mu)}.
}
\]

Its complete spectrum is

\[
\boxed{
M^2\lambda_r+\left(\frac nL\right)^2
\sum_{\mu=1}^4
\left[2-2\cos\left(\frac{2\pi k_\mu}{n}\right)\right],
}
\]

where

\[
\lambda_r\in\{0,10,16\}
\]

with multiplicities \(1,24,15\).

The heat trace factors exactly:

\[
\boxed{
\begin{aligned}
Z_n(t)={}&
\left(1+24e^{-10M^2t}+15e^{-16M^2t}\right)\\
&\times
\left[
\sum_{k=0}^{n-1}
\exp\left(
-\left(\frac nL\right)^2
\left(2-2\cos\frac{2\pi k}{n}\right)t
\right)
\right]^4.
\end{aligned}
}
\]

For

\[
M^{-2}\ll t\ll L^2,
\qquad
(L/n)^2\ll t,
\]

the internal excited modes are frozen while the base resolves a continuous four-torus. Rescaled discrete-torus heat kernels are known to converge to real-torus heat kernels, so this construction has

\[
d_s(t)\longrightarrow4
\]

in the controlled continuum window.

As a finite demonstration, for

\[
n=128,
\qquad L=32,
\qquad M=4,
\]

the running spectral dimension is

\[
\begin{array}{c|rrrrrr}
t&0.25&0.5&1&2&4&8\\
\hline
d_s&4.14493&4.06685&4.03228&4.01588&4.00787&4.00392.
\end{array}
\]

This resolves the earlier fixed-cell spectral-dimension obstruction by constructing a genuine family. It does **not** derive four dimensions from W33: the four-torus is an explicit base, and W33 is the internal fiber. Lorentzian causal dynamics, gravity, and a dynamical selection of the base remain open.

## Pass 4052 — one Witting state yields an exact irrational magic phase

Choose the Witting state

\[
|m\rangle=rac1{\sqrt3}(0,1,-1,1)
\]

in the computational basis

\[
|00\rangle,|01\rangle,|10\rangle,|11\rangle.
\]

Measure the first qubit in the \(X\) basis and retain the \(+\) result. The success probability is

\[
\boxed{p_{\rm prep}=\frac56}
\]

and the second qubit becomes

\[
\boxed{
|q\rangle=rac{-|0\rangle+2|1\rangle}{\sqrt5}.
}
\]

Apply the Clifford rotation

\[
R_x\!\left(\frac\pi2\right).
\]

Up to global phase, the result is the equatorial phase resource

\[
\boxed{
|A_\phi\rangle=rac{|0\rangle+e^{i\phi}|1\rangle}{\sqrt2},
}
\]

where

\[
\boxed{
e^{i\phi}=\frac{-4+3i}{5}.}
\]

Thus

\[
\cos\phi=-\frac45,
\qquad
\sin\phi=\frac35.
\]

The ratio \(\phi/\pi\) is irrational. If it were rational, the rational-cosine theorem would force the rational value \(\cos\phi\) to lie in

\[
\{0,\pm1/2,\pm1\},
\]

contradicting \(-4/5\).

### Exact postselected injection

For data

\[
|\psi\rangle=a|0\rangle+b|1\rangle,
\]

use \(|A_\phi\rangle\) as the target of a CNOT controlled by the data, then measure the resource qubit in the computational basis.

Outcome zero gives

\[
a|0\rangle+be^{i\phi}|1\rangle
=\operatorname{diag}(1,e^{i\phi})|\psi\rangle.
\]

Outcome one gives the inverse phase up to global phase. Each outcome occurs with probability \(1/2\), independent of the data. Postselecting outcome zero therefore gives total success probability

\[
\boxed{
p_{\rm total}=\frac56\cdot\frac12=\frac5{12}.}
\]

Because \(\phi/\pi\) is irrational, powers of \(R_z(\phi)\) are dense in the continuous \(z\)-axis subgroup. Clifford conjugation by \(H\) produces dense rotations about the \(x\) axis. The closures of these two nonparallel continuous one-parameter subgroups generate \(SU(2)\). Combining them with an entangling Clifford gate gives ideal postselected universal quantum computation.

This is a genuine closure relative to the previous fail-closed M36 ledger: M36 contains an exact non-Clifford universal resource under Pauli measurement, Clifford processing, and postselection.

It is not yet deterministic or fault tolerant. A practical protocol still requires handling the inverse outcome, logical encoding, noisy-state distillation or error correction, and an end-to-end threshold.

Bravyi and Kitaev established the general role of non-stabilizer ancillas in promoting Clifford computation to universality. The W33-specific result is the exact one-copy reduction, phase, and success probability above.

## Pass 4053 — an explicit finite-to-observable free-field functor

Use the base

\[
B_n=(C_n)^4
\]

and attach the W33 permutation module

\[
\mathbb C^{40}
\]

to each base vertex. The one-particle Hilbert space is

\[
\boxed{
\mathcal H_n=\ell^2(B_n)\otimes\mathbb C^{40}.
}
\]

Base nearest-neighbour transport acts trivially on the internal fiber. Full W33 automorphism invariance restricts a quadratic internal operator to the rank-three Bose--Mesner algebra

\[
\boxed{
\operatorname{span}\{I,A_{W33},J\}.
}
\]

The minimal invariant Klein--Gordon-type operator is

\[
\boxed{
K_n=\left(\frac nL\right)^2L_{B_n}\otimes I+
I\otimes\left[m_0^2I+g(12I-A_{W33})\right].
}
\]

It defines three exact free species sectors:

\[
\begin{array}{c|c|c}
\text{sector}&m_r^2&\text{multiplicity}\\
\hline
12&m_0^2&1\\
2&m_0^2+10g&24\\
-4&m_0^2+16g&15.
\end{array}
\]

For lattice momentum \(k=(k_1,\ldots,k_4)\), the propagator is

\[
\boxed{
G_r(k)=
\left[
m_0^2+g\lambda_r+\left(\frac nL\right)^2
\sum_{\mu=1}^4
\left(2-2\cos\frac{2\pi k_\mu}{n}\right)
\right]^{-1}.
}
\]

This supplies a non-arbitrary finite-to-observable dictionary at the free quadratic level:

- base position and translation become spacetime position and momentum;
- W33 spectral projectors become internal species labels;
- the Bose--Mesner selection rule restricts the invariant mass matrix to exactly three sectors;
- the scaling family supplies the continuum momentum limit.

It is not the Standard Model. There is no derived chirality, gauge connection, interaction vertex, generation assignment, symmetry breaking, or dimensional parameter prediction. The result identifies the precise first functorial layer that a more ambitious matter construction must extend.

## Pass 4054 — outside-box I: the exact reflection is a two-shell holographic beam splitter

The point-space reflection is

\[
U=-\frac{I+A}{3}+\frac{2J}{15}.
\]

For a localized input \(|v\rangle\), the amplitude is

\[
-\frac15
\]

on \(v\) and its 12 neighbours, and

\[
\frac2{15}
\]

on the 27 nonneighbours.

Define normalized shell states

\[
|N_v\rangle=\frac1{\sqrt{13}}
\sum_{u\in\{v\}\cup\Gamma(v)}|u\rangle,
\]

\[
|F_v\rangle=\frac1{\sqrt{27}}
\sum_{u\notin\{v\}\cup\Gamma(v)}|u\rangle.
\]

Then

\[
\boxed{
U|v\rangle=-\frac{\sqrt{13}}5|N_v\rangle+
\frac{2\sqrt3}{5}|F_v\rangle.
}
\]

The shell probabilities are

\[
\boxed{
P_N=\frac{13}{25},
\qquad
P_F=\frac{12}{25}.
}
\]

Thus the W33 reflection is an almost perfectly balanced two-output beam splitter between the closed-neighbourhood shell of size 13 and the far shell of size 27. The single-photon mode-partition entropy is

\[
\boxed{
H_2\!\left(\frac{13}{25}\right)
\simeq0.9988455359952018\ \text{bits}.
}
\]

Since

\[
U^2=I,
\]

the same operation recombines the shells exactly.

This provides a natural shell qubit and a directly testable spatial-amplitude signature. It is mode entanglement in a one-photon state, not a many-body holographic code, horizon, or gravity claim.

## Pass 4055 — outside-box II: the apartment frame is a five-angle projective code, not a 2-design

Normalize the 1620 signed apartment vectors in the 81-dimensional \(H_1\) space. They form a unit-norm tight frame of bound 20. Their absolute pairwise inner products belong to

\[
\boxed{
\left\{0,\frac18,\frac14,\frac38,\frac12,1\right\}.
}
\]

The exact ordered-pair census is

\[
\begin{array}{c|rrrrrr}
|\langle c_i,c_j\rangle|&0&1/8&1/4&3/8&1/2&1\\
\hline
\#&1{,}922{,}940&466{,}560&155{,}520&51{,}840&25{,}920&1{,}620.
\end{array}
\]

The first frame potential saturates the tight-frame bound:

\[
\sum_{i,j}|\langle c_i,c_j\rangle|^2
=32400=\frac{1620^2}{81}.
\]

The fourth-power frame potential is

\[
\boxed{
\sum_{i,j}|\langle c_i,c_j\rangle|^4
=\frac{79785}{16}.
}
\]

A real projective 2-design in dimension 81 would have value

\[
\frac{3N^2}{d(d+2)}
=\frac{97200}{83}.
\]

The exact defect ratio is

\[
\boxed{
\frac{F_2}{F_{2,\mathrm{design}}}
=\frac{16351}{3840}
\simeq4.25807.
}
\]

Therefore the apartments form a highly structured five-angle tight projective code but **not** a real projective 2-design.

This is an important falsifier. Tight-frame redundancy alone does not imply Haar isotropy, random-state behavior, or maximal scrambling. Any holographic or thermodynamic argument using the apartment frame must retain its exact high-order anisotropy.

## Pass 4056 — outside-box III: W33 has an exact spectral-calorimetry fingerprint

Treat the W33 Laplacian sectors

\[
0^1,
\qquad
10^{24},
\qquad
16^{15}
\]

as a finite single-particle spectrum in units of an energy scale \(J\). The canonical partition function is

\[
\boxed{
Z(\beta)=1+24e^{-10\beta}+15e^{-16\beta}.
}
\]

The internal energy is

\[
\boxed{
\frac{U}{J}=
\frac{240e^{-10\beta}+240e^{-16\beta}}{Z(\beta)}.
}
\]

The heat capacity is

\[
\frac C{k_B}=\beta^2
\left(\langle E^2\rangle-\langle E\rangle^2\right).
\]

It has a Schottky maximum at

\[
\boxed{
\beta_*\simeq0.4127094288166404,
}
\]

or

\[
\boxed{
\frac{k_BT_*}{J}\simeq2.422527756398217.
}
\]

The peak height is

\[
\boxed{
\frac{C_{\max}}{k_B}
\simeq3.8006256107565104.
}
\]

At the maximum,

\[
\frac UJ\simeq2.9816479655148593
\]

and the three sector occupation probabilities are approximately

\[
(0.71050504,\ 0.27504524,\ 0.01444972).
\]

The entropy runs from zero at low temperature to

\[
\ln40
\]

at high temperature.

This supplies a sharply falsifiable equilibrium fingerprint of the exact multiplicities \(1,24,15\). It could be tested through calibrated mode occupation or synthetic spectral calorimetry. It is not a measured response, and it does not include bosonic many-particle statistics or interactions.

## Five-front verdict

The five requested steps now stand as follows.

1. **Physical polar compiler:** exact minimal bounded degree-five QSVT target proved; phase extraction and block-encoding hardware remain.
2. **Executable \(H_1\) control:** exact phase gates, Householder pulses, overlap counts, and rotation alphabet proved; optimized robust schedules remain.
3. **Scaling family:** an explicit bounded-degree local family converging to a four-dimensional torus with W33 internal fiber is constructed; dimension four is input, not emergent.
4. **Non-Clifford closure:** one M36 state gives an irrational phase and ideal postselected universal computation with success \(5/12\); deterministic fault tolerance remains.
5. **Finite-to-observable map:** an exact free quadratic three-species functor and propagator are defined; Standard Model structure remains absent.

These are substantial physical and mathematical closures. They do not establish a fabricated universal machine or a theory of everything.

## Literature boundary

- Gilyén, Su, Low, and Wiebe, `arXiv:1806.01838`, provide the general QSVT framework for bounded parity-compatible polynomial transformations. The W33 minimal quintic is derived here.
- Bravyi and Kitaev, `quant-ph/0403025`, establish Clifford-plus-magic universality. The exact Witting-to-irrational-phase reduction is derived here.
- Chinta, Jorgenson, and Karlsson, `arXiv:0806.2014`, prove convergence of rescaled discrete-torus heat kernels to real tori. The W33-fibered four-torus family is defined here.
- Arrighi, Forets, and Nesme, `arXiv:1307.3524`, establish causal quantum-walk convergence to Dirac dynamics in higher dimensions. This motivates—but does not prove—the separate Lorentzian continuation still needed for the W33 fiber family.

## Evidence boundary

All promoted results are exact finite-dimensional algebra, graph spectra, pulse identities, postselected circuits, factorized heat traces, finite frame moments, or canonical finite-spectrum thermodynamics. No fabricated QSVT device, extracted phase list, deterministic injection, logical error threshold, Lorentzian spacetime, Standard Model, gravity, cosmology, measured calorimetry, or theory of everything is claimed.
