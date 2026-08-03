# Passes 2803–2807 — minimal frame silicon, M36 distillation, sensor scaling, transpose closure, and mixer retirement

## 2803 — exact two-bit affine frame engine

Among the six individual linear frame generators, no pair generates the full symplectic group, while exactly six triples do. The selected triple

`F_p, CX_p->f, CX_f->p`

generates all `51,840` elements of `Sp(4,3)`. The orbit of one nonzero translation `Z_p` contains all 80 nonzero frame vectors and spans all 81 translations, so the four-operation micro-ISA generates

`81 * 51,840 = 4,199,040 = |ASp(4,3)|`.

The micro-engine uses two opcode bits. This is an internal execution layer, not a silent reassignment of the public three-bit Holonet ISA.

## 2804 — deep M36 resources are two-copy distillable

The 11,520-element projective two-qubit Clifford group splits the 36 Witting resources into four state orbits of sizes

`960, 2880, 2880, 640`.

The search exhausts every one of the 5,355 binary `[[4,2]]` stabilizer projectors, all four syndromes, and full logical Clifford decoding. The shallow and both middle orbits have no improving branch. The deep eight-ray grade has exactly 48 improving branches.

One explicit branch uses input ray 5, stabilizers `IYZY` and `YZXY`, syndrome `(-1,+1)`, and a Hadamard on the second logical qubit, producing ray 7. With input depolarization parameter `p`,

`P_success=(p^2-2p+2)/4`,

`F_out=(5p^2-12p+8)/(4(p^2-2p+2))`,

and

`F_out-F_in=p(p-1)(3p-2)/(4(p^2-2p+2))`.

Thus fidelity improves for every `0<p<2/3`, which contains the full deep magic-witness interval

`0<p<(8-2sqrt(3))/9`.

This reverses the earlier arbitrary-decoder no-go. The earlier search fixed an arbitrary logical basis phase and did not exhaust logical Cliffords.

## 2805 — n-qutrit sensor exponent

For the standard finite qutrit Clifford lift, the scalar subgroup is `mu_12`. On an n-qutrit register of dimension `d=3^n`,

`Tr(U^k)^e/det(U^k)`

is phase invariant for `k=1,2` exactly when `e=d mod 12`. Consequently the minimal finite-lift exponent alternates:

- odd n: `e=3`;
- even n: `e=9`.

For arbitrary `U(1)` representative phases rather than the standard finite lift, the exponent must remain the full dimension `3^n`.

## 2806 — transpose and gate-direction closure at q=5 and q=7

The same involution satisfies

`T^2=I`, `T^T J T=-J`, and `T CX_p->f T^-1=CX_f->p`.

The reverse controlled-add also equals the local-Fourier conjugate of the forward gate. At q=5, `-1` is a square and `2T` is symplectic, so the projective class is inner. At q=7, `-1` is nonsquare and the class is the nontrivial diagonal outer class. This objectwise test closes the q=5/q=7 scope boundary.

## 2807 — the dead mixer is removed

`rtl/w33_spread_mixer36.sv` was rejected by both Icarus and Yosys. The synthesizable packed-bus port is already available as `rtl/w33_pass2773_spread_mixer36_synth.sv`. Pass 2807 removes the dead source, points the exact arithmetic verifier and frozen certificate to the live source, and updates the legacy workflow trigger.

## Evidence boundary

The exact Python jobs establish the finite group, code, phase, and modular-matrix claims. Icarus/Yosys/nextpnr results are promoted only after the dedicated workflow is observed. The M36 theorem is a state-fidelity distillation result, not yet a fault-tolerant injection threshold or asymptotic yield theorem.
