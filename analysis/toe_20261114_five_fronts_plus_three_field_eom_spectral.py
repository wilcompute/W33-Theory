#!/usr/bin/env python3
"""Five independently checked TOE frontiers + three orthogonal falsifiers.

Strict epistemic contract: exact finite combinatorics/Einstein-Maxwell
equations where specified; otherwise explicitly identified toy controls.
No assertion of global F8 optimum, full KK stability, or emergent TOE.
"""
from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
import json
import math

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "toe_20261114_five_fronts_plus_three_field_eom_spectral.json"


def gf8_mul(a, b):
    result = 0
    while b:
        if b & 1:
            result ^= a
        b >>= 1
        a <<= 1
        if a & 8:
            a ^= 0b1011
    return result


def gf8_trace(a):
    x, trace = a, 0
    for _ in range(3):
        trace ^= x
        x = gf8_mul(x, x)
    return trace


def trace_dual_mask(a):
    return sum(gf8_trace(gf8_mul(a, 1 << bit)) << bit for bit in range(3))


def chirped_pauli(t, x, y):
    return (8 * x + y, 8 * trace_dual_mask(gf8_mul(t, y)) + trace_dual_mask(gf8_mul(t, x)))


def symplectic(a, b):
    u, z = a
    v, w = b
    return ((u & w).bit_count() + (v & z).bit_count()) % 2


def f8_two_copy_bell_spectral_barrier():
    """Recompute nine disjoint symplectic Lagrangians and full Bell spectrum."""
    import numpy as np
    generators = [[(0, 1 << i) for i in range(6)]]
    generators += [
        [chirped_pauli(t, 1 << i, 0) for i in range(3)]
        + [chirped_pauli(t, 0, 1 << i) for i in range(3)]
        for t in range(8)
    ]
    lines = []
    for gs in generators:
        line = set()
        for v in range(1, 64):
            u, z = 0, 0
            for i, (a, b) in enumerate(gs):
                if (v >> i) & 1:
                    u ^= a
                    z ^= b
            line.add((u, z))
        assert len(line) == 63
        assert all((u & z).bit_count() % 2 == 0 for u, z in line)
        assert all(symplectic(a, b) == 0 for a in gs for b in gs)
        lines.append(line)
    covered = set.union(*lines)
    assert len(covered) == 567
    assert sum(len(lines[i] & lines[j]) for i in range(9) for j in range(i + 1, 9)) == 0

    all_eigen, symmetric, antisymmetric = Counter(), Counter(), Counter()
    for a in range(64):
        for b in range(64):
            r = sum(
                all((((a & z).bit_count() + (b & u).bit_count()) % 2) == 0 for u, z in gs)
                for gs in generators
            )
            eig = 64 * r - 9
            all_eigen[eig] += 1
            (symmetric if ((a & b).bit_count() % 2 == 0) else antisymmetric)[eig] += 1
            assert r == (9 if (a, b) == (0, 0) else 1 if (a, b) in covered else 0)

    assert all_eigen == Counter({567: 1, 55: 567, -9: 3528})
    assert symmetric == Counter({567: 1, 55: 567, -9: 1512})
    assert antisymmetric == Counter({-9: 2016})

    rng = np.random.default_rng(111426)
    amp = rng.standard_normal(64) + 1j * rng.standard_normal(64)
    amp /= np.linalg.norm(amp)
    expectations = 0.0
    for u, z in covered:
        val = sum(
            np.conj(amp[x]) * (-1 if (z & (x ^ u)).bit_count() % 2 else 1) * amp[x ^ u]
            for x in range(64)
        )
        assert abs(val.imag) < 1e-12
        expectations += val.real**2
    xi = np.array([[1 - 2 * gf8_trace(gf8_mul(a, b)) for b in range(8)] for a in range(8)])
    phi = np.array([
        [[1 - 2 * gf8_trace(gf8_mul(t, gf8_mul(a, b))) for b in range(8)] for a in range(8)]
        for t in range(8)
    ])
    A = amp.reshape(8, 8)
    transformed = np.einsum("ka,tab,bl->tkl", xi, A[None] * phi, xi, optimize=True) / 8
    independent_fourth = 64 * (sum(abs(v)**4 for v in amp)
                              + float(np.sum(abs(transformed)**4)) - Q(9, 64))
    assert abs(expectations - independent_fourth) < 1e-10
    return {
        "status": "EXACT_BELL_SPECTRUM_AND_RELAXATION_OBSTRUCTION",
        "n_bases": 9, "Paulis_per_basis_nonidentity": 63, "covered_Paulis": 567,
        "full_K_spectrum": {"567": 1, "55": 567, "-9": 3528},
        "symmetric_two_copy_spectrum": {"567": 1, "55": 567, "-9": 1512},
        "antisymmetric_two_copy_spectrum": {"-9": 2016},
        "independent_numeric_CZ_vs_Pauli_absolute_difference": abs(expectations - independent_fourth),
        "convex_mixed_state_relaxation_min": 0,
        "note": "min eig(K|Sym2)=-9 cannot bound pure-product minimum near 2.4985. Rank-one/product or PPT-type constraints remain essential.",
    }


