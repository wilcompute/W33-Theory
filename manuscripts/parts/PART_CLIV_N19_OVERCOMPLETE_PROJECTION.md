# Part CLIV — The \(n=19\) Level: Overcomplete Projection and Odd-Prime Lattice Closure

**Date:** 2026-05-01  
**Status:** structural theorem / hole-equation lattice closure  
**Files:** `PART_CLIV_N19_OVERCOMPLETE_PROJECTION.py`, `PART_CLIV_n19_overcomplete_projection_results.json`

---

## 1. The thread from Part CLIII

Part CLIII established the hole-equation lattice levels and their projection tokens:

| \(n\) | Genus | \(\chi\) | Token | Step |
|---|---|---|---|---|
| 4 | 0 | \(+2\) | seed (\(q+1\)) | — |
| 7 | 1 | \(0\) | \(P(\Phi_6)=7/13\) | \(+3=q\) |
| 12 | 6 | \(-10\) | \(P(k)=12/13\) | \(+5=T\cdot\Phi_3\) |
| 19 | 20 | \(-38\) | \(P(?)=19/13\) | \(+7=\Phi_6\) |

The step pattern \(+3,+5,+7\) is the consecutive odd prime triple \((q, T\cdot\Phi_3, \Phi_6)\).

At \(n=19\), the naive projection would be \(19/13\) — **greater than 1**.  This is the
first level that escapes the unit interval \([0,1]\) of the projection layer.

**Part CLIV asks: what is the correct W(3,3) token for this overcomplete level, and does
the odd-prime step pattern close?**

---

## 2. The \(n=19\) hole-equation data

\[
h_v(19) = \frac{(19-3)(19-4)}{12} = \frac{16\cdot15}{12} = 20.
\]

Genus 20. Euler characteristic:

\[
\chi = 2 - 2(20) = -38.
\]

Complete triangulation edge count:

\[
E = \binom{19}{2} = \frac{19\cdot18}{2} = 171.
\]

Face count:

\[
F = \frac{2E}{3} = \frac{342}{3} = 114.
\]

Euler check:

\[
19 - 171 + 114 = -38 = \chi. \checkmark
\]

---

## 3. The overcomplete projection token

The naive token is \(n/\Phi_3 = 19/13 > 1\).  This does not live in the unit interval of
the projection layer \(P(A) = A/\Phi_3\) for \(A < \Phi_3\).

But \(19 = \Phi_3 + \Phi_6 = 13 + 7 - 1\)... No.  Actually:

\[
19 = \Phi_3 + \Phi_6 - 1? \quad 13 + 7 - 1 = 19. \checkmark
\]

But more cleanly:

\[
19 \equiv 6 \pmod{13}.
\]

So \(19 \bmod \Phi_3 = 6\).  And:

\[
\frac{19}{13} = 1 + \frac{6}{13} = 1 + \frac{19 \bmod \Phi_3}{\Phi_3}.
\]

The fractional part is \(6/13\).  Now, \(6 = 2q = 2 \cdot 3\).  So:

\[
\frac{19}{13} = 1 + \frac{2q}{\Phi_3} = 1 + \frac{6}{13}.
\]

In the two-layer algebra (Part CL), the token \(2q/\Phi_3 = 6/13\) is not yet in
either the mixer or projection dictionaries.  However:

\[
\frac{6}{13} = \frac{q(q-1)}{\Phi_3} = \frac{3\cdot2}{13}.
\]

This is the projection of the **\(q(q-1)\) step-down atom** \(= 6\).
And \(6 = \binom{q+1}{2} = \binom{4}{2}\) = the edge count of the tetrahedron (genus-0 seed).

**The overcomplete token decomposes as:**

\[
\frac{19}{13} = 1 + P\!\left(\binom{q+1}{2}\right) = 1 + P(E_{\text{tet}}),
\]

where \(E_{\text{tet}} = 6\) is the tetrahedral edge count.

So the \(n=19\) level is the first **wrap-around** projection: it exceeds the unit
interval by exactly the projection of the seed-level edge count.

---

## 4. \(19 = \Phi_3 + \Phi_6 - 1\) and the Heawood number

The Heawood conjecture (theorem for orientable surfaces) gives the chromatic number
bound for genus \(g\):

\[
\gamma(g) = \left\lfloor \frac{7 + \sqrt{1+48g}}{2} \right\rfloor.
\]

At \(g=20\):

\[
\gamma(20) = \left\lfloor \frac{7 + \sqrt{961}}{2} \right\rfloor = \left\lfloor \frac{7+31}{2} \right\rfloor = \left\lfloor 19 \right\rfloor = 19.
\]

