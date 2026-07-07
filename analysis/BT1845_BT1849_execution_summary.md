# BT1845-BT1849 Execution Summary

## BT1845

Repo search found `analysis/bt959_selected_minimizer_stabilizer_orbit.py`. BT959 transports the tetracode block-permutation quotient S4 through the BT956 matrix. The selected minimizer has a 24-element S4 orbit, trivial stabilizer, and intersects the six support-60 minimizers only at minimizer 2. This closes the transported S4 quotient, while the local A2/Weyl/glue refinement remains open.

## BT1846

Added the canonical winner-2 E8 selector basis export. The canonical selector is `[(3,68),(4,42),(38,65),(90,144)]`, attached to the four runtime striations.

## BT1847

Added shot protocol compression. The 1440 aperture settings compress to 360 center/phase bundles, each preserving four striations. The nominal 144000-shot budget is preserved.

## BT1848

Added the E8-labelled trace runner specification. Trace rows carry base walk fields, `compiled_phase`, and canonical winner-2 E8 selector-pair labels.

## BT1849

Added a paper insert stating the selector is metric-canonical and transported-S4-rigid, with the local A2/Weyl/glue boundary explicitly retained.

## Honest boundary

No full CI, PDF rebuild, measured shot run, or full local A2/Weyl/glue stabilizer computation was executed in this connector pass.
