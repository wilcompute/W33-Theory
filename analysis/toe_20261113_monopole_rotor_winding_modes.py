"""Compute the W33 compact point-core Hardy winding zero modes."""

import argparse
from fractions import Fraction
import json
from pathlib import Path

import numpy as np
import sympy as sp

import toe_20261113_monopole_rotor_sea_flow as sea


OUT = sea.threshold.ROOT / "data/toe_20261113_monopole_rotor_winding_modes.json"


def check_holonomy(n_in, n_out, step):
    # a is the electric holonomy divided by 2 pi. Fermions have NS mode labels.
    for a in map(Fraction, ("-1/2", "-1/3", "0", "1/5", "1/2")):
        for r in range(-3, 4):
            source = r + Fraction(1, 2) - n_in * a / 2
            assert (source > 0) == (r >= 0)
            for k in (-2, -1, 0, 1, 2):
                target = r + k*step + Fraction(1, 2) - n_out * a / 2
                assert source + step*(k+a) == target
                assert (target > 0) == (r+k*step >= 0)


def zero_modes(rows):
    result = []
    for row in rows:
        n_out, = set(row["outgoing_pairings"])
        steps = [(n_in-n_out)//2 for n_in in row["incoming_pairings"]]
        assert all(step in (-1, 0, 1) for step in steps)
        assert sum(steps) == row["rotor_determinant_winding"]
        for n_in, step in zip(row["incoming_pairings"], steps):
            check_holonomy(n_in, n_out, step)
        result.append(dict(sector=row["sector"], steps=steps))
    return result


def counts(sectors, k):
    kernels = [sum(max(0, -k*step) for step in row["steps"]) for row in sectors]
    cokernels = [sum(max(0, k*step) for step in row["steps"]) for row in sectors]
    assert sum(kernels) == sum(cokernels) == 6*abs(k)
    return dict(winding=k, kernel_by_sector=kernels, cokernel_by_sector=cokernels,
                minimum_total_insertions=sum(kernels)+sum(cokernels))


def periodic_spin_control(sectors):
    # Distinct temporal boundary condition with the same seam symbol.
    rows = []
    for a in map(Fraction, ("-1/2", "-1/3", "1/5", "1/2")):
        sign = 1 if a > 0 else -1
        for n_in in (-1, 1):
            for n_out in (-1, 1):
                step = (n_in - n_out)//2
                start_in = (1 + sign*n_in)//2
                start_out = (1 + sign*n_out)//2
                assert start_in - start_out == sign*step
                for r in (-1, 0, 1, 2):
                    assert (r - n_in*a/2 > 0) == (r >= start_in)
        vanishing_defect_winding = -sign
        data = counts(sectors, vanishing_defect_winding + sign)
        assert data["minimum_total_insertions"] == 0
        rows.append(dict(electric_holonomy_in_turns=str(a),
                         effective_winding_offset=sign,
                         vanishing_defect_winding=vanishing_defect_winding))
    return rows


def smooth_loop_control():
    # For phi=z^d exp(a(z-z^-1)), ker(T(phi)) for d<0 is spanned by
    # exp(-a*z) z^j. The same check applied to conjugate symbols tests cokernels.
    nodes = 2048
    z = np.exp(2j*np.pi*np.arange(nodes)/nodes)
    max_residual = 0.0
    for a in (-0.81, 0.0, 0.37, 1.1):
        for d in (-3, -2, -1):
            symbol = z**d * np.exp(a*(z-z.conj()))
            for j in range(-d):
                vector = np.exp(-a*z)*z**j
                coeff = np.fft.fft(symbol*vector)/nodes
                residual = np.linalg.norm(coeff[:nodes//2])
                assert residual < 2e-14
                max_residual = max(max_residual, residual)
    return max_residual


def saturation_quartic(rows, incoming, outgoing, alpha, magnetic):
    active = [row for row in rows if row["rotor_determinant_winding"]]
    signs = [-int(sp.sign(row["rotor_determinant_winding"])) for row in active]
    sector_matrix = sp.Matrix([row["sector"] for row in active]).T
    assert sector_matrix.rank() == 3 and sector_matrix * sp.Matrix(signs) == sp.zeros(4, 1)
    legs = []
    for row, sign in zip(active, signs):
        # For positive winding use a kernel field on the incoming side and
        # a conjugate cokernel field on the outgoing side.
        pairs = row["incoming_pairings"] if sign == 1 else row["outgoing_pairings"]
        assert -1 in pairs
        weight = tuple(sign * (q-a)//2 for q, a in zip(row["sector"], alpha))
        weights = incoming if sign == 1 else outgoing
        labels = sorted({tuple(w[4:]) for w in weights if w[:4] == weight})
        assert labels
        pairing = int(sum(w*m for w, m in zip(weight, magnetic)))
        assert pairing == -sign
        legs.append(dict(side="incoming" if sign == 1 else "conjugate outgoing",
                         magnetic_pairing=pairing,
                         signed_occupation=sign, left_weyl_weight=weight,
                         formal_3B_L=labels))
    assert tuple(map(sum, zip(*(leg["left_weyl_weight"] for leg in legs)))) == (0, 0, 0, 0)
    assert [leg["formal_3B_L"] for leg in legs] == [
        [(0, -1)], [(0, 0), (0, 1)], [(-1, 0)], [(1, 0)]
    ]
    return dict(primitive_active_relation=signs, legs=legs,
                names=["E^c", "L or H_d", "U^c", "Q"],
                minimum_quartic_insertions_per_full_turn=3)


def factorized_yukawa_witness():
    path = sea.threshold.ROOT / "data/toe_20261110_light_yukawa_completion.json"
    fixture = json.loads(path.read_text(encoding="utf-8"))["completion"]
    up = sp.Matrix(fixture["up_matrix"])
    lepton = sp.Matrix(fixture["lepton_matrix"])
    determinants = int(up.det()), int(lepton.det())
    assert determinants == (-27, -729)
    # Coefficient of the twelve independent Grassmann variables in
    # (bilinear_up * bilinear_lepton)^3 / 3!, up to ordering sign.
    return dict(integral_lift_determinants=determinants,
                absolute_factorized_grassmann_coefficient=6*abs(determinants[0]*determinants[1]))


def lepton_overlap():
    path = sea.threshold.ROOT / "data/toe_20261113_monopole_triplet_charge.json"
    result = []
    for mesh in json.loads(path.read_text(encoding="utf-8"))["meshes"]:
        matrix = np.array(mesh["reflection_matrices_real"]) + 1j*np.array(mesh["reflection_matrices_imaginary"])
        active = matrix[:, :, :3]
        np.testing.assert_allclose(active.conj().transpose(0, 2, 1) @ active,
                                   np.broadcast_to(np.eye(3), (len(active), 3, 3)), atol=2e-12)
        overlap = abs(np.linalg.det(active[:, :3, :]))**2
        np.testing.assert_allclose(overlap, abs(matrix[:, 3, 3])**2, atol=2e-12)
        result.append(dict(radial_cells=mesh["radial_cells"], phase_count=len(active),
                           min_sampled_lepton_wedge_probability=float(min(overlap)),
                           max_sampled_lepton_wedge_probability=float(max(overlap))))
    return result


def calculate():
    incoming, outgoing, alpha = sea.threshold.color.flavor_weights()
    _, _, magnetic, _ = sea.threshold.boundary.angular_weights()
    rows, _ = sea.sector_flow(incoming, outgoing, alpha, magnetic)
    sectors = zero_modes(rows)
    return dict(status="PASS", sectors=sectors,
                winding_defects=[counts(sectors, k) for k in (-2, -1, 0, 1, 2)],
                smooth_loop_max_projected_residual=smooth_loop_control(),
                charge_neutral_quartic=saturation_quartic(rows, incoming, outgoing, alpha, magnetic),
                periodic_spin_holonomy_control=periodic_spin_control(sectors),
                conditional_factorized_yukawa_witness=factorized_yukawa_witness(),
                sampled_active_triplet_lepton_overlap=lepton_overlap())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUT)
    args = parser.parse_args()
    result = calculate()
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("Kernel and cokernel dimensions:", [(r["winding"], sum(r["kernel_by_sector"]),
                                               sum(r["cokernel_by_sector"]))
                                              for r in result["winding_defects"]])
    print("Smooth-loop residual:", result["smooth_loop_max_projected_residual"])
    print("Sampled lepton wedge probabilities:", result["sampled_active_triplet_lepton_overlap"])
