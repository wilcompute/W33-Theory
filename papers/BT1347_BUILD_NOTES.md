# BT1347 — Build Notes

## Files

| File | Purpose |
|------|---------|
| `BT1347_photonic_holonet_journal.tex` | Main manuscript (RevTeX 4-2, PRL style) |
| `BT1347_cover_letter.md` | Cover letter draft for PRL submission |
| `BT1347_BUILD_NOTES.md` | This file |

## Build commands

```bash
cd papers
pdflatex BT1347_photonic_holonet_journal.tex
pdflatex BT1347_photonic_holonet_journal.tex   # second pass for references
```

RevTeX 4-2 is included in any full TeX Live 2022+ or MiKTeX 22+ installation.
If the `physics` package is unavailable, replace `\ket{...}` with `|\cdots\rangle`.

## arXiv submission

1. Upload `BT1347_photonic_holonet_journal.tex` (source).
2. arXiv will compile it using its RevTeX 4-2 engine.
3. Primary category: **quant-ph**. Cross-list: **math-ph**.
4. Set the repository URL in the Comments field:
   `Source code and witnesses: https://github.com/wilcompute/W33-Theory`

## Paper series position

| Paper | Format | Length | Purpose |
|-------|--------|--------|---------|
| BT1345 | Markdown | Long | Accessible, full definitions |
| BT1346 | LaTeX | Medium | arXiv skeleton, general audience |
| BT1347 | LaTeX (RevTeX) | Short (PRL) | Formal journal submission |
