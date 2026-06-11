# BT807 — The q=3 Anti-Flag and the Two-Clock Theorem

Lifts BT806 from PG(3,2) to PG(3,3) and measures the collision between
the projective Singer clock and the symplectic W(3,3) structure.

## Construction

Singer cubic x^3 + 2x + 1 over F3 with companion matrix of TRUE order 13
(a cubic factor of x^13 - 1; the first attempt with order-26 companion
taught a lesson: extending diag(C,1) breaks the scalar g^13 = 2I and
fakes 26-orbits).  Frobenius multiplier f g f^-1 ~ g^3 gives the clock
F39 = C13:C3, the q=3 sibling of BT806's F21 = C7:C3.

## The anti-flag persists (q=3)

```text
F39 orbits on PG(3,3):
  points:  [1, 13, 13, 13]    vacuum + three tridecads
  lines:   [13, 13, 13, 13, 39, 39]
  planes:  [1, 13, 13, 13]
star(p0) = 13 lines through the vacuum point   - an orbit
lines(pi0) = 13 lines of the fixed PG(2,3)     - an orbit
p0 NOT on pi0                                  - ANTI-FLAG
```

13 = Phi3 = q^2 + q + 1 plays the role 7 = Phi6 played at q=2.  The
ladder of vacuum decompositions:

```text
q=2:  15 = 1 + 7 + 7         (two heptads)
q=3:  40 = 1 + 13 + 13 + 13  (three tridecads)
```

## The Two-Clock Theorem

The same 40 points carry two incompatible decompositions:

```text
Singer clock:     40 = 1 + 13 + 13 + 13      (C13, projective)
symplectic W33:   40 = 1 + 12 + 27           (vacuum + gauge + matter)
```

incompatible because 13 does not divide |PSp(4,3)| = 25920.  Measured
consequence: the 40 totally isotropic lines SHATTER over the ten C13
line orbits of PG(3,3):

```text
isotropic per C13 orbit: [2, 3, 3, 3, 4, 4, 4, 5, 5, 7]   mean = 4 = mu
star(p0) orbit:   exactly 4 = q+1 isotropic  (the W33 pencil of p0)
```

Only the star's count is forced (the GQ pencil); the rest is genuinely
non-uniform - the symplectic structure is invisible to the Singer clock
except through the pencils.

## The q=2 companion (contrast)

```text
doily W(3,2): 15 isotropic among 35
F21 orbit split: star (7,3), plane (7,3), generic (21,9)
```

At q=2 the split is clean (3 = pencil of GQ(2,2) in the star, 3 in the
plane, 9 generic): the doily distributes EVENLY over the anti-flag
orbits, while at q=3 the W33 lines shatter irregularly.  The Csaszar
trio's home field q=2 is exactly the field where the two clocks still
cohabit gracefully.

## Boundary

Open: which 13-orbit is lines(pi0) and why it carries 3 vs 5 isotropic
lines (plane types in symplectic PG(3,3)); the [2,...,7] shatter profile
as an invariant of the Singer-vs-symplectic relative position; and the
q=2 statement "doily = 3+3+9 over the anti-flag" as a Csaszar-side
theorem (which 6 faces of the torus carry the doily structure?).
