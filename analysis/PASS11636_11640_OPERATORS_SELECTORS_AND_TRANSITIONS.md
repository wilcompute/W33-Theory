# Passes11636–11640: incidence Yukawas, a radiative CP selector, and physical consistency tests

Reservation: `5bf052b08`. Main producer: `analysis/w33_pass11636_11640_operator_selector_transitions.py`. Fermion/infrared producer: `analysis/w33_pass11637_fermion_ir_normals.py`. Certificates have the corresponding names in `data/`; three compressed input/operator archives make the replay independent of ignored local artifacts. Regression: `tests/test_w33_pass11636_11640_operator_selector_transitions.py`.

All five requested targets have concrete computations. The strongest extension is a polynomial, symmetric E6 Yukawa operator from the actual Reye/Hesse incidence, followed by a calculated fermion determinant that can select full-rank CP-breaking sectors. These are supplied EFT constructions, not observed mass predictions or a complete TOE. The forty-points paper's boundary remains: finite geometry alone does not provide physical forces, masses, spacetime dynamics or an absolute vacuum energy.

## Prior ownership and search

The search included `RESULTS_INDEX.md`, `docs/index.html`, `w33_paper.tex`, the current forty-points manuscript, Python/Markdown/TeX sources and certified JSON, and exact result searches after experimentation. In particular:

- 11271 already owns the Pauli-allowed `d_ABC psi_i^A psi_j^B H^{C,ij}` symmetric-family interface. 11361 already converts projector/Bargmann phases into flavor CP; this is not the first projector CP construction.
- 11625–11629 owns the Reye configurations and the joint Hesse alignment model. 11632 owns a free-orbit mass-matrix lookup and the 4752/432 stabilizer census. The new result is a single continuous incidence operator, exact coverage of all sectors, and its conditional radiative selection.
- 7240 already owns the 4480 fixed-point-free order-three E8 structures. 11633 owns the repaired D4/Witting projection. The new result is the full compatibility-energy census and a named quantum selector.
- 11323 owns nonlinear metric-cycle shift elimination; 11363–11364 strengthens its rank/null theorem. The new result is an exact weighted single-cycle tree-transition witness and an explicit forest alternative.
- 11546 already proves the affine fixed-data shift criterion; 11624 distinguishes it from generic nonlinear sequestering. The new result allows geometry and the Planck coefficient to relax in the actual unequal-cap equations.

Per decision `5d60a217-5c1d-45ba-aca8-12d4fbb177e1`, prior11631–11635 keeps supplied coefficients/metrics and the branch-versus-average gravity distinction explicit. Per decision `914f6d35-836c-472a-a18b-f8074416621d`, the existing fixed-flux test is conditional and leaves physical matching and observed vacuum energy open. Both were checked against the current certificates rather than treated as fresh discoveries.

Broader D4/Witting and Levi/Witting context already appears in `analysis/BT1601_BT1603_physical_fano_universal_closure.md`, `analysis/BT1602_fano_witting_detector_bin_synthesis.md`, `analysis/BT1697_holonet_typed_packet_abi.md`, `analysis/BT1893_BT1895_summary.md`, `PASS1030_EIGHTY_CARRIER_ORIENTATION_OBSTRUCTION.md`, `W33_FOR_EVERYONE.tex`, `analysis/BT1741_BT1744_execution_summary.md`, and `analysis/BT4049_BT4056_five_front_outside_box.md`. These own earlier runtime allocations, typed interfaces, the point-versus-line orbit obstruction, and ideal Witting magic preparation. The compatibility-energy selector and nonlinear weighted exchange below do not claim the first connection between those objects.

## 11636 — a continuous incidence operator, not a sector lookup

Let `P_i` be the twelve normalized Hesse-ray projectors. For each unordered triple `t`, define `Q_t=sum_{i in t}P_i`. Introduce a real triple-incidence field `sigma_t` and a family triplet `h`. There are220 possible triples; each of the432 prior Reye configurations has sixteen occupied triples. Define

```
Y_a(sigma,h) = sum_t sigma_t conjugate(Q_t^a h) conjugate(Q_t^a h)^T,
a=1,2;     Yu=Y1,     Yd=Y1+epsilon Y2.
```

