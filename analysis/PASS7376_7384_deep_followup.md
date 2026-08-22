# Passes 7376–7384 — deep followup: logical Hodge split, curvature transgression, q=9 quotient, phase pole, and E8 local chain

This packet executes the five non-sequential attacks left by Pass7373–7375 and adds three deliberately outside-the-box probes. The governing rule is the same evidence firewall used elsewhere in the current frontier: exact finite identities are promoted; solver timeouts, representation analogies, and physical interpretations are not.

## 1. The 17-qutrit logical space is a genuine Hodge-like 7+10 split

Let

- `N : Z^36 -> Z^45` be the double-six/doily-slice incidence matrix,
- `R : Z^45 -> Z^27` be the tritangent/cubic-line incidence matrix,
- `Q=(RN)/3`.

Pass7364–7366 proved the exact integral curvature identity

\[
RN=3Q.
\]

Modulo three, therefore,

\[
\mathbb F_3^{36}\xrightarrow{N}\mathbb F_3^{45}\xrightarrow{R}\mathbb F_3^{27}
\]

is a chain complex with

\[
(\dim H_2,\dim H_1,\dim H_0)=(22,10,6).
\]

For the self-orthogonal ternary code `C3=im(N)=[45,14,15]_3`, Pass7373–7375 gave the abstract CSS code

\[
[[45,17,5]]_3.
\]

The present pass now identifies its two logical sectors canonically:

\[
\boxed{\mathcal L_{17}=\frac{\operatorname{im}R^T}{\operatorname{im}N}
\;\perp\;
\frac{\ker R}{\operatorname{im}N}.}
\]

The first quotient has dimension seven. Its projective minimum logical supports are exactly the 27 cubic-line stars, each of weight five. This is the already identified `T7=1|5|1` modular `W(E6)` sector.

The second quotient is literally

\[
\boxed{H_1=\ker R/\operatorname{im}N}
\]

of dimension ten. An exact meet-in-the-middle dependency search proves that `ker(R)` contains no full-support ternary dependency on fewer than six tritangent columns. At weight six there are exactly the 120 induced Steiner `K_{3,3}` supports, each carrying a one-dimensional full-support ternary relation. Hence the two pure logical sectors have different distances:

\[
\boxed{d_{\rm star}=5,\qquad d_{H_1}=6.}
\]

This sharpens the earlier module decomposition: the ten-dimensional absolutely irreducible sector is not merely isomorphic to a homology module; it is the first homology of the integral-prism reduction itself.

## 2. The 270 binary tetrads have a concrete cubic-surface meaning

The binary reduction of `Q^T` is the previously found

\[
[27,7,11]_2
\]

Schlaefli code. Its dual minimum weight is four, with exactly 270 tetrads.

The present pass classifies all 270 supports. Every tetrad induces

\[
\boxed{2K_2}
\]

in the 27-line meet graph: two meeting pairs with no cross incidences.

Even better, there is an exact objectwise bijection. There are 270 pairs of tritangent planes that share one cubic line. If `T1,T2` share the line `ell`, remove `ell` from their union. The remaining four lines form one of the binary dual tetrads, and every tetrad appears exactly once this way.

The resulting 4-subset system is an association design rather than a 2-design:

- each of the 135 meeting line pairs lies in exactly four tetrads;
- each of the 216 skew line pairs lies in exactly five tetrads.

Thus the 2-primary shadow of the integral `27-45-36` prism remembers the two natural relations of the Schlaefli geometry.

## 3. The q=9 involution gives an exact 380-variable symmetry branch

A parallel q=9 lane independently proved that the frozen 51-set has exact projective symplectic stabilizer `C2`. Pass7337–7352 had already produced an explicit symplectic lift `A` with `A^2=-I`.

The projective action has

\[
20\text{ fixed points}+400\text{ two-cycles}=420\text{ point orbits}.
\]

Forty two-cycles contain a collinear point pair, so they can never be selected by an `A`-invariant partial ovoid. The exact invariant branch therefore has only

\[
\boxed{380}
\]

orbit variables: 360 admissible two-cycles and 20 fixed points.

Using all 820 isotropic-line clique inequalities, the weighted quotient LP optimum is

\[
\boxed{74}.
\]

Conditioning on fixed-point count gives

\[
0\mapsto72,\qquad1\mapsto73,\qquad2\mapsto74.
\]

The frozen 51-set descends exactly to one fixed point plus 25 two-cycles. Since an invariant 52-set has even size, and the fixed locus is two isotropic ten-point lines, only fixed counts zero or two can occur in the invariant target-52 branch.

