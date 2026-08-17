#!/usr/bin/env python3
"""SUPERSEDED compatibility wrapper for Pass5880-5887.

The original BT1641 verifier used a 33-vertex circulant surrogate and labelled it
W33. Pass5888-5895 proved that this was the wrong graph identity and quarantined
the resulting FSR/finesse/capacity claims.

Run the exact replacement instead:
    python analysis/w33_pass5888_5895_ihara_identity_correction.py

Canonical facts now enforced:
- W(3,3) collinearity graph = SRG(40,12,2,4), 240 edges;
- Hashimoto operator = 480 directed edges, outdegree 11;
- 78 adjacency-induced nontrivial modes have modulus sqrt(11);
- finite eigenphases are not equidistributed;
- physical FSR/finesse/capacity require an independent propagation/coupling model.
"""

from analysis.w33_pass5888_5895_ihara_identity_correction import main

if __name__ == "__main__":
    main()
