# Current sterile-neutrino proposal: the scalar parent changes the verdict

The latest coupled sterile-neutrino proposal has a portal window, not yet a protected particle completion. Applying the repo's existing quantum-loop controls and specifying a minimal real scalar parent exposes two further requirements: a rapidly growing scalar self-coupling, and protection of both the sterile mass and the much heavier scalar threshold. The latest Lyman-alpha boundary also needs a full nonthermal transfer-function calculation before it can support an exclusion.

## What changed and what was actually read

The intake certificate `data/toe_20261106_changed_work_intake.json` enumerates **161 changed paths** from science commit829b86f29 through incomingbfbb685af. It records each patch segment's additions, deletions, headings, function definitions and scope flags. Fourteen top-level changed reports were read fully, together with the nested scorecard and selected source/certificate files:38 listed full-text paths. This is a complete path/patch-structure census and a partial full-content review. It is not a claim that every changed Python/JSON file, every weekly commit, or all215 paper pages were read. Full extracted-text paper coverage now reaches pages1-72, with page69 rendered and visually inspected in this continuation.

Pages69-72 reinforce a useful boundary: the exact Freudenthal quartic and quasiconformal separation reproduce established algebraic structures on the committed basis; the paper itself states that this supplies neither a physical black hole nor its charge lattice or dynamics. The real-form/signature choice is an additional issue. This algebra does not substitute for the threshold protection tested below.

The incoming `PASS12628_SIGN_OF_C_LINKS.md` addendum2 changes its sterile corridor to M_N around16-20keV with m_S around3-10TeV. The source `toe_uv/sterile_lya.py` obtains the lower edge by matching mean momentum per mass to thermal warm dark matter, then applies the older portal thermalization floor and clock ceiling. The actual JSON contains four open grid points: (16keV,3TeV), (16keV,10TeV), (18keV,10TeV), (20keV,10TeV). Every original and latest stored portal row is numerically replayed here.

## Ownership: the general quantum-loop obstruction was already ours

`toe_20261103_dark_radiative_stability.py` and its actual JSON already contain the Dirac Coleman-Weinberg curvature, three present-day matching subtractions, a residual along the background history, soft boson/fermion cancellation and its phase-only tradeoff. `toe_20261103_mechanism_portal_protection.py` already adds a specified supersymmetric portal RG leakage example. Those are prior methods, not new discoveries here.

