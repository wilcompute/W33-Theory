# W33 Five-Front Deep Verification: logical-coset census, arbitrary Gram discrimination, optical bounds, graph clock and E8 parity

**29 October 2026. Scientific status:** reproducible exact finite geometry, algebraic quantum-optics consequences and conservative error bounds. This is not experimental confirmation of a theory of everything.

## 1. q=3,5,7 isotropic-line logical-operator census

The producer builds all projective points of F_q^4, all symplectic isotropic lines, the binary adjacency row span and every two-line symmetric difference. Each nonzero pair is tested for stabilizer membership, and all weight-2q operators are reduced to **logical cosets modulo the adjacency row span**, rather than only counted.

| q | physical n | GF2 rank A | logical k | weight-2q logical words | different logical cosets | representatives per coset |
|---:|---:|---:|---:|---:|---:|---:|
| 3 | 40 | 16 | 8 | 240 | 120 | 2 |
| 5 | 156 | 66 | 24 | 2,340 | 2,340 | 1 |
| 7 | 400 | 176 | 48 | 11,200 | 11,200 | 1 |

All 79,800 unordered pairs of q=7 lines are classified: 11,200 intersecting pairs give weight-14 logical words, 68,600 skew pairs give weight-16 logical words. The 11,200 weight-14 words are in 11,200 distinct cosets. The familiar q=3 collapse of 240 words into 120 cosets is exactly the nonzero nonsingular E8/2E8 count. For q=5 and q=7 that particular doubling disappears. The E8 correspondence and lower-q code ranks are repository prior art; this is an independent cross-q exact coset census.

**Open:** The q=7 minimum remains rigorously 10 <= d <= 14, not a proof of d=14. A separate Claude track's large MILP also timed out inconclusively.

## 2. Arbitrary three-photon Gram matrices: exact fixed-port graph inequality

Both W33 and its nonisomorphic orthogonal dual have 40 modes and the same SRG parameters (40,12,2,4). At t=pi/2, their graph-matched one-photon unitary is U=[2J-5(I+A)]/15. Use the SAME input modes (0,7,9), independent in both graphs, and the SAME precommitted four possible triple outputs: (4,14,23), (4,14,32), (4,23,32), (14,23,32).

For arbitrary three *pure internal photon states*, define x=|<psi0|psi1>|^2, y=|<psi0|psi2>|^2, z=|<psi1|psi2>|^2, and B=Re(<psi0|psi1><psi1|psi2><psi2|psi0>), the real three-photon Bargmann invariant.

An exhaustive sum over all ordered pairs of S3 scattering permutations for each of the eight signed 3-by-3 submatrices yields

    15^6 P_W33 = 17496 +17496*x +17496*y +17496*z +34992*B
    15^6 P_dual = 3376 + 3376*x -1024*y -1024*z - 2048*B.

The checked signed patterns are W33 [511,511,511,511] and dual [259,3,35,32]. Hence

    15^6 (P_W33-P_dual) =
      14120+14120*x+18520*y+18520*z+37040*B.

Now x,y,z in [0,1] and |B|<=sqrt(x*y*z)<=(x+y+z)/3; the latter follows from AM-GM and xyz<=1. Therefore

    15^6 (P_W33-P_dual)
      >= 14120 + (5320*x+18520*y+18520*z)/3
      >= 14120.

**SHARP THEOREM:** For any three independent pure internal photon states (unequal overlaps and arbitrary complex phases included), the same-port fixed-event W33-vs-dual probability difference is at least 14120/11390625 = **0.0012396159122085048**. Equality occurs for fully distinguishable photons. Convex averaging gives the same inequality for *independently prepared mixed* internal states. It does not cover arbitrary three-photon entangled internal input, changes in internal states between devices, or non-ideal optics.

