# TOE physics-first followthrough: renormalizable E8 vacuum, orbifold GUT escape, global chirality, causal links, quantum vacuum

**2026-11-19 | status: six executed conditional calculations; not a Theory of Everything.**

This packet follows the user's five independent fronts with an additional quantitative photonic gate, and checks the latest parallel commits rather than repeatedly reusing earlier claims. The source census of balanced point-source E8 zero modes and the strict punctured-S3 relative-cup obstruction are **imported** from `cb1a66717`; the prior five-driving-field toric EFT and pure-vacuum nonuniqueness are from `ff5090ff5`; the three-adjoint SU5 benchmark is `017f5cde3`; newer spin^c/overlap and causal Dirac work arrived in `21e8ff606` (read in full). W33 is NOT used as a physical axiom. Known orbifold GUT/Atiyah–Singer/causal-set/CCR structures are literature prior art, not newly discovered laws.

Reproduction:

```powershell
python analysis/toe_20261119_uv_messenger_orbifold_causal_vacuum_followup.py
python -m unittest discover -s tests -p test_toe_20261119_uv_messenger_orbifold_causal_vacuum_followup.py -v
```

Machine-readable certificate: `data/toe_20261119_uv_messenger_orbifold_causal_vacuum_followup.json`.

## 1. Constructive renormalizable completion of the E8 five-driver singlet vacuum

Earlier research had all eight actual E8-charged Spin10 singlets and five gauge-neutral R-charge-2 drivers `X_i`, fixing five algebraically independent invariants

```
I1=AB, I2=DE, I3=AFE, I4=CEG1, I5=CEG2,
A=S12, B=S12conj, C=S13, D=S14,
E=S14conj, F=S24, G1/G2=two independent S34.
```

Gauge charges are the exact Z3 vectors from `sector_census()`; the eight-field U1^3 charge matrix has rank3. `X_i I_i` for degree-three I3,I4,I5 is dimension-four **superpotential** and nonrenormalizable in four dimensions. The most meaningful next question is whether it admits a fully cubic, perturbatively anomaly-neutral mediator UV completion.

**Yes, in a finite added-field N=1 4D EFT.** For each cubic invariant `P_i R_i` with `(P_i,R_i)=(A,FE),(C,EG1),(C,EG2)`, add a *pair* of heavy chiral gauge messengers `Y_i,Z_i` with

```
q_Y=-q_P, q_Z=q_P,
R(Y)=0, R(Z)=2, R(X)=2.
W_i = M Y_i Z_i + X_i P_i Y_i + Z_i R_i + t_i X_i.
```

All W terms have chiral degree at most3 (renormalizable) and R-charge2. Integrating out Y,Z by their holomorphic massive F equations yields

```
Y_i=-R_i/M, Z_i=-X_i P_i/M,
W_eff,i = -X_i P_i R_i/M + t_i X_i.
```

Thus this recovers the previously postulated nonrenormalizable quartic `X_i P_i R_i/M` as an ordinary messenger exchange, *with the sign and coefficient derived algebraically*. The two remaining drivers have W=`X1(AB-t1)+X2(DE-t2)`.

**Important point often missed:** At the desired vacuum `X_i=Z_i=0` but `Y_i=-R_i/M !=0`. These are charged scalar condensates; neglecting them incorrectly reports D=0. With M=10 and the prior exact source charge basis, the previous eight-field squared magnitudes `(2,1,2,1,4,1,1,1)` must be changed to

```
|A,B,C,D,E,F,G1,G2|²=(2.04,1,2.08,1,4,1,1,1).
Y1=Y2=Y3=-0.2, X_i=Z_i=0.
```

Each Y carries the opposite charge of its corresponding P, so the positive A and C adjustments cancel the messenger contributions **exactly**. Set t1=AB, t2=DE and t3/t4/t5=-(P_i Y_i)=P_i R_i/M at this point. All 19 holomorphic F derivatives and all three U1 D terms vanish. We explicitly construct the complete 19-field polynomial W in SymPy, differentiate it independently and check against the hand-built Jacobian.

