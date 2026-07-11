# W33 odd-q rank formalization

The `formal/` package contains two layers:

- `W33/OddQRank.lean`: arithmetic rank and Jordan-block identities;
- `W33/FourierBlocks.lean`: the kernel-checked interface from trivial/nontrivial additive-character blocks to the global odd-`q` theorem, including the exact `q=3` ranks and Jordan census
  \(D_3\sim J_4^2\oplus J_3^{22}\oplus J_1^6\).

`W33.lean` imports the complete package surface.

```bash
cd formal
lake update
lake build --wfail
```

The repository workflow `.github/workflows/lean-formal.yml` requires three independent conditions: `lake build --wfail`, an explicit repository scan rejecting `sorry` and `admit`, and the official bundled `leanchecker` pass through `leanprover/lean-action@v1`. The local execution container does not include Lean/Lake, so the committed Python witness validates source structure and algebra while GitHub Actions performs kernel and independent-checker validation.
