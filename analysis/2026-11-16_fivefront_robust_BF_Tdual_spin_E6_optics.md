# Five-front TOE deep follow-up: robust KK BF no-go, T-dual K-theory, spin/charge arithmetic, E6 dynamics, optical loss

**Date:** November 16, 2026. Starting local/GitHub `master=25aeb092699a949174ec712c485f079c4a6daa2f`. Five self-contained producer scripts, JSON certificates and targeted regression suite. Pre-existing uncommitted changes belong to parallel authors and were not staged.

**Evidence grading:** The algebra and finite-group orbits are verified. Stability claims apply to explicitly specified classical 11D fluctuation sectors. Full M-theory eight-derivative action, unequal-flux KK diagonalization, complete spinor/winding spectrum, a Standard-Model vacuum and optical hardware data remain OUTSTANDING.

## 1. The decisive BF mode has an order-one gap even as all 11D radii grow

Read source `analysis/2026-11-16_D9_mtheory_uplift.md`, particularly the physical **sphere-exchange-odd** scalar/transverse-Maxwell quadratic action. For equal periods `N0=N1=N2=N>0` on the square torus, the quantization equations give `lambda1=3pi`, so

`m_-² L² = 3pi-2-sqrt(4+48pi) = -5.016944081307837...`,

a deficit `delta_KK= sqrt(4+48pi)-3pi-2 = 1.016944081307837...` below the AdS5 BF limit -4. It is a **physical nonzero KK momentum sector**, not the homogeneous scalar. At these fixed period ratios, `(L/lp)^3=(9pi/2)N` and all round-sphere and fixed-shape torus radii grow as `N^(1/3)` in Planck units. A hypothetical generic local eight-derivative mass shift `+C(lp/L)^6` would need

`C >= delta_KK*(9pi N/2)^2`,

which grows like N², unlike the prior finite `C≈8993.68` threshold for the tiny near-equal homogeneous gap. No **bounded flux-independent C** can overcome this *equal-flux KK* gap at arbitrarily large N. This is NOT a calculation of the actual M-theory eight-derivative coefficient.

For `(N1,N2,N0)=(N+1,N,N)`, the exact quantization geometry gives

`A_T2/L² = 16pi*(N+1)/[N*k2*sqrt(8eta)]`, `k2=4(2-eta)`,
`eta*(2-eta)^2/[(1-eta)(1+eta)^2] = ((N+1)/N)^2`.

Numerical square-torus first eigenvalues approach 3pi as N grows. The **unequal-flux physical mixing matrix has NOT been diagonalized** here. Nevertheless, assuming the properly constrained physical KK operator varies continuously with eta and the isolated physical mode is not lost to gauge constraints, its order-one equal-flux BF deficit implies it remains unstable in a sufficiently small unequal-flux neighborhood. Thus a large-N near-equal family cannot be adjudicated from its homogeneous BF mass alone. **No explicit threshold N or precise unequal-flux eigenmass is claimed**; the code labels the equal-formula numerical proxy as such.

Producer: `analysis/toe_20261116_robust_torus_BF_nearequal.py`; certificate `data/toe_20261116_robust_torus_BF_nearequal.json`.

### Stronger new theorem: a SHARP BF mass-gap deficit uniformly across all flat torus shapes

The now-tracked parallel report `analysis/2026-11-16_winding_modular_statistics.md` correctly observes that in a modular cusp the *shortest* momentum eigenvalue tends to zero while **higher multiples** approach the optimal BF depth. Combining this with the sharp covolume-one lattice bound `Q_shortest<=2/sqrt(3)` yields a novel extremal theorem for the specific equal-flux ratio `N0/N=1`, rather than only an average over moduli.

Define `lambda_v = 3pi Q_tau(v)` and `delta(lambda)=sqrt(4+16lambda)-lambda-2` when `0<lambda<12`. Let `L=2pi sqrt(3)=10.8827961854...`. Every flat torus has `0<lambda1<=L`. If `lambda1>=1`, choose the shortest primitive vector; its eigenvalue lies in `[1,L]`. If `lambda1<1`, choose the integer multiple `j=ceil(1/sqrt(lambda1))` of that vector; then `1<=j²lambda1<(1+sqrt(lambda1))²<4<L`. Thus **all shapes have at least one mode with `1<=lambda<=L`**.

The function `delta` increases to its unique maximum at `lambda=15/4` and decreases thereafter. Its minimum on `[1,L]` is `delta(L)=sqrt(4+32pi sqrt(3))-2pi sqrt(3)-2=0.463541850418787...`, smaller than `delta(1)=sqrt(20)-3`. Consequently

`for every tau: max_{v!=0}[-4-m_-²(lambda_v)] >= delta(L) >0.`

**Sharpness:** At the hexagonal lattice `tau=1/2+i sqrt(3)/2`, `Q` is proportional to the Eisenstein norm `a²+ab+b²`, which takes values 1,3,4,..., never 2 (mod 3 it is a square). The next shell has `lambda>=3L>12`. Hence exactly six signed shortest labels enter the BF band, all at `lambda=L`, attaining the sharp worst-case depth `delta(L)`. Thus **no flat torus shape at N0=N1=N2 can even approach zero deepest BF deficit in the two-derivative theory**.

