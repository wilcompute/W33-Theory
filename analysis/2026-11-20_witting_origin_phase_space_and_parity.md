# Witting communication geometry is an odd-parity two-qutrit Wigner code

**Research date:** 2026-11-20. **Classification:** finite-field / Clifford / discrete-Wigner mathematics. **No new physical law, no optical experiment, no demonstrated quantum-key security, and no TOE prediction.**

## Source-origin and ownership audit

Two literatures meet without identifying their physical Hilbert spaces:

- Alexander Yu. Vlasov, *Scheme of quantum communications based on Witting polytope* (2025), https://arxiv.org/abs/2503.18431: 40 Witting pure rays in a four-level Hilbert space, organized into 40 orthonormal tetrads. The scheme's 13/40 compatibility means one chosen ray **itself plus 12 distinct orthogonal rays**. It is NOT an SRG of degree 13.
- Two-qutrit generalized Pauli operators, classical symplectic polarization and W(3,3): 40 projective nonidentity Weyl directions in F_3^4, 40 commuting four-ray isotropic contexts. This is standard finite quantum information, not a new graph discovery.
- The 40 Witting rays = the two-qutrit parity-odd rank-one reductions of the 40 eigenphase-zero Pauli projectors was **already proved in this repo**: analysis/w33_pass11663_odd_weil_normal_map.py. The exact Witting–W33 *point*-graph map, not the nonisomorphic Q(4,3) line graph, is owned by analysis/w33_pass4963_witting_pancharatnam_w33_reaudit.py. The ququart 2-design/communications and full E8 exterior Lie brackets likewise predate this pass.

**What this pass adds:** all-directions 9x9 reflection/transvection certificates; parity-conditioned full-operator projector sum and trace fingerprints; complete 81-point two-qutrit discrete-Wigner distributions on all 40 Witting rays; exact Wigner-negativity line geometry and Gram recovery; odd-prime p=5 negative control and a universal two-qudit counting identity connecting 13/40 to a Wigner-negativity threshold.

## All 40 communication reflections are restrictions of 9-dimensional Clifford transvections

Use the centered order-three Weyl operators W(v), v in V=F_3^4, where W(v)W(-v)=I. For every projective direction [v] define

    Pi_v = (I + W(v) + W(-v))/3,    U_v = I+(omega-1)Pi_v,
    omega = exp(2*pi*i/3).

Pi_v is the eigenvalue-one spectral projector (sometimes called **phase label 0**, but not a zero-eigenvalue projector). It has rank three in C9 and commutes with two-qutrit phase-space parity P. On the even eigenspace H_+ of parity (dim5) its rank is two; on odd H_- (dim4) its rank is one. The 40 odd projectors match the established Witting rays exactly, in the source's projective gauge.

These full-space unitary reflections have order three. Their Weyl conjugation is the symplectic transvection:

    U_v W(u) U_v^dagger = W(u+2 symp(u,v)v).

Every one of the 40 gates was compared against all 80 nonidentity Weyl operators (**3200 unitary conjugations**); 1600 odd-subspace ray-action cases were checked too. The observed full-space covariance maximum was approximately 6.5e-15. The 40 odd projections form the exact Witting complex projective 2-design; that design was already known. Note that each transvection fixes exactly 13 projective points: [v] plus the 12 other directions commuting with it.

For the physical gate U_v, normalized trace-amplitude squares are constant across v:

    |Tr_9 U_v /9|^2 = 1/3,
    |Tr_4 U_v,odd /4|^2 = 7/16,
    |Tr_5 U_v,even /5|^2 = 7/25.

The different traces are representation-sensitive and would require calibrated coherent order interference to compare experimentally. The ideal matrices alone do not provide a black-box causal-order or quantum advantage proof.

## A 40-setting parity estimator and a full displaced-Wigner estimator

The sum over the 40 eigenvalue-one spectral projectors is EXACTLY

    sum_[v] Pi_v = 13 I_9 + 3 P.

This follows by partitioning the 80 nonzero vectors in F3^4 into 40 pairs v,-v and using the standard centered-Weyl parity identity sum_{u in F3^4} W(u)=9P.

Uniformly choose one of the 40 directions; measure the three-outcome Pauli observable and count an **eigenvalue-one** event. For arbitrary two-qutrit rho, the accepted frequency in the calibrated ideal experiment has expectation

    p_0(rho) = [13+3 Tr(P rho)]/40.

Thus p0 is exactly 0.25 for parity-odd states, 0.40 for parity-even states, and 1/3 for maximally mixed rho=I9/9. The 40-subsystem aggregate sees ONLY the parity expectation; it is not informationally complete and does not certify arbitrary non-Clifford dynamics. Miscalibration, drift and postselection can spoof an observed threshold.

Let Gross discrete Wigner function W_rho(a)=Tr(A_a rho)/9 with A_a=W(a)P W(a)^dagger, a in F3^4. Translating the measurement by a Clifford displacement yields

    p0(a) = [13+27 W_rho(a)]/40,
    W_rho(a) = [40 p0(a)-13]/27.

Therefore a randomized measurement over the same 40 projective directions plus a selected *phase-space displacement* gives a calibrated operational estimator for each one of the 81 Gross Wigner values. This is standard informationally complete discrete-Wigner tomography (with an overcomplete measurement design), not a parameter-free new physical observable.