def nine_dimensional_einstein_maxwell_full_equations():
    """Exact AdS5 x S2 x S2 solution in D9 Einstein-Maxwell, all EOM."""
    D, d = 9, 5
    # Convention S = integral sqrt(-g) (R - F_MN F^MN/4).
    f2 = Q(14, 5)
    F_squared = 4 * f2  # two independent round-sphere components
    ext_ricci = -F_squared / (4 * (D - 2))
    int_ricci = f2 / 2 - F_squared / (4 * (D - 2))
    total_R = d * ext_ricci + 4 * int_ricci
    trace_R = Q(D - 4, 4 * (D - 2)) * F_squared
    assert ext_ricci == Q(-2, 5)
    assert int_ricci == 1
    assert total_R == trace_R == 2
    ads_radius2 = Q(d - 1, 1) / (-ext_ricci)
    assert ads_radius2 == 10
    A, B = Q(7, 5), Q(2, 1)
    V0 = 2 * A - 2 * B
    du = -Q(20, 3) * 2*A + Q(14, 3) * 2*B
    dv = Q(0)
    huu = Q(20, 3)**2 * 2*A - Q(14, 3)**2 * 2*B
    hvv = 4**2 * 2*A - 2**2 * 2*B
    assert (V0, du, dv, huu, hvv) == (Q(-6,5), Q(0), Q(0), Q(112,3), Q(144,5))
    assert ext_ricci == V0 / (d - 2)
    # Maxwell/Bianchi: F=f(vol_S2a+vol_S2b) with constant f.
    # Each sphere volume form is closed and co-closed on the product.
    return {
        "status": "EXACT_FULL_BACKGROUND_EINSTEIN_MAXWELL_EOM",
        "action": "D9 integral sqrt(-g)(R-F_MN F^MN/4)",
        "background": "AdS5 x S2 x S2, sphere radii 1, fixed magnetic flux magnitude sqrt(14/5) on each sphere",
        "flux_component_squared": str(f2), "F_MN_F_MN": str(F_squared),
        "external_Ricci_tensor_coefficient": str(ext_ricci),
        "internal_Ricci_tensor_coefficient_each_sphere": str(int_ricci),
        "scalar_curvature_9D": str(total_R), "AdS5_radius_squared": str(ads_radius2),
        "effective_potential_stationary_value": str(V0),
        "homogeneous_two_radion_Hessian": [[str(huu), "0"], ["0", str(hvv)]],
        "Maxwell_dF_and_dstarF": "both zero for constant sums of product-sphere volume forms",
        "limitations": "Not E6 ExFT or full KK nonhomogeneous stability; flux quantization needs specified gauge coupling/charges; not cosmologically realistic de Sitter."
    }


