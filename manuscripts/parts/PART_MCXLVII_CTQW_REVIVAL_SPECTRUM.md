# Part MCXLVII — W(3,3) Continuous-Time Quantum Walk Revival Spectrum

**Repository:** W33-Theory  
**Date:** 2025-05-17  
**Status:** Theorem proved and computationally verified

## Summary

This theorem establishes the exact revival structure of the continuous-time quantum walk (CTQW) on W(3,3) with Hamiltonian H = A (the adjacency matrix). The key finding is a **spectral triple coincidence** involving the secondary eigenvalue r = 2:

> r = λ (SRG intersection parameter) = GCD(eigenvalue differences) = log₂(ω)

This forces an exact quantum revival at T* = 2π/r = π.

## Theorem MCXLVII: CTQW Revival Spectrum

**Setup:** W(3,3) is SRG(40,12,2,4) with adjacency eigenvalues:
- k = 12 (multiplicity 1)
- r = 2 (multiplicity 24 = |SL(2,3)|)
- s = −4 (multiplicity 15)

**CTQW Hamiltonian:** H = A, time evolution U(t) = exp(−iAt).

### Part 1: GCD Triple Coincidence

The pairwise eigenvalue differences are:
- k − r = 10
- r − s = 6  
- k − s = 16

Their GCD equals 2 = r = λ:

$$\gcd(k-r,\; r-s,\; k-s) = \gcd(10,\; 6,\; 16) = 2 = r = \lambda$$

This is the *spectral triple coincidence*: the GCD equals both the secondary eigenvalue r AND the SRG intersection parameter λ (the number of common neighbors of any adjacent pair).

### Part 2: Quantum Revival at T* = π

Since all eigenvalues of H = A are integers with GCD = 2, every eigenvalue is an even integer. Therefore:

$$e^{-i \lambda_j \cdot \pi} = e^{-i \cdot (\text{even}) \cdot \pi} = 1 \quad \text{for all } j$$

This proves **exact quantum revival** at T* = 2π/2 = π:

$$U(T^*) = e^{-iA\pi} = I$$

The quantum walker returns to its initial state with unit fidelity after elapsed time π.

### Part 3: Partial Revival at T*/2 = π/2

At half the revival period, the phase acquired by each eigenspace is:
- k = 12: e^{−i·12·π/2} = e^{−6iπ} = **+1** (eigenspace dimension 1)
- r = 2: e^{−i·2·π/2} = e^{−iπ} = **−1** (eigenspace dimension 24)
- s = −4: e^{+i·4·π/2} = e^{2iπ} = **+1** (eigenspace dimension 15)

Only the r-eigenspace (dimension 24 = |SL(2,3)|) acquires a global phase −1. This partial revival implements the **SL(2,3) parity flip**: the binary tetrahedral sector is negated while all other sectors are preserved.

### Part 4: Clique-Eigenvalue Power Law

The clique number ω = 4 satisfies:

$$\omega = 2^r = 2^2 = 4$$

Equivalently: log₂(ω) = r = 2. This means the clique number is a power of the secondary eigenvalue, establishing the **clique-eigenvalue power law**.

## Complete Spectral Triple Coincidence

$$r = \lambda = \log_2(\omega) = \gcd(k-r,\; r-s,\; k-s) = 2$$

where:
- r = 2: smaller positive eigenvalue of A
- λ = 2: SRG intersection number (adjacent pairs)
- log₂(ω) = 2: logarithm of the clique number
- gcd = 2: GCD of all pairwise eigenvalue differences

**All four quantities are simultaneously equal to 2.** This is a deep structural identity of the W(3,3) geometry.

## Numerical Verification

All identities verified by exact computation in `analysis/w33_ctqw_revival_spectrum.py`. Tests in `tests/test_w33_ctqw_revival_spectrum.py` (8 tests, all passing).

## Key Constants

| Quantity | Value |
|----------|-------|
| Revival period T* | π |
| GCD of eigenvalue differences | 2 = r = λ |
| Clique number ω | 4 = 2^r |
| r-eigenspace multiplicity | 24 = \|SL(2,3)\| |
| Partial revival period T*/2 | π/2 (negates 24-dim sector) |

## Source Files

- Analysis: `analysis/w33_ctqw_revival_spectrum.py`
- Tests: `tests/test_w33_ctqw_revival_spectrum.py`
- Results: `PART_MCXLVII_CTQW_REVIVAL_SPECTRUM_results.json`
- Data: `data/w33_ctqw_revival_spectrum.json`
