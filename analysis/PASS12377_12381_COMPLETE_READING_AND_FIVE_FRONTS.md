# Passes 12377–12381: complete-paper intake and five-front continuation

The paper's full 211-page text has now been read, pinned at commit
`80c85d680cd38edddb8e4d12dabebcdbadfdc9ec`, SHA256
`5a041d4d047932ab2b377fa7f12d2dcbebf2d4297a97d52bea9eb67ab8594f26`.
This includes the entire claim ledger, glossary and references. The reading
ledger records every extracted page hash. Forty-seven previously read pages
were checked for normalized-text equality; the other 164 pages were read in
this session. This is complete **text** coverage, not a claim to have visually
inspected every figure or to have finished every historical two-week diff.

The last published science head was `1477a2f`; the following formula-universe
refresh `80c85d6` was inspected. Reservation `d4d4cf4` claims 12377–12381 and
avoids the other track's 12369–12376 reservation. No claim below completes a
theory of everything.

## Results and remaining boundaries

| Front | Executed result | What remains open |
|---|---|---|
| 12377: paper and flavour audit | General-CM counterexample independently verified with eta products, half-integer products and Jacobi theta; three stale TeX statements corrected | Full physical flavour model, lepton fit, vacuum stabilization |
| 12378: torsion | Exact integer cyclotomic screening of 2,093,416 characters on 13 grids | The full 464 necessary-order list, especially mixed-prime orders |
| 12379: native dispersion | Full 135-link Hessians, quotienting only actual gauge gradients; repair lifts the supplied order-three zero | Uniform energetic bound, metric-matched full dispersion, dynamically selected action |
| 12380: native matter | Free finite-temperature 432-site determinant, specified charge multiplets and onsite splitting; independent real-space verification | Interacting/chiral determinant and dynamical masses |
| 12381: Hamming and string controls | Exact native rank-nine intertwiner into 30 Hamming frames; known 10D string character block passes exact S and T tests | Faithful quantum H27 bridge and a new complete 4D worldsheet construction |

## 12377: repair a stale universal CM assertion

On the marked home `tau=1+i*sqrt(3)/2`, the primitive polynomial is
`4*tau^2-8*tau+7`, discriminant -48, so this is exactly CM. With

`f(tau)=exp(-pi*i/24)*eta((tau+1)/2)/eta(tau)`,

the symmetric leading texture ratio is

`|f(tau)|^16/4 = 0.513447581898477106805006318932068539610996815704846... < 1`.

Square and hexagonal controls give 4 and `2^(2/3)` respectively. This result
is **already owned by Pass12046**, whose source explicitly corrects the CM
over-read. The present contribution detects that the correction did not reach
the next paragraph of PDF page128 or the ledger's 11938/11939 rows. Those three
sites now say *tested elliptic CM homes*, not all CM homes. The later lepton
and parity exclusions are not rescinded. A ratio below one alone does not
construct a viable inverted-ordering flavour model. Weber quantities also
refer to the supplied marking; do not silently quotient all modular images.

Sources checked: `analysis/w33_pass12046_geometric_row_closure.py`, the complete
paper, its TeX sources, and the Magma modular-function documentation
<https://docs.magma-maths.org/BasicRings/RealAndComplexFields/elliptic-modular.html>.

## 12378: exact finite torsion grids

The native exceptional polynomial is `Q(h)=1/2*(h-1)^T*N*(h-1)`, with the
same integer N as Pass12346. Because the period matrix W is unimodular, h
characters and original z characters are in bijection at every finite order.
For each grid the producer expands each monomial in powers of a primitive
n-th root and takes **integer polynomial remainders modulo Phi_n**. No
floating tolerance enters a zero decision.

Tested n: `2,3,4,5,7,8,9,11,13,16,25,27,32`. Each grid has only the identity
unless divisible by three; n=3,9,27 have the identity plus exactly ten
order-three characters. Thus exact orders 2,4,5,7,8,9,11,13,16,25,27,32 do
not occur in these grids. This reinforces the earlier Pass12341–12345 census
through64; it is not a new discovery of the ten roots. It **does not** exclude
points of mixed orders such as 15,21 or35 by excluding their prime components.
The 464-order bound of Pass12346 remains a bound, not a classification.

