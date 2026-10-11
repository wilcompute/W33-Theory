# Pass 11923: the heterotic charm–up lock and the magnetized up lemma are one theorem — and it survives every Δ(54)-symmetric Higgs vacuum

Producer: `analysis/w33_pass11923_stabiliser_higgs_lock.py`
Certificate: `data/w33_pass11923_stabiliser_higgs_lock.json`
Regression: `tests/test_w33_pass11923.py`
Track: Claude. This pass joins the heterotic line (Passes 11903 and 11908) to the magnetized line (Passes 11918 and 11921).

## 1. One matrix in two string realisations

**The shared structure.** In both realisations, the family index a of Q and u^c is a qutrit:

| realisation | family qutrit |
|---|---|
| heterotic (Pass 11903) | the three fixed points of the Wilson-line-free family torus |
| magnetized (Pass 11921) | the 10's magnetic-translation qutrit |

**Three facts they share.**
* The ℤ₃ selection rule allows Q_a u_b H_k exactly when a + b ≡ k (mod 3).
* The coupling depends only on the class k and on a − b.
* Theta evenness makes the two off-diagonal values equal.

**The common Yukawa.** With the light Higgs a qutrit state h over its three copies,

  **Y_u(h)_{ab} = h_{a+b} g_{a−b},  g₊ = g₋.**

**How the earlier passes fit.**
* Pass 11903's lock (m_c = m_u for every Kähler modulus) is the case where h is a single Higgs row, a Z-eigenstate.
* Pass 11918's monomial lemma is the same matrix.
* The two "unrelated" charm–up locks are one theorem.

## 2. Every stabiliser Higgs locks

**The result.** Each of the 12 qutrit stabiliser states h gives Y_u(h) an exactly degenerate pair, for every even g.
Checked to 1.4·10⁻¹⁵ over 200 random complex g.

**The converse is false.** Minimising the gap from random starts found 54 of 60 degenerate solutions that are clearly
not stabiliser states (Pauli expectation down to 0.51). Haar-random h always unlock (minimum gap 10⁻³).

## 3. Every Δ(54)-symmetric Higgs vacuum is a stabiliser state

**The triplet.** The three Higgs copies form a Δ(54) triplet. This is standard for twisted states on a Wilson-line-free
T²/ℤ₃ (Kobayashi–Nilles–Plöger–Raby–Ratz 2006). In the magnetized case it is the exact 3-dimensional degeneracy of
Pass 11921.

**The potential.** For charge-preserving aligned vevs, the general degree-(2,2) Δ(27)-invariant potential is

  a Σ|h_i|⁴ + Re(c Σ_i h̄_i² h_{i+1} h_{i+2}) + (Σ|h|²)² terms.

**The result.**
* Over 300 random (a, c), the global minimum is **always** a stabiliser state. The infidelity is at most 6·10⁻¹¹.
* The snapped exact stabiliser state has the same potential value and a gap of 2·10⁻¹⁶.
* This reproduces the classical three-Higgs-doublet result (Ivanov–Nishi 2015; de Medeiros Varzielas et al.).

**Consequence.** The charm–up lock survives the **full Higgs triplet** at every Δ(54)-symmetric vacuum, not only the
single-row Higgs that Pass 11903 checked. To unlock it, the Higgs potential itself must break Δ(54).

## 4. The splitting measures the Higgs's magic

**The scaling.** Near a stabiliser state, the gap grows like the square root of the Higgs's stabiliser Rényi magic M₂.
The log-slope is 0.517 for 9 points over δ = 10⁻⁶ to 10⁻².

**Reading.** m_c ≠ m_u requires a *magic*, i.e. non-stabiliser, Higgs flavour state.
* The size of the charm–up splitting is set by how far the Higgs sits from W(3,3)'s stabiliser points.
* Breaking Δ(54) is the source of that magic.

## Reading for both lines

**Heterotic.** The local-10 lock of Passes 11903 and 11908 cannot be evaded by Higgs mixing among the family-torus
copies while the Higgs potential is Δ(54)-symmetric. It needs a Δ(54)-breaking source in the Higgs sector, for example
vevs of twisted fields in non-trivial Δ(54) representations, of the kind the Fayet–Iliopoulos (FI) condensate supplies.

**Magnetized.** The same holds. There the hypercharge Wilson line is an extra handle: it breaks the evenness g₊ = g₋
directly (Pass 11918).

**Next.** The next heterotic computation is the Δ(54) charges of the FI-condensate fields in the 152 local-10 models.
If a Δ(54)-breaking vev appears in the Higgs mass matrix, the lock lifts at the corresponding order.

## Prior art

* Δ(54) flavour symmetry in heterotic ℤ₃ orbifolds: Kobayashi–Nilles–Plöger–Raby–Ratz, Nucl. Phys. B768 (2007).
* Δ(27)/Δ(54) three-Higgs-doublet vacua: Ivanov–Nishi, JHEP 2015; de Medeiros Varzielas et al.
* The identification of those vacua with qutrit stabiliser states (Δ(27) as the qutrit Heisenberg group) is
  well-established.
* New here:
  * the unification of the two charm–up locks;
  * the stabiliser ⇒ lock theorem;
  * the magic scaling of the splitting.
* Corpus: Passes 11903, 11908, 11918, 11921; magic as a modular function (11877).
