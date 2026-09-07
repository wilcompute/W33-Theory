# Passes 2917–2923 — Seven-Front Breakthrough Packet

## Pass 2917 — seven-bit rank-coded frame engine

The base-three rank `27*xp + 9*zp + 3*xf + zf` is a bijection from the 81 frames to
`0..80`. The new synthesizable engine stores that rank in seven flip-flops and implements
all four micro-operations. The Python truth model closes 324/324 transitions and the
SystemVerilog testbench repeats the exhaustive check. Cell count and timing are deliberately
left pending until the dedicated workflow observes Yosys and nextpnr.

## Pass 2918 — complete first-order M36 census

Pass 2861's no-quadratic theorem excluded slope zero but did not establish that 2/3 was the
best positive slope. The full census supplies the missing implication. Deep class: 3393
closed branches, 48 improving; 12 have slope `2/3`, 36 have exact slope
`2 - 2*sqrt(3)/3`. The other three classes have minimum slope one. An accepted-output
mixture has slope `sum(w*q0*a)/sum(w*q0)`, so randomized or syndrome-conditioned mixing
cannot beat the minimum or cancel the linear term.

## Pass 2919 — antiunitary chirality of the middle classes

Complex conjugation swaps the middle 12-ray classes and fixes the shallow/deep classes
setwise. Their complete stabilizer-overlap probability spectra coincide. Odd-Y Pauli
expectations reverse sign; even-Y expectations match. This gives a phase-sensitive
operational separator relative to a fixed Pauli frame.

## Pass 2920 — adaptive diagnosis and representation-specific Landauer costs

The exact adaptive observer is rebuilt at worst depth four and uniform mean 94/27. Repeated
count-vector MAP routing is evaluated exactly under four independent asymmetric detector
models. Three samples per decision improve all four modelled channels.

The prior phrase “8/3 bits per support readout” is corrected. `8/3` is the conditional
phase entropy discarded after retaining support. The support outcome entropy is 3.673183
bits, a compressed exact identification transcript is `log2(81)=6.339850` bits, and naive
four-bit snapshot reset costs `484/27` bits on average.

## Pass 2922 — outside-box line-stabilizer falsifier

The 1296-element setwise stabilizer of the distinguished classical line is transitive on
all 36 magic points. Its 54-element pointwise stabilizer yields four 9-point coordinate
families. Neither produces the Clifford `4+8+12+12` split. The split needs structure beyond
the finite geometry plus chosen line.

## Pass 2923 — outside-box diameter-shell classification

All 4,199,040 affine transformations are searched again. The 188 depth-19 elements form 25
algebraic profiles. Affine-order histogram: `4:110, 5:6, 6:2, 8:22, 9:2, 10:6, 12:32,
18:8`. Fixed frames: `0:12, 1:174, 3:2`. Inverse depths: `16:18, 17:46, 18:48, 19:76`.
The profile partition is exact but is not yet called a conjugacy-class decomposition.
