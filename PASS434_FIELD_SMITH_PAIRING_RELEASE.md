# Pass 434 — Field-sensitive Smith pairing release

Pass 434 closes the q=7 v1.2 gate and identifies a field-sensitive spectral-to-Smith pairing law for the native Heisenberg bulk graph.

Exact 2-primary critical groups:

- \(q=3\): \((\mathbb Z/2)^6\oplus(\mathbb Z/8)^6\)
- \(q=5\): \((\mathbb Z/4)^{20}\oplus(\mathbb Z/8)^{40}\)
- \(q=7\): \((\mathbb Z/2)^{42}\oplus(\mathbb Z/16)^{126}\)
- \(q=9\), using \(GF(9)\): \((\mathbb Z/8)^{72}\oplus(\mathbb Z/16)^{288}\)
- \(q=11\): \((\mathbb Z/2)^{110}\oplus(\mathbb Z/8)^{550}\)

The proper \(GF(9)\) result is separated from the \(\mathbb Z/9\mathbb Z\) control, whose different Smith shape proves that the law is field-geometric rather than a bare odd-order pattern.

Artifacts:

- `analysis/w33_pass434_field_smith_pairing.py`
- `analysis/PASS434_FIELD_SMITH_PAIRING.md`
- `data/w33_pass434_field_smith_pairing.json`
- `tests/test_w33_pass434_field_smith_pairing.py`

Claim boundary: the five listed fields are exactly certified. The all-odd-prime-power formula remains conjectural pending an integral proof.
