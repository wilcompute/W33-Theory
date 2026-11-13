"""Project W33 triplet residues onto the physical Higgs and matter spaces."""

import json

import numpy as np

import toe_20261113_monopole_triplet_charge as charge
import toe_20261113_monopole_winding_residues as residues


OUT = residues.OUT.with_name("toe_20261113_monopole_winding_residue_flavors.json")


def calculate():
    threshold = residues.poles.threshold
    radial = threshold.radial
    triplet = threshold.triplet
    flat = triplet.flat
    gauge, adjoint, cartan, color, weak, y = flat.compact_chart()
    records = np.array(flat.vacuum.native.build_records())
    x, z, _, fundamental, spaces, (_, _, weights) = triplet.flavor.projected_space(
        gauge, adjoint, color, weak, y, records)
    core = triplet.adjoint_phase.core
    five = core.topology.representation_check(adjoint, cartan, weak, y)["fundamental5_chart"]
    step, _ = core.monopole_root(adjoint, five)
    positive = radial.exchange.LE[0]
    frames = radial.sector_frames(adjoint.astype(float), weights, step, positive)
    yukawa = flat.read(triplet.flavor.OUT)
    words = flat.read(flat.OUT)["repair"]["centered_trace_squared_terms"]
    rules = triplet.tensor_and_rules(yukawa)
    evaluators = [triplet.mass_evaluator(*f, records, words, rules) for f in frames]
    vacuum = np.diag(y).astype(float), np.concatenate((x, z)).reshape(5, 27, 3).astype(float)
    _, _, incoming, outgoing, (plus, minus) = radial.exterior_basis(evaluators, vacuum)
    rows, cols = plus.shape
    from scipy.linalg import null_space

    # Build physical frames in the very same magnetic orientation used
    # by the residue solver. The L-weight block is conjugate to the
    # orientation used by charge.physical_model().
    d_weight, hu_weight = triplet.WEIGHTS
    d_lifts = charge.chiral_lifts(spaces[tuple(-np.array(d_weight))], frames[1][1], null_space(minus))
    hu_lifts = charge.chiral_lifts(spaces[hu_weight], frames[0][0], null_space(plus.T))
    d, hu = (np.linalg.qr(v)[0] for v in (d_lifts, hu_lifts))
    upper = spaces[tuple(fundamental[15])]
    lower = [triplet.flavor.lower_doublet(v, weak) for v in upper]
    lepton_lifts = charge.chiral_lifts(lower, frames[0][1], null_space(plus))
    covector = np.array(yukawa["completion"]["down_higgs_covector"], float)
    lepton = np.linalg.qr(lepton_lifts @ null_space(covector[None]))[0]
    higgs = lepton_lifts @ np.linalg.solve(lepton_lifts.T @ lepton_lifts, covector)
    higgs /= np.linalg.norm(higgs)
    physical_in = np.column_stack((charge.flux_lift(d, "left", -1, cols, rows),
                                   charge.flux_lift(hu, "right", 1, cols, rows)))
    physical_out = charge.flux_lift(np.column_stack((lepton, higgs)), "left", 1, cols, rows)
    change_in = incoming.conj().T @ physical_in
    change_out = outgoing.conj().T @ physical_out
    np.testing.assert_allclose(incoming @ change_in, physical_in, atol=1e-11)
    np.testing.assert_allclose(outgoing @ change_out, physical_out, atol=1e-11)
    fixture = json.loads(residues.OUT.read_text(encoding="utf-8"))
    sector, = [row for row in fixture["sectors"] if row["sector"] == "L"]
    results = {}
    for name in ("positive", "negative"):
        row = sector[name]
        raw = np.array(row["real"]) + 1j*np.array(row["imag"])
        physical = change_out.conj().T @ raw @ change_in
        u, s, vh = np.linalg.svd(physical)
        np.testing.assert_allclose(s, row["singular_values"], atol=1e-13)
        results[name] = dict(energy=row["energy"], incident_Dc=float(sum(abs(vh[0, :3])**2)),
                             incident_conjugate_Hu=float(abs(vh[0, 3])**2),
                             outgoing_L=float(sum(abs(u[:3, 0])**2)),
                             outgoing_Hd=float(abs(u[3, 0])**2),
                             residue_real=physical.real.tolist(), residue_imag=physical.imag.tolist())
    for key in ("incident_Dc", "incident_conjugate_Hu", "outgoing_L", "outgoing_Hd"):
        np.testing.assert_allclose(results["positive"][key], results["negative"][key], atol=1e-9)
    return dict(status="PASS", input_labels=["D^c"]*3+["H_u conjugate"],
                output_labels=["L"]*3+["H_d"], poles=results)


if __name__ == "__main__":
    result = calculate()
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print({k: v for k, v in result["poles"]["positive"].items() if not k.startswith("residue")})
