# Passes11631–11635: five explicit physical interfaces

Reservation:420ab9140. These execute the five requested investigations. They
supply operations, maps, a numerical quantum Hessian and a conditional gravity
architecture. They do not derive all interactions from W33 or solve the TOE.

## 11631 — the instrument now has an explicit interaction schedule

Pass11630 owns the Reye/Witting filter, polar unitary U, magic preparation and
Steane decoder. Here ancilla a is prepared in |0>, with system qubits1,2 in
|++>. Put S=Y1, Pminus=(1-S)/2, r=2-sqrt3 and theta=acos(sqrt(r)). The pulse

    Hfilter = (theta/2) Ya - (theta/2) Ya Y1

has success block D=Pplus+sqrt(r)Pminus and failure block
E=sqrt(1-r)Pminus. Apply the numerical principal-log Hamiltonian
Hpolar=i log U on the two system qubits. Its complete16-term Pauli expansion
is certified, and contains only one- and two-body terms. The resulting
success block is UD=K, exactly the previous filter; the failure output is
**UE**, rather than the previous E, with the same effect E†E. Measure ancilla
Z and retain0, then system qubit1 in X and retain+.

The output is (-1,2)/sqrt5 with total success5(3-sqrt3)/12. Nine actual
conditional density-matrix trials combine pulse-angle errors{-0.02,0,0.02}
with ancilla bit errors{0,0.01,0.05}; their output x/z magic margin remains
positive. These trials are examples, not a universal noise threshold.

A norm bound is independent of those examples. If the coherent pre-readout
unitary has operator-norm error epsilon, the normalized successful pure-state
trace-norm error is at most4epsilon/sqrt(p_total). Therefore

    |bx|+|bz| >= 7/5 - 4sqrt2 epsilon/sqrt(p_total)

and epsilon<sqrt(p_total)/(10sqrt2) suffices with perfect projectors. Duhamel
bounds this error by the sum of integrated Hamiltonian-norm pulse errors.
The bound follows by normalizing the two subnormalized output vectors;
their vector distance is at most2epsilon/sqrt(p_total).