Both matrices are symmetric. The formula is polynomial in `sigma,h` away from the discrete minima as well. Under the actual finite Clifford generators, `h -> G h` and the triple labels are permuted; `Y -> conjugate(G) Y Gdag`. Thus

```
d_ABC psi_i^A psi_j^B H^C Y_ij
```

is E6 invariant, family invariant, and symmetric in the combined Weyl indices. All78 exact signed-cubic generator contractions vanish; the generators and270 nonzero tensor entries are included in a provenance-bound input archive. Exact projector covariance is checked for all48 generator/ray pairs. Central projective phases cancel between `psi psi` and `hbar hbar`.

If `sigma` is dimensionless, this is a dimension-six operator with coefficient `y/LambdaF²`; with a canonical dimension-one incidence scalar it is dimension seven and uses `y/LambdaF³`. The fixed Hesse projectors are finite-family invariant tensors, not untested adjoint fields of a continuously gauged family SU3. Two supplied27-Higgs channels specify the up/down spurions; their SM interpretation and vacuum selection require additional matching.

At the prior canonical free-sector representative, the exact invariant is

```
Tr([Yu†Yu,Yd†Yd]^3)/i =
-224 sqrt(3) epsilon³
 (40465783590952 epsilon³ + 36055395485682 epsilon²
  + 9913797539901 epsilon + 797029207506)/531441.
```

Conjugating the geometry reverses this CP invariant; changing the real coefficient `epsilon` is a different operation. At `epsilon=1`, the illustrative mixing invariant is `-3.77662236596e-5`. It is not a measured CKM prediction.

The full5184-sector census is **exact**, using symbolic witnesses on all28 unitary joint orbits plus exact generator covariance. Precisely4752 sectors have nonzero CP and trivial projective stabilizer; the432 order-three stabilizer sectors have zero CP. At `epsilon=1`, family rank pairs are `(3,3):3456`, `(2,3):1296`, `(1,1):144`, `(2,2):288`. A nonzero CP invariant does not imply every fermion is massive.

### A separate route: let the actual fermion determinant choose the sector

The same operators give a concrete test of whether dynamics prefers useful flavor. Hold the previously declared aligned flavor sectors fixed and the27-Higgs at the canonical unit vector. For one Weyl81, set

```
M = y d[:,:,0] tensor (Y1+epsilon Y2).
```

The committed cubic satisfies `d0³=d0` and `Tr(d0²)=10`: exactly ten copies of each family singular mass are nonzero. The fermion contribution is therefore the actual81-mode determinant, with two spin degrees per Weyl mode. Massless modes contribute zero to the normalized logarithm rather than being assigned artificial masses.

All28 exact family mass-trace polynomials are stored. At `epsilon=1/100`, the maximal trace is `70228111/202500`, with strict gap `1586/16875` to the other sectors. The two maximizing orbits are CP conjugates, each of size216, and both family matrices have rank three. Their CP invariant is nonzero; one representative gives

```
-6887083628711461021 sqrt(3)/16607531250000000.
```

This selection has an analytic finite-coupling certificate. In the shell `x in[1/100,1/4]`, use

```
0 <= u-log(1+u) <= u²/2   for u>=0,  and log25<4.
```

If `delta` is the leading trace gap and `U=Tr[(Yd†Yd)²]` at the winner, then

```
y² < 3 delta/(25 U)
```

makes its upper energy bound smaller than every competing lower bound. Here `U=1939840349756239/16402500000` and the sufficient bound is `184991040/1939840349756239`. The supplied benchmark `y=1/10000` satisfies it. A separate64-node determinant evaluation agrees with the ordering. This proves selection of432 full-rank CP-breaking sectors in this pinned flavor model.

The negative control matters: at `epsilon=1`, the determinant instead selects144 rank-one, CP-zero sectors. The geometry does not decide the coefficient. Merely finding a CP-breaking operator is insufficient; its quantum energy must also be tested.

