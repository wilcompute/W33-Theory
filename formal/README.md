# W33 odd-q rank formalization

The `formal/` package now contains two layers:

- `W33/OddQRank.lean`: arithmetic rank and Jordan-block identities;
- `W33/FourierBlocks.lean`: the kernel-checked interface from trivial/nontrivial additive-character blocks to the global odd-`q` theorem, including the exact `q=3` rank and Jordan census.

`W33.lean` imports the complete package surface.

```bash
cd formal
lake update
lake build --wfail
```

The repository workflow `.github/workflows/lean-formal.yml` uses `leanprover/lean-action@v1` and requires both `lake build --wfail` and the independent `nanoda` checker with `sorryAx` forbidden. The local execution container does not include Lean/Lake, so the committed Python witness validates source structure and algebra while GitHub Actions performs kernel validation.
