# Part CXXVIII — Loop-Conditioned Probability and First Self-Consistency

**Status:** theorem-grade structural extension  
**Date:** April 29, 2026

This part formalizes the intuition that probability becomes nontrivial only after a loop/self-consistency condition is imposed.  In the W(3,3) carrier this is not philosophical decoration: it is an exact theorem for the Hashimoto non-backtracking operator.

## 1. Local propagation without a loop

Let `B` be the Hashimoto operator on the 480 directed edges of the W33 collinearity graph.  Every directed edge has exactly

```text
k - 1 = 11
```

allowed non-backtracking continuations.

If no loop condition is imposed, a length-`n` local history from a fixed directed edge has

\[
11^n
\]

possible continuations.  The normalized local Markov operator is

\[
P = \frac{1}{11}B,
\]

and each row of `P` sums to one.  In this sense the unconditioned propagation has total probability `1`: all locally allowed histories survive.

There is no global selection yet.

## 2. The loop condition

A loop condition asks that the local history return to its starting directed edge after `n` non-backtracking transitions.  The number of globally self-consistent closed histories is

\[
Z_n = \operatorname{Tr}(B^n).
\]

For a fixed directed edge `e`, transitivity gives

\[
\#\{\text{closed length-}n\text{ histories based at }e\}
=\frac{Z_n}{480}.
\]

Thus the loop-closure probability is

\[
\boxed{
\Pr_n(\mathrm{loop}\mid e)
=\frac{Z_n}{480\cdot 11^n}.
}
\]

This is the finite version of the principle:

```text
local propagation gives possibility;
loop closure gives realized probability.
```

## 3. Exact W33 loop partition function

The Ihara--Bass formula for a 12-regular graph gives the Hashimoto trace exactly.  With adjacency spectrum

\[
12^1,\quad 2^{24},\quad (-4)^{15},
\]

and `m-n=240-40=200`, define

\[
S_0(\lambda)=2,
\qquad
S_1(\lambda)=\lambda,
\qquad
S_n(\lambda)=\lambda S_{n-1}(\lambda)-11S_{n-2}(\lambda).
\]

Then

\[
\boxed{
Z_n
=200(1+(-1)^n)+S_n(12)+24S_n(2)+15S_n(-4).
}
\]

Equivalently, using the Hashimoto eigenvalues,

\[
Z_n = 200(1+(-1)^n)+(11^n+1)
+24\left[(1+i\sqrt{10})^n+(1-i\sqrt{10})^n\right]
+15\left[(-2+i\sqrt7)^n+(-2-i\sqrt7)^n\right].
\]

This is an exact integer for all `n`.

## 4. First self-consistency appears at length 3

The first values are

\[
Z_0=480,
\qquad
Z_1=0,
\qquad
Z_2=0,
\qquad
Z_3=960.
\]

So no one-step or two-step non-backtracking loop exists.  The first nontrivial loop appears at length three.

Per directed edge,

\[
\frac{Z_3}{480}=2.
\]

These two closures are exactly the two triangle turns through the initial edge.  Therefore

\[
\boxed{
\Pr_3(\mathrm{first\ loop}\mid e)=\frac{2}{11^3}=\frac{2}{1331}.
}
\]

This is the sharp mathematical version of the slogan:

```text
The first nontrivial probability in W33 is the triangle-loop condition λ=2
inside the 11-way non-backtracking branch space 2+9=11.
```

The open branch count `9` is what fails to close at the first loop.  The triangle branch count `2` is what survives the first self-consistency test.

## 5. Loop-conditioned probability measure

Let `h` range over length-`n` non-backtracking histories beginning at `e`, and let `C_n(h)` be the condition that the final directed edge is again `e`.  With uniform local weight,

\[
w(h)=11^{-n},
\]

we define the loop-conditioned probability by

\[
\boxed{
\Pr(h\mid C_n,e)=
\frac{\mathbf 1_{C_n(h)}}{Z_n/480}.
}
\]

So the loop condition does not add random noise.  It restricts local propagation to globally self-consistent histories and normalizes over the surviving closures.

## 6. Theorem CXXVIII

**Theorem CXXVIII (Loop-Conditioned Probability).**  In the W33 Hashimoto carrier, unconditioned local propagation has total probability one over all `11^n` non-backtracking continuations, while nontrivial realized probability appears only after imposing a loop/self-consistency condition.  The loop partition function is

\[
Z_n=\operatorname{Tr}(B^n),
\]

with exact recurrence formula above.  The first nonzero loop condition occurs at `n=3`, where each directed edge has exactly two closed histories among `11^3` local histories:

\[
\boxed{
\Pr_3(\mathrm{loop}\mid e)=2/11^3.
}
\]

## 7. Conceptual translation

The mathematical content supports the following precise interpretation:

```text
feed-forward propagation: locally allowed histories, total probability 1;
loop-conditioned propagation: globally self-consistent histories, nontrivial probability distribution;
first W33 closure: triangle loop λ=2 selected from 11 local non-backtracking branches.
```

This gives a clean finite model for the idea that a state becomes `realized` only when local information is closed by a global consistency loop.

## 8. Connection to the recent MUB-frame law

Part CXXIV found that product overlap is the fixed-point count of the relative `S4` skeleton, while the entangled overlap is the binary-octahedral lift correction.  The same structural principle is visible here:

```text
local skeleton + global loop condition = realized state/probability.
```

For the Hashimoto carrier, the local skeleton is the 11-branch non-backtracking rule and the global loop condition is `trace(B^n)`.  For the MUB-frame carrier, the local skeleton is the relative `S4` product law and the global correction is the binary-octahedral lift/chirality law.

The two are the same architecture at different levels.

The accompanying regression tests are in:

```text
tests/test_loop_condition_probability_cxxviii.py
```
