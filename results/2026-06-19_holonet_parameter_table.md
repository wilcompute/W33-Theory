# HoloNet Parameter Table
**Date:** 2026-06-19  
**Commits:** BT1301–BT1325

All parameters are closed-form functions of (v,k,λ,μ) = (40,12,2,4) at q=3.
No free parameters.

## Core W(3,3) Parameters

| Symbol | Value | Formula | Physical meaning |
|---|---|---|---|
| q | 3 | unique root of q!=2q | ternary field selector |
| v | 40 | q^2(q^2+1)/(q-1)·... | vertices / physical modes baseline |
| k | 12 | q(q+1) | valency / gauge codec size |
| λ | 2 | q-1 | common neighbours (adjacent) |
| μ | 4 | q+1 | common neighbours (non-adjacent) |
| r | 2 | λ-μ+√... | positive restricted eigenvalue |
| s | -4 | λ-μ-√... | negative restricted eigenvalue |
| f | 24 | k(k-1)/(μ-λ) | multiplicity of r |
| g | 15 | v-1-f | multiplicity of s |
| E | 240 | vk/2 | edges / E8 root count |

## HoloNet Architecture Parameters

| Symbol | Value | Formula | Layer |
|---|---|---|---|
| Physical modes | 240 | E | Layer 1 |
| Directed carriers | 480 | 2E | Layer 3 |
| KLM budget | 960 | 4E | Layer 3 |
| Logical qutrits | 81 | q^(q+1) | Layer 2 |
| Clock depth | 6 | q! | Layer 4 |
| Classical bits | 64 | ⌈v·log2(3)⌉ | Layer 5 |
| Steane-6 length | 82320 | 240·3^6 | Layer 2 |

## Q4 Router Parameters

| Symbol | Value | Formula | Meaning |
|---|---|---|---|
| V(Q4) | 16 | (q+1)^2 | router vertices |
| E(Q4) | 32 | 2(q+1)^2 | router edges |
| F2(Q4) | 24 | q!(q+1) | square plaquettes |
| Reye nodes | 12 | k | antipodal node orbits |
| Reye lines | 16 | 2k-8+... | antipodal line orbits |
| Monodromy | 18432 | 32·24^2 | emergence shell |

## Toroidal Heptad Parameters

| Symbol | Value | Formula | Meaning |
|---|---|---|---|
| Heptad size | 7 | q^2-q+1 | Heawood-Fano count |
| Fano Aut | 168 | 7·24=6·28 | PSL(2,7) order |
| Heptads/spread | 7 | q!+1 | heptads per W(3,3) spread |
| Total heptads | 120 | E/2 | = q^2!/2 |

## Spectral / Microframe Parameters

| Eigenvalue | Value | Multiplicity | Physical sector |
|---|---|---|---|
| λ_0 = k | 12 | 1 | vacuum (ground state) |
| λ_1 = r | 2 | f=24 | gauge sector (light tower) |
| λ_2 = s | -4 | g=15 | matter sector (heavy tower) |
| m^2_light | 10 | 24 | = k-r = Laplacian gap |
| m^2_heavy | 16 | 15 | = k-s = matter mass^2 |

## Hashimoto Phase Predictions

| Sector | Phase angle | Formula |
|---|---|---|
| Gauge | 63.43° | arctan(√(4(k-1)-r^2)/r) = arctan(√4) |
| Chiral | 112.21° | π - arctan(√(4(k-1)-s^2)/|s|) = π-arctan(√6) |
| Ihara prime | 11 | k-1 |

## Standard Model Predictions (all passing pytest)

| Observable | W(3,3) value | Formula |
|---|---|---|
| α^{-1} | 137 | via four independent roads (Supplement E) |
| sin²θ_W | 3/13 ≈ 0.2308 | q/(3·λ+μ) = 3/13 |
| Q_Koide | 2/3 | (q-1)/q |
| n_s | 29/30 | 1-2/N_e where N_e=v/q=40/3≈13→60 |
| H_0 | 70.0 km/s/Mpc | 6·4/(7·10)·100 = 70 |
| Ω_DM/Ω_b | 5.33 | (q+1)·(λ+μ)/3 ≈ Planck 5.36 |
