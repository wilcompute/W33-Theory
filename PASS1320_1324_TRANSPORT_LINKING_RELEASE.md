# Passes 1320–1324 — Six-Channel Transport, Full Hecke Units, and the Linking Algebra

Status: **EXACT / machine-checkable**

## Pass 1320 — the six transports are species-resolved

The six orbital intertwiners in

\[
\operatorname{Hom}_{W(E_6)}(\mathbb C^{480},\mathbb C^{432})
\]

split exactly as

\[
\mathbf 1\;\oplus\;\mathbf{15}_a\;\oplus\;3\mathbf{20}\;\oplus\;\mathbf{60}_a.
\]

A deterministic Hecke-gauge alignment gives six mutually orthogonal channels. Their primitive orbital coefficient vectors are

\[
\begin{array}{c|c}
\text{species/copy} & (T_0,\ldots,T_5)\\ \hline
\mathbf1 & (1,1,1,1,1,1)\\
\mathbf{15}_a & (1,1,1,-3,-3,-3)\\
\mathbf{20}_0 & (1,-1,0,-3,0,3)\\
\mathbf{20}_1 & (1,-2,1,3,-3,0)\\
\mathbf{20}_2 & (1,1,-2,1,-2,1)\\
\mathbf{60}_a & (2,-1,-1,0,3,-3).
\end{array}
\]

Their squared singular scales are respectively

\[
207360,\quad41472,\quad20736,\quad31104,\quad20736,\quad10368.
\]

On this six-dimensional Hom-space, right Hashimoto action has spectrum

\[
11^1\oplus(-1)^5.
\]

## Pass 1321 — the complete noncentral Hecke algebra is explicit

The central decomposition from Pass 1315 is upgraded to all 26 rational matrix units. The noncommutative blocks are

\[
M_2(\mathbb Q)_{\mathbf6},\qquad
M_3(\mathbb Q)_{\mathbf{20}},\qquad
M_2(\mathbb Q)_{\mathbf{30}},\qquad
M_2(\mathbb Q)_{\mathbf{64}}.
\]

The deterministic symmetric splitters have spectra

\[
\{-2,2\},\quad\{-6,2,10\},\quad\{-2,2\},\quad\{-2,2\},
\]

and every relation

\[
E_{ij}E_{kl}=\delta_{jk}E_{il}
\]

is verified exactly over \(\mathbb Q\).

## Pass 1322 — Hashimoto cannot choose a species-20 copy

On the literal rank-20 species projector inside the directed-edge carrier,

\[
B\big|_{\mathbf{20}}=-I_{20}.
\]

Thus

\[
\mu_B(x)=x+1,
\qquad
\chi_B(x)=(x+1)^{20}.
\]

All three species-20 transport channels have the same Hashimoto eigenvalue \(-1\). Therefore Hashimoto dynamics alone does **not** select one of the three copies in the 432 carrier. A selection requires a chosen primitive Hecke idempotent—an explicit gauge choice—not a canonical dynamical distinction.

## Pass 1323 — the transport category closes to a linking algebra

Every product \(T_iT_j^*\) is expanded in the 26 Hecke matrix units, and every product \(T_i^*T_j\) is expanded in the species-refined Hashimoto projector basis. Their spans have dimensions

\[
12\quad\text{and}\quad4.
\]

Together with the two six-dimensional Hom corners, the complete common-support linking algebra has dimension

\[
12+4+6+6=28
\]

and exact Wedderburn form

\[
\boxed{
M_2(\mathbb C)\oplus M_2(\mathbb C)\oplus M_4(\mathbb C)\oplus M_2(\mathbb C)
}.
\]

The species-20 sector is the full Morita context

\[
M_3(\mathbb C)\;\dashv\;\mathbb C
\]

implemented by the three-dimensional bimodule \(\mathbb C^3\). This is an exact finite representation-theoretic theorem.

## Pass 1324 — manuscript claim ledgers promoted

Formal theorem/proof/retraction inserts are exported for both main manuscripts:

- `analysis/w33_paper_pass1320_1324_theorem_ledger.tex`
- `analysis/photonic_holonet_pass1320_1324_theorem_ledger.tex`

The chronological manuscript bodies remain intact under their declared historical-record policy. The companion ledgers are the active compile-ready theorem state.

## Reproduction

```bash
python analysis/w33_pass1320_1324_transport_linking.py
pytest -q tests/test_w33_pass1320_1324.py
```

Scope: finite permutation representations, rational association algebras, and equivariant intertwiners. No continuum, particle-physics, or hardware conclusion follows from these identities alone.