There are 11 R0 fields (8 original +3 Y) and eight R2 fields (5 drivers+3 Z). The W Hessian has off-diagonal block J of shape8x11, **rank(J)=8**, and full **rank(H)=16**; its three kernel directions are exactly the three broken complexified Abelian gauge directions, checked by J acting on all three gauge tangents. In this truncated 4D gauge model, the vacuum is locally isolated modulo gauge; the supersymmetric nonnegative F+D scalar potential has no extra local gauge-invariant massless chiral directions.

Each added messenger pair has opposite gauge charges, giving zero combined U1^3 and mixed grav-U1 anomalies. Its *fermions* have R charges -1,+1, canceling the mixed U1^2-Z4R and grav-Z4R coefficients *pairwise*. The baseline five-driver gravitational R anomaly parity remains zero modulo2. **This does not cancel any existing anomalous U1 currents in the original E8 spectrum** and is not a global anomaly/inflow proof.

The source also permits formal, one-spurion **diagonal** `16_i 16_i 10_H S_i/M` terms:

```
16_1² 10_34 S12conj/M,
16_2² 10_34 S12/M,
16_3² 10_24 S13/M.
```

We rechecked all three 3-component U1 charges from the actual `10` sector census, and all three spurion fields now have nonzero VEVs. With hypothetical nonzero and independently chosen physical couplings, an illustrative diagonal matrix has full rank3. **But** neither finite gauge invariance nor the renormalizable mediator model derives the physical localized E8 Yukawa integrals; the strict bulk cup on punctured S3 was shown to vanish. These formal masses are NOT an observed charged hierarchy or a physical prediction.

**Hard outstanding questions:** Why exactly three vectorlike mediator pairs and five R2 drivers? Who generates their scales t_i and M? How is exact Z4R produced and eventually broken in supergravity? Can the compact singular G2/source theory supply nonzero matter wavefunction overlaps, correct SM gauge breaking, anomaly inflow and natural mass hierarchies? The constructed 4D messenger model answers none of those. An engineered EFT UV completion is not a full quantum-gravity UV completion.

