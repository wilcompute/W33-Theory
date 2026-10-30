# Passes 1102–1106 — CTblLib/Clifford naming, full firewall transport, E8 pair carriers, Keysight transport, and formal closure

## Release status

- **86/86 exact certificate checks passed locally.**
- **7/7 focused pytest tests passed locally.**
- Parallel commit `7bd164ad386d2c4b407308a444d6a2b077a68f3f` is the observed strict formal baseline: all 42 pre-existing modules passed `lake build --wfail`.
- The new Pass-1106 module is umbrella-wired and submitted to isolated strict CI; no local Lean executable is available.
- The CTblLib resolver is committed, but literal row numbers are not claimed until a GAP/CTblLib run is observed.
- The Keysight adapter was exercised only against a reference SCPI endpoint. No physical optical hardware was connected.

## Pass 1102 — canonical ATLAS/CTblLib and Clifford layer

The exact 25-class character vectors from Pass 1092 are promoted to stable canonical fingerprints for the ten frame-visible constituents

\[
1,15_a,15_b,20,24,60_a,60_b,64,81_+,81_-.
\]

The certificate verifies pairwise character orthonormality, reconstructs the degree-540 frame permutation character, hashes every row, and freezes the CTblLib table identifier `U4(2).2`.

The restriction matrix to the inner `U4(2)` constituents

\[
1,15,20,24,30_a,30_b,60,64,81
\]

is explicit. In particular,

\[
15_a\downarrow=15_b\downarrow=15,
\qquad
60_b\downarrow=30_a\oplus30_b,
\qquad
81_+\downarrow=81_-\downarrow=81.
\]

The frame-visible induction matrix is its Frobenius-reciprocity transpose:

\[
\operatorname{Ind}(15)=15_a\oplus15_b,
\quad
\operatorname{Ind}(30_a)=\operatorname{Ind}(30_b)=60_b,
\quad
\operatorname{Ind}(81)=81_+\oplus81_-.
\]

A GAP companion queries `Position(Irr(CharacterTable("U4(2).2")), ...)` for every exact vector. Because GAP is absent locally, row numbers remain explicitly pending rather than guessed.

## Pass 1103 — line-by-line lift to the full 27-point cubic carrier

The nine dual-Hesse normals are now transported through the repository's exact Heisenberg coordinates to all 27 `e6id` vertices. Each line receives:

1. its affine coordinate \(u\in\mathbb F_3^2\);
2. the ordered central-\(C_3\) cycle \((u,0)\to(u,1)\to(u,2)\);
3. the corresponding forbidden cubic triad;
4. the canonical cubic sign.

The nine cycles partition all 27 `e6id` values. The nine deleted triads have 27 distinct internal edges, exactly the firewall bad-edge support. Their canonical sign distribution is

\[
2\text{ positive},\qquad7\text{ negative}.
\]

This is an objectwise transport of the Jacobiator support labels: every deleted cubic monomial is now identified with one dual-Hesse line. The pass does not claim newly recomputed full numerical Jacobiator coefficients.

## Pass 1104 — first positive E8-derived carriers for \(81_\pm\)

The complete declared pair-carrier universe was enumerated under the faithful `W(E6)=U4(2):2` action:

- unordered E8 root pairs, split by root inner product;
- unordered antipodal root-line pairs, split by absolute inner product.

The carrier census is:

| Carrier | Degree | \(m(81_+)\) | \(m(81_-)\) |
|---|---:|---:|---:|
| Antipodal root pairs | 120 | 0 | 0 |
| Root pairs, dot \(-4\) | 6,720 | 0 | 10 |
| Root pairs, dot \(0\) | 15,120 | 1 | 26 |
| Root pairs, dot \(4\) | 6,720 | 0 | 7 |
| Root-line pairs, abs-dot \(0\) | 3,780 | 0 | 6 |
| Root-line pairs, abs-dot \(4\) | 3,360 | 0 | 4 |

Thus the first Steinberg-bearing carrier in this declared universe is the 3,360-element nonorthogonal antipodal root-line-pair set, containing four copies of \(81_-\). The first \(81_+\) occurs in the 15,120 orthogonal-root-pair carrier with multiplicity one.

Minimality is claimed only inside the explicitly enumerated pair universe—not over every possible coset action or E8-derived construction.

## Pass 1105 — concrete Keysight FlexOTO/N7731A transport

A device-specific SCPI encoder now targets the Keysight FlexOTO profile with an N7731A two-channel 1x4 optical switch. It uses the documented surfaces

- `*IDN?`;
- `:CONFigure:SWITch:ACTive`;
- `:CONFigure:SWITch:ALL?`;
- `:CONFigure:PORT:CONNect`.

The W33 adapter retains:

- hard dry-run with zero I/O;
- firmware identity and allowlisting;
- external arm-token commitment;
- immutable manifest and sequence locks;
- calibration binding and expiry;
- four-port routing before acquisition;
- replay rejection;
- emergency stop.

All 240 schedule commands passed against a reference SCPI endpoint. Wrong arm token, unapproved firmware, replay, unarmed acquisition, expired calibration, and emergency-stop probes all failed closed. Acquisition operations are detector-service handoffs; the switch adapter does not fabricate click measurements.

## Pass 1106 — compact formal Clifford/firewall/carrier lock

`formal/W33/Pass1106CliffordFirewallCarrier.lean` freezes:

- the CTblLib identifier;
- the explicit restriction and frame-visible induction matrices;
- induction dimension identities for 15, 30, and 81;
- the nine exact firewall `e6id` cycles;
- the \(2/7\) cubic sign balance;
- multiplicity four of \(81_-\) in the 3,360 carrier;
- multiplicity one of \(81_+\) and 26 of \(81_-\) in the 15,120 carrier;
- hashes of the executable carrier and firewall certificates.

The new finite statements use kernel-evaluable `decide` and `norm_num`, following the parallel agent's strict-build repair that replaced expensive or invalid `native_decide` uses. The pre-existing 42-module tree has an observed strict build; the new module's build remains a CI boundary until observed.

## Authoritative artifacts

- `analysis/w33_pass1102_ctbllib_clifford_naming.py`
- `analysis/w33_pass1102_ctbllib_rows.g`
- `analysis/w33_pass1103_hesse_firewall_cubic_transport.py`
- `analysis/w33_pass1104_e8_pair_carrier_census.py`
- `analysis/w33_pass1105_keysight_n7731a_transport.py`
- `analysis/w33_pass1106_formal_clifford_firewall_carrier.py`
- `formal/W33/Pass1106CliffordFirewallCarrier.lean`
- `data/w33_pass1102_ctbllib_clifford_naming.json`
- `data/w33_pass1103_hesse_firewall_cubic_transport.json`
- `data/w33_pass1104_e8_pair_carrier_census.json`
- `data/w33_pass1105_keysight_n7731a_transport.json`
- `data/w33_pass1106_formal_clifford_firewall_carrier.json`
- `data/w33_pass1102_1106_release.json`
- `hardware/w33_pass1105_keysight_n7731a_receipt.json`
- `tests/test_w33_pass1102_1106.py`
- `.github/workflows/pass1102_1106_exact.yml`
