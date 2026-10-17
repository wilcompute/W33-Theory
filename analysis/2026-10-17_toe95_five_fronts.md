# TOE95 — five Witting / H27 research continuations

Date: **17 October 2026**. Research branch: \`toe95_witting_all_five_20261017\` based on the live W33-Theory repository. The authorized Remote Desktop Commander device was **offline**, so execution and verification use GitHub Actions Linux rather than the user's dirty Windows working tree.

Scope: exact finite algebra and classical finite-population sampling, numerically checked finite group actions and photonic POVMs, plus conditional calibration models. **No actual photonic experiment, no secure key exchange against coherent attacks, no universal quantum processor, and no theory of everything are established.**

## I. The \`F_1\` obstruction for **all 468** admissible CSS pair targets

TOE93 exhibited a particular partial \(H_{27}\)-equivariant edge map from the affine Witting sector (27 vertices, 108 edges) into the Schläfli 135-edge graph. TOE94 proved it cannot extend to the chosen 99-face complex using that fixed one/two-edge routing.

TOE95 permits **arbitrary \(\mathbb F_3\) 1-chains on all 135 target edges** as images of the four representatives of the source's \(H_{27}\)-orbits of undirected edges. That is \(4 \times 135=540\) unknown coefficients. The source has exactly **36 triangles and 324 chordless quadrangles**, partitioned into **16 \(H_{27}\) orbits**. The target has 45 triangles plus two 27-member square orbits. For each pair, require:

\[
\partial_{1,\mathrm{target}} F_1=F_0\partial_{1,\mathrm{source}},\qquad
F_1(\partial_{2,\mathrm{source}} f)\in\operatorname{im}(\partial_{2,\mathrm{target}})
\]
for all 16 source-face orbit representatives, and extend \(F_1\) equivariantly by all 27 Heisenberg translations.

The coefficient system has \(4(27)+16(135-r)\) equations where \(r\) is the target's ternary face rank. For the **36** admissible rank-83 targets, this is **940 equations**, coefficient rank **180**; for **432** rank-95 targets, **748 equations**, coefficient rank **143**. In all **468 individual systems**, the augmented matrix contains a contradiction: **zero consistent extensions**.

Important classification nuance: TOE86's 48-element target direction-normalizer has 13 target-pair orbits, **but only 6 of those 48 automorphisms also preserve the chosen affine source adjacency graph**. Therefore checking only 13 target representatives would not establish the asserted universal no-go; this script explicitly checks all 468.

**Proven obstruction type:** no \(H_{27}\)-equivariant, boundary-preserving \(F_1\) exists for the **fixed** affine 27-address vertex identification and **all 360 specified source 2-cells**, into any of the TOE83 468 admissible face-pair complexes. It does not rule out different \(F_0\), alternative source 2-cells, adding faces, ancillas, general CPTP maps, or physical error correction.

Producer: \`analysis/w33_20261017_toe95_allpairs.py\`.

## II. Projective \(\boldsymbol{PSp(4,3)}\) lifts and the candidate 155,520-element complex reflection group

TOE92 certified all **25,920** ray permutations projectively. TOE94 verified, exactly over \(\mathbb Q(\zeta_{12})\), a \(-I_4\) commutator for two projectively commuting elements.

TOE95 now checks the *whole* Cayley graph under five actual 4×4 order-three Witting unitary transvections. There are **129,600** directed generator transitions. Each numerical U(4) product matches its stored projective representative up to a scalar; the observed scalar discrepancies are precisely the six phases \(\mu_6\). Consequently the generated unitary group has the **numerical** order \(25{,}920 \cdot 6 = 155{,}520\), matching the established 4-dimensional complex reflection group \(G_{32}\) of Shephard–Todd. The determinant character reaches \(\mu_3\); its candidate determinant-one derived group has order 51,840, matching \(Sp(4,3)\).

There is also a **new exact relation** in the prescribed generator order:

\[
U_4 U_1 U_4=\omega\, U_1 U_4 U_1,\qquad
\omega=(-1+i\sqrt3)/2.
\]

It is verified using symbolic matrices in \(\mathbb Q(\sqrt3,i)\), alongside exact generator unitarity and determinant values. Thus both \(\omega I_4\) and the TOE94 \(-I_4\) are exhibited exactly, establishing a subgroup \(\mu_6\) of scalar phases. The **full kernel upper bound/order** and identification of the entire generated matrix group have only the stated finite *numerical* enumeration in this packet, not a fully exact cyclotomic BFS presentation.

Prior art: Shephard and Todd, *Finite unitary reflection groups* (1954); see discussion of \(G_{32}\), its order 155,520 and derived \(Sp(4,3)\) in [MathOverflow 360582](https://mathoverflow.net/questions/360582/finite-group-rm-sp-4-bbb-f-3-involutions-coming-from-a-4-dimensional-c).

Producer: \`analysis/w33_20261017_toe95_group32.py\`.

## III. An exact **non-IID classical** finite-population sampling bound — quantum boundary explicit

TOE94 used a binomial Clopper–Pearson interval, conditional on independent identical error trials. TOE95 allows **an arbitrarily fixed binary error pattern**, with **no IID/error-distribution assumption**, over \(N=4292\) positions. After the pattern is committed, secretly choose \(n=4096\) positions uniformly without replacement for testing, leaving \(196\) for key generation.

For \(k\) observed test errors and failure budget \(\epsilon=0.001\), invert the exact hypergeometric CDF:
\[
K_{\max}=\max\{K:\Pr[\operatorname{Hypergeom}(4292,K,4096)\le k]\ge\epsilon\}.
\]
Except on an event with probability at most \(\epsilon\), the **remaining binary classical errors** are at most \(K_{\max}-k\). The verified maximum remaining error counts for \(k=0,3,7,15,25,40,80\) are \(2,3,4,5,6,8,11\).

This robust classical sampling statement **does not establish coherent-attack Witting QKD security**. Quantum complementary-basis phase errors are not generally simultaneously defined preexisting bits; a quantum sampling reduction and a valid entropy-accumulation min-tradeoff relation are still missing. The script includes a transparent counterexample with 0 test errors and all 196 key positions wrong if an attacker learns the test schedule *before* fixing the errors.

Prior art: Metger and Renner, [*Security of quantum key distribution from generalised entropy accumulation*](https://www.nature.com/articles/s41467-023-40920-8), Nature Communications (2023); Kamin et al., *Finite-Size Analysis of Prepare-and-Measure and Decoy-State QKD via Entropy Accumulation*, PRX Quantum (2025). Their theorems are **not instantiated** here.

Producer: \`analysis/w33_20261017_toe95_finite_population.py\`.

## IV. MZI calibration planning: confidence bound versus physical observability

TOE93 supplied 40 ideal four-mode MZI control circuits. TOE94 explicitly modeled 0–0.01-radian phase drift in those analyzers. TOE95 specifies a **40-setting/4-probe** schedule with a coprime 17-step setting permutation, checks each of the 160 pure ideal basis-state probes, and quantifies the sampling overhead **under trusted IID calibration shots and rank-one projective receiver hardware**.

If **all** \(n\) trials for each probe produce its expected output, a conservative simultaneous 160-probe one-sided probability bound is
\[
p_{\mathrm{wrong}}\le1-(\epsilon/160)^{1/n}\quad(\epsilon=0.001).
\]
For trusted rank-one projective measurements, the corresponding projector spectral deviation obeys \(\|P-\widetilde P\|_\mathrm{op}\le\sqrt{p_{\mathrm{wrong}}}\); hence a deliberately conservative matched-operator separability ceiling is at most \(\min\{1,0.4+8\sqrt{p_{\mathrm{wrong}}}\}\). Certifying a ceiling of 0.44 by **this blunt method** with zero misroutes would need **479,312 shots per probe**, or **76,689,920 calibration shots total**. This motivates more efficient **informationally complete** tomography, as opposed to mistaking clean basis-output counts for a precision phase characterization.

The existing TOE94 phase-drift model is rerun as a cross-check. These are design calculations, not measurements. The calibration method would not by itself exclude drift between shots, untrusted preparation, detector attacks, or correlated SPAM errors.

Producer: \`analysis/w33_20261017_toe95_calibration.py\`.

## V. Exact polar-sector flagged CPTP measurement and nonuniform erasure law

The 13 polar rays of \(W(3,3)\), relative to the TOE93 fixed point, contain the fixed hub ray and its 12 orthogonal neighbors. Their projectors obey the exact 4-dimensional frame identity, numerically verified to machine precision:
\[
\sum_{r\in\mathrm{polar}}P_r=4I_4-3P_{\mathrm{hub}}.
\]
Every Witting ray belongs to four of the 40 tetrads. With a uniformly chosen tetrad, the effect of reporting a **polar flag** is therefore
\[
E_{\mathrm{flag}}=\frac1{10}\sum_{\mathrm{polar}}P_r
=0.4I_4-0.3P_{\mathrm{hub}},
\]
with eigenvalues **0.1, 0.4, 0.4, 0.4**.

For each tetrad \(b\), define four Kraus operators
\(K_{b,i}=|i,\mathrm{polar}(r_i)\rangle\langle r_i|\) from the ququart input to eight orthogonal classical output/flag labels. Their four effects sum to \(I_4\), establishing a trace-preserving completely positive instrument for each of all 40 bases. The explicit outputs are diagonal and the map is **entanglement-breaking**.

A polar flag is **state-dependent**, not a uniform erasure probability: its probability is **10%** for the hub state, **40%** for states orthogonal to the hub, and **13/40=32.5%** for a maximally mixed input. This supports a legitimate *measurement-and-classical-flag* implementation, not a nondestructive ququart erasure channel, H27/CSS decoder, or security-neutral selection rule. Flags and failures must remain in the original denominator of any QKD test.

Producer: \`analysis/w33_20261017_toe95_polar_instrument.py\`.

## Reproduction and test scope

\`python -m pytest -q tests/test_w33_20261017_toe95_all_five.py\` executes each certificate with assertions. The workflow \`.github/workflows/w33_toe95_five.yml\` reruns the five separate scripts on a clean Linux runner and publishes their JSON certificates as a workflow artifact. The research branch exists specifically to catch failures before proposing any merge to \`master\`. All result claims require a green hosted workflow.

## Five best independent research directions

1. **Test different 27-point embeddings or augment the source face geometry.** The 468-pair no-go fixes \(F_0\) and the chosen 360 source cycles; classify which modified data evade the now-exhaustive obstruction.
2. **Replace numerical \(G_{32}\) closure with exact cyclotomic group enumeration.** Verify the exact scalar kernel upper bound, central order, determinant-one derived subgroup and a finite presentation isomorphic to \(Sp(4,3)\).
3. **Derive quantum phase-error statistics for Witting contexts.** Construct a legitimate prepare-and-measure min-tradeoff function and invoke generalized entropy accumulation with realistic photon loss.
4. **Build an informationally complete hardware calibration protocol.** Optimize 4-mode probe states, per-basis tomography, drift-aware randomized schedules and audited device logs to beat the conservative 76.7-million-shot bound.
5. **Engineer nondestructive flagged quantum storage.** The polar instrument proven here is entanglement-breaking; find a physically specified isometric/ancilla architecture retaining logical quantum coherence and supporting genuine CSS stabilizer recovery.
