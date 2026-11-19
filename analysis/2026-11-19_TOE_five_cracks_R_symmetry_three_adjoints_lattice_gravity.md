# Five TOE cracks: symmetry-selected E8 vacuum, three-adjoint SU5, cohomological holonomy, lattice gravity, and photon activation

**Research date 2026-11-19. Physics-first independent pass.** This is a collection of explicit *conditional* effective-theory constructions and no-go tests, **not** a solved TOE or experimental discovery. W33 is not assumed anywhere.

## Source and literature collision audit

Read master `740af8b5b` ("Test SU5 adjoint completion and fit full DESI DR2 covariance with quantum operational gates") and the source `0ec1074e4`, `cb1a66717`, `40191f8e4`. **Parallel update:** commit `22ac80224` appeared during this analysis and independently confirms known two-copy photon SSR activation, extends the two-adjoint SU5 scan, and computes prior-sensitive DESI Bayesian evidence. The two-copy idea here is overlapping corroboration, NOT new relative to that parallel commit. The three-adjoint projector construction, source-specific Z4R selection and driving-field F/D model, flat-centralizer limitation and TT Nyquist test are distinct investigations. The established two-adjoint mass obstruction, E8 charged-sector census, BAO covariance and previous single-photon SSR theorem are imported where labeled; **nothing is claimed novel merely because it was newly computed here.** The physics literature includes adjoint fermionic SU5/type-III seesaw [P. Fileviez Pérez 2007](https://arxiv.org/abs/0705.3589), [two-triplet SU5 thresholds 2021](https://doi.org/10.1016/j.nuclphysb.2021.115484), [discrete SO10-compatible Z4R](https://doi.org/10.1016/j.physletb.2010.10.038), and [M-theory Higgs bundles](https://doi.org/10.1007/JHEP03(2019)199). We derive specific new *toy-case* consequences using the exact repo spectra and give reproducible counterexamples.

**Reproduce:**
```powershell
python analysis/toe_20261119_five_cracks_symmetry_adjoints_gravity_photons.py
python -m unittest discover -s tests -p test_toe_20261119_five_cracks_symmetry_adjoints_gravity_photons.py -v
```
Result certificate: `data/toe_20261119_five_cracks_symmetry_adjoints_gravity_photons.json`.

## 1. Three fermionic SU5 adjoints evade the two-adjoint light-leptoquark theorem

The parallel `740af8b5b` proves a spectral theorem: with **two** symmetric-mass fermionic SU5 adjoints `24_F`, both electroweak triplets light, at least one octet light, and *only* mass terms `Tr(24_F²)` and `Tr(24_F² 24_H)`, at least one unwanted Dirac `(3,2,-5/6)+(3bar,2,+5/6)` state is also light. This is a true obstruction within the specified two-generation class.

**Outside-box escape: use THREE adjoints with complementary light-flavor projectors.** The same renormalizable mass relations hold as matrices for all generations,

```
M8 = M0 + 2K
M3 = M0 - 3K
MX = M0 - K/2 = (M8+M3)/2
M1 = M0 - K = (2M8+3M3)/5.
```

Choose simultaneous diagonal flavor matrices with `M3=diag(t,t,MU)` and `M8=diag(MU,MU,o)`. The two-dimensional light-triplet subspace and one-dimensional light-octet subspace are complementary. Thus `MX=diag((MU+t)/2,(MU+t)/2,(MU+o)/2)`: **all three leptoquark partners remain at roughly MU/2**. The precise reason the two-adjoint no-go fails is the subspace dimension inequality: for n flavors, light subspaces of dimension r_T and r_O must intersect in at least `r_T+r_O-n` dimensions. With n=2 and ranks2+1, an intersection is forced; with n=3 it is not.

**One-loop all-component threshold refit.** Take *chosen* MU=2e16 GeV, MZ=91.1876 GeV, MS-bar inverse alphaEM=127.930, sin²(thetaW)=.23122, alpha_s=.1180. Include **every component of all three Weyl 24_F** in the SM one-loop running:
- triplet each beta shift `(0,4/3,0)`,
- octet each `(0,0,2)`,
- Dirac leptoquark-like pair each `(10/3,2,4/3)`,
- singlet zero. They add `(10/3,10/3,10/3)` per complete adjoint at a common scale.

Numerically solve two coupling-difference equations for t and o, with the partner masses constrained by the exact SU5 relation. Solution:

| Component | Explicit masses |
|---|---|
| SU2 triplets (3) | 7.67789089e6, 7.67789089e6, 2.0e16 GeV |
| SU3 octets (3) | 2.0e16, 2.0e16, 5.67838850e4 GeV |
| (3,2) partners (3) | about 1.0e16, 1.0e16, 1.0e16 GeV |
| sterile adjoint singlets (3) | about 8.0e15, 8.0e15, 1.2e16 GeV |

All three inverse couplings agree at **36.35908537** in this ONE-LOOP SM+24_F threshold calculation. No mass lies below MZ. Matrices M0,K are explicitly output. This is a concrete *counterexample* to promoting the two-adjoint claim into an arbitrary-number-of-adjoints no-go. It is not a new predicted spectrum. The smallest cancellation ratio relative to MU is about **2.84e-12**, an extreme fine-tuning. Extra SU5 Higgs masses, actual gauge boson mass/proton lifetime, two-loop effects, vacuum stability and vectorlike mixing are absent.

**Connection to neutrinos:** The same two light electroweak triplets can support a standard rank-two type-III seesaw with one massless active neutrino at tree level. An explicit flavor-diagonal 2x3 Yukawa matrix is constructed to reproduce the *imported* oscillation mass splittings. The PMNS matrix, CP phase, masses and flavor hierarchy are not predicted. This is a known mechanism, not a new explanation of observed masses.

## 2. A candidate Z4R selection rule for the actual E8 source spectrum

The preceding `0ec1074e4` enumerated exactly eight charged Spin10-neutral source fields and showed that a gauge-allowed singlet cubic `S13*S34*S14conj` forces `<S13>=0` at every simultaneous F/D-flat point whenever its coefficient is nonzero. Yet `<S13>` was required by one proposed third-family effective Yukawa.

Use a **candidate discrete Z4R** under which the superpotential carries R charge2:
- all three Spin10 16s have R=1;
- all eight charged singlets have R=0;
- `10_24`, `10_34`, `10_13`, `10_14` have R=0;
- `10_12` has R=1.

All formally allowed one-singlet family operators `16_i 16_i 10 S/M` have R=2 and remain allowed; all purely singlet polynomial operators have R=0 and are **forbidden from the superpotential to all orders**, provided the exact R symmetry remains unbroken. Thus the harmful cubic is absent by a selection rule rather than a fine-tuned vanishing coefficient. The S12/conjugate pair and S13/S34/S14conjugate triangle give a nonzero tree F/D-flat branch.

**Anomaly audit:** using Dynkin indices C2(Spin10)=8, T(16)=2, T(10)=1, the mixed Spin10²-Z4R coefficient is **4**, even modulo eta=2. Computing the full 3x3 mixed Abelian-squared R anomaly matrix from the eight singlets, five 10s and three 16s gives

```
[[-44,-16,-28],
 [-16,-30,-18],
 [-28,-18,-42]]
```
whose entries are all even. **These are necessary modular arithmetic checks, not proof of a valid discrete gauge symmetry**: Abelian charge normalization, U1 anomalies already present in the chiral spectrum, Green-Schwarz inflow and the entire global gauge-group structure remain open.

With 3 U1 and 45 Spin10 gauginos, eight singlet fermions, five10s and three16s, the *illustrative minimal 4D supergravity* mixed gravitational Z4R coefficient is **-21**, odd modulo2. Two neutral R=2 driving chiral multiplets increase it to **-19**, still odd. One additional neutral R=0 chiral modulus would make the residue even (−20), but such a field and every other global anomaly must follow from a real compactification. The discrete Z4R is therefore **not yet demonstrated anomaly-free**.

**Literature:** [A unique Z4R symmetry for the MSSM](https://www.sciencedirect.com/science/article/pii/S0370269310012499) gives a known GUT-compatible precedent; our toy E8 assignment and its specific computed anomaly coefficients are new to this pass.

### Actual F/D-flat nonzero condensate with neutral driving fields

To go beyond an unstabilized flat direction, add **two gauge-neutral driving chiral multiplets** `X_A,X_B` of R=2 and an *effective* gauge/R-invariant superpotential

```
W = X_A (A B - vA²) + (X_B/M)(C E G - vB³)
A=S12, B=S12conj, C=S13, E=S14conj, G=S34.
```

The following point has **every F-term and every U1 D-term exactly zero**:

```
A=B=vA; C=E=G=vB; X_A=X_B=0;
all other charged fields 0.
```

F_XA and F_XB fix the two gauge-invariant product magnitudes. Within this **five-charged-field branch**, 5 complex fields minus rank3 Higgsed Abelian gauge orbits minus 2 holomorphic constraints leave **zero** local complex moduli. Other full-spectrum modes remain and still need a mass/stabilization mechanism; the two scales and cutoff are arbitrary external inputs, and the `X_B CEG/M` term is *nonrenormalizable*.

The three independent nonzero Higgs charges have Smith normal form `diag(1,1,4)`, i.e. charge lattice index4, indicating a formal residual Z4 in naive U1³ with the chosen primitive coordinates. It is **NOT automatically a new independent symmetry**: the underlying E8 subgroup is globally `(Spin10 x SU4)/Z4`, and this index may encode the existing SU4 center/diagonal quotient. It is categorically distinct from the *postulated* discrete R symmetry; their shared numeral 4 is not a physical derivation.

This is an explicit mathematical **effective-theory F/D-flat branch**, not dynamically generated particle masses or a stabilized compactification.

## 3. Flat centralizer Wilson lines cannot cure unwanted adjoint multiplets while preserving Spin10

The previous punctured T3 Yukawa-cup escape has `b1=3`, and an unbroken trivial Spin10 adjoint local system would give three unwanted adjoint chiral multiplets. Could one simply turn on a Wilson line to remove them?

A flat complex rank-one local system on T3 is specified by holonomy `lambda=(lambda1,lambda2,lambda3)`. Its cellular cochain is the Koszul complex built from `a_i=lambda_i-1`:

```
0 -> C --d0--> C^3 --d1--> C^3 --d2--> C ->0.
```

If all lambdas equal1 its Betti numbers are **(1,3,3,1)**; if **any lambda differs from1**, contraction by `a_i^-1` gives an acyclic complex: **(0,0,0,0)**. The implementation verifies d1 d0=d2 d1=0 and all ranks for four cases. Removing an ordinary open ball does not change absolute H1 with local coefficients; the relevant relative source boundary conditions remain a separate problem.

For a Wilson line that preserves the **entire** Spin10 gauge algebra, its holonomy must commute with that algebra and therefore acts **trivially on its adjoint representation**. Hence the adjoint coefficient system remains the **untwisted** one. The three adjoint modes cannot be lifted by *this centralizer Wilson-line trick alone*. Using holonomy noncentral in Spin10 may remove some but also breaks part of Spin10. A different three-cycle, non-flat Higgs background, defect boundary projection or real mass dynamics is necessary.

This is a narrow, exact *topological gate*, not a general no-go for compact G2 solutions.

## 4. A gauge-exact finite Einstein operator still has high-frequency fake gravitons

On a periodic **8^4 Minkowski** lattice, define the centered commuting derivative `D_mu f=[f(x+e_mu)-f(x-e_mu)]/2`. Form the standard **linearized Einstein tensor** `G_mu nu^lin[h]` using D everywhere. Its contracted Bianchi identity and infinitesimal linearized gauge invariance follow algebraically from **commutation of D**:

```
D^mu G_mu nu^lin = 0,
G_mu nu^lin[D_mu xi_nu+D_nu xi_mu] = 0.
```

With random fields the code verifies both identities at double precision. **But this is NOT enough for a physical graviton theory.** On an even lattice, the alternating Nyquist mode `h_23=h_32=(-1)^x1` is a transverse/traceless spatial shear. Its centered difference vanishes in every direction, so `G^lin[h]=0` despite the nontrivial high-frequency field. A forward derivative on the same field has amplitude2. This is a genuine *spurious TT-sector null mode* of the chosen discretized operator, not a success of emergent gravity.

A viable discrete or information-update quantum gravity needs gauge consistency **and** a no-doubler, positive-norm, causal propagator, plus nonlinear first-class constraints and a Lorentzian continuum. It cannot claim to derive Einstein spacetime solely by matching Bianchi identities. Related lattice gauge/difference subtleties appear in [2024 real-time lattice conservation analysis](https://link.springer.com/article/10.1140/epjc/s10052-024-12725-6).

## 5. Two copies activate accessible single-photon entanglement, but consume two photons

A single shared photon `(|10>+|01>)/sqrt2` cannot expose its off-diagonal path coherence through strictly local number-commuting operators on one mode per laboratory. This is an **operational** local number-superselection restriction, not a prohibition on all single-photon nonlocality experiments.

Use **two identically phased copies** in modes A1/B1 and A2/B2. The sector with exactly one photon at each laboratory occurs with probability **1/2**, and its normalized state is

```
(|A1 B2>+|A2 B1>)/sqrt2.
```

Within each laboratory's one-photon **dual-rail** subspace, local Pauli X and Y are number-conserving mode interferometers. Hence this event-ready *conditional* state can attain CHSH **2sqrt2**, without assuming local vacuum↔one-photon Pauli rotations on a single mode.

That shows exactly how the operational SSR bottleneck can be **activated by another physical copy**. The price is two photons, two preparations, phase stability between copies, and a 50% ideal branching success before realistic losses. Event-ready selection must be heralded before Bell settings and loophole accounting; postselected detection alone does not prove a loophole-free Bell violation. Not a universal no-go for protocols using other reference-frame resources. Prior art [SSR accessible entanglement](https://doi.org/10.1103/PhysRevA.79.032109), [single-photon Bell without a shared frame](https://doi.org/10.1103/PhysRevA.88.012111).

## Falsifiability and claim taxonomy

**Mathematically checked:** three-adjoint *one-loop* complete multiplet threshold equality, explicit renormalizable mass-matrix relations, conditional rank-two seesaw from imported neutrino data; finite field inventory and Z4R charge checks; explicit effective W with nonzero F/D-flat condensates; degree-one flat-local-system cohomology; exact discrete *linearized* Bianchi identity and fake TT mode; dual-rail two-copy conditional Bell calculation.

**Not inferred or predicted:** any observed parameter, a realistic 4D particle vacuum, exact gauge/global anomaly freedom, heavy SU5 Higgs sector/proton decay, two-loop unification, a compact singular G2 metric, gravity from microscopic information updates, device-independent experiments, or a theory of everything.

## Top five independent next experiments

1. **E8 global anomaly and R origin:** prove or falsify a compactification-derived Z4R including grav/U1 anomalies and its own dynamics, derive driving fields and cutoff, and stabilize *all* charged and neutral moduli while generating full-rank physical Yukawas.
2. **Proton-safe SU5 spectrum:** run two-loop SM+3x24F+real scalar thresholds and vacuum stability, calculate SU5 X-boson mediated proton lifetime and charged flavor, then seek a symmetry that protects the 10^-12 mass-matrix cancellations.
3. **Compact chiral topology:** construct a complete sourced relative Dirac/colored-SQM theory on a space with nonzero family cup, prove exactly three families, and remove its adjoint exotics *without* Wilson-line breaking of the required gauge group.
4. **Physical quantum gravity:** design an explicit discrete derivative/constraint complex avoiding TT doubling, demonstrate nonperturbative anomaly-free first-class closure, causal unitary gravitons, and the Einstein limit.
5. **Operational photonic and foundational falsifier:** calculate actual resource overhead for local phase references/two-copy activation and event-ready losses; derive a new deviation from QM rather than interpreting standard Bell correlations as TOE evidence.