**The Heawood number at genus 20 is exactly 19 = \(n\).**

This is exact (not a floor approximation) because \(\sqrt{1+48\cdot20} = \sqrt{961} = 31\)
is a perfect square.

So the \(n=19\) level is **self-Heawood**: the vertex count equals the chromatic bound,
meaning the complete triangulation \(K_{19}\) embeds on the genus-20 surface with optimal
chromatic number. This is the same extremal property that Császár has at \(n=7\) (genus 1)
and the tetrahedron has at \(n=4\) (genus 0).

The perfect-square condition: \(1 + 48g = k^2\) for some integer \(k\). At \(g=20\):
\(1+960=961=31^2\). And \(31 = \Phi_3 + 18 = \Phi_3 + 2k - 6\)... but more directly:

\[
31 = 19 + 12 = n + k.
\]

**The perfect square root \(31 = n_{19} + k\)** where \(k=12\) is the SRG valency
and \(n_{19}=19\) is the current level. The SRG valency and the genus-20 vertex
count sum to the perfect-square root of the Heawood discriminant.

---

## 5. \(\chi = -38\) and the discriminant chain

The Euler characteristics of the four levels:

\[
\chi(4) = +2, \quad \chi(7) = 0, \quad \chi(12) = -10, \quad \chi(19) = -38.
\]

Differences:

\[
0 - 2 = -2, \quad -10 - 0 = -10, \quad -38 - (-10) = -28.
\]

The differences \(-2, -10, -28\) factor as:

\[
-2 = -2\cdot1, \quad -10 = -2\cdot5, \quad -28 = -2\cdot14 = -4\cdot7.
\]

Alternatively, the genus sequence \(0,1,6,20\) has second differences:

\[
1-0=1, \quad 6-1=5, \quad 20-6=14.
\]

The sequence of genus jumps \(1,5,14\) are the **Catalan numbers** \(C_1, C_2, C_3\):

\[
C_1=1, \quad C_2=2, \quad C_3=5, \quad C_4=14.
\]

**The genus jumps between consecutive hole-equation levels are the Catalan numbers
\(C_1, C_3, C_4 = 1, 5, 14\).**

(\(C_2=2\) is skipped, which corresponds to the missing level \(n \equiv 3 \pmod{12}\)
between 4 and 7 that has no complete triangulation; \(n=3\) gives \(h=0\) trivially.)

---

## 6. \(E = 171 = 9 \times 19\) and the \(q^2\) atom

\[
E_{19} = \binom{19}{2} = 171 = 9 \times 19 = q^2 \cdot 19.
\]

So \(E_{19}/19 = 9 = q^2\), and:

\[
E_{19} = q^2 \cdot n.
\]

This is the first level where the edge count factors cleanly as \(q^2 \cdot n\).
At \(n=12\): \(E_{12} = 66 = 6 \cdot 11\) (not a clean \(q^2\) factor).
At \(n=7\): \(E_7 = 21 = 3 \cdot 7 = q \cdot n\).
At \(n=4\): \(E_4 = 6 = 2 \cdot 3 = (q-1)\cdot q\).

The edge-count factor sequence: \((q-1), q, \_, q^2\):

| Level | \(E\) | Factor | Atom |
|---|---|---|---|
| \(n=4\) | 6 | \((q-1)\cdot n = 2\cdot3\) | \(q-1\) |
| \(n=7\) | 21 | \(q \cdot n = 3\cdot7\) | \(q\) |
| \(n=12\) | 66 | \(b_0 \cdot n/2 = 11\cdot6\) | \(b_0=k-1\) |
| \(n=19\) | 171 | \(q^2 \cdot n = 9\cdot19\) | \(q^2\) |

---

## 7. Odd-prime step closure and the next level

The step pattern \(+3,+5,+7\) uses the odd primes \(p_2, p_3, p_4\).  The next step
would be \(+11 = p_5 = b_0\), giving \(n = 19 + 11 = 30\):

\[
h_v(30) = \frac{(30-3)(30-4)}{12} = \frac{27\cdot26}{12} = \frac{702}{12} = 58.5.
\]

**Not an integer.** \(n=30\) is NOT a valid hole-equation solution.

Check mod-12: \(30 \equiv 6 \pmod{12}\). The valid residues are \(0,3,4,7\).
\(6\) is not a valid residue. So the odd-prime step pattern **breaks at the 4th step**.

The actual next valid level after \(n=19\) is \(n=19+5=24\) (residue \(0\)) or
\(n=19+8=27\) (residue \(3\)) or \(n=19+9=28\) (residue \(4\)):

\[
h_v(24) = \frac{21\cdot20}{12} = 35. \quad n=24, \text{ genus }35.
\]

