# Passes 4121–4128 — explicit gauge, relational DFS, decoder, foundry, attractors, and three outside-box probes

## Evidence boundary

This packet contains exact finite representation, channel, graph, projector, spectral, and combinatorial results, plus an explicitly labelled 64-seed nonlinear census and heuristic crossing-order optimization. It does **not** claim a derived Standard Model, a fabricated CORNERSTONE chip, measured decoding or patterns, a physical magnetic material, a graph-walk processor, an exceptional-point sensor, gravity, cosmology, or a theory of everything.

Frozen certificate: `data/PART_4121_4128_EXPLICIT_GAUGE_DFS_DECODER_FOUNDRY_ATTRACTORS_BONKERS.json`  
Semantic SHA-256: `a549172701e05bdcb0e629f8cea5282be46db70f223e043b4cb0359b9c3dc4bc`

## Pass 4121 — explicit 145-dimensional matrices and an anomaly correction

The carrier

\[
(\mathbb C^7\otimes V_1)\oplus(\mathbb C^6\otimes V_{15})\oplus(\mathbb C^2\otimes V_{24})
\]

was materialized with eight `SU(3)`, three `SU(2)`, and one hypercharge generator. The Lie-algebra and Hermiticity residuals are below `7.1e-16`.

The explicit matrices expose a correction to Pass 4105. Its anomaly cancellation concerned one abstract multiplicity-space generation. Acting identically over all `V15` and `V24` orbital copies gives W33 weights

\[
(q,u,d,l,e)=(1,15,15,24,1),
\]

and anomalies

\[
SU(3)^3=-28,\quad SU(3)^2U(1)=-\frac73,
\quad SU(2)^2U(1)=-\frac{23}{4},
\]

\[
\mathrm{grav}^2U(1)=-37,\qquad U(1)^3=-\frac{599}{36},
\]

with 27 weak doublets, hence an odd Witten count.

Without exotic representations, the linear anomaly equations force

\[
q=u=d=l=e.
\]

Thus an anomaly-free generation must use a common W33 multiplicity. Exact repairs are: a rank-one 15-dimensional gauged subspace inside the 145 states, breaking `PSp(4,3)`; a 225-dimensional `V15` generation; a 360-dimensional `V24` generation; or 600 dimensions containing one full generation in each of `V1,V15,V24`.

There are no bare gauge-invariant chiral masses. The gauge representation admits three Yukawa tensors, but a W33-singlet Higgs admits none because the fields occupy incompatible W33 sectors. The required mediator sectors are `V15,V15,V24` for up, down, and lepton couplings.

## Pass 4122 — a relational phase-reference subsystem

A single fixed-Hamming-weight sector is exactly decoherence-free under the shared sine reference, but the desired collective phase is only a global scalar there. This is an exact signal-protection no-go.

For odd `N=2r+1`, pair the equal-dimensional sectors `H_r` and `H_(r+1)`. After basis pairing, the code factors as

\[
\mathbb C^2_{\rm clock}\otimes\mathbb C^{\binom Nr}_{\rm payload}.
\]

The ideal phase acts only on the clock, while the noisy shared-reference channel is precisely the one-use `z1` channel on that clock and the identity on the payload. Every payload coherence is exact.

At `K=256`, `N=31` carries one phase clock plus 28 protected payload qubits. Its phase error is `7.3646628264e-5`, versus `5.5087125884e-2` for direct 29-qubit injection, an improvement factor `747.99`.

## Pass 4123 — graph-aware three-error decoder

For

\[
y=De+n,\qquad \|n\|_2\le\epsilon,\qquad |\operatorname{supp}e|\le3,
\]

threshold vertices by `|y_v|>2 epsilon`, then collect all unique Levi paths of length at most three between threshold vertices. Since every three-edge support is a forest, every true edge lies on one of these leaf-to-leaf paths under the certified amplitude condition.

An exhaustive audit of all 682,641 supports proves that the generated candidate graph has at most 20 edges. Therefore the exact least-squares stage tests at most

