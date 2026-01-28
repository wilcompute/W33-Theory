# Pancharatnam Phase Protocol (π/6, π/2) for Witting Rays

This protocol measures the geometric phase for a 3‑ray loop:

Φ = arg(⟨a|b⟩⟨b|c⟩⟨c|a⟩)

The Witting set exhibits phase quantization at ±π/6 and ±π/2.

## Target phase +pi/6
Ray indices: (0, 5, 9)

### Ray vectors (C^4)
- r0 = e0 = [(1+0j), 0j, 0j, 0j]
- r5 = (1,0,-w^0,-w^0)/sqrt3 = [(0.5773502691896258+0j), 0j, (-0.5773502691896258+0j), (-0.5773502691896258+0j)]
- r9 = (1,0,-w^0,-w^1)/sqrt3 = [(0.5773502691896258+0j), 0j, (-0.5773502691896258+0j), (0.2886751345948128-0.5000000000000001j)]

### Interferometric loop (conceptual)
1. Prepare |a⟩ = r_i.
2. Interfere |a⟩ with |b⟩ to extract arg⟨a|b⟩.
3. Interfere |b⟩ with |c⟩ to extract arg⟨b|c⟩.
4. Interfere |c⟩ with |a⟩ to extract arg⟨c|a⟩.
5. Sum phases to obtain Φ.

Expected phase: **0.523599 rad**

## Target phase -pi/6
Ray indices: (0, 5, 10)

### Ray vectors (C^4)
- r0 = e0 = [(1+0j), 0j, 0j, 0j]
- r5 = (1,0,-w^0,-w^0)/sqrt3 = [(0.5773502691896258+0j), 0j, (-0.5773502691896258+0j), (-0.5773502691896258+0j)]
- r10 = (1,-w^0,0,w^1)/sqrt3 = [(0.5773502691896258+0j), (-0.5773502691896258+0j), 0j, (-0.2886751345948128+0.5000000000000001j)]

### Interferometric loop (conceptual)
1. Prepare |a⟩ = r_i.
2. Interfere |a⟩ with |b⟩ to extract arg⟨a|b⟩.
3. Interfere |b⟩ with |c⟩ to extract arg⟨b|c⟩.
4. Interfere |c⟩ with |a⟩ to extract arg⟨c|a⟩.
5. Sum phases to obtain Φ.

Expected phase: **-0.523599 rad**

## Target phase +pi/2
Ray indices: (0, 5, 21)

### Ray vectors (C^4)
- r0 = e0 = [(1+0j), 0j, 0j, 0j]
- r5 = (1,0,-w^0,-w^0)/sqrt3 = [(0.5773502691896258+0j), 0j, (-0.5773502691896258+0j), (-0.5773502691896258+0j)]
- r21 = (1,0,-w^1,-w^1)/sqrt3 = [(0.5773502691896258+0j), 0j, (0.2886751345948128-0.5000000000000001j), (0.2886751345948128-0.5000000000000001j)]

### Interferometric loop (conceptual)
1. Prepare |a⟩ = r_i.
2. Interfere |a⟩ with |b⟩ to extract arg⟨a|b⟩.
3. Interfere |b⟩ with |c⟩ to extract arg⟨b|c⟩.
4. Interfere |c⟩ with |a⟩ to extract arg⟨c|a⟩.
5. Sum phases to obtain Φ.

Expected phase: **1.570796 rad**

## Target phase -pi/2
Ray indices: (0, 5, 37)

### Ray vectors (C^4)
- r0 = e0 = [(1+0j), 0j, 0j, 0j]
- r5 = (1,0,-w^0,-w^0)/sqrt3 = [(0.5773502691896258+0j), 0j, (-0.5773502691896258+0j), (-0.5773502691896258+0j)]
- r37 = (1,0,-w^2,-w^2)/sqrt3 = [(0.5773502691896258+0j), 0j, (0.2886751345948131+0.4999999999999999j), (0.2886751345948131+0.4999999999999999j)]

### Interferometric loop (conceptual)
1. Prepare |a⟩ = r_i.
2. Interfere |a⟩ with |b⟩ to extract arg⟨a|b⟩.
3. Interfere |b⟩ with |c⟩ to extract arg⟨b|c⟩.
4. Interfere |c⟩ with |a⟩ to extract arg⟨c|a⟩.
5. Sum phases to obtain Φ.

Expected phase: **-1.570796 rad**

## Notes
- Use any standard Pancharatnam/Berry phase interferometer.
- Phase quantization at ±π/6 and ±π/2 is the observed discrete signature.
- This is state‑preparation independent (depends only on ray overlaps).
