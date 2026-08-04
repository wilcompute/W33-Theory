# Passes 3143–3152 — five-front closure

## Executive result

All five requested fronts are now source-complete on a branch stacked over the Passes
3133–3142 certifying controller.  The main architectural chain is:

```text
parallel rank-three candidate
  -> independent fail-closed intake
  -> sparse exact D4 posterior
  -> mutual-information action
  -> epoch-typed edit synchronizer
  -> isolated recursive context
  -> calibrated sensor/ISA dispatch
  -> explicit reset
```

The packet produced one correction that materially changes the machine design.  The
previous 18-collision generator set is connected on the 81 frame vectors but generates
only 243 affine transformations.  It is not a universal replacement ISA.  Exhaustive
classification of all 210 frozen four-generator choices finds 24 universal choices and a
true universal minimum of 36 collisions.

---

## 3143 — every available rank-three candidate is independently certified

The repository currently contains no Pass 3125 rank-three candidate file or branch.  The
new intake searches every `data/*.json` file whose name contains `BT3125`, `rank3`, and
`candidate`, loads the independent Pass 3134 certifier, and records one of four typed
states:

```text
NO_INPUTS_DISCOVERED
ALL_DISCOVERED_CANDIDATES_REJECTED
ACCEPTED_CANDIDATES_PRESENT
MALFORMED_INPUT_FAIL_CLOSED
```

The present state is:

```text
source files discovered     0
candidate records           0
accepted records            0
status                      NO_INPUTS_DISCOVERED
```

This is deliberately not called a no-go result.  The instant a parallel Pass 3125 file is
published, the focused workflow will check binary rank, commutation, trace-eight
idempotence, annihilation of all nine single errors, nonzero clean success, and
non-stabilizerness of the accepted clean output through an implementation independent of
the search.

---

## 3144 — the full posterior has an exact 3,697-factor representation

The dense filter stores one weight for each of 48,826 hypotheses.  That is unnecessary.
For the 23 frozen base triangles, every hypothesis has support zero, one, or two.

Let `L_0` be the likelihood of the no-fault hypothesis.  For an atomic fault `a`, define
its unary likelihood ratio

```text
U_a = L_a / L_0.
```

For a two-fault hypothesis `(a,b)`, two distinct edges of `K_10` are either disjoint or
share exactly one triangle.

- If the edges are disjoint, no tested triangle contains both faults, so
  `L_ab / L_0 = U_a U_b` exactly.
- If the edges are adjacent but their shared triangle is not among the 23 tests, the same
  identity holds.
- If their unique shared triangle is tested, one noncommutative correction is required:

```text
C_ab(y) = P(y | symbol_ab) P(y | identity)
          ---------------------------------
          P(y | symbol_a) P(y | symbol_b)
```

and

```text
L_ab / L_0 = U_a U_b C_ab.
```

The 23 triangles contain three adjacent edge pairs each, and an adjacent edge pair belongs
to only one triangle.  Hence the dynamic factor count is

```text
baseline                                      1
atomic edge/group unaries                   315
23 triangles x 3 edge pairs x 7 x 7       3,381
                                             -----
total                                      3,697
```

against 48,826 dense weights.  Therefore:

```text
dynamic-value reduction    92.4282144759%
compression ratio          13.2069245334x
```

The identity is algebraic and holds for every observation transcript under any
row-memoryless D4 symbol channel.  As a regression, 32 noisy transcripts were evaluated
both ways.  Results:

```text
maximum log-weight error       5.6843418861e-14
maximum posterior error        1.6653345369e-15
maximum action-score error     3.1086244690e-15
next mutual-information action 32 / 32 identical
```

The action test scores all 97 unused triangles by one-step mutual information.  Thus the
compression preserves not merely approximate beliefs but the exact action chosen by the
frozen policy, up to floating-point evaluation of an algebraic identity.

---

## 3145 — clean blind acquisition is two symbols; blind insdel correction is impossible

The combined omitted-slot and pilot-order stream is

```text
7, 2, 16, 23, 20, 15, 0, 2, 7, 11, 16, 19
```

