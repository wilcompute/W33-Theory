# Five-front continuation: native gauge dynamics, constitutive freedom, and a central-flux obstruction

27 October 2026. Continuation of commit619cd06e5, with seven physics controls and two intake controls. This packet executes explicit calculations on each proposed research front, adds a microscopic induction test and a finite-momentum constitutive probe, and records the remaining work. **The TOE is not solved; the full historical reading remains unfinished.**

## Reproduce and inspect

```
python analysis/w33_20261027_five_front_followthrough.py
python -m pytest -q tests/test_w33_20261027_five_front_followthrough.py
python analysis/w33_20261027_research_intake.py
```

The science certificate is `data/w33_20261027_five_front_followthrough.json`. The intake manifest is `analysis/2026-10-27_research_intake_coverage.json`. The archive producer requires the existing historical Git objects and Poppler; its scratch files duplicate those objects rather than introduce new scientific data. The archive-check test explicitly skips on clean checkouts without these regenerable scratch copies. The mathematical tests use committed source/data.

Prior-art owners, read and used here:

* `analysis/2026-10-27_native_gauge_propagation_completion.md` and `analysis/w33_20261027_native_bloch_face_module.py`: the selected105-face obstruction, six16-traversal commutators, generic rank108, harmonic GramM and supplied matched loop metricH0.
* `analysis/2026-10-23_native_gq24_css_135_4_4.md` and `analysis/w33_20261023_native_135_4_4_css.py`: the finite code and original selected faces. Its code parameters are not new results of this continuation.
* `analysis/PASS12188_NATIVE_PERIOD_SYMPLECTIC_REPAIR.md`, `analysis/w33_pass12188_native_period_symplectic_repair.py`, and `analysis/w33_pass12189_12193_five_bridges.py`: the actual native period action, two inequivalent Eisenstein planes and contragredient conventions. We use momentumT=R^-T when testing invariance ofM, notR itself.
* `analysis/w33_pass10950_clock_albert_lorentz_spinor.py`, `data/w33_qpsi_matter_parity_e8_d8_bridge.json`, and `artifacts/canonical_su3_gauge_and_cubic.json`: the27 internal charges and45 signed cubic terms. Their branching and charge invariance are existing results.
* `analysis/w33_20261010_toe38_local_maxwell_2complex.py`, `analysis/2026-10-13_toe58_five_physics_postparallel_audit.md`, `analysis/2026-10-13_toe62_connected_research_recovery_record.md`: earlier different-cover commutators, compact rotor flux coordinates and Gauss-constrained matter methods.
* `analysis/w33_20261013_toe59_lorentz_velocity_gate.py`: the prior warning that spatial gauge Ward identities cannot fix independent electric and fermion temporal normalizations.

Result searches covered the result index, current Python/JSON/Markdown/TeX/HTML corpus, and the declared Holotrade source where relevant. No global mathematical priority is claimed for exterior algebra, compact lattice gauge theory, or dimensional reduction.

## 1. Common-cone classification leaves exactly one constitutive parameter

LetH be an arbitrary symmetric6x6 metric on the six commutator fluxes. With the prior period matrixW and fixed harmonic electric GramM, write

```
C(n)x = (Wn) wedge (Wx),
C(n)^T H C(n) = ((n^T M n)M-(Mn)(Mn)^T)/27.
```

This is a linear problem in21 unknown entries ofH. Evaluating the quadratic-in-n identity on the four coordinate vectors and their six pairwise sums gives all its coefficients. Exact rational elimination has **rank20**. The complete solution is

```
H(theta)=H0+theta J,
J_(01,23)=+1, J_(02,13)=-1, J_(03,12)=+1,
```

with symmetric companion entries and all others zero. The null direction is the wedge pairing of two2-forms in four dimensions. SinceC(n)x is decomposable, its contraction with this four-form vanishes. This is an exact classification for the fixed target symbol, not merely a fit on sampled rays.

For the actual nativeH0, (JH0)^2=4I, Tr(JH0)=0 and

