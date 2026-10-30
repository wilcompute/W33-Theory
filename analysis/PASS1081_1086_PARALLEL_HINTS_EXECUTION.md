# Passes 1081–1086 — parallel-hint execution package

## Status

- **74/74 exact checks passed.**
- **7/7 focused pytest tests passed in 0.05 seconds.**
- The parallel agent's full `lake build W33` at commit `0916335f2fdadcedee4dc26eb6a100b8a232f4c2` exited 0 for all 40 imported modules, including Pass 1074.
- No physical optical hardware was connected; Pass 1085 is a mock-controller hardware-in-the-loop rehearsal with cryptographic integrity checks.

## Pass 1081 — frame permutation-module lattice

The parallel agent's imprimitivity hint was reconstructed independently. The 540-frame action has unique block systems

\[
540\to135\text{ blocks of }4\to45\text{ blocks of }12,
\qquad
540\to36\text{ blocks of }15.
\]

Their permutation submodules have dimensions 135, 45, and 36. The 45-dimensional module lies inside the 135-dimensional module. The 135- and 36-dimensional modules intersect only in the constants, as do the 45- and 36-dimensional modules. The natural 36-dimensional spread-incidence row space is a second, distinct copy of the spread permutation module: its intersection with the 36-block quotient module is only one-dimensional, and their sum has dimension 71.

This gives the exact module lattice

\[
\dim U_4=135,
\quad \dim U_{12}=45,
\quad \dim U_{15}=36,
\]

with new quotient dimensions 90, 44, and 35 after removing the nested or constant sectors.

## Pass 1082 — corrected frame coherent configurations

The complete Schurian coherent configuration was computed on all ordered frame pairs.

The inner `PSp(4,3)` action has rank 32, but only 12 orbitals are self-paired. The remaining 20 form ten transpose pairs. This retracts only the pairing sentence in Pass 1079; the imprimitivity and frame-graph decomposition remain correct.

The outer `GSp(4,3)` stabilizer fuses the 32 inner orbitals to 22 outer orbitals. That fusion is not the transpose closure. The outer configuration has 14 self-paired and eight non-self-paired orbitals. Exact intersection tensors of shapes `32×32×32` and `22×22×22` are generated and hash-locked by the verifier.

The frame graph is exactly the union of seven inner relations with valencies

\[
3+6+12+12+12+24+48=117.
\]

## Pass 1083 — Levi-to-frame Steinberg intertwiners

The flag stabilizer has ten orbits on frames:

\[
27^5,\qquad81^5.
\]

For each cross-orbit incidence matrix `X`, the verifier applies the exact source and target projectors

\[
K_{\rm Levi}=160P_{H_1},
\qquad
Q_{\rm frame}=25515P_{\ker B},
\]

and constructs

\[
T=Q_{\rm frame}XK_{\rm Levi}.
\]

Eight of the ten relations yield rank-81 maps. Every selected map satisfies

\[
BT=0,
\qquad TD^T=0,
\qquad TK_{\rm Levi}=160T,
\]

and is equivariant under all five transvection generators.

The maps span a two-dimensional intertwiner space. Some pairs have the same 81-dimensional image, while generic pairs have combined rank 162. Therefore the 504-dimensional frame-incidence kernel contains at least two distinct copies of the Levi/Steinberg 81-module. This is a map-level result, not a dimension match.

## Pass 1084 — exact parabolic normalizer and arrangement

The setwise stabilizer of `x4=0` in `G32` has order

\[
3888=648\cdot6.
\]

Its pointwise stabilizer is the embedded `G25` of order 648. The quotient is `C6`; its action on the basic invariant ring factors through parity `C2`. An exact reflection word lifts to

\[
\operatorname{diag}(-\omega,-\omega,-\omega,1+\omega).
\]

On the `G25` basics it acts by

\[
u_6\mapsto u_6,
\qquad v_9\mapsto-v_9,
\qquad w_{12}\mapsto w_{12}.
\]

This explains structurally why the restricted `G32` invariant ring lies in the `v9`-even subring.

The characteristic-zero reflection arrangement was also enumerated exactly over `Q(ω)`: one `G32` hyperplane is the slice itself; after removing it, the other 39 restrict as 12 `G25` hyperplanes once and nine extra hyperplanes with multiplicity three.

## Pass 1085 — hardware-in-the-loop rehearsal

A deterministic mock MZI controller executes 240 commands:

- 40 calibration commands;
- 160 routing commands;
- 40 acquisitions.

The resulting 240 telemetry events are hash chained and HMAC signed. Every acquisition is bound to a calibration identifier. The public manifest contains only an escrow-key commitment; real acquisition requires separately supplied key material. Offline unblinding verifies the commitment, while a wrong key fails closed.

The synthetic contextual fixture returns

\[
W=10.03975>7,
\]

for the state-independent witness. No click-rate statistic is labeled as a contextual fraction.

## Pass 1086 — contextuality claim firewall

The legacy `bt1901_contextual_fraction_estimator.py` is corrected in place. It now identifies itself as a signal-click-rate estimator and emits fields such as `corrected_signal_click_rate`; it no longer emits `corrected_contextual_fraction`.

The firewall consumes Pass 1080's exact result

\[
CF(W(3,3))=1,
\qquad CF(W(2,2))=0,
\]

and rejects any executable hardware manifest that labels `0.1` as an Abramsky–Barbosa contextual fraction. The value `1/10` remains only an underived historical click-rate target until a separate observable derivation exists.

## Authoritative artifacts

- `analysis/w33_pass1081_1086_core.py`
- `analysis/w33_pass1081_frame_module_lattice.py`
- `analysis/w33_pass1082_frame_coherent_configuration.py`
- `analysis/w33_pass1083_levi_frame_steinberg_intertwiner.py`
- `analysis/w33_pass1084_g32_g25_parabolic_normalizer.py`
- `analysis/w33_pass1085_hardware_in_loop_rehearsal.py`
- `analysis/w33_pass1086_contextuality_claim_firewall.py`
- `analysis/PASS1079_ORBITAL_PAIRING_CORRECTION.md`
- `data/w33_pass1081_1086_release.json`
- `tests/test_w33_pass1081_1086.py`
- `.github/workflows/pass1081_1086_exact.yml`
