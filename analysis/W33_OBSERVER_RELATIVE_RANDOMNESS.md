# Observer-relative randomness and decryptability

## Core correction

The slogan "random information is encrypted information" is too strong. A stronger and technically safer formulation is:

> **Randomness is a relation among an outcome, an observer's side information, the observer's computational resources, and the physically admissible information available to that observer. Encryption is one engineered way of making information unresolved relative to an observer.**

For outcome `X`, observer information `O`, and added side information/key `K`, the exact Shannon identity is

\[
H(X\mid O)-H(X\mid O,K)=I(X;K\mid O).
\]

The left side is the amount of observer-relative uncertainty removed by the added side information. If

\[
H(X\mid O,K)=0,
\]

then all of the observer's Shannon uncertainty about `X` is resolved by `K`. Calling `K` a "key" is useful only when it is restricted to legitimate causal/side information; otherwise the trivial choice `K=X` makes the definition empty.

## Four different notions that should not be collapsed

1. **Epistemic randomness.** The outcome is determined by hidden state or a seed. More side information can reduce the conditional entropy to zero.
2. **Cryptographic pseudorandomness/secrecy.** The system is deterministic given a secret, but bounded observers cannot distinguish/invert efficiently; perfect secrecy is the stronger information-theoretic special case.
3. **Computational unpredictability.** Even when conditional entropy is zero in principle, computing the determined result can be expensive or undecidable for universal systems.
4. **Operational quantum randomness.** A protocol can certify positive guessing entropy/min-entropy against all adversary side information allowed by specified physical/causal assumptions. This does not by itself decide between metaphysical interpretations of quantum mechanics.

NIST explicitly separates deterministic random-bit generators from entropy sources: SP 800-90A specifies deterministic mechanisms, while SP 800-90B specifies entropy sources. A deterministic generator cannot increase information-theoretic entropy beyond its seed even when its output is computationally pseudorandom.

## Exact finite witnesses

`w33_observer_relative_randomness.py` checks four examples.

### Deterministic seeded expansion

An 8-bit seed is mapped deterministically to a 32-bit SHA-256 prefix. In the finite witness all 256 outputs are distinct, so

\[
H(X)=8,\qquad H(X\mid S)=0,
\]

while only `1/2^24` of the 32-bit output space is reachable. This is deliberately **not** a PRG security proof; it demonstrates that deterministic expansion does not create 32 information-theoretic bits from 8 seed bits.

### One-time pad

For a uniform four-bit message `M`, key `K`, and ciphertext `C=M XOR K`, exhaustive enumeration gives

\[
I(M;C)=0,
\]

\[
H(M\mid C)=4,
\]

\[
H(M\mid C,K)=0.
\]

So encryption can make structured information look maximally unresolved to the keyless observer while making it exactly recoverable to the keyed observer. This supports the metaphor but does not imply that every random string is ciphertext.

### W33 retained-noise-seed experiment

The existing reversible-observation experiment provides a project-native example. For two timing observations with independent two-bit jitter seeds,

\[
H(O\mid Y)=3\text{ bits},
\]

but

\[
H(O\mid Y,S)=0.
\]

Thus

\[
I(O;S\mid Y)=3\text{ bits}.
\]

The seed register is four bits, and one bit remains hidden after observing its effect:

\[
H(S\mid Y,O)=1\text{ bit}.
\]

That is a concrete example of apparent randomness being fully explained by retained causal side information without the side information itself being fully reconstructible from the effect.

### Shared-seed privacy failure

Reusing one seed across timings saves seed storage but makes common noise algebraically removable. For the current finite model, timing differences recover all exact timing information for two and four timing observations. Therefore more correlation can make an observer *less* uncertain even when the marginal noise remains nonzero.

## AI generation

For a sampling-based language model, knowing the model architecture/weights is not by itself enough to make a sampled completion reproducible. One also needs the prompt/context, sampler, RNG state/seed, software implementation and relevant numerical execution details. Current numerical frameworks also document operations whose results may not be reproducible across platforms or even under identical seeds unless deterministic algorithms are explicitly selected.