The current calculation applies those controls to the newly specified **Majorana** masses and actual `toe_uv/line_drift.json` histories. The general problem and the need to test beyond present-day subtraction are established in [Garny, hep-ph/0606120](https://arxiv.org/abs/hep-ph/0606120). Its mass-dependent bounds have hypotheses and are not universal experimental exclusions.

For the declared reference b=.053, reduced Mpl=2.435e27eV and H0=1.4466703e-33eV, one Majorana gives

    V1 = -m(phi)^4/(32 pi^2) [ln(m(phi)^2/mu^2)-3/2]
    m(phi) = m0 exp[-b(phi-phi0)/Mpl]
    V1''(phi0) = b^2 m0^4/(4 pi^2 Mpl^2) [1+4 ln(mu/m0)].

At mu=m0, the16keV point gives **3.758e23 H0^2**. This is a subtraction/naturalness benchmark. Choosing mu=m0 exp(-1/4) makes this local contribution zero; arbitrary counterterms can match a chosen mass. Neither operation supplies a symmetry preserving the full history. Using the old three-subtraction prescription and the actual four frozen histories, the remaining16keV loop potential at z=.5 is **1.30e17 to3.32e17 times** the declared reference dark-energy density. That residual is also prescription dependent, not a new likelihood constraint.

The inherited equal boson/Majorana cancellation control needs a constant soft mass parameter Delta below approximately **2.61e-8eV** at16keV if its curvature is to stay below H0^2. This parameter is not the physical partner mass splitting, which is Delta^2/(2m), approximately **2.13e-20eV**. A realistic thermal parent, visible portal and supersymmetry-breaking sector have not been built together.

## An explicit parent potential and a continuous tradeoff

The freeze-in source leaves the scalar potential unspecified. Test the extra hypothesis

    Lkin = (d phi)^2/2 + (d S)^2/2
    V = lambda_S/4 [S^2-w(phi)^2]^2
    w(phi)=w0 exp[-b(phi-phi0)/Mpl],  mN=y w=y vS/sqrt2.

The canonical real-scalar vev is **w=vS/sqrt2**: this preserves both the incoming mass relation and its width Gamma=y^2 mS/(16pi), as in AppendixA of1609.01289. An initial implementation set w=vS while retaining both source relations; that mixed conventions and underestimated the quartic by a factor2. The producer, independent server and tests were corrected before publication. At S=w the exact Hessian is

    2 lambda_S w^2 [[wprime^2,-wprime],[-wprime,1]],

with eigenvalues zero and2lambda_S w^2(1+wprime^2). The induced light-field metric is1+wprime^2. At the current points wprime^2 is around1e-34, so the leading radial relation is m_S^2=2lambda_S w^2=lambda_S vS^2. A tadpole/cubic potential, another symmetry-breaking sector, or a phi-dependent quartic changes these hypotheses; no universal relation for every sterile model follows.

The existing equilibrium-parent decay approximation has Omega proportional to y^2 M_N/m_S and therefore v^2 proportional to M_N^3/m_S. Its portal floor scales as sqrt(m_S), while the clock ceiling scales as m_S/M_N^3. Combining them gives

    mS at the portal boundary = 2435.13GeV (M_N/16keV)^6
    lambda_S at that boundary = 5.34217 (M_N/16keV)^15.

These are algebraic consequences of the declared existing approximations, not exact freeze-in cosmology. [Hall et al.,0911.1120, equations6.9-6.10](https://arxiv.org/abs/0911.1120) provide the equilibrium decay yield; two sterile daughters supply a factor2. An independent server calculation integrates the Boltzmann collision term rather than copying the Python coefficient and uses numerical bisection instead of the closed-form boundary.

| M_N (keV) | m_S (TeV) | inferred lambda_S | scalar-only beta_lambda/lambda |
|---|---|---|---|
|16|3|9.989|1.139|
|16|10|369.958|42.170|
|18|10|259.834|29.617|
|20|10|189.419|21.591|

Here beta_lambda=18lambda_S^2/(16pi^2) for V=lambda_S S^4/4. This follows also by converting g=lambda_S/4 in [Tong's scalar RG equation3.109](https://www.damtp.cam.ac.uk/user/tong/sft/sfthtml/S3.html) and reversing its infrared flow convention. All four grid points exceed the displayed fractional-beta threshold1 under this minimal potential. This is a breakdown warning, not a nonperturbative exclusion. Formal one-loop pole locations are recorded with this limitation and are not physical cutoff predictions.

For illustration, imposing the additional **chosen** cuts lambda_S<=1 or lambda_S<=4pi gives upper sterile masses14.31keV or16.94keV respectively. Requiring only beta_lambda/lambda<1 gives16.54keV. These are conditional continuous boundaries, not measurements, and they cannot be combined with a mean-momentum proxy to claim a decisive observational no-go. The portal inequalities by themselves have no absolute20keV ceiling: the replay gives a30keV portal boundary at a105.8TeV parent mass. The original ceiling depends on the10TeV scan endpoint unless an extra cutoff or a specified scalar potential is imposed.

The moving valley also makes the heavy radial mass phi dependent. At mu=m_S(today), its formal one-real-scalar CW curvature is -b^2m_S^4/(8pi^2Mpl^2), with magnitude **2.32e56 H0^2** at3TeV. This is an unprotected threshold benchmark in the stated prescription. The large scalar couplings at all four grid points prevent treating these one-loop numbers as precise physical predictions. Feeble sterile Yukawas alone do not protect either varying physical mass. Fixing the radial mass independently of w would require additional field dependence or structure, which must itself be matched and checked.

## Why the Lyman-alpha correction remains a proxy

Matching <p>/m is not a transfer-function calculation. [Koenig, Merle and Totzauer1609.01289, AppendixC](https://arxiv.org/abs/1609.01289) explicitly compare scalar-decay examples for which average/free-streaming classification discards spectra that their power-spectrum analysis accepts. Those2016 examples do not establish compatibility with current data or with our coupled background; they establish the methodological limitation.

The server certificate includes a transparent counterexample: normalized isotropic shells with all momentum at p=1, versus weights.9 and.1 at p=.1 and9.1. Both have mean momentum1. At k*tau=pi their free-ballistic density kernels are respectively0 and0.88419. This kernel is the angular average j0(k*v*tau). It is **not** a self-gravitating cosmological transfer function, but proves that a common mean does not determine even free propagation. Consequently the new15.2/16.8keV thresholds and the claimed7.1keV exclusion remain heuristic for this production model pending the actual distribution and coupled transfer function.

Incoming6bbda5729 adds a recalled decay-spectrum shape and an rms matching estimate, shifting the proxy edge by3.66% to15.8/17.4keV, and freezes the16-20keV statement as S5. Its complete patch was read. This still does not compute a transfer function. An extended server control has **both** mean momentum2 and second moment5 equal: equal weights at1 and3, versus weights2/9,5/9,2/9 at.5,2,3.5. Their ballistic kernels at k*tau=pi are0 and0.12126. Matching two moments is useful but cannot certify a nonthermal cosmological exclusion. The latest X-ray claims remain explicitly memory-based in the incoming source; no new mixing-angle exclusion is endorsed here. Its queued `sign_grid.py` fixes the base cosmology separately for each sign and is not marginalized posterior evidence.

Incomingbfbb685af subsequently estimates late parent decays and narrows the proposed corridor to about16keV,3TeV, explicitly leaving the Boltzmann solution open. Its entire five-path patch was read. The actual `sterile_hh.json` additionally contains `T_decay_GeV` and `omega_if_whole_relativistic_population_decays`, which its displayed producer does not generate. That source writes only its x=20 late-population estimate. The two new table quantities therefore lack a reproducible derivation in the committed producer. Its portal-width calculation also declares <S>=vS and requires a convention reconciliation with the retained sterile mass/width formulas; our normalized parent audit does not provide that portal matching. These estimates and a recalled-spectrum proxy cannot establish the final corridor. The new summary and queued positive-sign shear refit are inventoried without claiming that the queued fit has produced results.

## A positive control: published star-axion matter

To test a concrete repair direction, the second server script reproduces the charge spectrum of [Banks, Kongsore and Weiner, Big Axions2606.05276v2, Tables1-2](https://arxiv.org/html/2606.05276v2). Its supplied four-site charge kernel is(5,1,5,5); its published scalar quality dimension is16. The full spectator inventory matters:22 types comprising52 colorless pairs accompany10 extra colored Dirac flavors and two Higgs doublets. This is the published model, not a new construction from W33.

The actual integer calculation verifies all20 symmetric Abelian cubic anomalies, all four mixed gravitational sums and every listed spectator mass term. PC tests reconstruct these sums independently and rebuild the gauge beta matrix with exact rational arithmetic. Applying the repo's already-owned full inverse-kinetic-matrix running method gives B_YY=247/9, with substantial hidden mixing. At a chosen common threshold1e12GeV, gY=.4 and zero initial mixing, equal hidden couplings.05 or.10 keep K positive to2.435e18GeV; .15 or.20 do not. The boundary is approximately.11569 in this charge convention. These are supplied matching inputs, not measured predictions. Finite thresholds, the complete scalar vacuum, generic-mass loop quality, spectator decays and a common seesaw/gravity embedding remain unaudited.

## Verification and remaining boundary

The companion Python producer and server-V8 calculations certify the continuous portal boundary, explicit parent Hessian, inherited CW controls, same-mean counterexample and the published-spectrum reproduction. Twelve targeted tests compare independent collision integration, numerical derivatives, actual stored rows, continuous mass boundaries, both actual server artifacts, rational anomaly/beta sums and kinetic eigenvalues. An initial eight-test ordinary pytest run passed in175.07s; its process had already exited when a stop was attempted. The focused nine-test replay used `--noconftest` to avoid unrelated legacy-fixture startup; it passed in7.91s, followed by a frozen nine-test replay in29.88s. The final twelve-test validation receipt records the expanded producer/test replay and hashes.

The separate native-boundary axion packet was published as5e0cac65a with35 focused tests and explicit guard limitations. Its two failed UV repairs motivate auditing every field added to a model. The same principle applies here: a portal window for a sterile fermion is insufficient until the scalar parent, loop potential, thermal history and protecting mechanism coexist in one action. No common gravity-matter completion or solved TOE is claimed.