def microscopic_coin_quantum_clock():
    """Exactly local/unitary 1D two-component QCA and dispersion controls."""
    import numpy as np
    theta, N = 0.17, 101
    co, si = math.cos(theta), math.sin(theta)
    coin = np.array([[co, -1j*si],[-1j*si, co]], complex)
    assert np.allclose(coin.conj().T @ coin, np.eye(2))
    max_error = 0
    max_speed = 0
    for k in np.linspace(-math.pi, math.pi, 51):
        U = np.diag([np.exp(1j*k), np.exp(-1j*k)]) @ coin
        assert np.allclose(U.conj().T @ U, np.eye(2))
        assert abs(np.linalg.det(U) - 1) < 1e-12
        max_error = max(max_error, abs(np.trace(U).real/2 - co*math.cos(k)))
        speed = abs(co*math.sin(k)) / math.sqrt(1 - (co*math.cos(k))**2)
        max_speed = max(max_speed, speed)
        assert speed <= abs(co) + 1e-12
    psi = np.zeros((N,2), complex)
    psi[0, 0] = 1
    for tick in range(1, 12):
        mixed = psi @ coin.T
        psi = np.stack((np.roll(mixed[:,0],1), np.roll(mixed[:,1],-1)), axis=1)
        support = np.flatnonzero(np.linalg.norm(psi,axis=1)>1e-12)
        assert all(min(x,N-x) <= tick for x in support)
        assert abs(np.sum(abs(psi)**2) - 1) < 1e-12
    for tick in range(11, 0, -1):
        psi = np.stack((np.roll(psi[:,0],-1),np.roll(psi[:,1],1)),axis=1) @ coin.conj()
    assert abs(psi[0,0]-1)<1e-12 and np.linalg.norm(psi[1:])<1e-12
    return {
        "status": "FINITE_SPEED_REVERSIBLE_LOCAL_UNITARY_QCA",
        "coin_angle_radians": theta, "checked_ticks": 11,
        "dispersion_exact": "cos(omega(k))=cos(theta)cos(k)",
        "group_speed_bound_sites_per_tick": "|v| <= |cos(theta)| <= 1",
        "max_observed_group_speed": max_speed, "max_dispersion_trace_error": max_error,
        "continuum": "omega~sqrt(k^2+theta^2), for small k,theta; requires external length and time scales",
        "limitations": "Known quantum-walk dynamics, not derived from W33 geometry, ExFT, or 120 native Clifford ticks."
    }


def intrinsic_edge_subdivision_continuum_guard():
    """Intrinsic W33 edge subdivision: local weak limit infinite path, ds->1."""
    from scipy.special import i0e, i1e
    data = []
    for L in (2,4,8,16,32,64,128,256):
        v = 40 + 240*(L-1)
        mu2 = Q(120*L-200, v)
        # Two-edge contribution 2*E/(12*2) + interior (L-2)*E/4
        assert mu2 == Q(2, v)*(Q(2*240,12*2)+Q(240*(L-2),4))
        data.append({
            "segments_per_original_edge": L, "vertices": v,
            "normalized_adjacency_second_moment": str(mu2),
            "numerical_mu2": float(mu2),
            "distance4_branch_neighborhood_fraction_upper": min(1, (40 + 2*240*4)/v)
        })
    assert data[-1]["numerical_mu2"] > Q(49,100)
    limiting = {}
    for t in (1,3,10,100):
        H = float(i0e(t))
        ds = float(2*t*(1-i1e(t)/i0e(t)))
        limiting[str(t)] = {"heat_return":H,"spectral_dimension":ds}
    assert abs(limiting["100"]["spectral_dimension"] - 1) < .01
    return {
        "status": "EXACT_LOCAL_WEAK_LIMIT_ONE_DIMENSION",
        "base_graph": "W33 40-vertex 12-regular collinearity graph, 240 edges",
        "subdivided_vertex_count": "40+240(L-1)",
        "exact_second_moment": "(120L-200)/(240L-200) -> 1/2",
        "even_limiting_moments": "binomial(2k,k)/4^k, odd moments 0",
        "limiting_heat_trace": "exp(-t)*I0(t)",
        "limiting_spectral_dimension": "2t*(1-I1(t)/I0(t)) -> 1 for t >>1",
        "order_of_limits": "First L->infinity at fixed diffusion t, then large t; not interchangeable without bounds",
        "counts":data, "limit_values":limiting,
        "limitations": "No Lorentzian metric, gravity, or intrinsic 4D diffusion; 1D geometry results from graph edge refinement."
    }


