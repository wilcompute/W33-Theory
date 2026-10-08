# 2026-10-08 — W33 20-apartment Z2 breakthrough: a [[60,2,6]] binary CSS code, exact F20 logical SWAP, Wilson partition and physical no-gos

**Status:** five independent fronts executed with reproducible exact finite-algebra producers and tests. One **new binary stabilizer code and a symmetry-induced logical operation**, one **exact finite-field partition function** and two physically scoped no-go/error-bound calculations. The explicit characteristic-zero tetraquadric metric/Yukawa frontier was attempted but **not solved**. This is not a completed Theory of Everything.

**Research base:** `origin-https/master` commit `a858260b2`, after reading current and parallel commits, plus full repo source search. The selected 20 apartments came from October's earlier 45-cycle commuting atlas; many **related Z2 constructions** existed earlier but they must not be silently identified by group order or shared mod-two cohomology. All work was isolated from the dirty main checkout.

## 0. Source archaeology: what prior research *already* contained

The user's recollection refers specifically to the 20-apartment construction and the Z2 program, not the March external four-torus. An exact pre-October instance of **this particular signed 20-apartment support** was **not confirmed** from the accessible filename, commit-message and contents searches. Crucial older matches *were* found:

- **BT744 (June 2026):** all **1,620** W33 Levi eight-cycles are the apartments of the symplectic C2 building; Steinberg first homology has rank81.
- **July Pass 76–79:** D(Z3) toric code `[[18,2,3]]_3` on an ordinary 3×3 torus, and a *separate* attempted 40-point binary incidence code whose naive CSS check fails. In `analysis/2026-07-15_pass78_w33_40point_code.md`, the original document explicitly computes `AA^T ≠0 mod2`. Neither code is the present binary 60-edge code.
- **August Pass 4461–4465:** the global `[1620,39]` apartment-parity code and the 29D radical/10D symplectic quotient; **Pass 4647** constructs the **1620→810→270** two-sheet apartment lift with a central (C_2) deck operation inside six-sheet D12 monodromy. These are older **Z2** structures on distinct carriers.
- **September Pass 10967:** among 215 heterotic models, the program found **0/215 FI-compatible non-R matter parity vacua** in its specified gauge-torus × space-group class. The tentative geometric R-symmetry loophole in **Pass 10968** was **corrected/retracted by Pass 10974** because a non-prime-plane R-rule was invalid. These UV exclusions cannot be undone by finding a binary class on another complex.
- **October prior packets:** `analysis/2026-10-08_beyond_five_H27_center_atlas_physical.md` constructed a selected 45-apartment commuting subset and a 20-term integral relation. `analysis/2026-10-08_twenty_apartment_torus_F20_H27_physical_packet.md` proved the signed support's attached 40-vertex/60-edge/20-octagon CW complex has (pi_1=\mathbf Z^2), integral torus homology, and precise stabilizer (F_{20}=5{:}4). The following work is a **new binary CSS and physical consequence**, not the discovery of apartments/torus homotopy itself.
- **October Pass 11742–11750:** the **21-dimensional Klein-four-invariant tetraquadric linear system is basepoint-free**; generic smooth, free quotient members exist by Bertini. This predates the preceding assistant's claim of finding that existence result: the novelty boundary is corrected here. **No earlier selected explicit smooth polynomial** was verified.

## 1. Exact `[[60,2,6]]_2` CSS quantum stabilizer code from the selected 20 apartments

Take the **actual integral CW incidence maps** (\partial_2:\mathbf Z^{20}\to\mathbf Z^{60}\) and (\partial_1:\mathbf Z^{60}\to\mathbf Z^{40}\). Reduce mod 2, place one physical qubit on each of the 60 *edges*, assign X vertex/star checks (H_X=\partial_1\) and Z octagon/face checks (H_Z=\partial_2^T\). Crucially,

\[
H_XH_Z^T=\partial_1\partial_2=0\quad(\mathrm{mod}\;2).
\]