Related discrete R anomaly subtleties: [Dine & Monteux, 2014](https://doi.org/10.1007/JHEP01(2014)011), and [Note on gauge and gravitational anomalies of discrete Zn symmetries, 2018](https://doi.org/10.1007/JHEP01(2018)015). The mod2 condition is necessary and spectrum-dependent, not sufficient.

## 2. A qualitatively different SU5 escape: two-boundary orbifold projection

The previous three-adjoint 4D SU5 construction only unified the gauge couplings with light masses resulting from `~10^-12` cancellations in large signed mass matrices. Rather than tuning those masses, **change the question: can boundary conditions remove dangerous partners' zero modes altogether?**

Consider a compact fifth dimension with two boundary parity matrices acting by conjugation on SU5:

```
P_0=diag(1,1,1,1,1),
P_pi=diag(1,1,1,-1,-1), det P_pi=+1.
```

The SU5 Lie algebra splits exactly:
- even under P_pi: `su3(8)+su2(3)+u1(1)`, dimension12;
- odd under P_pi: `(3,2,-5/6)+(bar3,2,5/6)`, dimension12.

The code builds all 24 Hermitian traceless generators and verifies the 12/12 parity counts. The even (+,+) fields may have zero Kaluza-Klein modes; odd (+,-) fields do not. For interval length L, free KK levels are n*pi/L and (n+1/2)*pi/L, respectively. **Two boundary conditions matter:** for a five-dimensional Dirac spinor a single Z2 parity would still leave the opposite four-dimensional chirality for the odd generator, so the second boundary and chirality assignments cannot be omitted.

Thus a 5D adjoint fermion can have triplet and octet zero modes without a massless leptoquark-like X partner, while the off-block states are heavy KK modes. This is an established **orbifold GUT mechanism**, and a [2025 5D SU5 x U1PQ construction](https://doi.org/10.1140/epjc/s10052-025-14320-9) explicitly realizes octet/triplet zero-mode selection and analyses two-loop unification. Our new-to-repo result is a direct parity/generator count and comparison to the mass-matrix cancellation gate.

**Not established:** automatic masses for two weak triplets and one light octet (P alone retains both octet and triplet); model-dependent boundary masses/mixings, KK thresholds, proton decay, 5D gauge/supergravity anomaly and source geometry, fermion localization and full SM charged Yukawas remain separate. This is an *alternative architecture*, not a repaired 4D three-adjoint model.

## 3. Global Spin^c family index is charge-dependent, not universally three

The preceding `ff5090ff5` report noted the standard CP2 Spin^c index `(k²-1)/8` for fixed odd k and a chosen k5 ->3. The newest parallel `21e8ff606` builds nontrivial 4D overlap U1 flux indices and cautions that coarse lattice resolution can change the numerical finite-regulator index.

A further global consistency test: tensor the fixed Spin^c spinor bundle with an ordinary complex line bundle `E^q` of integer first Chern class qH. This shifts the *effective determinant* by **2q** and by Atiyah–Singer

```
index(D_(L,E^q)) = ((k+2q)^2-1)/8.
```

For chosen k=5 and q=-2,-1,0,1,2,3 the indices are respectively **0,1,3,6,10,15**. This is exact characteristic-class arithmetic. In particular, *the same* internal Spin^c background gives index 3 in one twist sector and index6/1 in adjacent twist sectors. Claiming a three-family universal chiral gauge multiplet from k5 without specifying how all gauge weights are twisted is not justified. A true G2/Spin10 family index needs the actual associated bundles and source/domain index, not a CP2 numerical coincidence.

CP2 is a compact Euclidean four-manifold used as an internal mathematical example, not four-dimensional physical Lorentzian spacetime; no CP2 compactification is presented. Sources: [Dirac operators and Spin^c geometry](https://georgedouzas.github.io/posts/fundamentals-of-mathematics-for-physicists/part-i-13-spinors-dirac-operator.html); [4D overlap flux and resolution, parallel 21e8ff606](https://github.com/wilcompute/W33-Theory/blob/master/analysis/2026-11-19_spinc_overlap_quantum_gravity_six_fronts.md).

## 4. A fixed microscopic link-thinning parameter does NOT recover bounded causal-neighbor degree

The previous exact 3+1 Poisson sprinkling expected future-link count in a time-1 truncated cone grows as `pi sqrt6 sqrt(rho)`, due to the near-lightcone region. We test a tempting information-hardware patch: accept each actual link independently with probability `exp(-alpha rho V_interval)`, where V is the **continuum embedding** Alexandrov volume, alpha>=0 is fixed and independent of rho, and the ordinary link probability is `exp(-rho V)`.

With `V=pi s²/24` and the exact cone measure `g(s)=sqrt(1-s)-s log((1+sqrt(1-s))/sqrt(s))`,

```
E[L_retained]=pi rho int_0^1 ds exp[-(1+alpha)rho*pi*s²/24] g(s)
            ~ pi sqrt(6/(1+alpha)) sqrt(rho).
```

The analytic limit follows from rescaling u=s sqrt(rho) and g(s)->1. Numeric quadrature at rho=160,2560,40960 and alpha=0,1,3,15 validates the asymptotic coefficient and that the expected retained degree still grows as sqrt(rho). Therefore **no fixed finite positive alpha within this family yields constant nearest-neighbor degree**. This is a narrow model-specific no-go, not a theorem forbidding causal quantum gravity or nonlocal kernels.

Crucially V is not observable from the empty causal interval itself; the thinning rule uses extra embedding/density information, so it is NOT an intrinsically order-only update rule. Causal-set nonlocality and possible mesoscopic operators are established in [Surya's causal sets review](https://doi.org/10.1007/s41114-019-0023-1) and [Benincasa-Dowker scalar curvature](https://doi.org/10.1103/PhysRevLett.104.181301). A successful fundamental model needs a covariant intrinsic mesoscopic kernel and an honest 3+1 Einstein/graviton continuum, not merely a finite directed graph.

## 5. Vacuum selection: energy minimization succeeds only after choosing a Hamiltonian

For a single quantum CCR pair `[q,p]=i`, the prior pure Gaussian family

```
V_r=diag(exp(2r),exp(-2r))/2
```

gives positive pure states with identical commutator for all r. If a positive oscillator Hamiltonian `H_omega=(p²+omega² q²)/2` is **supplied**, its energy

```
E_r(omega)=[exp(-2r)+omega² exp(2r)]/4
```

has unique minimum at `r=-0.5 ln(omega)` with `Emin=omega/2`. We tested omega=.5,1,2,4: distinct pure ground covariances all with exactly the same commutator. Thus a 'select minimum-energy vacuum' rule is not microscopically explanatory until a preferred time evolution and Hamiltonian are derived. It is not a proof that a causal Sorkin-Johnston construction fails; SJ chooses extra inner-product/spectral data, and the interacting Hadamard/positivity problem remains.

## 6. Experimental photon failure threshold in radians and real herald rate

The previous dual-rail two-copy photon/SSR activation test yielded conditional `Smax=2 w sqrt(1+exp(-sigma²))`, where sigma is Gaussian relative-source phase standard deviation (radians) and w is a model-specific white-noise Bell fraction. Solve the Bell inequality `Smax>2`:

```
sigma < sqrt[-ln(1/w²-1)].
```

At w=.82, the exact threshold is **sigma<0.8479741 rad**. A sigma above this cannot violate CHSH within this *specified* depolarization/dephasing model even with optimal observables. With source transmission eta=.8, the ideal two-copy one-per-lab herald event rate is `eta²/2=.32` per two-photon emission pair. If there are also two independent QND herald detectors each of efficiency .7, the modeled event rate drops to **.1568**, before final detection loss.

This is an independent quantitative feasibility/failure threshold. It uses ordinary quantum mechanics and assumed noise/loss, not a novel TOE prediction or a valid loophole-free experimental certification.

## Verdict and five orthogonal next steps

**Demonstrated under assumptions:** exact 19-field renormalizable supersymmetric F/D vacuum with no local physical singlet moduli and anomaly-neutral messenger pairs; two-boundary SU5 parity projection of unwanted X zero modes; charge-dependent twisted Spin^c index; density-independent causal thinning still grows; vacuum energy requires a selected Hamiltonian; photon Bell threshold and herald overhead.

**Not demonstrated:** a compact E8/G2 derived field theory, actual source overlap-generated charged masses, full anomaly cancellation, radiatively natural unified spectrum/proton safety, dynamic 4D Einstein and light-cone propagation, unique positive interacting vacuum/Born probabilities, or an observation disagreeing with standard QM.

Top independent tasks to execute next:

1. **E8 compact UV origin:** derive the six messenger and five driver zero modes plus their renormalizable W, t_i, M and physical Yukawa coefficients from one singular geometry; calculate all global/Abelian/discrete anomalies and true SM breaking.
2. **GUT mass/geometry route:** implement an actual 5D orbifold interval with correct fermion chirality, complete boundary action and KK spectrum, then fit two-loop unification and dimension-six proton decay without per-component fine-tuning.
3. **G2 family/adjoint chirality:** construct an honest globally compact 7D index complex with all gauge-associated bundles, source defects and spin^c twists, and verify exactly three desired families with no exotics.
4. **Causal Einstein exchange kernel:** find an intrinsic Lorentz-covariant finite/controlled-neighbor nonlocal kernel and a stable, positive-norm 3+1 graviton/first-class constraint continuum, rather than just weakening the link graph.
5. **Quantum state and decisive experiment:** derive preferred time/Hamiltonian and positive Hadamard state together with operational Born probabilities, then specify a photonic or gravitational prediction quantitatively distinct from both GR and conventional QM.
