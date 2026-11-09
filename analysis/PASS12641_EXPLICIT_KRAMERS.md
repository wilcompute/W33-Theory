# Pass 12641: the Kramers time reversal as an explicit antiunitary on C⁹ — it carries the doily S6, the chirality pairing and Kramers doublets

Claude track. Script: `analysis/w33_explicit_kramers.py` (`data/w33_explicit_kramers.json`). Builds on Pass 11210 (θ² = parity: the 36 E6 reflections are the Kramers time reversals) and Passes 12636–12640.

**Not a theory of everything.** Explicit finite operators; no dynamics.

## Construction

- **The symplectic data.** The 36 Kramers reversals are the anti-symplectic, fixed-point-free involutions T of F₃⁴, i.e. w(Tx, Ty) = −w(x, y), T² = ±I, with no F₃-eigenvector. Write T = S·K_map, with S ∈ Sp(4,3) (all 51,840 matrices enumerated) and K_map = diag(1, 1, −1, −1). The search finds 72 matrices, i.e. **36 projective θ's**, matching Pass 12523 and Pass 11210.
- **The unitary.** Complex conjugation K maps W_u to W_{K_map u} exactly. The Clifford unitary for S is U|j⟩ = W_{Sx₁}^{j₁} W_{Sx₂}^{j₂} |φ₀⟩, with φ₀ the joint eigenvalue-1 eigenvector of W_{Sz₁} and W_{Sz₂}. The lift is fixed only up to a Pauli factor, and that factor is chosen so that θ = W_c U K has θ² ∝ parity.

## Results (all checks pass)

1. **θ² ∝ parity for all 36** (parity: |j⟩ ↦ |−j⟩). This is Pass 11210's Kramers class, realised as operators on C⁹.
2. **Kramers doublets.** On the 4-dimensional parity −1 sector, a random Hamiltonian symmetrised over θ and parity has spectrum {a, a, b, b}, numerically {−4.957, −4.957, 17.202, 17.202}.
3. **Chirality.** For the θ whose 15 swapped splits form a given pentad's doily (Pass 12639), θ maps that pentad's 45 basis states (up to phases) onto those of pentad 164, **its chiral partner**: same 20 covered points, opposite PSp(4,3)-orbit.
4. **Factor exchange.** (θ⊗θ) S_A (θ⊗θ)⁻¹ = S_B for **all 15** of θ's doily splits. The time reversal exchanges the two tensor factors of exactly the factorisations whose swaps generate the S6 behind the theorem.

**Reading.** One antiunitary operator on two qutrits does all of the following:
- it is a Kramers time reversal (θ² = parity, with doublets in the odd sector);
- it exchanges the two positive-geometry regions over a codeword;
- it exchanges the tensor factors of the 15 factorisations whose swap operators generate the doily S6;
- through that S6's Jucys–Murphy element, it fixes the strong-unextendibility bound 1/9.

## Also recorded

- **d = 25 targeted search** (`w33_ququint_diverse.py`). Random-objective integer programs return 6 distinct size-13 double covers, all with λ_max(R) = 9 against a threshold of 7.4 (δ* = −0.32), and 5 distinct size-14 single covers, all with λ_max(R) = 4 against 3.6 (δ* = −0.16). These minimal uniform covers appear to be single orbit types, and **none certifies**. The pentad mechanism appears special to p = 3, where the doily S6 comes from W(E6) ≅ PGSp(4,3).
- **Three qubits.** Not advanced this round. A symmetry-reduced degree-6 real SOS needs the charge-1 block (Sym²(C⁸)⊗C⁸, dimension 288) and a reshuffled linear map onto Sym³. It is proposed as the next step rather than attempted.
- **Toward a structural proof of Sym²(C⁹) = 9·(5,1).** The other track's sector s = 0 is span{|0,0⟩} ⊕ span{|z,−z⟩ + |−z,z⟩ : z ∈ P¹(F₃)}, i.e. 1 + 4 = 5 dimensions. The doily S6 acts on it with character 3 on a transposition and 2 on a 3-cycle (Pass 12640), so it is (5,1). A computation-free identification of the six letters is still open.

