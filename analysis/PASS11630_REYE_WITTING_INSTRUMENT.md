# Pass11630: the Reye projective map becomes a heralded quantum instrument

Reservation151929231. Input: the user's19 files in Desktop/Perplexity, read
as research evidence rather than instructions. The supplied Perplexity work
owns the explicit embedding and the relative extension search. This packet
audits those results and adds a channel construction with named operators.

## Intake and prior ownership

All supplied prose, Python and PDF pages were read. Every JSON, CSV and NPZ
is inspected by the independent producer. Original bytes are preserved in
`data/w33_pass11630_perplexity_input.zip`,826497 bytes, SHA256
`0e85aef7030468d45048aa14d59fed7c1b2fb5e64ed40d53ef8dc0d7f4bb8659`.
Its manifest checks19 individual file hashes before interpretation.

The complete batch guard reports **HARD FAIL** because
`witting_experiment_results.json` ends at147 bytes. That file is quarantined,
not promoted to a result certificate. Guard collisions and forced arithmetic
were absent. Both supplied Python scripts were subsequently executed as fresh
processes in an isolated output directory. The first also imports **pandas**,
missing from its stated dependency list. Its regenerated result JSON is valid;
the MILP found the supplied12-point set. A different correspondence returned
determinant−2/3 rather than2/3: determinant sign depends on the chosen map and
correspondence, so this is not an invariant contradiction. The follow-up replay
matches the supplied discrete results, with only roundoff-scale changes in
three floating residuals/condition numbers.

Prior repo ownership matters:

- Pass4963 already proves the Witting graph is the W33 **point** graph and
  tabulates all3240 exact Bargmann phases; Pass4966 owns the outer phase sign.
- Pass8909–8916 already selects a complementary D4/Reye-type subsystem in E8.
- BT544's combinatorial Reye overlay on local MUB labels is distinct from this
  actual projective embedding into the90 Witting lines.
- Passes11625–11629 already build the Peres controls, the12-Higgs-ray Witting
  neighborhood, and the conditional coherent-query/Toffoli resource boundary.
- The rediscovery guard's D4/Witting candidates,
  `BT1601_BT1603_physical_fano_universal_closure.md`,
  `BT1602_fano_witting_detector_bin_synthesis.md` and
  `BT1697_holonet_typed_packet_abi.md`, describe detector/packet interfaces and
  separately supplied magic rails. They do not implement this Reye Kraus map.
- `BT1893_BT1895_summary.md` distinguishes the finite transaction verifier and
  ideal demonstrator from the fault-tolerant stack and an open continuum lift.
  Those architecture checks do not supply the quantum instrument constructed here.

