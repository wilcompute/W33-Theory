# Pass 53 Promotion Review — Parity Control And Table-Free Routing

Date: 2026-06-29

Status: **promote locally as verified candidate; keep remote-reconciliation warning.**

## Decision

Pass 53 should be treated as a verified local candidate rather than rejected. The exact witnesses pass:

- `analysis/w33_audit_qscan.py` verifies `q=2,3,4`, with `q=4=GF(4)` as the even-composite control.
- `analysis/holonet_cli.py bench --compare` verifies classical all-pairs next-hop state versus Holonet address routing.
- `tests/test_pass53_parity_compare.py` passes all four focused checks.

The only reason not to state it as settled public remote doctrine is repository topology: this checkout has local Pass 53 while `origin-https/master` contains the BT1905-BT1907 packet and intentionally lacks the Pass 53 public card/fast-path rows. The correct public wording is therefore:

> Verified locally in this checkout; pending branch reconciliation.

## Result 1 — Parity, Not Primality

The q-scan verifies:

| q | n | k | lambda | mu | ovoid | contextual fraction |
|---:|---:|---:|---:|---:|---:|---:|
| 2 | 15 | 6 | 1 | 3 | true | 0 |
| 3 | 40 | 12 | 2 | 4 | false | 1/10 |
| 4 | 85 | 20 | 3 | 5 | true | 0 |

The `q=4` row is the discriminating control because it is even and composite, yet still non-contextual. That makes the live interpretation sharper:

```text
even q  -> ovoid exists -> CF = 0
odd q   -> no ovoid     -> CF = 1/(q^2+1)
```

For the Holonet, `q=3` is the smallest contextual member and gives `CF=1/10`.

## Result 2 — Table-Free Routing

`holonet bench --compare` builds a classical all-pairs forwarding baseline and compares it to address-is-route routing.

| Quantity | Classical table-routed baseline | Holonet address-routed fabric |
|---|---:|---:|
| Nodes | 40 | 40 |
| Routing entries | 1560 | 0 |
| Bits per entry | 6 | 0 |
| Routing-state bytes | 1170 | 0 |
| Setup relaxations | 19200 | 0 |
| Max hops sampled | baseline reaches destination | 2 |
| Routers agree | true | true |

This is an architectural state/setup win, not a claim that a table lookup is slow. The point is that the classical router presupposes a table the Holonet never builds.

## Verification

```text
.venv/bin/python analysis/w33_audit_qscan.py
  ALL PASS -- every layer constant is forced by q; the Holonet is contextual because q=3 is ODD (parity, not primality).

.venv/bin/python analysis/holonet_cli.py bench --compare
  OK -- table-free routing verified equivalent; 0 bytes of routing state.

.venv/bin/python -m pytest tests/test_pass53_parity_compare.py -q
  4 passed in 146.87s
```

## Promotion Boundary

Promote into the presentation and local dashboard as a candidate exact result. Do not silently merge the remote branch state or claim `origin-https/master` already contains it. The remaining task is a clean branch reconciliation that preserves BT1905-BT1907 and Pass 53 together.
