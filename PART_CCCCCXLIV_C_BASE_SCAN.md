# PART_CCCCCXLIV_C — Small-Base Scan for 7 and W(3,3) Visibility

## Goal

Systematically scan small integer bases \(b\) and quantify how clearly each
base makes the \(7\)-structure and W(3,3) mod-7/mod-12 patterns "visible" in
its positional numeral system.

We are especially interested in:

1. **Full-reptend condition for 7**: \(\operatorname{ord}_7(b) = 6 = 7-1 = g_2\).
2. **Single-digit 7**: \(b > 7\) so that 7 is a single digit in base \(b\).
3. **Single-digit denominator scan**: for bases \(b \ge 10\), denominators
   \(1/n\), \(n=1,\dots,9\), are all single-digit and can be compared directly.
4. **Uniqueness of 1/7 period spike**: in the period spectrum of \(1/n\),
   \(n=1,\dots,9\), 1/7 should have uniquely maximal period.

This file describes the logic; the script `PART_CCCCCXLIV_C_BASE_SCAN.py`
implements it and prints detailed tables.

## Definitions

For each base \(b\):

- Factorization: \(b = \prod p_i^{e_i}\) with primes \(p_i\).
- Termination criterion: 1/n terminates in base \(b\) iff every prime divisor
  of \(n\) is among the \(p_i\).
- Period of 1/n in base \(b\): multiplicative order
  \(\operatorname{ord}_n(b)\) when \(\gcd(b,n)=1\), else 0 (terminating).
- Full-reptend for 7 in base \(b\): \(\operatorname{ord}_7(b) = 6\).

We scan bases \(b\) in a small range (default 2 to 36) and compute:

- \(\operatorname{ord}_7(b)\)
- whether 7 is a single digit (\(b>7\))
- for bases \(b\ge10\): decimal-like period spectrum \(\{\operatorname{period}_b(1/n)\}_{n=1}^9\)
- whether 1/7 has uniquely maximal period in \(n=1..9\)

## Heuristic "visibility" score

A base \(b\) is considered **high-visibility** for the 7/W(3,3) structure if:

1. \(b > 7\) (7 is a single digit),
2. \(\operatorname{ord}_7(b) = 6\) (full-reptend), and
3. 1/7 has **unique** maximal period among \(1/n\), \(1\le n \le 9\).

Base 10 is known to satisfy all three. The script checks which other bases in
\(2 \le b \le 36\) satisfy these conditions.

## Expected patterns

- Bases with \(b \equiv 3,5 \pmod{7}\) and \(\gcd(b,7)=1\) should have
  \(\operatorname{ord}_7(b)=6\) (primitive roots mod 7 classes).
- Among these, bases \(b>7\) give single-digit 7.
- Among bases \(b\ge10\), the period spectra \(1/n\), \(n=1..9\), will differ
  in how sharply they single out 7.

The script prints a ranked list of candidate bases, allowing us to see where
base 10 sits in the "visibility" landscape and whether any other base is
arguably as good or better.

Run:

```bash
python PART_CCCCCXLIV_C_BASE_SCAN.py
```

and inspect the printed tables.
