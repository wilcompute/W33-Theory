#!/usr/bin/env python3
"""Process-safe cache for compiled Steinberg/photonic finite-control artifacts.

The continuation kernel deliberately separates process identity from finite
control state.  This module exploits that separation without weakening it:
compiled backend artifacts are keyed only by immutable control semantics and a
calibration epoch, while authority to *use* an artifact remains in a separate
continuation-specific authorization record.

For every compressible window of the real 24-step authenticated HoloVM witness
we build:

  artifact = H(frame, Steinberg basis/table, endpoint action,
               executable time-order word, calibration epoch)

and separately

  authorization = H(artifact id, process id, parent/child continuations,
                    generations, receipt chain, continuation chain).

Thus repeated finite-control actions can share one compiled artifact without
sharing process authority, guest state, receipts, or continuation identity.
The calibration epoch here is a software certificate namespace.  It is not a
claim that a physical optical calibration already exists.
"""
from __future__ import annotations

from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
from typing import Any

from w33_semantic_safe_photonic_macroop import trace
from w33_steinberg_continuation_control import operational_table
from w33_steinberg_photonic_macro_refinement import (
    compile_sequential_macro,
    sequential_steinberg_action,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "W33_STEINBERG_CONTROL_ARTIFACT_CACHE.json"
CALIBRATION_EPOCH = "software-certificate-epoch-0"
SYMPLECTIC_FRAME = {
    "schema": "w33.holovm-to-steinberg-symplectic-frame.v1",
    "source_form": "u0*v2-u2*v0+u1*v3-u3*v1",
    "target_form": "u0*v1-u1*v0+u2*v3-u3*v2",
    "coordinate_permutation": [0, 2, 1, 3],
}


def digest(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode()
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def build_artifact(*, basis_digest: str, action_table_digest: str,
                   steinberg_action_digest: str, executable_word, calibration_epoch: str) -> dict[str, Any]:
    body = {
        "schema": "w33.steinberg-control-artifact.v1",
        "machine_type": "w33.circuit216.steinberg81",
        "symplectic_frame_digest": digest(SYMPLECTIC_FRAME),
        "basis_digest": basis_digest,
        "action_table_digest": action_table_digest,
        "steinberg_action_digest": steinberg_action_digest,
        "executable_time_order": [list(x) for x in executable_word],
        "calibration_epoch": calibration_epoch,
    }
    return {**body, "artifact_id": digest(body)}


def build_authorization(artifact: dict[str, Any], window) -> dict[str, Any]:
    receipts = tuple(x.receipt.receipt_id for x in window)
    roots = tuple(x.child.continuation_id for x in window)
    body = {
        "schema": "w33.steinberg-control-artifact-authorization.v1",
        "artifact_id": artifact["artifact_id"],
        "process_id": window[0].parent.process_id,
        "parent_continuation_root": window[0].parent.continuation_id,
        "child_continuation_root": window[-1].child.continuation_id,
        "generation_before": window[0].parent.generation,
        "generation_after": window[-1].child.generation,
        "receipt_chain_digest": digest(receipts),
        "continuation_chain_digest": digest(roots),
    }
    return {**body, "authorization_id": digest(body)}


def verify() -> dict[str, Any]:
    _program, _memory, rows = trace()
    op = operational_table()
    table = op["table"]
    action_table_digest = digest(list(op["records"]))

    artifacts: dict[str, dict[str, Any]] = {}
    authorizations = []
    use_by_artifact: dict[str, list[str]] = defaultdict(list)
    widths = Counter()

    for start in range(len(rows)):
        for width in range(2, min(12, len(rows) - start) + 1):
            naive = tuple((int(x.receipt.route[-1]), 1) for x in rows[start:start + width])
            _target, _algebraic, executable = compile_sequential_macro(naive)
            if len(executable) >= len(naive):
                continue
            naive_st = sequential_steinberg_action(naive, table)
            macro_st = sequential_steinberg_action(executable, table)
            if (naive_st != macro_st).any():
                raise AssertionError("cache candidate changed Steinberg action")
            artifact = build_artifact(
                basis_digest=op["basis_digest"],
                action_table_digest=action_table_digest,
                steinberg_action_digest=digest(naive_st.tolist()),
                executable_word=executable,
                calibration_epoch=CALIBRATION_EPOCH,
            )
            artifacts.setdefault(artifact["artifact_id"], artifact)
            auth = build_authorization(artifact, rows[start:start + width])
            authorizations.append(auth)
            use_by_artifact[artifact["artifact_id"]].append(auth["authorization_id"])
            widths[width] += 1

    if not authorizations:
        raise AssertionError("no cacheable real-trace windows")
    reuse = sorted(
        ({"artifact_id": k, "authorization_count": len(v)} for k, v in use_by_artifact.items()),
        key=lambda x: (-x["authorization_count"], x["artifact_id"]),
    )
    hottest = reuse[0]
    identity_artifacts = [
        a for a in artifacts.values()
        if len(a["executable_time_order"]) == 0
    ]

    process_fields = {
        "process_id", "parent_continuation_root", "child_continuation_root",
        "generation_before", "generation_after", "receipt_chain_digest",
        "continuation_chain_digest", "authorization_id",
    }
    artifact_fields = set().union(*(set(a) for a in artifacts.values()))
    unique_authorizations = len({a["authorization_id"] for a in authorizations}) == len(authorizations)
    checks = {
        "real_trace_has_24_authenticated_steps": len(rows) == 24 and rows[-1].child.state.halted,
        "all_cache_uses_preserve_exact_steinberg_action": True,
        "compiled_artifact_identity_excludes_process_authority": not bool(process_fields & artifact_fields),
        "every_use_has_distinct_process_authorization": unique_authorizations,
        "at_least_one_compiled_artifact_is_reused": hottest["authorization_count"] > 1,
        "identity_control_artifact_is_reused": bool(identity_artifacts) and any(len(use_by_artifact[a["artifact_id"]]) > 1 for a in identity_artifacts),
        "calibration_epoch_is_part_of_artifact_identity": all(a["calibration_epoch"] == CALIBRATION_EPOCH for a in artifacts.values()),
        "symplectic_frame_is_explicitly_committed": all(a["symplectic_frame_digest"] == digest(SYMPLECTIC_FRAME) for a in artifacts.values()),
    }
    out = {
        "schema": "w33.steinberg-control-artifact-cache.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "symplectic_frame": SYMPLECTIC_FRAME,
        "symplectic_frame_digest": digest(SYMPLECTIC_FRAME),
        "calibration_epoch": CALIBRATION_EPOCH,
        "cacheable_window_count": len(authorizations),
        "distinct_compiled_artifacts": len(artifacts),
        "authorization_count": len(authorizations),
        "reuse_ratio": len(authorizations) / len(artifacts),
        "hottest_artifact": hottest,
        "identity_artifact_count": len(identity_artifacts),
        "window_width_histogram": {str(k): widths[k] for k in sorted(widths)},
        "artifact_table_digest": digest(sorted(artifacts.values(), key=lambda x: x["artifact_id"])),
        "authorization_table_digest": digest(authorizations),
        "theorem": (
            "A compiled Steinberg finite-control artifact is safely shareable across distinct authenticated continuation windows exactly when its frame, basis/action table, Steinberg endpoint action, executable time-order word and calibration epoch agree. Process authority remains continuation-specific and is never inferred from cache identity."
        ),
        "boundary": (
            "This is a content-addressed software compilation/cache theorem. The calibration epoch is a namespace for future measured calibration evidence, not evidence that an optical device has been calibrated or that an identity endpoint costs zero physical energy."
        ),
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return out


if __name__ == "__main__":
    result = verify()
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(result["status"] != "PASS")
