# Passes 1112–1121 — Qontrol, A2 carriers, cubic incidence, and observed runtime closure

Status: **PR runtime pending**

This release preserves the completed parallel Passes 1102–1119 and adds only non-overlapping work.

## Pass 1112 — Qontrol Q8iv/BP8 transport

A second concrete vendor boundary implements the 240-command control schedule:

- 40 voltage-limit commands;
- 160 routing-voltage commands;
- 40 telemetry queries.

The adapter binds an approved controller identity, an external arming commitment, voltage limits, a hash-chained transcript, and emergency zeroing of all 40 channels. The committed receipt is from a reference serial double. No Qontrol, Keysight, detector, or optical hardware was connected.

## Pass 1113 — first tested E8-derived Steinberg carrier

The 2240 unordered E8 root triples satisfying

\[
\alpha+\beta+\gamma=0
\]

have exact frame-visible multiplicities

\[
\langle\chi_{2240},81_+\rangle=0,
\qquad
\langle\chi_{2240},81_-\rangle=3.
\]

This improves the pair-only minimum 3360, while the first tested 81-plus carrier remains the 15120 orthogonal-root-pair action.

## Pass 1114 — complete 45-term central-phase transport

The E6 cubic support decomposes as

\[
45=36+9,
\]

with 36 affine-line terms and nine vertical central-C3 firewall fibers. The exact central-phase histogram is

\[
0^{25}\oplus1^{10}\oplus2^{10}.
\]

The nine firewall signs remain 2 positive and 7 negative. The complete 45-term sign gauge is promoted only after the canonical solver is rerun and observed.

## Pass 1115 — formal source lock

`formal/W33/Pass1115A2PhaseQontrolClosure.lean` freezes the A2 multiplicities, phase histogram, firewall sign split, Qontrol schedule arithmetic, and carrier inequalities. It imports the strict parallel Pass-1106 package.

## Pass 1116 — fail-closed runtime ledger

The runtime ledger remains pending until all of the following are observed:

1. GAP/CTblLib row identities;
2. complete canonical cubic sign regeneration;
3. strict serial `lake build --wfail` with zero failed modules and zero phantom `.olean` errors.

The workflow assembles those artifacts automatically and refuses to report observed closure when any one is missing.

## Pass 1120 — complete CTblLib decomposition

A GAP program decomposes the full 2240-point permutation character against every irreducible row of `U4(2).2`. It verifies nonnegative integral multiplicities and reconstructs degree 2240 exactly. Row identities and the full constituent list are runtime outputs, not guessed labels.

## Pass 1121 — equivariant A2/cubic/firewall incidence

The executable constructs exact maps from all 2240 A2 root triples to:

- the 27 E6 labels;
- all 45 cubic supports;
- the nine selected firewall supports.

The predicted cubic-lift carrier is

\[
540=270+270,
\]

with six lifts per cubic term in the `27 x 3` sheet and six conjugate lifts in the `27bar x 3bar` sheet. The program checks all six E6 simple generators, computes the A2-triple orbit decomposition, and records ranks and kernels over characteristic zero certificates and over F3.

The nine firewall terms are treated as a selected support restriction. No claim is made that this nine-term subset is globally W(E6)-stable.

## Validation policy

The pre-existing Passes 1112–1116 carry 72 exact checks and eight focused tests. Pass 1121 adds 16 executable checks. The release is merged only after the PR workflow regenerates every certificate and the observed runtime ledger is committed.
