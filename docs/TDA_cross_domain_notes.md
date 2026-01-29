TDA cross-domain notes: GBS ↔ Genomics

Summary:
- Motivation: Both GBS sample spaces (photon-count threshold vectors) and genomic sequence populations show multi-scale structure that TDA (persistence diagrams / Betti curves) can summarize.

Early observations from prototypes:
- GBS (modes 2–6, η sweep): JS divergence increases with modes and loss in some regimes; H1 feature counts grow with modes. Some parameter boundaries (modes=6, η~1.0) show the largest JS and Wasserstein changes.
- Genomics pilot (synthetic mutations): H1 counts increase with mutation rate (0.01→0.03→0.1), Wasserstein distances and JS between mean k-mer distributions increase accordingly.

Tentative connections and hypotheses:
- JS divergence captures distributional shifts while Wasserstein on persistence diagrams captures geometric/topological rearrangements; together they may reveal multiscale phase-like transitions in information structure.
- Scale-invariance candidates: growth rate of H1 features vs system size (modes or genome complexity) and the relative scaling of JS vs Wasserstein.

Next experiments:
1. High-precision follow-ups on top GBS parameter pairs (running now) to produce tight CI on JS and more stable persistent homology.
2. Larger genomics pilot using real small datasets (viral genomes / PPI subnet) to test transferability.
3. Statistical cross-correlation: compute bootstrap p-values for JS vs Wasserstein correlations across parameters.

Notes and tools:
- Scripts: `scripts/quantum_photonics/run_gbs_tda_grid.py`, `run_gbs_tda_highprec.py`, `run_gbs_tda_followup.py`, `run_gbs_genomics_pilot.py`.
- Libraries: ripser, persim, giotto-tda.

This note will be included in the PR as context for the TDA additions.