The exact row ranks are (\operatorname{rank}_2 H_X=39), (\operatorname{rank}_2 H_Z=19), so

\[
k=60-39-19=\boxed2.
\]

The 40 vertex X checks have weight **3** (underlying 1-skeleton is trivalent). The 20 Z octagonal face checks have weight **8**. Because the 20-face complex is **branched**, 40 edges have face incidence 2, while 20 edges have face incidence 4; it is **not** a standard regular two-manifold surface-code cellulation, despite its torus homotopy type. This distinction matters for literal planar/local layout.

**Distance (d_Z=8)**, certified by a breadth-first search over the complete (40\times4) lifted graph of Z2² homology sector labels; the algorithm starts at every vertex and finds the shortest closed path with nontrivial evaluation on the two independent H1 cohomology classes. It supplies the exact eight-edge representative `[0,15,17,10,11,25,24,1]`.

**Distance (d_X=6)** was first found by a bounded integer linear-program optimum on both logical target coordinates with solver status success, zero MIP gap and weight-six witnesses. An **independent exhaustive proof** then checked all cocycle candidates of weights 1, 2 and 3 directly and weights 4 and 5 by finite syndrome meet-in-the-middle (2+2, 3+2, testing disjoint supports). **None** is a nontrivial cohomology class, and the independent six-edge witness `[25,30,40,45,48,57]` satisfies every face check while pairing nontrivially with a logical cycle.

Thus

\[
\boxed{[[n,k,d]]_2=[[60,2,6]]_2,\qquad(d_X,d_Z)=(6,8).}
\]

This is a **new concrete selected W33-apartment quantum CSS code**, distinct from both earlier W33 qutrit D(Z3) and binary global apartment codes. It does not come with a physically local stabilizer readout circuit, noise threshold, syndrome decoder or logical computational universality.

Files:
- `analysis/w33_20261008_twenty_apartment_binary_CSS_F20.py` and JSON
- `analysis/w33_20261008_twenty_apartment_X_cosystole.py` and JSON
- `analysis/w33_20261008_binary_CSS_exhaustive_distance.py` and JSON.