The theorem concerns a physical constrained scalar-Maxwell sector of the exact equal-flux solution. It does not assert uniform smallness of quantum corrections at a modular cusp, where one torus radius may shrink to the Planck scale when tau depends on N. Fixed finite shapes become large in Planck units as N grows; the sharp bound is purely classical.

Producer: `analysis/toe_20261116_uniform_KK_BF_shape_gap.py`; certificate `data/toe_20261116_uniform_KK_BF_shape_gap.json`; dedicated regression `tests/test_toe_20261116_uniform_KK_shape_gap.py`.

## 2. New exact twisted-K extension resolution using a topological T-dual

Let `Y(p,q)` be a nontrivial circle bundle over `S²xS²`; put `g=gcd(|p|,|q|)`, `a=p/g,b=q/g`. The free `z in H³(Y;Z)` has pushforward `pi_*z=a x-b y`. For optional integral NS twist `H=k z`, topological T-duality exchanges circle curvature and fiber-integrated H:

`c1(Yhat)= k(a x-b y)`, `Hhat=g zhat`, `pi_hat*zhat=a x+b y`.

The consistency cup relation `c1(Y) cup c1(Yhat)=0` follows from the off-diagonal intersection form on `S²xS²`. Twisted K-theory shifts parity under circle T-duality.

**New proved subfamily:** For `|k|=1`, `c1(Yhat)` is primitive, so `Yhat ≅ S²xS³`. Twisted Kunneth gives `K_Hhat^0(Yhat)=0` and `K_Hhat^1(Yhat)=Z_g⊕Z_g` (with `Z_1=0`). Therefore

`K_H^0(Y(p,q)) = Z_g⊕Z_g`,  `K_H^1(Y(p,q))=0`

for *all* nonzero p,q with primitive H. This **resolves the prior nonprimitive additive extension ambiguity** at unit twist, without simply selecting the split extension by assumption. Also resolve arbitrary nonzero k when p or q is zero, since Y=L(g,1)×S²; and arbitrary k with g=1 by Y=S²×S³.

**Remaining gap:** For g>1, |k|>1, and a*b≠0, the E-infinity filtrations only fix orders g²,k²; their group extensions remain unresolved in this work.

**Physical boundary:** The source-free IIB conifold solution in the repo has `H3=0`. These nonzero-twist spaces are *nearby mathematical models*, not the physical vacuum's Page or differential K charge spectrum. Full Freed-Witten, F5 and brane-endpoint analysis is absent.

Producer: `analysis/toe_20261116_twisted_K_Tduality_resolutions.py`; certificate `data/toe_20261116_twisted_K_Tduality_resolutions.json`. References: Bouwknegt–Evslin–Mathai, DOI 10.1103/PhysRevLett.92.181601; Mathai–Rosenberg, DOI 10.1007/s00220-004-1159-7.

## 3. Genuine global spinor/winding distinction plus a new SL(2,Z) orbit invariant

For equal quotient `T^{1,1}/Z_N`, existing local cover spinor Fourier labels `k=±1` obey the deck phase `exp(2pi i k/N)`. The ordinary lift retains residue k=0 modN, the alternative lift (for even N) residue k=N/2 modN. Thus the *cover* Killing spinor descends for N=1 (ordinary) or N=2 (alternative), not N>2. This reproduces previous work rather than inventing a supersymmetric 11D vacuum.

More interesting: the fiber loop generates `H1(Y;Z)=Z_g`. Formally tensoring the IIB F1/D1 **species** charge lattice `Z²` with the torsion fiber `Z_g` yields a candidate module `(Z_g)^2`, carrying the natural modular SL(2,Z) action on species. **New exact orbit classification:** the SL(2,Z) orbits in `(Z_g)^2` are labelled by `d=gcd(g,m,n)`, with size the Jordan totient `J2(g/d)`. At g=6 the four orbit cardinalities are **24,8,3,1**. Enumeration using modular S and T matrices agrees for g=1,2,3,4,5,6,8,9,12.

This finite species-orbit count must NOT be identified with the infinite 11D momentum spectrum or a proven conserved string charge group: endpoints, flux interactions, and the worldsheet spectrum have not been calculated. It is an arithmetic structure to be tested against any proposed full winding/spinor dictionary, not that dictionary itself. Fixed axiodilaton backgrounds need not have full SL(2,Z) as an internal symmetry; the action is duality covariance across moduli.

Producer: `analysis/toe_20261116_spin_winding_SL2_orbits.py`; certificate `data/toe_20261116_spin_winding_SL2_orbits.json`.

### Newly exposed discontinuity: near-equal quantized fluxes change global topology

