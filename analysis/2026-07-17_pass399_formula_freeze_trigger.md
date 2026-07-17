# Pass 399 formula-universe attestation

Pass 399 is merged and its formulas must be present in the frozen repository-wide search universe before the release is considered governance-complete.

The newly certified formula families are:

- bulk adjacency spectrum: `(q^2-1)^1, (-1)^(q^2-1), (q-1)^(q(q^2-1)/2), (-q-1)^(q(q-1)^2/2)`;
- normalized nontrivial spectral radius: `1/(q-1)`;
- Hashimoto circle: `|r|^2=q^2-2` for every nontrivial adjacency eigenvalue;
- Laplacian spectrum: `0^1, (q^2)^(q^2-1), [q(q-1)]^(q(q^2-1)/2), [q(q+1)]^(q(q-1)^2/2)`;
- spanning-tree law: `q^(q^3+q^2-5)(q-1)^(q(q^2-1)/2)(q+1)^(q(q-1)^2/2)`;
- projective quantum period: `2*pi/q`;
- phase-fibre revival obstruction: `a_1(t)=a_2(t)=0` forces `sin(qt)=0` and `exp(-i q^2 t)=1`, hence only scalar identity evolution.

This note intentionally triggers `.github/workflows/pass394-398-release.yml`, which regenerates `data/w33_formula_search_universe_v1.json` from the full checkout.
