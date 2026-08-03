# Evidence workflow revision

The base workflow now commits only stable integration outputs, PDF hashes, a compact manifest, and a one-shot `OBSERVED_COMPLETE.json` marker. Volatile synthesis logs remain workflow artifacts and cannot create a recursive evidence-commit loop.