\[
1+20+\binom{20}{2}+\binom{20}{3}=1351
\]

supports, a `505.29×` reduction. The restricted singular value remains

\[
\sigma_6=2\sin(\pi/14)=0.4450418679,
\]

so

\[
\|\hat e-e\|_2\le2\epsilon/\sigma_6.
\]

## Pass 4124 — CORNERSTONE 340-nm SOI feasibility audit

The exact four-router permutations were floorplanned as four 40-by-40 permutation regions. A balanced heuristic ordering gives 1,934 physical crossings and at most 21 crossings on one optical path.

A crucial device-count correction follows from spatial path encoding: 80 modes require 240 splitter MMIs and 240 recombiner MMIs. Six QSP phase planes require 480 phase shifters unless a common-mode phase mechanism is introduced.

Using conservative public platform inputs and explicit assumptions gives a conditional internal path loss of `5.486 dB` before MMI losses and `27.43 dB` over five signal uses. The worst all-π heater envelope is `9.6 W`, and independent control exceeds a referenced 120-DC package.

Verdict: the logical route table is exact, but the naive spatial CORNERSTONE SOI340 device is not tapeout-ready. The credible repair is low-loss SiN passive routing plus an active phase layer, or time/frequency serialization.

## Pass 4125 — nonlinear attractor orbit census

Sixty-four deterministic seeds were evolved to `t=500` for each cubic Turing selector and quotiented numerically by `PSp(4,3)` and global sign.

The 24-dimensional selector produced 25 observed orbit classes: seven pure bivalent classes and 18 mixed classes. Pure stabilizers include `V4`, `S3`, `D8`, `C6×C2`, `D10`, and `S5`.

The 15-dimensional selector produced nine classes: one pure bivalent `A5` class and eight mixed classes. The earlier seed-42 pure result remains correct, but the global claim that cubic saturation always stays in one Laplacian eigenspace is false.

## Pass 4126 — exact antiferromagnetic Ising ground state

The pure `A5` sign vector satisfies

\[
As=-4s.
\]

It cuts 160 of the 240 edges, saturating the spectral MaxCut bound. Every vertex sees eight opposite and four equal spins, and the antiferromagnetic energy is

\[
E_0=-80J.
\]

Its stabilizer has order 60, giving a 432-element sign orbit and 216 distinct cuts modulo global reversal.

## Pass 4127 — exact graph-walk Householder mirror

For `H=JA`, at

\[
t=\frac{\pi}{2J},
\]

the walk is

\[
U=I-2P_2=\frac{A^2-8A-18I}{30}
=-\frac{I+A}{3}+\frac{2}{15}J_{40}.
\]

It flips the entire 24-dimensional adjacency-eigenvalue-two sector and preserves the uniform and eigenvalue-minus-four sectors. It is an involution, with vertex-input probability totals `1/25` at the source, `12/25` on neighbors, and `12/25` on nonneighbors. Full revival occurs at `pi/J`.

## Pass 4128 — fifteen simultaneous exceptional points

Pair all 15 eigenvalue-minus-four modes with 15 of the 24 eigenvalue-two modes. On each pair use

\[
H_j=\begin{pmatrix}i\gamma&g\\g&-i\gamma\end{pmatrix}.
\]

At `gamma=g`, all 15 blocks are simultaneous second-order exceptional points. The paired 30-dimensional operator squares to zero and has rank 15. A diagonal detuning gives square-root splitting

\[
|\Delta\lambda|\sim2\sqrt{g|\epsilon|}.
\]

This is an exact controlled-projector construction, not a local or fabricated sensor.

## Reproducibility

Run:

```bash
python analysis/w33_pass4121_4128_explicit_gauge_dfs_decoder_foundry_attractors.py
pytest -q tests/test_w33_pass4121_4128_explicit_gauge_dfs_decoder_foundry_attractors.py
```

The verifier regenerates W33, the 145-dimensional generators, phase-reference errors, all 682,641 decoder supports, the crossing audit, the maximum cut, the graph-walk reflection, and the exceptional-point rank/nilpotency checks.
