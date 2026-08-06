# Passes 3913–3920 — multi-defect immunity, symmetry Lindbladian, process control, correlated fusion, phase inversion, and three architecture breakthroughs

## Exact status

```text
PASS_8_FRONTS 019183d46768ff68a5f57676540d8aefd853010614545fd834656b69c4c7eb15
```

The focused suite contains six regressions. Exact finite-geometry statements are separated from declared HMM, fusion, energy, and open-system models.

## 3913 — bounded multi-defect immune system

For every programmed adjacency matrix B define the W33 residual

\[
R(B)=B^2+2B-8I-4J.
\]

The verifier exhausts all 780 candidate edge toggles. Every one of the

\[
\binom{780}{2}=303{,}810
\]

two-toggle insert/delete mixtures has a distinct complete residual. It also exhausts all

\[
\binom{240}{3}=2{,}275{,}280
\]

three-edge deletions, again with no repeated residual. Thus general ambiguity cannot begin below weight three, and deletion-only ambiguity cannot begin below weight four. General insertion/mixed weight-three cases remain open.

The ordered two-defect corpus digest is

```text
eef644db8085884bd9a0c8cd3f115596343d6d131075ab540e6ce9143d227681
```

## 3914 — random-unitary W33 Lindbladian

Let the four generating transvections and their inverses act by permutation unitaries U_g. The generator

\[
\mathcal L(X)=\frac18\sum_g(U_g XU_g^\dagger-X)
\]

is a valid random-unitary Lindbladian. The ordered-pair action has exactly three orbits of sizes 40, 480, and 1080, so

\[
\operatorname{Fix}(\mathcal L)=\operatorname{span}\{I,A,J-I-A\}.
\]

The second eigenvalue of the discrete jump channel is

\[
0.9367092858522459,
\]

and the unit-rate continuous-time gap is

\[
\boxed{0.06329071414775411}.
\]

Each transvection is nine disjoint three-cycles plus thirteen fixed points. The eight directed jumps therefore admit a 72 three-mode-cycle compiler target. This does not prove that replacing each global jump by independently applied local cycles preserves the same fixed algebra.

## 3915 — partially observed closed-loop controller

A six-step hidden Markov benchmark has four hidden regimes, four noisy observations, five machine modes, 85% correct regime readout, discount 0.9, and switching cost two. Exact belief-state dynamic programming evaluates 5,461 reachable beliefs.

The partially observed optimum is

\[
\boxed{23.115384313076735},
\]

compared with best static cost

\[
30.176036574158424
\]

and fully observed lower bound

\[
16.514150252446512.
\]

Thus noisy online observation improves the declared benchmark by 7.060652261081689 relative to the best static mode, while imperfect observability costs 6.601234060630222 relative to full-state control. These values belong to the frozen HMM, not measured process-tensor data.

## 3916 — twelve-round fusion under common outages and memory decay

Each perfect-matching round contains twenty edge tokens. The exact 21-state chain tracks the number already established. A retry applies stored-edge survival 0.995, a shared-pump outage probability 0.05, and conditional independent fusion probability p. Five attempts are allowed per matching.

For a complete twelve-round epoch to succeed with probability at least 0.99, the required physical edge probability is

\[
\boxed{p\ge0.9158993399430635}.
\]

Without the common outage and decay, the threshold is 0.8668344006872047. The declared correlation/decay penalty is therefore 0.04906493925585875.

## 3917 — joint architecture phase diagram

Five implementations are compared: native W33, virtual W33, the local ring, a routed mesh, and a shared bus. The exact frozen grid contains 500 coefficient points spanning edge reliability p, consumable-token price b, round price g, and routing-hop price d, with static-link price normalized to one.

Winner census:

\[
\begin{array}{c|r}
\text{implementation}&\text{grid wins}\\\hline
\text{bus W33}&310\\
\text{virtual W33}&84\\
\text{native W33}&54\\
\text{local ring}&37\\
\text{mesh W33}&15
\end{array}
\]

Every implementation wins somewhere. There is no coefficient-independent architecture. Exact pairwise surfaces include native=virtual iff a=b and native=bus iff 239a=228g-824d. The mesh depth 120 is a declared benchmark coefficient.

## 3918 BONKERS — topology DNA

The complete oriented W33 edge set is the orbit of one ordered edge under four finite-field transvection generators. Their closure has order 25,920 and the ordered-edge orbit has size 480.

The topology can therefore be specified by four four-trit generator vectors plus one ordered edge: eighteen finite-field coordinate symbols rather than 960 endpoint symbols for the explicit oriented-edge table. The symbolic compression factor is

\[
\boxed{53.3333333333}.
\]

This is a mathematical graph seed, not a pulse-memory or fault-tolerant storage estimate.

## 3919 BONKERS — dual-geometry all-to-all scheduler

The 240 W33 edges have a twelve-round perfect-matching factorization. The 540 complement edges have an explicit twenty-seven-round factorization. Together they partition every edge of K_40:

\[
A+(J-I-A)=J-I.
\]

Hence a W33 phase followed by its complement phase implements a complete all-to-all interaction epoch in

\[
\boxed{12+27=39\text{ rounds}}.
\]

This is optimal because every mode has 39 partners and can meet at most one partner per one-port round.

Complete factorization digest:

```text
c17c5a424a90d28d1f2313d7db71774efa29ed54a452ec486c160ddd1dfd2553
```

## 3920 BONKERS — compressed multi-defect sensor

A fixed measurement set containing all forty residual diagonals and 152 seeded off-diagonal entries distinguishes every one of the 303,810 two-toggle syndromes. It uses

\[
\boxed{192/1600}
\]

of the complete matrix residual, an 8.3333-fold reduction.

Coordinate digest:

```text
41dd8419716ccd0fed529a0dd505c34de4b681879837c086589e032f58a3ef59
```

The construction is explicit but not proved minimum and has no noise-robustness theorem.

## Reproduction

```bash
python analysis/w33_pass3913_3920_multidefect_lindbladian_process_fusion_phase.py --json /tmp/pass3913_3920.json
pytest -q tests/test_w33_pass3913_3920_multidefect_lindbladian_process_fusion_phase.py
```

## Evidence firewall

No claim is made for general weight-three mixed-defect uniqueness, sparse local Lindbladian synthesis, learned process-tensor performance, microscopic fusion correlations, measured cost coefficients, minimal topology-DNA memory, simultaneous all-to-all coupling, minimum compressed sensing, remote CI/PDF success, or laboratory performance.
