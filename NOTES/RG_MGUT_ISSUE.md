RG / M_GUT discrepancy diagnostic
=================================

Summary:
- Running `V42_FULL_PRECISION_MASSES.py` with the repository's `w33_alpha_gut()` and `w33_m_gut()` produces a numerically nonphysical RG flow for QCD: the integrated `alpha_s(M_Z)` from the GUT starting point becomes enormous (and in fact the Euler/RK integrator encountered overflow), indicating a Landau-like pole between the GUT and M_Z scales under the current conventions.

What I changed for diagnostics:
- Fixed MS-bar two-loop beta-function normalization in `V42_FULL_PRECISION_MASSES.py` (beta0/(2π), beta1/(4π^2)).
- Replaced the simple integrator with a robust RK4 stepper and safety clamps.
- Added detection of nonfinite / runaway `alpha_s(M_Z)` values; when detected the script falls back to the PDG value `alpha_s(M_Z)=0.1179` for threshold-running so the remainder of the mass table can be computed and a structured report produced.

Observed outcome:
- The RG integration still yields a nonphysical `alpha_s(M_Z)` (>>1) when starting from the repo's `w33_alpha_gut()` and `w33_m_gut()`. The fallback to PDG alpha produces a stable mass-table run, but the heavy mismatch signals that the mapping between the repo's GUT coupling/scale definitions and the QCD MS-bar coupling is inconsistent or missing group-theory/threshold conversions.

Suggested next actions (theory + code):
1. Theoretical review: verify the definition of `w33_alpha_gut()` and `w33_m_gut()` and whether these are meant to represent the SU(3)_c coupling in MS-bar at M_GUT or instead a model-level unified normalization that requires conversion (group factors, trace normalization, embedding factors).
2. If `w33_alpha_gut()` is a model-level quantity, implement conversion code to produce the SU(3) MS-bar coupling at M_GUT, including any normalization by `Tr(T_a T_b)` and (if necessary) heavy-threshold matching.
3. Add a toggle in `V42_FULL_PRECISION_MASSES.py` to (a) use repository GUT values if `--assume-gut-consistent` is passed (with warning), or (b) force PDG-anchored RG matching by default for numerically stable predictions.
4. Add unit tests and regression checks that assert `0 < alpha_s(M_Z) < 1` after RG integration and that the produced `V42_precision_masses_report.json` contains a diagnostic flag when fallback was used.

Immediate code artifacts created:
- `V42_FULL_PRECISION_MASSES.py`: beta-function fix, RK4 integrator, fallback behavior, and structured JSON report.
- `V42_precision_masses_report.json` (produced by the run).

If you want, I can:
- Implement an automatic conversion function for SU(3)_c coupling at M_GUT given the repository's GUT normalization (needs the theoretical mapping), or
- Open a PR with the current diagnostics and suggested TODOs for the physics review.


