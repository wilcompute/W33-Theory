# Exact rational chiral clock, gauge flux, and three-qutrit magic

2026-11-13. Status: exact finite-dimensional theorem, with physical interpretation open.

## Prior art inside this repository

The 27-event Sym2(F3) null graph, its 108 edges and four eigenvalues appear in analysis/w33_20260924_null_history_spectral_clock.py. The four positive and four negative null directions, 36 oriented triangles, and the history-cycle character appear in analysis/w33_pass11549_history_arrow_cubic_character.py. PASS11548_HISTORY_ORIENTATION_SQUARE_CORRECTION.md distinguishes the actual 24-element projective group from SO(3,3) and corrects the earlier character mistake. PASS20261108_NULL_ORBIT_CHIRALITY.md explicitly identifies complex Hermitian hopping as a direction beyond the real-Hamiltonian no-go.

This pass adds a **particular operator**, its exact rational finite evolution, gauge-loop obstruction, non-Clifford Wigner negativity, and multipartite entanglement. The cone, four clock directions, and symmetry groups themselves are not new.

## The integer clock

Label the histories by S=(a,b,c) in Sym2(F3), with Q(S)=ac-b², and choose the four positive rank-one displacement vectors
\[
N_+=\{(1,0,0),(0,0,1),(1,1,1),(1,2,1)\}.
\]
These sum to zero mod three. Let T send each history to its four positive neighbours; A=T+T^T is the known null adjacency, and D=T-T^T is a signed current.

The certificate proves by integer matrices
\[
D^T=-D,\quad [A,D]=0,\quad D^3=-27D,\qquad
3D^2=-(A-8I)(A-2I)(A+4I).
\]
Fourier characters give spec(D)=0 (multiplicity 19), +3i√3 (multiplicity 4) and -3i√3 (multiplicity 4). The two nonzero modes are exactly the previously known 4+4 null Fourier sheets. The 24 congruence symmetries preserve D; the outer inversion flips D.

Taking H=iD, a **Hermitian** Hamiltonian, the evolution at t*=2π/(3√27) is
\[
U=\exp(t_*D)=I+\frac16D+\frac1{18}D^2,\qquad U^3=I,\quad U^TU=I.
\]
Moreover,
\[
M=9U=(18I+3D+D^2)/2
\]
is an **integer matrix**, with M^T M=81I, M³=729I, trace(M)=135 and every row containing one 5, ten 2's, and sixteen -1's. For every oriented null edge, opposite transition probabilities are exactly 4/81 and 1/81; directional contrast =1/27. The full per-column probability profile is (25/81)^1,(4/81)^10,(1/81)^16.

## Gauge-invariant physical dial

For the complex-Hermitian hopping family Hθ=e^{iθ}T+e^{-iθ}T^T, a directional 3-cycle encloses phase 3θ and the 4-step loop of four distinct positive null vectors encloses phase 4θ. A site-diagonal gauge removing every edge phase must have both e^{3iθ}=1 and e^{4iθ}=1. Their coprime winding lengths force θ=0 modulo 2π. This proves nontrivial graph-gauge flux for every nonzero uniform θ, but does **not** identify it with a measured electromagnetic field.

## Exact odd-prime Wigner witness

For the state U|000> on three qutrits, the Gross discrete-Wigner representation has 729 points and values:

| Wigner value | Count |
|---|---:|
| -1/243 | 432 |
| 2/243 | 270 |
| 5/243 | 27 |

Exact normalization and the pure-state purity identity 27 ΣW²=1 both hold. The total negative Wigner mass is 16/9, the Wigner L1 norm is 41/9, and mana is log(41/9) ≈ 1.516347489. By Gross's finite-dimensional Hudson theorem, this pure output is not a stabilizer state; thus **U is non-Clifford**. Exact rational Schmidt ranks across the three 1-vs-2 qutrit cuts are (3,2,3) for each of the 27 computational-basis inputs. It is an entangling magic-generating gate, not a proof of a universal gate set or fault-tolerant distillation.

## Reproducibility and boundaries

Independent scripts: analysis/toe_20261113_chiral_null_order3_gate.py and analysis/toe_20261113_chiral_null_wigner_magic.py. Regression: tests/test_toe_20261113_chiral_null_clock.py. Machine outputs: data/toe_20261113_chiral_null_order3_gate.json and data/toe_20261113_chiral_null_wigner_magic.json. The full-week/PDF metadata audit is analysis/toe_20261113_week_pdf_audit.py.

External anchors (existing results, not claims of our novelty):
- Gross, finite Hudson theorem: https://doi.org/10.1063/1.2393152
- Veitch et al., resource theory of magic: https://doi.org/10.1088/1367-2630/16/1/013009
- Frigerio et al., gauge Hamiltonians for quantum walks: https://doi.org/10.1103/PhysRevA.104.L030201
- Arnault and Debbasch, discrete gauge walks: https://doi.org/10.1103/PhysRevA.93.052301

Physical caveats: no local optical circuit, calibration data, laboratory device, universal computation guarantee, selected chirality vacuum, thermodynamic arrow, Einstein dynamics, metric continuum, or particle-mass prediction follows from this calculation. A dynamics or action selecting H, a noise budget, and an actual implementation remain open.
