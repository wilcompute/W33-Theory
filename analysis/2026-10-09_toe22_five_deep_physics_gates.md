# TOE Round 22 — five nonsequential physics searches on the native W33 carrier

**9 October 2026.** This packet executes the five directions selected after Round21:
construct the unique PGSp-invariant 81-cubic and test Jacobi; quantize the
selector; test whether four-dimensional locality emerges; make a local
qutrit Gauss+Wilson model; and test emergence of an absolute scale.

**Precision boundary:** These are exact finite-geometry and finite-model
statements plus declared numerical diagonalizations. No empirical TOE,
physical vacuum, Standard Model spectrum, Lorentzian metric or new E8 Lie
algebra is claimed. All files are separately named; parallel Pass398, Pass118xx
and others are left untouched.

## 1. Materialize the unique cubic — and falsify the naive 81D Lie bracket

**Prior result:** Round21's exact character sums established
`dim (Λ³ St81)^{PGSp(4,3)} = 1`, with PGSp order 51,840.
Pass11681 already constructs *another* legitimate E8 graded Lie algebra
as `sl(9)+Λ³(9)+Λ³(9)*`.

**New explicit tensor:** Generate the exact 51,840 flag permutations on
the 160 point-line chambers. Choose the ordered flag triple **(17,42,150)**.
Average its oriented wedge over the entire extended group to form the
integer signed-orbit three-form `F` on the flag permutation module.
Exactly **51,840 signed flag-triple terms** remain (in the stored
compressed alternating form). Restriction to the 81 fundamental Levi
cycle columns `Z` is **nonzero**, with direct integer evaluations
`-3780, -8047, 10381` on three seeded integer cycle triples.
The full tensor is invariant under checked group transformations. Since
the **prior exact character certificate** shows invariant
exterior-cubic multiplicity one, this constructs a generator of that
unique line rather than merely computing its dimension.

Let `G=Z^T Z`, the positive integral cycle Gram matrix. Make the
obvious metric-compatible candidate
`[x,y]^k=(G^{-1})^{kℓ} F(x,y,Z_ℓ)`.
This is alternating and PGSp-equivariant, but **does it obey Jacobi?**

**Answer: NO.** The producer computes Jacobi exactly modulo the
prime **101**, where `G` is invertible (its determinant is
`2^83 5^23`, previously established). All eight seeded test triples
have nonzero Jacobi vectors (nonzero coordinate counts **81, 81,
79, 78, 79, 77, 80, 81**). A saved *elementary fundamental-cycle basis
triple* also gives an explicit nonzero vector. This is a rigorous
counterexample in characteristic 101, hence an obstruction to the
rational/integer metric-raised 81-only Jacobi identity: a rational
identity with denominator invertible at 101 could not reduce to a
nonzero Jacobi vector.

**Important limitation:** The failure is for a standalone
`St81 × St81 -> St81` bracket, NOT for the real E8
`(27,3)×(27,3)->(27*,3*)` and
`(27,3)×(27*,3*)->(78,1)+(1,8)` mixed brackets.
A full graded Jacobi system needs those missing **86** adjoint
directions and their actual intertwiners. The unique cubic is not a
shortcut to E8; its identification with E8 matter sectors remains open.

## 2. Full two-boson quantum selector (not just nonlinear mean field)

Use native W33 Levi 80-vertex 4-regular graph. In its exact bosonic
N=2 Fock sector dimension `80*81/2=3240`, construct the full sparse
attractive Bose-Hubbard Hamiltonian

`H=-t Σ_{<i,j>}(b†_i b_j+b†_j b_i) - U/2 Σ_i n_i(n_i-1)`.

Numerical sparse Hermitian diagonalization with t=1 gives:

| U/t | E0/t | Gap/t | Pair doublon probability |
|---:|---:|---:|---:|
| 0 | -8 | 1.550510 | 0.012500 |
| 3 | -8.074182 | 1.412407 | 0.048124 |
| 8 | -9.920171 | 0.363002 | 0.762018 |
| 16 | -16.985129 | 0.186468 | 0.940163 |
| 32 | -32.498064 | 0.095930 | 0.984555 |

All observed site occupations agree with **2/80 = 0.025**
to better than 3e-14. This is not numerical luck:
the hopping graph on two-boson configurations is irreducible and
stoquastic for every `t>0`. Perron–Frobenius makes the finite
ground state **unique and positive** for every finite U. Since
graph automorphisms commute with H, the unique ground is invariant
and cannot choose a specific W33 site. The Round21 nonlinear
mean-field metastability does not override this finite-system theorem.

The strong-U doublon *pair* band has virtual hopping `2t²/U`
and leading gap `(2t²/U)(4-sqrt(6))`; its U=32 prediction
agrees with the exact 3240-state numerical gap to within 3%.
No finite quantum spontaneous symmetry breaking is established.
A controlled N scaling, decoherence, order-parameter field or
thermodynamic limit would be further, explicit hypotheses.

## 3. A stronger four-dimensional spacetime obstruction from symplectic symmetry

Round21 separately checked that the raw W(3,q) incidence graph family
does not give a 4D heat-kernel scaling plateau. Instead, test the
natural affine `F3^4` underlying the two-qutrit Pauli labels,
which has exactly 81 points. Suppose a kinetic graph is:
(i) invariant under all translations of this affine group and
(ii) invariant under the entire natural Sp(4,3) group.

