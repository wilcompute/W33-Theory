# Pass 12060: a relativity principle for the clock vacuum

Claude track. This pass continues 12059.

## Question

12055–12057 condense one event, and the vacuum picks one of its three clock real forms. 12059 showed that no
observer can make that choice. This pass asks the converse: **does the chosen clock pick an observer**, i.e. a rest
frame?

## Definitions

- **Clock symmetry.** The symmetry of the clock vacuum at p is H_p, the unique index-3 subgroup of the point
  stabiliser (12059). It is the same for all three clock forms at p.
- **Observer.** An observer is a Kramers reversal J (36 up to sign).
- **Fixed observer.** A vacuum symmetry g *fixes* the observer when gJg⁻¹ = ±J, i.e. g lies in the Lorentz group or
  in the parity coset.
- **Coverage.** Sp(4,3) has rank 3 on points: it is transitive on points, on collinear pairs and on non-collinear
  pairs. So one base event with all 39 partners covers every case.

## Theorem

1. **Relativity principle.** H_p is transitive on the 36 observers. A one-clock vacuum picks a time and no rest
   frame.
2. **Two compatible clocks pick three rest frames.** Take p and q collinear, so they lie in one context and are
   jointly measurable.
   - The common symmetry is H_p ∩ H_q ≅ ±1 × S₃ = D₁₂, of order 12.
   - It fixes exactly **three** observers: exactly the J with **Jp = q**, the frames in which the two events are each
     other's time reverse.
   - Its observer orbits are 1,1,1, 3⁹ and 6.
3. **Two incompatible clocks leave only spin.** Take p and q non-collinear.
   - The common symmetry is C₂ × Q₈, of order 16. It contains no translations at all.
   - Its observer orbits are 4,4,4,8,8,8, so no observer is fixed.

## Reading

- The single-event vacuum of 12055–12057 respects a finite relativity principle: every observer is equivalent.
- A preferred frame needs a second, compatible clock, and is then the **mirror frame** of the pair.
- Incompatible clocks break everything except the spin group.

## Scope

- These are finite-group statements; "rest frame" means an observer fixed by the vacuum symmetry.
- With three or more clocks the common symmetry falls to ±1 or to order 4, which fixes observers vacuously. No claim is
  made there.

## Prior art

- **Corpus:** 11831 (observers and Lorentz SL(2,9)), 12058 (clock group), 12059 (the clock group is canonical and is
  not Lorentz-invariant).
- **Classical:** the rank-3 action of Sp(4,3).
- **Search:** grep of the corpus for mirror frames and for fixed observers of a clock pair found nothing.

## Certificates

- Producer: `analysis/w33_pass12060_relativity_principle_for_the_clock_vacuum.py`, which writes
  `data/w33_pass12060_relativity_principle_for_the_clock_vacuum.json`.
- GAP cross-check: `analysis/search_drivers_12060/gap_crosscheck.g`, giving D12 for 12 partners and C2 × Q8 for 27
  partners, with the same orbit counts.
