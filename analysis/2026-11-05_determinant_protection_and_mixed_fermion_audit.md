# Colored determinants and mixed-fermion protection

This continuation applies an established axion-quality obstruction to the original D+Q+Q inventory, then tests a previously uncomputed fermion operator in the explicit protected replacement. It does not solve the TOE or supply one common UV action. The general determinant principle belongs to [Cheung, arXiv:1003.0941, section 2](https://arxiv.org/abs/1003.0941). [Bonnefoy, arXiv:2212.00102, sections III-IV](https://arxiv.org/abs/2212.00102) motivates checking heavy-field mediation rather than relying on scalar operator dimensions alone.

## 1. The original inventory has a degree-five obstruction

Assume ordinary anomaly-free four-dimensional protection, no Green-Schwarz term or inflow, and no additional colored fermions. The new masses come from renormalizable SM-singlet scalar couplings; heavy-SM and Higgs-induced D-Q mixing are excluded. SM quarks have full-rank renormalizable Yukawa matrices with one Higgs. A global PQ symmetry respected by these masses has a nonzero QCD anomaly.

There are five color-fundamental flavors: one D and the two weak components of each of two Q flavors. With arbitrary Q-flavor mixing the relevant polynomial is

\[
F=m_D(\Sigma)\,[\det M_Q(\Sigma)]^2.
\]

The QCD anomaly gives its transformation character. The SM contribution to the protecting mixed color anomaly vanishes by the full-rank one-Higgs Yukawa identities. Therefore anomaly cancellation makes F gauge invariant, while anomalous PQ makes it PQ charged. Each mass entry has scalar degree at most one, so F has degree at most five. Adding scalar fields or colorless anomaly-canceling fermions cannot remove this particular obstruction. Constants in the masses can lower the degree. This extends the repo's single-Sigma obstruction under the specified assumptions; it is an application of Cheung's general result.

The producer expands the generic determinant exactly and checks its magnitude in thirty independently changed unitary flavor bases. A separate enumeration covers all 64 diagonal assignments of D,Q1,Q2 masses to S,Sdag,T,Tdag. Forty have both protecting scalar charges nonzero; none has a primitive pure scalar invariant above degree five. These assignments alone do not certify all gauge anomalies.

For the existing supplied common heavy mass 27279937181.61975 GeV, reduced Planck mass 2.435e18 GeV and susceptibility (0.0756 GeV)^4, the allowed potential `-2 Re(c F/MP)` has amplitude/chi = **3.798924633535052e38 |c|**. A conservative sufficient condition for a phase-uniform theta bound below 1e-10 is **|c| < 2.632323871004147e-49**. F includes Yukawa factors. This coefficient convention is not a lower bound on independent monomial coefficients, a quantum-gravity prediction, or an exclusion of aligned phases.

Escapes require changing a hypothesis: the colored inventory, mass-generation/flavor sector, anomaly cancellation mechanism, or higher-dimensional/nonlocal axion origin. In particular, radiative flavor protection requires its own gauge anomalies, messenger spectrum and thresholds; invoking it by name does not complete this model.

## 2. The protected replacement allows dimension-nine fermion breaking

The explicit n=13 replacement in [the parent producer](toe_20261105_five_fronts_model_completion.py) has S,T charges (2,26), singlet Weyl charges N=1 and Nprime=-13, and renormalizable masses Sdag NN and T Nprime Nprime. General symmetric mass matrices are permitted; a paired Dirac texture is a special case. Choose PQ(S)=1, PQ(T)=0, PQ(N)=1/2 and PQ(Nprime)=0. Then

\[
\delta\mathcal L=\kappa\,S^6 NN'/M_P^5+\text{h.c.}
\]

is gauge invariant, Lorentz scalar and explicitly PQ breaking. Its canonical dimension is nine. An integer minimization, independently reproduced by dynamic programming in the tests, proves that no lower-dimensional PQ-breaking Lorentz scalar passes even the relaxed X-charge and fermion-parity rules for this inventory. Neutral SM fields and derivatives cannot reduce this bound. The singlet contraction attains it, so this is an actual allowed operator, not only a relaxed witness. The search includes conjugate charges; it does not enumerate all contractions or calculate full operator mixing.

The earlier **pure scalar** dimension-fourteen result remains valid. Extending that statement to every local operator would be incorrect; the parent explicitly left mixed fermion operators uncertified.

## 3. Its first potential term and the full flavor cost

For two left-handed Weyl fields take the symmetric mass matrix

\[
M=\begin{pmatrix}yS^*&\kappa S^6/M_P^5\\\kappa S^6/M_P^5&y'T\end{pmatrix}.
\]

Writing its entries as a,z,b, the phase-sensitive part of Tr[(Mdag M)^2] is **4 Re(a* b* z^2)**. The Weyl Coleman-Weinberg normalization is -1/(32 pi^2). Consequently two insertions generate `S^13 Tdag/MP^10`, with the same Planck power as the leading pure scalar term. In `V=2 Re(c S^13 Tdag/MP^10)`, the logarithmic counterterm obeys `dc/dln(mu)=-conj(y yprime) kappa^2/(8 pi^2)`. Unit fixed couplings and c(MP)=0 give a leading-log magnitude **0.18288655** at the supplied scalar scale 1.3038404810405298e12 GeV. This isolated calculation finds no enhanced inverse-heavy-mass term at this order.

There are actually **78 light and six heavy singlet Weyl fields**. The coefficient becomes the basis-invariant trace `Tr(YLdag kappa YHdag kappa^T)`. Pairwise Dirac mass matrices and a coherent all-ones mixing matrix give trace **468**, and a formal fixed-coupling coefficient **85.59090539**. This is a stress test, not a controlled UV evolution or a typical random-phase estimate. Complete running, finite matching and UV boundary data remain necessary. In particular, unit entries do not mean a unit matrix norm: the all-ones mixing matrix has Frobenius norm sqrt(468).

The useful sufficient inequality is

\[
|\mathrm{Tr}(Y_L^\dagger\kappa Y_H^\dagger\kappa^T)|
\leq \|Y_L\|_{op}\|Y_H\|_{op}\|\kappa\|_F^2.
\]

The tests check this trace in a complex changed basis and check the Coleman-Weinberg scale derivative numerically. A complete protected model must bound these matrices or evolve them. The scalar-only coefficient-one benchmark does not certify that requirement.

## Evidence, coverage and remaining work

Producer: `toe_20261105_determinant_and_fermion_quality.py`; output: `data/toe_20261105_determinant_and_fermion_quality.json`. The companion server JavaScript independently checks assignment counts, integer minima and quality arithmetic in actual server V8 while Remote Desktop Commander runs the PC producer. The validation harness replays the producer and nine new tests alongside 41 existing controls; its JSON records the actual result, source hashes and output hashes. The initial invocation with repository-wide conftest initialization finished nine tests in 156.75 seconds; the focused replay uses `--noconftest` and passed fifty tests in 39.93 seconds. A stop attempt after the initial delay found that test process had already exited.

The corpus search is result-oriented and bounded, with its exclusions recorded; it is not a novelty proof. The recent incoming e4cdbaa6c commit reserves 12616-12620 and contains no new scientific results to accept. PDF text pages **61-64** were additionally read in full, including prior native-gravity constraint failures and supplied flavor constructions. Cumulative coverage is **1-64 of 215 pages**; the complete PDF and complete past-week patch review remain unfinished.

The other ongoing fronts remain substantive open problems: complete SM/sterile/operator RG and matching; a global local chiral measure beyond the finite toron controls; generic nonlinear native gravity constraints; and a shared action that supplies both particle masses and gravity without independently fitted scales. This packet advances the protection front and its flavor connection. It does not claim to have completed all those fronts.