This is a supplied spin-control implementation. It is not a derivation of
native W33 interactions, a photonic device, a correlated-noise threshold or
a fault-tolerant output rate. The polar coefficients are numerical; the
filter algebra and ideal probabilities are exact. The prior distillation
result uses perfect stabilizer control and IID post-preparation output noise
[Reichardt](https://arxiv.org/abs/quant-ph/0411036).

## 11632 — incidence CP breaking now enters a physical flavor invariant

The previous joint Reye/Hesse inventory is retained. The complete5184
(config,Higgs-ray) pairs have unitary little-group orders1(4752pairs) or
3(432pairs). On a free selected pair, the unitary orbit has216 elements;
its CP partner is disjoint, giving432 assigned states. This matters: a
nontrivial common residual family unitary block-diagonalizes both Hermitian
mass matrices and forces the three-family Jarlskog invariant to vanish
when its eigenspaces split2+1 or1+1+1. An incidence-only CP order parameter
does not automatically become quark CP violation.

Choose symmetric seed Yukawas

    Yu = diag(1,2,4)
    Yd = [[2,1,i epsilon],[1,3,1],[i epsilon,1,4]].

For Hq=Yq†Yq the exact invariant is

    Tr([Hu,Hd]^3)/i = 6480 epsilon(epsilon^2+34).

It reverses under CP and vanishes at epsilon=0. At epsilon=1 both spectra
are positive and nondegenerate and |J|=0.0310476517026. The independent test
checks |Tr([Hu,Hd]^3)/i|=6|J product(up gaps) product(down gaps)| and family
rephasing invariance; no measured CKM fit is asserted.

The map is explicitly Hq(g.s)=G Hq(seed)G†, extended by complex conjugation
to the disjoint CP orbit. Projective phases cancel. All generator covariance
and CP identities are checked. Thus the incidence order parameter enters a
physical mass-squared/CP map, rather than a numerical resemblance. The seed
coefficients, epsilon, Higgs identification and scales are supplied. A
continuous parent-symmetric UV operator and potential selecting this orbit
are still missing; the other4752 sectors are not assigned invented Yukawas.
Per decision75c1b501-b7a4-4c79-907f-cd02867f8b31, the earlier retained-doublet
W=0 and missing sigma-dependent Yukawa boundary remains true for that older
model; this construction supplements it on a specified different orbit.

## 11633 — an exact compatible D4/E8/Witting quotient

The earlier selected D4 and the Eisenstein Coxeter quotient are individually
valid. Their direct combination has restricted N=Eᵀ(2omega+I)E of rank2,
where E selects the last four real coordinates. Its slant cosines are0,1;
the24 selected roots collapse to10 complex rays. It cannot realize the
invertible constant-slant1/sqrt3 map required here.

The certificate names an18-reflection Weyl word W. For omega'=W omega Wᵀ,
the new restricted N obeys N²=-I4. Set J=(2omega'+I)/sqrt3. An explicit
signed real permutation O and the **inverse-adjoint cell map**
Lminus=sqrt(2/3)(L0†)^-1 give

    P = Lminus O [I, iI] [E, JE]^-1,
    P J = i P.

All240 doubled E8 roots are matched to exactly one canonical Witting ray
by exact minors, with exact distinctness of the40 targets. Each fiber
contains6 roots and conjugated C^5 preserves the fibers. The selected D4
maps to12 distinct rays. Floating overlaps only suggest candidates; they
are never accepted without exact verification.

This closes a named compatibility problem by changing the chosen complex
structure. It does not make the choice physically canonical or transport
all real Peres orthogonal contexts. Prior owners:
`w33_e8_eisenstein_witting_weld.py`,
`w33_pass8909_8916_e7_e8_d4_reye_latin_selector.py`, and Pass11630's distinction
between primary and inverse-adjoint Reye cells.

## 11634 — the entire264-dimensional quantum normal Hessian

This extends the **declared** Pass11625 finite-cutoff Landau-background shell:
297 real scalars,45 vectors with factor3, c=g²=0.001, k=0.1, UV=0.5,
no fermions. Its old3-real stationary slice is used unchanged. The full
canonical297-coordinate gradient and Hessian are computed by automatic
differentiation using a custom spectral Frechet rule:

    DF(H)[E] = Tr(f1(H) E),
    Df1(H)[E] = Q (L .* (Qᵀ E Q)) Qᵀ,
    Lij = -sum_x wx/[(x+lambda_i)(x+lambda_j)].

This exact divided-difference identity remains valid at repeated masses;
no unstable eigenvector derivatives are used. The identity is evaluated
in float64, not as an interval proof. Canonical fields and scalar Hessian
match the previous numpy action before derivatives are accepted.

Final64-node quadrature results:

- Full gradient norm:7.54345e-11.
- Gauge tangent rank:33; norm(H G)=3.13376e-10.
- Orthogonal normal dimension:264.
- Minimum normal curvature:0.00161314946807765; all264 are positive.
- Minimum shell scalar denominator:0.00960900168347.
- Independent32/64 full-Hessian operator-norm difference:5.14417e-16.
- Four random full-space directional curvature controls agree with central
  differences at decreasing steps; their vectors and results are stored.

The Ward control caught a transposed tangent map during development. That
incorrect projection was discarded before publication. The accepted frame
is independently reconstructed in the tests. Positivity concerns this
supplied finite one-loop scheme only: fermions, infrared continuation,
gauge-independent physical poles, global vacuum selection, interval
certification and observed masses remain open.

## 11635 — native-edge gravity branches and exact ensemble consequences

BT547 already owns tau=2^83*5^23 and uniform tree edge inclusion79/160.
Pass11323 already exhibits the native160-edge cyclic metric extension's
nonlinear lapse Hessian of rank78 and proves no invariant79-edge tree
under an edge-transitive symplectic subgroup. Pass11386 supplies an
extra81st metric hub. None of those results is superseded or called new.

Here a conserved register T labels native spanning trees, with a uniform
measure. Each branch has80 supplied continuum metrics,79 native pairwise
Hassan–Rosen interactions and separately coupled matter. Graph
symmetries permute the register, so the ensemble is invariant even though
one tree is not. On regular branches with nondegenerate positive mass
couplings, the imported tree constraint theorem gives one massless and
79 massive spin-two fields, conditionally2+79*5=397 polarizations.
The action and a connected tree witness are named in the JSON. These are
continuum fields supplied to the native graph, not emerging spacetime.
See [bimetric constraints](https://arxiv.org/abs/1109.3515),
[cycle obstruction](https://arxiv.org/abs/1410.7774), and the current
[regular multivielbein analysis](https://arxiv.org/html/2604.07625v1).

The rational cut projector K is certified by integer identities
Knum²=160Knum, B Knum=160B and trace(Knum)=79*160. Uniform-tree indicators
satisfy Cov(Ie,If)=-Kef² for distinct edges. Adjacent edges give

    Cov = -729/25600,
    Var(deg_T(v)) = 1053/1600,
    Pr(e,f in T) = 689/3200.

Independent weighted Laplacian cofactors verify the two-edge partition
polynomial. Critically,

    -log E_T exp(-sum_e Ie Oe)
      = (79/160) sum_e Oe - (1/2) sum_ef Cov(Ie,If) Oe Of + ... .

When Oe starts quadratically, the covariance term starts at fourth order.
Averaging branch actions drops it and has no inherited ghost-free theorem.
A branch-changing register requires its own constraint/dynamics proof.

Nor does the ensemble remove a common vacuum-energy shift C. Between
unequal four-volumes V1,V2 its relative odds change by exp[-C(V1-V2)].
The finite flux control with rho=-7/10 and charge1/5 has a smallest positive
energy1/50 at |m|=6, but the next downhill state |m|=5 has energy-1/5.
The explicitly built nearest-neighbor detailed-balance generator has its
unique supplied Gibbs distribution; the positive state is not absorbing.
Thus no small-positive-vacuum selection follows without additional physics.
[Dynamical sequestering](https://arxiv.org/abs/1903.02829) supplies extra
global variables/flux equations; it is not contained in our tree measure.

## Reproducers and validation

- `analysis/w33_pass11634_full_quantum_normals.py 64 32` regenerates the full
  numerical certificate and independent quadrature control.
- `analysis/w33_pass11631_11635_physical_interfaces.py` then checks the bound
  certificate and regenerates all five interfaces.
- `tests/test_w33_pass11631_11635_physical_interfaces.py` independently checks
  physical invariants, all-root dictionary and deliberate corruptions.
- `.github/workflows/pass11631-11635-physical-interfaces.yml` pins the numerical
  toolchain and replays both producers before all focused tests.

Result-value searches covered RESULTS_INDEX, prior analysis scripts/reports,
ignored data certificates, docs and the manuscript. The instrument, old
finite sectors/tree shell, D4 selection, E8 quotient, tree complexity and
cycle/hub controls are credited directly. New scope is the named interaction
schedule, covariant physical CP map, compatible exact quotient, full quantum
normal calculation and conditional native-tree ensemble/cumulant interface.

### Advisory combination-token audit

The guard also retrieved broader prior bridges. Their ownership is retained:
`analysis/BT1601_BT1603_physical_fano_universal_closure.md`,
`analysis/BT1602_fano_witting_detector_bin_synthesis.md`,
`analysis/BT1697_holonet_typed_packet_abi.md`, and
`analysis/BT1893_BT1895_summary.md` own earlier D4/Witting runtime and
interface architecture;
`analysis/BT1707_BT1709_qubit_contextuality_hesse_bridge.md`,
`analysis/BT1741_BT1744_execution_summary.md`,
`analysis/BT1745_BT1748_execution_summary.md`, and
`analysis/BT1745_June24_25_commit_audit.md` own the earlier Hesse crossover,
E8 root-hexagon allocation and channel weld. The originating quotient itself
is credited above.

`PASS1030_EIGHTY_CARRIER_ORIENTATION_OBSTRUCTION.md` rules out equating the
transitive E8 eighty-carrier with the Levi point/line union; our gravity
register does not make that identification.
`analysis/PASS11070_11075_ORIENTED_CHAMBER_LOCAL_E8_NERVE.md` already freezes
the81-cycle chart-overlap topology.
`analysis/BT4049_BT4056_five_front_outside_box.md` already reduces a supplied
Witting state to(-1,2)/sqrt5 and builds ideal pulse/free-field interfaces;
that reduction is not new here. `W33_FOR_EVERYONE.tex` is broader background
on Reye/Witting and tree gravity, not a source of the present regular-tree
constraint or vacuum-selection proof. Its matching sections were checked;
this packet does not amend its historical physical interpretations.

The scope asserted here is each explicitly named extension, not novelty of
these combinations of topic words.

The final report also retrieved the `hesse+levi` advisory token. Prior
`PASS1087_1091_FIVE_STREAM_RELEASE.md` owns dual-Hesse hyperplanes and
Steinberg parity; `analysis/BT1720_BT1723_repo_mining_execution.md` owns
Hesse/Fano chart-count bridges; and
`analysis/PASS10949_FREUDENTHAL_QUASICONFORMAL_CLOCK_CONE.md` owns the exact
Freudenthal cone and clock-real-form Lorentzian Peirce slice. These reports
were read in entirety. No such result is rederived or attributed to this packet.
