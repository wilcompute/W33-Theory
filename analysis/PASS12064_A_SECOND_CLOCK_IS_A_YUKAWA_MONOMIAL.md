# Pass 12064: a second clock is a Yukawa monomial, and two clocks split matter by triality

Claude track. Builds on 12056 and 12060.

## Results

1. **Far fibres carry cubic monomials.** The three colour-3 roots of each far fibre project to a zero-sum tritangent
   (an E6 cubic monomial) of the 27 of E6(p).
   - The zero sum is automatic, since r + ωr + ω²r = 0.
   - The 270 lifted triples are corpus: 2026-09-21 matter81.
   - The 27 far points give 9 tritangents, three points each. These **partition** the 27 weights, i.e. they form one
     of the nine-tritangent covers of PASS5010.
2. **Vacuum symmetry on matter (modulo −1, which only swaps 27 and 27̄):**
   - one clock: transitive;
   - two collinear clocks: 27 = 3+3+3+6+6+6;
   - two non-collinear clocks: 27 = 1+1+1+8+8+8.
3. **Triality.** For the non-collinear pair:
   - The fixed weights are exactly the second clock's monomial.
   - The E6 roots orthogonal to that monomial form D4, and they are exactly the fibres of the four common neighbours
     {p,q}^⊥ (the D4 of 12056).
   - The three 8-orbits are distinct minuscule D4 weight systems.
   - So **27 = 1+1+1 + 8_v + 8_s + 8_c**, the Spin(8) triality branching.

## Reading

Relative to a clock at p, every non-collinear event is a Yukawa coupling 27³. A second clock there leaves spin only
(12060) and splits one generation into the three triality octets plus the monomial's three singlets.

## Prior art and scope

- The E6 ⊃ D4 × U(1)² branching and the cubic triples are classical or corpus.
- New: the two-clock vacuum realises the branching, with the singlets on the second clock.
- An earlier guess, that far points equal single weights, is **refuted**: each far point carries three weights.
- This is weight-level only; no Yukawa magnitudes are computed.

Producer: `analysis/w33_pass12064_a_second_clock_is_a_yukawa_monomial.py`.
