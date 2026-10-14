# TOE77 synthesis — W33 embedding overturns local 120° flux, and a genuine \(H_{27}\rtimes D_8\) symmetry acts on 27 native octagons

**Date:** 14 October 2026. **Status:** the individual certificates and GitHub Actions workflows linked below passed. **Category:** exact finite graph/group mathematics and numerical model-fermion results, **not** a proof of physical unification, classical RH, or experimentally observed chirality.

## Research trail and independent controls

Read source/proofs from the W33 graph-RH manuscript \`manuscripts/tex/part27_graph_rh_theorem.tex\`, \`analysis/w33_ihara_zeta.py\`, the irregular Bass correction \`analysis/w33_pass3080_3082_bass_regular_audit.py\`, the 80-vertex Levi source \`w33_pass74_zeta_frontier.py\`, the TOE73–76 theta/flux, 27-cover orbit, chirality and gauge files, and current parallel commits. Relevant established graph-zeta mathematics: Kotani–Sunada (2000) and the weighted Ihara/Hashimoto/Bass determinant literature. The regular graph RH for W33's degree-12 collinearity graph and degree-four incidence graph remains distinct from the *irregular* 11-vertex theta and does **not** imply classical RH.

The original isolated 11-site \(\Theta(4,4,4)\) graph has a rigorously derived free five-fermion ground optimum at \(s=|1+e^{i\phi_1}+e^{i\phi_2}|=0\), precisely the two conjugate 120° phase pairs. Its unitary-twisted Ihara determinant depends on the **same** \(s\). Since this is true of **every** uniform equal-arm theta graph, it is not W33-specific without information from its 80-vertex embedding.

## Exact theorem 1 — W33-incidence flat-band obstruction and spectral nuclear norm

The native 80-vertex W33 Levi graph is bipartite with a \(40\times40\) point-line incidence block \(M\). Its untwisted singular values are \(4^1,(\sqrt6)^{24},0^{15}\). Thus the exact **half-filled 40-fermion ground energy** is
\[
E_0=-\|M\|_* =-(4+24\sqrt6).
\]
This follows from the bipartite Hamiltonian's singular-value pairs \(\pm\sigma_i(M)\). Introducing complex unit-modulus holonomies on only **two existing chord edges** changes at most two entries of \(M\), so \(\mathrm{rank}(M_\phi)\le27\) and the full Hermitian 80-state one-particle hopping Hamiltonian retains **at least 26 exact zero modes** for all such fluxes. At least fifteen independent entry perturbations are *necessary* to remove the simple rank-protected lower bound (not sufficient). The sublattice index is zero, so this is NOT a chiral Standard Model zero-mode theorem.

The nuclear-norm triangle inequality supplies an independently checkable all-phase bound \(|E_\phi-E_0|\le|e^{i\phi_1}-1|+|e^{i\phi_2}-1|\le4\) for the fully coupled W33 graph.

**Producer:** \`analysis/w33_20261014_toe77_nuclear_norm_transition.py\`.

## Verified numerical experiment 2 — the W33 exterior moves the flux optimum

Preserve unit weight on the 12 native theta edges, multiply all **other 148 native W33 Levi edge hoppings** by a common exterior amplitude \(t\). At \(t=0\), the remaining 69 vertices are isolated, reproducing the exact theta 120° theorem. At \(t=1\), the entire W33 Levi graph is restored, with two selected theta chords carrying magnetic phases. At half filling, the verified 80×80 direct spectral calculations give
\[
E_{120}-E_{\pi,\pi}=
\begin{cases}
-0.0206931704210,&t=0,\\
-0.0154690506454,&t=1/4,\\
-0.0063616117564,&t=1/2,\\
+0.0182225316338,&t=1.
\end{cases}
\]
There is an approximate **fixed-background equality** at \(t\approx0.6393317238\). This is NOT a thermodynamic phase transition; the continuously optimized phase moves smoothly along \((\pi+\delta,\pi-\delta)\), from \(\delta/\pi=1/3\) at \(t=0\) toward numerically zero at \(t=1\). The value \(t\approx0.9999909\) from finite-difference \((\pi,\pi)\) curvature is sensitive to small flat-band scales and should not be treated as an exact critical point.

**Conclusion:** 120° is an exact optimum **only for the isolated free theta graph**. Coupling to the actual 69-vertex W33 exterior changes its matter energetics and numerically favors the \((\pi,\pi)\) sector at the fully restored point. These are *static noninteracting finite-lattice* calculations with arbitrarily chosen two-chord magnetic background, not a dynamical 4D gauge vacuum.

**Independent 80-site CI:** https://github.com/wilcompute/W33-Theory/actions/runs/38643924681. **Nuclear-norm CI:** https://github.com/wilcompute/W33-Theory/actions/runs/38644376858.

## Exact theorem 3 — W33 octave/Ihara geodesics produce the first full magnetic response

Girth eight of the W33 Levi graph ensures that all closed-walk phase dependence first appears at power eight. Each undirected eight-cycle contributes two orientations and eight basepoints, i.e. 16 terms, so for two selected chord holonomies,
\[
\boxed{\mathrm{tr}[H_{\phi,t}^8]-\mathrm{tr}[H_{0,t}^8]
=16\sum_{C\in\mathrm{Octagons}(W33)}
t^{d_C}\bigl(\cos(w_C\cdot\phi)-1\bigr).}
\]
The source explicitly enumerates all **1620 native octagons**, the winding pair \(w_C\), and the number \(d_C\) of edges outside the theta motif. Nine independent direct 80-eigenvalue trace checks verified the formula. Of 1620 octagons, precisely **135** carry nonzero winding around at least one of the two selected chord edges.

This is an embedding-sensitive mathematical bridge from finite Ihara/prime-geodesic counting to a quantum-walk spectral response. It is **not** an equivalence with Riemann's classical zeta function.

## Exact theorem 4 — 27 common octagons carry a genuine Heisenberg group action

Every W33 Levi **flag edge** belongs to 81 undirected primitive octagons. The two particular theta chords occur together in **27** octagons, so their union comprises \(81+81-27=135\) holonomy-sensitive octagons. The number 27 suggested, but did not prove, a connection to the existing regular/Payne and trinification \(H_{27}\) program.

The explicit PGSp(4,3) stabilizer audit \`analysis/w33_20261014_toe77_twentyseven_octagons.py\` shows that the **unordered two-chord flag-pair orbit** has size **240**. Since \(|PGSp(4,3)|=51840\), the pair stabilizer has order **216**. It acts **transitively and faithfully** on those 27 shared octagons, with point stabilizer of order **8**.

The follow-up \`analysis/w33_20261014_toe77_H27_shared_octagon_group.py\` computes actual induced permutations, generates all 216 elements, and exhibits a **normal, regular 27-element subgroup** whose center has order three and whose remaining 26 elements all have order three. It is nonabelian. By the classification of groups of order 27 this is exactly the exponent-three extraspecial **Heisenberg group \(H_{27}\)**. For a selected base octagon \(C_0\), the map \(h\mapsto h(C_0)\) therefore gives a canonical (up to choice of origin) H27 *address coordinate system* on the 27 shared cycles.

This is a **genuine equivariant construction** rather than numerology based on matching 27.

## Exact theorem 5 — the surrounding order-216 group is \(H_{27}\rtimes D_8\), NOT a guessed Clifford 216

The induced action has an **actual order-eight subgroup disjoint from the normal H27**; the two subgroups multiply to the full 216 elements. The order-eight subgroup has element-order histogram \(1^1,2^5,4^2\), identifying the **dihedral group \(D_8\)** rather than quaternion \(Q_8\). Therefore
\[
\boxed{\mathrm{Stab}_{PGSp(4,3)}(\{\text{two chord flags}\})\cong H_{27}\rtimes D_8.}
\]

The group center has order **one**. The eight nonzero classes of \(H_{27}/Z(H_{27})\cong\mathbb F_3^2\) split into exactly **two \(D_8\)-orbits of size four**. Inverting the central order-three phase is a nontrivial outer part of the D8 action: since the center of the complete group is trivial, the D8 action on the order-three center cannot be entirely trivial.

**Critical operator-algebra boundary:** fixing a qutrit Schrödinger representation with central \(z\mapsto\omega I\), no *complex-linear unitary conjugation* can send the scalar \(\omega I\) to \(\omega^{-1}I\). Such a center-flipping automorphism requires an antiunitary/complex-conjugation operation or a change of central-character sector. This is a concrete mathematical place to explore chirality/time reversal, but it is NOT a demonstration of Standard Model CP violation. Likewise, **equal order 216 does not identify this group with the usual projective single-qutrit Clifford group** \(3^2\rtimes SL(2,3)\): compare their normal p-subgroups and representation actions before asserting any isomorphism.

**Verified CI:** https://github.com/wilcompute/W33-Theory/actions/runs/38645794430 — 3/3 group-structure tests passed; previous independent group generators/checks also passed.

## What is genuinely new versus unproved

**New exact finite results:** true H27 regular action on 27 octagons, full 216-element stabilizer structure H27 by D8, the 26 protected W33 zero-mode lower bound, the all-1620-octagon magnetic trace identity, and the nuclear-norm half-filled energy bridge. **New finite numerical result:** embedding-induced reversal of the isolated 120° preference and continuous migration toward π,π.

**Unproved:** mapping these octagons to 27 cubic-surface lines or E6 27 weight vectors; identifying this order-216 group with the machine's chosen Clifford 216; deriving a nonzero 4D chiral overlap index with anomaly cancellation; proving a positive infinite-rotor gap; experimental evidence; and any complete Theory of Everything.

## Five independent strongest next steps

1. **Construct the equivariant map to E6.** Compare the actual H27 multiplication/action on 27 W33 shared octagons against the regular/Payne H27 action on cubic-surface objects and the trinification central-character representation. Either exhibit an explicit intertwiner preserving incidence and commutators, or produce an obstruction certificate.

2. **Realize the center-inverting D8 gates.** Construct explicit 3×3 qutrit unitary/antiunitary matrices for the H27 by D8 action. Determine which D8 generators require conjugation, what phases they impose on chirality, and whether photonic OAM/time-bin hardware can test them.

3. **Prove embedding-dependent flux minimizers.** Interval-certify the 80-site nuclear-norm phase minimum over U(1)², derive the flux-current susceptibilities from all 1620 octagon Fourier coefficients, and compare multiple inequivalent two-chord pairs—not only the one theta motif.

4. **Build the 27-orbit quantum pairing representation theory.** Test whether this explicit 27-cycle H27 address action extends equivariantly to the separate 27 known PGSp ground-cover orbits and their 41-transition seed graph; do not identify them solely because the number 27 recurs.

5. **Cross the actual physical threshold.** Construct a local 4D anomaly-checked spin/overlap Dirac lattice and establish verified ordered eigenvalue lower bounds for the unbounded gauge rotor; match finite-model holonomy signatures to real optical controls before any fundamental-physics claims.

The classical Riemann hypothesis and experimentally validated Theory of Everything both remain unsolved.