[Waegell–Aravind1701.06512](https://arxiv.org/abs/1701.06512) establishes the
Penrose/Witting equivalence and distinguishes complex Witting contextuality
from real E8 parity proofs. [Waegell–Aravind1103.6058](https://arxiv.org/abs/1103.6058)
describes the paired24-cell Peres construction. [Vlasov2208.13644v2](https://arxiv.org/html/2208.13644v2)
supplies the Witting coordinates,90 complex lines and measurement circuits.
These are prior results, not new theorems of this packet.

## Exact primal and contragredient maps

Let L be the supplied4×4 projective matrix, and define

\[
J=\begin{pmatrix}0&0&-1&0\\0&0&0&-1\\1&0&0&0\\0&1&0&0\end{pmatrix},
\qquad c=1/\sqrt3.
\]

The exact pullback is

\[
L^\dagger L=I+icJ,\qquad J^T=-J,\qquad J^2=-I.
\]

It is not proportional to a unitary metric. Nevertheless its real part is I:
the map embeds real R4 isometrically into real R8, with constant slant angle
cosine1/√3. For real r,s, complex orthogonality requires **both**
r·s=0 and rᵀJs=0. This explains precisely why six of the18 real internal
orthogonal pairs disappear while12 survive. Real projective lines survive;
orthogonal measurement contexts need not.

The dual12 rays require **L⁻†**, not L. Applying L to the second real24-cell
has maximum target squared overlap2/3, not1. The exact normalized dual map is

\[
L_-=\sqrt{2/3}\,L^{-\dagger},\qquad L_-^\dagger L_-=I-icJ,
\qquad L^\dagger L_-=\sqrt{2/3}\,I.
\]

Thus cross-cell orthogonality is preserved by the contragredient pairing.
All144 projective minors for the two maps vanish exactly. The24 combined
normalized image projectors sum to6I. This tight frame is still KS-colorable.
The source's Reye incidence bridge does not transport the Peres proof intact.

The standard geometric meaning of a slant plane is a constant angle between
its tangent plane and its image under the ambient complex structure; see
[Chen's definition](https://www.i-repository.net/contents/osakacu/sugaku/111F0000002-03901-3.pdf).
No novel definition of geometry is needed here.

## A complete operation, its optimal success, and its failure carrier

Put S=iJ=Y⊗I, P±=(I±S)/2, r=2−√3 and

\[
p=\frac1{1+c}=\frac{3-\sqrt3}{2}.
\]

An explicit two-outcome instrument is

\[
K_+=\frac{L}{\sqrt{1+c}},\qquad
F_+=\sqrt{1-r}\,P_-,\qquad K_+^\dagger K_++F_+^\dagger F_+=I.
\]

Every normalized real input has success probability p. Failure has a fixed
two-dimensional complex carrier; all24 real Peres input rays project there
to six Pauli qubit rays, each four times. The six lost internal orthogonal
pairs collapse to identical failure rays. This is a trace-preserving instrument
when both outcomes are retained, not renormalized loss masquerading as a channel.

The producer exports an actual8×8 unitary, not only an existence assertion.
With U the polar unitary of L, D=P++√rP− and E=√(1−r)P−, it is

\[
\mathcal U=\begin{pmatrix}UD&-UE\\E&D\end{pmatrix}.
\]

Five real rays already fix the map: the four coordinate rays imply any Kraus
operator with the prescribed pure outputs is L diag(a0,a1,a2,a3); one half-vector
with all nonzero coordinates forces all ai equal. The homogeneous projective
constraint matrix has exact rank15. Hence every success Kraus operator is ajL,
and trace nonincrease implies Σ|aj|²≤p. The displayed operation saturates
the bound even among multi-Kraus success operations with those same pure targets.
A deterministic CPTP operation mapping those five inputs to the prescribed pure
outputs is impossible because L†L is not scalar. This argument is stronger than
merely noticing that L is not unitary.

## Complementary maps give a weak-Pauli channel

The second branch can use the same U:

\[
K_-=U(\sqrt r P_++P_-),\qquad F_-=\sqrt{1-r}P_+.
\]

Choosing + or− uniformly gives

\[
\frac12(K_+^\dagger K_++K_-^\dagger K_-)=pI
\]

for **every complex input**. Conditional on success, forgetting the choice
gives the exact channel

\[
\mathcal E(\rho)=U\left[
\frac{1+\eta}{2}\rho+\frac{1-\eta}{2}S\rho S\right]U^\dagger,
\qquad \eta=\sqrt{2/3}.
\]

All16 matrix units are checked exactly. Retaining the choice gives the
corresponding binary Lüders weak-Pauli measurement with effects(I±cS)/2,
followed by U. Weak-measurement decompositions themselves are standard:
[Oreshkov–Brun](https://arxiv.org/abs/quant-ph/0503017). Their universality
for generalized **measurements** is not automatically computational universality.

## A concrete conditional magic-state route

Prepare the stabilizer state |++>. K+ success maps it to Witting ray4,
(0,1,−1,1)/√3 up to phase. Measure X on the first qubit and keep the+ outcome.
The remaining qubit is

\[
|m\rangle=\frac{(-1,2)}{\sqrt5},\qquad
\mathbf b=(-4/5,0,-3/5).
\]

The readout succeeds with probability5/6, so the complete preparation succeeds
with probability5(3−√3)/12 per independent attempt. Its Bloch l1 norm7/5
exceeds the stabilizer octahedron bound1. Repeated ideal preparation plus
stabilizer operations therefore meets the known pure-state sufficient condition
for quantum universality: [Reichardt0411036](https://arxiv.org/abs/quant-ph/0411036).

For IID depolarization **after successful preparation**, a further explicit
stabilizer construction closes the threshold. Conjugate by Y and twirl by
choosing I or H uniformly. The Bloch vector becomes (7v/10,0,7v/10).
The producer builds the Steane logical projection from its eight classical
codewords, independently deriving the known decoder of
[Reichardt, Section II](https://arxiv.org/html/quant-ph/0411036v1):

\[
x'=\frac{x^3(7+8x^4)}{1+14x^4},\qquad
p_{\rm accept}=\frac{1+14x^4}{64},\qquad x_0=7v/10.
\]

The exact gain factors as
\[
x'-x=\frac{x(1-x^2)(4x^2-1)(1-2x^2)}{1+14x^4}>0
\quad(1/2<x<1/\sqrt2).
\]
Iteration therefore converges to the Hadamard magic state for **v>5/7**.
At v≤5/7, the Y-rotated input is explicitly the stabilizer mixture
(4v/5)|+X><+X|+(3v/5)|+Z><+Z|+(1−7v/5)I/2.
This is a tight threshold for this noise family with **perfect stabilizer
control**, not merely an outside-polytope witness. The decoder and threshold
theory are published prior art; the application to this specified preparation
is the added connection. Acceptance is costly, especially near threshold.
No noisy-K analysis, correlated-error guarantee, native Hamiltonian or physical
realization of K is supplied. The extra operation is doing the computational
work; incidence alone does not supply it.

## Independent replay of the supporting witnesses

- All25920 group permutations are regenerated from eight **exact** Eisenstein
  triflection permutations and compared to the supplied NPZ set. The given
  Reye orbit is540, stabilizer48; its unordered paired orbit270, stabilizer96.
  These classify the supplied orbit, not every conceivable embedding.
- The39-edge spanning-tree gauge and all501 triangle updates replay in exact
  Q(ω,√3), checking every recovered oriented Gram entry. This supplies constructive
  labeled rigidity; mod-two homology alone would not prove phase uniqueness.
- Exhaustion of14893 candidate extensions of the fixed24-ray union reproduces
  minimum6 and48 minimum extensions. The29-ray/14-tetrad witness has132 orthogonal
  edges and all29 deletion colorings are verified. The tetrad-only problem has
  an explicit coloring: pair exclusivity is essential. No global KS minimum claim.
- Supplied rays, projectors, all15 operator generators,225 commutators,2730
  nonzero CSV structure constants, triple-product array, local Clifford matcher,
  embedding data and basis/SIC tables are checked. Floating matrix-array checks
  retain explicit tolerances; exact phase and channel checks use no tolerances.

Validation is recorded in the publication receipt after the producer and eleven
independent regressions complete. This is finite geometry and an engineered
quantum operation; it does not determine observed masses, mixing, couplings,
gravity or the cosmological constant, and it is not a complete TOE.
