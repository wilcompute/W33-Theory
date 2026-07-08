# W(3,3) Packet VM

The bytecode lifter gives each instruction a W33 route and Q6/tomotope packet
slot. The packet VM executes that stream and verifies that the wrapped program
returns the same value as the source function.

| Sample | VM result | Static packet ops | Executed packet steps | Loop expansion | Max hops |
|---|---:|---:|---:|---:|---:|
| sample_sum_squares | `140` | 18 | 82 | 4.56 | 2 |
| sample_rule110_step | `00110000` | 59 | 347 | 5.88 | 2 |

Boundary: this is a compact executable semantics for the current Holonet opcode
subset, not a full CPython replacement.
