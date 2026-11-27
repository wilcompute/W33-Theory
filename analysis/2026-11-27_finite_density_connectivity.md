# Finite-density exchange matter still loses connectivity

The fixed-particle result in `analysis/2026-11-27_cycle_connectivity_thermodynamic_limit.md` left open whether an extensive number of particles could stabilize a single cycle. On the same labeled simple degree-two ensemble, **connectivity still vanishes at every fixed finite matter inverse temperature and positive Wilson cycle weight, uniformly over particle number**. The proof compares graphs through their changed bonds and works even at half filling.

For a graph G, let H(G) be the sum of I−S over its edges, where S swaps the two site occupations, restricted to the k-particle sector. Write Z(G)=Tr exp(−b H(G)). For nonnegative couplings, adding r unit-strength edges changes the partition function by a factor in [exp(−br),1]. The upper bound follows from positive semidefinite I−S and eigenvalue monotonicity. For the lower bound, the negative Hamiltonian has nonnegative off-diagonal entries in the occupation basis. Its exponential has nonnegative entries by adding a scalar to the generator before exponentiation. Consequently the Gibbs expectation of the swap permutation is nonnegative, and the derivative of log Z with respect to the inserted edge coupling is −b(1−⟨S⟩) in [−b,0]. Integrate over each coupling. This uses the same positivity as the random-stirring representation of exchange. [Tóth's original pressure argument](https://web.ma.utexas.edu/mp_arc-bin/mpa?yn=93-62).

Cut one bond from each of m cycles, leaving m disjoint paths. Reinsert those m bonds to recover G, or join path ends cyclically with m new bonds to obtain an n-cycle C_n. Both bond sets give factors in [exp(−bm),1] relative to the common path partition. Therefore

```
exp(-bm) <= Z(G)/Z(C_n) <= exp(bm)
```

for every sector k, including sequences k(n) growing proportionally to n. No division by particle density or estimate of the many-body spectral gap is needed.

Let O_n(q) denote disconnected/connected odds without matter at per-cycle weight q. The odds with matter satisfy

```
exp(-b) O_n(q exp(-b)) <= O_n(q; matter) <= exp(b) O_n(q exp(b)).
```

Indeed each disconnected term contains q^(m−1) times the trace ratio. The prior exact cycle generating function then gives upper and lower probability bounds of order n^(-q exp(-b)/2) and n^(-q exp(b)/2), respectively, with constants independent of k. These are bounds on the decay, and the exact exponent with matter is still open. The prior Wilson floor q≥1/3 implies the same loss of connectivity even with size-dependent gauge coupling at fixed b. With size-dependent matter b, the two-cycle term alone gives a weaker direct sufficient criterion, exp(-2b) log n → infinity at fixed q, since the two-cycle odds grow as (q/2) log n.

The verifier diagonalizes the actual exchange Hamiltonian on individual cycles and convolves their canonical partition functions over particle counts. It checks every occupation sector and cycle type for n=6,8,10,12 at four inverse temperatures. The enumeration includes symmetry factors for repeated cycles and reduces to the previous exact generating-function result at b=0. Run `python analysis/toe_20261127_finite_density_connectivity.py`. The theorem concerns the supplied equilibrium exchange graph law. Changing the sign or form of the matter interaction, permitting higher valence, or asking for an actual spacetime continuum requires new input.

The proof also applies to any fixed local dimension d, in any sector of specified populations of the d basis labels. The bond still permutes product basis vectors, and the Hamiltonian preserves each population sector. Thus promoting the site from a qubit to the repo's two-qutrit exchange register does not rescue the connectivity limit for the same pair-swap Hamiltonian and graph measure. Higher shared-tick terms may define a different Hamiltonian.
