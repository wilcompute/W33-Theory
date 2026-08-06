# Passes 3973–3980 — extremal code, active-mixer compiler, photon competing-model experiment, rank-48 tensor, and Monster gate

## Exact status

```text
PASS_EXACT_FIVE_FRONT_THREE_BONKERS_MONSTER_EXTERNAL_AND_PHOTON_LAB_PENDING
03c37b821bb9b6f875a8bd4edde8dc96fe36a43d6d8dc24144d8dbd5e3aa5104
```

The content-addressed verifier reconstructs the six-bit minus-type quadratic space, all 945 admissible weight-four extensions, the order-51,840 coordinate group, two exact maximum-clique searches, both multiport factorizations, all 200 exact covers, all 48 orbitals, and all 904 nonzero intersection constants. The compressed certificate and literal tensor are independently hashed and replayed by `analysis/w33_pass3973_3980_check.py`.

## Pass 3973 — global extremality of the 57-word stratum

Let `C=[36,6,16]` be the binary character code on the 36 nonsingular vectors of the six-dimensional minus-type quadratic space. There are exactly 945 weight-four words in `C^⊥`. Join two when their supports meet in even cardinality, equivalently when they can coexist in a doubly-even self-orthogonal extension of `C`.

The resulting 945-vertex compatibility graph is regular of degree 624. The exact `O_6^-(2)≅U_4(2):2` action splits its vertices into two orbits:

\[
\boxed{945=135+810}.
\]

A deterministic colored-bitset branch-and-bound proves:

\[
\omega(\Gamma[135])=15,
\qquad
\omega(\Gamma[810])=54.
\]

For the second equality, transitivity reduces the calculation to one fixed vertex and its neighborhood. Any clique meeting the 135-orbit may likewise be moved to contain one fixed representative; exact search of that neighborhood gives 57. Therefore

\[
\boxed{A_4\le57}.
\]

The previously constructed 57-word clique attains the bound, so it is globally extremal among doubly-even self-orthogonal extensions containing the fixed parent code. Its span is

\[
\boxed{D=[36,17,4]}
\]

with weight enumerator

\[
\begin{aligned}
W_D(z)={}&1+57z^4+852z^8+7332z^{12}+57294z^{16}\\
&+57294z^{20}+7332z^{24}+852z^{28}+57z^{32}+z^{36}.
\end{aligned}
\]

The proof is genuinely geometric: ordinary MacWilliams nonnegativity permits larger formal values of `A4`, so the bound does not follow from the one-parameter weight enumerator alone.

The intersection-two graph on the 57 extremal words decomposes as

\[
\boxed{\operatorname{SRG}(45,16,8,4)\sqcup K_{2,2,2}\sqcup K_{2,2,2}}.
\]

The coordinate-degree profile is

\[
\boxed{9^{20},3^{16}}.
\]

Uniqueness and a complete orbit census of maximum codes remain open.

## Pass 3974 — exact active-mixer optimization

For the 36-port involution

\[
H=(2A_{36}-J)/6,
\]

the prior exact adjacent compiler used 398 factors in 69 layers. Its exact accounting is

\[
398=302\text{ genuine mixers}+96\text{ signed swaps}.
\]

Allowing distinct input and output port orders produces a second exact radical factorization:

\[
\boxed{401=296\text{ genuine mixers}+105\text{ signed swaps}}
\]

in the same 69 layers. Every intermediate entry remains a one-radical rational multiple, the final off-diagonal residual is exactly zero, and the terminal diagonal is `+I`. The parameter digest is

```text
7aa8934af6206f213f4ef02659d754b1cab3f2c6089e8433129df3fe7cd054d9
```

Thus six active mixing elements are removed if signed swaps can be virtualized into static routing or port relabeling. This is not a reduction in total nearest-neighbor factors: 401 exceeds 398. No physical-free-swap assumption is hidden.

For the original common port order, every adjacent gate crossing a cut changes the corresponding off-diagonal transfer block by rank at most one. The exact cut ranks are

