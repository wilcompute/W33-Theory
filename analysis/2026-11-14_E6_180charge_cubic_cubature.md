# 2026-11-14: Cubature of the signed E6 cubic by its 180 minimal integral charges

## Exact theorem in the canonical native coordinate basis

Let N(x)=sum over the 45 signed tritangent supports (i,j,k) of s_ijk*x_i*x_j*x_k, with s_ijk in {+1,-1}. Let C be the 180 signed coordinate vectors obtained by placing signs (epsilon_i,epsilon_j,epsilon_k) on one tritangent, zero elsewhere, and requiring epsilon_i*epsilon_j*epsilon_k=s_ijk. These are precisely the previously certified 180 integral charges of cubic value N=+1 and squared norm 3 (Pass 12668).

**For every real x in R^27**, the following exact polynomial identities hold:

    sum_{z in C} (z dot x)   = 0
    sum_{z in C} (z dot x)^2 = 20 sum_i x_i^2
    sum_{z in C} (z dot x)^3 = 24 N(x)
    sum_{z in C} (z dot x)^4 = 20 sum_i x_i^4
                             + 24 sum_{{i,j} edge of Schlaefli} x_i^2 x_j^2.

The edges are the 135 unordered pairs appearing together in one tritangent. Every coordinate occurs in exactly five of the 45 tritangents, every graph vertex has degree ten, and every graph edge lies in exactly one tritangent. Consequently C is a uniform **spherical 2-design of radius sqrt(3)** with covariance matrix I27/9. It is **not** a spherical 3-design: its signed third moment is nonzero and is exactly the E6 cubic.

In tensor form, with ordered indices,

    sum_z z_i z_j = 20 delta_ij
    sum_z z_i z_j z_k = 4 s_ijk if (i,j,k) is an ordered tritangent, 0 otherwise
    sum_z z_i^4 = 20
    sum_z z_i^2 z_j^2 = 4 if {i,j} is a Schlaefli edge, 0 otherwise.

The fourth tensor vanishes for all other index multiplicity patterns (except permutations of the two repeated pairs just described).

## Short proof without enumeration

For each tritangent there are exactly four allowed sign patterns, uniform subject to the product of three signs equaling s_ijk. The mean of any nonempty proper subset of those signs is zero, whereas the mean of their triple product equals s_ijk.

Therefore degree-one moments vanish. In degree two the off-diagonal moments cancel; the five lines through each vertex each contribute four diagonal units, yielding 20I27. In degree three only products of all three distinct coordinates on a single tritangent survive, each weighted 4s_ijk. Upon contracting with x tensor x tensor x, all six permutations contribute, giving 6*4=24 times N(x). In degree four, only a single coordinate to the fourth power or two distinct squared coordinates survive: the first occurs on five lines (20 terms), the second on the unique shared tritangent (4 terms). Contracting the fourth tensor supplies six permutations of each two-pair monomial, hence 24 times the edge sum. These arguments prove the formulas for all real x, not merely the tested integer samples.

**Exact producer:** analysis/toe_20261114_E6_180charge_cubic_cubature.py
**Machine-readable certificate:** data/toe_20261114_E6_180charge_cubic_cubature.json
**Regression:** tests/test_toe_20261114_E6_180charge_cubic_cubature.py

The producer performs complete integer moment-tensor enumeration (not floating-point fitting) and independently checks all four polynomial contractions on 40 random integer vectors.

## A nested two-layer design in the repo

The prior [twistor result](2026-11-14_E6_stabilizer_twistor_qubit_2design.md) proves that the 1,080 three-qubit stabilizer projectors map six-to-one onto these 180 charge vectors. Within each quaternionic CP1 fiber the six projectors form a **complex projective 2-design**, while the 180 projected charges form a **spherical 2-design** whose third moment reconstructs the exceptional cubic and whose fourth moment reconstructs Schlaefli adjacency.

This is a two-level finite ensemble with different moment geometry on its fiber and base. It suggests exact sampling methods for charge-polynomial observables and an explicit way to measure how a putative physical operation departs from preserving N. However, spherical and complex projective designs are different objects; their respective strengths should not be conflated, and neither identity produces spacetime dynamics, a physical vacuum or quantum gravity.

## Priority and falsifiers

The 45-term cubic, 180 minimal positive charges, and the Schlaefli graph are established in the existing repo and classical finite geometry. The exact moment-cubature formula and its nested-design interpretation are new deductions in this pass; external literature novelty has not been established. This is an exact finite mathematical theorem for the chosen signed canonical basis, not evidence for a TOE.

A falsifier would be any signed cubic monomial that is missing from the third-moment tensor, any spurious nonzero third-order monomial, or any off-graph mixed fourth moment; all are excluded by full enumeration. A further useful test is whether the 180 quaternionic base points satisfy higher-order **quaternionic projective** design identities, which cannot be inferred solely from their spherical 2-design property.
