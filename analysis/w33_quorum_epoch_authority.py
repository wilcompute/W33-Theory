#!/usr/bin/env python3
"""Byzantine-aware quorum certification for W33 capability epochs.

The earlier signed epoch bus used one Ed25519 issuer.  This module replaces that
single authorization point with a 4-of-5 quorum certificate while preserving the
same immutable EpochTransitionBody and neutral ST81 <-> 36 <-> ST64 transport.

Safety model:
  * n = 5 authority members;
  * threshold t = 4;
  * at most f = 1 Byzantine member;
  * each honest signer votes at most once for a given predecessor/from-state.

Any two 4-of-5 quorums intersect in at least 3 members, so at least 2 members in
the intersection are honest under f <= 1.  Therefore two conflicting certified
successors cannot both be produced without violating the honest one-vote rule.
The implementation also emits explicit fork evidence if conflicting valid quorum
certificates are nevertheless presented.

This is a quorum certificate made of individual Ed25519 signatures, not a
single aggregated threshold-signature scheme and not a wide-area consensus
protocol with view changes/timeouts.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import base64
import hashlib
import json
from typing import Any

from w33_heterogeneous_36_ipc import FiberEndpoint, IPCCapability
from w33_heterogeneous_36_kernel import HeterogeneousKernel36, SharedObjectStore36
from w33_signed_epoch_bus import EpochTransitionBody, canonical
from w33_typed_universal_microvm import Carrier


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


@dataclass(frozen=True)
class MemberSignature:
    member_id: str
    signature_b64: str


@dataclass(frozen=True)
class QuorumCertificate:
    schema: str
    body: EpochTransitionBody
    threshold: int
    population: int
    signatures: tuple[MemberSignature, ...]

    @property
    def certificate_id(self) -> str:
        return digest({
            "schema": self.schema,
            "body": asdict(self.body),
            "threshold": self.threshold,
            "population": self.population,
            "signatures": [asdict(x) for x in self.signatures],
        })

    def descriptor(self) -> dict[str, Any]:
        return {
            "schema": self.schema,
            "body": asdict(self.body),
            "threshold": self.threshold,
            "population": self.population,
            "signatures": [asdict(x) for x in self.signatures],
        }

    @staticmethod
    def from_descriptor(value: dict[str, Any]) -> "QuorumCertificate":
        return QuorumCertificate(
            schema=value["schema"],
            body=EpochTransitionBody(**value["body"]),
            threshold=int(value["threshold"]),
            population=int(value["population"]),
            signatures=tuple(MemberSignature(**x) for x in value["signatures"]),
        )


class QuorumMember:
    def __init__(self, member_id: str, private_key: Any) -> None:
        self.member_id = member_id
        self.private_key = private_key
        self.votes: dict[tuple[Any, ...], str] = {}

    def predecessor_key(self, body: EpochTransitionBody) -> tuple[Any, ...]:
        return (body.issuer, body.from_epoch, body.from_root, body.previous_transition_id)

    def sign(self, body: EpochTransitionBody) -> MemberSignature:
        key = self.predecessor_key(body)
        tid = body.transition_id
        previous = self.votes.get(key)
        if previous is not None and previous != tid:
            raise PermissionError(f"honest member {self.member_id} refuses conflicting successor")
        self.votes[key] = tid
        sig = self.private_key.sign(canonical(asdict(body)))
        return MemberSignature(self.member_id, base64.b64encode(sig).decode("ascii"))


def verify_member_signature(public_key: Any, body: EpochTransitionBody, row: MemberSignature) -> bool:
    try:
        public_key.verify(base64.b64decode(row.signature_b64), canonical(asdict(body)))
        return True
    except Exception:
        return False


def certify(body: EpochTransitionBody, members: list[QuorumMember], threshold: int) -> QuorumCertificate:
    if not (1 <= threshold <= len(members)):
        raise ValueError("invalid quorum threshold")
    rows = tuple(sorted((member.sign(body) for member in members[:threshold]), key=lambda x: x.member_id))
    return QuorumCertificate("w33.capability-epoch-quorum-certificate.v1", body, threshold, len(members), rows)


def verify_certificate(cert: QuorumCertificate, public_keys: dict[str, Any], *, expected_population: int = 5, expected_threshold: int = 4) -> dict[str, Any]:
    unique = {x.member_id for x in cert.signatures}
    signatures_valid = all(
        row.member_id in public_keys and verify_member_signature(public_keys[row.member_id], cert.body, row)
        for row in cert.signatures
    )
    checks = {
        "schema": cert.schema == "w33.capability-epoch-quorum-certificate.v1",
        "population_exact": cert.population == expected_population,
        "threshold_exact": cert.threshold == expected_threshold,
        "unique_signers": len(unique) == len(cert.signatures),
        "quorum_reached": len(unique) >= cert.threshold,
        "all_signatures_valid": signatures_valid,
        "single_generation": cert.body.to_epoch == cert.body.from_epoch + 1,
        "roots_content_addressed": cert.body.from_root.startswith("sha256:") and cert.body.to_root.startswith("sha256:"),
    }
    return {"ok": all(checks.values()), "checks": checks, "signers": sorted(unique)}


def conflict_key(body: EpochTransitionBody) -> tuple[Any, ...]:
    return (body.issuer, body.from_epoch, body.from_root, body.previous_transition_id)


def fork_evidence(a: QuorumCertificate, b: QuorumCertificate, public_keys: dict[str, Any]) -> dict[str, Any] | None:
    va, vb = verify_certificate(a, public_keys), verify_certificate(b, public_keys)
    if not (va["ok"] and vb["ok"]):
        return None
    if conflict_key(a.body) != conflict_key(b.body) or a.body.transition_id == b.body.transition_id:
        return None
    sa, sb = set(va["signers"]), set(vb["signers"])
    overlap = sorted(sa & sb)
    return {
        "schema": "w33.epoch-quorum-fork-evidence.v1",
        "predecessor": list(conflict_key(a.body)),
        "left_certificate": a.certificate_id,
        "right_certificate": b.certificate_id,
        "left_transition": a.body.transition_id,
        "right_transition": b.body.transition_id,
        "double_signer_candidates": overlap,
        "intersection_size": len(overlap),
        "evidence_digest": digest({"a": a.descriptor(), "b": b.descriptor()}),
    }


class QuorumAuthorityReplica:
    def __init__(self, issuer: str, epoch: int, root: str, public_keys: dict[str, Any]) -> None:
        self.issuer, self.epoch, self.root = issuer, epoch, root
        self.public_keys = dict(public_keys)
        self.last_transition_id: str | None = None
        self.certificates: dict[str, QuorumCertificate] = {}

    def apply(self, cert: QuorumCertificate) -> str:
        verification = verify_certificate(cert, self.public_keys)
        if not verification["ok"]:
            raise PermissionError("epoch quorum certificate invalid")
        body = cert.body
        if body.issuer != self.issuer:
            raise PermissionError("issuer mismatch")
        if body.previous_transition_id != self.last_transition_id:
            raise PermissionError("transition chain mismatch")
        if body.from_epoch != self.epoch or body.from_root != self.root:
            raise PermissionError("stale or conflicting epoch certificate")
        cid = cert.certificate_id
        if cid in self.certificates:
            raise PermissionError("certificate replay")
        self.epoch, self.root = body.to_epoch, body.to_root
        self.last_transition_id = body.transition_id
        self.certificates[cid] = cert
        return cid


def ipc_cap(carrier: Carrier) -> IPCCapability:
    return IPCCapability(carrier, frozenset(range(36)), frozenset({"send", "recv", "ack", "derive"}))


def verify() -> dict[str, Any]:
    try:
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    except Exception as exc:
        return {"schema": "w33.epoch-quorum-certificate-demo.v1", "status": "FAIL", "reason": str(exc)}

    keys = [Ed25519PrivateKey.generate() for _ in range(5)]
    members = [QuorumMember(f"authority-{i}", keys[i]) for i in range(5)]
    pubs = {members[i].member_id: keys[i].public_key() for i in range(5)}
    issuer = "w33-runtime-root"
    r0 = digest({"issuer": issuer, "epoch": 0, "revoked": []})
    r1 = digest({"issuer": issuer, "epoch": 1, "revoked": []})
    body = EpochTransitionBody("w33.capability-epoch-transition.v1", issuer, 0, r0, 1, r1, None)
    cert = certify(body, members, 4)
    certificate_valid = verify_certificate(cert, pubs)

    replica = QuorumAuthorityReplica(issuer, 0, r0, pubs)

    store = SharedObjectStore36()
    kernel = HeterogeneousKernel36(queue_depth=2, object_store=store)
    source = FiberEndpoint(Carrier.CIRCUIT_ST81, 6 * 8 + 1)
    target = FiberEndpoint(Carrier.PAIR_ST64, 6 * 8 + 5)
    handle = store.put(cert.descriptor(), target.carrier, target.base36)
    message = kernel.send(source, ipc_cap(source.carrier), target.carrier, target.base36, handle, nonce="quorum-epoch-1")
    delivered = kernel.recv(target, ipc_cap(target.carrier))
    if delivered is None:
        raise RuntimeError("quorum certificate was not delivered")
    received = QuorumCertificate.from_descriptor(store.read(target, delivered.shared_handle))
    applied = replica.apply(received)

    replay_blocked = False
    try:
        replica.apply(received)
    except PermissionError:
        replay_blocked = True

    insufficient = QuorumCertificate(cert.schema, body, 4, 5, cert.signatures[:3])
    insufficient_blocked = not verify_certificate(insufficient, pubs)["ok"]

    # Honest double-vote prevention.
    conflict = EpochTransitionBody(body.schema, issuer, 0, r0, 1, digest({"fork": 1}), None)
    honest_conflict_blocked = False
    try:
        members[0].sign(conflict)
    except PermissionError:
        honest_conflict_blocked = True

    # Construct explicit forensic fork evidence by modeling compromised signers
    # with fresh signer objects holding the same private keys. This is evidence
    # handling, not a claim the honest implementation would produce the fork.
    compromised = [QuorumMember(f"authority-{i}", keys[i]) for i in range(5)]
    conflict_cert = certify(conflict, compromised, 4)
    fork = fork_evidence(cert, conflict_cert, pubs)

    n, t, f = 5, 4, 1
    minimum_intersection = 2 * t - n
    checks = {
        "four_of_five_certificate_valid": certificate_valid["ok"],
        "quorum_certificate_crosses_neutral_36_bus": delivered.message_id == message.message_id,
        "replica_advances_exact_certified_state": replica.epoch == 1 and replica.root == r1 and applied == cert.certificate_id,
        "certificate_replay_blocked": replay_blocked,
        "three_of_five_is_insufficient": insufficient_blocked,
        "honest_member_refuses_conflicting_vote": honest_conflict_blocked,
        "conflicting_valid_certificates_emit_fork_evidence": fork is not None and fork["intersection_size"] >= minimum_intersection,
        "quorum_intersection_exceeds_byzantine_budget": minimum_intersection == 3 and minimum_intersection > f,
    }
    return {
        "schema": "w33.epoch-quorum-certificate-demo.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "parameters": {"n": n, "threshold": t, "assumed_max_byzantine": f, "minimum_quorum_intersection": minimum_intersection},
        "certificate_id": cert.certificate_id,
        "transition_id": body.transition_id,
        "fork_evidence": fork,
        "checks": checks,
        "interpretation": "Capability-epoch rotation is now authorized by a 4-of-5 Ed25519 quorum and transported as one immutable neutral-36 object. Honest members refuse competing successors; conflicting certified histories are converted into explicit fork evidence.",
        "honesty_boundary": "This is quorum certification with a one-vote safety rule, not a complete asynchronous BFT protocol or an aggregated threshold-signature implementation.",
    }


if __name__ == "__main__":
    out = verify()
    print(json.dumps(out, indent=2))
    raise SystemExit(0 if out.get("status") == "PASS" else 1)
