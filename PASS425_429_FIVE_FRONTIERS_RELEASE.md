# Passes 425–429 — Five Frontier Closure

This release executes five orthogonal follow-ups to Passes 420–424 and retains explicit claim boundaries between exact proofs, deterministic numerical certificates, synthetic channel models, and physical measurements.

## Pass 425 — Exact extension-field Smith gluing

The square biaffine incidence Smith layers are derived from the projective monomial-type elementary-divisor formula through the affine-chart inclusion–exclusion

\[
\mathrm{PG}(3)-2\,\mathrm{PG}(2)+\mathrm{PG}(1),
\]

followed by valuation reversal and the single middle correction. The construction reproduces the exact \(q=3,5,9\) instances and closes the formerly unresolved characteristic-primary layers:

\[
K_{25,(5)}\cong
(\mathbb Z/5)^{3200}\oplus
(\mathbb Z/25)^{6976}\oplus
(\mathbb Z/125)^{2800}\oplus
(\mathbb Z/625)^{800}\oplus
(\mathbb Z/15625)^{623},
\]

\[
K_{27,(3)}\cong
(\mathbb Z/3)^{1920}\oplus
(\mathbb Z/9)^{3678}\oplus
(\mathbb Z/27)^{6812}\oplus
(\mathbb Z/81)^{3354}\oplus
(\mathbb Z/243)^{1596}\oplus
(\mathbb Z/729)^{595}\oplus
(\mathbb Z/19683)^{727}.
\]

Prime-to-characteristic components are not asserted here.

## Pass 426 — Mixed-state qutrit phase portrait

The maximally mixed state is fixed with acceptance \(1/81\), zero linearization, and generic cubic local return. The computational-basis depolarizing axis is exactly invariant with

\[
r_{\rm out}=r^5
\]

and constant acceptance \(1/81\). A deterministic 141-seed census finds 135 trajectories converging to \(I/3\), while the six points of one Clifford orbit at radius \(0.9\) purify toward the pure boundary. A fine scan of that orbit’s depolarizing ray has interleaved mixed and boundary-purifying outcomes. This is a Julia-like numerical signature, not a proof of fractality.

## Pass 427 — Adaptive telemetry channel

The measured divisor determines the exact fibre size, so no prefix header is required. Each source length uses the shortest systematic distance-three Hamming frame. The average protected lengths fall from fixed 18 and 21 bits to

\[
6.817187186168\quad\text{unordered},
\qquad
10.633293985227\quad\text{ordered}.
\]

All worst cases remain within three bytes. A finite Gaussian-jitter/erasure/bit-flip optimization selects guard widths and beats the fixed protected frame in all 36 certified scenarios. These are model-based guaranteed-correct-event costs, not measured link-layer performance.

## Pass 428 — Bayesian hardware diagnosis

The 387-component inverse dictionary now returns normalized component posteriors under family priors and correlated common-mode noise. Across 150 seeded synthetic fault trials, the certificate obtains at least 149 top-1 identifications, 150 top-5 identifications, and 150 correct component families. Low-rank marginal likelihood separates a shared three-bin delay fault from three independent phase trims in all 48 dedicated trials. Priors and covariance are synthetic and require physical calibration.

## Pass 429 — Inductive custody verification

The custody model is lifted from bounded attack enumeration to an inductive event system. `Init` satisfies the global invariant; every one of 24 generic append cases and all three finalize cases preserve it; and removing any of eleven guards yields an executable counterexample. The induction applies to arbitrarily long interleavings and arbitrary finite study maps, while each study retains the fixed eight-stage preregistered protocol. The TLA+ specification records the temporal safety theorem. TLC/Apalache execution and unconditional liveness are not claimed.

## Validation

- all five Pass 425–429 witnesses are deterministic in `--check` mode;
- six focused regression tests pass;
- Passes 415–424 remain included and independently checked;
- the permanent workflow validates the complete Passes 415–429 stack and the claims ledger.
