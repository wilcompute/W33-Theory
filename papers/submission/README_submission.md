# arXiv Submission Package: W(3,3) Paper

## Files

| File | Role |
|---|---|
| `main.tex` | Root document (includes §0-intro, §§1,4,5, bibliography) |
| `section2_uniqueness.tex` | §2: C1-C5 Uniqueness Theorem |
| `papers/standalone/section3_tau_bridge.tex` | §3: Tau bridge, C5 curve, j-tower, C6 |
| `arXiv_metadata.txt` | Title, abstract, MSC, categories |

## Compile

```bash
# From the repository root:
pdflatex main.tex
pdflatex main.tex   # second pass for \ref resolution
```

Requires standard TeX Live packages: `amsmath`, `amssymb`, `amsthm`,
`hyperref`, `booktabs`.

## arXiv Upload Checklist

- [ ] `pdflatex main.tex` produces no errors
- [ ] All `\ref{}` and `\cite{}` resolve (check .log for `?`)
- [ ] Abstract matches `papers/submission/arXiv_metadata.txt`
- [ ] Primary category: **math.NT**
- [ ] Cross-list: **math.CO**, **hep-ph**
- [ ] MSC codes entered on arXiv form: 11F11, 05C50, 11G15, 11R11
- [ ] Companion repo URL in `\bibitem{Dahn2026repo}` is correct
- [ ] Test count in abstract matches current `pytest` output

## Test Suite

```bash
pip install pytest sympy scipy numpy
pytest tests/ -v --tb=short
```

Expected: **456 passed** (as of Phase CCLXXXVI).
