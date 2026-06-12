# BT860 — Bell-Shell Register Arithmetic: The [4,4,6,12] Relations Named

**Status: PROVEN (machine-verified, `analysis/bt860_bell_shell_register_arithmetic.py`, data `data/bt860_bell_shell_register_arithmetic.json`)**

Closing BT858's open. The Bell shell (27 now-contexts disjoint from the Bell
line L₀) is an F₃³ torsor under the line parabolic's O₃ (BT858). Assigning
every shell context a 3-trit address (base context + O₃-basis), the four
Stab-suborbits [4,4,6,12] become **difference-vector classes**, and the
geometry is a function of register arithmetic alone — verified uniform over
all 351 pairs:

| register class | size | geometry of the pair | shared transversals onto L₀ |
| --- | --- | --- | --- |
| ± meet class | 4 + 4 (±-paired) | the two contexts **meet** | exactly **1** |
| far skew | 6 | disjoint | exactly **0** |
| near skew | 12 | disjoint | exactly **2** |

(Each shell context M has a transversal tetrad T(M) onto L₀, in canonical
bijection with L₀'s 4 points by the GQ axiom; |T(M) ∩ T(M′)| is the natural
"shadow overlap" of two matter contexts on the Bell line.)

## Reading

The matter sector of the photon's Bell shell is not just *labeled* by 3
trits (BT858) — its entire incidence physics is **priced by register
differences**: switching between two matter now-contexts costs a relation
determined by their 3-trit XOR-analogue (F₃ difference), with the shadow
overlap on the Bell line (1 / 0 / 2 transversals) as the physical signature.
This is the ternary twin of the chart layer's F₂³ Gray-code arithmetic: the
machine's data plane does base-2 register routing on charts and base-3
register incidence on matter contexts, both exact.

## Open

- The meet-class ± pairing: an orientation bit on meeting context pairs —
  relate to the chirality ledger (BT857).
- The near/far skew split (12 vs 6) vs the BT835 schedule overlap law
  (15 near / 20 far partners at the schedule level): same near/far language,
  different objects — is there a covering map?