def single_photon_four_logical_qubits():
    """Exactly unitary one-photon 16-rail logical circuit and exponential resources."""
    import numpy as np
    n=4; dim=1<<n
    H=np.eye(dim,dtype=complex)
    for j in range(dim):
        if j&1: continue
        H[j,j]=H[j,j^1]=H[j^1,j]=1/math.sqrt(2)
        H[j^1,j^1]=-1/math.sqrt(2)
    assert np.allclose(H.conj().T@H,np.eye(dim))
    def cnot(control,target):
        U=np.zeros((dim,dim),complex)
        for j in range(dim):
            k=j ^ ((1<<target) if j&(1<<control) else 0)
            U[k,j]=1
        assert np.allclose(U.conj().T@U,np.eye(dim))
        return U
    psi=np.zeros(dim,complex);psi[0]=1
    psi=H@psi
    for target in (1,2,3):
        psi=cnot(0,target)@psi
    assert np.allclose(psi[0],1/math.sqrt(2)) and np.allclose(psi[-1],1/math.sqrt(2))
    assert np.linalg.norm(psi[1:-1]) < 1e-12
    # Exactly 2^(n-1) independently coupled pairs for logical H,
    # and 2^(n-2) swaps for any controlled bit flip.
    resources=[{"logical_qubits":j,"orthogonal_modes":2**j,
                "one_qubit_H_disjoint_couplers":2**(j-1),
                "CNOT_transpositions":2**(j-2)} for j in range(2,13)]
    eta=.98; sigma=.1
    visibility=math.exp(-sigma*sigma)
    accepted=math.ceil(2*math.log(40)/(.05**2))  # Hoeffding for +-1 samples, 95%
    raw=math.ceil(accepted/(eta**4))
    assert resources[2]["orthogonal_modes"]==16 and resources[2]["one_qubit_H_disjoint_couplers"]==8
    return {
        "status":"EXACT_16_RAIL_GHZ_GATE_CIRCUIT_AND_SCALING_GUARD",
        "GHZ_state":"(|0000>+|1111>)/sqrt(2) for one photon across 16 orthogonal modes",
        "logical_H_requires_disjoint_50_50_couplers":8,
        "logical_CNOT_permutation_swap_pairs":4,
        "logical_CZ_mode_specific_pi_phase_shifts":4,
        "total_optical_mode_scaling":"M>=2^n to represent n independent logical qubits in one photon's M-dimensional one-particle space",
        "resource_table":resources,"per_element_survival":eta,"chosen_circuit_depth":4,
        "four_pass_success_probability":eta**4,
        "independent_Gaussian_mode_phase_sigma":sigma,
        "GHZ_X4_visibility_under_relative_phase_noise":visibility,
        "Hoeffding_accepted_shots_for_0p05_absolute_precision_95pct":accepted,
        "raw_shots_at_loss_only_survival":raw,
        "limitations":"Internal logical entanglement does not certify spacelike Bell nonlocality; exponential spatial/time modes prohibit polynomial mode scalability; Gaussian phase errors assumed, not measured."
    }


def flux_orientation_chirality_blind_spot():
    """Conjugate fluxes share ring energy spectrum yet reverse oriented current."""
    n, flux = 3, 2*math.pi/3
    energies=lambda phi: sorted(2*math.cos((2*math.pi*k+phi)/n) for k in range(n))
    a,b=energies(flux),energies(-flux)
    assert max(abs(x-y) for x,y in zip(a,b))<1e-12
    current=lambda phi:(2/n)*math.sin(phi/n)
    assert abs(current(flux)+current(-flux))<1e-12
    assert abs(current(flux)) > .2
    return {
        "status":"EXACT_TIME_REVERSAL_SPECTRAL_DEGENERACY",
        "ring_sites":n,"wilson_angle": "2*pi/3",
        "energies_at_plus_flux":a,"energies_at_minus_flux":b,
        "oriented_current_at_plus_flux_groundlabel_k0":current(flux),
        "oriented_current_at_minus_flux_groundlabel_k0":current(-flux),
        "limitation":"Minimal U(1) flux ring, not a proof of E6 chirality; spectroscopy without oriented current cannot select flux sign."
    }