A useful conditional extension follows for the **flavor functional alone**, with sigma restricted to the432 discrete configurations and the27-Higgs fixed; only u,h are relaxed. Prior11625's positive alignment potential has finitely many projective minima, two phase circles, eight positive normal curvatures, and coercive radial terms. Adding the displayed fermion determinant is analytic in `y²` on compact neighborhoods, with energy `-A y² T+O(y⁴)`. The implicit-function theorem shifts each isolated projective minimum by `O(y²)`; its relaxed energy changes the ordering only at `O(y⁴)`. Coercivity localizes global minima, so the strict trace gap selects the same CP-breaking orbit pair for sufficiently small nonzero `y` at fixed positive finite pin coefficients. Full rank and nonzero CP persist by continuity. This is an existence argument: the explicit bound above belongs to the pinned limit, and is not a computed finite-pin coupling bound or full gauge/scalar quantum vacuum certificate. The27-Higgs and the other gauge/scalar determinants remain outside this flavor stability statement.

## 11637 — add fermions and resolve infrared quadrature

This is a separate declared45/126 Spin(10) EFT. Starting with11634's complete297 canonical scalar coordinates, add three Weyl16 species with the symmetric126 Yukawa mass and two spin degrees each. The finite Landau-background action is

```
.001 Vtree + shell(.001 Hscalar) + 3 shell(.001 Hvector)
             - 6 shell(y² S†S),
shell(H)=integral_{k²}^{.25} x Tr log(1+H/x) dx/(64pi²).
```

A32-dimensional realification doubles each16-dimensional Hermitian fermion eigenvalue, so its implementation coefficient is minus three, exactly equivalent to minus six on the original spectrum. Every case independently relaxes the background before constructing all297 Hessian rows. The33 actual gauge tangents are built from the generators, and all264 physical normals are retained.

| k | y | minimum normal curvature, order64 |
|---|---|---|
| .10 | .03 | .00161518058118 |
| .06 | .03 | .00161026076510 |
| .03 | .03 | .00160927452284 |
| .10 | .30 | .00164422432558 |

Full gradients and gauge Ward residuals pass; every normal is positive. Independent order128 backgrounds/Hessians differ in operator norm by `8.43724e-18` at `k=.1` and `1.94425e-9` at `k=.03`. The original32/64 attempt failed the unchanged `1e-8` convergence requirement and was discarded; increasing quadrature, not relaxing the requirement, resolved it.