## 12379: actual link dispersion

Inputs are the literal 105 face boundaries, six 16-step commutators and
135 integral edge voltages from the stored certificates. The model uses unit
short-face weights, mixed-loop coefficient matrix R from the six-term repair,
and an identity electric link metric. These are supplied couplings; this run
does not substitute them for another metric-matched model.

For momentum k form the actual 135-by27 gauge gradient D, choose an orthonormal
basis T of `ker(D^dagger)`, and diagonalize `(A*T)^dagger*(A*T)`.
The repaired rows are the mixed rows plus
`sqrt(.001*w(k))*L[[0,5]]`, where `w=sum(mu=0..2)|exp(i*k_mu)-1|^2`.

At `k=(2*pi/3,2*pi/3,0,0)`:

| Operator | Smallest physical eigenvalue |
|---|---:|
| Unweighted three mixed loops | numerical zero (-7.3e-15) |
| Six-term repair, epsilon=.001 | 0.0011837233362156094 |
| Unweighted six separate loops | 0.008547472992197568 |

Gauge Ward residuals are below 2e-15 here. All sampled repaired nonidentity
points have no physical null; the identity retains its four global holonomies.
The smallest repaired-minus-original eigenvalue along `t*(1,2,-1,1)` scales
approximately by16 on halving t (1.73e-8,1.12e-9,7.02e-11,4.40e-12), consistent
with the already proved fourth-order correction. These are full-link spectra,
not the reduced four-mode Rayleigh estimate `49/39000` from the old witness;
those numbers answer different questions and need not agree.

## 12380: independently checked finite-cover matter response

Use spinless number-conserving fermions on the native `2^4`-cell cover:
432 sites, hopping magnitude1, beta2 and chemical potential .3. The six
independent charge multiplets are `(dimension,q_chi,q_psi)`:

`(10,1,1),(5,-3,1),(1,5,1),(5,-2,-2),(5,2,-2),(1,0,4)`.

The linear and all four cubic Abelian charge moments vanish. This is the
known complete E6-branch charge inventory, not a constructed 4D Weyl theory.
For equal spectra the quadratic charge traces are120,72 and0. Put onsite
energy .7 on the dimension-10 multiplet only; its effective chemical potential
is -.4. If K0 and K1 are the corresponding scalar static link kernels, then

`Pi_chichi=120*K0+10*(K1-K0)`,
`Pi_psipsi=72*K0+10*(K1-K0)`,
`Pi_chipsi=10*(K1-K0)`.

On the normalized first native commutator probe:

| Momentum bits | chi/psi response ratio |
|---|---:|
| (1,0,0,0) | 1.680026336333125 |
| (0,0,1,0) | 1.4078803492983283 |
| (1,1,0,0) | 1.4916968757053977 |

Ward residuals are below3.1e-16. An independent real-space 432-by432 Peierls
Hamiltonian and grand-potential finite difference agrees with the analytic
Bloch kernel to6.8e-9 at step .003 and4.3e-9 at step .0015. The scalar static
kernel is indefinite; its lowest eigenvalue is about -.14. These ratios are
responses in a supplied finite model, not positive gauge couplings or a
prediction of a physical mixing angle. The explicit mass splitting is an
input. Earlier unpublished free-response sources were lost in the workspace
reset; this packet restores and independently verifies them. It does not
replace the earlier interacting two-particle Hubbard response of Pass12344.

## 12381: an actual intertwiner, with an exact obstruction

Reuse the 30 Hamming codes and the 15-by15 rational incidence transform of
`w33_20261029_klein_e8_hamming_twistor_transform.py`. On the eight coordinates,
take disjoint cycles `(012)` and `(345)`. Their commuting action on the30 code
frames has orbit sizes `9,9,3,3,3,3`; the two 15-frame rulings and their
incidence transform are equivariant under this `C3^2` action.

For native H27, with multiplication
`(a,b,c)*(A,B,C)=(a+A,b+B,c+C-b*A)` modulo3, define an integer map J from its
27-dimensional regular address module into a chosen nine-frame orbit by
`J*e_(a,b,c)=P^a*Q^b*e_frame`. The stored 30-by27 matrix is checked against
all27 basis vectors for X,Y,Z. It has exact rank9. Dividing by3 corresponds
to averaging the centre before embedding the quotient regular module.

