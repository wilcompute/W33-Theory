"""Real-energy W33 triplet conversion and pole interference."""

import argparse
import json
from pathlib import Path

import numpy as np

import toe_20261113_monopole_winding_residue_flavors as flavors
import toe_20261113_monopole_winding_residues as residues


OUT = residues.OUT.with_name("toe_20261113_monopole_triplet_line_shape.json")


def conversion(matrix):
    return np.linalg.norm(matrix[:3, 3])**2


def decompose(full, pole):
    regular = full-pole
    matrix_terms = [regular[:3, 3], pole[:3, 3]]
    background, resonant = map(lambda v: np.linalg.norm(v)**2, matrix_terms)
    interference = 2*np.vdot(*matrix_terms).real
    total = conversion(full)
    np.testing.assert_allclose(total, background+resonant+interference, atol=1e-13)
    # Complementary blocks of any 3+1 unitary have equal total cross flux.
    np.testing.assert_allclose(total, np.linalg.norm(full[3, :3])**2, atol=1e-9)
    return dict(total=float(total), regular=float(background), poles=float(resonant),
                interference=float(interference))


def factor(energy, location, projector, inverse=False):
    zero, pole = location.conjugate(), location
    if inverse:
        zero, pole = pole, zero
    return np.eye(len(projector)) + ((pole-zero)/(energy-pole))*projector


def projectors(locations, matrices):
    result = []
    for z, residue in zip(locations, matrices):
        for previous, projector in zip(locations, result):
            residue = residue @ factor(z, previous, projector, inverse=True)
        _, singular, vh = np.linalg.svd(residue)
        assert singular[1] < 1e-10*singular[0]
        vector = vh[0]
        result.append(np.outer(vector.conj(), vector))
    return result


def calculate():
    change_in, change_out = flavors.flavor_frames()
    data = json.loads(flavors.OUT.read_text(encoding="utf-8"))["poles"]
    locations = np.array([complex(*row["energy"]) for row in data.values()])
    matrices = np.array([np.array(row["residue_real"])+1j*np.array(row["residue_imag"])
                         for row in data.values()])
    system = next(item for item in residues.poles.threshold.prepare(40) if item[0] == "L")
    positive = np.unique(np.r_[np.linspace(0., .004, 25), locations[0].real])
    energy = np.r_[-positive[:0:-1], positive]
    rows = []
    dets, stripped, allpass = [], [], []
    projections = projectors(locations, matrices)
    for e in energy:
        full = change_out.conj().T @ residues.matching(system, e) @ change_in
        unitary = np.linalg.norm(full.conj().T @ full-np.eye(4))
        assert unitary < 1e-8
        principal = np.sum(matrices/(e-locations)[:, None, None], axis=0)
        rows.append(dict(energy=float(e), unitarity_error=float(unitary), **decompose(full, principal)))
        product = np.eye(4, dtype=complex)
        for z, projection in zip(locations, projections):
            product = factor(e, z, projection) @ product
        np.testing.assert_allclose(product.conj().T @ product, np.eye(4), atol=1e-13)
        smooth = full @ product.conj().T
        stripped.append(smooth)
        allpass.append(product)
        dets.append(np.linalg.det(full))

    # On the real line a scalar all-pass factor carries the paired poles.
    # Strip its phase to measure the smooth determinant phase directly.
    scalar_factor = np.prod((energy[:, None]-locations.conj())/(energy[:, None]-locations), axis=1)
    np.testing.assert_allclose(abs(scalar_factor), 1., atol=1e-14)
    corrected = np.array(dets)/scalar_factor
    full_phase = np.unwrap(np.angle(dets))
    corrected_phase = np.unwrap(np.angle(corrected))
    factor_phase = np.unwrap(np.angle(scalar_factor))
    np.testing.assert_allclose(full_phase-full_phase[0], corrected_phase-corrected_phase[0]
                               +factor_phase-factor_phase[0], atol=1e-10)
    for row, full, background in zip(rows, full_phase-full_phase[0], corrected_phase-corrected_phase[0]):
        row.update(determinant_phase=float(full), determinant_phase_without_pole_factors=float(background))
    central = stripped[len(rows)//2]
    for row, smooth, product in zip(rows, stripped, allpass):
        row.update(unitary_background_conversion=float(conversion(smooth)),
                   fixed_background_model_conversion=float(conversion(central @ product)),
                   unitary_background_change=float(np.linalg.norm(smooth-central, ord=2)))
    return dict(status="PASS", cells=80, exterior_cut=5., rows=rows,
                projector_overlap=float(np.trace(projections[0] @ projections[1]).real),
                max_fixed_background_conversion_error=max(
                    abs(r["total"]-r["fixed_background_model_conversion"]) for r in rows),
                sampled_minimum=min(rows, key=lambda row: row["total"]),
                sampled_maximum=max(rows, key=lambda row: row["total"]),
                zero_energy=rows[len(rows)//2])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUT)
    args = parser.parse_args()
    result = calculate()
    args.output.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    for key in ("sampled_minimum", "sampled_maximum", "zero_energy"):
        print(key, result[key], flush=True)
