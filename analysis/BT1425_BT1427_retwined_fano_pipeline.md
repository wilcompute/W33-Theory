# BT1425--BT1427: retwined CSS frame, Fano quotient, and end-to-end optical simulation

This packet executes the next three moves and folds in a deeper repo search across the Fano/Hamming bridge, Fano group bridge, holonet TeX, and Q4 diamond TeX layers.

## Repo hints used

The existing Fano/Hamming bridge already states the key identity:

\[
|Aut(Fano)|=|GL(3,2)|=|PSL(2,7)|=168.
\]

It also records that the Fano plane has 7 points, 7 lines, and 21 incidences, and that

\[
168\cdot240=8!.
\]

The Fano group bridge then upgrades the count to an orbit/stabilizer mechanism:

\[
168 = 21\text{ Fano flags}\times 8\text{ flag stabilizer states},
\]

while the point stabilizer has order 24.  This is the exact source of the active/guard split

\[
192=168+24.
\]

## BT1425 — retwined CSS frame correction

BT1424 proved that the D4 guard shear is not a silent automorphism of the identity-intertwined CSS carrier.  BT1425 supplies the missing companion operation.

Let \(J\) be the guard-tail column permutation

\[
216+a\cdot12+b\cdot3+p \mapsto 216+a\cdot12+b\cdot3+(p+b\bmod3).
\]

The companion correction is:

1. update the tracked Pauli/error coordinate frame by the same old-to-new map \(J\);
2. replace the stabilizer matrices by the retwined matrices
   \[
   H_X' = H_XJ^{-1},\qquad H_Z'=H_ZJ^{-1};
   \]
3. decode syndromes in the retwined frame.

The verifier checks the exact invariant:

\[
\operatorname{syn}_{H}(e)=\operatorname{syn}_{H'}(Je)
\]

for every basis error coordinate and both nonzero qutrit values \(1,2\).  It also confirms that the retwined carrier still has

\[
rank(H_X')=39,
\qquad
rank(H_Z')=120,
\qquad
k=81,
\]

and that one-sided retwining fails commutation.  So the operational rule is exact: the D4 guard shear is legal only as a tracked frame transition.

## BT1426 — Fano-quotiented S3 optimizer frontier

BT1426 applies the Fano active symmetry to the objective packetization of the S3 Max-2CSP frontier.  It does not claim that the Fano group already acts on the 40 W33 line variables.  Instead it gives a weighted quotient of the physical objective constraints:

\[
210 = 21\cdot10,
\]

\[
330 = 168+162 = 21\cdot8 + 27\cdot6.
\]

Thus the raw 540 terms compress to

\[
21 + 21 + 27 = 69
\]

weighted packet representatives.  The correction side compresses to

\[
21+27=48
\]

representatives.  The packet weights are \(10,8,6\), so the packet-symmetric score step has gcd 2.  Consequently, inside a Fano-packet-symmetric subproblem, a better score cannot be 211; the next possible score above 210 is 212, i.e. correction score 328.

The full problem remains open, but the quotient gives a sharper exact attack surface: prove the weighted packet objective is bounded by 210, then either lift that certificate or identify the symmetry-breaking terms needed by a 211 witness.

## BT1427 — end-to-end Fano optical simulator

BT1427 simulates the complete symbolic front-end trace:

\[
Fano\ flag \to K_7\ edge\ channel \to K_7\ star\ mesh \to active\ detector\ bin \to CSS\ frame\ update.
\]

The active trace has 168 events:

\[
21\text{ flags}\times2\text{ orientations}\times4\text{ residues}=168.
\]

Every K7 channel has 8 active events, and every K7 star mesh has 24 active events.  The 24 guard events are separated from the active mesh; exactly 12 of them trigger the nontrivial D4 retwined CSS frame update from BT1425.

This closes the symbolic front-end loop:

\[
168_{active}+24_{guard}=192_{tomotope\ bus}.
\]

## Verification commands

```bash
python tools/bt1425_retwined_css_frame_correction.py
python tools/bt1426_fano_quotiented_s3_optimizer.py
python tools/bt1427_end_to_end_fano_optical_simulator.py
python -m pytest -q tests/test_bt1425_bt1427_retwined_fano_pipeline.py
python -m py_compile tools/bt1425_retwined_css_frame_correction.py tools/bt1426_fano_quotiented_s3_optimizer.py tools/bt1427_end_to_end_fano_optical_simulator.py tests/test_bt1425_bt1427_retwined_fano_pipeline.py
```
