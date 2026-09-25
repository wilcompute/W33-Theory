# Pass 10942 — dark Strange to metaplectic universal VM port

Pass 10942 resolves the open dark-Strange resource question left by Pass
10941. It does **not** manufacture the ninth-root qutrit T state. Instead, it
proves an independent exact route from the repository's certified dark H27
Strange ray to the metaplectic reflection

\[
R=\operatorname{diag}(1,1,-1),\qquad |R\rangle=R|+\rangle,
\]

and welds that resource to every mode of the seven-qutrit VM. Qutrit
Clifford+R is approximately universal.

## Exact two-stage resource factory

In the current Pauli convention, the dark ray is Clifford-equivalent to

\[
|S\rangle=(|1\rangle-|2\rangle)/\sqrt2.
\]

Two copies projected onto the +1 eigenspace of \(Z_1Z_2\), with logical
operators \(\bar Z=Z_2\) and \(\bar X=X_1^2X_2\), produce
\(|N\rangle=(|1\rangle+|2\rangle)/\sqrt2\) with probability 1/2. Two Norell
states projected onto the +1 eigenspace of \(\omega X_1X_2\), with
\(\bar X=X_2\) and \(\bar Z=Z_1^2Z_2\), produce
\(X^2|U_Z(\pi/3,2\pi/3)\rangle\) with probability 1/4. The Pauli correction
\(X^2Z\) gives \(|R\rangle=(|0\rangle+|1\rangle-|2\rangle)/\sqrt3\).

These reductions are literature-owned by Anwar--Campbell--Browne and are
written explicitly in [Prakash (2020)](https://pmc.ncbi.nlm.nih.gov/articles/PMC7544352/).
The repository increment is an executable decoder in its own convention,
including exact logical-operator checks and the dark-H27/VM weld.

The pure four-Strange batch succeeds with probability 1/16. A naive full
restart consumes 64 Strange states on average; buffering the successful
intermediate Norell states reduces the expectation to 32 Strange states per
R state.

## Injection into the seven-qutrit VM

Controlled-X^2, with the resource as control and data as target, followed by
computational-Z measurement of the data qutrit, has Kraus branches

\[
K_m=3^{-1/2}R X^{-m},\qquad m=0,1,2.
\]

Pauli tracking converts them to the three conjugate reflections
\(X^mRX^{-m}\). Their projective closure has order four. The desired branch
appears with probability 1/3 on each repeat-until-success round, so one logical
R injection consumes three R states, or 96 buffered Strange states, on average.
The resource is genuinely magic: R is outside the qutrit Clifford group and
\(|R\rangle\) has maximum stabilizer fidelity 7/9.

Combining `R_INJECT(mode)` with the Pass 10941 `F/P/CZ` lowering gives the
approximately universal seven-qutrit Clifford+R instruction set described by
[Glaudell et al. (2022)](https://arxiv.org/abs/2202.09235). The parallel Fano
fabric certificate shows that Pass 10941's six P7 pair couplers already close
the Clifford target; the 21-edge K7 completion restores full Fano routing
symmetry but is not required for the algebraic universality claim.

## Exact noise boundary

For independently depolarized inputs
\(\rho_S(p)=(1-p)|S\rangle\!\langle S|+pI/3\), the producer derives

\[
q(p)=\frac{4p(3p^2-7p+6)}{(p+1)(5p^2-10p+9)}=\frac83p+O(p^2),
\]

and

\[
q(p)-p=\frac{-p(p-1)(5p^2-12p+15)}{(p+1)(5p^2-10p+9)}>0
\quad(0<p<1).
\]

The circuit is therefore a **resource converter, not a distiller**. A
pre-distilled Strange source or another protected preparation must precede it.

## Cyclotomic separation from the T lane

Finite qutrit stabilizer protocols preserve projective amplitude ratios in
\(K=\mathbb Q(\omega,\sqrt3)=\mathbb Q(\zeta_{12})\), a degree-four field.
The canonical T magic state requires \(\zeta_9\), whose minimal polynomial
\(x^6+x^3+1\) has degree six. Since six cannot divide four,
\(\zeta_9\notin K\). Thus no finite stabilizer-only protocol converts exact
Strange states into the Pass 10941 T state. The internal Strange lane closes
universality through R, independently of the ideal T-analyzer lane.

## Artifacts and boundary

- `analysis/w33_pass10942_strange_metaplectic_factory.py`
- `data/w33_pass10942_strange_metaplectic_factory.json`
- `tests/test_w33_pass10942_strange_metaplectic_factory.py`

This is an exact logical/algebraic resource theorem conditional on physically
preparing the certified dark Strange ray as a qutrit state. It does not prove
dynamical population of that ray, a distillation threshold, fault-tolerant
overhead, or a laboratory implementation.
