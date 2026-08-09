# Part MCLXXIX: 37 Bi-Split Matter Horizon Lock

## Claim Boundary

MCLXXIX is a finite arithmetic horizon theorem. It identifies the first open
prime after the MCLXXVIII `31#` closure as a simultaneous Gaussian/Eisenstein
split prime. It does not claim continuum dynamics and does not prove a formal
universality theorem.

## Statement

MCLXXVIII compressed the prime-trigger tower to

```text
Q = 21660532934040 = 108*31#.
```

The first open prime after the `31` horizon is

```text
37.
```

This prime is not just another lcm step. It is the first open bi-split horizon:

```text
37 = 1 mod 4, so 37 splits in Z[i],
37 = 1 mod 3, so 37 splits in Z[omega],
37 = 1 mod 12, so both splittings occur simultaneously.
```

The already-closed bi-split prime in the trigger tower is `13`; the next
bi-split channel after the `31` closure is `37`.

## W33 Witnesses

The horizon prime has three independent W33 forms:

```text
37 = v - q = 40 - 3,
37 = (q!)^2 + 1 = 6^2 + 1 = |6+i|^2,
37 = N_E(Phi6(q) + q*omega) = N_E(7 + 3*omega).
```

Here

```text
q = 3,
Phi3(q) = q^2 + q + 1 = 13,
Phi6(q) = q^2 - q + 1 = 7,
N_E(a+b*omega) = a^2 - a*b + b^2.
```

So the same integer is simultaneously:

- the W33 complement deficit `v-q`,
- the Gaussian matter pole `|6+i|^2`,
- the Eisenstein mixed norm `N_E(7+3*omega)`.

## Local Residue Data

The Gaussian splitting is visible modulo `37` because

```text
x^2 + 1 = 0 mod 37
```

has roots

```text
x = 6, 31 = +/-6 mod 37.
```

The Eisenstein split branches are

```text
x^2 + x + 1 = 0 mod 37
```

with roots

```text
x = 10, 26.
```

The base qutrit value `q=3` is not itself on one of these cyclotomic branches:

```text
Phi3(3) = 13,
Phi6(3) = 7,
37 does not divide either value.
```

So `37` is not a plain `q +/- omega` valuation event. It is a mixed horizon:
Gaussian matter norm on one side, Eisenstein `Phi6(q)+q*omega` norm on the
other.

## Superbeat Residue

The 31-closed superbeat lands on the W33 `mu` channel modulo the open horizon:

```text
Q mod 37 = 4 = mu = q + 1.
```

This residue is itself a square:

```text
4 = 2^2 = 35^2 mod 37.
```

The minimal bi-split closure is therefore

```text
R = 37*Q = 801439718559480 = 108*37#.
```

It preserves the scaled temporal/geometric duality:

```text
R/360 = 37*(Q/360),
R/81  = 37*(Q/81).
```

## Artifacts

- Analysis: `analysis/w33_bisplit_37_horizon.py`
- Tests: `tests/test_w33_bisplit_37_horizon.py`
- Result: `PART_MCLXXIX_BISPLIT_37_HORIZON_results.json`
