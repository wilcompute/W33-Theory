# Native reflection lift, joint response, compact cycles and a continuous running bound

This continuation investigates each of the five requested directions and adds a
cross-track analytic result. It does not solve a Theory of Everything. The chiral
regulator and complete paper/history reading remain unfinished.

Producer: `analysis/w33_20261027_microscopic_response_and_lifts.py`.
Certificate: `data/w33_20261027_microscopic_response_and_lifts.json`.
Controls: `tests/test_w33_20261027_microscopic_response_and_lifts.py`.

The baseline is science commit `ff6b9f202`, followed by formula-index refresh
`bc28197ea`. GitKraken returned `Transport closed`; local Git was used to fetch
and fast-forward the latter. Other dirty work was excluded.

## 1. An exact reflection of the infinite translated graph

The previous packet supplied a metric reflection on momentum space but no
microscopic lift. We now exhibit one. With

```
F = [-1 0 0 0; 1 1 0 0; -1 0 1 0; 0 0 0 1],
L = F^T,
```

define `(x,v) -> (L x + o_v, p(v))`, with the27-vertex permutation and integer
offsets in the certificate. Search used igraph's51,840 automorphisms of the
native27-vertex/135-edge graph; the committed producer verifies the found map
directly without an igraph dependency or rerunning the search.

For every oriented native edge the exact integer identity is

`signed_V_(p(edge)) = V_edge F + (B o)_edge`.

Also `p^2=1`, `L o_v + o_(p(v))=0`, `F^2=1`, and `F^T M F=M`.
These certify an involution on the **infinite** cover, rather than only a finite
cover or the acoustic metric. Every zero-voltage boundary loop maps to another
zero-voltage boundary loop. In particular the full set of short simple
zero-voltage triangles, squares and pentagons is preserved. No vertex/deck count
identification substitutes for the map.

The selected105-face action fails this symmetry:47 selected faces have images
outside that selected set. More decisively, its completed physical spectra at
`k=(.17,.31,-.23,.41)` and `F k` differ by0.1809435. This failure concerns the
chosen action, not the existence of a graph reflection.

We supply the repair `S_sym=(S+reflection^* S)/2`, using literal image boundaries
and the same positive commutator metric. Positivity, locality with finite loop
support, and gauge invariance are preserved. Reflection invariance follows
algebraically from its involution; two spectral controls have maximum differences
below4e-14. On `k=t(1,2,-1,1)` its three soft squared eigenvalues divided by`t^2`
approach the prior target94/27: at`t=.005` they are
`(3.46818,3.47940,3.48863)`, versus target3.48148148.

**Boundary:** averaging adds microscopic interactions. The radius, compactification,
orbifold boundary conditions and matter projection are not dynamically selected.
The no-native-H27-invariant rank3 projector result of the previous packet still
stands: this reflection does not commute with that group. The paper's Delta54
reflection on *families* (pages107–108) is a different action on a different
carrier; we do not identify it with this spatial reflection.

## 2. Electric and magnetic response from the same microscopic action

On the previous19-site/20-link theta patch, take the supplied spinless fermion
action

`S_f=sum_q mult(q) bar(psi)[d_tau+i q a0+K_q(A)-mu]psi`,

with `(q,mult)=(1,16),(-2,10),(4,1)` and unit hopping. Integrating these free
fermions gives one determinant. Its static Hessian gives the magnetic curvature;
the same hopping's current vertices, diamagnetic vertices and spectral bubble
give the frequency kernel. For energy differences`Delta_ab`, the real symmetric
bubble weight at nonzero Euclidean frequency is

`[f(e_a)-f(e_b)] Delta_ab/(Delta_ab^2+nu^2)`.

At zero frequency the divided difference includes the thermal derivative on
degenerate energies. All vertices and contact terms come from the same K.

An independent finite-time transfer calculation checks the response. Use
`L_t=W_t exp(-dt K_t)`, `Z=det(1+L_(N-1)...L_0)` and temporal links that map
frame`t` to`t+1`. Under independent vertex frames,
`L_t -> G_(t+1) L_t G_t^-1`, so Z is unchanged. A seeded time-dependent
transformation changes log|Z| by at most3.6e-15. Centered determinant variations
at the first Matsubara frequency converge toward the spectral kernel: increasing
time slices24->48 reduces the three directional errors by approximately four;
the largest final error is6.5e-7. This is a covariance and response calculation,
not just a charge-count identity.

