# Coupled scalar transport: a computed classical evolution and its phase boundary

The earlier packet c7079f950 evaluated omitted self-reactions on frozen parent histories. This packet actually evolves scalar number and energy, alongside three sterile-daughter momentum moments. It imposes internal Maxwell-Boltzmann kinetic equilibrium with a free dark temperature and chemical potential; it does not impose chemical equilibrium. The calculation includes3<->2 reactions, inverse-Higgs production, scalar decays, portal annihilation and bath scattering. It is a specified classical two-moment benchmark, not a full momentum-resolved or finite-temperature completion.

The result is useful in two distinct ways. Self-reactions change the benchmark abundance by a few percent, rather than by the enormous instantaneous rate evaluated on the old history. Meanwhile, the calculation exposes an early phase inconsistency and a quantum-statistics limitation of the16keV example. Neither abundance matching nor numerical convergence removes those physical boundaries.

## What changed in the repo, and what was read

The current local work was revalidated rather than assumed running after the session change. The previous reaction-rate-table process handle was missing; its terminal table existed. The first coupled integration was then actually started. A raw-variable Jacobian overflow failed that run; positive log-number/log-temperature coordinates fixed the thermodynamic-domain problem. A separate equilibrium test detected temperature-interpolation error amplified by the stiff chemical rate; Newton polishing fixed the inversion rather than relaxing the test. Later SciPy finite-difference-Jacobian scaling warnings on passive integral coordinates are retained as execution observations; completed outputs and conservation residuals are checked separately.

Incoming commit47683e807f8fd9347d3a7a4632668cafb9f34113 accepts the earlier radiative audit and demotes the proposed particle-carrier corridor to a mechanism requiring unbuilt protection. Its report, producer, test and cited certificates were inspected. This transport calculation does not repair that naturalness problem. The incoming `sterile_boltzmann.py` also contains a bath-temperature number-only interpolation and a fitted scalar vev. Those are distinct from the independently evolved temperature, energy and specified amplitudes here; no physical priority over standard kinetic theory is claimed.

Eleven further incoming commits,0e87357a2 through a7132f92a, were read in their entirety as1015 patch lines and fast-forwarded. Their six changed files supply a constants catalog, an explicit common-flavor falsifier, a conditional QED calculation, scale/gauge-normalization obstructions and a syntactic provenance scanner. Their successful scan receipt is an incoming attestation, not a new full scan performed here. The seven incoming focused tests are replayed by this validation harness. None supplies the missing normalized physical action or scalar protection mechanism.

Manuscript `papers/forty_points/main.pdf`, raw SHA256 `003b75482b6584e20e83a55d9e9ba0a181f93b8dff0f94c1d615039c21213cbb`, was checked against the extraction before continuing. Pages73-84 were read in full extracted text and page75 was rendered and visually inspected. The text itself retracts an equivariant tick-to-clock identification and distinguishes untwisted family counts from full orbifold spectra; those cautions matter when trying to identify finite algebraic structures with matter dynamics. This is reading of those manuscript claims, not independent reproof of every cited computation. Cumulative manuscript coverage is now1-84of215 pages; complete weekly-commit and PDF reading remain unfinished.

## Established methods, declared action and new numerical object

