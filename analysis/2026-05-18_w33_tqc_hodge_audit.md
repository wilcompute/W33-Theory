# W(3,3) TQC / Standard-Model Bridge Audit

## Exact finite result

Constructing W(3,3) directly over F_3 gives:
- vertices: **40**
- edges: **240**
- isotropic lines: **40**
- line-triangles: **160**
- SRG parameters: **{'v': 40, 'k': 12, 'lambda': 2, 'mu': 4}**
- adjacency spectrum multiplicities: **{'-4': 15, '2': 24, '12': 1}**

The line-triangle chain complex over F_3 gives the key decomposition:

```text
dim C1 = 240
rank d1 = 39
rank d2 = 120
beta1  = 81
C1 = im(d1^T) + im(d2) + H1 = 39 + 120 + 81 = 240
```

This is the strongest exact structural reading I found: the 240 edge-qutrit carrier splits into **39 exact-gradient modes**, **120 triangle-boundary modes**, and **81 harmonic/homological modes**.  The 120-sector is exactly half of the 240-edge/E8-root count, while the 81-sector is the protected qutrit homology repeatedly appearing in the theory.

## Claim boundary table

| Claim | Status | Computed | Note |
|---|---:|---|---|
| W(3,3) collinearity graph is SRG(40,12,2,4) | PASS_EXACT | `{"k": 12, "lambda": 2, "mu": 4, "v": 40}` | Constructed directly from the alternating form on PG(3,F_3). |
| Adjacency spectrum has multiplicities 12^1, 2^24, (-4)^15 | PASS_EXACT | `{"-4": 15, "12": 1, "2": 24}` | The multiplicities 1,24,15 are exact graph invariants. |
| Line-triangle complex has H_1 dimension 81 over F_3 | PASS_EXACT | `C1=240, rank(d1)=39, rank(d2)=120, beta1=81` | This gives the exact qutrit carrier decomposition 240=39+120+81. |
| SM count identity 40 = 1 + 24 + 15 | PASS_NUMERIC_DICTIONARY | `40 = 1 + 24 + 15` | Exact arithmetic and suggestive dictionary; not by itself a particle-physics derivation. |
| Total SM on-shell count 73 = Phi_12(3) = 28 + 45 | PASS_NUMERIC_DICTIONARY | `Phi12=73, T7=28, Q=45, T7+Q=73` | Exact arithmetic; physical degree-of-freedom convention must be specified separately. |
| Aut(W(3,3)) = 1,451,520 as full braid representation order | CONFLICT_OR_UNSPECIFIED_EXTENSION | `standard PGSp/Sp order for W(3,3) action = 51840; claimed = 1451520` | 1,451,520 = 28 * 51,840; it may be an extended carrier action, but it is not the bare W(3,3) automorphism order without extra structure. |
| W(3,3) is a [[40,12,13]]_3 CSS code | THEOREM_OBLIGATION | `No stabilizer check matrix supplied by W(3,3) alone in this audit.` | A CSS code claim requires explicit commuting H_X,H_Z and a distance computation; graph counts alone do not determine [[n,k,d]]. |
| Z_3 parafermion braiding gives universal TQC on this substrate | BRIDGE_ONLY | `Not a finite-graph invariant computed here.` | Requires a concrete modular category / braid representation / density theorem or compilation theorem. |
| Bruhat-Tits tree degree p+1=12 at p=11 matches k=12 | PASS_NUMERIC_BRIDGE | `p+1=12 and k=12` | Degree matching is exact arithmetic; finite-quotient and SM-over-Q_11 claims require a covering/lattice construction. |

## Interpretation

The cleanest next theorem is not merely `40 = 1+24+15`; it is the finite Hodge package `240 = 39+120+81`.  This gives a precise substrate mechanism for separating gauge/exact modes, triangle-curvature modes, and protected homological matter memory.  It also creates a disciplined interface for physics claims: a physics identification should specify which of the three sectors it uses and how measurement/braiding acts on that sector.