So a better statement is:

\[
\text{AI output}=F(\text{model},\text{context},\text{sampler},\text{random state},\text{execution environment}).
\]

Fix every argument and a deterministic implementation gives a fixed output. Hide the random state and the output is stochastic relative to the observer. Use a secure PRG and the hidden state can be computationally inaccessible even when the generator is public.

## A Theory of Everything still need not imply universal prediction

Deterministic physical law does not imply that every future proposition is calculable. The repository already constructively reduces authenticated HoloIR to finite counter programs and then to a two-counter Minsky core. Under ordinary Turing-computability assumptions, if a physical theory faithfully embeds universal computation, then a predictor that decided for every encoded state whether execution would ever reach `HALT` would solve the halting problem.

Therefore:

\[
\boxed{\text{deterministic law}\not\Rightarrow\text{universal calculability}.}
\]

A complete law could still leave three different barriers:

- insufficient observer side information,
- prohibitive resource requirements,
- formal undecidability.

This is stronger than chaos: chaos is sensitivity and precision growth; undecidability is the absence of a single algorithm answering all instances.

## Quantum boundary

The statement "true probability lies at the quantum scale" is operationally defensible only with an explicit model. Bell-inequality-based device-independent randomness generation can certify unpredictability against broad classes of adversarial side information under causal/measurement-independence assumptions. But Bell tests rule out local deterministic hidden-variable models, not every deterministic interpretation. Bohmian mechanics is deterministic but nonlocal; Everett-style unitary evolution is deterministic at the global wavefunction level.

A useful cryptographic translation is:

> **Device-independent quantum randomness tries to certify that no physically admissible adversary side information acts as a sufficient decryption key for the observed outcome.**

That is an operational statement about guessing probability/min-entropy, not a proof that no deeper ontology could be deterministic.

## W33/contextuality extension

The next project-specific pressure point is contextuality. If quantum randomness were always classical "missing-key" randomness, one would expect a single context-independent hidden lookup table assigning all outcomes. But W33's two-qutrit Pauli geometry is built from overlapping commuting contexts, and the repo already treats contextuality as the failure of context-independent predetermined values.

This suggests a stronger object than a hidden key:

\[
K(c)=\text{context-dependent side information for measurement context }c.
\]

The finite-geometry question becomes whether these local decryption maps glue to one global section. Contextuality says, in the relevant scenarios, they do not. That gives a geometric version of the slogan:

> classical randomness may be missing global side information; quantum contextuality can obstruct the existence of any single noncontextual global decryption key.

This should be tested with an exact W33 contextuality cocycle/section obstruction rather than asserted from analogy.

## Reproduce

```bash
python analysis/w33_observer_relative_randomness.py
```

The script writes `data/W33_OBSERVER_RELATIVE_RANDOMNESS.json` and fails closed if the exact finite identities do not hold.

## Sources and boundaries

- NIST SP 800-90A Rev. 1: deterministic random bit generators: https://csrc.nist.gov/pubs/sp/800/90/a/r1/final
- NIST SP 800-90B: entropy sources: https://csrc.nist.gov/pubs/sp/800/90/b/final
- Stanford CS255 notes: one-time pad and perfect secrecy: https://crypto.stanford.edu/~dwu4/notes/CS255LectureNotes.pdf
- PyTorch reproducibility notes: https://docs.pytorch.org/docs/stable/notes/randomness.html
- Pironio et al., randomness certified by Bell's theorem: https://www.nature.com/articles/nature09008
- Liu et al., device-independent quantum random-number generation: https://www.nature.com/articles/s41586-018-0559-3
- Stanford Encyclopedia, Many-Worlds Interpretation: https://plato.stanford.edu/entries/qm-manyworlds/

No worldwide novelty claim is made. The exact novelty here is the project-specific observer/key separation certificate and its explicit weld to the existing W33 reversible-noise-seed model and universal-counter-machine boundary.
