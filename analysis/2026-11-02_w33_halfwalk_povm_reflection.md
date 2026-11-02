# 2026-11-02 — A half-revival quantum walk equals the route-POVM reflection

**Status:** Exact finite matrix identity and single-particle toy Hamiltonian, checked at q=3,5,7; NOT a physical derivation of J, time, spacetime, photons or gravity. Producer: `analysis/w33_20261102_quantum_walk_half_revival.py`; certificate `data/w33_20261102_quantum_walk_half_revival.json`.

## Setup

Let `G_q` be the point-collinearity graph of `W(3,q)` for odd prime powers q; its `v=(q+1)(q²+1)` vertices have `k=q(q+1)` neighbors. The adjacency matrix `A` satisfies the exact strongly regular identity

`A²=(q²-1)I - 2A + (q+1)J`.

Its spectrum is `k` (multiplicity 1), `r=q-1` (multiplicity `f=q(q+1)²/2`), and `s=-(q+1)` (remaining multiplicity). The positive-eigenspace spectral projector is

`E_+ = ((q²+1)(A+(q+1)I)-(q+1)J)/(2q(q²+1))`.

The producer verifies its idempotence, rank, and `R=I-2E_+` being a reflection **by exact integer matrix multiplication**.

## Exact dynamics

Choose the *declared* one-particle hopping Hamiltonian `H=J A` for real coupling `J>0` (units where ħ=1). Then

`U(t)=exp(-it H)=e^{-iJkt}E_0+e^{-iJrt}E_+ + e^{-iJst}E_-`.

For odd q, all three eigenvalues k,r,s are even and `k,s` have identical phase modulo 4, opposite to r. Consequently,

`U(pi/(2J)) = (-1)^((q+1)/2) (I-2E_+)`,
`U(pi/J) = I`.

These are exact matrix identities, and the model is strictly periodic. The global phase in the first identity is +1 at q=3, -1 at q=5, +1 at q=7.

At t=pi/(2J), the amplitude magnitude is `(q-1)/(q²+1)` for a destination identical or adjacent to the initial vertex, and `(q+1)/(q(q²+1))` for a nonadjacent destination, giving the transition probabilities

`p_same=p_adj=((q-1)/(q²+1))²`,
`p_far=((q+1)/(q(q²+1)))²`.

There are `k+1` near-or-same destinations and `v-k-1` far destinations, and these probabilities sum to 1. For q=3 the probabilities are **1/25** and **4/225** respectively (12 adjacent and 27 far). For q=5 they are `16/676` and `36/16900`; for q=7 `36/2500` and `64/122500`. This exact two-band fingerprint can test any implementation of the prescribed adjacency Hamiltonian.

## The previously missing link to our POVM

For q=3, the earlier 216-route frame `Z` obeys `Z.T Z=360E_+`. Therefore the half-revival gate has the simple identity

`U(pi/(2J))=I - (Z.T Z)/180`.

The verifier checks this **as an exact integer equality of 40×40 matrices**. This unites a dynamical unitary on the 40-vertex label space with the very same 24D eigenspace used to define the 216-output abstract POVM. The relation does **not** mean the walk implements the POVM as a quantum measurement: it is a reflection in 40D, while the POVM uses a 24D input and 216 output modes. A real device needs state preparation, correct couplings, interferometric readout and noise modeling.

## Falsification and continuum-limit firewall

A candidate 40-mode implementation must reproduce the group-invariant return/neighbor/far probabilities as functions of t and a full revival at pi/J within calibrated experimental errors. An experimentally nonuniform Hamiltonian will not generally preserve this identity. The identity has no free fine-structure, mass, or cosmological parameters; J is assumed, not calculated.

The point graphs have diameter two for all q; normalized Laplacian nonzero eigenvalues converge to 1, so the bare graph tower has no standard gapless spatial continuum. This **does not** rule out a different local cover, Hamiltonian, edge weighting, time-dependent coupling, or graph-refinement limit.

**Prior ownership:** the spectral idempotent and 24D route POVM are previously committed. The substantive new step here is their explicit half-revival relation for the adjacency quantum walk and the q=3,5,7 transition census.
