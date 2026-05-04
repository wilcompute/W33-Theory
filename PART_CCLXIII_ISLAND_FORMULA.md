# PART CCLXIII: Island Formula and Black Hole Entropy

## Overview

This part connects quantum information theory's island formula to W(3,3) through:

1. **Black hole entropy**: Bekenstein-Hawking formula and quantum corrections
2. **Page curve**: Entanglement entropy evolution during Hawking evaporation
3. **Islands**: Quantum extremal surfaces and AdS/CFT correspondence
4. **Ryu-Takayanagi formula**: Holographic entanglement entropy

## Black Hole Entropy and the Island Formula

### Bekenstein-Hawking Entropy

The entropy of a black hole:
$$S_{\text{BH}} = \frac{k_B A}{4 l_p^2} = \frac{k_B c^3}{4 G \hbar} A$$

where:

- $A$ is the event horizon area
- $l_p$ is the Planck length
- The coefficient $1/4$ is universal across all black holes

### Information Paradox

Hawking evaporation creates a paradox:

- **Early time**: Radiation appears thermal (no information)
- **Late time**: Black hole evaporates completely
- **Question**: Where is the information?

### Island Formula Resolution

The entropy formula incorporating quantum islands:
$$S(R) = \text{min}_{\text{islands } I} \left[ \frac{\text{Area}(\partial I)}{4} + S_{\text{vN}}(R \cup I) \right]$$

where:

- $R$ is the radiation region
- $I$ are quantum extremal surfaces (islands)
- First term: geometric contribution
- Second term: entanglement entropy

## Ryu-Takayanagi Formula

### AdS/CFT Correspondence

In the holographic duality, entanglement entropy of boundary region $A$ is:
$$S(A) = \frac{\text{Area}(\gamma_A)}{4 G_N}$$

where $\gamma_A$ is the **minimal surface** in the bulk AdS space with boundary $\partial A$.

### Extremal Surface Generalization

For time-dependent geometries:
$$S(A) = \text{min}_{\gamma: \partial\gamma = \partial A} \text{Area}(\gamma)$$

The extremal surface need not be connected to the boundary.

### Islands in AdS

When islands appear, the entanglement entropy formula becomes:
$$S(A) = \frac{\text{Area}(\gamma_{A \cup I})}{4 G_N}$$

The island $I$ contributes to the minimal surface calculation.

## W(3,3) and Holographic Structure

### Ground State Degeneracy on Torus

For a topological system on a genus-1 surface (torus):
$$\text{GSD}_{\text{torus}} = Q^{\lambda} = 3^2 = 9$$

where:

- $Q = 3$: number of topological sectors
- $\lambda = 2$: number of independent non-contractible cycles on torus

### Central Charge

The conformal central charge encodes topological order:
$$c = \ln(\text{GSD}) = \ln(9) \approx 2.2$$

For W(3,3) structure, this corresponds to a **non-chiral CFT** with modest anomalous dimension.

### K3 Surface Connection

The K3 surface has Hodge diamond:
$$\begin{array}{ccccc}
  &  & 1 &  &  \\
  & 0 &  & 0 &  \\
20 &  & 24 &  & 20 \\
  & 0 &  & 0 &  \\
  &  & 1 &  &
\end{array}$$

with central charge:
$$c_{\text{K3}} = 24$$

The relationship to W(3,3): $24 = f$ (number of faces in genus-2 JR resolution).

## Page Curve and Entanglement Entropy

### Page Curve Definition
The entanglement entropy between Hawking radiation and black hole:
$$S_{\text{Page}}(t) = \begin{cases}
S_0 \ln(t/t_1) & t \ll t_{\text{evap}} \text{ (linear growth)}\\
S_0(1 - t/t_{\text{evap}}) & t \gg t_{\text{evap}} \text{ (decrease to 0)}
\end{cases}$$

### Island Phase Transition
At the critical time when islands appear:
$$t_{\text{crit}} = \frac{M_{\text{BH}} t_P}{M_P}$$

there is a **first-order phase transition** in the minimal surface geometry.

Before islands: $S(R) = S_{\text{thermal}}$ (increasing)
After islands: $S(R) = S_{\text{island}}$ (decreasing)

### W(3,3) Analog
For W(3,3) on a genus-2 surface:
- Number of independent surfaces: related to $f = 24$ faces
- Extremal surfaces: multiple candidates with comparable area
- Entropy dominance: whichever island minimizes total area

## Extremal Surfaces on Higher Genus

### Genus 1 (Torus)
Minimal surface winding around torus:
- **Handles**: 1 non-contractible cycle
- **Genus of surface**: $g = 1$
- **Self-intersection number**: determines uniqueness

### Genus 2 Extremal Surfaces
The JR resolution creates genus-2 surfaces with:
- **Possible islands**: $2g = 4$ independent non-contractible cycles
- **Extremal candidates**: multiple minimal surfaces to compare
- **Entropy formula**: select surface with minimal area

For W(3,3) with $f = 24$ faces:
- Triangulation creates natural extremal surfaces
- Duality between bulk surfaces and boundary regions
- Islands emerge from topological structure

## Black Hole Interior and W(3,3)

### Effective Description
The black hole interior degrees of freedom can be organized as:
- **Exterior**: radiation region $R$
- **Island**: interior region $I$
- **Relation**: connected through entanglement island

### Boundary Condition
The island formula implies:
$$\rho_{R \cup I} = \prod_{\text{edge}} \text{SWAP}(\text{island})$$

where the SWAP operators create entanglement between interior and exterior.

For W(3,3) structure: $k = 12$ independent edges per vertex enable rich island structure.

## Quantum Extremal Surfaces

### Definition
A surface $\gamma$ is **quantum extremal** if:
$$\delta_\perp \text{Area}(\gamma) + \delta_\perp S_{\text{vN}}(A \cup \gamma) = 0$$

(first variation vanishes in normal direction)

### W(3,3) Extremal Surfaces
The W(3,3) graph encodes extremal surfaces via:
- Vertices: 40 possible configurations
- Edges: 240 potential boundary locations
- Faces: 24 natural regions (genus-2 structure)

Extremal condition determines which regions are "islands".

## References
- Penington, D. (2020). Entanglement wedges of radiation in the black hole interior.
- Almheiri, A., et al. (2020). The entropy of bulk quantum fields and the entanglement wedge of an evaporating black hole.
- Ryu, S., & Takayanagi, T. (2006). Holographic derivation of entanglement entropy from AdS/CFT.
