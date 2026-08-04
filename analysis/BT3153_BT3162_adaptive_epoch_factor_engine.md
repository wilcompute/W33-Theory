# Passes 3153–3162 — adaptive epoch factor engine

## Executive result

The five requested fronts now form one typed execution layer:

```text
rank-three candidate intake
  -> monotone promotion gate
  -> exact 3,697-factor belief update
  -> in-band edit-robust epoch
  -> causal/route/calibration collision price
  -> equal-footprint dual-ISA switch
```

The packet also exhausts every five- and six-opcode subset of the frozen affine library at
the universality, collision, frame-distance and spectral levels, then performs exact
4,199,040-state BFS on all eight non-dominated designs.

---

## 3153–3154 — every larger frozen-library ISA

There are

\[
\binom{10}{5}+\binom{10}{6}=252+210=462
\]

five- and six-generator subsets.  The library separates six zero-translation symplectic
maps from four pure translations, so universality is certified without a 4.2-million-state
closure for every subset:

\[
|\langle L\rangle|=51,840,
\qquad
\dim_{\mathbf F_3}\operatorname{span}(\langle L\rangle T)=4.
\]

Exact census:

| size | subsets | universal | minimum collisions | minimizers |
|---:|---:|---:|---:|---:|
| 5 | 252 | 80 | 45 | 4 |
| 6 | 210 | 114 | 63 | 8 |
| total | 462 | 194 | — | — |

Eight designs survive the joint non-dominance test over collision probability, 81-frame
mean distance, directed spectral radius and decoder-operation count.  Exact full-group BFS
was locally completed for all eight.

The strongest runtime candidate is

```text
F_f + CX_pf + CX_fp + Z0 + Z1 + Z3.
```

Its exact metrics are:

```text
full affine order          4,199,040
collisions                 63 / 486 = 0.1296296296
81-frame mean distance     3.5679012346
81-frame diameter          5
SLEM                       0.7732176173
full-group mean length     13.7293695702
full-group diameter        19
```

Its complete growth series is

```text
1, 6, 28, 116, 424, 1411, 4212, 11388, 28227, 65479,
138689, 262570, 453578, 709805, 935817, 894279, 531294,
151951, 9694, 71.
```

Comparison:

| ISA | opcodes | collision probability | mean length | diameter |
|---|---:|---:|---:|---:|
| current | 4 | 0.138888889 | 14.175585134 | 19 |
| low-collision equal-footprint | 4 | 0.111111111 | 15.216323969 | 20 |
| fast six-opcode | 6 | 0.129629630 | 13.729369570 | 19 |

Thus the six-opcode design strictly improves both runtime mean length and collision
exposure relative to the current ISA before decoder area and switching cost are charged.
It crosses the low-collision four-opcode design at collision/instruction price

\[
c=16.701642493.
\]

Below that price the six-opcode design has lower modeled runtime cost; above it the
36-collision four-opcode set wins.

**Boundary.** Universality, collisions, frame distances and spectral metrics are exact for
all 462 subsets.  Full-group BFS is locally observed for the eight non-dominated designs.
The committed exhaustive workflow must still run full BFS for all 194 universal subsets
before a global mean-distance optimum is claimed.

---

## 3155–3156 — the exact factor table becomes a seven-lane machine

The sparse posterior has

\[
1+315+3381=3697
\]

dynamic values.  Its interaction geometry gives a natural conflict-free banking:

- bank index: one of seven nonidentity \(D_4\) labels;
- unary address: one of 45 edges;
- correction address: one of 69 measured adjacent-edge pairs and one of seven left labels.

Therefore each bank has

\[
45+69\cdot7=528
\]

words.  A sweep is:

```text
45 unary cycles + 69×7 correction cycles = 528 cycles.
```

Seven 18-bit factors update on every accepted cycle.  The exact memory count is

\[
7\cdot528\cdot18+18=66,546\text{ bits}.
\]

Conservative bank-local iCE40 packing uses three 4-kbit EBRs per bank, or 21 EBRs total.
At a stated 100 MHz design point, not observed timing, the schedule corresponds to

\[
189,393.94\text{ factor sweeps/s}
\]

and 12.6 Gbit/s of internal factor-write bandwidth.

The RTL uses synchronous reads so the evidence lane tests block-RAM inference rather than
an accidental asynchronous LUT implementation.

---

