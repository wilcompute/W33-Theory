# K12, toroidal polyhedra and the genus oscillator

September 15, 2026. Exact certificate: `w33_k12_genus_polarization.json`; executable: `w33_k12_genus_polarization.py`.

## Three meanings that must remain separate

The complete graph K_12, the rank-12 Coxeter–Todd lattice K12, and a genus-six surface are different objects. A genus-six surface has rank-12 integral first homology. This packet constructs an integral symplectic identification with that abstract homology module; it does not construct a triangulation, a conformal surface, or a physical oscillator.

Jungerman–Ringel's *Minimal triangulations on orientable surfaces* (1980), Theorems 1.1–1.2, gives

    n_min(g) = ceil((7 + sqrt(1+48g))/2), except n_min(2)=10;
    E = 3n + 6g - 6; F = 2n + 4g - 4.

[Original paper](https://archive.ymsc.tsinghua.edu.cn/pacm_download/117/6282-11511_2006_Article_BF02414187.pdf).

The orientable genus of the complete graph is ceil((n-3)(n-4)/12). Dropping the ceiling is valid only on the triangular neighborly rungs n modulo 12 in {0,3,4,7}. The first rungs n>=4 are 4, 7, 12 with genera 0, 1, 6. Császár has (V,E,F)=(7,21,14); its combinatorial dual Szilassi has (14,21,7). At genus six the complete-graph triangulation counts are (12,66,44), with dual counts (44,66,12). Counts do not establish a straight-edged realization in three-dimensional space.

| Genus | Minimal triangulation counts | Linear oscillator counts |
|---|---|---|
| 0 | 4,6,4 | 4,6,4 |
| 1 | 7,21,14 | 7,21,14 |
| 2 | 10,30,20 | 10,30,20 |
| 3 | 10,42,28 | 13,51,34 |
| 6 | 12,66,44 | 22,96,64 |

The linear counts (4+3g,6+15g,4+10g) satisfy Euler's equation but cease to be minimal at g=3. This is prior work in `exploration/w33_seven_realizations_oscillator.py`, BT802 and Pass2022, not a discovery of this packet. Their missing-edge count is 9g(g-1)/2. For every g>=3, 3+3g vertices already satisfy the Heawood bound, so the linear count cannot be minimal. The paper's handle subtraction holds vertices fixed and changes (V,E,F) by (0,-6,-4); it is not the linear oscillator's (+3,+15,+10) step. Arithmetic lattice genus, used in lattice mass formulas, is a third, unrelated use of the word genus.

## Explicit integral bridge

Starting with the existing 126 Eisenstein minimal-line representatives, the audit takes each representative and its omega multiple, and computes a column Hermite basis B of their integer span. Its index in the ambient coordinate lattice is 64. Put Q=diag([[1,-1/2],[-1/2,1]]) and O=diag([[0,1],[-1,0]]), each with six blocks. The stored matrices satisfy

    G = B^t Q B, det G = 729;
    E = B^t O B / 2, det E = 1;
    W^2 + W + 1 = 0;
    J = (2W+1)/sqrt(3), J^2 = -1;
    E J = G/sqrt(3) > 0;
    T^t E T = O, det T = 1.

G and E are integral. Thus E is a principal Riemann form for the natural complex structure J. The explicit Darboux matrix T supplies the promised integral symplectic module map. The symplectic nature of K12 is classical; the contribution here is a reproducible matrix certificate tied to this repository's representatives, with the following comparison and obstruction.

## A boundary from Torelli

W is scalar omega on the complex tangent space and preserves the principal polarization. Suppose this polarized abelian sixfold were a smooth curve's canonically polarized Jacobian. Strong Torelli lifts W, up to sign, to a curve automorphism. Its scalar action on holomorphic differentials fixes the canonical image pointwise. For a nonhyperelliptic curve the canonical map is an embedding, forcing the identity. For a hyperelliptic curve it has degree two, leaving only the identity or hyperelliptic involution. Both act as ±1 on differentials, contradicting ±omega. Therefore this specified polarized sixfold is not such a Jacobian. This is an application of classical theory, not a new Torelli theorem. [Milne, Jacobian Varieties, Theorem 12.1](https://www.jmilne.org/math/xnotes/JVs.pdf).

This does not rule out other complex structures, other polarizations, isogenies, higher-genus Jacobian quotients, or discrete surface models. Torelli itself is an external theorem used in this proof; the Python audit verifies the matrix hypotheses, not a formal proof of Torelli.

## Gaussian comparison

Holotrade commit b63daac owns the antilinear Gaussian structure. An independently recovered explicit integral matrix I is stored and checked here:

    I^2=-1, I^t G I=G, IW=W^2 I, I^t E I=-E.

It reverses the Eisenstein form. Its metric-compatible Gaussian Riemann form D=-GI satisfies DI=G>0 and has polarization type (1,1,1,3,3,3), computed by Smith normal form. This particular form is not principal; no uniqueness claim about Gaussian polarizations is made. A computational architecture that exchanges these two complex structures must also track which integral pairing is preserved.

## Oscillator interpretation and coverage

The existing Heawood bridge has adjacency spectrum ±3 once and ±sqrt(2) six times. For P=(9-A^2)/7, rank P=12 and (PA)^2=2P. The centered first-order generator therefore differs from the mechanical model x''=-(3-A)x, whose middle frequencies are sqrt(3±sqrt(2)) for unit masses and the specified stiffness. None of these dimensionless spectra supplies measured masses or time units.

Prior owners include `exploration/w33_heawood_harmonic_bridge.py`, Pass297, BT802, BT1844 and `analysis/w33_pass2022_the_genus_oscillator_and_which_rungs_are_symplectic.md`. The inventory records 57 Python files and 12016 lines discovered by oscillator/harmonic/genus filenames. All were structurally parsed; many relevant sources were read fully, but not every source sentence or every paper has been semantically audited. It is not an exhaustive content-based census. Historical module descriptions in the inventory are quotations, not endorsements; in particular an Euler characteristic alone cannot make the W33 two-skeleton a surface.

Run `OPENBLAS_NUM_THREADS=1 python3 analysis/w33_k12_genus_polarization.py`. The certificate retains the basis, both alternating forms, both integral complex operators, the Darboux map and the genus comparison rows.

The rediscovery guard also flags broad Eisenstein/Heawood and Eisenstein/Szilassi combinations in `analysis/BT1707_BT1709_qubit_contextuality_hesse_bridge.md` and `analysis/w33_BREAKTHROUGH_289_triangle_group_hurwitz_tower.py`. Both were read in full: they address contextuality and Hurwitz counts, respectively, rather than the polarization matrices above. Their broad thematic connections are prior art. In particular the latter's printed identification of 84 with Császár/Szilassi edge counts is inconsistent with the 21-edge combinatorial count; this report uses the explicit count, without modifying the historical file. `w33_pass95_genus_mass.py` was also read fully: its genus is arithmetic lattice genus, not surface genus.

A subsequent full read of `analysis/w33_css_genus_percolation_hinge.py` identifies the likely source of that mismatch: it correctly records **84 flags**, not 84 edges, for each toroidal polyhedron. Each edge belongs to two faces and has two endpoints, giving four vertex-edge-face flags per edge: 4*21=84. Thus the 84 coincidence can be retained with its correct incidence type; it is not an edge-count identity. That script also relates the quadratic roots 3 and 4 to the repository's asymmetric CSS distances, while explicitly limiting the conclusion to arithmetic compatibility. It does not construct a surface/code equivalence.
