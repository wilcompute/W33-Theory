# Pass 78 -- Equivariant zeta / Terwilliger / code-boundary closure

**Status: PASS** -- witness `w33_pass78_equivariant_closure.py`, JSON
`w33_pass78_equivariant_closure.json`, and focused test
`tests/test_pass78_equivariant_closure.py`.

Pass 77 proved the rank-3 point-module representation and the W/Q ovoid
separator.  Pass 78 turns that into a more careful architecture map:

1. **Vertex Artin-Ihara map.**  On the 40-dimensional point module, only three
   irreducible constituents are active: `1`, `15`, and `24`.  They carry the
   Bass factors `(1-12u+11u^2)`, `(1+4u+11u^2)^15`, and
   `(1-2u+11u^2)^24`; the `(1-u^2)^200` tail brings the total denominator
   degree to `480`, the directed-edge carrier.
2. **Local algebra fingerprint.**  The global Bose-Mesner algebra has dimension
   `3`; the point-rooted Terwilliger algebra has dimension `16`, with distance
   fibres `[1,12,27]`.  The full Wedderburn/T-module decomposition remains the
   next exact local-algebra target.
3. **Ovoid/spread duality.**  The odd-q W side has `alpha=7` and no ovoid; the
   parabolic-quadric dual has `alpha=10`.  Meanwhile W has exactly `36` spreads,
   every isotropic line lies in exactly `9`, and spread overlaps are
   `{1:360, 4:270}`.
4. **Code-boundary honesty.**  The `[[66,8,3]]_3` protected-store claim is
   heavily documented, but this pass does not promote a generator/stabilizer
   construction.  That is now marked as the concrete next verification target.
5. **Weil/Clifford carrier.**  The two-qutrit oscillator dimension is
   `q^2=9=5+4`, using the GAP-confirmed degree-4 and degree-5 irreducibles.
6. **Spence boundary.**  The W/Q pair is a proved cospectral, locally identical,
   non-isomorphic pair.  The full 28-graph hearing table still requires Spence
   adjacency data or a generator for all 28 graphs.
7. **Finite ladder.**  The verified carrier ladder is:
   `3 -> 9 -> 16 -> 40 -> 36 -> 480 -> 51840`.

The main theoretical correction is that "full equivariant zeta" is complete
only for the point-module/Bass-Ihara layer.  The edge-zeta Artin factorization
over all 34 irreducibles remains open and should be treated as a sharper Pass
79 target, not as already solved.