## 3157–3158 — an epoch delimiter with a proof

The payload period is

```text
7, 2, 16, 23, 20, 15, 0, 2, 7, 11, 16, 19.
```

Symbols 1 and 22 are unused.  The epoch marker is

```text
1, 22, 1, 22, 1.
```

Every payload-only word contains zero marker-alphabet symbols.  Transforming any such word
of length \(L\) into the five-symbol marker requires at least

\[
\min(L,5)+|L-5|=\max(L,5)\ge5
\]

edits.  Hence the marker and payload radius-two Levenshtein balls are disjoint:

\[
\boxed{\text{two-edit false epoch acquisition is impossible}.}
\]

The RTL detects the surviving marker alphabet, then uses the already-proved unique cyclic
payload pairs to reacquire exact phase in two clean payload symbols.

Spacing remains a design choice:

| payload symbols between markers | overhead | maximum received symbols to robust confirmation |
|---:|---:|---:|
| 12 | 29.41% | 19 |
| 24 | 17.24% | 31 |
| 48 | 9.43% | 55 |
| 96 | 4.95% | 103 |
| 192 | 2.54% | 199 |
| 384 | 1.29% | 391 |
| 768 | 0.65% | 775 |

No additional optical symbol or mode is introduced.

**Boundary.** The delimiter theorem is adversarial and exact.  The committed detector's
post-marker two-symbol acquisition assumes those acquisition symbols are clean; the
existing edit-mask controller remains responsible for continuing edit corruption.
Laboratory confusion probabilities remain absent.

---

## 3159 — monotone promotion, not candidate optimism

The merged Pass 3125 packet supplies a duplicate-free engine for all 50,868,675 rank-three
isotropic subspaces, but its full census is still separately gated and no accepted
candidate has been observed.

The new intake recursively scans every Pass 3125 artifact and refuses to interpret no input
as a no-go.  Every candidate must first pass:

1. three independent commuting symplectic generators;
2. trace-eight Hermitian idempotent projector;
3. annihilation of all nine first-order error vectors;
4. nonzero clean success;
5. non-stabilizer accepted clean output.

Accepted candidates then receive:

- all 4,096 Hermitian Pauli expectations;
- a fixed-Weyl-frame qubit negativity witness;
- an exact maximum over 46,656 product stabilizer states, reported only as a lower bound on
  unrestricted stabilizer fidelity;
- a three-logical-qubit symplectic frame for the rank-three code;
- exact first- and second-order accepted-success and output-fidelity coefficients for the
  frozen independent local-error model.

Two larger quantities remain explicit exhaustive gates:

```text
maximal isotropic stabilizer subspaces     4,922,775
logical Clifford elements modulo phase   92,897,280
```

This is a monotone-analysis pipeline, not a candidate-existence claim.

---

## 3160 — adaptive equal-footprint ISA switching

For the two four-opcode designs,

\[
J_i(c)=\bar L_i+c\,\bar L_i p_i.
\]

The zero-switch crossover is

\[
c_0=3.741933824.
\]

With a 0.25-instruction switching cost, exact hysteresis thresholds are

\[
c_{\uparrow}=4.640798576,
\qquad
c_{\downarrow}=2.843069071.
\]

The programmable effective price is

\[
c_{\rm eff}=c_{\rm base}+0.35H_{\rm causal}+0.5R_{\rm route}
 +(1-\kappa_{\rm calibration}).
\]

The coefficients are controller parameters.  A low-collision decoder that is not marked
calibrated fails closed to the current ISA.  The six-opcode candidate remains an advisory
third mode until its larger decoder receives observed area and timing.

---

## Evidence ladder

- **Exact finite:** 462-set universality/collision/frame/spectral census; eight complete
  4,199,040-state BFS runs; 528-cycle bank schedule; edit-distance delimiter proof;
  dual-ISA crossover and hysteresis algebra.
- **Exact for explicit models:** runtime cost comparisons and error-slope definitions.
- **Source-complete:** larger-ISA exhaustive engine, seven-bank RTL, epoch tracker,
  monotone pipeline, adaptive scheduler, regressions, paper integrator and evidence lanes.
- **Pending:** all-194 full BFS workflow, accepted M36 candidate, exhaustive stabilizer
  fidelity/Clifford orbit, RTL simulation/synthesis/place, materialized front doors, PDFs,
  and all laboratory behavior.
