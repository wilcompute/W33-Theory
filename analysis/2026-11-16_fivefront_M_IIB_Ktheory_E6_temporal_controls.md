# Five independent TOE-front tests: flux limits, K-theory, SUSY, E6 dynamics, and temporal qutrits

**Date:** 2026-11-16. **Claim status:** Four mathematical/computational verifiers with regressions; one physical duality interpretation supplied by earlier work. No claimed TOE solution or full 11D spectrum classification.

**Source files examined before this pass:** `analysis/2026-11-16_D9_mtheory_uplift.md`, `analysis/2026-11-16_D9_iib_conifold_dual.md` (untracked local draft by another research track, not staged or modified), `analysis/2026-11-16_circle_bundle_ring_winding_staircase.md`, `analysis/toe_20261116_iib_circle_gysin_betti_BF_audit.py`, `analysis/toe_20261116_iib_weakcurvature_winding_control.py`, `analysis/2026-11-16_sevenfront_IIB_topology_W33_ancilla_F8_photonic.md`, and prior `analysis/2026_11_03_two_slot_quantum_memory_choi.py`. The wider repository was searched for related implementation and proofs. New results below are incremental relative to that material.

## A. Eleven-dimensional stability: approaching a BF-saturated equal-flux line

Earlier committed M-theory paper establishes the *homogeneous* scalar eigenvalue
`m_low^2 L^2=4-sqrt(64+320(eta-1/2)^2)`, where
`(N1/N2)^2=eta(2-eta)^2/((1-eta)(1+eta)^2)`.
It also derives the distinct nonzero-torus-momentum instability at exact equal mixed flux. We have not recomputed the entire coupled eleven-dimensional KK spectrum.

**New exact asymptotic:** Take positive integer charges `N1=N+1,N2=N,N0=N`. Differentiating the positive flux ratio at `eta=1/2` gives `d(N1/N2)/d eta=2/3`, hence `eta-1/2=3/(2N)+O(N^-2)`. Consequently
`m_low^2 L^2=-4-45/N^2+O(N^-3)`.
The high-precision verifier uses 65-digit Decimal bisection of the squared flux-ratio equation, and computes the gap as `320 delta^2/(sqrt(64+320 delta^2)+8)` to avoid cancellation. It reproduces `N^2*gap=44.9995499...` at N=100000.

**New physical-order warning:** Along that quantized family the eleven-dimensional curvature scale has `(L/lp)^3=(pi/8)N k1 k2 = O(N)`; the first known M-theory R^4 corrections are parametrically `(lp/L)^6=O(N^-2)`, **the same order as the classical BF deficit**. This is *not* a calculation of the correction to the mass, and its sign/coefficient are unknown. Thus an arbitrarily slight unequal-charge departure is classically BF-unstable but is not automatically a robust quantum-stability conclusion in a double-scaling limit. Fixed unequal ratios still have finite classical gaps.

Verifier: `analysis/toe_20261116_near_equal_flux_BF_scaling.py`. Certificate: `data/toe_20261116_near_equal_flux_BF_scaling.json`.

## B. Integral global charges: untwisted topological K-theory is richer than additive groups

Let `Y(p,q)` be the circle bundle over `S2 x S2` with Euler/Chern class `p x+q y`, not both zero, and `g=gcd(|p|,|q|)`. The existing ordinary integral Gysin calculation finds `H^2(Y;Z)=Z+Z_g, H^4(Y;Z)=Z_g`; our prior addition fixed its cup product.

The new **K-theory Gysin** result starts from `K^0(S2 x S2)=Z[X,Y]/(X^2,Y^2)` with `X=[L_x]-1,Y=[L_y]-1`. The Euler element is
`[L]-1=p X+q Y+pq XY`. The multiplication map in basis `1,X,Y,XY` has matrix
```
  0    0  0  0
  p    0  0  0
  q    0  0  0
  pq   q  p  0
```
whose nonzero Smith factors are `g,g`; rank is two. As `K^1(S2 x S2)=0`, the K-theory Gysin sequence proves
`K^0(Y)=Z^2 + Z_g + Z_g` and `K^1(Y)=Z^2`.

