# Pass 12086: Hosotani dynamics does not select SU(5) or the Standard Model (negative)

Claude track. Builds on 12078 and 12081.

## Results

Order-2 holonomies on T^k generate subspaces of E8/2E8; this pass compares their one-loop energies.

- **k = 4, equal radii, all bases of every type.** The bosonic minimum is d4 (-239.34). su(5) comes second (-238.77),
  only 0.24% higher.
- **k = 4, 625 radius vectors.** d4 wins every time; su(5) never does.
- **k = 5.** a3 (-289.9) beats the Standard-Model type su(3)+su(2) (-275.6).

## Reading

The one-loop Wilson-line potential follows the maximal-symmetry branch e6 -> so(10) -> d4 -> a3. Selecting the
Standard Model needs another ingredient: orbifold projections, fluxes, or matter beyond the adjoint.

Producer: `analysis/w33_pass12086_hosotani_does_not_select_su5.py`.
