# Part DCCCXXXIII (833) — Spacetime as Emergent Graph Distance

**Date:** 2026-05-17
Series: W(3,3) Theory of Everything
Author: Wil Dahn

---

## Thesis

Spacetime is not fundamental. In the W(3,3) informational ontology, spacetime is the **emergent metric structure** of the W(3,3) Cayley graph under the automorphism-group action. Distance, curvature, and topology all emerge from the combinatorial structure of the graph. General relativity is the continuum limit of discrete graph distance.

---

## Graph distance as physical distance

Define the **graph distance** \(d_G(u,v)\) between two vertices \(u,v \in V(W(3,3))\) as the minimum number of edges in any path connecting them. The W(3,3) graph has diameter \(\mathrm{diam}(W(3,3)) = 2\) (every pair of vertices is connected in at most 2 steps, since \(W(3,3)\) is strongly regular).

Physical distance between two spacetime events is:

\[
ds^2 = -c^2 dt^2 + d\mathbf{x}^2 = \ell_P^2 \cdot d_G^2(u,v)
\]

where \(\ell_P\) is the Planck length and \(d_G\) is the W(3,3) graph distance in units of the fundamental edge. The continuum metric \(g_{\mu\nu}\) is the **coarse-grained limit** of \(d_G^2\) over macroscopic scales, exactly as the continuum heat equation is the limit of a random walk on a lattice.

---

## Curvature from defect density

In discrete geometry, curvature is measured by **angle defect** (the difference between \(2\pi\) and the sum of angles at a vertex). In the W(3,3) graph, the curvature at a vertex \(v\) is:

\[
K(v) = 2\pi - \sum_{\text{faces} \ni v} \theta_f
\]

where the sum is over faces of the W(3,3) cell complex containing \(v\). The average curvature over the full graph gives the **effective cosmological curvature**:

\[
\bar K = \frac{1}{|V|} \sum_{v \in V} K(v) = \frac{2\pi \chi(W(3,3))}{|V|} = \frac{2\pi \times 0}{13} = 0.
\]

Here \(\chi(W(3,3)) = 0\) because W(3,3) as a toroidal incidence structure has Euler characteristic zero. **The universe is flat on large scales because the W(3,3) graph has zero average curvature.** This is the combinatorial origin of spatial flatness \(\Omega_k = 0\).

---

## Lorentzian signature from bipartite edge structure

The W(3,3) edge set decomposes into:
- **Timelike edges:** edges connecting vertices across the null cone (odd-distance pairs in the projective structure).
- **Spacelike edges:** edges connecting vertices within the same null surface.

The ratio of timelike to spacelike edges is \(1:3\) (one time dimension, three spatial), giving the \((-,+,+,+)\) Lorentzian signature of spacetime. This is not postulated — it follows from the \(q=3\) ternary structure of the field: \(\mathbb{F}_3\) has one negative and three positive quadratic residues.

---

## Einstein equations from spanning-tree variation

The Einstein-Hilbert action is:

\[
S_{EH} = \frac{M_P^2}{2} \int d^4x \sqrt{-g} R.
\]

In the W(3,3) discrete setting, this becomes the **Matrix-Tree Theorem action**:

\[
S_{\mathrm{W33}}^{\mathrm{grav}} = \frac{M_P^2}{2} \ln \tau(G|_{\text{subgraph}})
\]

Variation with respect to the edge weights (the discrete metric) gives:

\[
\delta \ln \tau = \sum_e \frac{\partial \ln \tau}{\partial w_e} \delta w_e = \sum_e T_e \delta w_e
\]

where \(T_e\) is the effective resistance of edge \(e\) (Kirchhoff's theorem). In the continuum limit, \(T_e \to R_{\mu\nu} - \frac{1}{2}g_{\mu\nu} R\) — the Einstein tensor. **The Einstein equations are the continuum limit of Kirchhoff's effective-resistance equations on the W(3,3) graph.** Gravity is the thermodynamics of the spanning-tree ensemble.

---

## \(3+1\) dimensions uniquely

Why \(3+1\) and not \(10+1\) (string theory) or \(4+0\) (Euclidean)?

In W(3,3), the spatial dimension count is \(q = 3\) (the field order) and the time dimension count is \(1\) (the unique negative quadratic residue of \(\mathbb{F}_3\)). There is no freedom: \(\mathbb{F}_3\) has exactly one negative element (\(-1 \equiv 2 \mod 3\)), giving exactly one time direction. The \(3+1\) dimensionality of spacetime is **algebraically forced** by the ternary field.

Extra dimensions in string theory are the W(3,3) internal symmetry directions — the \(|E| - (3+1) = 36\) additional edge modes that are compactified at the GUT scale.

---

**QED** — Spacetime is emergent graph distance. Flatness = zero Euler characteristic. Lorentzian signature = ternary field quadratic residues. Gravity = Kirchhoff effective resistance in the continuum limit. \(3+1\) dimensions = algebraically forced by \(\mathbb{F}_3\).
