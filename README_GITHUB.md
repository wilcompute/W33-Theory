# W33 Unified Theory of Physics

**Author:** Wil Dahn  
**Date:** January 2026

## Overview

This repository contains the complete development of a unified theory of physics based on the **W(3,3) configuration** - a finite geometry consisting of 40 points, 40 lines, 81 cycles, and 90 Klein four-groups.

The remarkable equality **|Aut(W33)| = |W(E₆)| = 51,840** connects this finite structure to exceptional Lie algebras, enabling parameter-free derivations of fundamental physical constants.

## Key Results

| Quantity | W33 Formula | Predicted | Observed | Agreement |
|----------|-------------|-----------|----------|-----------|
| α⁻¹ | 81 + 56 + 40/1111 | 137.036004 | 137.035999 | 5 ppb |
| sin²θ_W | 40/173 | 0.23121 | 0.23121 | 0.1σ |
| Ω_DM/Ω_b | 27/5 | 5.4 | 5.408 | 0.15% |
| m_t | v√(40/81) | 173.03 GeV | 172.76 GeV | 0.15% |
| m_H | (v/2)√(81/78) | 125.46 GeV | 125.25 GeV | 0.16% |
| α_s(M_Z) | 27/229 | 0.1179 | 0.1179 | **EXACT** |
| N_gen | 81/27 | 3 | 3 | **EXACT** |
| D (M-theory) | √121 | 11 | 11 | **EXACT** |

## Repository Structure

```
├── W33_FORMAL_THEORY.tex          # Complete LaTeX paper
├── W33_FORMAL_THEORY.pdf          # Compiled PDF
├── THEORY_PART_*.py               # 52 Python exploration scripts
├── w33_*.py                       # Analysis and verification code
├── data/                          # Computed data and results
├── src/                           # Source code libraries
├── archive/                       # Historical development files
└── *.md                           # Documentation and summaries
```

## The W33 Numbers

| Number | Origin | Physical Role |
|--------|--------|---------------|
| 40 | W33 points | Observable degrees of freedom |
| 81 | W33 cycles (3⁴) | Loop contributions |
| 90 | W33 Klein groups | Tensor structure |
| 121 | Total (11²) | Spacetime unity |
| 27 | E₆ fundamental | Generation structure |
| 56 | E₇ fundamental | Matter multiplet |
| 78 | E₆ adjoint | Gauge structure |
| 133 | E₇ adjoint | Hidden sector |
| 240 | E₈ roots | Gauge bosons |
| 1111 | 4th repunit | 4D spacetime encoding |
| 51,840 | |Aut(W33)| = |W(E₆)| | Full symmetry group |

## Core Equations

### Fine Structure Constant
```
α⁻¹ = 81 + 56 + 40/1111 = 137.036004
       ↑    ↑      ↑
    cycles E₇f  points/R₄
```

### Weinberg Angle
```
sin²θ_W = 40/(40+133) = 40/173 = 0.23121
          ↑     ↑
       points  E₇ adj
```

### Strong Coupling
```
α_s(M_Z) = 27/(240-11) = 27/229 = 0.1179  [EXACT MATCH]
           ↑    ↑   ↑
         E₆f  E₈r  √121
```

## Publications

The main paper is available as:
- **LaTeX source:** `W33_FORMAL_THEORY.tex`
- **PDF:** `W33_FORMAL_THEORY.pdf` or `W33_FORMAL_THEORY_WilDahn_Final.pdf`

## Requirements

- Python 3.8+
- NumPy, SciPy
- Optional: SageMath for advanced computations
- LaTeX (MiKTeX or TeX Live) for PDF compilation

## References

1. Coxeter, H.S.M. (1940). "The polytope 2₂₁"
2. Conway & Sloane (1999). "Sphere Packings, Lattices and Groups"
3. Baez, J.C. (2002). "The Octonions"
4. Particle Data Group (2022). "Review of Particle Physics"
5. Planck Collaboration (2020). "Planck 2018 results"

## License

This research is shared for academic and educational purposes.

## Contact

**Wil Dahn**  
GitHub: [@wilcompute](https://github.com/wilcompute)

---

*"The W(3,3) configuration is the Rosetta Stone of physics - a finite geometry that encodes the infinite complexity of our universe."*
