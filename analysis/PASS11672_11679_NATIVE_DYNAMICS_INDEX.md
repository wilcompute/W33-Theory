# Passes11672–11679: a dynamical native sextet and a kinetic triplet on the resolved kernel geometry

Reservation62cb3c3a7 was pushed before computation. Producer: `analysis/w33_pass11672_11679_native_dynamics_index.py`; source-bound certificate: `data/w33_pass11672_11679_native_dynamics_index.json`; independent regressions: `tests/test_w33_pass11672_11679_native_dynamics_index.py`.

The strongest constructive results are a global, renormalizable native scalar vacuum with a nonzero sextet; a complete38-coordinate scalar-plus-U1 one-loop local vacuum; and a specified spin-c kinetic operator on an actual exceptional divisor whose zero-mode representation is exactly the earlier three-dimensional mass kernel. They execute the flavor, matching and chirality investigations with concrete objects. Gravity and vacuum energy also receive actual constrained dynamics, but their Einstein and absolute-energy requirements remain unsolved. This packet does not solve the TOE or predict observed masses, mixing or couplings.

## Corpus and literature ownership

Fresh GitKraken fetch/status/history review found no incoming changes beyond the previous verification receipt76764cd73. The past-three-day commit subjects were reviewed; this turn does not claim a fresh full-diff reading of every older commit. Current result searches covered `RESULTS_INDEX.md`, Python/Markdown/JSON/TeX/HTML sources, the latest site cards, and the forty-points physics section. Its area-law paragraph explicitly says gravity is hosted, not derived. The main paper remains unchanged.

11663 owns the actual normal derivative and the classical Maschke quartics.11664–11671 owns the actual G25/H27 kernel weld, polarized parent maps, bare Dirac stability and parameter-space zero line.1068/1077 owns G25 inside G32;11271/11636 owns symmetric E6-family Yukawas.11286 owns engineered distinct-spectrum sextet CP potentials; the equal-spectrum parent below does not supersede it.11306 owns parametrized native graph constraints,11639 the nonlinear tree-exchange obstruction, and11629 compact flux rotors.11563/11566 owns frame compatibility and a Wilson-regulated kinetic candidate. The earlier2026-09-23 physics packet owns the odd-dimensional Kramers obstruction; the four-dimensional group-specific obstruction here is different.

