# Part DCCLXXIII - Toroidal Markov / E6 Burden Bridge

**Scripts:**

- `scripts/tomotope_toroidal_markov_algebraic_closure_bridge.py`
- `scripts/tomotope_toroidal_markov_cubic_recurrence_bridge.py`
- `scripts/tomotope_toroidal_markov_generating_function_bridge.py`
- `scripts/tomotope_toroidal_markov_trace_generating_function_bridge.py`
- `scripts/tomotope_toroidal_markov_trace_recurrence_bridge.py`
- `scripts/w33_e6_so10_charge_moment_bridge.py`
- `scripts/w33_e6_sm_burden_of_proof_bridge.py`

**Focused suite:** `python scripts/run_focused_bridge_tests.py markov-e6-burden`

---

## 1. What This Adds

DCCLXXIII extends the existing toroidal/tomotope Markov chain from the DC-DCII
line into a closed arithmetic compiler:

```text
lambda_k = 1/8 + (3/4) cos(2*pi*k/7), k = 1..6
512*x^3 - 168*x - 7 = 0
m_{n+3} = (21/64)m_{n+1} + (7/512)m_n
```

The six nontrivial modes are therefore not just a numerical spectrum. They are
one exact cubic packet with doubled roots, exact moment recurrence, exact
moment generating function, exact trace generating function, and exact trace
recurrence.

---

## 2. Markov Closure

The nontrivial moment sequence starts:

```text
m_0 = 6
m_1 = 0
m_2 = 21/16
```

The ordinary generating function is:

```text
M(z) = (6 - (21/32)z^2) / (1 - (21/64)z^2 - (7/512)z^3).
```

For the 8-state toroidal Markov operator:

```text
T(z) = sum_{n>=1} Tr(P^n) z^n = z/(1-z) + (M(z)-6).
```

Its denominator yields the exact trace recurrence:

```text
t_n = t_{n-1} + (21/64)t_{n-2} - (161/512)t_{n-3} - (7/512)t_{n-4}.
```

This makes the toroidal transport loop a finite rational control system rather
than a floating spectral observation.

---

## 3. E6 / SO(10) Charge Moments

The companion E6 branch is:

```text
27 = 16_{-1} + 10_{+2} + 1_{-4}.
```

Its exact charge moments are:

```text
M0 = 27
M1 = 0
M2 = 72
M3 = 0
```

After three generations:

```text
M0 = 81
M2 = 216
```

The same packet links to the root split:

```text
240 = 72 + 6 + 81 + 81.
```

---

## 4. Burden Certificate

The final certificate deliberately stays narrow. It combines:

- `81 = 3 * 27`
- `27 = 16 + 10 + 1`
- exact Standard Model anomaly cancellation per generation
- the running reciprocity invariant from DCCLXV
- the Markov cubic and recurrence closure above

This is a burden-of-proof bridge, not a full symbolic branching-functor proof.
It states which exact finite arithmetic already closes and which representation
theorem still has to be supplied separately.
