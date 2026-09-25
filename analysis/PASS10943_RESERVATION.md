# Pass 10943 — protected metaplectic VM five-front closure

Pass 10942 built an exact Strange-to-reflection converter and proved that its
raw depolarizing error is amplified. This packet closes the missing protected
supply chain while keeping the hardware boundary explicit.

## 1. Protected Strange-to-R composition

The ternary Golay `[[11,1,5]]_3` Strange-state protocol of Prakash (2020) has

```text
delta_out = delta^3 P(delta)/(2 Q(delta))
          = (55/18) delta^3 + O(delta^4).
```

Composing that map with the exact Pass 10942 converter gives

```text
q_R(delta) = (220/27) delta^3 + O(delta^4).
```

The first nonzero fixed point is `0.2715245018525886`; below it, the complete
distill-then-convert path improves error. At input error 0.1, two Golay rounds
put the converted R state below `1e-6`. In the pure-input acceptance limit,
one round costs 1,824,768 raw Strange states per successful injected R gate;
two rounds cost 34,685,190,144. These are exact architecture ledgers, not
claims of practical optimality.

## 2. Exact dark-Strange preparation target

With `|N>=(|1>+|2>)/sqrt(2)`, the two jumps

```text
L0 = sqrt(gamma) |S><0|,    LN = sqrt(gamma) |S><N|
```

have the unique steady state `|S><S|`. At unit gamma the nine-dimensional
Liouvillian spectrum is `{0^1, (-1/2)^4, (-1)^4}`, so the gap is `gamma/2`.
The parent Hamiltonian `I-|S><S|` has spectrum `{0^1,1^2}`. This is an exact
reservoir-engineering specification. It does not derive gamma or show that
the current Holonet device implements either jump.

## 3. Fault-tolerant logical ABI

The committed five-row ternary generator is self-orthogonal, has `|C|=243`,
`|C^perp|=729`, minimum weight six in C, and minimum weight five in
`C^perp-C`. It therefore replays the `[[11,1,5]]_3` CSS code and corrects any
two physical qutrit errors. The certificate counts all 3,609 Pauli errors of
weight at most two and compiles the Strange-to-Norell, Norell-to-R, and RUS
injection measurements to logical Pauli operations. Circuit-level syndrome
extraction and malignant-pair counting remain open.

## 4. M36 is a direct qutrit-resource transducer in a fixed gauge

For every one of the 36 committed four-mode M36 rays, delete its exactly dark
mode and relabel the three active modes as a qutrit. Exhaustive classification
gives

```text
27 rays -> qutrit R-magic Clifford orbit
 9 rays -> qutrit stabilizer states.
```

There are 18 distinct R-orbit outputs and nine distinct stabilizer outputs;
the shortest correction to canonical `|R>` has Clifford word length at most
four. A selected R-producing family costs one M36 state per R state and three
M36 states per successful RUS injection. If the ray is uniformly unknown,
the R yield is `3/4`, giving expected costs `4/3` and four respectively.

This map changes the encoding from four optical modes to one qutrit and is
conditioned on the known family. It is not a two-qubit Clifford operation, so
there is no magic-monotonicity contradiction. All 216 permutations of the
three surviving output coordinates preserve the classification.

The parallel temporal atlas sharpens the control architecture. One two-bit
M36 family selector now names all of the following:

- the dark optical mode and three-mode partial isometry;
- one projective null direction in `Sym2(F3)`;
- one Hesse striation and one temporal E8 A2 component, with six choices of
  origin and orientation for the exact `2+27+54+82+54+27+2` parabolic clock;
- an R-magic output for families A, B, C, or a stabilizer calibration output
  for family D in the canonical ROM phase gauge.

The Hesse affine symmetry treats the four striations equivalently. Therefore
the 3+1 resource split is a programmable optical gauge assignment, not an
intrinsic preferred null direction or an arrow of time.

## 5. R/T instruction economy

The seven-qutrit VM now has two typed non-Clifford opcodes. Native R injection
uses three selected M36 states, or 96 protected Strange states when supplied
through the exact converter. The literature construction of `R tensor I`
from Clifford+T uses one returned borrowed qutrit and 39 T gates. Thus native
R is cheaper when one T resource costs more than `32/13` distilled-Strange
units. Exact Clifford+R remains a strict subset of exact Clifford+T: no number
of R ancillas produces exact T, while a lone qutrit cannot produce exact R from
Clifford+T.

## Corrected boundary

The earlier repository wording that matter equals magic and therefore removes
the distillation factory was an over-read. The finite geometry certifies a
contextual inventory. A protected supply requires the Golay path, the exact
dissipative pump if physically built, or the calibrated four-to-three-mode M36
interface. No component error rates, syndrome circuit threshold, fabricated
mode interface, or device measurement are claimed.

The executable witness is
`analysis/w33_pass10943_protected_metaplectic_five_front.py`; its frozen output
is `data/w33_pass10943_protected_metaplectic_five_front.json`.