Standard context: [Kitaev surface codes](https://errorcorrectionzoo.org/c/surface) and [homological codes](https://errorcorrectionzoo.org/c/higher_dimensional_surface). These references do not contain the present selected 60-edge complex.

## 2. A new exact operation: physical edge permutation induces logical SWAP

The previous exact (F_{20}) support stabilizer acts on all 40 vertices, 60 edges and 20 faces. The action on edge qubits therefore permutes the support of **every** X-star and Z-face check. Over F2, a simultaneous basis change gives (H^1(X;\mathbf F_2)=\mathbf F_2^2). The 20-element induced representation has image exactly (C_2\subset GL(2,2)), census:

| Order in F20 | Number | Action on encoded logical Pauli classes |
| --- | ---: | --- |
| 1 | 1 | identity |
| 2 | 5 | identity |
| 4 | 10 | **logical SWAP** |
| 5 | 4 | identity |

In a verified **dual X/Z logical basis**, each of the ten order-four elements exchanges **both** logical X generators and **both** logical Z generators. The certificate includes an explicit permutation of **all 60 physical qubits** and logical representative supports; the producer verifies the stabilizer rowspace and symplectic logical pairing directly rather than guessing from the abstract group order.

This is a **permutation-only logical Clifford SWAP, up to possible Pauli-frame phases**. Its physical implementation might require expensive long-range qubit routing; it is not a demonstrated transversal fast optical gate, entangler, injection protocol or universal computer. The order-two and order-five elements act trivially on logical Pauli classes, which does not by itself prove a global-phase identity on encoded states.

Files:
- `analysis/w33_20261008_twenty_apartment_logical_SWAP.py` and JSON
- `tests/test_w33_20261008_Z2_torus_CSS_physics.py`.

## 3. Finite lattice gauge **dynamics** and exact partition functions, no claimed gravity

Use vertex gauge transformation (a\mapsto a+\delta\phi) for a finite (\mathbf Z_q\) link potential on the same 60 edges. Each globally exact plaquette field (F=\delta a\in\mathbf Z_q^{20}\) obeys the **one signed top-cycle condition**, with all 20 coefficients units \(\pm1\).

For q=2, the realizable face-field code is **even parity** ([20,19,2]_2), with weight enumerator (\sum_{w\;\rm even}\binom{20}{w}t^w\). For q=3, nonzero fluxes have two possible signs and the enumerator is
\[
W_3(t)=\frac{(1+2t)^{20}+2(1-t)^{20}}3.
\]

Modding out the 39 effective vertex gauge parameters, **every exact field strength has (q^2) flat holonomy sectors** because (H^1(X;\mathbf Z_q)=\mathbf Z_q^2). Define, solely as an explicitly *chosen* toy Wilson action,

\[
S_q(a)=\sum_{f=1}^{20}\bigl[1-\cos(2\pi F_f/q)\bigr].
\]

The gauge-quotiented finite partition functions are then **exactly**

\[
\boxed{Z_2(\beta)=2\big[(1+e^{-2\beta})^{20}+(1-e^{-2\beta})^{20}\big],}
\]
\[
\boxed{Z_3(\beta)=3\big[(1+2e^{-3\beta/2})^{20}
+2(1-e^{-3\beta/2})^{20}\big].}
\]

Direct finite-state dynamic programming over 20 plaquettes independently matched both formulas. The minimum nonzero *globally exact* plaquette action is **4** (two excited Z2 plaquettes) or **3** (two excited Z3 plaquettes), in the declared dimensionless normalization. Their zero-temperature flat degeneracies are **4** and **9**.

These are finite topological gauge theories **with prescribed toy action**, not a derivation of the Einstein-Hilbert action. A **fixed finite CW complex** does not supply a continuum refinement or propagating graviton merely by having torus homotopy. The mathematical question of coupling apartment C8 currents and imposing a hypersurface-deformation constraint algebra remains open.

File: `analysis/w33_20261008_twenty_apartment_exact_gauge_partition.py` and JSON.

## 4. Photonic hardware robustness: adversarial coherent gate errors and unequal detector efficiencies

Start with the earlier *model-conditional* nominal sorted-histogram separation (\delta_d\) between the 27-port quantum walks at 36, 72 or 144 stages. Suppose each ideal unitary stage differs from its implemented stage by at most (g\) in operator norm. The telescoping inequality gives

\[
\|\widetilde U_d-U_d\|_{\rm op}\le dg
\quad\Longrightarrow\quad
\|\widetilde P_d-P_d\|_\infty\le2dg.
\]

Let final detector relative efficiencies lie within (1\pm r\), yielding conditional probability distortion bounded conservatively by (2r/(1-r)\). The cross-hypothesis worst-case sorted-histogram margin is therefore **at least**

\[
\delta_{\rm robust}\ge\delta_d-
2\big(2dg+2r/(1-r)\big).
\]

Reapply the earlier Hoeffding classifier with conditional failure ≤0.025, and invert the **exact** independent-launch binomial tail with detection-collection failure ≤0.025; the union bound gives ≥0.95 joint correct-classification probability **only under the declared uncertainty model**.

| Per-stage unitary op-norm error bound | Final detector relative efficiency bound | Preferred tested stages | Minimum model-certified launches |
| ---: | ---: | ---: | ---: |
| 0 | 0 | 72 | **2,538** |
| 0.00005 | 0.002 | 72 | **3,116** |
| 0.00010 | 0.005 | 72 | **4,098** |
| 0.00020 | 0.010 | 72 | **7,750** |
| 0.00050 | 0.010 | **36** | **34,729** |

The depth-optimum can actually change under worst-case coherent error: at sufficiently large systematic gate error, the shorter 36-stage circuit wins despite greater ideal Trotter error. **No fabrication, loss, gate error, or detector distribution was measured**; the values are conservative design conditional statements, not predictions for a real chip. A 60-qubit edge permutation logical SWAP is a separate code-symmetry result and is **not automatically executable** by this 27-port optical circuit.

File: `analysis/w33_20261008_photonic_coherent_fabrication_guard.py` and JSON.

## 5. Proton hexality: the **available binary class is insufficient**, proven from MSSM operators

The previous report established an unexpected mod-2/mod-3 contrast: the full (F_{20}) subgroup preserves precisely **one nontrivial** class in (H^1(X;\mathbf F_2)) and **zero nontrivial** classes in (H^1(X;\mathbf F_3)). A discrete binary Wilson-line sector **could** provide one abstract (Z_2) selector, but no physical matter-field charge assignment is given.

This pass independently solves the non-R binary selection-rule question for eight MSSM+N superfields `Q,Uc,Dc,L,Ec,Nc,Hu,Hd`:

- Impose invariance of up-quark, down-quark, charged-lepton, Dirac-neutrino Yukawas and the (\mu\) term.
- Exhaust all (2^8=256\) binary charge assignments. **Eight** meet the allowed-operator constraints. **None** simultaneously vetoes all `QLDc`, `LLEc`, `UcDcDc`, `QQQL` and `UcUcDcEc`; the maximum is **four of five**.
- The no-go also has an exact symbolic proof. The allowed down/up Yukawas and (\mu\) yield (q_{UDD}=q_Q+q_{H}), (q_{QLD}=q_L+q_H), and (q_{QQQL}=q_Q+q_L\) mod 2. Therefore (q_{UDD}+q_{QLD}+q_{QQQL}=0\) mod 2: those three operators **cannot all be odd** under one such non-R parity. Similarly (q_{QLD}=q_{LLE}\) and (q_{QQQL}=q_{UUDE}\).

Under the previously stipulated full (P_6\) charge table `(0,1,5,4,1,3,5,1)`, both dimension-five operators are even mod 2, but forbidden mod 6. The ternary factor is essential for this class of selection rules. All necessary modular anomaly checks or charge tables from previous passes remain **insufficient** to construct an FI-compatible anomaly-free UV symmetry.

**Crucial repo veto:** Pass10967's 0/215 string-vacuum failure for gauge-torus × space-group non-R parities and Pass10974's correction of the Pass10968 non-prime-plane R rule remain authoritative for their specified models. This new elementary `F20/H1(Z2)` cohomology class does **not** overturn them.

The classic proton-hexality classification is Dreiner, Luhn and Thormeier, *Phys. Rev. D 73*, 075007 (2006), https://doi.org/10.1103/PhysRevD.73.075007 . Later discussion emphasizes its ability to forbid dangerous dimension-five operators unlike ordinary matter parity: https://www.sciencedirect.com/science/article/abs/pii/S0370269310010300 .

File: `analysis/w33_20261008_F20_binary_proton_hexality_no_go.py` and JSON.

## 6. Explicit tetraquadric smoothness and Yukawa: rigorously *not yet certified*

Repo prior-art audit found that the previous generic basepoint-free/Bertini argument was **already proven** in Pass11742 and developed into precise 21-basis and quotient flavor/Serre/HYM constraints through Pass11750. This pass **did not** claim to derive generic existence anew.

For a truly explicit candidate, we tested the (\Gamma=Z_2\times Z_2\)-invariant integer polynomial

\[
F=\prod_{i=0}^3(x_i^2+y_i^2)
+2\prod_{i=0}^3(x_i^2-y_i^2)
+3\prod_{i=0}^3(2x_iy_i).
\]

For simultaneous sign flip (g), coordinate swap (h), and their product (gh), the 48 nonidentity ambient fixed points yield nonzero values proportional to \(1\pm2\), \(1\pm3\) and \(2\pm3\) respectively (with factors (16\) on the latter two), so **this explicit candidate avoids all 48 fixed points over characteristic zero**.

But a direct Jacobian Gröbner test of the first affine chart at **prime 7** gave a **nonunit** ideal: this candidate does **not** have a certified smooth good reduction at 7. Nonunit reduction at 7 **does not imply characteristic-zero singularity**. A 30-seed search for another candidate over F3 also found singular F3-rational reduction points and produced no certified complex-smooth polynomial. We explicitly retain these **negative/inconclusive controls** and never claim a normalized Yukawa.

An additional deterministic 21-orbit mod7 modular Gröbner search was attempted, but its first generic computation was too costly to finish within this pass; no result from that unfinished branch is promoted. The next method should use Singular/Macaulay2/Sage for exact saturated Jacobian ideals instead of forcing costly SymPy grevlex elimination.

Even after exhibiting one smooth free quotient, a physical mass still needs moduli fixing, Ricci-flat and HYM metrics, harmonic wavefunctions, anomaly/FI constraints, and normalized overlaps. Earlier Pass11742's nonzero **holomorphic** cubic does **not** equal a physical Yukawa, and Pass11750's other constraints remain.

Partial negative certificate: `data/w33_20261008_tetraquadric_sparse_good_reduction.json`.
Reproducible script: `analysis/w33_20261008_tetraquadric_sparse_good_reduction.py`. Modular prefilter script and certificate: `analysis/w33_20261008_tetraquadric_explicit_smooth_modular_search.py`, `data/w33_20261008_tetraquadric_explicit_smooth_modular_search.json`. No physical mass prediction is asserted.

## Tests, physical firewalls and reproducibility

The focused regression suite `tests/test_w33_20261008_Z2_torus_CSS_physics.py` verifies CSS commutators, two independent exact dX checks, dZ BFS, all 20 induced logical F20 operations, a 60-edge SWAP permutation witness, gauge weight enumerators, discrete-proton operator tables, photonic error margins and the negative tetraquadric reduction. Combined tests additionally use the previously landed torus fundamental-group/H27/F20/photonic producers and old F20-normalizer controls.

**No-go clarity:**
- binary stabilizer `[[60,2,6]]_2` ≠ a universal machine; no fault-tolerance threshold,
- logical SWAP ≠ entangling Clifford/non-Clifford gate,
- exact finite Wilson partition ≠ Einstein gravity or 4D QFT continuum,
- conserved Z2 class ≠ a gauged UV matter parity with chiral spectrum,
- basepoint-free invariant tetraquadric family ≠ selected smooth Ricci-flat vacuum,
- ideal photon sample bound ≠ a measured photonic prototype.

## Top five independent next steps (nonsequential)

1. **Build an actual decoder and faulty syndrome-extraction circuit** for the 60-edge branched surface-code-like construction; test circuit-level threshold/overhead and whether the SWAP edge permutation can be routed locally without leakage or violating code distance.
2. **Derive a controlled physical limit of the finite W33 apartment gauge theory**, including propagating modes and an action; attempt a Bianchi/Dirac constraint closure, explicitly comparing prior C8 center noncommutation. A pure 20-face Wilson toy partition will not yield GR by itself.
3. **Compile the 27-port optical graph discriminator under measured/calibrated coherent errors**, optimize depths and unknown detector efficiencies, and design an experiment that can falsify the two candidate transport geometries.
4. **Search an FI-compatible anomaly-free UV (Z_6) remnant**, using the full Pass10967/10974 string-selection-rule guards; the isolated mod2 Wilson class cannot forbid all dimension-four/five operators.
5. **Certify a single explicit Klein-four-free smooth integer tetraquadric with exact characteristic-zero Jacobian saturation**, then tackle HYM/harmonic normalization and a nonzero physical Yukawa. Prior Bertini establishes generic existence only.
