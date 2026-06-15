# BT1126 — Main-paper patch helpers

BT1126 corrects the W33 paper target and adds dry-run support.

## Main source correction

The main W33 source is

```text
w33_paper.tex
```

not

```text
paper/w33_preprint.tex
```

The W33 patch helper now targets `w33_paper.tex` and inserts staged section inputs before

```text
\end{document}
```

using root-relative paths such as

```text
\input{paper/sections/sec_bt1120_1122_k3_yukawa_build_path}
```

## Dry-run support

Both helpers now accept:

```text
--dry-run
```

and report the target and planned insert count without mutating source files.

## Boundary

This updates the helper path and prevents future confusion between preprint and main paper.  It does not claim the full TeX compile has run.
