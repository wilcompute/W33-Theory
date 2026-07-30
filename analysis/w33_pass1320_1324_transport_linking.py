#!/usr/bin/env python3
"""Passes 1320--1324 exact transport/linking algebra release."""
from __future__ import annotations
from pathlib import Path
import json
import w33_pass1315_1319_exact_frontiers as prior
from w33_pass1320_1324_common import COMMON_SPECIES,RelationAlgebra,fractions_to_json
from w33_pass1320_1324_hecke import build_noncentral_matrix_units
from w33_pass1320_1324_transport_core import (build_transport_orbitals,build_left_action,species_projection_matrices,aligned_transport_channels,build_hashimoto_matrix,right_hashimoto_action,restricted_species20_dynamics)
from w33_pass1320_1324_linking import composition_and_linking
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"w33_pass1320_1324_transport_linking.json"
def manuscript_insert() -> str:
    return r"""% Passes 1320--1324 exact theorem-ledger insertion.
\subsection{The six-channel linking algebra between the coset and Hashimoto carriers}
\begin{theorem}[Exact transport/linking theorem]
Let $X=\mathbb C[W(E_6)/S_5]$ be the $432$-dimensional coset carrier and let
$Y=\mathbb C[E_{\rm dir}]$ be the $480$-dimensional directed-edge carrier.
Then
\[
 \dim\operatorname{Hom}_{W(E_6)}(Y,X)=6.
\]
The six-dimensional transport space splits by irreducible species as
\[
 \operatorname{Hom}_{W(E_6)}(Y,X)
 \cong \mathbb C_{\mathbf1}\oplus\mathbb C_{\mathbf{15}_a}
 \oplus\mathbb C^3_{\mathbf{20}}\oplus\mathbb C_{\mathbf{60}_a}.
\]
The complete common-support linking algebra is
\[
 M_2(\mathbb C)\oplus M_2(\mathbb C)\oplus M_4(\mathbb C)
 \oplus M_2(\mathbb C),
\]
of dimension $28$.  In particular, the species-$20$ sector realizes the full
Morita context $M_3(\mathbb C)\dashv\mathbb C$ through three independent
transport channels.
\end{theorem}
\begin{proof}[Exact computational proof]
The literal diagonal action on $X\times Y$ has six orbits.  Their indicator
matrices give a basis of the Hom-space.  Character projectors split that basis
with ranks $1,1,3,1$.  The $26$ coset relations are decomposed into complete
matrix units, and every product $T_iT_j^*$ and $T_i^*T_j$ is expanded in those
matrix units and in the species-refined Hashimoto projector basis.  The left
and right products have spans $12$ and $4$, respectively, while the two Hom
corners each have dimension $6$; hence the linking dimension is
$12+4+6+6=28$.  All associativity and matrix-unit identities are checked over
$\mathbb Q$ by
\texttt{analysis/w33\_pass1320\_1324\_transport\_linking.py}.
\end{proof}
\begin{remark}[Hashimoto does not choose a preferred species-$20$ copy]
On the literal species-$20$ image in $Y$, the Hashimoto operator is exactly
$-I_{20}$, with minimal polynomial $x+1$.  It therefore transports with the
same eigenvalue through all three species-$20$ channels and cannot select one
of the three copies in $X$.  A copy choice requires a Hecke-gauge primitive
idempotent, not Hashimoto dynamics alone.
\end{remark}
\begin{center}
\begin{tabular}{lll}
\toprule
Historical claim & Active status & Exact replacement\\
\midrule
Nine coset orbitals & Retracted & Twenty-six literal orbitals\\
Coordinate-surrogate matrix units & Retracted & Carrier-level rational units\\
Preferred species-$20$ Hashimoto channel & False & Threefold scalar degeneracy\\
Carrier identification $432=480$ & False & Six-dimensional equivariant bridge\\
\bottomrule
\end{tabular}
\end{center}
"""


