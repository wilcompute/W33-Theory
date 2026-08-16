# Passes 5619–5626 — deck parity, gauge transversality, magnetic continuum, and causal physics boundaries

## Status

Eight physics-directed attacks were executed against the current W33/s12/E6/Dirac frontier. Seven close with exact finite statements. Pass5623 closes the fixed-line representation theorem but keeps the explicit moving-12-to-F4 object dictionary fail-closed until the direct GAP conjugator runs.

## Pass 5619 — the q=3 double lift is signed, but the naive spinor identification fails

The standard two-qutrit Weil/metaplectic module is 9-dimensional. Its central symplectic element `-I` is represented by finite qutrit parity, with spectrum

\[
+1^5\oplus(-1)^4,
\]

not by scalar `-1`. Thus the ordinary two-qutrit Weil module is not automatically a spin-1/2-like projective module merely because the projective W33 carrier has a two-sheet vector lift.

The intrinsic 32-state `+/-` Segre lift behaves differently. The deck involution commutes with the magnetic Hamiltonian and gives

\[
32=16_+\oplus16_-.
\]

The signed sector has

\[
\operatorname{spec}H_-=-6^4\oplus-3^4\oplus3^4\oplus6^4.
\]

This is a genuine 16-dimensional signed deck module. It is **not** identified with either D5 half-spin 16. The repo's Pass346 no-go remains decisive: the full PGSp outer controller swaps the D5 half-spin chiralities, so the substrate cannot intrinsically choose one physical chirality.

## Pass 5620 — the E6 36/9 firewall is horizontal versus vertical

Pass5618 killed total Z3 charge as the selector: all 45 E6 cubics are neutral. The already-derived principal-Z3 bundle gives the actual invariant.

The 27 vertices project to the nine points of `AG(2,3)`.

* Each of the 36 allowed cubics projects to **three distinct fibers whose base points form an affine line**, with exactly one lifted point in each fiber and an affine lift law `t_i=k+i lambda`.
* Each of the nine firewall cubics projects to **one base point** and consists of the entire vertical Z3 fiber.

Therefore

\[
\boxed{\text{allowed36 = horizontal/covariantly affine lifts},\qquad
       \text{bad9 = vertical kernel fibers}.}
\]

The distinction survives arbitrary independent translations of the fiber coordinate, because the projection and its cardinality are gauge invariant. This is an exact mathematical firewall selector. A physical Yukawa theory would still need to show that vertical gauge fibers are redundant/gauge rather than interaction vertices.

## Pass 5621 — hierarchical composition produces a continuum, but not spacetime

Increasing `q` alone leaves the magnetic bulk atomic (Pass5611). Genuine finite repo covers such as selected135 -> 270 and the 810 -> 1620 apartment cover split spectra, but do not by themselves form a proven infinite spatial refinement tower.

A different hierarchy is exact. For the deck-odd magnetic cell,

\[
\mathbb P(X=\pm3)=\mathbb P(X=\pm6)=\frac14,
\qquad
\phi_X(t)=\frac12(\cos3t+\cos6t),
\]

with

\[
\sigma^2=\frac{45}{2},\qquad \gamma_2=-\frac{41}{25}.
\]

For the N-cell tensor-sum `H_N`,

\[
\frac{H_N}{\sqrt{(45/2)N}}
\Longrightarrow \mathcal N(0,1),
\qquad
\gamma_2(N)=-\frac{41}{25N}.
\]

Thus a continuous spectral density can emerge from many W33 magnetic cells without changing field order. It is a many-body/configuration-space central-limit continuum with exponential degeneracy, **not** a Weyl eigenvalue-counting law for 3+1-dimensional spacetime.

## Pass 5622 — particle-hole symmetry conditionally removes the additive mass

On the deck-odd sector the matrix is purely imaginary Hermitian, so ordinary complex conjugation obeys

\[
K H_- K^{-1}=-H_-,\qquad K^2=1.
\]

For

\[
M=m_0I+gH_-,
\]

requiring the same antiunitary symmetry,

\[
K M K^{-1}=-M,
\]

forces

\[
\boxed{m_0=0}.
\]

The exact Dirac dispersion then has two absolute internal levels,

\[
3|g|,\qquad6|g|,
\]

and therefore the scale-free ratio

\[
\boxed{m_{\rm heavy}/m_{\rm light}=2}.
\]