This does **not** make the symmetry WLOG: an unrestricted 52-set could be asymmetric. The result is an exact branch-and-cut reduction for the unique symmetry class naturally attached to the incumbent, not an upper bound for `alpha(W(3,9))`.

## 4. Coxeter phase selects a phase pole; the flat 12-set is its local chart

Pass7370–7372 found 12 phase-flat orthogonal `D4+D4` coordinates, inducing `3K4` in the 45-coordinate `SRG(45,12,3,3)`.

The new replay proves something stronger and conceptually simpler:

\[
\boxed{\{\text{12 phase-flat coordinates}\}=N(p)}
\]

for one unique coordinate `p` in the deterministic Coxeter-phase gauge.

Moreover every local graph of `SRG(45,12,3,3)` is `3K4`. The special feature is therefore not a new graph isomorphism type. The Coxeter phase picks one particular local chart — a distinguished **phase pole** — out of the 45 equivalent local charts.

This also prevents an attractive but false shortcut. The older BT660 `4K4` lives on a different 16-flag Levi carrier and requires a secondary product-codec relation to lift to `Q4`. The new `3K4` has 12 coordinates and is the local graph of the 45-tritangent carrier. No 12-to-16 identification is promoted without an explicit map.

## 5. `RN=3Q` induces a rank-seven curvature transgression

Because `RN=3Q`, every `z in ker(N mod 3)` has a well-defined curvature image

\[
\kappa(z)=Qz\pmod3.
\]

On the 22-dimensional `H2=ker(N mod3)` this map has

\[
\boxed{\operatorname{rank}\kappa=7,\qquad\dim\ker\kappa=15.}
\]

Its image is exactly

\[
\boxed{\operatorname{im}(RR^T)},
\]

also of dimension seven. Since `R` restricted to `im(R^T)` has kernel exactly `im(N)`,

\[
\operatorname{im}(R^T)/\operatorname{im}(N)\cong\operatorname{im}(RR^T).
\]

Therefore the integral curvature induces a canonical secondary map from the 22-dimensional two-cycle space onto the same seven-dimensional logical star sector identified above.

The terminology matters. This is **Bockstein-like**, but it is not presently a standard Bockstein homomorphism: `RN` is not zero integrally, so we do not start from an ordinary integral chain complex. A February 2026 result by Junichi Haruna (`arXiv:2602.14499`) proves that genuine Bockstein maps can characterize refinement of transversal diagonal gates for CSS codes. That makes construction of a true integral lift whose Bockstein realizes (or fails to realize) this rank-seven transgression a high-value next theorem, but it does not license renaming the present map.

## Outside-box A. Repairing the new E8 spectral descent reveals Clebsch and Petersen

A same-day parallel commit computed the nested local spectra

\[
240\to56\to27\to16\to10
\]

inside the positive-inner-product E8 root graph, but then promoted `27+6=33` as a W33 vertex count. The spectral computation is useful; that final interpretation is not.

The exact replay keeps the mathematics and repairs the carrier:

1. the Coxeter/Eisenstein construction partitions the 240 E8 roots into **40 six-root fibres**;
2. every fibre has real rank two and is literally an `A2` root hexagon;
3. the quotient is the already certified W33 **point** graph `SRG(40,12,2,4)`;
4. the 16-vertex local graph is the **complement of the Clebsch graph**;
5. the 10-vertex next local graph is the **complement of the Petersen graph**.

Thus the correct nested picture is not `33=W33`. W33 remains the 40-fibre Eisenstein quotient established at Pass1021.

There is nevertheless an intriguing representation-theoretic shadow at the Schlaefli level. Choosing one of 27 vertices partitions the set as

\[
\boxed{27=1+16+10},
\]

the same dimensions appearing in the standard `E6 -> Spin(10)` branching of the 27. This is recorded as structural context only; no particle assignment is inferred.

The uploaded `e8_eisenstein_w33_results.json` independently reports the same local spectra and the existence of 40 six-root Eisenstein lines. The attachment is truncated before completing its `w33_descent` object, so only the visible fields are used as evidence; they are also independently regenerated here.

## Outside-box B. The Eisenstein fibre is literally `A2`

Pass1021 identified the fibre group as the six Eisenstein units `<-1,omega> ~= Z6`. The new exact root calculation adds a root-system interpretation:

- each fibre consists of six E8 roots;
- its span has rank two;
- among its 15 unordered root pairs the doubled-coordinate inner products are `+4^6,-4^6,-8^3`.

That is exactly a six-root `A2` hexagon with three antipodal pairs.

So the established map can now be written schematically as

\[
\boxed{E_8\text{ roots }240 = 40\times A_2\text{-hexagon}(6)}.
\]