This addition is more than another additive tally. Put `a=p/g,b=q/g`; the torsion generator `u=pi*((1+X)^a (1+Y)^b -1)` satisfies
`u^2=2ab*w (mod g)` with `w=pi*(XY)` order g. Hence the K^0 rings for `(3,0)` and `(3,3)` differ: both have torsion `Z3+Z3`, but the former has `u^2=0`, the latter `u^2=2w !=0`.

**Scope:** This is *ordinary untwisted topological K-theory*. Do not identify this with the full RR charge lattice until background H-flux twists, quantization conventions, Freed–Witten constraints, dynamical brane endpoints, and differential K-theory have been imposed. Source: K-theoretic Gysin sequence of circle bundles, https://inspirehep.net/files/4eadf33259d623493f52eaba5c45ec90 ; topological T-duality, Bouwknegt–Evslin–Mathai, https://doi.org/10.1103/PhysRevLett.92.181601.

Verifier: `analysis/toe_20261116_iib_K_gysin_ring.py`. Certificate: `data/toe_20261116_iib_K_gysin_ring.json`.

## C. SUSY and spin: why a spin structure does not certify a supercharge

For every `Y(p,q)`, `TY` is stably `pi^*T(S2 x S2)+1`, so `w2(Y)=0`: all these oriented circle-bundle totals are spin. There are two spin structures iff `g` is even, and one otherwise. **This spin-structure count is not a Killing-spinor count.**

The previously derived local conifold Killing-spinor deck phases are `exp(±2 pi i/N)` for the equal charge quotient `T11/Z_N`. A lift shift by `-1` exists for even N. Rational-phase enumeration verifies that only N=1 (ordinary lift) and N=2 (alternate lift) retain a cover Killing spinor. N=4 is spin and has two spin structures but no invariant cover spinor. This is an *independent regression of an existing claim*, not discovery of a new SUSY family. It also does not settle the M/IIB spinorial duality dictionary because charged winding sectors need their own analysis.

The exact spin-lift tests are bundled with the K-theory verifier. Earlier repo anchor: `analysis/toe_20261116_iib_circle_gysin_betti_BF_audit.py`.

## D. Exceptional algebra dynamics: an exact cubic-only flat-direction obstruction

Under manifest trinification `SU3_A x SU3_B x SU3_C`, the E6 27 has three 3x3 matrix sectors `A,B,C`. Take the standard invariant cubic superpotential
`W=det A+det B+det C-Tr(ABC)`.

The verifier checks its exact invariance under nontrivial integer SL3 transformations and computes its F gradients via adjugates. Two transparent results:

1. **A-only obstruction.** Setting B=C=0, the F term demands `adj(A)=0`, so rank(A)<=1. Traceless SU3 moment-map D-flatness demands `A A^dagger` proportional to the identity, so rank(A)=0 or 3. Their only common solution is A=0. A rank-one F-flat vev thus cannot by itself solve the full F+D system.
2. **Three-link nonzero F+D-flat family.** For `A=B=C=s I3`, `s` arbitrary complex, `adj(A)=s^2 I` and `BC=s^2 I`: every F term vanishes. Each SU3 moment map also vanishes. Every nonzero `s` gives an unbroken diagonal SU3, **not** the observed Standard-Model group. Because F and D equations scale quadratically, a homogeneous cubic superpotential cannot fix the overall magnitude of any nonzero F+D-flat vacuum.

This provides a concrete *dynamics obstruction* for the naive cubic-only action; it does **not** rule out other E6 actions with soft terms, singlets, higher invariants, D terms, or a different symmetry-breaking sector. No particle masses have been predicted.

Verifier: `analysis/toe_20261116_e6_trinification_cubic_flat_branches.py`. Certificate: `data/toe_20261116_e6_trinification_cubic_flat_branches.json`.

## E. Photonic and temporal quantum information: two experimentally separable levels