\[
1,2,3,4,5,6,7,7,8,9,10,9,10,10,11,10,11,10,11,
10,10,10,10,9,9,8,8,7,7,6,5,4,3,2,1,
\]

so every factorization respecting that order needs at least

\[
\boxed{253}
\]

adjacent two-mode factors. This strengthens the prior connectedness lower bound 35, but it is a fixed-order bound rather than a global ordering optimum.

## Pass 3975 — photon idea as a six-model experiment

The photon hypothesis is no longer represented by one preferred ontology. The packet freezes six competing models.

### P0 — invariant-front direct sum

`M` distinguishable modes of one photon provide an ideal alphabet of `log2(M)` bits. The causal front remains `c`.

### P1 — transverse-structure axial delay

In a paraxial benchmark,

\[
\Delta t\simeq\frac{L\langle k_\perp^2\rangle}{2ck^2}.
\]

Internal spatial structure can therefore change axial group delay without changing the invariant local propagation speed. Giovannini et al. measured arrival-time changes of spatially structured single photons in free space (arXiv:1411.3987), and Roger et al. used Hong–Ou–Mandel timing to study OAM-dependent delay (arXiv:1711.05582).

### P2 — hidden-node variable-speed model

A literal node-count mechanism predicts a residual arrival-time shift when the mode count changes while spectrum, path length, and transverse-momentum distribution remain fixed. That is a sharp null test. A pulse-peak delay alone is not a measurement of a changed causal front.

### P3 — W33 graph-kinetic model

If an engineered 40-mode transverse kinetic operator is proportional to the W33 Laplacian

\[
L_{W33}=12I-A,
\]

its exact spectral sectors are

\[
\boxed{0,10,16}.
\]

The declared experiment predicts three relative delay plateaus in the ratio

\[
\boxed{0:10:16}
\]

under that hardware mapping. This is a proposed device model, not established vacuum physics.

### P4 — hyperentangled tensor model

Independent degrees of freedom multiply dimensions. Forty spatial modes have dimension 40, while independent path, polarization, time-bin, frequency, and OAM factors may realize a product dimension. Forty independent qutrit factors would require dimension `3^40`; it is not implied by forty labels in one mode space. Temporal modes form a high-dimensional orthogonal framework for photonic information processing (Brecht et al., arXiv:1504.06251), and frequency-bin encodings provide another scalable mode basis (Lukens and Lougovski, arXiv:1612.03131).

### P5 — self-similar coupling model

Matching internal and external symmetry may improve mode sorting, selection rules, coupling efficiency, and crosstalk while leaving vacuum `c` invariant. This is the most conservative form of the self-similarity intuition.

### Three-axis protocol

1. **Isodelay mode-count sweep:** vary `M=1,4,16,40` while fixing spectrum, path, detector, and `⟨k_perp²⟩`; jointly measure accessible information and arrival-time residual.
2. **Isoalphabet structure sweep:** hold `M` fixed and vary `⟨k_perp²⟩`; P1 predicts the paraxial linear delay law.
3. **W33 spectral sweep:** prepare the `0,10,16` graph-Laplacian sectors and test the engineered `0:10:16` plateau prediction.
4. **Factorization sweep:** compare 40 spatial modes, `20×2` path–polarization modes, and `10×2×2` path–polarization–time modes at equal total dimension.
5. **Front/peak firewall:** separately estimate causal-front arrival and pulse-peak/group delay.

For a declared Gaussian timing benchmark, two equal independent conditions require approximately

\[
N\ge2(z\sigma_t/\delta t)^2.
\]

At the illustrative values `z=5`, `σt=20 ps`, and `δt=1 ps`, this is 20,000 events. These are planning coefficients, not measured apparatus performance.

## Pass 3976 — literal 48-relation coherent tensor

The verifier reconstructs:

- 27 nonzero singular vectors;
- 36 nonsingular vectors;
- 45 maximal singular lines;
- all 200 exact nine-line covers of the singular set;
- the exact cover split `160+40`;
- the combined five fibers

\[
\boxed{1\mid27\mid36\mid40\mid160}.
\]

