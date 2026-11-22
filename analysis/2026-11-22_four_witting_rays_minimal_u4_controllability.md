# Minimal Witting four-mode controllability theorem

**2026-11-22.** New finite-dimensional control certificate, independent of fixed-phase optical compilation. No scalable universal quantum computation or TOE claim.

Use the canonical 40-ray Witting enumeration of `analysis/toe_20261121_hermitian45_pauli_sic_bridge.py`. Let omega be a primitive cube root of unity and choose ray indices **5, 26, 33, 36** (zero-based), represented by

- v5 = (1,0,-1,-1)
- v26 = (1,-omega,0,omega^2)
- v33 = (1,0,-omega^2,-omega)
- v36 = (0,1,-omega^2,omega^2).

Every vector has norm squared 3. Let P_j = v_j v_j^dagger / 3. Each independent phase control is R_j(theta) = exp(i theta P_j) = I + (exp(i theta)-1)P_j.

**Exact theorem:** Lie_R(i P5, i P26, i P33, i P36) = u(4).

**Certificate:** Starting with the four unnormalized projectors, nested commutators create ranks **4, 8, 14, 16**. One fixed 16-word Lie witness has full rank modulo **7, 13, 19, 31, 37 and 43**, using roots of x^2+x+1 in each prime field. Nonzero modular determinant implies characteristic-zero independence in Q(omega); complexified closure is gl_4(C), so the compact skew-Hermitian real closure is u(4). The chosen four vectors span C^4, and their nonorthogonality graph is connected. A generator set of three or fewer rank-one projectors fixes a nonzero joint orthogonal subspace and cannot generate U(4). Thus **four is minimal under the rank-one control model**.

**Physical boundary:** independent, continuously tunable phase gates on single-photon four-mode rails yield arbitrary U(4) mode-unitary control under ideal assumptions. This is **not** a deterministic entangling gate between separate photons, a fault-tolerant scalable computer, a quantized gauge field, or a gravity derivation. Fixed-angle finite reflection groups do not imply the continuous-control theorem or vice versa.

**Repo predecessor:** `analysis/toe_20261122_witting_fourmode_switch_compiler.py` compiles *each* of the 40 fixed phase-pi reflections but does not compute the Lie closure of a minimal generator subset. Separate two-ququart OSR8 certificates are in `analysis/toe_20261122_witting_phase_schmidt_law.py`; they concern 16-dimensional bipartite unitaries, not this 4-dimensional single-photon U(4).

**Literature:** Lie algebra rank condition (https://link.springer.com/article/10.1140/epjqt/s40507-022-00138-x); universal interferometers (Clements et al., Optica 2016, https://ora.ox.ac.uk/objects/uuid:12001441-51c7-4bb7-913c-18a1c208ed2e); complex reflection group G32 and E6 (https://ems.press/journals/pm/articles/14297577).

**Independent execution:** the modular verifier passed over all six primes, and its four focused pytest controls passed 4/4. A reproducible four-file source/test/certificate/report bundle was generated this session. No local Windows checkout synchronization can be claimed because Desktop Commander reports its monthly usage limit reached.

**Next falsification:** Does a small **discrete** gate-angle set yield a dense subgroup of SU(4), or does it close into a finite exceptional complex reflection group? Requires exact group/density checks, not visual matching.
