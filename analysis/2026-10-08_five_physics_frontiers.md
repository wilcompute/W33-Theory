# Five TOE frontiers: operational, constraint, chirality, vacuum and normalization probes (2026-10-08)

**Status: executed exact finite checks and necessary-condition filters, not a complete physical theory.** Producer `analysis/w33_20261008_five_physics_frontiers.py`; certificate `data/w33_20261008_five_physics_frontiers.json`; regression `tests/test_w33_20261008_five_physics_frontiers.py`.

## Prior ownership and why these are not recycled breakthroughs

- September 24 `w33_20260924_history_pointline_cospectral_firewall.py` first proved the two W33 27-state carrier graphs cospectral but nonisomorphic. October 8 `w33_20261008_dual_27_electrical_transport.py` identified different exact effective resistance profiles.
- Pass10952 showed an antiunitary odd clock is not a standalone CPTP qutrit channel; Pass11038 showed that raw off-Bell Weyl basis elements are not CP channels. This packet **does not** rehabilitate those operations; it constructs a different, explicitly classicalized channel.
- Pass11675 built true SU(2) graph Gauss constraints but expressly **not** Hamiltonian/diffeomorphism constraints; Pass11639 documented additional lapse/metric obstructions.
- Pass11697/11698 first established the 320 chiral stabilizer-vacuum pairs, with no sign selection. This packet rechecks the counting and tests its boundary against a separate familiar anomaly constraint.
- Pass11742–11757 contain real string/model, gauge, Higgs and normalization no-go tests. This packet checks a deliberately weaker, model-independent abelian necessary condition, not their exhaustive spectra or worldsheet calculations.
- The PDF `papers/forty_points/main.pdf`, sections 9–11, openly leaves dynamics, chirality, a viable string vacuum, gravity and masses unresolved. The five tests do **not** change that status.

## I. Constructive CPTP transport on both 27-state carriers

For each of the two W33-induced 8-regular 27-vertex graphs, define directed-edge Kraus operators

\[
K_{j\leftarrow i}=\frac{|j\rangle\langle i|}{\sqrt8}
\quad(i\sim j).
\]

There are 216 directed edges, so `sum K^dag K=I` exactly. The Choi operator is diagonal in the vectorized matrix-unit basis: 216 positive eigenvalues of `1/8` and 513 zero eigenvalues. Therefore each map is CPTP and entanglement-breaking, with minimum environment dimension 216 for a single-step Stinespring isometry for this exact map. The channel measures its input in the vertex basis and prepares a neighboring vertex uniformly; it is **not** a coherent unitary W33 gate, and the 27-dimensional vertex system is not automatically one physical qutrit.

For diagonal input and output, two steps have probability matrix `A^2/64`. Exhaustive exact histogram for 702 **ordered distinct** pairs:

| Number of length-2 walks | Opposite W33 point carrier | Transverse null-line carrier |
|---|---:|---:|
| 0 | 54 | 0 |
| 1 | 216 | 216 |
| 2 | 0 | 324 |
| 3 | 432 | 0 |
| 4 | 0 | 162 |

The total row count is 64 (including the 8 two-step returns). Thus in an engineered 27-level measure-and-prepare device, 54 ordered point-carrier pairs have strictly zero two-step transition probability while **all** off-diagonal line-carrier pairs have positive two-step probability. This is a much closer operational discriminator than spectra or resistance alone. A real instrument design, error budget, finite-shot decision theory and physical encoding remain open.

