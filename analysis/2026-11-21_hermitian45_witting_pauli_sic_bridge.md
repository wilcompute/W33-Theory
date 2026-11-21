# The 45 missing Witting points: Hermitian polarity, two-qutrit tensor frames and dual-SIC readout

**Date:** 2026-11-21. **Status:** independently executable finite-projective and ideal-quantum calculation; **not** a new physical theory or QKD security proof.

## Sources, and strict novelty boundary

- A. Yu. Vlasov, *Scheme of quantum communications based on Witting polytope* (2025), https://arxiv.org/abs/2503.18431 : equations (1)-(4), 240 complex polytope vertices / six phase lifts = 40 rays, and 40 orthogonal four-ray contexts; the discussion describes an ideal two-ququart communication protocol, NOT two entangled qutrits.
- Frans Marcelis, *Witting polytope*, https://fgmarcelis.wordpress.com/witting-polytope/ : a 2160-triangle complex-polytope construction and 40 hexagonal diameters, with an 8D/E8 visualization. His site https://fgmarcelis.wordpress.com/ also discusses PG(3,4), the 600-cell and octad geometry. The cited constructions are antecedents, not newly claimed.
- Planat–Saniga, *On the Pauli graphs of N-qudits*, https://arxiv.org/abs/quant-ph/0701211 : Pauli commutation and symplectic finite geometry (historically sometimes using the dual quadrangle).
- Earlier **W33-Theory** proofs: \`tools/witting_graph_isomorphism.py\`; \`tools/witting_pg32_fiber_analysis.py\` already uses GF(4) Hermitian coordinates; \`scripts/w33_witting_deck_control_audit.py\` proves the 36-spread decks; \`analysis/2026-10-15_toe90_vlasov_witting_research.md\` establishes the 40-ray projective 2-design; \`analysis/toe_20261104_witting_operator_dark_spectral_A5_duality.py\` already proves the ququart projector Gram's rank 16 and -4 spectral sector; \`analysis/toe_20261120_octonion_mereology_radon.py\` already enumerates 45 two-qutrit tensor frames. We **do not claim novelty** for any of those isolated facts.

The new **explicitly assembled and verified dictionary** here goes all the way from the 45 GF(4) isotropic points through their 8-point polar neighborhoods to **exactly the 45 Pauli nondegenerate plane-pair frames**, and identifies each eight-ray optical chart as **two orthogonal qubit tetrahedral SICs**, leading to a second exact measurement-context realization of the same Witting informationally-complete POVM.

The requested \`https://finitegeometry.org/sc/map.html\` did not respond to HTTPS requests via the public web fetcher or the Windows host on this pass (the latter timed out after 12 s). Its complete list of linked papers was **not** inspectable; no assertion of having read that list is made. Its attribution to Steven H. Cullinane and related finite square/cube sources was corroborated using the SourceForge project page and indexed bibliographic references.

## The finite-field bridge

Use GF(4) = {0,1,a,a^2} with a^2=a+1, and Hermitian form
\[
h(x,y)=\sum_{j=1}^4 x_j^2 y_j.
\]
Of 85 points in PG(3,4), exactly 45 are Hermitian isotropic and 40 anisotropic. The anisotropic points are the 4 coordinate axes plus 36 points having exactly three nonzero coordinates. Reduce Vlasov's 40 complex Witting rays by sending the cubic phase \(\omega\) to \(a\), with signs disappearing in characteristic two. Both the complex Hermitian zero-overlap graph and the GF(4) Hermitian-polar zero graph agree on **all 780 unordered pairs**, yielding SRG(40,12,2,4). This is a bridge of finite incidence and a specific complex realization, **not** a ring homomorphism C → GF(4).

Let \(A\) be the 40-by-40 collinearity adjacency matrix in the equivalent symplectic W(3,3) realization. Enumerate its 40 totally isotropic four-point lines and their point-line incidence matrix \(N\):
\[
NN^{\mathsf T}=4I+A,\qquad
{\rm spec}(NN^{\mathsf T})=16^1+6^{24}+0^{15},
\]
\[
{\rm SNF}_{\mathbb Z}(N)=\operatorname{diag}(1^{25},0^{15}).
\]
Thus the integer image is saturated of rank 25: reducing N modulo *any* prime does not lower the rank. This is strictly stronger than a numerical rank check.

## The 45 ↔ 45 dictionary

For each of the **45 isotropic Hermitian** points \(z\) set
\[
S_z=\{x\ \text{among the 40 anisotropic points}\mid h(z,x)=0\}.
\]
The exhaustive result is:

1. \(|S_z|=8\) for every z, and each anisotropic point belongs to 9 such sets.
2. The induced graph on each \(S_z\) is precisely **K(4,4)**.
3. The 45 support sets are distinct and intersect pairwise in **zero points (270 pairs)** or **two points (720 pairs)**.
4. Independently, over F3 enumerate the 90 two-dimensional nondegenerate symplectic planes L in F3^4. Pair each plane with its four-point symplectic orthogonal complement L-perp; each unordered pair defines an 8-point projective subset. There are **45**.
5. Under an independently found Witting→W(3,3) graph isomorphism, the **45 polar sets are exactly the 45 symplectic two-plane-complement supports, without exceptions**. The complete GF(4) point → eight Pauli indices lookup is frozen in JSON.

Write \(K_{z,x}=1[x\in S_z]\), a 45-by-40 incidence. Its exact identities are
\[
K^{\mathsf T}K=8I+2A+J,\qquad
{\rm spec}(K^{\mathsf T}K)=72^1+12^{24}+0^{15}.
\]
The frame incidence map and line incidence map therefore have the **same 15-dimensional kernel** (the W33 adjacency eigenvalue -4 sector). The projector Gram of the actual Witting ququart rays is instead
\[
G_{xy}=\operatorname{Tr}(P_xP_y)=(2I+J-A)/3,
\quad {\rm spec}(G)=10^1+2^{15}+0^{24}.
\]
Its 15 traceless physically observable directions are **precisely those invisible to chart/line incidence SUMS**, while the individual output labels retain their information. The rank-16 Gram identity was already known in the repo; the explicit GF(4) polarity/chart duality and the combined measurement interpretation are the emphasis here.

## Two qubit tetrahedral SICs per Hermitian point

Inside one induced K(4,4), the two independent four-vertex classes consist of four rays with pairwise squared overlap \(1/3\), each spanning exactly a two-dimensional complex subspace. Each is a tetrahedral qubit SIC. Those two subspaces are orthogonal and fill C4. Over **all 90 four-ray blocks** and all **45 eight-ray sets**, a numerical check finds
\[
\sum_{x\in S_z}P_x=2I_4.
\]
This produces a valid **eight-outcome POVM** for each chart: \(E_{x|z}=P_x/2\) for x∈S_z. It is a generalized POVM, *not* an ordinary four-outcome projective measurement; a physical implementation requires additional optical measurement structure or randomized/coarse-grained implementation.

### A distinct implementation of exactly the same 40-outcome POVM

**Original Vlasov contextual projective implementation:** choose one of the **40 orthonormal tetrads** uniformly, record one of four projective outcomes \(P_x\), and forget which tetrad was used. Each ray belongs to four tetrads, so the marginal effect is \(4P_x/40=P_x/10\).

**New 45-chart double-SIC implementation:** choose one of the **45 Hermitian/tensor charts** uniformly, record one of eight outcomes with effects \(P_x/2\), and forget the chart. Each ray belongs to nine charts, so the marginal effect is \(9P_x/(45\cdot2)=P_x/10\).

Both are the same 40-outcome informationally complete Witting ququart POVM. The source-state probabilities are directly checked on a nontrivial pure Witting state; each of 45 chart POVMs normalizes to one. These equivalent **unlabeled** statistics do not mean the full **labeled** instruments, noise mechanisms or security guarantees are equal. Chart dependence may be operationally valuable, but a rigorous key protocol must control the announced settings and adversarial loss.

## Physical limits and next falsifiers

This is a **duality of incidence and POVM realizations**. The 45 Pauli charts are two-qutrit tensor factorizations on a **nine-dimensional Hilbert space**, whereas the 45 double-SIC contexts are measurement architectures on **four-dimensional ququart Hilbert space**. No physical C4→C9 intertwining isometry preserving all Weyl algebra operations is asserted. The full two-qutrit Heisenberg representation is irreducible, so a common 4D invariant subspace does not exist. An operational two-qutrit bridge must specify an encoding/channel and measurable fidelity, not merely the 45-chart bijection.

Other independent remaining fronts, not solved by these finite calculations: a physical dynamical selector of one of 45 charts; a covariant Lorentzian/Einstein limit; anomaly-free chiral families and mass mechanism; instrument-calibrated delayed-query finite-key QKD; and a process-tensor witness of genuine multitime memory beyond static Choi correlation.

## Reproduce

\`\`\`shell
python analysis/toe_20261121_hermitian45_pauli_sic_bridge.py
python -m pytest -q tests/test_toe_20261121_hermitian45_pauli_sic_bridge.py
\`\`\`

Certificate: \`data/toe_20261121_hermitian45_witting_pauli_sic.json\`. Script recomputes the 85 finite-field points, all graph edges, independent graph isomorphism, 45 Pauli charts, 45 GF(4) polar supports, Smith normal form and all optical SIC/POVM checks.
