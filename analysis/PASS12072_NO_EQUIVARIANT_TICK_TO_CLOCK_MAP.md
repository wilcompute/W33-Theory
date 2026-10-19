# Pass 12072: there is no equivariant tick-to-clock map

Claude track. Settles the question flagged in 12068.

## Results

1. **Ticks are affine hyperplanes.** Pauli conjugation shifts labels by ω(r,p). So the 120 Clifford ticks carry the
   action of ASp(4,3) on the 120 affine hyperplanes {ω(x,p) = k}.
2. **Every copy of Sp(4,3) fixes 40 ticks.**
   - H¹(Sp(4,3), F₃⁴) = 0: GAP finds one complement class of translations in ASp(4,3), of order 4,199,040.
   - So every Sp(4,3) in the Clifford group is a point stabiliser of AG(4,3) and fixes 40 ticks.
   - Directly in the operator model: with symmetric Weyl labels D_v = ω^(−a·b) XᵃZᵇ, the 40 label-0 Weil ticks have
     orbits 40 + 80.
   - Control: 12055's own label-0 ticks also generate translations and are transitive on all 120.
3. **Clocks have no fixed point.** Clocks form one orbit of 120, with stabiliser of order 432, and the point stabiliser
   fixes none of the three clocks at its point.

## Conclusion

No tick–clock bijection is equivariant. A tick determines its event, but not its clock.

## Consequences

- 12055's "120 = the clock involutions" is a count only.
- **12061's reading "a two-tick condensate carries the 12060 rest frames" is WITHDRAWN.** Its spectra and inequalities
  stand.
- 12060's clock-group results stand.

Producer: `analysis/w33_pass12072_no_equivariant_tick_to_clock_map.py`. GAP driver:
`analysis/search_drivers_12072/complements.g`.
