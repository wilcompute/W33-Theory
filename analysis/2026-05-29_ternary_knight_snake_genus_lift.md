# Ternary Knight / Snake / Genus Lift Theorem

Date: 2026-05-29

This corrects the binary-router interpretation by adding the ternary/qutrit information geometry hiding inside each knight move.

The endpoint graph is binary:

```text
4x4 toroidal knight graph = Q4.
```

But each knight jump is internally ternary. A knight move is a three-unit micro-walk:

```text
straight, straight, perpendicular.
```

So if we count the square currently occupied plus the three unit updates, we see 4 squares. But if we regard the starting square as the landing square of the previous jump, each new macro move contributes exactly 3 new microsteps.

That gives the qutrit/ternary lift:

```text
Q4 endpoint edge -> Z3 three-step fiber.
```

## Ternary knight microgeometry

The verifier decomposes every macro knight edge in the toroidal Gray clock into three unit moves:

```text
(a, a, b), with b perpendicular to a.
```

It checks:

```text
each knight jump has exactly 3 microsteps
first two microsteps are parallel/equal
last microstep is perpendicular to the first two
landing square parity flips every jump
micro-phases are balanced: phase 0 = 16, phase 1 = 16, phase 2 = 16
```

So the full 16-edge Gray cycle has

```text
16 macro jumps * 3 microsteps = 48 microticks.
```

That is exactly the Reye incidence count:

```text
48.
```

This gives the first clean answer to the binary/ternary tension:

```text
Q4 is the binary endpoint skeleton.
The knight edge is a ternary information fiber.
The combined geometry is a Z3-fibered Q4 router.
```

## Snake-in-the-box correction

The full 16-cycle Gray clock is Hamiltonian, but it is not an induced cycle in Q4. Therefore it is not a snake/coil code in the strict snake-in-the-box sense.

The verifier checks this explicitly:

```text
full 16-cycle = router clock, not induced coil.
```

The snake/error-detecting layer is instead an induced Q4 coil of length 8. An explicit one is:

```text
0000, 0001, 0011, 0111, 1111, 1110, 1100, 1000.
```

The brute-force search verifies:

```text
max Q4 coil length = 8.
```

Ternary-lifting that coil gives

```text
8 macro jumps * 3 microsteps = 24 microticks.
```

So:

```text
Q4 full Gray clock -> 48 ternary microticks = Reye incidences.
Q4 induced snake/coil -> 24 ternary microticks = m_r / Cl4 square-face count.
```

This separates roles cleanly:

```text
Gray Hamilton cycle = full router scan.
Snake/coil induced cycle = error-detecting subclock.
Ternary knight lift = qutrit information flow on each edge.
```

## Genus and triangular closure

The minimal triangulation formula for complete graphs is

```text
g(K_n)=((n-3)(n-4))/12.
```

This is integral exactly when

```text
n = 0,3,4,7 mod 12.
```

The verifier checks the residue set:

```text
0,3,4,7 = 0,q,chi,Phi6.
```

That is a very clean W33 packet:

```text
0 = closure vacuum
3 = q = triangle, minimal loop closure
4 = chi = tetrahedral/simplex closure
7 = Phi6 = toroidal K7 closure
```

Key complete-graph genera:

```text
K3  -> genus 0
K4  -> genus 0
K7  -> genus 1  (Csaszar torus)
K12 -> genus 6  (= g2)
```

So the genus condition is not separate from the router logic. It determines which complete-graph information geometries can close as triangular surfaces.

## Information-geometry summary

The new geometry is:

```text
endpoint skeleton: binary Q4 / 4x4 toroidal knight graph
edge fiber: ternary Z3 three-step knight word
full clock: 16 macro jumps, 48 ternary microticks
snake subclock: 8 macro jumps, 24 ternary microticks
surface closure: n = 0,3,4,7 mod 12
```

Or more compactly:

```text
Q4 is not the qutrit theory.
Q4 is the binary endpoint network on which ternary knight fibers carry the qutrit information flow.
```

## Relation to prior packet

The previous factorization survives:

```text
|W(E6)| = 51840 = 40 * 16 * 81.
```

But now the 16 router states are no longer merely binary states. Each adjacent binary transition carries a ternary micro-fiber, so the information geometry is better described as:

```text
W33 anchors * Q4 endpoint states * H1 phase frame
with Z3 knight fibers on Q4 edges.
```

The ternary microcounts explain why the same packet keeps hitting 24 and 48:

```text
24 = induced Q4 snake length 8 * ternary edge length 3
48 = full Q4 Gray cycle length 16 * ternary edge length 3.
```

## Honest boundary

This proves the finite ternary lift, the snake/coil correction, and the triangular-genus residue condition. It does not yet construct a global qutrit stabilizer code over the Q4-fibered W33 anchor bundle. The next step is to build the actual incidence matrix of the Z3-fibered Q4 router and test whether its cycle space maps into the W33 H1 phase-frame projector.
