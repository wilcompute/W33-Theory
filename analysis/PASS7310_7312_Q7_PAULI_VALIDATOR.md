# Passes 7310–7312 — a proof-carrying q=7 Pauli validator

## Result

The packet-owned 33-point snapshot in
`data/PART_W33_PASS7310_Q7_HARDWARE_WITNESS.json` now has a synthesizable,
independently replayed hardware verifier.  Its provenance points to the upstream
`data/PART_W33_Q7_LNS_OVOID_33.json`, but no test depends on that parallel-owned
mutable path.  The snapshot's 528 unordered
pairs satisfy

\[
  x_0y_1-x_1y_0+x_2y_3-x_3y_2\ne0\pmod 7.
\]

Under the Pass 7204 dictionary this is exactly the statement that the 33
projective Weyl–Heisenberg labels form a pairwise noncommuting family.  The
hardware verifies this supplied construction; it does not search for it and it
does not prove that 33 is maximum.

The architecture is deliberately proof-carrying rather than orbit-generating.
Replaying Pass 7215's exhaustive scalar-realisation method on this exact
snapshot gives a coloured/projective-conformal stabilizer of order two.  The
typed distinction from Passes 7313–7316 is load-bearing: the one nonidentity
map has nonsquare similitude multiplier at q=7, so it lies in PCSp but outside
PSp.  Therefore the standard Clifford/PSp stabilizer is trivial, while the
larger commutation-preserving PCSp stabilizer is \(C_2\).  Clifford symmetry does
not compress the certificate at all.  If the broader conformal map is admitted,
it fixes one selected label and pairs the other 32, giving exactly 17 orbit
seeds.  A loadable certificate plus a complete pair checker remains the honest
build.

## Exact arithmetic and the gauge firewall

GAP independently reads the frozen 33-point list embedded from the source of
record, rejects illegal or zero vectors, recomputes all 528 products, and checks
the RTL packing.  It obtains

| representatives | counts at residues 0,1,2,3,4,5,6 |
|---|---|
| canonical source | 0, 88, 90, 94, 90, 90, 76 |
| independently rescaled | 0, 73, 120, 80, 81, 88, 86 |

This is a useful negative result: the six nonzero-bin populations are not
projective invariants.  Only zero versus nonzero survives independent rescaling.
Accordingly, the production RTL exports `inputs_valid` and `noncommute`; it does
not expose a coordinate-dependent phase label as geometry.

The optimized pair core uses \(7=2^3-1\).  A six-bit product reduces modulo seven
by adding its low and high three-bit chunks, followed by at most one subtraction
of seven.  Yosys SAT proves this circuit equal to both the signed integer formula
and a deliberately naive `% 7` implementation for every one of the
\(2^{24}=16,777,216\) raw input assignments.  The proof used 20,319 SAT
variables and 59,982 clauses and returned `SUCCESS`.

## Measured architecture frontier

All figures below are from Yosys 0.33 `synth_ice40`, not estimates from source
lines.

| design | SB_LUT4 | SB_CARRY | FF | BRAM | complete-check latency |
|---|---:|---:|---:|---:|---:|
| naive one-pair core | 528 | 262 | 0 | 0 | combinational |
| Mersenne one-pair core | 129 | 40 | 0 | 0 | combinational |
| 528-pair parallel endpoint | 58,462 | 21,120 | 0 | 0 | combinational |
| register serial | 1,637 | 63 | 814 | 0 | 562 cycles |
| synchronous-BRAM serial | 196 | 63 | 48 | 1 | 1,618 cycles |

The cycle counts include 33 loads and the final `done` cycle:
\(33+528+1=562\), and \(33+3\cdot528+1=1618\).  Icarus accepts the exact
certificate and rejects a deterministic corruption in which point 1 is replaced
by point 0 in all three architectures.

The BRAM architecture is the strongest build: compared with register serial it
trades 1,056 cycles for a reduction from 1,637 to 196 LUT4s and from 814 to 48
flip-flops.  It infers one `SB_RAM40_4K`; the 396-bit certificate is data rather
than hardwired theorem-specific logic.

A deterministic nextpnr 0.10 proxy on iCE40HX8K-CT256, seed 7310 and a 12 MHz
target, routed both serial designs:

| design | routed logic cells | block RAM | final reported Fmax |
|---|---:|---:|---:|
| register serial | 2,439 / 7,680 | 0 | 31.80 MHz |
| synchronous-BRAM serial | 230 / 7,680 | 1 / 32 | 41.31 MHz |

The run used unconstrained IO, so these are seeded place-and-route proxies—not
board timing, IO validation, power measurements, or device results.  nextpnr
describes itself as a timing-driven FPGA place-and-route tool; the distinction
between this output and measurement is intentional
([official project](https://github.com/YosysHQ/nextpnr)).

## Ownership and external boundary

This packet does not rediscover the Pauli dictionary.  Passes 5351–5352 own its
explicit q=2 form, Pass 7204 owns the odd-q translation, and Pass 7215 owns the
exhaustive projective-realisation method used here.  Passes 7313–7316 own the
typed correction: PSp is the standard projective Clifford carrier, whereas the
larger PCSp can contain non-Clifford conformal maps.  This exact replay gives
PSp order one and PCSp order two, so the two numbers are not conflated.  Pass
2966 is the earlier GF(3) one-pair commutator RTL;
Pass 4398 owns the prior finite-field datapath pricing method; Passes 2772–2776
own the warning that a synthesized circuit cannot by itself recover a larger
cross-output mathematical invariant.

The standard finite-dimensional Pauli/Clifford arithmetic background is
described by Hostens, Dehaene and De Moor
([arXiv:quant-ph/0408190](https://arxiv.org/abs/quant-ph/0408190)).  The q=7
partial-ovoid search sits in the computational generalized-quadrangle literature
of Cimráková and Fack
([publication record](https://biblio.ugent.be/publication/358180)).  Yosys's
`-prove-asserts` operation has the documented meaning used here
([formal documentation](https://yosyshq.readthedocs.io/projects/yosys/en/v0.59.1/cmd/index_formal.html)).

The theorem boundary is strict: this is a finite GF(7) Weyl–Heisenberg
commutator certificate validator.  It is not quantum state preparation, a
quantum experiment, dynamics, an energy or mass model, continuum physics, or a
proof of the maximum partial-ovoid size.

## Reproduction

```bash
gap -q analysis/w33_pass7310_7312_q7_pauli_validator.g
python3 analysis/w33_pass7310_7312_q7_pauli_validator.py --all
W33_RUN_EDA_SYNTH=1 W33_RUN_EDA_FORMAL=1 W33_RUN_EDA_PNR=1 \
  pytest -q tests/test_w33_pass7310_7312_q7_pauli_validator.py
```

The full 58,462-LUT parallel endpoint is intentionally opt-in because its
synthesis takes several minutes:

```bash
python3 analysis/w33_pass7310_7312_q7_pauli_validator.py --synthesize --full-synthesis
```
