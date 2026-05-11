# W(3,3) Theory

> **The W(3,3)–E₈ Correspondence Theorem**: deriving the Standard Model from a single finite geometry with zero free parameters.

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](LICENSE)

---

## What this is

This repository contains the full computational record of a mathematical physics programme centred on the symplectic polar space **W(3,3)** — the unique generalised quadrangle of order \((3,3)\).

W(3,3) is a strongly regular graph SRG(40, 12, 2, 4) whose combinatorial rigidity simultaneously encodes:
- the gauge groups of the Standard Model (SM)
- the root system of E₈ (240 roots, 480 directed)
- a single master equation \(q! = 2q\) uniquely solved by \(q=3\)

---

## Key Theorems (May 2026 Synthesis)

| Part | Theorem | Status |
|---|---|---|
| CCCCCXXV | Quantum return \(U(\pi)=I\); Shannon capacity \(\Theta=10\) | ✓ Proved |
| CCCCCXXVI | Complement eigenvalues \(\pm q\); \(C(-1)=q^{q+1}\) | ✓ Proved |
| CCCCCXXVII | Kirchhoff index \(267/2\); heat kernel coefficient \(=2E\) | ✓ Proved |
| CCCCCXXVIII | Ramanujan property; optimal mixing time \(\approx 3.36\) steps | ✓ Proved |
| CCCCCXXIX | W(2,2)→W(3,3)→W(4,4) hierarchy; E₆–E₈ mirror | ✓ Stated |

See [`MASTER_SYNTHESIS_APPENDIX.md`](MASTER_SYNTHESIS_APPENDIX.md) for all proofs consolidated.

---

## Repository Structure

```
/
├── MASTER_SYNTHESIS_APPENDIX.md   ← Consolidated new theorems (May 2026)
├── PART_CCCCC*.md                 ← Individual theorem notes (Parts 500+)
├── PART_CCCC*.md                  ← Individual theorem notes (Parts 400+)
├── *.py                           ← Computational scripts
├── *.json                         ← Machine-readable results
├── CITATION.cff                   ← Citation metadata
└── LICENSE                        ← CC BY 4.0
```

---

## Core Parameters of W(3,3)

| Symbol | Value | Meaning |
|---|---|---|
| v | 40 | Vertices |
| k | 12 | Valency |
| λ | 2 | Triangles per edge |
| μ | 4 | Non-adjacent common neighbours |
| r | 2 | Positive eigenvalue |
| s | −4 | Negative eigenvalue |
| E | 240 | Edges (= E₈ roots) |
| α | 10 | Independence number |
| Θ | 10 | Shannon capacity |
| Kf | 267/2 | Kirchhoff index |

---

## Citation

See [`CITATION.cff`](CITATION.cff) for the canonical citation.

---

## License

[Creative Commons Attribution 4.0 International](LICENSE)
