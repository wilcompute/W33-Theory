# Next steps — Quantum Photonics prototypes (prioritized)

1. GBS notebook: implement small-mode probability computation using The Walrus (hafnian) and compare to Strawberry Fields runs using the Gaussian backend where appropriate; implement fallback to Fock backend for small N where direct sampling is needed.
2. Implement a robust wrapper in `scripts/quantum_photonics/run_gbs.py` to: (a) choose backend (gaussian vs fock), (b) generate interferometers reproducibly, (c) compute classical emulator probabilities and KL/Jensen-Shannon metrics, (d) export JSON results and plots.
3. CV repeater notebook: implement full covariance matrix propagation under loss and entanglement swapping node, compute log-negativity and success rates; add quantum-scissors distillation module (optional).
4. Add unit tests (pytest) for core utilities and add GitHub Actions CI to run quick smoke tests (import checks and small deterministic runs).
5. Add more papers to the annotated bibliography and extract figures/claims (automated PDF fetch + parse).

Estimated time: 6–12 hours for items 1–3 (depending on simulation depth), 2–4 hours for items 4–5.