This is a finite root-fibration statement. It does not mean physical spacetime contains 40 independent `A2` gauge factors.

## Outside-box C. The qutrit code fails naive ternary triorthogonality

The new `C3=[45,14,15]_3` code is self-orthogonal and its deterministic basis rows all have weights divisible by three. That is not enough for a transversal non-Clifford theorem.

The cubic overlap form

\[
T(u,v,w)=\sum_i u_i v_i w_i\pmod3
\]

was evaluated on all basis triples with repetition. It is nonzero on 275 triples. Hence the trilinear form itself is nonzero on `C3`:

\[
\boxed{T\not\equiv0.}
\]

So a direct ternary analogue of total binary triorthogonality fails. No transversal non-Clifford gate claim follows from the current code.

This firewall is timely. Recent 2026 triorthogonal-code work continues to emphasize simultaneous pairwise and triple-overlap constraints for transversal non-Clifford gates in the binary setting (`arXiv:2605.24519`), while current CSS-gate work increasingly formulates more general conditions homologically (`arXiv:2602.14499`, `2601.21514`). Our correct next target is therefore the actual homological refinement problem, not retrofitting the code to a failed overlap criterion.

## Same-day parallel-commit audit

The substantive parallel work today was read as a set of mathematical lanes rather than treating reservation/merge/publication commits as independent discoveries.

### q=7/q=9 extremal partial ovoids

The strongest parallel result independently closes the stabilizer question: after several self-caught implementation bugs, the q=7 optimum and the frozen q=9 51-set both have exact projective symplectic stabilizer `C2`. That independently validates the symmetry used in the present q=9 quotient.

The same lane calibrates large-neighborhood search on known q=7 and `Q^-(5,4)` optima, extends the certified q=9 basin, and explicitly keeps

\[
51\le\alpha(W(3,9))\le73
\]

open. This matches the evidence boundary here.

### Pauli interpretation

Another parallel pass gives the controlled finite dictionary: points of `W(3,q)` are projective two-qudit Pauli classes, collinearity means commuting, and a partial ovoid is therefore a pairwise noncommuting Pauli family. The small stabilizer means the q>=7 incumbent families are Clifford-rigid. This is useful quantum-information language for the q=9 extremal problem, but it does not turn an unknown maximum into a physical law.

### E8 spectral descent

The new E8 spectral script successfully reproduces the E8/E7/Schlaefli local spectra. Its `33=W33 vertex count` interpretation is rejected. The repository already has a stronger objectwise theorem, Pass1021, proving a 6:1 E8-root fibration onto **40 W33 points**. The present Clebsch/Petersen replay preserves the good spectral content while putting it back on that established carrier.

### General finite-field constructor

The parallel `Q^-(5,q)` lane usefully validates the LNS transfer to a different generalized quadrangle. Its earlier claim of a general `GF(p^k)` constructor had a degree>=4 irreducibility boundary issue caught elsewhere in today's repo history. The degree-two/three fields used in the verified q=4,9,25,27 examples remain within the safe regime; the broader constructor claim should continue to use the later irreducibility repair.

## Literature connections and limits

- **Haruna 2026, arXiv:2602.14499**: a genuine Bockstein homomorphism characterizes a transversal diagonal-gate refinement problem for CSS codes. This motivates, but does not identify, the present curvature transgression.
- **Baldelli et al. 2026, arXiv:2605.24519**: recent triorthogonal-code constructions again require simultaneous pairwise/triple overlap conditions. Our ternary cubic form fails the naive analogue, which is why no transversal-gate theorem is claimed.
- **Camps-Moreno et al. 2026, arXiv:2601.21514**: provides a broader algebraic program for determining diagonal transversal gates of CSS codes. This is a natural external benchmark for the new `[[45,17,5]]_3` code.
- The standard `E6 -> SO(10)` context places a 16-dimensional spinor and a 10-dimensional vector inside the 27. The E8 local graph partition `27=1+16+10` is therefore structurally suggestive, but no Standard Model assignment is inferred from a graph-neighborhood decomposition.

## Evidence boundary

Promoted here:

- exact finite incidence identities;
- exact binary/ternary code parameters and minimum-support classifications;
- exact finite-group symmetry reductions;
- exact linear-program relaxation values;
- exact E8 root/local-graph identifications.

Still open:

- `alpha(W(3,9))` and target 52 in the unrestricted problem;
- whether the curvature transgression is realizable as a standard Bockstein of a natural integral lift;
- any transversal non-Clifford gate for `[[45,17,5]]_3`;
- any particle-physics interpretation of the E6/E8 branching dimensions;
- any identification of the new 12-coordinate `3K4` chart with the older 16-flag `4K4` codec.
