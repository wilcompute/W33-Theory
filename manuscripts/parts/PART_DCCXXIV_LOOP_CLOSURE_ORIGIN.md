# Part DCCXXIV — The Loop-Closure Origin of (q, q+1)

**Bridge:** `verify_dccxxiv_loop_closure_origin.py` — Verified
**Tests:** `tests/test_dccxxiv_loop_closure_origin.py` — 20/20 pass
**Data:** `data/dccxxiv_loop_closure_origin.json`

---

## 1. The insight

> "3 being the minimum points to close a loop and when you have three points
> you automatically get a 4th because it creates a triangle face."

This is a **topological** origin of the (q, q+1) = (3, 4) pair that has
governed the program — separate from, and underlying, the algebraic
Master Equation q! = 2q.

---

## 2. Loop-Closure Theorem

A non-degenerate closed 1-loop in a simplicial complex requires **at
least 3 vertices**. Once you have three pairwise-connected vertices,
the bounded interior is forced to be a **2-face**, giving:

$$
(V, E, F) \;=\; (3, 3, 1).
$$

The total sub-cell count of the minimal loop is

$$
V + E + F \;=\; 3 + 3 + 1 \;=\; 7 \;=\; \mathbf{M_3 = 2^3 - 1.}
$$

This is exactly the **Heawood number**.

Adding a single apex vertex with edges to all three triangle vertices
closes the 2-cycle (the boundary surface) into a 3-cell: the
**tetrahedron**. Its sub-cell count is

$$
(V, E, F, T) \;=\; (4, 6, 4, 1), \qquad \text{total} = 15 = \mathbf{M_4 = 2^4 - 1.}
$$

This is exactly the **W(3,3) g eigen-multiplicity**.

---

## 3. The Mersenne picture

An n-simplex has 2^(n+1) − 1 = M_{n+1} non-empty sub-simplices (all
non-empty subsets of its n+1 vertices). At q = 3:

| simplex | dim | vertices | sub-cells | Mersenne |
|---|---:|---:|---:|---:|
| Triangle (minimal loop) | 2 | q = 3 | 7 | M_q = 2^q − 1 |
| Tetrahedron (minimal volume) | 3 | q + 1 = 4 | 15 | M_{q+1} = 2^{q+1} − 1 |

So the **two Mersenne numbers** M_q = 7 and M_{q+1} = 15 are the sub-cell
totals of the consecutive simplices that close a loop and its bounded
volume.

Both are W(3,3) primitives:

* M_q = 7 = Heawood = Császár V = Szilassi F = Fano points/lines
* M_{q+1} = 15 = g eigen-multiplicity in the W(3,3) SRG spectrum

So the **W(3,3) eigen-multiplicities trace back to simplex sub-cell
counts**.

---

## 4. The pincer becomes topological

DCCXVIII formalised the "q = 3" derivation as a pincer bound between
quantum non-commutativity (q ≥ 3) and topological realisability
(q ≤ 3). DCCXXIV refines BOTH sides into purely topological statements:

| bound | source | reformulation |
|---|---|---|
| lower | loop closure requires non-degenerate 1-cycle | q ≥ 3 |
| upper | rigidity: every vertex permutation realised as rigid motion (q! ≤ 2q) | q ≤ 3 |

The lower bound is now a **topological** statement (you need 3 vertices
to even form a cycle), while the upper bound remains combinatorial /
geometric. Their intersection — q = 3 — is exactly where loop closure
saturates rigidity.

This is the deepest reading of the Master Equation: it lives at the
unique integer where **the act of closing a loop coincides with the
condition that every vertex relabelling is a rigid motion**.

---

## 5. Why (q, q+1) emerges automatically

The closure act creates **one new cell of dimension one above the
loop**, hence the +1:

```
{q vertices closing a loop}   +   {1 new face from closure}
            =
{q + 1 elements at the next dimension}
```

At q = 3 this is:

* 3 vertices + 3 edges + 1 face → triangle (= 2-simplex)
* 4 vertices = q+1 of the next simplex (tetrahedron) → 3-simplex
* The "+1" is the topological act of closure

So (q, q+1) is not an arbitrary pair: it is the (loop-size, volume-size)
pair at the minimum dimension where loops can close. This is the
**natural reading** of all the (3, 4) coincidences in the program:
(q, q+1), (Heawood / sum, codec / product), (sphere V / torus V),
(F at h = 0 / F at h = 1 if we ignore one face), etc.

---

## 6. Decisive identity

$$
\boxed{\;
\text{loop closure}_q
\;\Longrightarrow\;
\text{sub-cell total} = 2^q - 1 = \text{Heawood}, \;
\text{apex closure} \Longrightarrow 2^{q+1} - 1 = \text{g eigen-mult};
\;}
$$

and combined with the rigidity bound q! ≤ 2q (DCCXVIII upper),

$$
\boxed{\;
\text{loop closure} \cap \text{rigidity} \;=\; \{q = 3\}.
\;}
$$

---

## 7. What this part adds

* A **topological** derivation of (q, q+1) = (3, 4) from minimal loop
  closure.
* Identification of the **Heawood number 7** with the Mersenne **M_q**
  and the **W(3,3) g eigen-multiplicity 15** with **M_{q+1}**.
* A topological reformulation of the DCCXVIII pincer: the lower bound
  q ≥ 3 is the cycle-existence condition; the upper bound q ≤ 3 is the
  rigidity condition; their saturation is the Master Equation.

---

## 8. Honest boundary

* This part derives the **pair** (q, q+1) topologically; it does **not**
  reconstruct the full W(3,3) SRG, the photonic-QEC codec, the empirical
  closures, or the spectral-action machinery — those still depend on
  the parts CCCCXXXI–CCCCCXXIII.
* The identification of W(3,3)'s g eigen-multiplicity = 15 with M_{q+1}
  is a numerical coincidence at q = 3, not a constructive realisation
  of the spectrum from simplex sub-cell counts.

---

## 9. One-line summary

$$
\boxed{\;
3 = \min \big\{ |V| : G \supset \text{closed 1-loop} \big\}
\;\Longrightarrow\;
\text{triangle has } 2^3 - 1 = 7 \text{ sub-cells}
\;\Longrightarrow\;
(q, q + 1) = (3, 4) \text{ is topological.}
\;}
$$