This rank is maximal **for this action**: the target's centre acts trivially,
so every intertwiner kills the18-dimensional nontrivial-central subspace of
the source. The quotient source is the regular `C3^2` module; the target
contains two regular nine-orbits plus four three-orbits. Consequently the
complex Hom space has dimension30, and rank9 is attainable, as J demonstrates.

No faithful native H27 action can arise through eight-coordinate permutations:
`v3(8!)=2`, hence the image of the order27 group has order at most9; all such
images are abelian and kill the commutator centre. This is not an obstruction
to projective or more general unitary quantum representations. In particular,
the address H27 and operator H27 must still be distinguished.

The rediscovery guard flagged a broad E6/hexagonal compound. The entire
`analysis/BT7163_BT7170_e8_hexagonal_lift.md` was read: its root-fibration,
binary-code and D4 results are prior art and are not claimed here. Searches
included the global result index, vocabulary and docs HTML. No exhaustive
novelty claim across every file in the repository is made.

## String continuation: executable modular closure control, not a new vacuum

In character order O,V,S,C, the known ten-dimensional SO(16)xSO(16) parent has

`V8*(OO+SS)-S8*(OS+SO)+O8*(VC+CV)-C8*(VV+CC)`.

The producer stores its full 4-by16 signed coefficient matrix A and checks
`S8*A*(S16 tensor S16)^T=A` exactly over the rationals. All eight nonzero
terms also pass exact T-phase congruences modulo24. Dropping a sector fails S;
changing one T weight fails level matching. Common noncompact bosonic factors
are suppressed. This is an executable known parent character block, **not a
complete new 4D partition function** and not an escape from Pass12363–12368.

A primary-paper search independently identified a different construction:
Faraggi–Matyas–Percival, <https://arxiv.org/abs/2011.04113>, classifies
non-SUSY Z2xZ2 Pati–Salam models, including tachyon-free three-generation
examples with equal massless boson/fermion counts, and examines their one-loop
partition functions. Its abstract also excludes one heavy-Higgs-deficient
class. That is a concrete external lead beyond the99-model Z6-II sample;
no W33 embedding, complete vacuum or compatible Higgs sector was verified here.

## Reproduction and validation

From the repo root:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python analysis/w33_pass12377_12381_continuation.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -m pytest -q tests/test_pass12377_12381_continuation.py
```

Dependencies: numpy, sympy, mpmath, pytest. Five independent tests pass,
including a Jacobi-theta evaluation, transverse basis change, exact symbolic
root substitution, exact rational intertwiner rank and a modular negative
control. The producer additionally runs the independent real-space determinant
check and exhaustive integer torsion decisions. Producer/certificate hashes
are stored. A scoped index is generated without replacing the full global
index from a partial checkout. Manual workflow decisions and the complete
reading ledger accompany this packet.

## Five independent next investigations

1. Finish the exact mixed-prime torsion classification using sparse cyclotomic
   relations or certified algebraic elimination, not a larger floating grid.
2. Quantify full-link dispersion for the **metric-matched** positive couplings
   and optimize the weakest finite-momentum stiffness under a fixed budget.
3. Replace the supplied spinless mass split by an explicit chiral, anomaly-free
   interacting inventory and test its full frequency-dependent Ward identity.
4. Build and audit one concrete S-class Z2xZ2 worldsheet model from the external
   construction, including all sectors, Higgs breaking and massive towers.
5. Seek a central-character-preserving **quantum** H27 action on the Hamming/E8
   frames; the coordinate-permutation route cannot supply it faithfully.

## Corrected PDF build receipt

The corrected PDF was built with three XeLaTeX passes using the original TeX Gyre font specifications. Pagination stabilizes at215 pages (the read input snapshot had211). Corrected passages are present in extracted output; rendered pages128 and194 were inspected. Final log has no undefined-reference or missing-character warning; pre-existing overfull-box warnings remain. This is a targeted correction and layout check, not a complete visual audit of215 pages. See `data/w33_pass12377_paper_build_receipt.json` for source, input and output hashes.
