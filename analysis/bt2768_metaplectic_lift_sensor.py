#!/usr/bin/env python3
"""Two-shot, global-phase-invariant metaplectic sensor for all Sp(4,3) classes."""
from __future__ import annotations

import gzip
import hashlib
import json
import math
from pathlib import Path

import numpy as np

from bt2767_2771_core import (
    I4,
    canonical_geometry,
    conjugacy_classes,
    generate_group,
    geometry_signature,
    matrix_json,
    phase_code,
    recover_word,
)

ROOT = Path(__file__).resolve().parents[1]


def qutrit_generators() -> dict[str, np.ndarray]:
    w = np.exp(2j * np.pi / 3)
    F = np.array([[w ** (j * k) for k in range(3)] for j in range(3)], dtype=complex) / math.sqrt(3)
    P = np.diag([w ** ((2 * j * j) % 3) for j in range(3)]).astype(complex)
    I = np.eye(3, dtype=complex)
    SUM = np.zeros((9, 9), dtype=complex)
    for p in range(3):
        for f in range(3):
            SUM[3 * p + ((f + p) % 3), 3 * p + f] = 1
    base = {"Fp": np.kron(F, I), "Ff": np.kron(I, F), "Sp": np.kron(P, I), "Sf": np.kron(I, P), "CX": SUM}
    out = dict(base)
    for name, U in base.items():
        out[name + "^-1"] = U.conj().T
    return out


def theta(U: np.ndarray, k: int) -> complex:
    Uk = np.linalg.matrix_power(U, k)
    return np.trace(Uk) ** 9 / np.linalg.det(Uk)


def signature_json(sig: tuple) -> list[dict[str, int]]:
    return [{str(length): count for length, count in profile} for profile in sig]


def deterministic_gzip(payload: bytes) -> bytes:
    import io
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode="wb", mtime=0) as gz:
        gz.write(payload)
    return buf.getvalue()


def build() -> dict:
    group, parent, _ = generate_group(with_words=True)
    classes = conjugacy_classes(group)
    geom = canonical_geometry()
    Ug = qutrit_generators()
    unitaries: dict = {I4: np.eye(9, dtype=complex)}
    for g, (prev, name) in parent.items():
        if g == I4:
            continue
        assert prev is not None and name is not None
        unitaries[g] = unitaries[prev] @ Ug[name]

    class_of = {x: i for i, cls in enumerate(classes) for x in cls}
    class_theta: dict[int, tuple] = {}
    for g in group:
        code = (tuple(phase_code(theta(unitaries[g], 1)).items()), tuple(phase_code(theta(unitaries[g], 2)).items()))
        idx = class_of[g]
        if idx in class_theta:
            assert class_theta[idx] == code
        else:
            class_theta[idx] = code
    assert len(class_theta) == 34

    rows = []
    joint, geo_only, theta_only, geo_theta1 = set(), set(), set(), set()
    for idx, cls in enumerate(classes):
        rep = cls[0]
        U = unitaries[rep]
        geo = geometry_signature(rep, geom)
        t1 = phase_code(theta(U, 1))
        t2 = phase_code(theta(U, 2))
        gkey = str(geo)
        tkey = (tuple(t1.items()), tuple(t2.items()))
        joint.add((gkey, tkey)); geo_only.add(gkey); theta_only.add(tkey); geo_theta1.add((gkey, tuple(t1.items())))
        rows.append({
            "class_id": idx,
            "class_size": len(cls),
            "representative": matrix_json(rep),
            "representative_word": recover_word(rep, parent),
            "geometric_signature": signature_json(geo),
            "theta_1": t1,
            "theta_2": t2,
        })
    assert len(geo_only) == 15
    assert len(geo_theta1) == 30
    assert len(theta_only) == 33
    assert len(joint) == 34
    return {
        "schema": "w33.pass2768.metaplectic_lift_sensor.v1",
        "status": "COMPLETE_LOCAL_EXACT",
        "group_order": len(group),
        "conjugacy_classes": len(classes),
        "geometric_signatures": len(geo_only),
        "geometry_plus_theta1_signatures": len(geo_theta1),
        "theta1_theta2_signatures": len(theta_only),
        "complete_joint_signatures": len(joint),
        "sensor": {
            "definition": "Theta_k(g)=Tr(U_g^k)^9/det(U_g^k), k=1,2",
            "global_phase_invariant": True,
            "shots": 2,
            "carrier_sizes": [40, 40, 160, 240, 1620],
            "phase_code": "(phase mod 4, twice log_3 magnitude, zero flag)",
        },
        "negative_result": (
            "Permutation-cycle carriers are invariant under inversion and cannot resolve all inverse classes. "
            "A phase-sensitive lift observable is therefore necessary."
        ),
        "rows": rows,
    }


def main() -> None:
    out = build()
    raw = (json.dumps(out, sort_keys=True, separators=(",", ":")) + "\n").encode()
    gz = deterministic_gzip(raw)
    path = ROOT / "data" / "PART_BT2768_SP43_METAPLECTIC_LIFT_SENSOR.json.gz"
    path.write_bytes(gz)
    summary = {key: out[key] for key in ("group_order", "conjugacy_classes", "geometric_signatures", "geometry_plus_theta1_signatures", "theta1_theta2_signatures", "complete_joint_signatures")}
    summary["gzip_sha256"] = hashlib.sha256(gz).hexdigest()
    (ROOT / "data" / "PART_BT2768_SP43_METAPLECTIC_LIFT_SENSOR_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
