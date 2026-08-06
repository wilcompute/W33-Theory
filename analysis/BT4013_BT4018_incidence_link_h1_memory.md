# Passes 4013–4018: the physical incidence links carry the protected H1 memory

## Executive result

The 80-mode point–line incidence architecture introduced in Pass 3997 is not merely the lower-degree alternative to the direct 40-mode W33 coupler. Its **160 physical point–line couplers** have an exact cut/cycle decomposition

\[
160=79+81,
\]

and the 81-dimensional summand is precisely the canonical Hodge/Kirchhoff cycle space of the W33 Levi graph. Thus the same physical layout supports two mathematically distinct resources:

1. point/line mode dynamics on an 80-dimensional mode space; and
2. protected boundaryless link-current memory on an 81-dimensional subspace of the 160-dimensional coupler-current space.

The executed certificate is

```text
bf19623ed99a287cde193ec3315e5a7f86b101f4340a1546a9dee394904c5bd3
```

All exact checks pass.

## Pass 4013 — physical incidence-link H1 projector

Let \(L\) be the W33 point–line Levi graph. It has

\[
|V(L)|=80,\qquad |E(L)|=160,\qquad \deg L=4.
\]

Orient every incidence edge and let

\[
D\in\{-1,0,1\}^{80\times160}
\]

be the vertex–edge boundary matrix. Since \(L\) is connected,

\[
\operatorname{rank}D=79,
\qquad
\dim\ker D=160-79=81.
\]

Put \(K=D^TD\). Its exact spectrum is

\[
0^{81},\quad 8^1,\quad 4^{30},\quad
(4-\sqrt6)^{24},\quad(4+\sqrt6)^{24}.
\]

Therefore the integral polynomial

\[
\boxed{
320P_{H_1}
=(K-8I)(K-4I)\bigl((K-4I)^2-6I\bigr)
}
\]

satisfies

\[
(320P_{H_1})^2=320(320P_{H_1}),
\qquad
DP_{H_1}=0,
\qquad
\operatorname{rank}P_{H_1}=81.
\]

Because its image lies in \(\ker D\) and both have dimension 81, this is exactly the canonical orthogonal Hodge/Kirchhoff projector onto the physical link cycle space. Every link has diagonal weight

\[
(P_{H_1})_{ee}=\frac{81}{160}.
\]

This independently reconstructs the earlier BT547 cycle projector from the actual 160-coupler physical layout.

## Pass 4014 — exact link-memory reflection

The projector gives the exact involution

\[
\boxed{R_{H_1}=I-2P_{H_1}.}
\]

It acts as

\[
+1\quad\text{on the 79-dimensional cut space},
\]

\[
-1\quad\text{on the 81-dimensional boundaryless cycle-memory space},
\]

with total trace

\[
\boxed{\operatorname{Tr}R_{H_1}=79-81=-2.}
\]

This is an exact matrix gate on coupler-current coordinates. It is not a claim that a fabricated device already implements the polynomial.

## Pass 4015 — an independent two-step incidence revival

The raw Levi adjacency has spectrum

\[
-4^1,\quad(-\sqrt6)^{24},\quad0^{30},\quad
(+\sqrt6)^{24},\quad4^1.
\]

There is no nonzero exact global period for \(e^{-itA_L}\), because \(4/\sqrt6\) is irrational. Squaring folds the signs:

\[
H_2=A_L^2,
\qquad
\operatorname{Spec}(H_2)=0^{30}+6^{48}+16^2.
\]

Hence

\[
\boxed{e^{-i\pi H_2}=I,}
\]

\[
\boxed{e^{-i\pi H_2/2}=I-2E_6,}
\]

and

\[
\boxed{e^{-i\pi H_2/4}=I+(i-1)E_6}
\]

has order four and trace \(32+48i\).

This is distinct from Pass 4005’s exact finite-detuning block Hamiltonian. Both use the same incidence matrix \(N\), but they are different generators and should not be conflated.

## Pass 4016 — sign-resolved four-moment tomography

The raw adjacency has five signed sectors. Define

\[
a=p_{+4}+p_{-4},\qquad b=p_{+\sqrt6}+p_{-\sqrt6},
\]

\[
d=p_{+4}-p_{-4},\qquad e=p_{+\sqrt6}-p_{-\sqrt6}.
\]

From moments \(m_j=\langle A_L^j\rangle\),

\[
\boxed{a=\frac{m_4-6m_2}{160}},
\qquad
\boxed{b=\frac{16m_2-m_4}{60}},
\]

\[
\boxed{d=\frac{m_3-6m_1}{40}},
\qquad
\boxed{e=\frac{16m_1-m_3}{10\sqrt6}}.
\]

Then

\[
p_0=1-a-b,
\qquad
p_{\pm4}=\frac{a\pm d}{2},
\qquad
p_{\pm\sqrt6}=\frac{b\pm e}{2}.
\]

The rational synthetic test reconstructs all five populations exactly.

## Pass 4017 — centered delay recovers all 160 incidences

In the ideal model

\[
Q=\tau_{\rm common}I+\theta' A_L,
\]

common-delay removal yields

\[
\boxed{Q-\frac{\operatorname{Tr}Q}{80}I=\theta' A_L.}
\]

Thus the centered delay kernel recovers all 80 Levi vertices and all 160 point–line flags—not merely the 240 edges of the W33 collinearity graph.

This is an exact inverse in the ideal model. Measured scattering matrices, noise, loss, calibration drift, and finite-bandwidth identifiability remain experimental frontiers.

## Pass 4018 — mode memory and link memory are distinct

The architecture carries two non-equivalent decompositions:

\[
\mathbb C^{80}=E_0^{30}\oplus E_6^{48}\oplus E_{16}^{2}
\]

for the two-step mode Hamiltonian, while

\[
\mathbb R^{160}=\operatorname{cut}^{79}\oplus H_1^{81}
\]

for physical link currents.

The 48-dimensional mode middle sector, 30-dimensional mode kernel, and 81-dimensional link-cycle sector are different spaces. The breakthrough is architectural coexistence, not a dimension-based identification.

## Evidence boundary

Proved: finite geometry, spectra, exact integer projectors, ranks, involutions, ideal-model tomography inverses, and the identity of the physical-link cycle projector with the canonical Hodge projector.

Not proved: fabricated implementation, local synthesis cost of the projector polynomial, robustness to loss/disorder, measured Wigner–Smith data, laboratory timing, variable vacuum \(c\), literal hidden photon nodes, Monster embedding, remote CI, or PDF success.
