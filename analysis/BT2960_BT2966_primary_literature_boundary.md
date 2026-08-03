# Passes 2960–2966 primary-literature boundary

The Pass 2963 simulator treats OAM crosstalk, phase stability, insertion loss, detector efficiency, and time/frequency sorting fidelity as independent configurable parameters. This is consistent with primary experimental mode-sorting literature, but the committed profiles are deliberately synthetic and are not fitted to any one apparatus.

Relevant primary anchors include:

- Yan et al., *Mode division multiplexing using an orbital angular momentum mode sorter and MIMO-DSP over a graded-index few-mode optical fibre*, Scientific Reports 5, 14931 (2015).
- Fontaine et al., *Laguerre-Gaussian mode sorter*, Nature Communications 10, 1865 (2019).
- Serino et al., *Programmable high-dimensional mode-sorting of time-frequency states of single photons*, CLEO FS 2024.
- Vu and Saito, *Finite-Time Quantum Landauer Principle and Quantum Coherence*, Physical Review Letters 128, 010602 (2022).
- Lee et al., *Speed Limit for a Highly Irreversible Process and Tight Finite-Time Landauer's Bound*, Physical Review Letters 129, 120603 (2022).
- Baumeler and Wolf, *Free energy of a general computation*, Physical Review E 100, 052115 (2019).

These papers motivate the modeled failure channels and the distinction between logical reversibility and finite-time thermodynamic cost. They do not certify the Holonet optical carrier, its component budget, or the synthetic profile numbers.