This is conditional on selecting the deck-odd sector and its antiunitary symmetry as physical. The overall dimensionful scale `|g|` is not fixed: dimensionless finite incidence data do not provide an SI clock, length, energy, or action normalization.

## Pass 5623 — the q=5 fixed point is a global singlet direction, not a proved vacuum

The selected 13-cover belongs to the q=5 `NO_5^+(5)` branch. Its stabilizer image has orbits `1+12`. The associated design is

\[
2-(13,6,60),\qquad b=312,\qquad r=144.
\]

Every point lies on 144 blocks and every pair lies on 60 blocks. Hence the fixed point is **not locally distinguished** by the balanced design.

Globally, a `1+12` action on the centered 13-point simplex has exactly one invariant line, represented by

\[
12e_{\rm fixed}-\sum_{i\in\rm moving}e_i.
\]

This is a genuine symmetry-breaking singlet/order-parameter direction. Calling it a physical vacuum is unjustified: it is a q=5 object and no action-level bridge maps it to the q=3 W33 physical substrate. The moving-12-to-F4 dictionary remains gated on the direct GAP S12 conjugator.

## Pass 5624 — exact causal cube, emergent Dirac cone, and the speed-of-light firewall

The Pass4067 split-step walk applies one conditional nearest-neighbor shift in each spatial coordinate per macrostep. With spatial lattice spacing `ell`,

\[
|\Delta x_j|\le\ell,
\qquad
|\Delta x|_2\le\sqrt3\,\ell.
\]

At long wavelength,

\[
\frac{U_a-I}{-ia}\to m\beta+\sum_jp_j\alpha_j,
\]

so

\[
E^2=p^2+m^2,
\qquad |v_g|\le1
\]

in natural lattice units. At finite step the product formula splits the spin branches and equal-|p| directions can have different quasienergies; the relativistic cone is a continuum-limit statement.

Physical `c` is a conversion such as `ell/tau` between a lattice spacing and a macrostep time. The graph supplies causality; node counts do **not** determine `299792458 m/s` without a physical clock/length calibration.

## Pass 5625 — exact finite eta phase diagram replaces a quarantined anomaly story

The legacy `tests/test_anomaly_polynomial.py` is explicitly skipped under the Pass1150 shifted-adjacency retraction and is not reused.

For the intrinsic 32-state lift, `M(r)=rI+H_mag` has spectral-flow walls

\[
r\in\{-9,-6,-3,-2,1,3,6\}.
\]

The eta values in the eight open chambers are

\[
-32,-30,-22,-12,0,6,20,32.
\]

Hence the full lift has a robust balanced chamber

\[
\boxed{-2<r<1}. 
\]

The deck-odd sector has walls `-6,-3,3,6` and a symmetric balanced chamber `-3<r<3`.

These are exact finite spectral-asymmetry/spectral-flow statements. They are not a continuum APS theorem and do not establish gauge-anomaly cancellation.

## Pass 5626 — deck parity is an exact superselection label

Compression of each `+/-` fiber gives

* for symplectic exponent `B=0`: even weight `2`, odd weight `0`;
* for `B != 0`: even weight `-1`, odd weight `+/- i sqrt(3)`.

There are 12 zero-symplectic rook-complement edges and 60 nonzero ones. Thus

\[
H_+\text{ is real and }KH_+K^{-1}=H_+,
\]

whereas

\[
H_-\text{ is purely imaginary and }KH_-K^{-1}=-H_-.
\]

The odd block satisfies

\[
(H_-^2-9I)(H_-^2-36I)=0.
\]

Every observable commuting with deck reversal is block diagonal on `16_+ + 16_-`; mixing the sectors requires a deck-odd/frame-reversal-breaking perturbation. The exact statement is therefore a **frame-neutral versus frame-sensitive Z2 superselection split**, not a proved vacuum/matter or boson/fermion decomposition.

## External boundary

Finite-field Weil representations are classical objects; this packet does not claim their invention. Causal discrete Dirac quantum walks and their continuum convergence are likewise established. The new repo-level content is the exact composition and falsification work involving the specific W33 vector lift, E6 Z3 bundle, magnetic spectrum, deck parity, and existing cover layers.

## Evidence boundary

All promoted results are finite algebra, spectrum, bundle, cover, coding, or quantum-walk identities. No physical spin-statistics theorem, Standard Model mass assignment, SI speed of light, continuum gauge anomaly theorem, physical vacuum identification, or spacetime Weyl law is claimed.