over a 24-symbol alphabet.  Every one of its twelve cyclic length-two words is distinct.
Therefore clean blind phase acquisition requires exactly two received symbols.

There is also a necessary impossibility result.  For every sequence, every phase, and every
finite length `L`, the phase-`p+1` word can be obtained from the phase-`p` word by deleting
the first symbol and appending one symbol.  Adjacent phase words therefore have
Levenshtein distance at most two for every `L`.  Their one-edit balls intersect.

Consequently:

> Blind insertion/deletion correction with no absolute epoch is impossible, regardless of
> how long the periodic word is observed.

This is not a weakness of the chosen 24-symbol sequence; it is the unavoidable distinction
between phase and an edit.  The physical controller must supply a trusted reset, source
tick, or equivalent epoch whenever insdel correction is required.

---

## 3146 — every two-edit burst relocks within four received symbols

With phase locked before the burst, the exact transducer allows at most two operations from

```text
substitution, insertion, deletion
```

whose source positions lie in a six-symbol window.  All clean placements, operation types,
inserted/substituted symbols, cancellations, and duplicate scripts are generated and
collapsed by identical observation-plus-phase histories.

The finite object contains:

```text
distinct observation/phase traces    41,641
```

Every trace relocks after the source window closes:

| received symbols to relock | traces |
|---:|---:|
| 1 | 34,411 |
| 2 | 7,148 |
| 3 | 81 |
| 4 | 1 |

Thus:

```text
worst-case relock delay = 4 received symbols
unresolved traces       = 0
```

The RTL uses a three-layer, twelve-phase Levenshtein mask bank.  The layers represent zero,
one, and two edits used; insertion consumes an observed symbol without advancing phase,
deletion advances phase through epsilon closure, and substitution consumes and advances.
Each guest owns private masks.  With a source-tick window-close signal, the same automaton
collapses within at most two clean symbols after closure; the four-symbol theorem requires
no such externally aligned close pulse beyond the frozen six-source-symbol model.

---

## 3147 — the 18-collision ISA was not universal

The frozen candidate library has ten generators:

```text
F_p, F_f, S_p, S_f, CX_pf, CX_fp, Z0, Z1, Z2, Z3.
```

All `C(10,4)=210` four-generator sets were classified by:

1. exact linear subgroup order;
2. dimension of the invariant translation span;
3. total affine order `|L| 3^d`;
4. collision count on the 324 labeled outgoing frame edges.

The full affine target has order

```text
51,840 x 81 = 4,199,040.
```

The previously selected set

```text
CX_fp + Z0 + Z1 + Z2
```

generates only

```text
243 = 3^5
```

affine transformations.  Its 18 collisions are real, but it is not a universal ISA.  The
prior “minimum collision cost of computing” used connectivity on 81 frame vectors as a
surrogate for generation of the complete affine group; that surrogate was insufficient.

The corrected exhaustive result is:

```text
four-generator sets checked           210
universal four-generator sets           24
minimum universal collision count       36
sets attaining the minimum                8
```

The lexicographically first minimum choice is

```text
CX_fp + CX_pf + F_f + Z0.
```

### Exact full-group growth comparison

Both the current and selected alternative were breadth-first enumerated on all 4,199,040
affine transformations.

| metric | current `F_p,CX_pf,CX_fp,Z1` | alternative `CX_fp,CX_pf,F_f,Z0` |
|---|---:|---:|
| collisions | 45 | 36 |
| diameter | 19 | 20 |
| mean length | 14.175585134 | 15.216323969 |
| standard deviation | 1.768246753 | 1.812848419 |
| modal length | 15 | 16 |

Current growth series:

```text
1, 4, 15, 53, 176, 547, 1630, 4648, 12729, 33142,
81619, 184858, 365370, 623863, 909304, 1002688, 696532,
255270, 26403, 188
```

Alternative growth series:

```text
1, 4, 14, 45, 135, 379, 1015, 2620, 6638, 16242,
37723, 83630, 177084, 346856, 598578, 875149, 1000588,
748566, 277761, 25952, 60
```

