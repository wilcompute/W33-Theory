#!/usr/bin/env python3
"""Part DCCXVI: axis-syndrome selector codec bridge.

DCCXV showed that the 480 expected fusion attempts are a native QEC syndrome
ledger.  This bridge factors the local 12-turn alphabet:

    12 = 3 axes * 2 signs * 2 roles.

The classical 40-trit selector records the 3-axis coordinate.  The sign and
accepted-vs-return role are syndrome/frame layers, not extra classical trits.
Adding one KLM rail bit gives the 960 primitive ledger.
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccxv_photonic_fusion_syndrome_qec_bridge import (  # noqa: E402
    build_bridge as build_dccxv_bridge,
)


OUT_PATH = ROOT / "data" / "dccxvi_axis_syndrome_selector_codec_bridge.json"

Q = 3
LAM = Q - 1
V = (Q**4 - 1) // (Q - 1)
K = Q * (Q + 1)
H1 = Q**4
E = V * K // 2
DIRECTED = 2 * E
KLM = 2 * DIRECTED


@dataclass(frozen=True)
class BridgeSummary:
    local_codec_size: int
    classical_axis_trits: int
    fusion_attempt_slots: int
    klm_primitive_slots: int
    all_identities_hold: bool


def _build_local_slots() -> list[dict[str, Any]]:
    axes = ["B23", "B31", "B12"]
    signs = ["+", "-"]
    roles = ["accepted", "return"]
    slots: list[dict[str, Any]] = []
    for axis in axes:
        for sign in signs:
            for role in roles:
                slots.append(
                    {
                        "slot": f"{role}:{sign}{axis}",
                        "axis": axis,
                        "sign": sign,
                        "role": role,
                    }
                )
    return slots


def build_bridge() -> dict[str, Any]:
    dccxv = build_dccxv_bridge()
    local_slots = _build_local_slots()
    axes = sorted({slot["axis"] for slot in local_slots})
    signs = sorted({slot["sign"] for slot in local_slots})
    roles = sorted({slot["role"] for slot in local_slots})

    local_codec = {
        "axis_alphabet": axes,
        "sign_alphabet": signs,
        "role_alphabet": roles,
        "local_slots": local_slots,
        "factorization": "12 = 3 axes * 2 signs * 2 accepted/return roles",
    }

    global_codec = {
        "vertices": V,
        "axis_layer_slots": V * len(axes),
        "signed_axis_layer_slots": V * len(axes) * len(signs),
        "fusion_attempt_slots": V * len(axes) * len(signs) * len(roles),
        "klm_primitive_slots": V * len(axes) * len(signs) * len(roles) * LAM,
    }

    selector_record = {
        "classical_selector_trits": V,
        "choices_per_trit": Q,
        "selector_state_count": Q**V,
        "fits_64_bit_envelope": 2**63 < Q**V < 2**64,
        "read": (
            "The 40-trit classical selector stores one 3-axis coordinate per vertex; "
            "sign and accepted/return role remain syndrome/frame layers."
        ),
    }

    layer_roles = {
        "classical_axis_selector": {
            "alphabet_size": len(axes),
            "stored_as": "40 trits",
            "role": "axis coordinate B23/B31/B12",
        },
        "quantum_sign_frame": {
            "alphabet_size": len(signs),
            "stored_as": "Pauli/Clifford frame bit",
            "role": "orientation + or - on the selected axis",
        },
        "heralded_return_syndrome": {
            "alphabet_size": len(roles),
            "stored_as": "fusion syndrome bit",
            "role": "accepted bond or heralded return slot",
        },
        "klm_rail_lift": {
            "alphabet_size": LAM,
            "stored_as": "optical primitive rail bit",
            "role": "doubles 480 directed attempts to 960 KLM primitives",
        },
    }

    qec_read = {
        "edge_qubits": E,
        "logical_h1": H1,
        "css_identity": "39 + 120 + 81 = 240",
        "codec_read": (
            "The classical selector does not overencode all 12 local turns. "
            "It records the ternary axis; the two binary layers are exactly the "
            "frame/syndrome data absorbed by the protected QEC runtime."
        ),
    }

    identities = {
        "local_codec_factors_as_3_times_2_times_2": (
            len(local_slots) == Q * LAM * LAM == 12
            and len(axes) == Q
            and len(signs) == LAM
            and len(roles) == LAM
        ),
        "fusion_slots_are_40_times_local_codec": (
            global_codec["fusion_attempt_slots"]
            == dccxv["summary"]["fusion_attempts"]
            == DIRECTED
        ),
        "accepted_and_return_roles_each_cover_240_slots": (
            sum(1 for slot in local_slots if slot["role"] == "accepted") * V == E
            and sum(1 for slot in local_slots if slot["role"] == "return") * V == E
        ),
        "classical_selector_is_40_trits_inside_64_bit_envelope": (
            selector_record["classical_selector_trits"] == V
            and selector_record["choices_per_trit"] == Q
            and selector_record["fits_64_bit_envelope"] is True
        ),
        "klm_rail_bit_doubles_the_fusion_codec": (
            global_codec["klm_primitive_slots"] == dccxv["summary"]["klm_primitives"] == KLM
        ),
        "selector_axis_layer_is_not_the_full_12_turn_alphabet": (
            layer_roles["classical_axis_selector"]["alphabet_size"] == Q
            and global_codec["axis_layer_slots"] == V * Q == 120
            and global_codec["fusion_attempt_slots"] == 4 * global_codec["axis_layer_slots"]
        ),
        "qec_tail_remains_logical_not_stabilized": qec_read["edge_qubits"] - qec_read["logical_h1"] == 159,
    }

    summary = BridgeSummary(
        local_codec_size=len(local_slots),
        classical_axis_trits=selector_record["classical_selector_trits"],
        fusion_attempt_slots=global_codec["fusion_attempt_slots"],
        klm_primitive_slots=global_codec["klm_primitive_slots"],
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "local_codec": local_codec,
        "global_codec": global_codec,
        "selector_record": selector_record,
        "layer_roles": layer_roles,
        "qec_read": qec_read,
        "theorem": (
            "The 480 fusion-attempt carrier factors as 40*3*2*2. The 40-trit "
            "classical selector stores the ternary axis coordinate, while the two "
            "binary factors are the Clifford sign frame and the accepted/return "
            "fusion syndrome. Adding the KLM rail bit gives 40*3*2*2*2=960."
        ),
        "honesty_boundary": (
            "This is a finite codec theorem for the promoted photonic/QEC runtime. "
            "It does not model hardware noise rates, detector physics, or curved "
            "4D spectral-action asymptotics."
        ),
        "identities": identities,
    }


def write_bridge(path: Path = OUT_PATH) -> Path:
    payload = build_bridge()
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def main() -> None:
    out = write_bridge()
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