## All 40 Witting states: negative finite lines, positive perpendicular hyperplanes

For every nonzero projective Pauli direction v, define the physical two-qutrit pure density matrix

    rho_v = Pi_v (I-P)/2.

The completely **unfitted** 81-point Wigner distribution satisfies exactly

    W_v(a) =
      -1/9,  if a belongs to the F3-line span(v) (three points);
      +1/18, if symp(a,v)=0 and a is not in span(v) (24 points);
       0,    otherwise (54 points).

All 3240 [ray,phase-space point] instances agree to machine precision. The three negative phase-space positions literally recover the projective direction [v]; it is an intrinsic *address* relative to the chosen Gross phase-space origin and Weyl convention. The total phase-space mass is one, and the Wigner l1 norm is 5/3 with mana log(5/3).

A concrete representative is v=(1,0,0,0): rho_v is |0><0| tensored with the single-qutrit Strange state (|1>-|2>)/sqrt2. The other 39 rays are reached by centered Clifford symplectic transformations. This is a two-qutrit *qutrit-resource* interpretation; it must not be confused with the separate two-qubit/ququart Witting magic-state resource M36 or the preexisting H27 dark Strange multiplicity state in the repository.

This Wigner support pattern reconstructs the ququart ray Hilbert-Schmidt overlaps purely through finite phase-space incidence:

    Tr(rho_v rho_w) = 9 sum_a W_v(a) W_w(a)
                    = [(2I+J-A_W33)/3]_[v,w].

It therefore equals 1 on the diagonal, 0 if distinct projective directions commute, and 1/3 if they do not; the resulting 40-by-81 Wigner-array matrix has rank16. This gives a fully constructive, phase-space version of the Witting orthogonality <-> Pauli commutation graph dictionary.

## Why the number 13 occurs twice

A point of the W(3,p) symplectic point graph has valency k=p(p+1), hence **self plus commuting neighbors** k+1=p^2+p+1. The projective Pauli direction count is N=(p+1)(p^2+1). In the universal two-qudit parity projector-sum identity the scalar coefficient is

    (N-1)/p = p^2+p+1 = k+1.

Consequently the scheme's projective compatibility fraction (k+1)/N is **exactly** the zero-Wigner threshold for the uniform projector protocol at the phase-space origin, for every two-qudit system of odd prime dimension p:

    W_rho(0)<0  iff  p0< (k+1)/N.

For p=3 this is the remarkable shared 13/40 fraction. For p=5 it is 31/156. These are two **distinct probability experiments**; their equality is a representation-theoretic counting identity, not a shared key-security or quantum-state preparation theorem.

## Uniqueness and counter-model at p=5

For odd prime p and n>=2 qudits, the total Hilbert dimension is p^n, the parity even/odd dimensions are (p^n +- 1)/2, and the eigenvalue-one direction projector ranks are

    rank_even=(p^(n-1)+1)/2,
    rank_odd =(p^(n-1)-1)/2.

Demanding rank_odd=1 in every projective direction forces p^(n-1)=3, uniquely p=3,n=2. Thus the Witting-like **rank-one odd-sector representation** is distinguished within the given family, but no argument thereby selects the physical number of qutrits in nature.

For p=5,n=2, the full calculation constructs all 156 directions on C25. The parity dimensions are (13,12); the eigenvalue-one projector ranks are (3,2), NOT odd rank1; the exact 156-projector sum is 31I25+5P, with measured sector eigenvalues 36 and 26. This negative control was verified by independent 25-by-25 matrix calculations.

## Reproduce

    python analysis/toe_20261120_witting_transvection_parity.py
    python -m unittest discover -s tests -p test_toe_20261120_witting_transvection_parity.py -v

The standalone script uses NumPy and writes data/toe_20261120_witting_transvection_parity.json; the 18 tests include arbitrary positive density matrices, p5 higher-rank controls, Wigner line supports, the exact Wigner Gram, and transvection gate covariance.

## What would make this physics rather than a dictionary?

- Identify a local physically motivated Hamiltonian or field action dynamically selecting the odd parity carrier, rather than using parity as a supplied superselection selector.
- Specify actual photonic hardware that can implement 40 Clifford settings with independently calibrated acceptance/loss and readout; test the parity/Wigner statistics and quantify SPAM bias.
- Show how an even/odd split transforms under a candidate Lorentzian continuum and yields anomaly-free chiral matter; finite Wigner negativity alone is not fermion chirality.
- Derive a parameter-independent physical coupling or experimentally falsifiable value from a complete microscopic dynamics.
- Establish a composable security proof, if the intended operational task is cryptography; 13/40 compatibility and Wigner negativity are not sufficient.

**Major source references:**
- A. Yu. Vlasov (2025), https://arxiv.org/html/2503.18431 .
- Waegell & Aravind (2017), https://arxiv.org/abs/1701.06512 .
- D. Gross (2006), *Hudson's theorem for finite-dimensional quantum systems*, https://arxiv.org/abs/quant-ph/0602001 .
- Repository prior art: analysis/w33_pass11663_odd_weil_normal_map.py; analysis/w33_pass4963_witting_pancharatnam_w33_reaudit.py; analysis/2026-10-15_toe90_vlasov_witting_research.md; analysis/w33_pass11681_e8_from_two_qutrits.py.

