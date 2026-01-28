# W33 Edge Projections as Root-Like System

## Setup

- W33 edges: 240
- λ=2 eigenspace dimension: 24

## Edge Projection Properties

- Common norm: 1.183216
- Norm variance: 0.0000000000

### Inner Product Values (normalized)

- ⟨ê_i, ê_j⟩ = -0.190476: 10800 pairs (i≠j)
- ⟨ê_i, ê_j⟩ = -0.071429: 25920 pairs (i≠j)
- ⟨ê_i, ê_j⟩ = 0.047619: 15120 pairs (i≠j)
- ⟨ê_i, ê_j⟩ = 0.285714: 240 pairs (i≠j)
- ⟨ê_i, ê_j⟩ = 0.523810: 4320 pairs (i≠j)
- ⟨ê_i, ê_j⟩ = 0.642857: 960 pairs (i≠j)
- ⟨ê_i, ê_j⟩ = 1.000000: 0 pairs (i≠j)

## Comparison to E8 Root System

### E8 Inner Product Values (normalized)

- ⟨r_i, r_j⟩ = -1.000000: 240 pairs (i≠j)
- ⟨r_i, r_j⟩ = -0.500000: 13440 pairs (i≠j)
- ⟨r_i, r_j⟩ = -0.000000: 30240 pairs (i≠j)
- ⟨r_i, r_j⟩ = 0.500000: 13440 pairs (i≠j)
- ⟨r_i, r_j⟩ = 1.000000: 0 pairs (i≠j)

### Inner Product Comparison

| W33 Edge IP | Count | E8 Root IP | Count |
|-------------|-------|------------|-------|
| -0.1905 | 10800 | -1.0000 | 240 |
| -0.0714 | 25920 | -0.5000 | 13440 |
| 0.0476 | 15120 | -0.0000 | 30240 |
| 0.2857 | 240 | 0.5000 | 13440 |
| 0.5238 | 4320 | - | - |
| 0.6429 | 960 | - | - |

## Root System Properties Check

### 1. Equal Length
- All 240 vectors have norm 1.183216 ✓

### 2. Integrality Check (2⟨α,β⟩)

- Max deviation from integer: 0.428572
- ✗ Not all 2⟨α,β⟩ are integers

### 3. Closure Under Reflection

- Samples checked: 1225
- Closure violations: 1225
- ✗ 1225 reflection not in set

## Adjacency Structure of Edge Projections

- Edge graph degree: 22
- Edge graph total edges: 2640

### Comparison to E8

| Property | W33 Edge Graph | E8 Root Graph |
|----------|----------------|---------------|
| Degree | 22 | 112 |
| Total edges | 2640 | 13440 |

## Inner Product vs Graph Adjacency

### Adjacent edge-pairs (share a W33 vertex):
- IP = 0.5238: 2160
- IP = 0.6429: 480

### Non-adjacent edge-pairs:
- IP = -0.1905: 5400
- IP = -0.0714: 12960
- IP = 0.0476: 7560
- IP = 0.2857: 120

## Antipodal Structure

- Antipodal pairs (IP ≈ -1): 0
- Expected for root system: 120 (= 240/2)

## Summary

### Structural Parallel

| Property | W33 Edge System | E8 Root System |
|----------|-----------------|----------------|
| Vectors | 240 | 240 |
| Equal norm | ✓ | ✓ |
| Dimension | 24 | 8 |
| IP values | 6 distinct | 4 distinct |
| Antipodal pairs | 0 | 120 |

No antipodal structure - the system lacks ±root symmetry