### The thermal obstruction and a gapped control

At nonzero temperature the static and dynamic zero-frequency limits differ.
The jump is the positive semidefinite current covariance inside equal-energy
spaces, including diagonal energy entries. At T=1 its eigenvalues are
`(0,1.9419040)` to numerical precision. Thus `(K(nu)-K(0))/nu^2` generally
diverges; calling it a local Maxwell electric coefficient would be wrong. Small
nonzero frequency values are explicitly labeled analytic continuations; thermal
Matsubara frequencies themselves are discrete.

The distinction between equilibrium and isolated dynamic susceptibility is
established linear-response theory, rather than a new general physical effect:
see [Wilcox1968](https://doi.org/10.1103/PhysRev.174.624). Here it is an explicit
diagnostic on this particular native patch and filling.

A supplied zero-temperature chemical potential`mu=.1` lies inside a spectral
gap and eliminates that thermal occupation derivative. It gives positive static
curvature

```
B = [1.56362712 -0.52753370; -0.52753370 1.56362712]
```

and a regular positive dynamic coefficient approaching approximately

```
E = [9.778 -3.403; -3.403 9.778].
```

The zero-temperature three-point frequency refinement tests convergence. This
constructs both responses in a concrete model; it does **not** derive the desired
metric. The equal diagonal constraint on this theta patch remains incompatible
with the target H0 diagonals25/9 and11/3. A finite pair of flux coordinates also
does not define continuum photon propagation. Spin, a chiral spectrum and a
common relativistic limiting speed remain absent.

## 3. All integer cycles of a larger compact patch

Generalizing the actual translated commutator construction gives a three-cycle
patch and the six-cycle patch with43 vertices and48 links. A spanning-tree chord
test gives absolute determinant1 in both cases. Therefore the chosen cycle rows
span the entire **integer** cycle lattice of each patch, not just its real cycle
space or a proper finite-index sublattice.

The Hamiltonian uses integer electric flux`E=m C`, electric energy
`g^2 |E|^2/2` and the previously certified positive27-harmonic compact potential.
Restricting unused flux coordinates to zero gives exactly the corresponding H0
principal Hessian. Gauss's law holds for every retained basis vector.

Three-cycle hard-wall cutoffs2..7 atg=.5 decrease the ground energy from
7.9412998 to7.6890152649; the last change is3.30e-8 and the final boundary
probability is4.0e-10. Atg=1 and2, cutoffs2..5 give the recorded refinement.

For all six cycles atg=1:

| Cutoff | Dimension | Ground energy | First gap | Boundary probability |
| --- | ---: | ---: | ---: | ---: |
| 1 | 729 | 3.6863228209 | 5.9743169930 | 1.82e-3 |
| 2 | 15,625 | 3.6862869910 | 5.9613411914 | 1.01e-6 |

These are Galerkin calculations, with residuals in the certificate. Cutoff
differences and boundary probabilities are diagnostics, not rigorous errors on
the infinite-cutoff answer. The patch's integer cycle space is complete; the
135-edge translated graph and all its matter/gauge modes are not simulated.
There is no phase diagram or confinement conclusion.

Prior ownership: `analysis/w33_20261013_toe62_three_loop_matter.py` already has
three overlapping loops and dynamical fermions on a different14-site Levi patch.
The new calculation extends the Oct27 deck-commutator construction, with its own
geometry and supplied matched compact potential. Standard Hamiltonian compact
gauge theory is prior art: [Kogut–Susskind1975](https://doi.org/10.1103/PhysRevD.11.395).

## 4. Explicit nonabelian links and anomaly conditions; regulator still open

The independent internal27 carrier is supplied in its standard decomposition

`10_(1,1)+bar5_(-3,1)+1_(5,1)+5_(-2,-2)+bar5_(2,-2)+1_(0,4)`

under`SU5 x U1_chi x U1_psi`. On10, use the actual exterior-square matrix
`R(U)_(ab,cd)=U_ac U_bd-U_ad U_bc`; on5 andbar5 useU and its conjugate.
Multiply each block by its two charge phases. This provides a finite group
representation and gauge-covariant hopping on every native edge. Seeded
homomorphism and hopping covariance errors are below2e-15.

For a general traceless SU5 Cartan elementX and independenta,b, the exact
polynomial`Tr_27(X+a Qchi+b Qpsi)^3` vanishes identically; the linear trace also
vanishes. Conjugacy to the Cartan and polarization imply cancellation of all
local cubic and mixed anomalies of this supplied representation. No opposite
Qpsi pair exists, so a bare Weyl mass bilinear is forbidden while that U1 remains
unbroken. Under the embedded SU2 acting on two fundamental colors, the27 has
six doublets and15 singlets.

The standard branching and anomaly cancellation are **already owned** by
`analysis/w33_20261019_round13_chiral_anomaly_27.py`; explicit SU5 generators
and24^3 anomaly entries already occur in
`analysis/w33_pass11984_native_fiber_overlap.py`. The added objects here are the
joint finite-link representation and covariance controls, not a new GUT spectrum.

A current primary-source connection is Craig's October2026
[preprint2610.09093, Proposition11.1](https://arxiv.org/html/2610.09093v1#S11.SS1).
It states representation conditions involving the cubic anomaly and even
half-integer SU2 multiplicities for a measure construction on ordinary4D
Euclidean lattices. This SU5 restriction passes those representation conditions.
We have inspected the relevant statement, not independently verified that
preprint's full proof or implemented its measure. Its spacetime/admissibility
construction and the extra U1 factors cannot be imported merely from the counts.
[Lüscher2000](https://arxiv.org/abs/hep-lat/0006014) supplies the established
perturbative reference; [Lüscher1998](https://arxiv.org/abs/hep-lat/9811032)
treats the abelian nonperturbative construction.

**Boundary:** ordinary hopping is vectorlike. A chiral fermion measure/regulator,
an intertwiner to the canonical signed45-term cubic, global anomaly completion,
three generations, exotic masses and a physical vacuum remain unbuilt.

## 5. Content review and an extra analytic result from another track

The reading ledger now marks39 of210 pages:72–110. The additional pages95–110
were read as full extracted text. They document FI/parity obstructions,
fractional-charge indices, flavor degeneracy and unstable vacuum directions;
none is bypassed by the finite gauge model above.

Six of the frozen481 original commits now have full-patch read flags: five are
empty reservation commits, and one is the complete substantive
`a15185e5c9fa28d820a69df8d1dcfda7fb040544`. The substantive patch was read in
four contiguous chunks, including its Python, JSON, TeX and PDF text conversions.
Its running calculation led to the following strengthening. All remaining
original commits retain false flags. Extraction/archival, basename resolution
and reading are distinct; the complete requested review is **unfinished**.

### A continuous bound replaces a sampled common-threshold exclusion

Pass12330 computes full-spectrum coefficients`(b3,b2,bY)=(7,16,148/3)` and
samples53 common thresholds. Using exactly its frozen low-scale inputs and
one-loop model, set`u=log(M_X/M_Z)/(2pi)`. Above the common threshold, at the
alpha2=alpha3 crossing,

```
log(M_cross/M_Z)/(2pi) = 31u/54 + 31133509/13275000,
A2 = 539u/54 - 105434563/13275000,
AY = 2297u/162 - 27610213/1593000,
AY - (2297/1617) A2 = -3607345249/596268750 < 0.
```

Therefore, on **every** crossing above the common threshold withA2>0,

`kY=AY/A2 <2297/1617 <8/3`.

This conditional exclusion is continuous in the threshold. It does not depend
on sampling53 points. The formula reproduces all53 stored grid values to
3.7e-13. Searches for2297/1617,539/54 and variants across the results index and
Python/JSON/Markdown/TeX/HTML found no existing version of this bound. The
sampled obstruction belongs to Pass12330; this packet supplies its analytic
strengthening. Separate thresholds, two-loop corrections and different spectra
are outside the theorem. No unification or TOE has been obtained.

## Independent next directions

Validation before publication: the producer regenerated its certificate; all21
focused controls across the new packet and the two preceding Oct27 packets
passed in24.91s. The rediscovery guard passed. The results index was regenerated
after the new source and report paths existed. Unrelated shared files were
excluded from the commit.

1. Find a microscopic mechanism selecting the reflection-averaged action and radius.
2. Compute interacting gapped-matter response on the full native cell.
3. Obtain certified truncation bounds and enlarge the compact patch.
4. Build the canonical-cubic intertwiner and an actual chiral regulator.
5. Complete the content review and test nondegenerate thresholds in the string candidate.