**Full exact 80-vector breadth-first orbit** under 40 elementary
symplectic transvections shows Sp4(3) is transitive on every nonzero
displacement of `F3^4`. A translation-Cayley edge displacement
set invariant under Sp must be a union of orbits, so it is
**either empty or all 80 nonzero displacements**.

The ONLY nontrivial fully symmetric translation hopping is therefore
the **complete graph K81**, not a four-axis local lattice.
Its normalized graph Laplacian has eigenvalues `0^1,(81/80)^80`,
with heat return `P(t)=(1+80 exp(-81t/80))/81`.
In particular, four sparse axial unit-displacements require a
**symmetry-breaking choice of frame** or a fundamentally different
encoding. For general q, the same Sp4(q) transitivity gives K_(q⁴).

This is a specific no-go for simultaneous *unbroken* natural
symplectic and affine translation invariances on this carrier,
**not** a theorem forbidding 4D Lorentzian spacetime in any W33-derived
theory. A local emergent vierbein, causal metric and suitable
refinement remain open.

## 4. An explicit local 160-link qutrit gauge Hamiltonian — 81 killed by flatness

On the **actual** 80-vertex, 160-flag W33 Levi graph, place one
qutrit on each oriented incidence link. Let D be its 80x160
integer signed vertex-edge boundary and let `C` be the matrix
of all **1,620** simple oriented eight-cycle vectors.

Build commuting qutrit Pauli operators
`G_v = ∏_{e} X_e^{D_{v,e}}` (four-link vertex Gauss)
and `W_c= ∏_{e} Z_e^{C_{c,e}}` (eight-link Wilson cycle).
The exact incidence identity `D C^T =0 mod 3` guarantees
`[G_v,W_c]=0`. Vertices commute among themselves, as do loops.
Define a **conditional** local stabilizer Hamiltonian
`H=-gΣ_v(G_v+G_v†)-κΣ_c(W_c+W_c†)` with g,κ>0.

The native exact rank audit gives
`rank D=79`, `rank C=81` over F3 and a
full independent stabilizer rank `79+81=160`.
Consequently:
- **Gauss only:** `[[160,81]]_3` stabilizer space: 81 logical
  qutrits, *no code distance implied*.
- **Gauss + complete flatness:** `[[160,0]]_3`:
  **unique ground stabilizer state**; no logical qutrits.
- Every nontrivial individual constraint violation costs 3g or
  3κ in energy; a positive gap exists in this commuting model.

Thus the 81 protected **cycle coordinates** are not simultaneously
81 freely surviving quantum logical modes when the full Wilson
flatness projector is chosen. Keeping them requires different
dynamics: flux excitations, boundaries, constrained subsets,
higher-dimensional cells, or a nontrivial topological phase.
A 1D finite graph's gauge redundancy does not supply 3+1D Yang–Mills.

## 5. Actual quantum scale analysis: exact scaling and Feynman–Hellmann

Use the same independently fixed N=2 Bose Hubbard Hamiltonian.
The exact operator identity `H(t,U)=tH(1,U/t)` means
`E_n(ct,cU)=cE_n(t,U)`.
We checked this numerically for three arbitrary positive rescalings
`c=0.5,1.7,3`. Every energy and gap scales with c
while eigenvectors, normalized pair correlations, occupation ratios,
and every dimensionless spectral ratio remain unchanged.

A second independent check uses Feynman–Hellmann:
`dE0/dU=-<Σ_i n_i(n_i-1)/2>`.
At `U/t=8`, symmetric central finite differences give
`dE0/dU ≈ -0.76201535`, against doublon
`-0.76201813`: difference ≈2.8e-6.

The U=32 effective low-band gap from virtual hopping is
`2t²(4-sqrt(6))/U ≈0.09691t`, compared with numerically
`0.09593t`. This is a **tunable emergent dynamical scale**
for a *specified* finite toy Hamiltonian, not an absolute value
derived by geometry or an observed particle mass.

The exact finite matrix partition function
`Z(β,t,U)=Tr exp[-βH(t,U)]` is analytic for all finite β
and real t,U. A universal continuum renormalization-group law or
nonanalytic thermodynamic transition does not follow without an
additional scaling limit; the graph does not select t or U in eV.

## Hard evaluation

Strongest positive structural result: an **explicit materialization**
of the unique PGSp-invariant cubic tensor on 81 cycles.
Strongest new hard obstruction: its **native metric-dual 81 Lie bracket
violates Jacobi**, so the proposed shortcut to E8 is false.
Strongest viable physics designs: a fully local commuting 160-qutrit
gauge model, and an exact finite attractive-pair quantum model,
each with experimentally meaningful but **parameter-dependent**
spectra. Neither establishes observed 3+1D physics.

### Reproducers

- `analysis/w33_20261009_toe22_cubic_jacobi.py` and
  `data/w33_20261009_toe22_cubic_jacobi.json`
- `analysis/w33_20261009_toe22_two_boson_quantum_selector.py`
- `analysis/w33_20261009_toe22_symplectic_locality_nogo.py`
- `analysis/w33_20261009_toe22_native_gauge_hamiltonian.py`
- `analysis/w33_20261009_toe22_scale_nogo.py`
- matching `data/w33_20261009_toe22_*.json` certificates and
  `tests/test_w33_20261009_toe22_five_toe_fronts.py`.