Result searches for `23/8`, `(2,1,1,1)`,31 positive directions, exceptional Dirac indices, canonical bundles, Serre duality and native octagon gauge actions were performed. Numeric matches in monitor/code certificates were read as different objects. No claim to general mathematical priority is made. In particular, projective-space Dirac indices and fermion constructions are classical: [Dolan–Nash](https://arxiv.org/abs/hep-th/0207078) and [Ben Halima](https://dml.cz/handle/10338.dmlcz/119734). The new application is to the actual resolved mass-kernel bundle and its explicit stabilizer characters.

The broad compound guard also pointed to `PASS2300_2305_FIVE_FRONTIERS_RELEASE.md`, `analysis/BT2300_BT2305_five_frontiers.md`, `PASS1030_EIGHTY_CARRIER_ORIENTATION_OBSTRUCTION.md`, `analysis/BT1741_BT1744_execution_summary.md`, `analysis/BT888_color_is_matter_heisenberg.md`, `analysis/PASS11413_11417_PIN_REGGE_VACUUM_NOISE.md`, `analysis/2026-07-15_pass357_master_forcing_table.md`, `analysis/2026-09-23_execute_all5_plus3_physics_frontier.md` and `analysis/BT1621_BT1623_sm_bridge_comparator.md`. These reports were read: they own different Weil, finite color/architecture, supplied flavor, Regge, compiler and parameter-comparator objects. Older physical or numerical interpretations are not imported as continuum derivations. Broad guard candidates remain advisory rather than a claim of blanket novelty. The general exposition was result-searched, not newly read in full.

##11672: a globally minimized dynamical sextet, without a Yukawa lookup

Retain the native complex fields f4, q10=Sym2(f4), z5. Write the symmetric4x4 matrixT using normalized off-diagonal coordinates qij/sqrt2, so ||q||²=Tr(T Tdag). The earlier fully polarized maps satisfy P(Q(f))=sqrtG F(f), and intertwine on arbitraryq. The action is

```
V0=(||f||²-1)²+||q-Q(f)||²+||z-P(q)||²+||z||²
   -5||q||²/4+Tr[(T Tdag)²]/8.
```

All terms have field degree at most four. The new matrix quartic is U4-invariant and hence preserves the native G32 covariance; the earlier P term is only native-group invariant. The theory also preserves the common U1 with charges f1,q2,z4.

There is an obstruction to using only a radial q quartic. A nonzero unsourced transverse q eigenvalue forces the common radial coefficient to vanish. The sourced axis equation would then require0=||f||². A matrix quartic gives separate singular-value equations and escapes this obstruction.

Let s=||f||² and u be the largest Takagi singular value ofT. The contraction inequality gives Re<ffT,T> <= su. Each remaining singular value minimizes `-sigma²/4+sigma⁴/8` at sigma=1. Dropping the nonnegative z/P terms and minimizing s gives the rigorous global bound

```
V0 >= u⁴/8-3u²/4-u+1/8
   = -23/8+(u-2)²(u²+4u+6)/8.
```

It is attained at

```
f=(sqrt(3/2),0,0,0),  T=diag(2,1,1,1),  z=0, P(q)=0.
```

Thus the global minimum is exactly-23/8. All38 real first derivatives vanish. The full tree Hessian has31 positive eigenvalues and seven zero eigenvalues; its smallest positive value is about.4076693. The actual transverse Sym2(3) sextet isTtrans=I3, full rank. All three tree singular values are equal. Seven Hessian zeros alone do not classify a smooth seven-dimensional vacuum manifold; some may be lifted beyond quadratic order.

The coefficients are supplied. This is a native-field construction, not a derivation of those coefficients or an E6 UV theory.

##11673: all38 scalar modes, a gauged phase, and full one-loop relaxation

Promote the parent's U1 to a gauge symmetry, with supplied g=.1 and canonical kinetic terms `sum |D phi|²-F²/4`. There are no chiral fermions in this bosonic completion. Real coordinatesx have canonical fields sqrt2x; therefore scalar squared masses are eigenvalues of Htree/2, not Htree. The gauge squared mass is

```
mA²=2g²(||f||²+4||q||²+16||z||²).
```

It is.59 at the tree reference. In the specified Euclidean shell A=.01,B=.25, Landau gauge, use

```
Veff=V0+1/(32pi²) integral_A^B x[
         sum38 log(1+mu_j(x)/x)+3log(1+mA²(x)/x)]dx.
```

Here the integration variable is squared momentum, whereas the argument of the field-dependent Hessian is the38-coordinate field vector. The scalar sum includes every tree zero and every heavy scalar. The three gauge polarizations are explicit; massless Landau-gauge ghost terms are field independent in this inventory.

The Hessian is quadratic in fields. Exact polarization constructs all first and second mass-matrix derivatives. For

```
w(mu)=integral_A^B x/(x+mu)dx
     =B-A-mu log((B+mu)/(A+mu)),
```

spectral divided differences ofw give the full analytic determinant Hessian, including noncommuting mass derivatives. This avoids differentiating eigenvalues individually at degeneracy. The complete tree/loop tadpoles are relaxed in all38 coordinates, retaining one phase orbit.

The resulting stationary point has

- gradient norm3.32e-14;
- one common-phase gauge zero satisfying Ht=0 directly;
-37 positive real normal curvatures, minimum5.155751469e-5;
- three small normal-curvature pairs/branches above5e-5, lifting the six extra tree flats;
- transverse sextet singular values approximately .9987951563,.9987951563,.9987095607.

The tiny2+1 splitting is generated by this action's scalar loops; it is not an imposed eigenvalue target. It does not give three distinct observed masses or CKM/PMNS mixing. The selected solution is CP even. The27 diagonal cube-root phase choices are on a native symmetry orbit: the D1 ray stabilizer combined with the common phase rotates one transverse coordinate, and SUM transports it to the other coordinates. Complex cube phases therefore do not by themselves establish broken generalized CP. Numerical searches and positive local curvature do not prove that these are all global quantum minima.

### An angular UV result that does not depend on a fitted counterterm

The divergent terms are `-Tr(mu²)log(B/A)/(64pi²)` and `-3mA⁴log(B/A)/(64pi²)` in the UV expansion, along with lower power divergences. Counterterms and running remain necessary in normal/radial directions.

On the diagonal three-phase family, however, **every native-group/U1-invariant counterterm of field degree<=4 is phase independent**. Restrict a monomial to the nonzero f0,q0,q11,q22,q33 and their conjugates. Independent native cube phases force each transverse phase frequency to be divisible by3. A nonzero such frequency requires at least three charged q factors; degree<=4 cannot cancel their U1 charge with the remaining fields. Opposite transverse frequencies require at least six factors. Enumeration checks every allowed monomial, independently of the loop formula.

Consequently the scalar angular determinant difference is UV finite. Direct controls give Tr(mu)=489/2 and Tr(mu²)=45993/8 at all tested phase choices. The phase difference is positive for the tested pi-versus-zero control. This result removes arbitrary renormalizable phase counterterms on that family; it does not protect against higher-degree EFT operators, determine finite radial matching, or establish the global phase landscape.

This is a specified bosonic scalar+U1 action. Earlier E6 fixed-spurion Dirac models, fermion loops, E6/SU3 gauge loops and the unequal-cap gravity laboratory have different inventories and are not silently combined. The loop certificate is numerical, not interval certified; its stable stationary point belongs to the finite-shell action and Landau gauge, not a demonstrated continuum UV fixed point.

##11674: the actual bulk zero-line kinetic index is minus ten

The five Maschke quartics have40 base points. At every point, the projective derivative has rank3, so the local base ideal is the maximal ideal to first order. On

```
X=Bl40 CP3,
L=O_X(-4H+sum E_i),
KX=O_X(-4H+2sum E_i),
KX^(1/2)=O_X(-2H+sum E_i),
```

the quartic map resolves and L is the extension of the actual mass-zero line. X is spin. Choose a Kahler metric and Chern connections and define the genuine elliptic kinetic operator

```
D_L=sqrt2(dbar+dbar_dagger)
on Lambda^(0,*) tensor KX^(1/2) tensor L.
```

Its Dolbeault coefficient bundle is O_X(-6H+2sumE). Adding an exceptional divisor once or twice contributes O_E(-1) or O_E(-2), both acyclic onCP2. Thus its cohomology equals that of O_CP3(-6): `(0,0,0,10)`. The spin Dirac index is exactly-10.

Serre duality identifies the ten zero modes with H0(O(2))dual=Sym2(C4), the same representation as the parent's ten scalar coordinates. Every tested canonical Weil generator has determinant1, so this equality has no hidden determinant character for that lift. It is a representation connection, not an identification of bosons with fermions. For central extensions with a nontrivial determinant, spin-lift characters must be tracked separately.

The independent A-hat integral gives index(O(k))=(k³-k)/6 on ordinaryCP3. No integer line twist gives index3: |k|>=3 gives magnitude>=4; k=-2..2 gives -1,0,0,0,1. Three zero Dirac singular masses were never a chiral index.

##11675: true nonlinear Gauss constraints on the native holonomy graph

The actual Levi graph has80 vertices,160 edges and exactly1620 girth-eight cycles. Give each edge a suppliedSU2 link Ue and its cotangent electric momentum. The usual left/right moment maps give

```
Gv=sum_in Le-sum_out Ad(Ue^-1)Le,
{Gv^a,Gw^b}=delta_vw epsilon_abc Gv^c,
H=sum_e |Le|²/(2I)+kappa sum_all1620_octagons(1-ReTrW/2).
```

Wilson traces conjugate at their base vertex, so the magnetic energy is gauge invariant and `{G,H}=0` exactly. Using every shortest cycle makes the loop set graph-automorphism invariant. Noncommuting, nonflat links are explicitly evaluated; independent vertex frame changes preserve all1620 trace values. At a generic irreducible connection, the phase space960 reduces by240 first-class Gauss constraints to480 dimensions. Singular stabilizer strata require separate counting.

This replaces the earlier four supplied commuting fiber projectors with actual non-Abelian nonlinear constraints and propagating link variables. It is **gauge dynamics**, not Einstein gravity. [Kogut–Susskind](https://journals.aps.org/prd/abstract/10.1103/PhysRevD.11.395) owns the Hamiltonian method; the native graph/all-shortest-loop implementation is what is constructed here.

A gravitational branch link must intertwine not only its constraints but also their field-dependent inverse-metric structure operators. It additionally needs Hamiltonian and spatial diffeomorphism constraints. None follows from Gauss closure or a Wilson phase on a free polarization register. The certified11639 metric-cycle lapse obstruction remains in force; this SU2 action neither supersedes nor evades it by a claimed graviton count. [Metric-cycle gravity](https://arxiv.org/abs/1410.7774) and [HR bimetric constraints](https://arxiv.org/abs/1109.3515) remain imported theories.

##11676: a neutral membrane reference gives a flux measure, but retains absolute energy

Supply two compact rotors, imposing G=n1+n2=0. Their physical states are |n,-n>. The neutral dressed transition S1 S2dag preserves this constraint; a single undressed shift has zero physical projection. In the benchmark

```
H=rho+n²-.2(S1 S2dag+h.c.),
```

the ground state supplies an actual flux probability measure, rather than an assumed coherent state or independently prescribed Markov distribution. Finite windows -21..21 and -31..31 agree in ground energy to the stored tolerance; edge probabilities are negligible and shifts never wrap around. The positive excitation gap is about1.06180167.

The reference compensator restores gauge-invariant coherence. Yet the constant response is exactly

```
E0(rho+C)=E0(rho)+C,
probabilities(rho+C)=probabilities(rho).
```

Restoring suppliedV,q gives VC and Vq²n². A constant term is harmless to probabilities on a fixed background but remains in a gravitational Hamiltonian constraint. Thus this dynamics does not select a small CC. Compact topology, reference inventory, charges, volume, gravitational membrane bounce and cosmological state remain inputs. It builds on11629 and the classical [Bousso–Polchinski flux mechanism](https://arxiv.org/abs/hep-th/0004134); it is not a new neutralization theorem.

##11677: an exact triplet kinetic operator on one exceptional divisor

The blowup supplies a concreteCP2 exceptional divisor E at each Witting point. CP2 is not spin because c1=3h is odd, but has its canonical spin-c Dolbeault operator. On one chosen E, let chi be the axis character and R the actual mass-kernel triplet. Projective tangent directions transform by W=chi^-1R.

The actual zero-line restriction retains its linearization:

```
L|E=O_E(-1) tensor chi.
B=(L|E)^4 tensor det(W)^-1
 =O_E(-4) tensor det(W)^-1 tensor chi,
```

because chi³=1 for the tested ray stabilizer. Define D_E=sqrt2(dbar_B+dbar_Bdag) on Lambda^(0,*)tensorB. Equivariant Serre duality gives

```
H²(O_E(-4))=W tensor det(W),
H²(B)=W tensor chi=R,
H*(B)=(0,0,3),  index D_E=+3.
```

The determinant correction is essential; dropping it gives the wrong G25 character even when H27 alone cannot see the error. Likewise, dividing transverse vectors by the axis phase is essential outside fixed-vectorH27. The tests check literal generator equality `chi^4 W=R`, not dimension matching.

This is an actual kinetic construction carrying precisely the earlier kernel representation. It **does not derive defect localization or the fourth-power twist**. Activating all40 equal defect operators gives120 modes. Choosing one exceptional divisor as an internal compactification changes the physical model and its dimensional interpretation. Dolan–Nash's projective-space index work remains prior art; the new interface is this resolved normal-map divisor and its exact phase/determinant characters.

##11678: representations, anomaly signs and the UV inventory

Under a continuousSU3 family extension, the quadratic bulk representation restricts to1+3+6. Cubic traces of diag(1,1,-2) give A(6)=7A(3). The negative bulk Dolbeault chirality therefore gives signed anomaly-8, or-216 if tensored with E6's27. The single positive defect triplet gives+27 when tensored with27. Neither inventory is anomaly closed.11271 already supplies a spectator strategy for the latter; no new cancellation is inferred from the number ten.

These are conditional continuousSU3 anomalies, not anomalies assigned to finite G25 by dimension alone. The dynamical conjugate sextet can enter the earlier symmetric E6 operator

```
dABC psi_i^A psi_j^B h^C conjugate(Ttrans)^{ij}/M.
```

This is a dimension-five interface; an E6 Higgs and actual mediators are required. The bosonic U1 inventory gives one-loop beta coefficient `(4+4*10+16*5)/3=124/3`: it does not supply a UV asymptotically free completion. Adding charged Weyls changes anomaly and running budgets.

##11679: whyCP3 is not automatically an invariant four-dimensional twistor spacetime

For the actual odd Weil4, the canonical order-three D0 has spectrum1,omega²,omega²,omega² and nonreal trace1+3omega². An antilinear intertwiner B obeys go B=B conjugate(go). D0 forces every matrix entry exceptB00 to zero; F0 killsB00. The exact antilinear commutant is zero.

Allowing projective scalar phases does not help: an intertwining phase alpha for D0 would satisfy alpha³=alpha⁴=1 by its order and determinant, hence alpha=1, contradicted by the nonreal trace. Thus there is no unbroken native-group-invariant quaternionicJ withJ²=-1 on thisC4. Even dimension alone is insufficient.

The classical Euclidean CP3→S4 twistor fibration requires a chosen quaternionic real structure; see [Woit's twistor notes](https://www.math.columbia.edu/~woit/twistorp1.pdf). A symmetry-breaking Sp2 structure remains possible, and Lorentzian twistors require a different reality condition. This is not a no-go for spacetime or twistor gravity in general. It specifies the extra structure that the current native group does not select.

## Reproduction and remaining physical obligations

Run the dedicated pytest file against the frozen JSON, run the producer, then test again. The workflow uses the exact science commit and preserves frozen-before-replay ordering. Independent tree-potential differences and direct38x38 resolvent differentiation check the complete action Hessian, with Richardson checks on its soft directions; Todd and Cech counts check both kinetic indices; projector controls check neutral reference transitions; a second basis tests metric-invariant singular values.

The most actionable missing object is a microscopic localization/mediator mechanism that simultaneously selects one exceptional kinetic triplet and transmits the native dynamical sextet to anomaly-consistent E6 matter. A separate gravitational kinetic/action constraint system and a radiatively stable absolute vacuum-energy mechanism are still needed. Placing the finite constructions in one report does not establish a single complete physical theory.
