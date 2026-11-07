# The minimal scalar potential changes the sterile-parent histories

The momentum benchmark in commit4b97ce7d1 explicitly assumed negligible scalar self-interactions. Its tabulated minimal-Z2 quartics were diagnostics, not interactions included in its transport. This follow-up evaluates the first omitted collisions on those actual distributions. For the16 and30keV examples, number-changing collisions are large; for100keV the sampled number-changing rates are small, but elastic entropy production is large. Thus those frozen histories and spectra cannot be promoted to solutions of the minimal broken-Z2 model. This does not retract the earlier, explicitly weak-self-sector collision benchmark or prove that every other scalar potential fails.

## Ownership, search and the unexpected threshold zero

The physical methods are established. [Voloshin, hep-ph/9211242](https://arxiv.org/abs/hep-ph/9211242) treats threshold amplitudes in broken scalar theory. [Hufnagel and Tytgat,2212.09759](https://arxiv.org/abs/2212.09759), section2, explicitly describe the vanishing tree-level number-changing amplitudes in the broken-Z2 case and the need for momentum dependence. Selected relevant sections were read; no entire-paper reading or new threshold theorem is claimed. Their dark matter is the scalar itself; here the calculation tests a decaying scalar parent of sterile dark matter.

Preconstruction searches included the explicit citations, nullification and threshold-cancellation expressions in RESULTS_INDEX.md and the code, paper, data and documentation trees, with a1MB per-file cap. Broad threshold expressions produced unrelated hits, including optical matrix nullification and gauge-coupling symbols; these are not scalar collision results. An exact citation search returned no matches in that scope. The previous kinetic packet and its explicit self-sector limitation are the immediate repo owners. Neither these searches nor the new computation establish priority over the corpus or literature.

Use the canonical fluctuation s and

    V(s) = mS^2 s^2/2 + g3 s^3/3! + g4 s^4/4!.

For the minimal broken-Z2 potential lambdaS/4*(S^2-w^2)^2,

    mS^2=2lambdaS w^2,  g3=3mS^2/w,  g4=3mS^2/w^2=6lambdaS.

All numerical amplitudes use mS=1 and five incoming four-momenta. Their physical amplitude has one additional factor1/mS. Let Dij=(pi+pj)^2-1. The complete tree amplitude, up to an irrelevant overall sign, is

    M5 = g3*g4 sum_{10 pairs ij} 1/Dij
       + g3^3 sum_{15 disjoint unordered pairs ij,kl} 1/(Dij Dkl).

At threshold it reduces to

    M5_threshold = -5g3(3g4-g3^2)/8 = 0

for the minimal potential. The code checks the generic-coupling expression, including the published identical-particle normalization, and compares the25-diagram enumeration with an independently rooted recursive tree construction. Finite incoming momenta remove this threshold cancellation. A zero-momentum constant-rate estimate would miss the relevant collisions.

## Both chemical directions on the computed histories

The parent distributions are regenerated from the previous packet's stated collision equation, without altering that packet. At r=mS/T equal to.3,1,3,6, the new calculation inserts the actual fS into

    gamma32 = 1/(3!2!) integral dPi1 dPi2 dPi3 f1 f2 f3
              integral dPhi2 |M5|^2,
    dnS/dt + 3H nS = gamma23 - gamma32.

Here dPi=d^3p/[(2pi)^3 2E] and dPhi2=beta/(8pi)*dOmega/(4pi). Sampling incoming triples from a normalized MB proposal permits both directions on the same phase space. If R(q)=fS(q)/exp(-E/T), the forward weight contains R1R2R3 and the reverse weight R4R5: energy conservation cancels the equilibrium exponentials. Equilibrium and arbitrary-fugacity controls verify detailed balance and the direction of chemical relaxation. The physical distributions themselves are not assumed thermal.

Rounded diagnostics at r=1, with the same supplied1TeV parent, are:

| Supplied sterile mass | lambdaS if minimal Z2 | (gamma23-gamma32)/(nS H) | elastic entropy production/(nS H) |
|---|---:|---:|---:|
|16keV|0.37066|about1.13e7|about2.3e8|
|30keV|0.05650|about1.63e4|about1.4e6|
|100keV|0.001627|about0.0128|about36|

For the16 and30keV histories, the sampled net chemical term changes sign later: it is positive at r=.3 and1 and negative at r=3 and6. These are first omitted collision terms, not integrated abundance changes. A large collision term requires solving the changed equations; multiplying it by a Hubble time cannot predict the resulting density. A reported quartic that would make a one-way rate small while holding the history fixed is only a perturbative diagnostic; changing the potential changes the history and the couplings.

## Elastic entropy makes the100keV distinction concrete

The complete tree elastic amplitude is

    M4 = g4 + g3^2 [1/(s-1)+1/(t-1)+1/(u-1)].

Elastic reactions conserve total number and energy but can reshape the distribution. An event frequency alone does not demonstrate redistribution of an already equilibrated distribution. Therefore the code computes the classical entropy production

    D22 = 1/(2*2!*2!) integral dPi1 dPi2 dPhi2 |M4|^2
          (f1 f2 - f3 f4) log[(f1 f2)/(f3 f4)] >= 0.

The extra1/2 avoids counting forward and reverse copies of the same elastic transition twice. This vanishes for any MB temperature and chemical potential; tests include both cases. The100keV frozen distribution has positive D22/(nS H), around36 at r=1 and much larger at later sampled times. Hence even its comparatively weak chemical term does not certify the published spectrum for the minimal potential.

There is also a useful surviving boundary: a number-conserving scalar collision drops out of the earlier integrated branching identity. In the no-contact, no-number-changing, constant-width limit with zero initial scalars and complete final decay, elastic reshaping alone does not change the total sterile yield fixed by inverse-Higgs production times branching fraction. It does change momentum information. This separates the density question from the spectral question; it is not a proof that the100keV model passes a corrected thermal or structure-formation calculation.

## Numerical evidence and remaining physics

The PC implementation uses full momentum-dependent tree amplitudes and four independently scrambled Sobol integrations. The validation receipt records a17-to18-power refinement, sampling errors, exact tested source hashes and the test output. A separate actual server-V8 calculation uses an ordinary Monte Carlo gamma-distribution rejection sampler at r=1, independently builds the kinematics and propagators, and agrees at the percent level. Its saved input and executable source are included. Remote Desktop Commander was checked and remained offline; no unavailable remote-PC computation is claimed.

Tests cover independent tree enumeration, generic threshold normalization, Lorentz transformations, permutation symmetry, on-shell momentum conservation, proposal normalization, chemical detailed balance, coupling scaling and elastic entropy equilibria. Monte Carlo error estimates and refinement differences are numerical diagnostics, not rigorous bounds on rare phase-space regions.

This calculation does not integrate a corrected self-interacting parent distribution or sterile spectrum. Quantum statistics, finite-temperature masses, scalar symmetry restoration, mean-field evolution,4<->2 reactions, loop corrections, reheating and cosmological transfer functions remain absent. The minimal potential's Higgs/quintessence vacuum and radiative problems are also unresolved. The result changes the next calculation from assuming small self-couplings to constructing and solving the actual dark-sector dynamics. It supplies no solved TOE claim. Complete weekly-commit and manuscript reading remain unfinished; cumulative manuscript full-text coverage is1-72of215 pages.
