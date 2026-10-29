# Three-photon W33/dual discrimination: corrected global shot counts and conditional loss model

**October 29, 2026.** \`analysis/w33_20261029_three_photon_loss_global_budget.py\` extends the *existing* fixed-input, four-output W33/dual witness and corrects one earlier integer optimization error in its trial-count table.

For real common pairwise overlap \(s\), the **previously proven** event probabilities are
\[
p_W(s)=\frac{17496+52488s^2+34992s^3}{15^6},\qquad
p_D(s)=\frac{3376+1328s^2-2048s^3}{15^6}.
\]
The exact optical formula is prior work. The new contribution is a **global discrete threshold optimization** and a carefully specified loss/background envelope.

For \(N\) independent trials and success threshold \(k\), the two errors are
\[
\mathrm{FN}=\Pr_{p_W}[\mathrm{Bin}(N,p_W)<k],\qquad
\mathrm{FP}=\Pr_{p_D}[\mathrm{Bin}(N,p_D)\ge k].
\]
For each integer \(N\), the verifier finds the **smallest** threshold \(k\) meeting \(\mathrm{FP}<0.001\), then tests \(\mathrm{FN}<0.001\). It scans every \(N\) from one to the first viable count, rather than merely checking \(N-1\) against one previously chosen \(k\).

**Correction:** at \(s=0\), the true global minimum under these rules is **\(N=19,427\), \(k=15\)**, with FN approximately \(0.000999712\) and FP approximately \(0.000938946\). The prior certificate's \(N=20,333,k=16\) was a valid but nonminimal decision rule. At \(s=0.5,0.8,1\), the old results \(6,881/9\), \(2,437/5\), \(1,413/4\) remain unchanged. The original producer, certificate, tests and report have been corrected to prevent this error from propagating.

**Conditional loss model:** independently surviving each of three photons with probability \(\eta\) gives threefold survival \(\eta^3\). If a failed triple produces a *hypothesis-independent* false success with probability \(\beta\), the per-emitted-trial event probability is
\[
p_{\mathrm{obs},h}=\eta^3p_h+(1-\eta^3)\beta
\quad(h=W,D).
\]
At \(s=0.8\), \(\eta=0.9\), \(\beta=0\), the global minimum is \(N=3,345\), cutoff 5, versus ideal \(N=2,437\). With \(\eta=0.7,\beta=0\), it becomes \(N=7,115\). These are model-dependent source-to-detector budgets, not laboratory calibrations.

**Boundaries:** mode-dependent efficiencies, interferometer drift, correlated dark counts, number resolution, calibration uncertainty, and source multiphoton contamination are not modeled. The model assumes independent emitted trials and equal loss/background parameters across the two graph hypotheses; violating this assumption invalidates the simple likelihood comparison. Ordinary quantum optics predicts these probabilities—there is no claimed departure from quantum mechanics or direct TOE prediction.

The additional four-program packet includes a native XOR \(q=7\) distance search which remains inconclusive; neither this photonic correction nor the W33 spectral-dimension-three *external-lattice positive control* resolves the unsolved physical dynamics.
