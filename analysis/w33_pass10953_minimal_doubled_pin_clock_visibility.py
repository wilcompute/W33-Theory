#!/usr/bin/env python3
"""Pass 10953: minimal doubled Pin clock and trace-Choi visibility.

Pass 10952 showed that the determinant-odd Z8 tick is not a CP qutrit channel
but becomes unitary on H3 + conjugate(H3).  Here we prove that doubling is
minimal once the faithful qutrit Heisenberg sector is retained, identify the
determinant bit with an explicit sector flip, compute the exact Z8 spectrum
and character, and connect the admissible even C4 to the repository's existing
trace-Choi visibility readout.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass10951_clock_pin_spin_central_sign_bridge as p51
import w33_pass10952_clock_complete_positivity_firewall as p52

OUT = ROOT / "data/w33_pass10953_minimal_doubled_pin_clock_visibility.json"
TOL = 1e-8
def block_diag(a, b):
    z = np.zeros_like(a)
    return np.block([[a, z], [z, b]])


def matrix_power(m, n):
    return np.linalg.matrix_power(m, n)


def nearest_zeta8_exponent(z):
    roots = np.exp(2j * np.pi * np.arange(8) / 8)
    k = int(np.argmin(np.abs(roots - z)))
    return k, float(abs(roots[k] - z))


def action_residual(d, op, target):
    image = d @ op @ d.conj().T
    phase, err = p52.phase_residual(image, target)
    return [float(phase.real), float(phase.imag)], err


def normalized_bell_overlap(u):
    d = u.shape[0]
    omega = np.zeros(d * d, dtype=complex)
    for j in range(d):
        omega[j * d + j] = 1 / np.sqrt(d)
    state = np.kron(np.eye(d), u) @ omega
    return np.vdot(omega, state)
def main():
    p52_data = json.loads(
        (ROOT / "data/w33_pass10952_clock_complete_positivity_firewall.json")
        .read_text(encoding="utf-8")
    )
    g = tuple(
        tuple(x for x in row)
        for row in p52_data["qutrit_extended_clifford"]["clock_matrix_g"]
    )
    reps, rep_error = p52.build_sl23_representatives()
    s = p51.mm(g, p52.J)
    u = reps[s]
    v = u @ u.conj()

    zero = np.zeros((3, 3), dtype=complex)
    d = np.block([[zero, u], [u.conj(), zero]])
    eye3 = np.eye(3, dtype=complex)
    gamma = block_diag(eye3, -eye3)

    assert np.linalg.norm(d @ d.conj().T - np.eye(6)) < TOL
    assert np.linalg.norm(gamma @ d @ gamma + d) < TOL
    # The doubled Heisenberg representation carries the two faithful
    # central characters omega and omega^{-1}.
    rx = block_diag(p52.X, p52.X.conj())
    rz = block_diag(p52.ZQ, p52.ZQ.conj())
    center = rz @ rx @ rz.conj().T @ rx.conj().T
    expected_center = block_diag(
        p52.omega * eye3, p52.omega.conjugate() * eye3
    )
    assert np.linalg.norm(center - expected_center) < TOL
    assert np.linalg.norm(gamma @ rx - rx @ gamma) < TOL
    assert np.linalg.norm(gamma @ rz - rz @ gamma) < TOL
    assert np.linalg.norm(d @ center @ d.conj().T - center.conj().T) < TOL

    gx = (g[0][0], g[1][0])
    gz = (g[0][1], g[1][1])
    target_x = block_diag(p52.weyl(*gx), p52.weyl(*gx).conj())
    target_z = block_diag(p52.weyl(*gz), p52.weyl(*gz).conj())
    xphase, xerr = action_residual(d, rx, target_x)
    zphase, zerr = action_residual(d, rz, target_z)
    assert xerr < TOL and zerr < TOL
    # Minimality: any linear implementer that inverts the centre bijects the
    # omega and omega^{-1} eigenspaces. Retaining one irreducible qutrit sector
    # forces dimensions at least 3+3.
    cvals = np.linalg.eigvals(center)
    omega_dim = int(np.sum(np.abs(cvals - p52.omega) < TOL))
    omegabar_dim = int(np.sum(np.abs(cvals - p52.omega.conjugate()) < TOL))
    assert omega_dim == omegabar_dim == 3
    minimal_dimension_lower_bound = 2 * omega_dim
    assert minimal_dimension_lower_bound == 6 == d.shape[0]

    # Exact spectral fingerprint.
    eigs = np.linalg.eigvals(d)
    spectral_labels = [nearest_zeta8_exponent(z) for z in eigs]
    exponents = sorted(k for k, _ in spectral_labels)
    max_root_error = max(err for _, err in spectral_labels)
    assert exponents == [0, 1, 3, 4, 5, 7]
    assert max_root_error < TOL

    poly_residual = float(np.linalg.norm(
        matrix_power(d, 6) - matrix_power(d, 4)
        + matrix_power(d, 2) - np.eye(6)
    ))
    assert poly_residual < TOL
    traces = []
    visibilities = []
    sector_structure = []
    for n in range(8):
        dn = matrix_power(d, n)
        tr = np.trace(dn)
        traces.append([float(np.round(tr.real, 12)),
                       float(np.round(tr.imag, 12))])
        vis = float(np.round(abs(tr) / 6, 12))
        visibilities.append(vis)
        parity_error = float(np.linalg.norm(
            gamma @ dn @ gamma - ((-1) ** n) * dn
        ))
        assert parity_error < TOL
        diag_norm = float(
            np.linalg.norm(dn[:3, :3]) + np.linalg.norm(dn[3:, 3:])
        )
        offdiag_norm = float(
            np.linalg.norm(dn[:3, 3:]) + np.linalg.norm(dn[3:, :3])
        )
        sector_structure.append({
            "power": n,
            "det_parity": "even" if n % 2 == 0 else "odd",
            "sector_preserving": n % 2 == 0,
            "diag_norm": diag_norm,
            "offdiag_norm": offdiag_norm,
            "gamma_grading_error": parity_error,
        })
    expected_traces = [[6.0, 0.0], [0.0, 0.0], [2.0, 0.0], [0.0, 0.0],
                       [-2.0, 0.0], [0.0, 0.0], [2.0, 0.0], [0.0, 0.0]]
    expected_visibility = [1.0, 0.0, 1/3, 0.0, 1/3, 0.0, 1/3, 0.0]
    assert np.allclose(np.array(traces), np.array(expected_traces), atol=TOL)
    assert np.allclose(visibilities, expected_visibility, atol=TOL)

    # Bell-overlap identity is checked directly in the 6D carrier.
    overlap_errors = []
    for n in range(8):
        amp = normalized_bell_overlap(matrix_power(d, n))
        target = np.trace(matrix_power(d, n)) / 6
        overlap_errors.append(float(abs(amp - target)))
    assert max(overlap_errors) < TOL

    # The physical two-tick qutrit C4 has the same nontrivial 1/3 visibility.
    qutrit_traces = []
    qutrit_visibility = []
    for n in range(4):
        vn = matrix_power(v, n)
        tr = np.trace(vn)
        qutrit_traces.append([float(np.round(tr.real, 12)),
                              float(np.round(tr.imag, 12))])
        qutrit_visibility.append(float(np.round(abs(tr) / 3, 12)))
    assert np.allclose(qutrit_visibility, [1, 1/3, 1/3, 1/3], atol=TOL)
    # Symplectically the two-tick step is in the Fourier order-four class.
    b = p51.mm(g, g)
    conjugators = [
        h for h in reps
        if p51.conj(h, b) == p52.MF
    ]
    assert len(conjugators) == 4
    h = sorted(conjugators, key=str)[0]
    hvh = reps[h] @ v @ reps[h].conj().T
    displaced_fourier = []
    for a in range(3):
        for bb in range(3):
            phase, err = p52.phase_residual(
                hvh, p52.weyl(a, bb) @ p52.F
            )
            if err < TOL:
                displaced_fourier.append({
                    "pauli": [a, bb],
                    "phase": [float(phase.real), float(phase.imag)],
                    "residual": err,
                })
    assert len(displaced_fourier) == 1

    old_protocol = (
        ROOT / "analysis/bt820_self_entanglement_protocol.py"
    ).read_text(encoding="utf-8")
    assert '("F3", F3, 1/3)' in old_protocol
    assert "V = abs(np.trace(U)) / 3" in old_protocol
    out = {
        "schema": "w33.pass10953.minimal-doubled-pin-clock-visibility.v1",
        "status": "PASS_MINIMAL_DOUBLED_PIN_CLOCK_VISIBILITY_BRIDGE",
        "parents": {
            "pass10952": p52_data["status"],
            "existing_readout": "BT820 trace-Choi visibility V(U)=|Tr(U)|/3",
        },
        "minimal_linearization": {
            "carrier": "H_omega direct-sum H_omega^-1",
            "dimension": 6,
            "omega_central_eigenspace_dimension": omega_dim,
            "omega_inverse_central_eigenspace_dimension": omegabar_dim,
            "lower_bound": minimal_dimension_lower_bound,
            "attained": True,
            "reason":
                "a linear implementer of z->z^-1 bijects the omega and "
                "omega^-1 central eigenspaces; retaining the irreducible "
                "three-dimensional qutrit sector therefore forces 3+3",
        },
        "sector_grading": {
            "Gamma": "diag(I3,-I3)",
            "Gamma_anticommutes_with_tick": True,
            "Gamma_commutes_with_Heisenberg_generators": True,
            "tick_inverts_Heisenberg_center": True,
            "X_action_phase_and_error": [xphase, xerr],
            "Z_action_phase_and_error": [zphase, zerr],
            "powers": sector_structure,
        },
        "z8_spectrum": {
            "eighth_root_exponents": exponents,
            "missing_exponents": [2, 6],
            "max_root_error": max_root_error,
            "minimal_polynomial": "x^6 - x^4 + x^2 - 1",
            "minimal_polynomial_matrix_residual": poly_residual,
            "trace_sequence": traces,
            "normalized_trace_visibility": visibilities,
            "six_dimensional_Bell_overlap_max_error": max(overlap_errors),
        },
        "physical_even_C4": {
            "generator": "V=U_S U_S^* = two algebraic clock ticks",
            "trace_sequence": qutrit_traces,
            "normalized_trace_visibility": qutrit_visibility,
            "symplectic_matrix": [list(row) for row in b],
            "Fourier_class_conjugator_count": len(conjugators),
            "one_qutrit_lift_after_conjugacy": displaced_fourier[0],
            "reading":
                "every nonidentity physical C4 step has trace-Choi "
                "visibility 1/3 in the existing Bell-qutrit calibration",
        },
        "interferometric_prediction": {
            "full_doubled_Z8_visibility":
                [float(np.round(x, 12)) for x in visibilities],
            "existing_qutrit_C4_visibility":
                [float(np.round(x, 12)) for x in qutrit_visibility],
            "odd_tick_zero_reason":
                "the unitary tick swaps orthogonal conjugate sectors, so its "
                "block trace vanishes",
            "hardware_boundary":
                "the existing qutrit Bell interferometer can test the even C4 "
                "sequence directly; the full Z8 sequence requires a 6D "
                "sector-resolved implementation",
        },
        "theorem": (
            "The determinant-odd Pass10951 clock has a minimal complex-linear "
            "unitary carrier of dimension six: the direct sum of the two faithful "
            "qutrit Heisenberg sectors with central characters omega and omega^-1. "
            "Its sector grading Gamma anticommutes with one tick, so determinant "
            "parity is literally sector-swap parity. The unitary Z8 spectrum is "
            "zeta8^{0,1,3,4,5,7}, with minimal polynomial "
            "x^6-x^4+x^2-1 and normalized trace visibility "
            "[1,0,1/3,0,1/3,0,1/3,0]. The physical even qutrit C4 has visibility "
            "[1,1/3,1/3,1/3] and its generator lies in the Fourier order-four "
            "symplectic class, with an explicit Pauli-displaced Fourier lift."
        ),
        "boundary": (
            "The doubled C2 sector is a conjugate-representation/orientation "
            "register forced by linearization. It is not identified with literal "
            "past/future, particle/antiparticle, physical chirality or spacetime "
            "time orientation. The existing qutrit trace-Choi apparatus tests only "
            "the even C4 without a new six-dimensional implementation."
        ),
    }

    OUT.write_text(
        json.dumps(out, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "status": out["status"],
        "minimal_dimension": out["minimal_linearization"]["dimension"],
        "z8_exponents": exponents,
        "z8_visibility": visibilities,
        "qutrit_C4_visibility": qutrit_visibility,
        "fourier_displacement": displaced_fourier[0]["pauli"],
    }, indent=2))


if __name__ == "__main__":
    main()
