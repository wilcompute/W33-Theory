#!/usr/bin/env python3
"""Independent, standard-library-only reproducer for eight TOE model controls.

Exact arithmetic for F8 Pauli combinatorics, the D9 Einstein-Maxwell background,
W33 edge-refinement moments, cohomology and dimensional scaling; idealized
finite numerical checks for a quantum walk, single-photon rails and flux ring.

NOT a global F8 minimum proof, E6 ExFT compactification, full KK stability,
native 4D spacetime, or polynomial-resource BQP.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import product
from math import comb, cos, sin, pi, sqrt, exp, ceil, log
import json
from pathlib import Path


def mul(a, b):
    out = 0
    while b:
        if b & 1:
            out ^= a
        b >>= 1
        a <<= 1
        if a & 8:
            a ^= 0b1011
    return out


def trace(a):
    value, out = a, 0
    for _ in range(3):
        out ^= value
        value = mul(value, value)
    return out


def dual_mask(a):
    return sum(trace(mul(a, 1 << i)) << i for i in range(3))


def pauli_label(t, x, y):
    return 8*x+y, 8*dual_mask(mul(t, y))+dual_mask(mul(t, x))


def f8_two_copy_spectrum():
    generators = [[(0, 1 << i) for i in range(6)]]
    for t in range(8):
        generators.append([pauli_label(t, 1 << i, 0) for i in range(3)]
                          + [pauli_label(t, 0, 1 << i) for i in range(3)])
    groups = []
    for gs in generators:
        group = set()
        for mask in range(1, 64):
            a = b = 0
            for i, (u, v) in enumerate(gs):
                if mask & (1 << i):
                    a ^= u
                    b ^= v
            group.add((a, b))
        assert len(group) == 63
        assert all(((u & v).bit_count() & 1) == 0 for u, v in group)
        groups.append(group)
    cover = set.union(*groups)
    assert len(cover) == 567 and sum(len(groups[i] & groups[j])
                                    for i in range(9) for j in range(i+1, 9)) == 0

    full, symmetric, antisymmetric = Counter(), Counter(), Counter()
    for a, b in product(range(64), repeat=2):
        r = sum(all((((a & z).bit_count() + (b & u).bit_count()) & 1) == 0
                    for u, z in gs) for gs in generators)
        assert r == (9 if (a,b) == (0,0) else 1 if (a,b) in cover else 0)
        eig = 64*r - 9
        full[eig] += 1
        (symmetric if not ((a & b).bit_count() & 1) else antisymmetric)[eig] += 1

    assert full == {567:1, 55:567, -9:3528}
    assert symmetric == {567:1, 55:567, -9:1512}
    assert antisymmetric == {-9:2016}
    return {"status": "EXACT", "covered_Pauli_labels": 567,
            "full_Bell_spectrum": dict(full),
            "symmetric_Bell_spectrum": dict(symmetric),
            "antisymmetric_Bell_spectrum": dict(antisymmetric),
            "naive_symmetric_spectral_lower_bound": -9,
            "mixed_density_matrix_relaxation_lower_bound": 0,
            "warning": "Neither relaxed bound proves the positive F8 pure-state optimum."}


def einstein_maxwell_ads5_s2_s2():
    d, D, flux_sq = 5, 9, F(14, 5)
    f2 = 4*flux_sq
    external = -f2 / (4*(D-2))
    internal = flux_sq/2 + external
    scalar = d*external + 4*internal
    assert (external, internal, scalar) == (F(-2,5), F(1), F(2))
    assert scalar == F(D-4, 4*(D-2))*f2
    A, B = F(7,5), F(2)
    V = 2*A-2*B
    grad_u = -F(20,3)*2*A + F(14,3)*2*B
    huu = F(20,3)**2*2*A - F(14,3)**2*2*B
    hvv = 16*2*A - 4*2*B
    assert (V, grad_u, huu, hvv) == (F(-6,5), F(0), F(112,3), F(144,5))
    assert external == V/(d-2)
    return {"status":"EXACT_BACKGROUND_EOM",
            "action":"integral sqrt(-g)(R-F^2/4), D=9",
            "geometry":"AdS5 x S2 x S2, both spheres unit radius",
            "magnetic_f_squared":str(flux_sq), "F_squared":str(f2),
            "Ricci_external":str(external), "Ricci_internal":str(internal),
            "AdS_radius_squared":"10", "nine_D_scalar_curvature":str(scalar),
            "V_at_critical":str(V), "homogeneous_radion_Hessian":[str(huu),str(hvv)],
            "Maxwell_equations":"dF=d*F=0 for constant sphere-volume-form flux",
            "warning":"Not the E6 ExFT theory; nonhomogeneous KK spectrum and quantization require further checks."}


def reversible_two_component_clock():
    N, ticks, theta = 31, 9, 0.17
    ct, st = cos(theta), sin(theta)
    p = [[0j,0j] for _ in range(N)]
    p[0][0] = 1+0j
    for t in range(1, ticks+1):
        q = [[0j,0j] for _ in range(N)]
        for x,(a,b) in enumerate(p):
            q[(x+1)%N][0] = ct*a-1j*st*b
            q[(x-1)%N][1] = -1j*st*a+ct*b
        p = q
        assert abs(sum(abs(x)**2 for pair in p for x in pair)-1)<1e-12
        assert all(min(x, N-x) <= t for x in range(N)
                   if abs(p[x][0])+abs(p[x][1]) > 1e-12)
    for _ in range(ticks):
        q = [[0j,0j] for _ in range(N)]
        for x in range(N):
            a, b = p[(x+1)%N][0], p[(x-1)%N][1]
            q[x] = [ct*a+1j*st*b, 1j*st*a+ct*b]
        p = q
    assert abs(p[0][0]-1)<1e-12 and sum(abs(x)**2 for pair in p[1:] for x in pair)<1e-20
    return {"status":"UNITARY_LOCAL_REVERSIBLE", "site_count":N,
            "ticks_verified":ticks, "coin_angle":theta,
            "dispersion":"cos(omega)=cos(theta)cos(k)",
            "group_speed_bound":"|d omega/dk| <= |cos(theta)| <= 1",
            "warning":"External lattice spacing/tick duration and quantum-walk dynamics assumed."}


def subdivided_w33_limit():
    records=[]
    for L in (2,4,8,16,64,256):
        n=40+240*(L-1)
        mu2=F(120*L-200,n)
        assert mu2 == F(2,n)*(F(2*240,12*2)+F(240*(L-2),4))
        records.append({"path_length":L,"vertices":n,"second_moment":str(mu2)})
    assert F(120*256-200,40+240*255)>F(49,100)
    # The normalized local-root measure tends to the infinite path.
    # Its normalized-adjacency even moments are central binomial/4^k.
    assert [F(comb(2*k,k),4**k) for k in range(4)] == [F(1),F(1,2),F(3,8),F(5,16)]
    return {"status":"EXACT_LOCAL_WEAK_LIMIT",
            "refinement":"Uniformly subdivide each of W33's 240 collinearity edges",
            "vertex_formula":"40+240(L-1)",
            "normalized_second_moment":"(120L-200)/(240L-200) -> 1/2",
            "limit_heat_trace":"exp(-t) I0(t)", "limit_spectral_dimension":"1",
            "moments":records,
            "warning":"Sequential large-L and large-t limit; no native 4D or Lorentzian geometry."}


def photon_16_rail_ghz():
    N=16
    p=[0j]*N; p[0]=1+0j
    q=[0j]*N
    for j in range(0,N,2):
        q[j]=(p[j]+p[j+1])/sqrt(2)
        q[j+1]=(p[j]-p[j+1])/sqrt(2)
    p=q
    for bit in (1,2,3):
        q=[0j]*N
        for j in range(N):
            q[j ^ ((1<<bit) if j&1 else 0)] = p[j]
        p=q
    assert abs(p[0]-1/sqrt(2))<1e-12 and abs(p[-1]-1/sqrt(2))<1e-12
    assert all(abs(p[j])<1e-12 for j in range(1,15))
    accepted=ceil(2*log(40)/(.05**2))
    assert accepted==2952
    return {"status":"EXACT_IDEAL_LOGICAL_GHZ",
            "logical_qubits":4,"photon_modes":N,
            "H_disjoint_coupler_count":8,"each_CNOT_mode_swaps":4,
            "single_photon_mode_requirement":"M>=2^n",
            "X4_analyzer_additional_couplers":32,
            "phase_sigma":0.1,"ideal_X4_visibility":exp(-0.1**2),
            "accepted_events_Hoeffding_95pct_error_0p05":accepted,
            "preparation_only_raw_events_eta98":ceil(accepted/.98**4),
            "preparation_plus_X4_analyzer_raw_events_eta98":ceil(accepted/.98**8),
            "warning":"One-photon internal entanglement, not separated-photon Bell nonlocality or scalable BQP."}


def flux_chirality_blind_spot():
    phi=2*pi/3
    energies=lambda f: sorted(2*cos((2*pi*k+f)/3) for k in range(3))
    assert all(abs(x-y)<1e-12 for x,y in zip(energies(phi),energies(-phi)))
    current=lambda f: (2/3)*sin(f/3)
    assert abs(current(phi)+current(-phi))<1e-12
    return {"status":"EXACT_RING_TIME_REVERSAL",
            "isospectral_plus_minus_flux":True,
            "oriented_current_plus_flux":current(phi),
            "oriented_current_minus_flux":current(-phi),
            "warning":"Unoriented spectrum cannot determine chirality."}


def flux_topology_guard():
    torus=[comb(4,k) for k in range(5)]
    spheres=[1,0,2,0,1]
    assert (torus,spheres)==([1,4,6,4,1],[1,0,2,0,1])
    return {"status":"EXACT_KUNNETH",
            "T4_Betti":torus,"S2xS2_Betti":spheres,
            "third_form_ranks":[torus[3],spheres[3]],
            "Euler_characteristics":[0,4]}


def speed_of_light_units_guard():
    pairs=[(F(1),F(1)),(F(2),F(1)),(F(1),F(3)),(F(3),F(7))]
    speeds=[str(a/t) for a,t in pairs]
    assert speeds==["1","2","1/3","3/7"]
    return {"status":"EXACT_SCALE_UNDERDETERMINATION",
            "same_dimensionless_unitary":True,"possible_hop_speeds":speeds}


def main():
    checks={
        "F8_spectral_relaxation": f8_two_copy_spectrum(),
        "nine_dimensional_Einstein_Maxwell_background":einstein_maxwell_ads5_s2_s2(),
        "local_quantum_clock":reversible_two_component_clock(),
        "intrinsic_W33_refinement":subdivided_w33_limit(),
        "photonic_single_particle_GHZ":photon_16_rail_ghz(),
        "extra_chirality_ring":flux_chirality_blind_spot(),
        "extra_flux_topology":flux_topology_guard(),
        "extra_dimensional_speed":speed_of_light_units_guard()
    }
    assert len(checks)==8
    print(json.dumps({"status":"PASS_EIGHT_SPECIFIED_MODELS","checks":checks}, indent=2))
    return checks


if __name__=="__main__":
    main()
