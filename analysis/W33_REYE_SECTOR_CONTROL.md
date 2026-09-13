# From Reye sectors to a controllable three-qubit register

The certified Reye Pauli carrier now has an executable control model. Its twelve
Hamiltonians alone generate four independently addressed qubit rotations. Exactly
three additional **individual Pauli Hamiltonians** suffice, and are necessary,
for full operator control of this eight-dimensional register. This is a concrete
extension of the existing geometry, not a new general controllability theorem.

## The actual register and instructions

Import the carrier from `data/w33_e7_d4_presymplectic_reye_normal_form.json`:

    {X,Y,Z}_1 × {I,Z}_2 × {I,X}_3.

Assume every listed Hamiltonian can be switched independently for arbitrary signed
angles, with no drift or noise. The base associative algebra is
`M2(C) tensor C^4`; the dynamical Lie algebra is `su(2)^4`, dimension 12.
The four sector projectors are

    Q(s,t) = (I+s Z2)(I+t X3)/4, s,t in {-1,+1}.

Each has rank two. They sum to identity and are pairwise orthogonal. Their labels
are joint eigenvalues, not the radical offsets of a classical incidence point.
Coherent superpositions between sectors remain possible; the base controls cannot
change the sector populations. No physical hidden-variable interpretation follows.

`SELROT(axis,s,t,theta)` implements `exp(-i theta axis_1 Q(s,t))` using four
commuting pulses, at angles `theta/4, s theta/4, t theta/4, st theta/4` on
`axisII, axisZI, axisIX, axisZX`. This operates coherently on the complete register
while leaving the other three sectors unchanged. The script verifies all twelve
axis-sector cases against their full eight-by-eight matrices.

## Two controls remove the commuting symmetry but still fall short

Add `IXI` and then `IIZ`. The Lie dimensions progress

    12 -> 20 -> 36.

After both additions, the entire complex commutant is scalar. Nevertheless, all
36 generated Hermitian directions satisfy

    P^T J + J P = 0, J = YZX, J^T = -J.

Their skew-Hermitian multiples therefore generate precisely the compact
symplectic algebra `sp(4)` acting on `C^8`, rather than `su(8)`. The checker
constructs every one of the 36 directions and verifies the skew-form equation.
This is an explicit instance of the standard distinction between irreducibility
and full operator controllability, explained by
[Zeier and Schulte-Herbrueggen](https://arxiv.org/abs/1012.5256).

Adding `IZI` breaks that form constraint and generates all 63 nonidentity Pauli
directions: `su(8)`. The final controls are all single-qubit additions. The base
carrier already contains multi-qubit interactions; they are part of the assumed
control resources, not something supplied free by the added controls.

## Minimality and executable synthesis

There are 51 nonidentity Pauli words outside the base. Exhaustive closure of all
1,275 distinct pairs of additions gives:

| Lie dimension | Number of pairs |
|---|---:|
| 14 | 3 |
| 20 | 168 |
| 21 | 48 |
| 30 | 288 |
| 36 | 768 |

None reaches 63. Single additions also fail, and the displayed triple succeeds.
This proves minimality **within additional individual Pauli controls**, not among
arbitrary Hamiltonian linear combinations or ancilla-assisted schemes.

The certificate stores a topologically ordered commutator derivation for every
generated direction. The compiler converts it into actual pulse lists using

    R_A(pi/4) P_B R_A(-pi/4) = -i P_A P_B = sign P_C

for anticommuting Pauli words. Recursive conjugation gives a finite sequence for
`R_C(theta)`. All 63 rotations were checked at `theta=pi/7` on complete matrices;
the algebraic identity establishes arbitrary-angle correctness. Maximum numerical
matrix error was below `4e-16`. Matrix multiplication order is the pulse-list
product order; a chronological hardware executor must apply the rightmost pulse
first. No pulse-count or time optimality is asserted.

The audit independently checks every Pauli bracket using dense matrices with
Gaussian-integer entries, and repeats the control-rank calculation after a
Hadamard change of basis on qubit three. Constructive gate decompositions are
established prior art; see [Khaneja and Glaser](https://arxiv.org/abs/quant-ph/0010100).

Run:

    OPENBLAS_NUM_THREADS=1 python3 analysis/w33_reye_sector_control.py

Add `--write` to regenerate the adjacent JSON. The normal-form certificate is
required and its actual selected words are compared, rather than trusting its
status alone. The result is a finite register and ideal control compiler. It does
not establish a scalable universal machine, physical pulse availability, timing,
error correction, fault tolerance, or energy advantage.

## Change intake and cross-repository connections

`W33_SEPT12_CHANGE_INTAKE.json` records 21 W33 commits (`51e1ecb02..4292575fa`)
and 22 Holotrade commits (`6a49550..361b51e`), covering 49 net changed paths.
The complete net diffs were read. Every per-commit patch was retrieved through
GitKraken and its changed lines compared against that read material; the remaining
intermediate workflow continuation edits were inspected separately. This bounded
review does not complete the earlier history and recursively included manuscript
reading backlog. The three top-level manuscript files are wrappers, which were
read and traced to their bodies and shared inserts.

Existing parallel results own the hidden V4 decoder, affine group of order 576,
Schur image of order 288, non-elementary cross-fibre kernel, and observer-relative
min-entropy. This work cites their carrier and adds continuous control semantics.
Searches covered result strings, Pauli/skew-form expressions, RESULTS_INDEX,
Python/JSON/Markdown/TeX/HTML, both repositories, and primary literature. No claim
of worldwide novelty or exhaustive semantic indexing is made.

Holotrade's minimized 1,080-move circuit library, mass-40 depth-five structural
certificates, explicit Gram embedding and provenance synthesis remain prior work.
Its zero-dependency five-frontier cross-certificate validator passes locally.
That validates agreement between frozen certificates; it does not rerun their
large searches or prove an attested worker actually executed the claimed vectors.
The deterministic provenance example uses simulated signed verifier verdicts and
placeholder execution digests. It establishes software binding behavior, not a
real measured-boot event. Connecting the existing solver-free dual receipts to
that execution boundary remains a useful independent implementation target.

A further intake detail: the new Schur 288 action certificate already corrects
the earlier order-576 identification. Its earlier affine-decoder certificate still
contains historical alignment wording; the later correction governs interpretation.
The quotient-grid file also retains its earlier proposed uniform-fibre target,
while the later fibre calculation rules out that particular kernel identification.
These are recorded as historical frontier transitions, not silently treated as
simultaneously live conjectures.

## Validation outcome

All eight new parallel W33 regression scripts passed via their standalone
entrypoints, covering the normal form, radical decoder, observer entropy,
affine symmetry, quotient grid, fibres, two-sheet obstruction and order-288
bridge. Two pytest collection attempts were interrupted before running tests
because directory scanning was slow on this checkout; direct entrypoints execute
the same test functions without that collection overhead. The new control audit,
Holotrade cross-certificate validator, workflow parse and rediscovery check pass.
The refreshed index contains 9,862 files and 13,958 distinctive results. Full
repository CI, remote CI and a complete LaTeX build were not verified here.