## Addendum: the six letters, the codeword operator, and status

**Six letters** (`w33_six_letters.py`). In the sector s = 0, the vector fixed by the point stabiliser S5, together with its five images under the star transpositions, gives **six vectors forming a regular simplex**: they sum to 0, have unit norm and pairwise overlap −1/5, and S6 permutes them up to sign. This is exactly the standard representation (5,1) as the six letters minus their centroid. They are **not product states**: each reshaped 9×9 matrix has full rank, with singular values 0.516 (×2) and 0.258 (×7). Their distinguished 2-planes are computational-basis pairs {|z⟩, |−z⟩}, which depends on the other track's computational-basis sectors, not on invariant structure. **No basis-independent state interpretation of the letters was found; this remains open.**

**The codeword operator** (`w33_codeword_hamiltonian.py`).
- At first moment, Σ|e⟩⟨e| over any k bases is k·I, which carries no information.
- At second moment, θ⊗θ maps M_L to M_R, and **M_L = M_R exactly**: by the twirl identity, M depends only on the covered point set, which the two chiral pentads share. So spec(M_L + M_R) = 2·{1/9, 16/9}, and the certificate is automatically time-reversal invariant.
- **The theorem's bound is a property of the codeword's covered half and cannot see chirality.** The chirality lives in the regions and states (Pass 12641, results 3–4), not in the second-moment operator.

**Not advanced:**
- the three-qubit degree-6 real SOS (needs the 288-dimensional charge-1 block);
- the exact replay of Pass 12641 by the other track, which has been working on Q8 tomography and witnesses (ec986540b, 421e8b11b);
- an audit of which corpus results depend on W(E6) ≅ PGSp(4,3), proposed in the handoff.

## Addendum 2: the six letters are the six codewords of a time reversal; chirality appears at third moments (`w33_letters_codewords.py`)

**Letters, basis-free.** In (5,1), letter k's vector is the −1 eigenvector of J_k, the sum of the swaps of the 5 splits containing k (an ovoid of the doily). So the basis-free letter space is ker(R_k + 1), which is a codeword's 16/9 eigenspace. For one θ (all checks exact or to 10⁻⁸):
- θ's 15 doily splits contain the sentinels of exactly **12 pentads = 6 codewords × 2 chiral partners**, and chiral partners share their sentinels;
- the 6 sentinel sets are the doily's **6 ovoids**: any two share exactly one split, and each split lies in exactly two;
- the six codewords' 16/9 eigenspaces are 9-dimensional with **tr(P_k P_l) = 9/25** for k ≠ l, the regular-simplex value.

> **The six letters of a Kramers doily are the six codewords sharing that time reversal** (216 = 36 × 6). The S6 of the proof permutes them.

**Chirality and moments.** For random mixed states:
- max |Σ_L p_e² − Σ_R p_e²| = 7×10⁻¹⁶, identical, since M_L = M_R;
- max |Σ_L p_e³ − Σ_R p_e³| = 1.3×10⁻³, different.

**Chirality first becomes measurable at the three-copy level.**

**W(E6) dependency audit (scope only).** 340 analysis files cite W(E6) ≅ PGSp(4,3) (or 51,840 = |W(E6)|); a list of `PASS*` examples is in this pass's commit. Every result built on that isomorphism is p = 3-specific by construction, consistent with the d = 25 non-certification. A per-result audit was not done.

**Page updated** (version 3): https://claude.ai/artifact/F9piRZo3UkxGiuURXFLHwV now includes the time-reversal and chirality section.

**Not done this round:** the three-qubit degree-6 SOS, and the other track's exact replay (requested again in the handoff).
