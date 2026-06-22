# BT1422--BT1424: Fano 168, native K7 meshes, and CSS shear boundary

This packet executes the next three front-end moves and absorbs the Fano hint as a structural theorem rather than a numerology note.

## BT1422 — the 168 active bus is Fano

The active detector count

\[
168 = 21\cdot2\cdot4
\]

is exactly the Fano collineation group order:

\[
|GL(3,2)|=|PSL(2,7)|=168.
\]

The objectwise refinement is

\[
168 = 21\text{ Fano flags}\times 8\text{ flag-stabilizer states}.
\]

This matches the holonet front end:

\[
21\text{ edge channels}\times2\text{ orientations}\times4\text{ residues}=168.
\]

The 24 guard apertures are also Fano-native:

\[
24=|\operatorname{Stab}_{GL(3,2)}(p)|,
\]

the point stabilizer, i.e. the tetrahedral \(S_4\) guard. Hence

\[
192=168+24
\]

is a Fano orbit/stabilizer decomposition of the tomotope bus.

The S3 optimizer frontier now has a sharper front-end split:

\[
330=168+27\cdot6,
\qquad
210=21\cdot10.
\]

So the correction side is the Fano-active bus plus a Steinberg/S3 cache.

## BT1423 — native K7 star meshes replace abstract F6 analyzers

BT1419 used an abstract six-mode Fourier block \(F_6\). BT1423 replaces it by a native mesh on the line graph \(L(K_7)\).

A Cs\'asz\'ar/Szilassi star at a K7 vertex contains the six incident K7 edge channels. Inside \(L(K_7)\), those six channels form a \(K_6\) clique, with

\[
\binom{6}{2}=15
\]

native two-mode slots. Across all seven stars this gives

\[
7\cdot15=105
\]

native adjacent edge-channel pairs, exactly the edge count of \(L(K_7)\).

The verifier decomposes \(F_6\) into 15 complex Givens rotations plus a diagonal phase tail and reconstructs the Fourier target with error below \(10^{-10}\). Both Cs\'asz\'ar and Szilassi modes use seven such meshes, so the symbolic native slot total is

\[
2\cdot7\cdot15=210.
\]

The active detector count remains 168.

Boundary: this is still symbolic mesh synthesis, not a lithographic routing/loss model.

## BT1424 — D4 guard shear is not a silent CSS automorphism

BT1424 pushes the D4 guard shear through the actual \([[240,81,3]]_3\) CSS carrier. The shear acts on the 24 tail coordinates by

\[
216 + atom\cdot12 + branch\cdot3 + phase
\mapsto
216 + atom\cdot12 + branch\cdot3 + (phase+branch\bmod3).
\]

It moves 12 coordinates in four 3-cycles. The original CSS carrier has

\[
rank(H_X)=39,
\qquad
rank(H_Z)=120,
\qquad
k=81.
\]

The key result is negative and useful:

\[
\operatorname{rowspan}(H_X)\ne \operatorname{rowspan}(H_XJ),
\qquad
\operatorname{rowspan}(H_Z)\ne \operatorname{rowspan}(H_ZJ).
\]

The rank joins increase to

\[
rank(H_X,H_XJ)=45,
\qquad
rank(H_Z,H_ZJ)=128.
\]

Also, a one-sided shear breaks CSS commutation against the unchanged opposite stabilizer. But permuting both stabilizer sides together preserves CSS commutation and the code parameters. Therefore the D4 shear is not a free logical automorphism of the current identity-intertwined carrier. It is a retwined injection frame requiring an explicit CSS frame update/correction.

This is exactly the right boundary for the architecture: non-Clifford guard injection is real, but it cannot be smuggled through the protected memory without a tracked frame change.

## Verification commands

```bash
python tools/bt1422_fano_168_s3_optimizer_bridge.py
python tools/bt1423_native_k7_star_meshes.py
python tools/bt1424_d4_shear_css_logical_action.py
python -m pytest -q tests/test_bt1422_bt1424_fano_frontier.py
python -m py_compile tools/bt1422_fano_168_s3_optimizer_bridge.py tools/bt1423_native_k7_star_meshes.py tools/bt1424_d4_shear_css_logical_action.py tests/test_bt1422_bt1424_fano_frontier.py
```