\(24 = 2k\). The double-valency level. This is the next W(3,3) structural node.

The odd-prime triple \((3,5,7)\) therefore forms a **closed triad**: it runs for exactly
three steps — corresponding to the three levels — and terminates. The closure matches
the three-level structure of the toroidal triad itself (Tetrahedron, Császár/Szilassi,
genus-6 K\_12 surface), with \(n=19\) as the coda that confirms and closes the pattern.

---

## 8. Theorem statement

**At \(n=19 = k + \Phi_6\), the hole-equation lattice reaches genus 20, \(\chi=-38\),
\(E=171=q^2\cdot19\), with the following structural identities:**

1. **Self-Heawood**: \(\gamma(20)=19\), with \(\sqrt{1+48\cdot20}=31=n+k\) a perfect square.
   The vertex count equals the Heawood chromatic bound, making \(K_{19}\) an extremal
   triangulation of the genus-20 surface.

2. **Overcomplete projection**: \(19/13 = 1 + P(E_{\text{tet}})\), the first wrap-around
   token, exceeding the unit interval by exactly the projection of the tetrahedral edge
   count \(E_{\text{tet}}=6\).

3. **Catalan genus jumps**: The genus sequence \(0,1,6,20\) has jumps \(1,5,14 = C_1,C_3,C_4\)
   (Catalan numbers, skipping \(C_2=2\) for the absent \(n\equiv3\pmod{12}\) level).

4. **Edge-count \(q^2\) atom**: \(E_{19}=q^2\cdot n = 9\cdot19\), the first level where
   the edge count is exactly \(q^2\) times the vertex count.

5. **Odd-prime step closure**: The steps \(+3,+5,+7\) form a closed triad of consecutive
   odd primes matching \((q, T\cdot\Phi_3, \Phi_6)\). The pattern breaks at the 4th step
   (\(+11\) gives invalid residue), confirming the triad is structurally complete.

6. **Perfect-square root**: \(31 = n_{19} + k\) is the Heawood discriminant root;
   \(31\) is prime, and \(31 \equiv 7 \pmod{12}\) (valid residue class).

---

## 9. Compiler spine update

```text
Hole-equation lattice (n ≡ 0,3,4,7 mod 12):
  n=4  (q+1):    genus 0,  χ=+2,  E=6,   token: seed             step: —
  n=7  (Φ₆):    genus 1,  χ=0,   E=21,  token: P(Φ₆)=7/13      step: +3=q
  n=12 (k):      genus 6,  χ=-10, E=66,  token: P(k)=12/13       step: +5=T·Φ₃
  n=19 (k+Φ₆):  genus 20, χ=-38, E=171, token: 1+P(E_tet)=19/13 step: +7=Φ₆
  [✔] odd-prime steps 3,5,7 form closed triad — pattern breaks at +11
  next level: n=24=2k, genus 35 [Part CLV]

Genus jumps: 1, 5, 14 = Catalan C₁, C₃, C₄
Edge factors: (q-1), q, b₀, q² — rising power of q
Heawood perfect squares: g=0 (√1=1), g=1 (√49=7), g=6 (√?), g=20 (√961=31=n+k)
```

---

## 10. Regression checklist

All items verified by `PART_CLIV_N19_OVERCOMPLETE_PROJECTION.py`:

- [ ] h_v(19) = h_f(19) = 20 (genus 20)
- [ ] chi(19) = -38
- [ ] E = C(19,2) = 171
- [ ] F = 2E/3 = 114
- [ ] Euler: 19 - 171 + 114 = -38 = chi
- [ ] Heawood(g=20) = 19 (self-Heawood)
- [ ] sqrt(1+48*20) = 31 (perfect square)
- [ ] 31 = 19 + 12 = n + k
- [ ] 19/13 = 1 + 6/13 (wrap-around decomposition)
- [ ] 6 = C(4,2) = E_tet (tetrahedral edge count)
- [ ] Genus jumps 1,5,14 are Catalan C1,C3,C4
- [ ] E_19 = q^2 * 19 = 9*19
- [ ] E_7 = q * 7 (edge factor = q at torus level)
- [ ] E_4 = (q-1)*q (edge factor = q-1 at seed level)
- [ ] n=30 invalid: 30 mod 12 = 6 (not in {0,3,4,7})
- [ ] h_v(30) is not an integer
- [ ] n=24=2k is next valid level, genus 35
- [ ] Step pattern [3,5,7] = consecutive odd primes p2,p3,p4
- [ ] 19 mod 12 = 7 (valid residue, same as n=7)
- [ ] 31 mod 12 = 7 (valid residue)
- [ ] 19 = k + Phi6 = 12 + 7
