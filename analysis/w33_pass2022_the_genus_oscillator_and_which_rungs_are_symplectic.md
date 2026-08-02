# Pass 2022 — the genus oscillator, and which of its rungs a symplectic quadrangle can reach

Following the user's pointer to the percolation / harmonic-oscillator /
genus-oscillator scripts. The repo has far more of this than I expected, and it
changes what Pass 2018 means.

---

## What the repo already had

`data/dccxxiii_genus_equation_spectrum.json` carries the **genus equation** as a
quadratic and reads its constants in `W(3,3)`'s own primitives:

```text
g(K_n) = (n-3)(n-4)/12          i.e.   n^2 - 7n + 12 = 12g
discriminant of n given g       :      1 + 48g       (Heawood)

12 = q(q+1)   = local W(3,3) valency  ("codec")
 7 = q + (q+1) = Heawood number
```

So the denominator of the complete-graph genus formula is **the `W(3,3)` point-graph
valency**, and its linear coefficient is `q + (q+1)`, both at `q = 3`. The repo
frames this as **three clocks**:

| clock | origin | appears in |
|---|---|---|
| mod 12 | `q(q+1)`, the valency | genus denominator, `ℤ₁₂ = ℤ_q × ℤ_{q+1}` CRT, `ζ(−1) = −1/12`, tomotope order 12 |
| mod 7 | `q + (q+1)`, Heawood | Császár's 7 vertices, Szilassi's 7 faces, Fano's 7 points, Heawood graph |
| mod 10 | `ΔF = 2(q+1) + 2` | `F(h) = 4 + 10h`, and `1/7 = 0.142857` |

And the **genus oscillator** itself:

```text
h=0 : v= 4, E= 6, F= 4, chi= 2, g=0
h=1 : v= 7, E=21, F=14, chi= 0, g=1
h=2 : v=10, E=36, F=24, chi=-2, g=2
h=3 : v=13, E=51, F=34, chi=-4, g=3
```

This was all in place. Pass 2017 found the `h0/h1/h6` ladder; this is the engine
under it.

---

## What Pass 2018 actually adds: a reachability filter

The repo's integer-genus spectrum for `n ≤ 50` has **16** entries. My residual
decomposition (Pass 2016) says a spread's residual set is `q²+1` copies of
`K_{q+1}`, so a rung `n` is realised by a symplectic quadrangle exactly when
`q = n − 1` is a prime power:

```text
   n     g   q=n-1   prime power?   symplectically reachable
   3     0       2        yes       yes  (but q even: no sigma_S)
   4     0       3        yes       YES  <- the substrate
   7     1       6         no       --   the classical Csaszar/Szilassi rung
  12     6      11        yes       YES
  15    11      14         no       --
  16    13      15         no       --
  19    20      18         no       --
  24    35      23        yes       YES
  27    46      26         no       --
  28    50      27        yes       YES
  31    63      30         no       --
  36    88      35         no       --
  39   105      38         no       --
  40   111      39         no       --
  43   130      42         no       --
  48   165      47        yes       YES
```

> **Of the 16 integer-genus rungs below `n = 50`, only six have `n − 1` a prime
> power, and only five of those are odd — `q = 3, 11, 23, 27, 47`. The smallest
> is the substrate's own `q = 3`.**

Ten of sixteen rungs, including the classical Császár/Szilassi one, have no
symplectic quadrangle at all. So the genus oscillator is a much longer ladder
than the symplectic side can climb, and the rungs it *can* reach are sparse and
begin exactly at `q = 3`.

That is the honest form of the connection: the repo owns the ladder and the
three clocks; this pass supplies which rungs a spread's residual `K_{q+1}` can
occupy, and why `q = 11` (Pass 2011) landed on 66 rather than on nothing.

---

## The self-reference worth flagging

The genus formula's denominator is `12 = q(q+1)` at `q = 3`, and I used that same
formula to compute the genus of `K_{q+1}` for *varying* `q`. Those two roles of
`q` are different — one is the substrate's fixed valency, the other ranges over
prime powers — and the coincidence at `q = 3` is what makes `h0` the substrate's
own rung.

**I am flagging rather than developing this**, because it is precisely the shape
that produced three false claims in this arc: a constant that is `12` for one
reason being read as `q(q+1)` for another. The repo's `dccxxiii` pass asserts the
identification; I am not extending it.

---

## Percolation: explored, not integrated

`analysis/2026-05-21_genus_percolation_information_hole.md`,
`analysis/w33_css_genus_percolation_hinge.py` and
`data/PART_BT500_CORRECTED_TOROIDAL_PERCOLATION_THRESHOLD_LEDGER_results.json`
are the percolation lane, and `analysis/bt802_oscillator_atlas_verification.py`
the oscillator atlas. **Read, not integrated** — I have not established any link
between them and the spread obstruction, and I am not asserting one on the
strength of shared vocabulary.

---

## Prior art

- `dccxxiii` / `data/dccxxiii_genus_equation_spectrum.json`,
  `verify_dccxxiii_genus_equation_spectrum.py` — **own** the genus equation in
  `W(3,3)` primitives, the three clocks, the genus oscillator, and the integer
  spectrum.
- BT1844 / `w33_toroidal_h6_66_bridge.json` — **own** the complete-adjacency
  ladder (Pass 2017).
- `manuscripts/tex/part18_jungerman_ringel.tex` — the minimal-triangulation lane.
- Pass 2016 — the `K_{q+1}` decomposition, from the user's observation.

## Still open

- Whether the mod-12 self-reference is structural or a coincidence at `q = 3`.
- Any actual link between the percolation lane and the spread obstruction.
