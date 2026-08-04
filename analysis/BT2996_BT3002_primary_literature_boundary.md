# Passes 2996–3002 — primary-literature boundary

The repository results are exact finite calculations or explicitly modeled policies. The references below motivate the engineering abstractions; no published performance number is imported as a Holonet measurement.

## Adaptive testing

Aldridge, *Adaptive group testing as channel coding with feedback*, arXiv:1203.5927, formulates adaptive group testing information-theoretically. Li et al., *Group Testing with Prior Statistics*, arXiv:1401.3667, develops adaptive maximum-entropy and Shannon–Fano/Huffman policies under nonuniform defect priors. Passes 2996 and 2999 differ technically because their observations are nonabelian `D4` triangle products rather than Boolean OR tests, but the information-gain and prior-weighted decision principles are analogous.

## Pauli and frame tracking

Paler et al., *Software Pauli Tracking for Quantum Computation*, arXiv:1401.5872, establishes that teleportation/QEC byproducts can be propagated classically and output results reinterpreted instead of applying physical corrections. Ryan-Anderson et al., arXiv:2107.07505, demonstrates real-time fault-tolerant correction using both software Pauli-frame updates and physical gates. These support the conditional Pass-3000 rule that frame-covariant byproducts should not automatically become hardware gates.

## Self-synchronizing coding

Fujiwara and Tonchev, *High-Rate Self-Synchronizing Codes*, IEEE Transactions on Information Theory 59(4), 2328–2335 (2013), DOI 10.1109/TIT.2012.2234501, constructs error-tolerant self-synchronizing codes from difference systems of sets. Pass 3001 is a new exact length-12 four-symbol cyclic search tailored to the Holonet pilot geometry; it does not claim to supersede the general coding literature.

## Predictive thermodynamics

Still, Sivak, Bell, and Crooks, *Thermodynamics of Prediction*, Physical Review Letters 109, 120604 (2012), DOI 10.1103/PhysRevLett.109.120604, relates nonpredictive memory to thermodynamic inefficiency. Pass 3002 uses that principle only as a design boundary: it computes the exact entropy of the next-action statistic for one frozen decision prior. Physical dissipation still requires a temperature, finite-time reset protocol, and hardware model.

## Claim boundary

- No external source proves the repository’s 23/24/25 adaptive depth census.
- No external source proves the exact W33 transvection diameter-two library.
- No external source proves optimality of `102332001123`; that proof is internal and finite.
- Literature supports the abstractions and implementation policies, not the project-specific numerical results.