The tree scalar Hessian at these relaxed backgrounds has a negative eigenvalue. The finite integral is valid because `k²+minimum_scalar_mass²>0`; naively reducing `k` below the stored boundary near `.019–.020` crosses the real logarithm's domain. The result therefore does not establish `k->0`, pole masses, gauge-independent global stability, interval bounds or higher-loop protection. [Espinosa–Konstandin's hard/soft Goldstone resummation](https://arxiv.org/abs/1712.08068) supplies the relevant method; no uncalculated self-energy shift is inserted here. The earlier complete E6 fermion determinant belongs to a different inventory and its T-saddle result is not inherited by this model.

## 11638 — a constructed quantum selector for compatible complex structure

Enumerate the already-owned4480 Weyl conjugates of the order-three E8 structure using exact integer matrices, with all eight reflection permutations and a stored BFS parent word for every structure. On the selected D4 plane, let `N=(2 omega+I)|D4` and `E=||N²+I||F²`. Its exact census is

```
E=0:2304;  E=10:2048;  E=16:128.
```

The compatible induced reflection graph is connected, with2304 vertices and7920 edges. Its spectral projector is the explicit polynomial

```
P0(E)=(E-10)(E-16)/160.
```

For supplied positive `kappa,t`, define a positive Hamiltonian

```
H = kappa diag(E)
  + t sum_edges P0(E_i)P0(E_j)(|i>-|j>)(<i|-<j|).
```

Its unique zero ground state is the uniform coherent state on all2304 compatible structures. A connected-graph path/Cauchy estimate gives the exact positive gap lower bound `min(10 kappa,2t/2303²)`. It selects the compatible subspace, not one classical orientation. The restricted complex slope is `1/sqrt3<1`, so the D4 plane has no intersection with its complex rotation; its24 roots therefore remain twelve distinct complex rays, as in the11633 target.

Removing the specified kinetic gating is observable: unrestricted reflection hopping applied to that ground state has outside-support leakage norm squared **25/16**. The gating and energy are constructed couplings, not a derived microscopic force or an automatic property of E8.

## 11639 — tree exchange has a nonlinear constraint cost

Use the actual80-vertex160-edge Levi graph. A concrete spanning tree plus a native chord creates an octagon; replacing one octagon edge yields a second spanning tree. Overlap their weights continuously. Exact nonlinear shift elimination gives

```
Ured = min_c sum_e (N_i+N_j) sqrt(w_e²+j_e²),  j=j0+C c,
H_lapse = -g g^T/a   for the single cycle.
```

At the midpoint there is an exact rational stationary current/source witness with `a=2012/125` and a nonzero lapse eigenvalue **-45/503**. The Hessian has rank one, while either fixed-tree endpoint has no cycle variable. Positive overlap tests at `.01,.1,.5,.9,.99` all have rank one. This is a necessary nonlinear constraint test of the named metric-pair model, not a full Dirac count or a claim about distinct multivielbein actions. The [metric-cycle analysis](https://arxiv.org/abs/1410.7774) and [bimetric constraint construction](https://arxiv.org/abs/1109.3515) are imported prior theory.

There is a constructive alternative: remove the old edge before adding the new one. The explicit continuous path remains a forest, but its midpoint has78 edges and two components. Conditional static spin-two counting changes from397 to394 there, with an extra massless sector. More generally, a continuous acyclic-support path between different spanning trees must disconnect: a connected79-edge acyclic support has a locally fixed edge basis until an edge vanishes. Overlap makes a cycle; avoiding overlap changes rank.

Promoting this parameter to a field or adding quantum register hopping still needs an explicit operator preserving the physical constraints, especially at the rank-changing point. Neither branch averaging nor this held-parameter path supplies that missing nonlinear dynamics.

## 11640 — solve geometry's response, not just a fixed-data Ward identity

Continue11302's closed unequal-cap Euclidean membrane model with distinct Maxwell and sequestering forms. Hold chosen fluxes fixed, use `sigma(Lambda)=Lambda+alpha Lambda³`, and `hatsigma(K)=K`. Solve Israel's junction condition, `Volume=Q sigma_prime`, and `averageR=-2 Qhat/(Q sigma_prime)` together. The reference cap volumes are about277.8553 and54.6991.

For `alpha=0`, a common constant threshold `C` gives exactly `d(R,Lambda,K)/dC=(0,-1,0)`, despite the unequal volumes. At `alpha=1`, the computed implicit derivative is approximately `(-.17997783,.05688070,1.25622648)`. A direct finite shift `.03` solves to residual below`1e-9` and changes both geometry and the Planck coefficient. A threshold `.01` on only one cap changes the saddle even on the affine branch.

Exact unequal-volume source subtraction also keeps the field-dependent terms:

```
rho1=C+a x1^4, rho2=C+b x2^4;
rho_i-<rho> is independent of C;
local matter forces remain 4a v1 x1³ and 4b v2 x2³.
```

Constant vacuum cancellation does not remove local radiative physics. This quantifies the existing affine criterion with allowed geometry response; it does not refute generic nonlinear sequestering's approximate radiative stability. [Local sequestering](https://arxiv.org/abs/1505.01492), [sequestered vacuum decay](https://arxiv.org/abs/1604.04000), and the distinct [graviton-loop extension](https://arxiv.org/abs/1606.04958) remain credited mechanisms. This laboratory does not select fluxes, the observed residual CC, a stable Lorentzian cosmology, a bounce determinant or a native W33 spacetime.

## Reproduction and practical limits

Run the fermion producer with `64 128`, then the main producer, then the focused pytest file with `--noconftest`. Committed JSON binds source hashes and compressed archives; tests independently reconstruct the exact orbit coverage, scalar gauge tangents, nonlinear rational witness and cap equations. The dedicated workflow verifies frozen certificates, regenerates both producers and verifies them again.

The five constructions are distinct model interfaces. Combining their coefficients and fields into one shared renormalized action is not established by placing them in one report. The actual new opportunity is conditional radiative full-rank CP selection from incidence-generated operators; the strongest constraints are the finite infrared domain, required complex-selector gating, nonlinear tree-exchange obstruction and unselected vacuum flux data.
