# Passes 3997–4004: photon layout, delay tomography, orbital Fourier, Monster execution, stabilizers, and three constructions

## Executive result

Five open fronts and three additional photon constructions were pursued. The physical-layout comparison, Wigner–Smith tomography model, and three maximum-code stabilizer identifications close exactly. Literal orbital Fourier/relation-fusion and Monster overgroup execution are supplied as self-publishing fail-closed workflows; their generated outputs remain pending.

Executed certificates:

- layout/tomography/edge memory: `ed4eddab150575ec2a719bc55974ac24e0b1852b1a3bec4a08204bc9114f4960`
- code stabilizers: `2bb684e7fcbfc8ca00e233c4955fc7a985c8aada6791c932599db10b4287598c`

## Pass 3997 — exact physical-layout competition

Both sparse architectures admit complete one-factorizations.

| architecture | modes | links | degree | disjoint coupling layers |
|---|---:|---:|---:|---:|
| direct W33 | 40 | 240 | 12 | 12 |
| point–line incidence lift | 80 | 160 | 4 | 4 |

The direct schedule consists of twelve perfect matchings of twenty couplers. The incidence schedule consists of four perfect matchings of forty couplers. Their frozen schedule hashes are `9c59e365c9c3fd771e65c63297e1558fd588cabb9e49401153ebb8708978c5fe` and `9c023abfbdc7dd4c7fa9c9c37e3bcae65c53dd600a381dda2d5409d7043d50c4`.

For linear fabrication cost

\[
C=\alpha(\#\text{modes})+\beta(\#\text{links})+\gamma(\#\text{layers}),
\]

\[
C_{40}-C_{80}=-40\alpha+80\beta+8\gamma.
\]

Therefore

\[
\boxed{C_{40}<C_{80}\iff5\alpha>10\beta+\gamma.}
\]

The direct architecture wins when mode count dominates. The incidence architecture wins when link count, node degree, or calibration layers dominate. The W33 spectral balanced-cut lower bound is 100 links; the incidence bound is \(20(4-\sqrt6)>31\). These are abstract congestion bounds, not planar crossing counts.

## Pass 3998 — Wigner–Smith tomography

For

\[
S(\omega)=e^{i\theta(\omega)L},\qquad Q=-iS^\dagger\partial_\omega S=\theta'(\omega)L,
\]

the three sector populations follow from \(m_1=\langle Q\rangle/\theta'\) and \(m_2=\langle Q^2\rangle/(\theta')^2\):

\[
p_{16}=\frac{m_2-10m_1}{96},\qquad p_{10}=\frac{16m_1-m_2}{60},\qquad p_0=1-p_{10}-p_{16}.
\]

A synthetic population `(0.17,0.51,0.32)` was reconstructed to floating-point precision. Three-frequency central differences showed second-order convergence with successive error ratios \(3.95237,3.98805,3.99701\). A brute-force full coherent transfer reconstruction uses forty input probes and 1,600 complex transfer amplitudes per frequency; at three frequencies this is 9,600 real scalar values before gauge reduction.

## Pass 3999 — literal orbital Fourier and relation fusion

The new exact harness executes the existing 48-orbital Fourier verifier, groups relation columns by their seven-character signatures, and refines that partition against every frozen multiplication coefficient until all fused products are constant on output blocks. It then tests every pairwise merger of the resulting closed blocks.

The workflow writes `data/PART_3983_ORBITAL_CENTRAL_FOURIER.json` and `data/PART_3999_ORBITAL_RELATION_FUSION.json`. No coefficient or relation-fusion count is promoted until that workflow commits its output.

## Pass 4000 — Monster execution escalation

The Monster workflow installs GAP character tables and `mmgroup`, clones the published maximal-subgroup generator database, composes `U4(2)` class fusions through maximal overgroups, performs the bounded order-three quadruple search, applies the strict final word gate, and records aggregate pool and quadruple counts. A negative bounded search is not an absence proof. No Monster embedding is promoted without four portable words and all object-action and class-fusion checks.

## Pass 4001 — exact stabilizer structures

The three fixed-parent maximum-code stabilizers are

\[
\boxed{G_{540}\cong S_4\times V_4.}
\]

Its six-coordinate action has image `S4`, kernel `V4`, and a commuting order-24 complement.

\[
\boxed{G_{270}\cong D_8\rtimes_{\operatorname{sgn},\alpha}S_4,}
\qquad \alpha:r\mapsto r^{-1},\quad s\mapsto r^2s.
\]

The action of the `S4` complement on `D8` has image two and kernel `A4`. This corrects the tempting but false direct-product identification.

Finally,

\[
\boxed{G_{135}\cong C_2\wr S_4=2^4:S_4=W(B_4).}
\]

Its faithful eight-coordinate action preserves four opposite pairs. Since the group and the full automorphism group of four disjoint pairs both have order 384, they coincide. This is an exact bridge from the extremal-code orbit to the four-dimensional hyperoctahedral/4-bit hypercube symmetry program.

## Pass 4002 — bonkers: delay tomography recovers geometry

Since \(\operatorname{Tr}L/40=12\),

\[
\boxed{Q-\frac{\operatorname{Tr}Q}{40}I=-\theta' A_{W33}.}
\]

The common-delay-free Wigner–Smith matrix is exactly the negative adjacency matrix, up to one scalar. Thresholding its off-diagonal entries reconstructs all 240 W33 edges. A delay experiment can therefore recover the finite geometry itself rather than merely its spectral multiplicities.

## Pass 4003 — bonkers: 240-edge cycle-memory processor

Let `D` be an oriented 40-by-240 vertex-edge incidence matrix. Then

\[
\operatorname{Spec}(D^TD)=0^{201}+10^{24}+16^{15}.
\]

Therefore

\[
\boxed{e^{-i\pi D^TD/2}=I-2E_{10}.}
\]

A single analog flight on the 240-edge carrier reflects precisely the 24-dimensional sector while leaving a 201-dimensional cycle-space kernel dark. The 201-dimensional raw graph cycle space is not the previously certified 81-dimensional Hodge/CSS logical space.

## Pass 4004 — bonkers: memory–metrology duality

For frequency estimation generated by `Q`, pure-state quantum Fisher information is

\[
F_Q=4\operatorname{Var}(Q).
\]

A localized vertex has Laplacian moments 12 and 156, hence

\[
\boxed{F_Q^{\rm vertex}=48(\theta')^2.}
\]

A cat state between the delay-0 and delay-16 sectors reaches

\[
\boxed{F_Q^{\rm opt}=256(\theta')^2.}
\]

The same delay spread interpreted as internal memory is exactly the metrological resource for estimating frequency-dependent evolution.

## Boundary

Proved: graph identities, one-factorizations, resource phase boundary, synthetic noiseless tomography, common-delay geometry recovery, edge-carrier spectrum/reflection, QFI laws, and the three stabilizer structures.

Pending: physical placement/routing, loss and disorder calibration, measured scattering matrices, literal orbital Fourier output, relation-level fusion output, explicit Monster words, laboratory performance, remote CI, and manuscript PDFs.