**External anchor:** Pollock et al., [Operational Markov condition for quantum processes](https://arxiv.org/abs/1801.09811). Operational interventions and reference systems matter; a channel demonstration is not evidence that the proposed temporal ontology is correct.

## II. A local-current closure obstruction on the actual W33 Levi graph

The actual point-line Levi graph reconstructed here has 80 vertices, 160 edges and degree four at every vertex. At each oriented edge `i -> j` define a canonical scalar edge current

\[
J_{ij}=(p_i+p_j)(q_i-q_j),\quad\{q_i,p_j\}=\delta_{ij}.
\]

For a two-edge path `i-j-k`, exact symbolic differentiation gives

\[
\{J_{ij},J_{jk}\}
=p_i(q_k-q_j)+p_j(q_k-q_i)+p_k(q_j-q_i).
\]

In particular the bracket contains `p_i q_k-p_k q_i`. In a bipartite Levi graph, `i` and `k` are not nearest neighbors; no linear combination of nearest-edge current generators contains either such monomial. All 480 centered two-edge wedges have this support defect. **Therefore this naive strictly edge-local current ansatz does not form a closed Poisson algebra**; any attempt to use it as a diffeomorphism current must introduce more generators, nonlocal structure, or change the ansatz.

This is *not* a no-go theorem for all discretizations of GR: Bonzom–Dittrich constructed discrete Dirac algebras in special gravitational sectors. Nor does this disprove the repository's valid graph SU(2) Gauss closure. It shows precisely why the latter cannot be promoted to 4D gravity by nomenclature.

**External anchors:** [Bonzom–Dittrich 2013](https://arxiv.org/abs/1304.5983); [Discrete approaches to quantum gravity in four dimensions](https://pmc.ncbi.nlm.nih.gov/articles/PMC5253799/).

## III. Chirality and anomaly compatibility: orthogonal constraints

The 40 W33 isotropic lines each have 8 nonzero characters of their underlying \(\mathbb F_3^2\). Each of four projective kernel directions receives exactly two opposite nonzero characters. Hence the known even quartic potential's 320 line-character vacua come in exactly 160 conjugate-sign pairs. **The even potential does not select the observed sign.** A sign-biased term would be a new physical input unless derived from a previously specified independent sector.

For an *independent* Standard Model family of left-handed Weyl multiplets \(Q,U^c,D^c,L,E^c,N^c\), we checked exact rational hypercharges and \(B-L\): all of \(SU(3)^2Y,SU(2)^2Y,\mathrm{grav}^2Y,Y^3,\mathrm{grav}^2(B-L),(B-L)^3\) vanish with \(N^c\). Removing \(N^c\) while holding the other representations fixed makes the last two anomalies exactly \(-1\) per generation in the selected normalization. The point is the tension, not a paradox: under the minimal anomaly-free gauged \(B-L\) field content, the same \(N^c\) that cancels anomalies carries odd matter parity and breaks it if it condenses.

This does not rule out different anomaly-cancelling fermion contents and does not equate W33 stabilizer parity with a continuum chiral gauge representation.

**External anchors:** [Heeck, Unbroken B-L symmetry](https://doi.org/10.1016/j.physletb.2014.10.067); [Lee, CP nonconservation and spontaneous symmetry breaking](https://doi.org/10.1016/0370-1573(74)90020-9).

## IV. String-vacuum safety: two logically independent operator filters

With conventional rational \(Y\) and \(B-L\) assignments, and matter parity \((-1)^{3(B-L)}\), the following *necessary* abelian invariance statements hold:

- \(U^cD^cD^c, QLD^c, LLE^c\): \(Y=0\), \(B-L=-1\), matter parity odd.
- Multiply any by \(N^c\): \(Y=B-L=0\), matter parity **even**. A nonzero \(\langle N^c\rangle\) can therefore permit the three familiar renormalizable RPV terms if the corresponding higher couplings are allowed.
- \(QQQL\) and \(U^cU^cD^cE^c\): already \(Y=B-L=0\) and matter parity even, *without* any \(N^c\) insertion. Thus an intact matter parity alone does not guarantee the absence of dimension-five proton-decay operators.

Nonabelian \(SU(3)\times SU(2)\) contractions and nonzero holomorphic monomials require suitable generation indices; repeated identical superfields may make antisymmetric contractions vanish. These necessary charge filters are **not** sufficient in any particular heterotic compactification: worldsheet instanton, space-group, revised rotation/R and other string selection rules must be independently checked. This pass does not override the repository's exhaustive nine-family negative result or prove any particular RPV term actually exists there.

**External anchors:** [Kobayashi et al., Revisiting Coupling Selection Rules](https://arxiv.org/abs/1107.2137); [Nilles et al., discrete R symmetries with Wilson lines](https://doi.org/10.1016/j.physletb.2013.09.041).

## V. Normalization and spectrum: two ways that geometry cannot fix masses

Both 27-state carriers have \(L=8I-A\) spectrum \(0^1,6^{12},9^8,12^6\). For the *supplied* quadratic toy action

\[
\mathcal L=\frac Z2\dot q^T\dot q
-\frac12q^T(aI+bL)q,
\qquad
\omega_\lambda^2=(a+b\lambda)/Z,
\]

take \(a=3,b=2,Z=5\). The four squared frequencies are \(3/5,3,21/5,27/5\). The conditional ratio \((\omega_{12}^2-\omega_0^2)/(\omega_6^2-\omega_0^2)=2\) follows from the graph, but its physical realization does not.

Two independent failures of parameter determination are explicit:

1. \((a,b,Z)\mapsto(7a,7b,7Z)\) leaves every \(\omega^2\) unchanged; it is an overall action normalization redundancy.
2. \((a,b,Z)\mapsto(7a,7b,Z)\) multiplies every squared frequency by 7 and changes the predicted absolute excitation scale **without changing either graph**.

Moreover both graphs have the same mode frequencies but different pairwise transport behavior (Part I). A physical prediction requires the field content, kinetic/Kähler metric, renormalized parameters, matching scale and observable map, not just combinatorial eigenvalues.

**External anchors:** [Blesneag–Buchbinder–Candelas–Lukas, holomorphic Yukawas](https://arxiv.org/abs/1512.05322), [SMEFT review, matching and running](https://doi.org/10.1103/RevModPhys.96.015006).

## Acceptance rules for future TOE claims

1. A claimed quantum tick or transport operation must have a CPTP Choi certificate, a physical degree-of-freedom encoding and a reference-system test.
2. A claimed gravity theory must supply Hamiltonian and spatial-diffeomorphism constraints whose **full** Poisson brackets close, including phase-space-dependent structure functions; SU(2) Gauss constraints are a different algebra.
3. A chirality claim must select the sign from specified action/boundary conditions and survive gauge and gravitational anomaly checks.
4. A proton-stability claim must check both VEV-induced dimension-four RPV and direct dimension-five operators, with actual string selection rules and a model-specific massless spectrum.
5. A claimed mass/coupling prediction must be insensitive to unphysical field basis while explicitly specifying the physical kinetic normalization, matching, thresholds and uncertainties.

Nothing here completes the TOE; the packet isolates what a physically testable completion would need, building on rather than overwriting previous certificates.