The alternative pays 1.040738836 extra mean instructions.  Including each ISA’s own
collision exposure, it becomes cheaper only when

```text
collision-resolution cost / instruction cost > 3.7419338235.
```

So the correct decision is conditional:

```text
ratio below 3.74193   -> keep the current ISA
ratio above 3.74193   -> use the 36-collision universal ISA
```

At equal costs, the current ISA wins.  The earlier one-instruction break-even conclusion is
withdrawn because it compared the current ISA to a nonuniversal 243-element subgroup.

---

## 3148 — resource-comparable ISA dispatch hardware

A parameterized SystemVerilog dispatcher implements both four-opcode maps over the four
F3 frame coordinates.  Both variants expose the same input/output shape and opcode width,
so synthesis can compare them without wrapper bias.

Current map:

```text
F_p, CX_pf, CX_fp, Z1
```

Alternative map:

```text
CX_fp, CX_pf, F_f, Z0
```

The testbench checks representative affine outputs for both.  Cell count, critical path,
and placed frequency remain pending the focused workflow.

---

## 3149 — recursive inference is one physical controller

The controller now contains:

- the five Q1.15 D4 Fourier prediction lanes;
- sixteen private nine-bit causal contexts;
- sixteen private three-layer edit-mask contexts;
- the frozen action-rate-distortion selector;
- explicit per-context reset;
- a shared double-buffered calibration store;
- one aggregate update per cycle with deterministic round-robin continuation;
- both current and alternative ISA dispatch maps for measured selection.

The context boundary is structural.  A write names exactly one context index; no write path
exists from that operation to another context’s causal state or edit masks.

The eleven-point action frontier is compiled to four sensing classes:

```text
budget tiers 0..3   STOP / no route sensing
budget tiers 4..5   V4 sensing
budget tiers 6..9   conjugacy-class sensing
budget tier 10      full D4 sensing
```

The generated policy ROM may refine the tier-to-action table, but the physical integration
and reset semantics are fixed.

---

## 3150 — memory and bandwidth close numerically

At eighteen bits per log factor:

```text
dense posterior storage     878,868 bits = 109,858.5 bytes
sparse factor storage        66,546 bits =   8,318.25 bytes
```

A one-factor-per-cycle design point at 100 MHz gives:

```text
dense sweep       48,826 cycles     2,048.089 sweeps/s
sparse sweep       3,697 cycles    27,048.959 sweeps/s
throughput gain                         13.2069x
```

The calibration matrix has `8 x 9 = 72` entries.  Two sixteen-bit banks require 2,304
bits and permit an inactive bank to load before one atomic commit toggles the active bank.

Each recursive guest stores:

```text
causal state                 9 bits
three twelve-phase masks    36 bits
action                       4 bits
valid                         1 bit
                            -------
                              50 bits
```

Sixteen guests therefore require 800 context bits before implementation-specific packing.
The shared engine sustains one aggregate context update per cycle and one update per guest
every sixteen cycles under strict round-robin scheduling.

The 100 MHz figures are an explicit design point, not observed placed timing.

---

## 3151–3152 — publication and evidence contract

The paper, Photonic Holonet, machine blueprint, and site insert are reorganized around:

```text
candidate -> certifier -> sparse posterior -> costed action
          -> edit mask -> recursive context -> calibrated dispatch -> reset
```

Required corrections carried into every front door:

1. no Pass 3125 input is not a no-go result;
2. the sparse posterior is exact because support is at most two and adjacent edges share at
   most one tested triangle;
3. blind clean phase acquisition and blind insdel correction are different problems;
4. the 18-collision set is nonuniversal and cannot price universal computation;
5. 100 MHz throughput, FPGA area, timing, and optical behavior remain unobserved until the
   dedicated lane passes.

The focused lane must regenerate both Python certificates, run the candidate intake, run
pytest, simulate the old and new controllers, synthesize and place both ISA dispatchers and
the recursive top, prove front-door idempotence, and compile all three PDFs before merge.