The operational Markov definition uses a **causal break**: measure the qutrit, reset it to a chosen state independent of the outcome, then examine whether the future depends on the past. See Pollock et al., https://arxiv.org/abs/1801.09811 and the process-tensor review, https://doi.org/10.1103/PRXQuantum.2.030201 .

**Classical temporal memory null/control:** Choose uniformly random `h in F3`. Apply `X^h` in two separated slots, insert a computational measurement `j` and independent reset to `|0>`, then measure outcome `k`. For fresh independent h each slot (Markov), `P(j,k)=1/9`; for *persistent* h (environmental memory), `P(j,k)=delta(j,k)/3`. The one-slot channel is identical in both processes: the shift twirl, i.e. complete dephasing in the qutrit Fourier basis (entanglement-breaking). Yet `P(j=k)` changes from 1/3 to 1, and mutual information from 0 to log2(3). A hypothetical 24-trial result with at least 16 matches has exact binomial-tail P under the Markov null `~0.00085948` (fixed prespecified design, no real data). This verifies temporal *memory*, not quantum temporal entanglement.

**Coherent memory control beyond classical correlations:** Prepare a reference–system Bell qutrit state `|Phi3>` and an environment qutrit in `|0>`. SWAP system and environment, causally reprepare the system in `|0>`, then SWAP again. The environment carries the coherence across the break and the final Bell fidelity is exactly **1**. If the environment instead stores only the original computational basis label and later reprepares it, the reference–system state is `sum_j |jj><jj|/3`, giving Bell fidelity **1/3**. Both have identical final computational-basis coincidence statistics; only a phase-sensitive Bell analyzer distinguishes the quantum memory. Exact partial transpose of the coherent Bell state is SWAP/3, with three negative eigenvalues `-1/3`; the classical mixture has none.

This experiment **requires separately addressable reference/system/environment registers, coherent SWAP control and Bell analysis**. Neither a physical implementation nor hardware statistics have been obtained. A full general-process tomography/temporal-entanglement certificate would require additional instrument bases and causal constraints.

Verifier: `analysis/toe_20261116_qutrit_causal_break_discriminator.py`. Certificate: `data/toe_20261116_qutrit_causal_break_discriminator.json`.

## F. Additional falsification priorities

- The IIB spectrum computed in a point-field two-derivative supergravity truncation does not include nonzero `(u,v)` wrapped string windings. A full duality equality must respect spin, winding and Page sectors, not just matching metrics.
- The older BF band (0<\lambda<12) admits an entire large-radius family of instabilities. The near-equal homogeneous gap discussed here is **a different mode and a different limit**; do not conflate them.
- Untwisted K-group torsion and the nontrivial ring product are algebraic invariants; a *physical* discrete gauge symmetry demands flux-compatible dynamical brane/string charges and observables.
- Pure cubic trinification vacua fail to determine a scale or unique electroweak breaking; a realistic model needs a non-arbitrary potential and matched observables.
- The causal-break classical memory witness has a classical explanation; any claim of quantum temporal entanglement needs the separate coherent-memory/Bell-return witness and ultimately a process-tensor test.

## Reproduction

```powershell
python analysis/toe_20261116_iib_K_gysin_ring.py
python analysis/toe_20261116_near_equal_flux_BF_scaling.py
python analysis/toe_20261116_e6_trinification_cubic_flat_branches.py
python analysis/toe_20261116_qutrit_causal_break_discriminator.py
python -m unittest discover -s tests -p test_toe_20261116_iib_K_gysin_ring.py -v
python -m unittest discover -s tests -p test_toe_20261116_near_equal_flux_BF_scaling.py -v
python -m unittest discover -s tests -p test_toe_20261116_e6_trinification_cubic_flat_branches.py -v
python -m unittest discover -s tests -p test_toe_20261116_qutrit_causal_break_discriminator.py -v
```

The four producers use the Python standard library; the certificate JSON outputs are generated deterministically. Preserve the existing dirty working tree and stage only these newly introduced files and their certificates.