The freshly tracked parallel IIB derivation `analysis/2026-11-16_D9_iib_conifold_dual.md` independently shows `pi1(Y)=Z_g` and a discrete `Z_g x Z_g` M-theory C-field translation subgroup, matching the topological F1/D1 winding-residue labels. Our new result is the cross-family comparison: the equal sequence `(N1,N2)=(N,N)` has `g=N`, torsion complex K0 order `N²`, and fundamental group `Z_N`, whereas the near-equal sequence `(N+1,N)` has `g=1`, torsion-free K0 and simply-connected total space diffeomorphic to `S²xS³`, even as flux *ratios* and local sphere/torus 11D geometry converge. This is a **discontinuity of global topological charges**, not a discontinuity of all propagating excitations. The full 11D physical momentum modes are not deleted merely because their IIB wrapped counterparts cease to carry protected homotopy charge. No equality of full fermionic/winding spectra has been demonstrated.

## 4. E6 dynamics: symmetry breaking, soft radial mass and SUSY supertrace firewall

Existing cubic `W=det A+det B+det C-Tr(ABC)` has the exact F=D-flat locus `A=B=C=s I3`; its singlet Hessian has a complex massless modulus. For equal gauge couplings gYM and canonically normalized SU(3) generators, the three gauge-site fields couple through the graph Laplacian of the triangle (eigenvalues 0,3,3). The gauge sector is:

- **8 massless** SU(3) diagonal gauge bosons;
- **16 massive** gauge bosons of squared mass `3*gYM²*|s|²`.

Residual diagonal SU3 has rank 2, whereas SM SU3×SU2×U1 has rank 4: this branch can never reproduce SM unbroken gauge symmetry.

Test a manifest gauge-invariant *toy* soft EFT with `I=Σ Tr(M_i†M_i)`:
`V_soft=(m²/3) I + κ I³/(729 M²)`.
On the F=D-flat branch `I=9|s|²`, so `V=3m² r²+κ r⁶/M²`. For m²<0, κ>0 its nonzero stationary scale has `r⁴=-m² M²/κ`. The canonically normalized **radial mass²=-4m²**, while the phase remains massless. This explicitly inserts soft scales and does not prove non-singlet stability or explain the SM spectrum.

**Extra one-loop obstruction:** In exact unbroken 4D N=1 SUSY, each of the 16 massive gauge vector multiplets has 3 massive-vector plus 1 real-scalar bosonic degrees of freedom and 4 Dirac-fermion degrees of freedom at the same mass, hence `Str M²=Str M⁴=0` for this multiplet. A Coleman–Weinberg potential formed from gauge-vector loops *alone* is physically incomplete: its apparent radial lifting cancels when superpartners are included. Any legitimate quantum lifting of this moduli branch requires SUSY breaking, nonperturbative effects, or additional dynamical fields and a consistently treated full spectrum.

Producer: `analysis/toe_20261116_E6_soft_gauge_falsifier.py`; certificate `data/toe_20261116_E6_soft_gauge_falsifier.json`.

## 5. Four-MUB qutrit Bell-return test: remove the fair-sampling loophole in planning

The earlier mathematical operator identity `Σ_b P_match(b)=I9+3|Phi3><Phi3|` gives `S=Σ C_b=1+3F_Bell` and the separable bound `S<=2`. Prior shot estimates were for *accepted detected pairs*, and would overstate feasibility if efficiency were not independently certified.

For an **event-ready** experiment where every prespecified heralded attempt is counted, including no-click as mismatch, suppose each recorded click-and-match effect is dominated by the ideal matched-basis projector up to validated per-setting bias `epsilon`. Then `S_true≥S_click−4epsilon` without simply discarding lost trials.

For the isotropic `rho(v)=v Phi3+(1-v)I9/9` and pair-detection probability `eta` independent of basis and outcome *for this planning calculation*, `E[S_click]=eta*4(1+2v)/3`. Thus no-calibration-loss detection is possible using this witness only if
`eta > 3/[2(1+2v)]`.
At v=.75, eta must exceed .60. With eta=.70, alpha=.01, beta=.10, epsilon=.01 per setting, Hoeffding requires **312 gross event-ready trials per basis** (1,248 total); with epsilon=0 it needs 242 per basis. At v=.75 eta=.50, no number of trials is sufficient under this witness/model. Other witnesses may do better.

This is **not device-independent**: a valid setting-calibrated measurement and dominations of click effects by the intended projectors are essential. Losses, dark counts, crosstalk and multipair events must be bounded empirically. The coherent SWAP memory and reference Bell qutrit remain unbuilt; no physical measurements occurred.

Producer: `analysis/toe_20261116_qutrit_eventready_loss_bound.py`; certificate `data/toe_20261116_qutrit_eventready_loss_bound.json`.

## Reproduction and ownership

Run producers individually, then:
`python -m unittest discover -s tests -p test_toe_20261116_fivefront_deep_followup.py -v`.
The tests cross-check the prior BF, AHSS, E6 and four-MUB producers. The five new source files, five deterministic JSON certificates, this markdown report and the one test file are the ONLY intended staged changes. Do not stage other untracked or modified research files.

**Unresolved decisive physics tasks:** derive full unequal-flux coupled 11D momentum operator; compute complete eight-derivative correction on corrected background; solve general nonprimitive twisted K extensions and actual Page charge spectrum; derive fermionic/winding dual operator map; find realistic chiral E6 vacuum; fabricate/characterize an event-ready photonic memory.
