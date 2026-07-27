# Passes 1107–1111 — Qontrol, the A₂ Steinberg carrier, complete cubic phases, and observed runtime closure

## Status

- **72/72 local exact certificate checks passed.**
- **8/8 focused pytest tests passed.**
- Runtime-dependent GAP/CTblLib, canonical-sign, and strict-Lean observations are intentionally pending the PR workflow.
- No physical Qontrol controller, detector, or optical device was connected.

These passes are additive to the parallel Passes 1102–1106 release. They do not overwrite its exact CTblLib fingerprints, signed nine-fiber transport, pair-carrier census, Keysight adapter, or formal Clifford package.

## Pass 1107 — a second concrete vendor boundary: Qontrol Q8iv/BP8

A transport for the Qontrol Q8iv controller on a BP8 backplane implements the documented 115200-8-N-1 serial boundary and the raw command surfaces `ID?`, `vmax[port]=value`, `v[port]=value`, and `vipall?`.

The deterministic schedule contains

\[
40\text{ voltage limits}+160\text{ route voltages}+40\text{ telemetry queries}=240
\]

commands across forty ports. The transport defaults to dry-run, constructs no serial object in dry-run, requires an externally committed arm token, binds the returned Q8iv identity, enforces port and voltage limits, hash-chains the transcript, and zeros all forty outputs on emergency stop.

The reference-double run produced 243 transcript events and 281 raw serial writes, including identity and emergency-zero commands. Unarmed, wrong-token, wrong-identity, and over-voltage probes all fail closed. This is a second vendor implementation alongside Pass 1105's Keysight SCPI boundary, not a physical-device result.

## Pass 1108 — the A₂ root triples beat the pair-carrier minimum

Pass 1104 searched natural root-pair and antipodal-root-line-pair carriers and found its first Steinberg-bearing pair carrier at degree 3360, carrying four copies of \(81_-\). It found the first \(81_+\) at degree 15120.

The extension adds the canonical E8-derived set

\[
\mathcal A_2=\{\{\alpha,\beta,\gamma\}:\alpha+\beta+\gamma=0\}.
\]

There are exactly

\[
|\mathcal A_2|=2240
\]

unordered A₂ root triples. Their exact fixed-point character in the same 25-class ATLAS order has inner products

\[
\langle\chi_{\mathcal A_2},81_+\rangle=0,
\qquad
\langle\chi_{\mathcal A_2},81_-\rangle=3.
\]

Thus the improved tested hierarchy is

\[
2240:\;3\cdot81_-,
\qquad
3360:\;4\cdot81_-,
\qquad
15120:\;81_+\oplus26\cdot81_-.
\]

Minimality is claimed only over the explicit Pass-1104 pair universe plus the A₂ triple carrier—not over every possible E8-derived G-set.

## Pass 1109 — complete 45-triad central-phase transport

Pass 1103 attached the nine dual-Hesse lines to the nine signed firewall fibers. Pass 1109 transports the entire cubic support through the concrete Heisenberg coordinates on all 27 E6 labels.

The 45 tritangent triads split exactly as

\[
45=36\text{ affine-line lifts}+9\text{ vertical central-}C_3\text{ fibers}.
\]

For every triad the central phase

\[
z_1+z_2+z_3\pmod3
\]

is computed. The exact histogram is

\[
\boxed{0^{25}\oplus1^{10}\oplus2^{10}}.
\]

The nine vertical terms retain the exact canonical sign split from Pass 1103:

\[
\boxed{2\text{ positive},\;7\text{ negative}}.
\]

They are simultaneously the deleted firewall monomials and the declared \(l_3\)/Jacobiator-repair support. A full 45-term Chevalley sign table is included only when the canonical solver artifact is actually regenerated; absence remains an explicit boundary.

## Pass 1110 — formal A₂/phase/Qontrol closure

The Lean module `formal/W33/Pass1110A2PhaseQontrolClosure.lean` imports the parallel Pass-1106 formal package and freezes:

- zero \(81_+\) multiplicity and multiplicity three for \(81_-\) in the A₂ carrier;
- the central-phase histogram \((25,10,10)\);
- the signed firewall count \((2,7)\);
- the Qontrol schedule count \((40,160,40)\);
- the strict inequalities \(2240<3360<15120\).

It uses kernel tactics (`decide`/`norm_num`) and no `native_decide`. Compilation is not claimed until the strict PR workflow is observed.

## Pass 1111 — multi-runtime closure

The PR-visible workflow has four independent jobs:

1. all local Python certificates and focused tests;
2. GAP plus CTblLib, resolving the ten canonical row indices in `U4(2).2`;
3. regeneration and verification of the complete canonical SU(3)/E6 cubic sign solve;
4. a serial `lake build --wfail` of every module imported by `formal/W33.lean`, with a zero phantom-olean requirement.

The release remains `PASS_LOCAL_RUNTIME_PENDING` until those artifacts are inspected. No green status is inferred from a workflow definition alone.

## Authoritative artifacts

- `analysis/w33_pass1107_qontrol_q8iv_transport.py`
- `data/w33_pass1107_qontrol_q8iv_transport.json`
- `hardware/w33_pass1107_qontrol_q8iv_receipt.json`
- `analysis/w33_pass1108_e8_a2_triple_carrier_extension.py`
- `data/w33_pass1108_e8_a2_triple_carrier_extension.json`
- `analysis/w33_pass1109_full_cubic_central_phase_extension.py`
- `data/w33_pass1109_full_cubic_central_phase_extension.json`
- `formal/W33/Pass1110A2PhaseQontrolClosure.lean`
- `analysis/w33_pass1110_formal_a2_phase_qontrol_lock.py`
- `data/w33_pass1110_formal_a2_phase_qontrol_lock.json`
- `analysis/w33_pass1111_runtime_closure.py`
- `data/w33_pass1111_runtime_closure.json`
- `tests/test_w33_pass1107_1111.py`
- `.github/workflows/pass1107_1111_runtime.yml`
