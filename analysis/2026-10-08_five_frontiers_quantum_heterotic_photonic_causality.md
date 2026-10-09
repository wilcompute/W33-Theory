# 2026-10-08: Five independent physics frontiers — seven-state vacuum, thermal curvature, optical loss, heterotic benchmark sieve, and native causal shells

This report cross-checks the previous Pass11769-11777 work and the **parallel** Pass11778-11785 compactness / nonlinear curvature packet. It does not claim a physical TOE, a numerical spectral lower bound, a first-principles Standard Model, or an experimental demonstration.

## 1. Improved Ritz upper bound, not an excitation gap

The previous five-state basis comprised the optimized Pass11769 Gaussian and point/line sums of normalized He2 and He4 on their 15-dimensional incidence kernels. Add point and line collective He6 states, each with norm

    N_n = 40[1+12(-1/3)^n+27(1/9)^n], n=2,4,6.

Different Gaussian chaos degrees and independent point/line kernel factors make the seven basis states exactly orthonormal. All matrix elements of H=sum(J_e^2) reduce to the eight incidence pair orbits, evaluated as four-variate Gaussian moments. For n<=6 the integrands have total polynomial degree <=16, so tensor 9- and 10-node Gauss-Hermite quadratures independently integrate the moments to degree-exact floating-point accuracy.

    prior five-state bound  E0 <= 127.61937784333912
    new seven-state bound  E0 <= 127.61920315299878
    improvement                         0.00017469034030
    max matrix difference (orders 9/10) 6.83e-13

A lower Ritz eigenvalue is an **upper** bound to the actual bottom of the Friedrichs Hamiltonian. It is neither the lower energy bound nor a gap. The parallel Pass11778 packet separately proves compactness and the existence of a positive, but as yet *unquantified*, excitation gap; do not credit that theorem to this seven-state experiment.

## 2. Antiunitary curvature: a thermal selection rule

The verified antiunitary T satisfies T^2=+1 and T J_e T^-1=J_e for every one of 160 currents. Therefore the Hermitian curvature i[J_e,J_f] is T-odd. Of the 12,720 unordered incidence-edge pairs, exactly 480 are adjacent and potentially noncommuting, while 12,240 commute.

In every invariant pure or mixed state, including a trace-class Gibbs state of H, the expectations of all these 480 curvature observables vanish. A 2-by-2 real-symmetric current toy checks the rule while having a **nondegenerate** ground eigenvalue; T^2=+1 implies no Kramers theorem. This is not a classification of the full antiunitary normalizer and not an identification with physical CP.

## 3. Continuous-variable optical loss and a spurious positive null

For the exact two-mode single-edge quartic gate of the previous report, pure loss with transmission eta and independent zero-mean Gaussian electronic noise of variance sigma_e^2 gives

    theta = (39/20)^2 tau
    kappa4_obs = eta^2 * (618440/6591) * theta^4
    Var_obs = 1/2 + eta*(5207/3042)*theta^2 + sigma_e^2.

At tau=.05 and sigma_e^2=.01, the excess kurtosis varies from 0.3749 (eta=1) to 0.1047 (eta=.5) and 0.0180 (eta=.2). Gaussian-null heuristic 5-sigma sample scales are respectively about 4.3e3, 5.5e4, 1.86e6 and are **not** detector-aware power guarantees.

Critical confound: a mixture of mean-zero Gaussians with shot-dependent conditional variances v has positive kappa4=3 Var(v). A measured nonzero cumulant can therefore be caused by variance drift and does not by itself certify a quartic gate. This remains a **single-edge CV** control, not a 160-edge W33 machine or a finite-dimensional two-qutrit gate.

## 4. External exact-R-parity benchmark: exact fixed-shift sieve

Input: Lebedev et al., "The Heterotic Road to the MSSM with R parity", arXiv:0708.2691, Phys. Rev. D 77, 046013 (2008), **Appendices E.1a and F.1a**. Both benchmark models have gauge shift

    V = (1/3,-1/2,-1/2,0,0,0,0,0)
        (1/2,-1/6,-1/2,-1/2,-1/2,-1/2,-1/2,1/2).

The separate W33 Pass10960 ledger holds 128 Z6-II selected models on **29** distinct base-shift labels. Their full original V vectors were recovered from the user's WSL orbifolder scan directory, cross-checked against those 128 names, and frozen with raw-file SHA-256 hashes in data/w33_20261008_heterotic_base_shift_29.json.

A necessary gauge-equivalence sieve under independent E8 Weyl actions, E8 root-lattice translations and optional exchange of the two E8 factors gives:

    29 input W33 base-shift labels
    18 match the pair of factor orders of benchmark V
     7 also match the pair (order, order*V^2 mod 2)
     1 also matches the pair of numbers of unbroken E8 roots.

The benchmark has factor signatures (6,2/3), (6,5/3) and unbroken root counts (44,84), with all arithmetic performed using exact rational fractions and a generated 240-root E8 system. The unique remaining W33 base label is **Z6II_34**, containing **15** of the 128 selected Z6-II model labels.

**Scope firewall:** the sieve excludes 28/29 base labels **only under the stated fixed-twist-generator equivalence operations**. It has NOT compared Wilson-line classes, complete space-group generator redefinitions, matter hypercharge embeddings, singlet supports or F-flatness. It is incorrect to conclude that the remaining 15 models contain the published benchmark, or that 113 models are impossible under a broader generator equivalence. The existing W33 matter-even D-flat no-go is not contradicted.

## 5. Finite native shells cannot select a physical dimension

All 80 vertices of the 4-regular W33 Levi incidence graph have exact shortest-path shells

    radius:          0   1    2    3    4
    shell vertices:  1   4   12   36   27
    ball vertices:   1   5   17   53   80.

Graph diameter is four. Its complete eigenvalue multiset is ±4 once each, ±sqrt(6) twenty-four times each, and zero thirty times. A finite-difference ball-growth "dimension" from radii 2/3/4 is approximately 1.766, 2.804, and 1.431, respectively. No limit stabilizes here, so neither "3 spatial dimensions" nor c can be read from the finite shell profile. Large-scale growth requires a specified replication / continuum family, state and coupling dynamics. This complements Pass11771's manually supplied 3D common-cone construction and the parallel nonlinear-curvature work.

## Execution and validation

Producers: analysis/w33_20261008_7state_ritz.py; analysis/w33_20261008_current_curvature_thermal.py; analysis/w33_20261008_photonic_loss_control.py; analysis/w33_20261008_heterotic_benchmark_{shift_screen,class_gate,root_sieve}.py; analysis/w33_20261008_levi_shell_dimension.py. Heterotic fixture freeze: analysis/w33_20261008_freeze_heterotic_base_shift_29.py.

Regression suites test the Ritz 9/10 quadratures, 240 E8 roots, benchmark filters and lattice-shift controls, optical loss/variance-drift controls, antiunitary current-pair counts and native incidence shells. Other independent parallel work is left intact.