Earlier parallel commits had proved only the equal-real-overlap theorem and an ideal s=1 shot budget. The complete general complex-Gram bound and its sharp global minimum are the new results here. Background: Shchesnovich, Phys. Rev. A 91, 013844 (2015), DOI 10.1103/PhysRevA.91.013844; October 2026 Gram tomography https://arxiv.org/abs/2610.06736. These are consequences of *ordinary quantum mechanics*, not beyond-QM effects.

## 3. Certified optical error budget and uniform loss

For ideal 40x40 unitaries U and implemented V, with ||U-V||_operator <= epsilon, their three-photon symmetric tensor powers differ in operator norm by at most 3 epsilon (telescoping expansion). Thus any number-resolving outcome's total-variation deviation is at most 3 epsilon. If both graph devices satisfy the same epsilon guarantee and receive the same three-photon internal state, their fixed-event gap stays strictly positive provided

    epsilon < 14120 / (6*15^6) = 0.0002066026520347508.

Alternatively the sufficient condition on each device's full output total-variation error is delta < 14120/(2*15^6) = 0.0006198079561042524. These are **conservative sufficient**, not necessary tolerances and are not measured device specifications.

For uniformly attenuating and mode-independent photon survival eta, conditional-on-three-survivors output statistics are unchanged. Average emitted triples per registered triple increase by 1/eta^3; at eta=.9 this is approximately 1.37174. **Do not apply this conclusion** to mode-dependent loss, phase errors, correlated loss or outcome-dependent detection bias.

## 4. Odd-q symplectic quantum-walk exact clock and no-go for physical units

Every odd prime q in W(3,q) has n=(q+1)(q^2+1), degree k=q(q+1), adjacency eigenvalues k, r=q-1 and s=-(q+1). The r-eigenprojector is

    P_r = [A + (q+1)I - ((q+1)^2/n)J] / (2q).

At dimensionless t=pi/2, the unitary equals (-1)^((q+1)/2)*(I-2P_r). This forces **exact** single-photon site/neighbor probability ((q-1)/(q^2+1))^2, and each nonneighbor probability ((q+1)/(q*(q^2+1)))^2. Verified with rational arithmetic and exact total normalization for q=3,5,7: onsite probabilities 1/25, 4/169, 9/625.

For **all odd q**, gcd(k-r,r-s)=2, making t=pi the first complete projective graph-walk revival, with U(pi)=I. If the energy Hamiltonian is H=g A, the physical revival clock is T=pi*hbar/|g|; geometry alone does not select g, hbar, measured couplings, masses or a propagation speed. Quantum walks have exponentially small but generally nonzero amplitudes beyond graph distance at arbitrarily small times; finite graph diameter is not a literal relativistic light cone.

## 5. E8 central integral sign as optical Fock parity

The already established 51,840-element integral Sp(4,3) cover contains central -I8. Under standard passive bosonic second quantization it acts by a_j^dagger -> -a_j^dagger and therefore by (-1)^N on an N-photon signal Fock state. In a fixed-number signal-only measurement this is an unobservable global phase. A coherent reference arm or controlled path outside these eight modes is necessary to measure the phase. It is not a new physical interaction or proof of fundamental E8 dynamics.

## Beyond the five: identifiability firewall

The mathematical group, incidence code, Hilbert-space unitary, clock and optical discrimination are not a parameter-free experimental prediction beyond standard quantum theory. If U_g(t)=exp(-i g A t/hbar), then varying the unselected coupling g simply rescales time. A credible physical TOE must propose an independently fixed interaction and an observable *different* from established physics, and compare it with independent data.

### Verification

Run in the repository root:

    python analysis/w33_20261029_deep_five_verifier.py
    python -m unittest discover -s tests -p test_w33_20261029_deep_five.py -v

The executable producer was run independently against the Windows checkout in a temporary file before release; its results were checked before freezing the JSON certificate. It does not modify the existing photonic or manuscript source. Results are finite exact algebra and strict inequalities; they are not experimental demonstrations.
