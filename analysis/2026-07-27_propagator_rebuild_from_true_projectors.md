# Step 2 — Exact Point-Carrier Functional Calculus

**Date:** 2026-07-27  
**Status:** COMPLETE

For `D=A-I` on the 40-point `W(3,3)` carrier,

`spec(D)=11^1+1^24+(-5)^15`,

and

`(D-11I)(D-I)(D+5I)=0`.

## Projectors

`P_11=(D-I)(D+5I)/160`, rank 1;

`P_1=-(D-11I)(D+5I)/60`, rank 24;

`P_-5=(D-11I)(D-I)/96`, rank 15.

They are exactly idempotent, pairwise orthogonal, and sum to the identity. Hence

`f(D)=f(11)P_11+f(1)P_1+f(-5)P_-5`.

## Heat, evolution, and resolvent

The positive heat operator is built from `D^2`:

`exp(-tD^2)=exp(-121t)P_11+exp(-t)P_1+exp(-25t)P_-5`,

so

`Tr exp(-tD^2)=exp(-121t)+24exp(-t)+15exp(-25t)`.

The signed semigroup `exp(-tD)` grows on the negative eigenspace and is therefore
not called a heat kernel. Unitary evolution and the resolvent are

`Tr exp(-itD)=exp(-11it)+24exp(-it)+15exp(5it)`,

`(zI-D)^-1=P_11/(z-11)+P_1/(z-1)+P_-5/(z+5)`.

## Trace tower

`Tr(D^n)=11^n+24+15(-5)^n`, beginning

`40,-40,520,-520,24040,114200`.

It obeys

`m_(n+3)=7m_(n+2)+49m_(n+1)-55m_n`.

The earlier values `17480,-61480` and the label `exp(-tD)` as a positive heat
kernel are corrected here.

## Certificate

- verifier: `analysis/w33_pass1133_true_spectral_functional_calculus.py`
- result: `data/w33_pass1133_true_spectral_functional_calculus.json`
- status: PASS
