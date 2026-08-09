# Pass 4460 — the Hagedorn temperature, the thermal track, and a homonym to avoid

Pass 4453 found that the prime geodesics of W(3,3) form a gas with a Hagedorn temperature
at `β_c = log q = log 11 = 2.3979`, which is the Ihara zeta's dominant pole at `u = 1/q`
under `u = e^(−β)`. This file connects that to work already in the repository — and, more
usefully, flags a connection that must **not** be made.

## The real connection: `q = 11` is already a first-class token here

`bt565_leakage_resonance_244_121.py` line 10 defines it exactly:

> `121 = 11^2 = p_Ih^2 = (nonbacktracking outdegree)^2 for the W33 graph.`

So `p_Ih = 11` — the repository's "Ihara prime" — **is** the `q = d − 1` of the zeta track
and of Pass 4453. It appears as an arithmetic token across dozens of passes
(`w33_BREAKTHROUGH_101`, `_105`, `bt565`, …), usually as a factor in substrate identities
like `22 = λ·p_Ih` and `449 = μ·137 − q²·p_Ih`.

What Pass 4453 adds is that this integer is a **temperature**:

```
β_c = log(p_Ih) = 2.397895…
```

the point above which the geodesic gas has a partition function and below which it does
not. Everywhere `p_Ih` appears as a factor in the corpus, it is being used as a number; here
it is the exponential growth rate of a density of states, and its logarithm is a physical
scale. That is a genuinely different role for a token the corpus already tracks.

The divergence is **logarithmic**, not a pole: `π(m) ~ q^m/m` makes `Σ π(m) e^(−βm)` the
logarithm series at `β_c`. That 1/m is what makes it Hagedorn rather than an ordinary radius
of convergence — the same exponential-density-of-states mechanism that produces a limiting
temperature in string theory.

## The homonym: two different things are called "the partition function" here

`w33_BREAKTHROUGH_22_partition_function_substrate.py` and
`w33_BREAKTHROUGH_308_partition_function_substrate.py` are about the **integer partition
function** `P(n)` — the number of ways to write `n` as a sum of positive integers:

```
P(3) = 3 = q          P(6) = 11 = p_Ih          P(9)  = 30 = h(E_8)
P(4) = 5 = F_5        P(7) = 15 = g             P(13) = 101
```

That is a **combinatorial counting function**. Pass 4453's `Z(β) = Σ_m π(m) e^(−βm)` is a
**statistical-mechanics partition function**. They share a name and nothing else: one takes
an integer and returns an integer, the other takes a temperature and returns a real number
that can diverge.

> **Do not connect them.** Two objects sharing an English phrase is precisely the signature
> `CLAUDE.md` failure mode 6 exists for, and the shared word plus the shared appearance of
> `11` (as `P(6) = 11` and as `q = 11`) makes this an unusually inviting trap. `P(6) = 11`
> is a fact about integer partitions; `q = 11` is the non-backtracking outdegree. The
> equality of the two 11s is a coincidence of small numbers.

I record this because I nearly made the connection myself while looking for where the
Hagedorn result belonged, and the grep that found these files found them **by the word**.

## What the thermal track does contain

Genuine thermodynamics lives elsewhere:

- `bt2937_2945_global_code_landauer_oam.py` — Landauer bounds on the global code.
- `w33_BREAKTHROUGH_459_vacuum_thermal_substrate_physics.py` — Stefan–Boltzmann, Wien, BEC
  critical density, Casimir `1/240 = 1/|E(W(3,3))|`.
- The blueprint's wattage figures (Passes 4336–4363), whose cadence assumption Pass 4363
  showed carries a 1000× span.

Pass 4453's Hagedorn temperature is **not** derived from, and does not derive, any of these.
It is a property of the graph's geodesic spectrum, in units where a geodesic of length `m`
has energy `m`. Converting it to joules would need a physical energy per edge-traversal,
which nothing here supplies — the same unit-gauge gap Pass 4411 found in the neutrino row.

## Evidence boundary

The identification `β_c = log q` is exact and follows from `π(m) ~ q^m/m`; it was located
numerically at Pass 4453 by the term ratio. The claim that `p_Ih` in the substrate-identity
passes is the same 11 as the non-backtracking outdegree rests on `bt565`'s own definition,
quoted above. Nothing here derives a physical temperature, and the homonym warning is a
warning, not a claim that anyone has made the error.