```
det(H0+theta J)=(4-theta^2)^3.
```

Consequently positivity is exactly **-2<theta<2**. Imposing an orientation-reversing constitutive symmetry would settheta=0, but imposing that symmetry and the target cone is still additional physics. This result narrows the missing microscopic selection problem rather than solving it.

The relation to metric/dilaton/axion constitutive freedom in ordinary spacetime electrodynamics is useful background: [Hehl2016](https://arxiv.org/abs/1601.00320). Here we have **four spatial periods and external Hamiltonian time**. OurJ is a spatial four-form ambiguity of this model; it is not automatically the spacetime axion term of3+1 electromagnetism, and has no demonstrated relation to strongCP.

### Extra probe: the ambiguity becomes visible at finite lattice momentum

For the literal translated loops, F_comm(k)^dag J F_comm(k) is nonzero. On k=t(1,2,-1,1), its operator norm divided byt^3 approaches about31.97 at the smallest sample. Thus the leading symbol is blind to a parameter that the finite lattice can detect. Thetheta=-1,0,+1 spectra are frozen separately. This is a discretization effect, not a measured optical activity or an exact topological action.

## 2. A three-dimensional projection exists, but it must break native symmetry

The native momentum action preservesM. Its rational commutant has dimension4 and splits as two copies ofQ(sqrt(-3)), one for each inequivalent order-three plane. An idempotent in each field is0 or1, so the complete set of symmetry-invariant rational projector ranks is

```
0, 2, 4; never3.
```

Because a finite-group invariant subspace admits an invariant rational orthogonal projector, there is no hidden rational3D invariant subspace missed by this criterion. A symmetry-preserving3+1 truncation is therefore unavailable in this four-period representation.

There is, however, a concrete integral metric reflection:

```
R=[-1 0 0 0
    1 1 0 0
   -1 0 1 0
    0 0 0 1],
R^2=I, detR=-1, R^T M R=M.
```

Its odd line is generated by(-2,1,-1,0), and its even projector(I+R)/2 has rank3. It does not commute with the native group. This names an actual lattice isometry rather than an abstract instruction to discard a dimension.

Ordinary circle compactification leaves **two3D photon polarizations plus one massless scalar** from the compact gauge component. Zero-mode gauge transformations cannot remove that scalar. An S1/Z2-type assignment with tangent gauge components even and compact component odd removes its zero mode. Such assignments are standard; see [Arai–Blaschke–Eto–Sakai2018](https://academic.oup.com/ptep/article/2018/6/063B02/5043095).

The present reflection has **not** been lifted to an automorphism of the full selected-face microscopic action, and no compactification radius is stabilized. Nor is the resulting charged theory automatically consistent at boundaries: orbifold fixed points can carry localized anomalies even when integrated anomalies cancel, as shown by [Scrucca–Serone–Silvestrini–Zwirner](https://arxiv.org/abs/hep-th/0110073). The calculation supplies a continuum candidate and an exact symmetry cost, not an emergent physical dimension.

## 3. A compact periodic interaction realizes the requestedH0 exactly

The previous quadratic flux energy was noncompact. To construct an actual periodic interaction, write

```
V(f)=sum_q w_q(1-cos(q.f)), w_q>0, q in Z^6.
```

All six unit harmonics are included with coefficient1/100. A linear program locates21 further harmonics, and exact rational elimination verifies their weights and

```
sum_q w_q q q^T = H0.
```

There are **27 terms**, all charge-vector entries are only **-1,0,+1**, and every weight is strictly positive. The certificate contains the full rational specification. The six unit harmonics prove that the only global minimum on the six-flux torus is f=0 modulo2pi. Thus compactness does not obstruct this harmonic metric. The LP is used to find a feasible decomposition, not to claim optimality.

Each flux belongs to a finite native loop. Products of up to six loop phases are finite-support gauge-invariant interactions, but they are additional multi-loop couplings; this is not a demonstrated nearest-neighbor hardware Hamiltonian. Other higher-order interactions can share the same Hessian, so compact completion does not uniquely select the theory.

### Compact quantum calculation on actual lifted native loops

Lift the first two prior commutators to the finite Z3^4 cover and take their actual supporting links. After cancellations their union is a connected **19-vertex,20-link theta graph**, with paths of lengths4,8,8. Its two integral cycle rows obey

```
C B=0,
C C^T=[12 4;4 12].
```

This uses two spatial loop coordinates, not a fictitious two-link graph. Choose the corresponding principalH0 block with periodic potential

```
(10/9)(1-cos f1)+2(1-cos f2)+(5/3)(1-cos(f1-f2)).
```

In the electric basism in Z^2, E=C^T m, electric energy is(g^2/2)|E|^2 and magnetic cosines are integer shifts. Gauss's law holds exactly for every retained basis state. Hard-wall cutoffsL=2,4,6,8,10 give dimensions25 through441, with variationally decreasing ground energies.

| g | E0 atL=10 | E1-E0 | largestL8-toL10 ground-energy change |
|---|---:|---:|---:|
|0.5|5.3882634722|4.4484256137|4.9e-12|
|1|4.0717963469|5.8784888937|5.7e-14|
|2|1.1847909663|23.7955464417|1.1e-12|

Wilson cosine expectations and boundary probabilities are also frozen. These differences and boundary tails are numerical convergence diagnostics, **not rigorous infinite-cutoff error bounds**. This small model has a positive finite-patch gap; it does not establish a thermodynamic phase diagram, confinement, deconfinement, or a continuum photon. Standard flux-Hamiltonian context: [Kaplan–Stryker2020](https://doi.org/10.1103/PhysRevD.102.094515).

## 4. Explicit internal charge coupling, with dynamical Gauss controls

Use the actual signed45-termE6 cubic and the already-ownedQpsi dictionary anchored at internal index0:

```
27=16_(+1)+10_(-2)+1_(+4).
```

All45 terms have charge zero:40 of type(-2,1,1),5 of type(-2,-2,4). On every native spatial edgev->w, the named charge-subgroup hopping is

```
-sum_A t_A psi_(w,A)^dag U_edge^(q_A) psi_(v,A)+h.c.,
G_v=divE_v-sum_A q_A n_(v,A)+background_v.
```

For every internal component, the gauge phase is exactly

```
-q chi_w+q(chi_w-chi_v)+q chi_v=0.
```

The spatial vertexv and the internalE6 indexA are separate tensor factors. Their equal cardinalities are never used to identify them.

On the19-site patch, allow one charged particle to hop between the endpoints of one actual link. In a transferred sector, the electric string increases byq times that link, and the charge density changes by its divergence. Exact Gauss constraints hold in every electric/occupation basis state. Forq=1,-2,4, theL8 Hamiltonians have dimension578 and positive gaps approximately1.06810,2.40676,5.62726. Static endpoint-charge controls are separate.

This is an explicit **U1 subgroup interface** and one-particle dynamical check. It does not gauge all ofE6, derive a chiral regulator, compute a full many-body vacuum, or identify a physical three-generation spectrum. In particular, charge trace identities do not by themselves establish anomaly cancellation for the projected interacting boundary theory.

### Extra probe: a native charged determinant prefers central flux but fails the target metric

As a concrete microscopic candidate, integrate out static spinless hopping copies with charge multiplicities(16,10,1) on this actual19-site graph, atmu=0,t=1. Use analytic thermal spectral derivatives, including divided differences in degenerate eigenspaces, rather than cancellation-prone finite differences.

All27 charges satisfyq=1 mod3. At flux(f1,f2)=(2pi/3,4pi/3), the species hopping matrices are **gauge-equivalent with the same spectrum**, rather than literally equal in the harmonic gauge. Explicit vertex-phase intertwiners are checked on every patch link. Their response coefficients obey

```
sum q=0, sum q^2=72, sum q^3=0, sum q^4=432.
```

The central flux is stationary at every temperature because the first derivative is proportional tosumq. The third derivative vanishes as well. This is the phase action of theE6 center on the27, realized here as a native-loop response; the underlying charge branching and trace identities are standard/prior results.

On the theta graph, exchange of the two equal-length paths combined with flux conjugation fixes this central background. Hence its induced Hessian has equal diagonal entries at everyT. The requestedH0 principal block instead has diagonal25/9 and11/3: **the central induced Hessian cannot be proportional to that target**. This is a structural obstruction for this particular microscopic candidate.

AtT=0.25, the central Hessian eigenvalues are0.2064532 and0.2960277, while zero flux has negative curvature. AtT=1 and2, the central curvature remains positive but falls rapidly. A13x13 grid and five local optimizations locate central minima at lowerT; global minimality is not certified, and the highT optimizer becomes insensitive as the landscape flattens. The unequal target shape is excluded by symmetry, independently of those numerical minimizations. A static spatial determinant still does not supply the electric response or a relativistic action.

## 5. Historical intake is now archival-complete, not reading-complete

The frozen481 historical commits were exported **in full**, including binary patches and separate diffs against both parents of the single merge commit, with streaming SHA256 and gzip archives:59,133,515 uncompressed patch bytes. All210 PDF pages were separately extracted and hashed. The manifest does not label extraction as model reading.

This continuation fully read PDF pages72-94 and inspected a rendered page89. It also read the complete incominga0db8f2a2 formula-index patch. The remaining historical reading is explicitly open. The page findings reinforce the current scope:

* Pages72-76: a chosen Albert real form gives an internal Lorentzian slice, but does not fix propagating gauge dynamics.
* Pages77-79: the proposed equivariant tick-to-clock bijection was retracted; counts cannot replace maps.
* Pages80-86: untwisted family counts, complete orbifold spectra, hypercharge and radius conditions have different scopes and several corrections. Our charge-compatible hopping does not bypass those results.
* Pages86-90: the Peirce charge dictionary and its parity/spin interpretation are existing results; page90 explicitly separates internalLorentz symmetry from physical spacetime.
* Pages91-94: the finite1+3+8 module is not a gauge Lie algebra, and a Pauli-stableE6 action is excluded. Our separate internal charge index does not supply or claim that missing nonabelian action.

Across all paperTeX sources,1216 literalcert-macro mentions resolve to1185 available local files,30 existing commit objects and one declaredHolotrade file. IgnoredJSON and external citations are resolved explicitly to avoid false missing-file reports. **Existence is not proof**, and no claim is made that all those witnesses were executed or fully read.

## Validation and operating record

The tests check the four-form nullspace/positivity, actual integer reflection, exact rational compact Hessian and periodicity, lifted-loop and charged-transfer Gauss identities, rotor variational behavior, charge-center identities, the induced-metric obstruction, and archive hashes/coverage. The raw-archive hash check is local/regenerable as stated above. This is a focused packet, not a claim that the entire legacy suite or hostedCI passes.

The repo's GitKraken transport remained closed at intake. LocalGit was used as the recorded fallback; incominga0db8f2a2 was fully reviewed and fast-forwarded. Shared dirty work and the read-only project mirror were preserved. Continuity initially accepted supported bounded-writer logging; a later editor-owned lock rejected one attempt, so deliberate changes and the failure were also recorded durably inSESSION_NOTES.md.

## Five independent next experiments

1. **Temporal microscopic induction:** calculate both electric and magnetic response from one native matter model, and test the complete common-cone requirement rather than a spatial Hessian alone.
2. **Microscopic orbifold lift:** construct the reflection as a chain map on the entire translated link/face module, with boundary Gauss laws and localized anomaly tests.
3. **Growing compact patches:** enlarge the current two-loop sector with controlled truncations and Wilson correlations; distinguish finite gaps from thermodynamic phases.
4. **Chiral nonabelian interface:** supply an actual regulator and gauge connection for the intended internal representation, with index, doublers and anomaly checks.
5. **Complete content audit:** read the remaining archived patches and paper pages, updating only verified reading flags and testing every discovered prior result against this construction.