def flux_topology_sector_obstruction():
    """Kunneth gives distinct cohomology/flux ranks of T4 versus S2xS2."""
    import math as m
    torus=[m.comb(4,k) for k in range(5)]
    spheres=[1,0,2,0,1]
    assert torus==[1,4,6,4,1] and spheres==[1,0,2,0,1]
    assert sum((-1)**k*x for k,x in enumerate(torus))==0
    assert sum((-1)**k*x for k,x in enumerate(spheres))==4
    return {
        "status":"EXACT_INEQUIVALENT_COHOMOLOGY_AND_FLUX_GRADING",
        "T4_Betti":torus,"S2xS2_Betti":spheres,
        "T4_three_form_independent_topological_fluxes":torus[3],
        "S2xS2_three_form_independent_topological_fluxes":spheres[3],
        "T4_two_form_flux_rank":torus[2],"S2xS2_two_form_flux_rank":spheres[2],
        "Euler_characteristics":{"T4":0,"S2xS2":4},
        "limitation":"This prohibits a topology-preserving identification; topology change/duality with further fields is not ruled out."
    }


def clock_dimensionful_speed_no_selection():
    """Same dimensionless unitary automaton admits arbitrary physical speed."""
    scales=[(Q(1),Q(1)),(Q(2),Q(1)),(Q(1),Q(3)),(Q(3),Q(7))]
    speeds=[a/dt for a,dt in scales]
    assert speeds==[Q(1),Q(2),Q(1,3),Q(3,7)]
    return {
        "status":"EXACT_DIMENSIONFUL_SPEED_UNDERDETERMINATION",
        "same_dimensionless_coin_angle":"0.17 radians","same_lattice_unitary":True,
        "physical_a_dt_and_max_hop_speed":[{"a":str(a),"delta_t":str(dt),"a_over_delta_t":str(c)} for (a,dt),c in zip(scales,speeds)],
        "limitation":"Absent an independent length/time anchor, a count-of-exchanges clock cannot derive c in SI units."
    }


FRONTS={
 "1_F8_lower_bound_spectral_relaxation":f8_two_copy_bell_spectral_barrier,
 "2_full_Einstein_Maxwell_compactification_background":nine_dimensional_einstein_maxwell_full_equations,
 "3_microscopic_unitary_clock":microscopic_coin_quantum_clock,
 "4_intrinsic_W33_edge_refinement":intrinsic_edge_subdivision_continuum_guard,
 "5_photonic_logical_gate_resource_experiment":single_photon_four_logical_qubits,
 "extra_6_gauge_chirality_spectral_blind_spot":flux_orientation_chirality_blind_spot,
 "extra_7_topological_flux_sector_guard":flux_topology_sector_obstruction,
 "extra_8_clock_speed_dimensional_underdetermination":clock_dimensionful_speed_no_selection,
}


def run_all():
    values={}
    for title,fn in FRONTS.items():
        values[title]=fn()
        print("PASS",title,values[title]["status"],flush=True)
    ans={"status":"PASS_EIGHT_INDEPENDENT_CONDITIONAL_CONTROLS","n_fronts":len(values),
         "boundary":"No TOE solution, globally certified F8 optimum, complete KK stability, native W33 continuum, or scalable one-photon BQP.",
         "results":values}
    OUTPUT.parent.mkdir(parents=True,exist_ok=True)
    OUTPUT.write_text(json.dumps(ans,indent=2)+"\n",encoding="utf-8")
    return ans


if __name__=="__main__":run_all()
