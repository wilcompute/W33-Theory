# Five executed genus-six directions

September 20, 2026. Producer: `analysis/w33_genus_six_execution.py`. Certificate: `analysis/w33_genus_six_execution.json`. These are finite mathematical constructions and specified dynamical models, not a physical TOE derivation.

## 1. A surface-period alternative exists, at a definite cost

The previous packet `W33_K12_GENUS_POLARIZATION.md` obstructed the **natural Eisenstein complex structure with its specified principal polarization** from being a smooth genus-six Jacobian. It did not obstruct changing complex structure.

We now use the smooth projective completion of **y²=x¹³−1**, a classical hyperelliptic curve of genus six. Tadokoro's Proposition 4.1 gives explicit cyclotomic A- and B-period matrices; the implementation forms tau=A^(-1)B and transports multiplication by i through the old integral Darboux marking T to the Coxeter–Todd lattice's underlying real vector space. The integral principal form E is retained.

The matrix is symmetric and its imaginary part is positive definite (minimum eigenvalue approximately 0.5135587815). Independently evaluated 50- and 80-digit results differ by 7.64e-50. The transported J satisfies J²=-1 and EJ symmetric positive definite numerically at the working precision. The curve and period formula are classical; this packet supplies the explicit marked transport and its checks. These high-precision checks are not interval-certified error bounds.

**The price is explicit:** the new J neither commutes with the old Eisenstein operator W nor preserves the original Coxeter–Todd metric G. Thus the old obstruction remains correct. We have a Jacobian structure on the same marked symplectic module, not a Jacobian realization of the unchanged metric and Eisenstein symmetry.