def main() -> dict:
    print("Pass 1320-1324: reconstructing literal actions")
    root = prior.root_model()
    hecke = prior.hecke_and_432(root)
    point = prior.point_model()
    hashi = prior.hashimoto_and_species20(point)
    alg = RelationAlgebra(hecke)

    print("Pass 1321: constructing full Hecke matrix units")
    matrix_units = build_noncentral_matrix_units(alg, hecke["decomp432"])

    print("Pass 1320: resolving six transport channels")
    transport = build_transport_orbitals(hecke, hashi)
    left_action = build_left_action(hecke, transport)
    projections = species_projection_matrices(alg, left_action)
    channels = aligned_transport_channels(
        alg,
        matrix_units,
        projections,
        left_action,
        transport["sizes"],
    )

    B = build_hashimoto_matrix(hashi)
    B_action = right_hashimoto_action(transport, B)
    # Row-vector convention: orbital coefficients q transform as q * B_action.
    eigenvalue_counts = {}
    for channel in channels:
        q = channel["orbital_coefficients"]
        image = [
            sum(q[i] * int(B_action[i, j]) for i in range(6))
            for j in range(6)
        ]
        expected = 11 if channel["species"] == "1" else -1
        assert image == [expected * x for x in q]
        eigenvalue_counts[expected] = eigenvalue_counts.get(expected, 0) + 1
        channel["hashimoto_eigenvalue"] = expected
    assert eigenvalue_counts == {11: 1, -1: 5}

    print("Pass 1322: restricting Hashimoto to species 20")
    species20 = restricted_species20_dynamics(point, hashi, B)

    print("Pass 1323: closing the transport composition category")
    linking = composition_and_linking(
        alg,
        hecke,
        transport,
        left_action,
        projections,
        matrix_units,
        channels,
    )

    insert = manuscript_insert()
    insert_path = ROOT / "analysis" / "BT1320_BT1324_transport_linking_theorem.tex"
    insert_path.write_text(insert, encoding="utf-8")
    w33_ledger = ROOT / "analysis" / "w33_paper_pass1320_1324_theorem_ledger.tex"
    photonic_ledger = ROOT / "analysis" / "photonic_holonet_pass1320_1324_theorem_ledger.tex"
    w33_ledger.write_text(insert, encoding="utf-8")
    photonic_ledger.write_text(insert, encoding="utf-8")

    result = {
        "schema": "w33.pass1320_1324.transport_linking.v1",
        "status": "PASS",
        "scope": "Exact finite permutation representations, rational association algebras, and equivariant linking operators only.",
        "pass1320_six_channel_diagonalization": {
            "transport_orbital_sizes": transport["sizes"],
            "transport_label_sha256": transport["sha256"],
            "species_projection_matrices": fractions_to_json(projections),
            "projection_ranks": {"1": 1, "15a": 1, "20": 3, "60a": 1},
            "aligned_channels": fractions_to_json(channels),
            "hashimoto_action_on_transport_basis": B_action.tolist(),
            "hashimoto_eigenvalue_multiplicities_on_hom": {"11": 1, "-1": 5},
        },
        "pass1321_full_hecke_matrix_units": matrix_units["json"],
        "pass1322_species20_hashimoto_dynamics": species20,
        "pass1323_transport_composition_and_morita_context": linking,
        "pass1324_manuscript_ledger_promotion": {
            "shared_insert": "analysis/BT1320_BT1324_transport_linking_theorem.tex",
            "w33_paper_ledger": "analysis/w33_paper_pass1320_1324_theorem_ledger.tex",
            "photonic_holonet_ledger": "analysis/photonic_holonet_pass1320_1324_theorem_ledger.tex",
            "contains_formal_theorem": True,
            "contains_exact_proof": True,
            "contains_retraction_table": True,
            "main_source_integration_policy": "Companion current-claims ledgers are canonical and compile-ready; chronological manuscript bodies remain unmutated to preserve their explicit historical-record policy.",
        },
        "checks": {
            "six_transport_channels": len(channels) == 6,
            "species_split_1_1_3_1": [
                sum(channel["species"] == name for channel in channels)
                for name in COMMON_SPECIES
            ] == [1, 1, 3, 1],
            "full_26_matrix_unit_basis": matrix_units["json"]["wedderburn_dimension"] == 26,
            "species20_hashimoto_is_minus_identity": species20["hashimoto_eigenvalue"] == -1,
            "hashimoto_does_not_select_copy": not species20["selects_unique_432_copy"],
            "linking_algebra_dimension_28": linking["linking_algebra_dimension"] == 28,
            "morita_context_full": linking["species20_morita_context"].startswith("M_3"),
            "manuscript_ledgers_written": all(path.exists() for path in (insert_path, w33_ledger, photonic_ledger)),
        },
    }
    assert all(result["checks"].values()), result["checks"]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    # Persist compact, code-searchable certificates; large tables are split by algebraic block.
    data_dir = OUT.parent
    simple_components = {
        "pass1320_six_channel_diagonalization": "w33_pass1320_six_channel_diagonalization.json",
        "pass1322_species20_hashimoto_dynamics": "w33_pass1322_species20_hashimoto_dynamics.json",
        "pass1324_manuscript_ledger_promotion": "w33_pass1324_manuscript_ledger_promotion.json",
    }
    for key, filename in simple_components.items():
        payload = {"schema": f"w33.{key}.v1", "status": "PASS", "scope": result["scope"], key: result[key]}
        (data_dir / filename).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    hecke = result["pass1321_full_hecke_matrix_units"]
    block_files = {}
    for name, block in hecke["blocks"].items():
        safe = name.replace("_", "-")
        filename = f"w33_pass1321_hecke_block_{safe}.json"
        block_files[name] = filename
        payload = {"schema": "w33.pass1321.hecke_block.v1", "status": "PASS", "irrep": name, "block": block}
        (data_dir / filename).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    hecke_summary = {key: value for key, value in hecke.items() if key != "blocks"}
    hecke_summary["block_files"] = block_files
    (data_dir / "w33_pass1321_full_hecke_matrix_units.json").write_text(
        json.dumps({"schema": "w33.pass1321.full_hecke_matrix_units.v1", "status": "PASS", "pass1321_full_hecke_matrix_units": hecke_summary}, indent=2) + "\n",
        encoding="utf-8",
    )

    linking = result["pass1323_transport_composition_and_morita_context"]
    x_table = linking["x_side_products_in_hecke_matrix_units"]
    y_table = linking["y_side_products_in_species_refined_hashimoto_basis"]
    (data_dir / "w33_pass1323_x_side_compositions.json").write_text(
        json.dumps({"schema": "w33.pass1323.x_side_compositions.v1", "status": "PASS", "x_side_products_in_hecke_matrix_units": x_table}, indent=2) + "\n",
        encoding="utf-8",
    )
    (data_dir / "w33_pass1323_y_side_compositions.json").write_text(
        json.dumps({"schema": "w33.pass1323.y_side_compositions.v1", "status": "PASS", "y_side_products_in_species_refined_hashimoto_basis": y_table}, indent=2) + "\n",
        encoding="utf-8",
    )
    linking_summary = {key: value for key, value in linking.items() if key not in ("x_side_products_in_hecke_matrix_units", "y_side_products_in_species_refined_hashimoto_basis")}
    linking_summary["x_side_table"] = "w33_pass1323_x_side_compositions.json"
    linking_summary["y_side_table"] = "w33_pass1323_y_side_compositions.json"
    (data_dir / "w33_pass1323_transport_composition_and_morita_context.json").write_text(
        json.dumps({"schema": "w33.pass1323.transport_composition_and_morita_context.v1", "status": "PASS", "pass1323_transport_composition_and_morita_context": linking_summary}, indent=2) + "\n",
        encoding="utf-8",
    )

    component_map = {
        **simple_components,
        "pass1321_full_hecke_matrix_units": "w33_pass1321_full_hecke_matrix_units.json",
        "pass1323_transport_composition_and_morita_context": "w33_pass1323_transport_composition_and_morita_context.json",
    }
    summary = {
        "schema": result["schema"], "status": result["status"], "scope": result["scope"],
        "components": component_map,
        "headline": "Six exact transports close to M2(C)+M2(C)+M4(C)+M2(C); the full rational Hecke matrix units are explicit and Hashimoto is -I on species 20.",
        "checks": result["checks"],
    }
    OUT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "status": "PASS",
                "channels": len(channels),
                "hecke_units": matrix_units["json"]["wedderburn_dimension"],
                "species20_hashimoto": -1,
                "linking_dimension": linking["linking_algebra_dimension"],
            },
            indent=2,
        )
    )
    return result


if __name__ == "__main__":
    main()
