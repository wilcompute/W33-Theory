# BT1428--BT1430: 211 defect frontier, retwined pulse scheduler, and Fano-bus Holonet pass

## BT1428 — symmetry-breaking 211 frontier

BT1426 showed that the Fano-packet-symmetric weighted quotient cannot realize a one-unit improvement over the current score:

\[
210\to211
\]

because the packet weights are

\[
10,8,6,
\]

with gcd \(2\).  The next packet-symmetric score above \(210\) is \(212\), not \(211\).

BT1428 therefore enumerates the exact one-defect frontier that any 211 witness must hit.  A 211 witness must split one raw correction slot out of a packet orbit:

\[
330=168+162.
\]

The defect families are:

\[
168=21\text{ Fano flags}\times8\text{ local stabilizer states},
\]

and

\[
162=27\text{ Steinberg cycles}\times6\text{ S3 labels}.
\]

Thus there are exactly

\[
168+162=330
\]

minimal one-defect targets.  The BT1376 radius certificate still applies, so a full 211 gauge must also be at S3-label radius at least 4 from the current incumbent.

Boundary: this is not a global Max-2CSP solve.  It is the exact symmetry-breaking search contract for the next solver.

## BT1429 — retwined pulse scheduler

BT1429 turns the BT1425 retwined frame rule into a symbolic control schedule.  The schedule has two phases:

\[
168\text{ active optical detection pulses}
\]

followed by

\[
24\text{ guard-frame pulses}.
\]

Every K7 channel appears in eight active pulses, and every K7 star mesh sees 24 active pulses.  The guard phase contains 24 apertures; exactly 12 are nontrivial and trigger the D4 retwined CSS frame update.

The frame update program is:

\[
e\mapsto Je,
\qquad
H_X\mapsto H_XJ^{-1},
\qquad
H_Z\mapsto H_ZJ^{-1}.
\]

Active detector bins use identity frame tracking.  Guard apertures either sample identity or run the retwining program.

Boundary: this is a symbolic pulse/control schedule, not analog optical calibration.

## BT1430 — Fano-bus Holonet integration pass

BT1430 adds a master TeX insert and idempotent splicer for the Fano-bus closure.  The paper-level law is:

\[
168=21\cdot8=|GL(3,2)|=|PSL(2,7)|,
\]

\[
24=|\operatorname{Stab}_{GL(3,2)}(p)|,
\]

and

\[
192=168+24.
\]

The insert includes a TikZ figure showing:

\[
Fano\ plane\to active\ optical\ bus\to tomotope\ bus,
\]

with the separated guard rail feeding the retwined CSS frame.

Connector boundary: the pass added the master insert and exact splicer.  It did not rebuild `photonic_holonet.pdf` in place because the connector interface does not safely execute the full local LaTeX toolchain here.

## Verification commands

```bash
python tools/bt1428_symmetry_breaking_211_search.py
python tools/bt1429_retwined_pulse_scheduler.py
python tools/bt1430_fano_holonet_integration_manifest.py
python -m pytest -q tests/test_bt1428_bt1430_symmetry_pulse_integration.py
python -m py_compile tools/bt1428_symmetry_breaking_211_search.py tools/bt1429_retwined_pulse_scheduler.py tools/bt1430_fano_holonet_integration_manifest.py tests/test_bt1428_bt1430_symmetry_pulse_integration.py
```