Source: [Tadokoro, arXiv:1211.6910, Proposition 4.1](https://arxiv.org/html/1211.6910). No conformal identification between the following triangulation and this particular curve is asserted.

## 2. Actual genus-six chains, not Euler counts alone

We import **manifold_2_12_4_5** from [Frank Lutz's triangulation catalogue](https://www3.math.tu-berlin.de/IfM/Nachrufe/Frank_Lutz/stellar/2_manifolds.txt). The source owns the 44-face triangulation. The independent audit checks all 66 edges twice, consistent orientation, a connected face dual, and a single cycle in every vertex link. It obtains (V,E,F)=(12,66,44), genus six and Betti numbers (1,12,1).

A primal spanning tree and disjoint dual spanning tree give a face-boundary elimination minor of determinant ±1. This proves the resulting twelve generators form an **integral** homology basis, not merely a rational or mod-3 basis. The certificate stores both boundary matrices, the homology projection, the Alexander–Whitney cup matrix, twelve symplectic cycle columns and an explicit **66×12 lattice-to-cycle map**. The pullback of the surface intersection form is exactly E. Adding any face boundary leaves the homology coordinates unchanged.

The earlier Reye 44-face pseudocomplex is deliberately rejected as a negative control. Its retraction in `w33_k12_singular_css_closure.py` remains in force; the new surface does not repair or silently reinterpret its face table. No straight-edged realization in R³ is claimed.

## 3. Topology-changing instructions with checked inverses

`HandleVM` implements ALLOCATE by connected sum with the catalogue's seven-vertex torus: remove one face from each surface and identify their boundaries with reversed orientation. Each instruction changes (V,E,F) by **(+4,+18,+12)** and genus by +1. This is a concrete simplicial operation, different from the fixed-vertex Jungerman–Ringel handle subtraction.

Three allocations produce genus 6→7→8→9. Three receipt-checked FREE operations recover the original face table exactly. FREE rejects changed topology and a live pair of handle coordinates, so it does not silently discard stored state. This is a classical topology/register prototype with in-memory receipts; durable storage, fault tolerance and universal computation are not established by these instructions alone.

## 4. Two oscillator models produce different responses

For the Heawood adjacency A, the same normalized middle-sector initial vector is propagated by both i psi-dot=A psi and x-double-dot=−(3I−A)x. The first model has frequency sqrt(2); the mechanical model has frequencies **sqrt(3−sqrt(2))** and **sqrt(3+sqrt(2))**, approximately 1.2592801267 and 2.1010029896.

Across 101 sample times from 0 to 20, numerical ODE integration differs from spectral evolution by at most 4.82e-11; mechanical energy drift is below 2.51e-10. The first-order formula agrees with direct matrix exponentials to 1.09e-14. `W33_GENUS_SIX_RESPONSE.svg` displays the two return amplitudes. Units and generator choices are declared; these are not measured hardware frequencies. The Heawood spectrum itself is prior work in `exploration/w33_heawood_harmonic_bridge.py`.

## 5. The two polarizations give different computation rules modulo 3

For primes 2,3,5,7 the Eisenstein alternating form E has rank twelve. The Gaussian form D=−GI has rank twelve except at 3, where its rank is **six**, with a six-dimensional radical. At p=3 these support, respectively, six quantum pairs and three quantum pairs plus six central label coordinates. Fixing a central character leaves irreducible register dimensions 3^6 and 3^3. This is a finite Heisenberg representation statement, not a physical identification of the E6 fundamental representation.

The central-extension multiplication is explicitly

    (u,a)(v,b) = (u+v, a+b+uᵀCv) mod p,
    C = strict upper triangular part of the alternating form.

Bilinearity proves associativity for all vectors; 13,824 basis-triple checks exercise the implementation. A chosen two-pair subspace embeds the existing two-qutrit Pauli labels into E mod 3; all **6,561 ordered label pairs** preserve the commutator phase. The embedding depends on a Darboux basis: it is not a canonical E8-to-K12 lattice map.

## September 20 intake and scope

GitKraken integrated W33 3fe34a872..0d1d014d6 (340 commits, 244 changed paths) and Holotrade bf78db7..d1fe6ce (166 changed paths). Existing local genus files and unrelated continuity/instruction edits were preserved. Earlier September 15 intake already read the E8 Pauli weld, support, grading and lift sources/reports and the frozen Wilson-line hinge result. The new E8/Pauli construction is prior-owned and supplies the phase-space convention used here.

The latest incoming physics work distinguishes label actions from physical parity, restores the full extra-U1 centralizer, and includes a further retraction of the claimed 55/87 doublet-triplet cancellation escape: Holotrade d1fe6ce identifies the co-localized states as components of the same local multiplet, invalidating the independent-coefficient premise. The reported locked-coefficient result is 0/87. This is the incoming audit's stated scope, not a new independent string-amplitude calculation here. Higher-order effects and F-flatness require separate work. The new `w33_e6_gauge_three_qutrit_pauli_firewall.py` also makes it essential not to turn a 27-dimensional register count into an E6 gauge-Pauli identification.

This packet does not claim sentence-level validation of every one of the hundreds of incoming files, nor completion of the older all-paper and 57-script semantic reading backlog. Intake and theorem certification remain distinct.

Reproduce with `OPENBLAS_NUM_THREADS=1 python3 analysis/w33_genus_six_execution.py`; focused regressions are in `tests/test_genus_six_execution.py`.

## September 20 validation and parallel-update boundary

All three focused regression functions pass both directly and under isolated pytest (3 passed in 45.99 seconds): full certificate replay, boundary/basis invariance, and corrupt-surface/invalid-FREE rejection. The plot was successfully rendered with a temporary Matplotlib environment. The rediscovery guard flags broad E6/Heawood and Eisenstein/Heawood combinations: prior `BT1788_hesse_relation_materializer.md`, `BT1707_BT1709_qubit_contextuality_hesse_bridge.md` and `MARCELIS_DEEP_CRAWL_2026_09_09.md` were read in full. Their CSP, contextuality and atlas claims are prior work; this packet does not claim those topic combinations as new. `W33_FOR_EVERYONE.tex` was also flagged but was not fully reread for this packet.

The fixed-range cross-repository intake manifest covers 410 changed paths by hashes and Python/JSON structural checks, with targeted semantic reading. It is not a claim that every incoming proof was reread. Two subsequent W33 commits, b81856277 and 3464454d3, revise the doublet-triplet paper row and refresh the numerical-formula universe. The row uses stronger coefficient-locking language than the Holotrade producer's explicit residual scope; local Clebsch factors and actual singlet representations remain uncomputed. Holotrade's companion `LOCAL_NINE_SPURION_ALGEBRA.md` supplies a one-flagship exact nine-weight replay and a conditional 17-dimensional spurion algebra, not a general string-theory no-go.
