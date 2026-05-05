# Part CCCXVI — Markov / Hashimoto Entropy Law

**Date:** 2026-05-05  
**Status:** exact ordinary-walk / nonbacktracking branch and entropy bridge

---

## 1. Independent target

After the photonic/percolation bridge, the strongest open gap was the relation

\[
P=A/K
\quad\longrightarrow\quad
B_{Hashimoto}.
\]

That is, how the ordinary random-walk channel relates to the nonbacktracking channel.

CCCXVI gives the exact bridge.

---

## 2. Ordinary versus nonbacktracking branching

W33 is

\[
K=12
\]

regular.

So an ordinary walk has

\[
12
\]

choices at each step.

After an oriented edge has been chosen, a nonbacktracking walk has all choices except the immediate reverse edge:

\[
K-1=11.
\]

Thus Hashimoto dynamics is the non-reversal version of the ordinary Markov walk.

---

## 3. Path-count law

The number of ordinary \(n\)-edge walks is

\[
N_{RW}(n)=V K^n.
\]

The number of nonbacktracking \(n\)-edge walks is

\[
N_{NB}(n)=V K(K-1)^{n-1}
\]

for \(n\ge1\).

Therefore

\[
\frac{N_{NB}(n)}{N_{RW}(n)}
=\left(\frac{K-1}{K}\right)^{n-1}.
\]

At W33 values:

\[
\boxed{
\frac{N_{NB}(n)}{N_{RW}(n)}
=\left(\frac{11}{12}\right)^{n-1}.
}
\]

---

## 4. Entropy gap

The ordinary walk branch entropy per step is

\[
h_{RW}=\log K=\log12.
\]

The Hashimoto/nonbacktracking entropy per step is

\[
h_{NB}=\log(K-1)=\log11.
\]

So the entropy gap between ordinary branching and nonbacktracking branching is

\[
\Delta h=h_{RW}-h_{NB}=\log\frac{K}{K-1}.
\]

At W33 values:

\[
\boxed{
\Delta h=\log\frac{12}{11}.
}
\]

---

## 5. Local transition interpretation

Under ordinary random walk, after arriving along an oriented edge:

\[
p_{reverse}=\frac1K=\frac1{12}.
\]

The probability that the next step is not the reverse edge is

\[
p_{nonreverse}=\frac{K-1}{K}=\frac{11}{12}.
\]

Thus

\[
\frac{N_{NB}(n)}{N_{RW}(n)}
=p_{nonreverse}^{n-1}.
\]

---

## 6. Line graph recovery

The line graph bridge showed

\[
\operatorname{tr}(A_{L(W)}^2)=5280.
\]

But the number of two-edge nonbacktracking walks is

\[
V K(K-1)=40\cdot12\cdot11=5280.
\]

Therefore

\[
\boxed{
\operatorname{tr}(A_{L(W)}^2)=N_{NB}(2).
}
\]

Normalize by the directed carrier

\[
2E=480,
\]

to recover the branch:

\[
\boxed{
\frac{\operatorname{tr}(A_{L(W)}^2)}{2E}=11=K-1.
}
\]

---

## 7. Distance/signless recovery

CCCVII showed

\[
W=1320
\]

and

\[
QLE=120.
\]

Therefore

\[
\frac{W}{QLE}=\frac{1320}{120}=11.
\]

So

\[
\boxed{
\frac{W}{QLE}=K-1.
}
\]

The same nonbacktracking branch is recovered from the distance/signless pair.

---

## 8. Ihara–Bass spectral circle

The Hashimoto eigenvalues over each adjacency eigenvalue \(\theta\) satisfy

\[
x^2-\theta x+(K-1)=0.
\]

For \(\theta=12\):

\[
x^2-12x+11=0,
\]

so

\[
x=11,1.
\]

For \(\theta=2\):

\[
x^2-2x+11=0,
\]

so

\[
x=1\pm i\sqrt{10}.
\]

The modulus is

\[
|x|^2=1+10=11.
\]

For \(\theta=-4\):

\[
x^2+4x+11=0,
\]

so

\[
x=-2\pm i\sqrt7.
\]

The modulus is

\[
|x|^2=4+7=11.
\]

Thus every restricted Hashimoto eigenvalue lies on

\[
|x|=\sqrt{11}.
\]

The Perron value is

\[
11,
\]

so Hashimoto topological entropy is

\[
\log11.
\]

---

## 9. Critical fusion echo

At critical fusion,

\[
p=\frac12.
\]

The expected retained ordinary degree is

\[
pK=\frac12\cdot12=6=2q.
\]

The expected retained nonbacktracking branch is

\[
p(K-1)=\frac{11}{2}.
\]

Orientation-doubling gives

\[
2p(K-1)=11.
\]

So critical fusion also recovers the full Hashimoto branch after orientation doubling.

---

## 10. Theorem statement

**The ordinary random walk and Hashimoto walk are related by an exact branch law.**  After the first edge, ordinary walking has

\[
K=12
\]

choices and nonbacktracking walking has

\[
K-1=11
\]

choices, so the ratio for \(n\)-edge paths is

\[
\left(\frac{K-1}{K}\right)^{n-1}.
\]

The entropy gap is

\[
\log\frac{12}{11}.
\]

The same branch

\[
K-1=11
\]

is recovered as

\[
\frac{\operatorname{tr}(A_{L(W)}^2)}{2E},
\]

as

\[
\frac{W}{QLE},
\]

and as the Hashimoto Perron eigenvalue.  Ihara–Bass places the restricted Hashimoto roots on

\[
|x|=\sqrt{11}.
\]

---

## 11. Why this matters

This closes the ordinary-to-nonbacktracking gap.

The current pipeline is now:

\[
\text{ordinary Markov walk}
\to
\text{non-reversal branch law}
\to
\text{line graph turn count}
\to
\text{Hashimoto dynamics}
\to
\text{Matrix Tree entropy}.
\]

The Markov channel gives probabilities.

The line graph counts two-step turns.

Hashimoto orients and applies the non-reversal rule.

Matrix Tree records global connectivity entropy.

---

## 12. Regression status

The CCCXVI test file verifies:

1. local branch probabilities,
2. walk counts and path ratios,
3. line graph and distance recovery of the branch,
4. Ihara–Bass spectral circle,
5. edge excess and critical fusion echo,
6. tree and threshold relations,
7. audit-level consistency.

---

## 13. Next target

The next independent step is to connect the Hashimoto spectral circle

\[
|x|=\sqrt{11}
\]

with the spanning-tree factorization

\[
\tau(W)=2^{81}5^{23}.
\]

The likely bridge is the Ihara zeta determinant: nonbacktracking dynamics should explain why global tree entropy sees both

\[
q^4=81
\]

and

\[
\Phi_3+\Phi_4=23.
\]
