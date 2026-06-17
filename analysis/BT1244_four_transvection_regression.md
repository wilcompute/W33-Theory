# BT1244 -- Four-Transvection Regime Regression

## Purpose

BT1244 protects the BT1242 global four-transvection regime classifier inside the named Clifford/R3/recovery regression test.

## New asserted values

The regression now asserts:

\[
\binom{40}{4}=91390,
\]

32 stabilizer-orbit representatives, 16 unique word-metric profiles, and global order distribution

\[
24^{90},\quad 27^{40},\quad 72^{1440},\quad 576^{1620},\quad 648^{26640},\quad 51840^{61560}.
\]

It also asserts the full-order diameter split

\[
51840_{d=10}^{22680},
\quad
51840_{d=12}^{25920},
\quad
51840_{d=14}^{12960}.
\]

## Boundary

This adds regression protection. It does not add new classification beyond BT1242.

## File

- Updated test: `tests/test_bt1231_bt1233.py`
