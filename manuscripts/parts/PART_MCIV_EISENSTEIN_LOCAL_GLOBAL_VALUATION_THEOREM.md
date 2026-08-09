# Part MCIV: Eisenstein Local-Global Valuation Theorem

The cyclotomic packet can now be stated in fully local-global Eisenstein language rather than only as a residue-class shadow.

Let
\[
\Phi_3(q)=q^2+q+1=N(q-\omega),
\qquad
\Phi_6(q)=q^2-q+1=N(q+\omega)
\]
in the Eisenstein integers $\mathbb{Z}[\omega]$, where $\omega^2+\omega+1=0$ and $N(a+b\omega)=a^2-ab+b^2$.

Fix a split prime $p\equiv 1\pmod 3$. Then
\[
(p)=\pi_r\,\bar\pi_r
\]
for exactly two conjugate prime ideals, which can be written as
\[
\pi_r=(p,\omega-r),
\qquad
\bar\pi_r=(p,\omega-r')
\]
where $r,r'$ are the two Hensel-lifted nontrivial cube roots of unity attached to the branch modulo powers of $p$.

## The exact branch criterion

On the matching branch, the valuation depth is no longer merely a congruence heuristic. It is exact:

\[
v_{\pi_r}(q-\omega)=n
\iff
q\equiv r \pmod{p^n}
\text{ but not }\pmod{p^{n+1}},
\]
and similarly
\[
v_{\pi_r}(q+\omega)=n
\iff
q\equiv -r \pmod{p^n}
\text{ but not }\pmod{p^{n+1}}.
\]

Equivalently,

\[
v_p\!\bigl(\Phi_3(q)\bigr)=n
\iff
v_{\pi_r}(q-\omega)=n
\]
on the $\Phi_3$ branch, and

\[
v_p\!\bigl(\Phi_6(q)\bigr)=n
\iff
v_{\pi_r}(q+\omega)=n
\]
on the $\Phi_6$ branch.

So the Hensel tree and the prime-ideal tree are literally the same object viewed in two coordinate systems: one on integers mod $p^n$, the other on valuations in $\mathbb{Z}[\omega]$.

## Why this sharpens the packet

Earlier parts established:

- split-prime support,
- the residue classifier mod $p^2$,
- the full $p$-adic valuation tree,
- the local density law $\mu(v_p\ge n)=2/p^n$.

This theorem identifies the hidden algebraic mechanism underneath all four. The packet is not simply a collection of congruence classes. It is the valuation packet of $q\mp\omega$ under the two split prime ideals above $p$.

In particular, the Heawood cube event
\[
\Phi_3(18)=\Phi_6(19)=343=7^3
\]
is exactly the statement that the corresponding Eisenstein prime above $7$ occurs with valuation $3$ on the matching branch.

## Local-global interpretation

At each split prime, there are exactly two branches, one for each prime ideal above $p$. The full packet is therefore a restricted product of local branch choices. The finite residue conditions glue by CRT on the integer side; on the algebraic-number-theory side, the prime-ideal valuations glue because norms multiply.

That is the clean local-global bridge:

\[
\text{branch residue data mod }p^n
\quad\Longleftrightarrow\quad
\text{prime-ideal valuation data in }\mathbb{Z}[\omega].
\]

So the cyclotomic defect process is not only split-prime and not only $p$-adic. It is genuinely an Eisenstein valuation process.
