# Payne Hesse Packet Dictionary

This note explains the artifact `artifacts/payne_hesse_packet_dictionary.json` in
plain language.

The point of the artifact is that one fixed local `45`-object is now seen in
three exact ways at once:

- Payne side: `9` hyperbolic lines plus `36` ordinary lines.
- Qutrit side: `9` H27 fibers plus `36` internal triangles.
- Cubic side: `9` type-2 tritangents plus `36` type-1 tritangents.

Those three pictures glue into one `9`-point / `12`-line Hesse configuration.
The `9` hyperbolic packets are the points. The ordinary `36` split into `12`
packets of `3`, and those are the lines.

## What the artifact proves

- There are exactly `9` point packets and `12` line packets.
- Each point packet lies on `4` line packets.
- Each line packet contains `3` point packets.
- Two line packets meet in exactly one point packet, unless they are parallel,
  in which case they are disjoint.
- The packet symmetry orders are exactly `1296 -> 432` and `648 -> 216`.
- The central order-`3` kernel acts on cubic labels as the `9` hyperbolic
  3-cycles.

This is exactly the classical Hesse incidence pattern: the same `9` points and
`12` affine lines as the plane `F3^2`.

## The 9 point packets

On the qutrit side, each point packet is the fiber with fixed `(x,y)` and
`z = 0,1,2`.

| AG(2,3) point | H27 fiber | Payne hyperbolic line | Cubic hyperbolic tritangent |
| --- | --- | --- | --- |
| `(0,0)` | `(0,0,*)` | `[0,1,2]` | `a_1, b_6, c_16` |
| `(0,1)` | `(0,1,*)` | `[3,4,5]` | `c_15, c_24, c_36` |
| `(0,2)` | `(0,2,*)` | `[6,7,8]` | `a_3, b_5, c_35` |
| `(1,0)` | `(1,0,*)` | `[18,19,20]` | `a_5, b_4, c_45` |
| `(1,1)` | `(1,1,*)` | `[24,25,26]` | `a_6, b_2, c_26` |
| `(1,2)` | `(1,2,*)` | `[21,22,23]` | `c_13, c_25, c_46` |
| `(2,0)` | `(2,0,*)` | `[9,10,11]` | `c_14, c_23, c_56` |
| `(2,1)` | `(2,1,*)` | `[12,13,14]` | `a_4, b_3, c_34` |
| `(2,2)` | `(2,2,*)` | `[15,16,17]` | `a_2, b_1, c_12` |

## The 12 line packets

Each row below is one affine line in `F3^2`. The `phase patterns` column gives
the three qutrit triangles on that line, read along the ordered line shown in the
first column.

| AG(2,3) line | Direction | Phase patterns | Cubic 9-label packet |
| --- | --- | --- | --- |
| `(0,0)-(0,1)-(0,2)` | `(0,1)` | `000; 112; 221` | `a_1,a_3,b_5,b_6,c_15,c_16,c_24,c_35,c_36` |
| `(1,0)-(1,1)-(1,2)` | `(0,1)` | `021; 102; 210` | `a_5,a_6,b_2,b_4,c_13,c_25,c_26,c_45,c_46` |
| `(2,0)-(2,1)-(2,2)` | `(0,1)` | `021; 102; 210` | `a_2,a_4,b_1,b_3,c_12,c_14,c_23,c_34,c_56` |
| `(0,0)-(1,0)-(2,0)` | `(1,0)` | `000; 121; 212` | `a_1,a_5,b_4,b_6,c_14,c_16,c_23,c_45,c_56` |
| `(0,1)-(1,1)-(2,1)` | `(1,0)` | `011; 102; 220` | `a_4,a_6,b_2,b_3,c_15,c_24,c_26,c_34,c_36` |
| `(0,2)-(1,2)-(2,2)` | `(1,0)` | `022; 101; 210` | `a_2,a_3,b_1,b_5,c_12,c_13,c_25,c_35,c_46` |
| `(0,0)-(1,1)-(2,2)` | `(1,1)` | `000; 121; 212` | `a_1,a_2,a_6,b_1,b_2,b_6,c_12,c_16,c_26` |
| `(0,1)-(1,2)-(2,0)` | `(1,1)` | `011; 102; 220` | `c_13,c_14,c_15,c_23,c_24,c_25,c_36,c_46,c_56` |
| `(0,2)-(1,0)-(2,1)` | `(1,1)` | `022; 101; 210` | `a_3,a_4,a_5,b_3,b_4,b_5,c_34,c_35,c_45` |
| `(0,0)-(1,2)-(2,1)` | `(1,2)` | `000; 121; 212` | `a_1,a_4,b_3,b_6,c_13,c_16,c_25,c_34,c_46` |
| `(0,1)-(1,0)-(2,2)` | `(1,2)` | `011; 102; 220` | `a_2,a_5,b_1,b_4,c_12,c_15,c_24,c_36,c_45` |
| `(0,2)-(1,1)-(2,0)` | `(1,2)` | `022; 101; 210` | `a_3,a_6,b_2,b_5,c_14,c_23,c_26,c_35,c_56` |

## Symmetry ladder

- `1296`: the full local H27 symmetry at the chosen base point.
- `648`: the determinant-1 or projective half of that symmetry.
- `432`: the induced symmetry on the `9` point packets and `12` line packets.
- `216`: the determinant-1 quotient on the packet geometry, i.e. the classical
  Hessian subgroup.

So the fixed local `45` is not just "similar to" a Hesse configuration. It is an
exact Hesse configuration with a bigger qutrit/cubic phase lift above it.

## The phase lift

Every line packet is an affine line in `F3^3`: if the three phase patterns on one
line are written as functions of the line coordinate `u in F3`, then they always
have the form

`t_s(u) = b(u) + s r(u)` for `s in F3`.

Up to affine reparameterization of the line coordinate, there are exactly three
palette types:

- `4` packets of type `000, 112, 221`, i.e. `t_s(u) = s (2u^2 + u + 1)`.
- `6` packets of type `011, 102, 220`, i.e. `t_s(u) = u^2 + s (2u^2 + 2u + 1)`.
- `2` packets of type `012, 120, 201`, i.e. `t_s(u) = u + s`.

The important obstruction is that this phase lift is real: there is no global
affine gauge of the form `z -> a z + g(x,y)` with `a != 0` that turns all `12`
line packets into constant phase slices at once.

So the ordinary `36` are not just the affine lines of `F3^2`. They are a genuine
nontrivial phase-decorated lift of those `12` lines.
