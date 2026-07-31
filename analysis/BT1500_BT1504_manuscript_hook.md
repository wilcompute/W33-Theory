# Passes 1500–1504 manuscript hook

The exact Passes 1500–1504 release was already merged to `master` in commit `0547db3f33e47ce76f7f10eab22dbcee724b0f9d`. This follow-up makes the existing theorem insert reachable from `paper/w33_preprint.tex` without rewriting the historical complement-duality section.

The prior `paper/sections/sec_complement_duality.tex` blob is preserved byte-for-byte as `sec_complement_duality_body.tex`. The original path becomes a reversible wrapper that inputs the preserved body once and then inputs `sec_bt1500_bt1504_five_frontiers.tex` once.

No worker, source, compact certificate, theorem boundary, or exact hash is changed.