The simultaneous `O_6^-(2)` action has exactly 48 orbitals. Their source/target relation-count matrix is

\[
\boxed{
\begin{pmatrix}
1&1&1&1&1\\
1&3&2&1&1\\
1&2&3&1&2\\
1&1&1&3&4\\
1&1&2&4&8
\end{pmatrix}.}
\]

Every intersection constant is materialized. Exactly

\[
\boxed{904}
\]

of the `48^3=110,592` tensor positions are nonzero, giving sparse compression factor

\[
\boxed{122.3362831858\ldots}.
\]

The canonical tensor digest is

```text
a17a375552c102d281e3ba79b602b67aa54a426fd68b1878293763ea65395ff9
```

This upgrades the earlier rank-48 statement and Wedderburn decomposition

\[
\mathbb Q^2\oplus M_2(\mathbb Q)^3\oplus M_3(\mathbb Q)\oplus M_5(\mathbb Q)
\]

to a literal orbital basis and complete multiplication tensor. Fusion schemes remain open.

## Pass 3977 — external Monster gate remains fail-closed

The exact internal queue contains 51,840 ordered standard pairs in two centralizer orbits of 576. The repository's strict `mmgroup` harness requires four portable serialized Monster words and checks the full order-25,920 closure, pair/triple signatures, element-order census, and all object hashes.

No such words or executed class-fusion artifact are present, and `mmgroup` is unavailable in the current local runtime. Therefore

```text
PENDING_EXPLICIT_MM_WORDS_AND_CLASS_FUSION
```

is the only promoted result. The `mmgroup` project provides explicit Monster arithmetic and long-term element representations, and recent work has published reproducible `mmgroup` generators for maximal Monster subgroups (Dietrich–Lee–Pisani–Popiel, arXiv:2411.12230). Those resources do not themselves supply the required U4(2) words for this packet.

# Three bonkers constructions

## Pass 3978 — the extremal code has an order-192 stabilizer

The coordinate stabilizer of the chosen extremal 57-word code has order

\[
\boxed{192}
\]

and element-order census

\[
\boxed{1^1\,2^{59}\,3^8\,4^{68}\,6^{40}\,12^{16}}.
\]

Together with the `45+6+6` geometry, this is a new exact order-192 barcode. The project already contains other appearances of 192, including the integral triple-incidence cokernel and tomotope flag count. Equality of orders is not an objectwise identification; this packet records a concrete comparison target rather than declaring the groups identical.

## Pass 3979 — W33 delay spectroscopy

The exact graph spectrum supplies a three-line spectroscopic target. Instead of asking whether a photon literally traverses forty hidden nodes, engineer forty accessible modes whose transverse kinetic coupling realizes `L_W33`. Internal graph sectors then become externally measurable delay classes. A successful `0:10:16` pattern would validate the device mapping, not a variable vacuum speed.

## Pass 3980 — 904-constant algebraic microcode

The 904 nonzero structure constants are a complete sparse multiplication program for the five-fiber coherent algebra. Relative to the dense cube they compress the algebraic instruction ledger by more than 122-fold. This is finite-algebra microcode—not a claim about physical memory cells, pulse count, or processor throughput.

## Reproduction

```bash
python analysis/w33_pass3973_3980_check.py
pytest -q tests/test_w33_pass3973_3980_extremal_mesh_photon_tensor_monster.py
```

## Evidence boundary

Proved exactly:

- global `A4=57` extremality in the fixed parent-extension problem;
- the order-192 stabilizer census and `45+6+6` geometry;
- the 296-active-mixer/105-swap factorization;
- the fixed-order adjacent lower bound 253;
- all 48 relations and all 904 nonzero constants;
- the algebraic and dimensional identities used in the photon protocol.

Not proved:

- uniqueness or a complete orbit census of maximum codes;
- global mesh optimality or physically free swaps;
- literal hidden photon nodes or a node-dependent vacuum speed;
- achieved information capacity, measured delay, or laboratory performance;
- Monster embedding or class fusion;
- remote CI or manuscript PDF success.