[Hufnagel and Tytgat2212.09759](https://arxiv.org/abs/2212.09759), selected sections2-3, describe internal-temperature/chemical-potential evolution with number-changing scalar reactions. [De Romeri et al.2003.12606](https://arxiv.org/abs/2003.12606) treat Higgs-fusion production of sterile dark matter. The source/branching logic, threshold nullification and moment methods are established; the contribution here is an explicit tested implementation for the repo's supplied examples. The prior normalized kinetic packet4b97ce7d1 and self-reaction packet c7079f950 remain the immediate owners of the input histories, conventions and25-diagram amplitude.

Use canonical S=w+s and

    Vself = lambdaS/4*(S^2-w^2)^2,
    Vportal = lambda_p/4*S^2*sum_{a=1}^4 h_a^2,
    mS^2=2lambdaS w^2,  mN=yw.

The four bath scalars are massless MB states at T, with fixed radiation-dominated g*=106.75. The scalar mass and vev are held constant during this calculation. The same supplied1TeV parent and16,30,100keV sterile masses are used; the inherited couplings were previously chosen to target the no-self-collision density. They are not refitted here or predicted by W33.

Define r=mS/T, x=ln r, t=Tdark/mS,

    I=2pi^2*nS/T^3,
    R=2pi^2*rhoS/T^4,
    J=(I/r)*K1(1/t)/K2(1/t),
    R/(rI)=K1(1/t)/K2(1/t)+3t.

The internal distribution is fS=z exp(-E/Tdark). Its temperature follows from the last equation and its fugacity follows from nS. Energy and number are independent evolving variables. All scalar self-reactions conserve R in their collision term, while free expansion gives dR/dx=r^2 J. The chemical term in dI/dx is

    Cself = -2pi^2*(M0/mS)*r^5*lambdaS^3*k32(t)
            *(nS/mS^3)^2*[(nS-n_eq(Tdark))/mS^3].

Here M0=MPl/(1.66sqrt(g*)). The coefficient k32 is computed from the complete previously tested five-point tree amplitude, with3!2! symmetry factors. The saved table spans t=1e-4 through1e4 at65 temperatures and uses two scrambled Sobol integrations at each point. Both15- and16-power tables are retained. Very hot, nearly collinear rate estimates have materially larger sampling variation than the production-era coefficients; the whole table is not certified at percent precision. Coarse-table and factor-of-two rate controls test the output sensitivity.

For the included partial decays, write DN=M0*Gamma_NN/mS^2 and DH=M0*Gamma_hh/mS^2, with the canonical widths already audited. Their contributions are

    dI/dx|decay = r^3*[DH*r*K1(r)-(DN+DH)*J],
    dR/dx|decay = r^3*[DH*r^2*K2(r)-(DN+DH)*I].

The daughter's zeroth, first and second comoving q=p/T moments satisfy

    dIN/dx = 2DN*r^3*J,
    dM1/dx = DN*r^3*I,
    dM2/dx = DN*r^3*[(2/3)R-r^2*J/6].

Thus scalar decay energy lost to NN is exactly gained by the daughter first moment. The integrated generalized branching identity is independently monitored:

    IN = 2BR_N*[Iinitial-Ifinal + inverse-Higgs source
                + net portal-annihilation integral + net self-number integral].

Elastic redistribution drops out. This identity explains why a huge instantaneous self-collision term need not imply a huge final density correction: the distribution and forward/reverse rates relax together.

## Portal exchange must accompany the minimal self-potential

The old weak-self-sector benchmark had only the contact portal amplitude. Imposing the minimal cubic also adds a leading scalar-exchange diagram. In mS=1 units,

    M(ss->hh)/lambda_p = 1+3/(s_hat-1),
    M(sh->sh)/lambda_p = 1+3/(t_hat-1).

The annihilation coefficient and its energy-weighted integral are evaluated by invariant one-dimensional thermal quadrature. The bath-scattering matrix integrates the squared second expression over momentum transfer before reducing the massless bath. Its kernel is

    Kij=1/2 integral_{|qi-qj|}^{qi+qj} dQ exp(-Q/2)
        [1+3r^2/((Ei-Ej)^2-Q^2-r^2)]^2.

It retains positive transitions, MB detailed balance and scalar-number conservation. In the heavy, soft-transfer limit its cross section is four times the old contact value; this is tested independently. Higher-order portal diagrams, medium masses and infrared regulation are not included. They cannot be assumed negligible throughout the unmodeled high-temperature phase merely from a small vacuum portal coupling.

## Computed classical benchmark and physical limits

Rounded coupled results, retaining the earlier input couplings, are:

| Supplied sterile mass | Coupled Omega h^2 | mean q | rms q |
|---|---:|---:|---:|
|16keV|0.11706|2.6836|3.1236|
|30keV|0.11092|3.2587|3.7114|
|100keV|0.12017|8.4554|9.3199|

These are outputs of the stated closure, not observational fits or physical exclusions. In particular, they are not a new dark-matter mass prediction. The first two abundances lie below their input no-self targets because the integrated self-number term is negative. A large instantaneous rate on the old frozen history would not have predicted these finite corrections.

The diagnostics expose the approximation's limits:

*16keV:* the classical Hartree restoration indicator reaches about109, above its unit threshold, early in the nominal history. Only about1e-7 of the modeled sterile number is produced while that indicator exceeds one, but this does not prove that the preceding phase has no effect on later scalar initial conditions. About18% is produced while the parent MB occupation at zero momentum exceeds.1, so quantum statistics can matter during production. The fixed broken potential is therefore not a certified physical history.

*30keV:* the sampled restoration indicator remains below one but reaches about.39, which is not a guarantee of negligible thermal mass or vev shifts. The modeled production fraction above the.1 occupation flag is about.003. A finite-temperature treatment remains necessary.

*100keV:* occupation and classical Hartree flags are small, but about93% of the modeled sterile production occurs below160GeV. The fixed four-state massless Higgs bath, constant vevs and constant entropy degrees of freedom need replacement. Passing the scalar classical flags is not passing the hot Standard Model calculation.

The internal self-elastic rate is fast during almost all modeled production; production fractions with rate below10H are approximately1e-9,3e-8 and.0011 for the three examples. This supports investigating a kinetic-equilibrium closure, but event frequency alone does not bound all nonthermal distortions. Quantum statistics,4<->2, loop amplitudes, mean-field evolution, phase transitions and NN backreaction remain uncomputed. Neither a transfer function nor a full minimal-potential relic calculation is established.

## Validation and publication boundary

The executable validation harness regenerates the baseline, refines48/20 to72/32 momentum/transfer nodes, compares BDF with Radau, varies the initial source seed and chemical rates, tests reheating cutoffs, compares leading portal exchange and uses the coarser MC table. The receipt records actual outcomes and exact hashes rather than inferring success from the existence of a file. Eight coupled physics tests cover thermodynamics, positive/detailed-balanced scattering, low-temperature normalization, scalar/daughter energy conservation, generalized number balance and independent server rate coefficients. The seven incoming constants tests are distinct from those physics checks.

An actual server-V8 ordinary-Monte-Carlo computation independently checks thermal chemical rate coefficients at mS/Tdark=1 and3 using262144 events each. It is not a second full coupled ODE solver. Remote Desktop Commander was authoritatively offline, so no unavailable remote computation is claimed. GitKraken was absent from the enabled tools and returned no plugin search result; GitHub history tools and a documented narrow Git CLI fallback were used for authorized synchronization and publication.

The central missing object remains a protected common action with the correct thermal history and physical gravity/matter interpretation. The naturalness conclusion accepted in47683e8 is unchanged. This packet advances the dynamics and identifies the next physical obstruction; it does not solve the TOE.
