# Five independent follow-ups: exact W33 geometry versus physical claims (22–23 October 2026)

This note implements **all five requested fronts** after inspecting the October 22 latest `master`. The main manuscript's physical caveats remain in force. Exact finite computations are distinguished from conjectures, phenomenological Hamiltonians, physical optical hardware, and continuum spacetime.

Code: `analysis/w33_20261022_allfive_deeper_frontiers.py`, `analysis/w33_20261022_K_jordan_extension_census.py`.
Tests: `tests/test_w33_20261022_allfive_deeper_frontiers.py`.
Certificates: `data/PART_20261022_ALLFIVE_DEEPER_FRONTIERS.json` and `data/PART_20261022_K_JORDAN_EXTENSION_CENSUS.json`.

## 1. Logical Jordan extension: exact nonsplitting and a new uniform candidate

Retain the distinct ternary point-coordinate modules
`C=row(B)`, `K=C^perp=ker(B)`, and `Q=K/C`.
A point transvection `T` acts on all three. The previous all-prime
decomposition of `C=Sym^(p-1)(F_p^4)^*` is proved, but the quotient extension does **not** generally split.

At p=3 the exact Jordan multiplicities are:

| Module | J1 | J2 | J3 |
|---|---:|---:|---:|
| C, dimension 10 | 3 | 2 | 1 |
| Q, dimension 20 | 3 | 4 | 3 |
| K, dimension 30 | 8 | 2 | 6 |
| A hypothetically split C + Q | 6 | 6 | 4 |

Since the Jordan type of K is not that of C direct-sum Q, the short exact sequence
`0 -> C -> K -> Q -> 0` is **non-split as an F3[<T>]-module**.

The independent computation works with the 40-dimensional permutation module `M`:
the coordinate dot product identifies `K=(M/C)^*` equivariantly, and the cyclic
Jordan type is preserved by duality. Hence, if `D=T-I`,

`rank(D^j | K) = rank([basis(C); D^j])-dim(C)`.

This gives exact rank-power sequences for p=2,3,5,7, and a second pattern:

```
K | <T>  ?=  J1^((p²+p+4)/2)
           + sum_(j=2)^(p-1) Jj^j
           + Jp^(p(p+1)/2).
```

The equality **is presently a four-prime conjecture**, not an all-prime theorem. It is verified by modular elimination for p=2,3,5,7. The p=2 overlap of the last and intermediate block conventions is handled explicitly. This new intermediate-module pattern could help the algebraic extension proof. Pass12187 is separately reserved on another Codex track: prior code and simultaneous work take precedence.

## 2. Clock dynamics: actual thermodynamic symmetry breaking, but in a phenomenological model

Build a **40-state Curie–Weiss Potts model** from N replicated anchor variables,
with `n_a` the number selecting W33 point a and
`E_N= -J/(2N) sum_(a=1)^40 n_a²`, J positive.

For a macroscopic occupation vector s, the exact mean-field variational functional is

`F_beta(s)/J = -(1/2)sum s_a² + (1/(beta J))sum s_a log(s_a)`.

Established mean-field Potts theory (Ellis et al.; see published treatment at
https://www.cambridge.org/core/journals/advances-in-applied-probability/article/on-approximating-the-potts-model-with-contracting-glauber-dynamics/8E47C85A421D23D07DE50860487744B9)
gives the first-order transition for q>=3,

`beta_c J = 2(q-1)/(q-2) log(q-1) = 7.519942326266117` for q=40.

At coexistence, the disordered state has s_a=1/40 while each of forty
ordered states has one occupation 39/40 and the remaining 39 occupations
1/1560 each. The two free energies agree exactly. The uniform branch
does not lose **local** stability until beta J=40.

The finite-N Gibbs ensemble remains symmetric; symmetry-broken pure phases
arise only after taking N to infinity and selecting an extremal phase.
Crucial firewall: this toy model has the **larger full S40 permutation symmetry**;
nothing in it uniquely selects W33 incidence geometry, fixes chirality,
derives physical time, or derives an Einstein action. It demonstrates a
mathematically consistent thermodynamic selection mechanism, not a TOE.

## 3. Optical-gate preparation: direct 12-regular W33 graph SWAP circuits

Each symplectic projective transvection consists of nine disjoint 3-cycles
and 13 fixed points. Every 3-cycle's moving vertices are pairwise **noncollinear**,
so the previous 2-layer/18-SWAP method needs B couplers (degree 27),
not the ordinary W33 collinearity graph A (degree 12).

The new exact route is to implement each remote swap of endpoints u,v (A[u,v]=0)
along an A-path u-h-v using three adjacent physical swaps:

`SWAP(u,h), SWAP(h,v), SWAP(u,h)`.

For each of the nine simultaneously required remote swaps, assign a distinct
common-neighbor h which is *not an endpoint of any of the nine pairs*.
A deterministic augmenting-path matching proves that a collision-free choice exists
for **all 40 anchors in both remote-swap stages**.

The entire transvection therefore compiles to
**6 parallel layers, 9 SWAPs per layer, 54 A-edge SWAPs total**.
The certificate freezes both sets of nine intermediate vertices for every anchor.
Each complete permutation is replayed on all 40 labels, not just counted.
The depth is a **constructive upper bound**, not a proven optimum. Every one of the **2,160 individual A-edge SWAP placements** (40 anchors x 54 SWAPs) is explicitly exported in six per-anchor `swap_layers` schedules, alongside the intermediate assignments. Under a hypothetical independent per-SWAP failure probability `epsilon_swap`, the no-fault probability for one transvection is `(1-epsilon_swap)^54`, and a union bound gives total gate-failure probability at most `54 epsilon_swap`; this is a parameterized idealized estimate, not measured fidelity.

Physical firewall: this is an ideal 40-qudit SWAP-only nearest-neighbor
architecture. The single-photon path/time/frequency Holonet carrier is not
automatically a 40-physical-qutrit processor; native photonic mode couplers,
routing loss, timing, failure probabilities, gate calibration and syndrome
extraction still need an actual device model.

## 4. Non-Clifford injection: the failed gate has a rank-three *flat* syndrome spectrum

The previous `U=diag(1,zeta_9,zeta_9²)^(tensor 40)` trial had
post-projection survival probability 1/27 on an explicit weight-4 logical coset.

A stronger exhaustive calculation enumerates the **59,049** classical C words.
Writing each word as `c=t_0 C_0+...+t_9 C_9`, the additional ninth-root phase
for `u=(1,1,1,1,0,...,0)` reduces to `omega^{f(t)}`, where

```
f(t) = 2(t0²+t1²+t2²+t0*t1+t0*t2+t1*t2) mod 3,
omega=e^(2pi i/3).
```

This is an *exact quadratic phase polynomial* on three of ten
stabilizer coordinates; its symmetric cross-term matrix has rank 3 over F3.
Consequently its full ternary Fourier transform has **27 nonzero** components,
each of normalized probability **1/27**, and the other 59,022 amplitudes vanish.
An independent 10-axis ternary FFT verifies the exhaustive arithmetic.

Interpretation: the ninth-root gate has coherently distributed this logical coset
among 27 Pauli-Z character/syndrome components. It suggests a finite
rank-three stabilizer-phase correction problem, but **does not** prove that a
syndrome-conditioned Pauli correction implements one deterministic logical
non-Clifford gate for *all* 3^20 logical basis cosets; compatibility between
different cosets is the missing test. No injection circuit, decoder, distillation
threshold, or physical gain has yet been established.

Relevant established frameworks include Hu–Liang–Calderbank,
*Designing the Quantum Channels Induced by Diagonal Gates*
(https://arxiv.org/abs/2109.13481), and Campbell–Anwar–Browne,
*Magic state distillation in all prime dimensions using quantum Reed–Muller codes*
(https://arxiv.org/abs/1205.3104).

## 5. Multi-anchor escape route: spectra detect the symplectic pairing

Take the *already certified* DCLXVIII Markov base Hamiltonian
`H0=27I-B` and the nonnegative anchor Laplacians
`D_u=2I-T_u-T_u^-1`.
For two **distinct** projective anchors u,v define
`H(u,v)=H0+D_u+D_v`.

An exact SymPy characteristic-polynomial factorization finds two
different spectra, *classified by the symplectic pairing*:

- If u,v **commute / are collinear** (240 unordered pairs), H has
  **6 distinct eigenvalues**: 0,24,27,30,33,36.
- If u,v **do not commute / are noncollinear** (540 unordered pairs), H has
  **12 distinct eigenvalues**, including roots of
  `lambda²-66lambda+1086` and `lambda²-54lambda+726`.

The script certifies representative exact integer characteristic
polynomials, and tests **all 780 unordered pairs** by an independent
symmetric eigensolver classification. Projective symplectic symmetry
explains why the two pair-orbit spectra are constant.

This is a rigorous finite spectral **commutation witness**:
noncommuting clock anchors split the five-level single-clock spectrum
substantially more than commuting anchors. It **escapes the restricted
one-anchor p+2 bound**, but neither two anchors nor a 40-dimensional
Hamiltonian produces a Weyl-law continuum, Lorentz covariance, or gravity.
A genuinely growing tower of interacting modes is still required.

## Independent top five next steps

1. Prove the all-prime *K* Jordan formula and derive the nontrivial extension
   class relating C,K,Q, including Frobenius twists at p^t.
2. Break the Potts model's artificial S40 enhancement by a genuinely
   W33-native interaction, and derive its large-N vacuum phase diagram.
3. Lower-bound and optimize the verified six-layer SWAP routing on A,
   then compile onto real photonic couplers and evaluate errors and loss.
4. Evaluate the ternary Fourier syndrome support as a function of
   **logical** coset label, seeking a coherent feedforward correction
   whose induced logical action is non-Clifford and unitary on every input.
5. Determine whether a growing number m(q) of noncommuting anchor
   interactions can yield a local low-energy field theory, spectral
   dimension and causal propagation with controlled scaling.
