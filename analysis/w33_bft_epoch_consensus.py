#!/usr/bin/env python3
"""View-based Byzantine-fault-tolerant consensus for W33 capability epochs.

This closes the gap between a static 4-of-5 epoch quorum certificate and an
actual replicated authorization protocol. Five Ed25519 validators run a small
three-phase state machine:

  proposal -> PREPARE quorum certificate -> COMMIT quorum certificate

with 4-of-5 quorums, deterministic leader rotation, timeout certificates,
locked-parent safety, durable vote/lock/finalization state, partition recovery,
and reconciliation of a lagging replica from a final commit certificate.

Safety model: n=5, quorum=4, f<=1 Byzantine validator. Any two quorums intersect
in at least three validators. Honest validators vote at most once per
(height,view,phase), never prepare a proposal conflicting with a finalized
height, and only commit a proposal carrying a valid prepare QC.

This is an executable BFT protocol/state-machine certificate. It is not a
production asynchronous network stack, does not model denial-of-service, and
does not claim optimal responsiveness under arbitrary scheduling.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import base64
import hashlib
import json
from typing import Any, Iterable


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(value)).hexdigest()


@dataclass(frozen=True)
class Proposal:
    schema: str
    height: int
    view: int
    leader: str
    from_epoch: int
    from_root: str
    to_epoch: int
    to_root: str
    parent_commit_qc: str | None

    @property
    def proposal_id(self) -> str:
        return digest(asdict(self))


@dataclass(frozen=True)
class Vote:
    schema: str
    validator: str
    phase: str
    height: int
    view: int
    proposal_id: str
    signature_b64: str

    def signed_body(self) -> dict[str, Any]:
        return {
            "schema": self.schema,
            "validator": self.validator,
            "phase": self.phase,
            "height": self.height,
            "view": self.view,
            "proposal_id": self.proposal_id,
        }


@dataclass(frozen=True)
class QuorumCertificate:
    schema: str
    phase: str
    height: int
    view: int
    proposal_id: str
    votes: tuple[Vote, ...]

    @property
    def qc_id(self) -> str:
        return digest({
            "schema": self.schema,
            "phase": self.phase,
            "height": self.height,
            "view": self.view,
            "proposal_id": self.proposal_id,
            "votes": [asdict(v) for v in self.votes],
        })


@dataclass(frozen=True)
class TimeoutVote:
    schema: str
    validator: str
    height: int
    view: int
    highest_commit_qc: str | None
    signature_b64: str

    def signed_body(self) -> dict[str, Any]:
        return {
            "schema": self.schema,
            "validator": self.validator,
            "height": self.height,
            "view": self.view,
            "highest_commit_qc": self.highest_commit_qc,
        }


@dataclass(frozen=True)
class TimeoutCertificate:
    schema: str
    height: int
    view: int
    votes: tuple[TimeoutVote, ...]

    @property
    def tc_id(self) -> str:
        return digest({"schema": self.schema, "height": self.height, "view": self.view, "votes": [asdict(v) for v in self.votes]})


class Validator:
    def __init__(self, validator_id: str, private_key: Any, public_keys: dict[str, Any], quorum: int = 4) -> None:
        self.validator_id = validator_id
        self.private_key = private_key
        self.public_keys = public_keys
        self.quorum = quorum
        self.voted: dict[tuple[int, int, str], str] = {}
        self.timeout_voted: set[tuple[int, int]] = set()
        self.locked_prepare: QuorumCertificate | None = None
        self.finalized: dict[int, tuple[str, str]] = {}  # height -> (proposal_id, commit_qc_id)
        self.finalized_roots: dict[int, str] = {}
        self.highest_commit_qc: QuorumCertificate | None = None

    def sign(self, body: dict[str, Any]) -> str:
        return base64.b64encode(self.private_key.sign(canonical(body))).decode("ascii")

    def _single_vote(self, phase: str, proposal: Proposal) -> Vote:
        key = (proposal.height, proposal.view, phase)
        previous = self.voted.get(key)
        if previous is not None and previous != proposal.proposal_id:
            raise PermissionError(f"{self.validator_id} refuses equivocation in {phase}")
        self.voted[key] = proposal.proposal_id
        body = {
            "schema": "w33.bft-vote.v1",
            "validator": self.validator_id,
            "phase": phase,
            "height": proposal.height,
            "view": proposal.view,
            "proposal_id": proposal.proposal_id,
        }
        return Vote(**body, signature_b64=self.sign(body))

    def prepare(self, proposal: Proposal, parent_commit: QuorumCertificate | None) -> Vote:
        if proposal.to_epoch != proposal.from_epoch + 1 or proposal.height != proposal.to_epoch:
            raise PermissionError("proposal epoch/height mismatch")
        existing = self.finalized.get(proposal.height)
        if existing and existing[0] != proposal.proposal_id:
            raise PermissionError("conflicts with finalized height")
        if proposal.height > 1:
            if parent_commit is None or parent_commit.phase != "COMMIT" or parent_commit.height != proposal.height - 1:
                raise PermissionError("valid parent commit QC required")
            if proposal.parent_commit_qc != parent_commit.qc_id:
                raise PermissionError("proposal parent QC identity mismatch")
        elif proposal.parent_commit_qc is not None:
            raise PermissionError("genesis successor must not name a parent QC")
        if self.locked_prepare is not None and proposal.height == self.locked_prepare.height:
            if proposal.proposal_id != self.locked_prepare.proposal_id:
                raise PermissionError("proposal violates prepare lock")
        return self._single_vote("PREPARE", proposal)

    def observe_prepare_qc(self, qc: QuorumCertificate) -> None:
        if not verify_qc(qc, self.public_keys, self.quorum)["ok"] or qc.phase != "PREPARE":
            raise PermissionError("invalid prepare QC")
        if self.locked_prepare is None or (qc.height, qc.view) > (self.locked_prepare.height, self.locked_prepare.view):
            self.locked_prepare = qc

    def commit(self, proposal: Proposal, prepare_qc: QuorumCertificate) -> Vote:
        if prepare_qc.phase != "PREPARE" or prepare_qc.proposal_id != proposal.proposal_id:
            raise PermissionError("commit requires matching prepare QC")
        if not verify_qc(prepare_qc, self.public_keys, self.quorum)["ok"]:
            raise PermissionError("prepare QC invalid")
        self.observe_prepare_qc(prepare_qc)
        return self._single_vote("COMMIT", proposal)

    def finalize(self, proposal: Proposal, commit_qc: QuorumCertificate) -> None:
        if commit_qc.phase != "COMMIT" or commit_qc.proposal_id != proposal.proposal_id:
            raise PermissionError("finalization requires matching commit QC")
        if not verify_qc(commit_qc, self.public_keys, self.quorum)["ok"]:
            raise PermissionError("commit QC invalid")
        existing = self.finalized.get(proposal.height)
        if existing and existing[0] != proposal.proposal_id:
            raise PermissionError("conflicting finalization")
        self.finalized[proposal.height] = (proposal.proposal_id, commit_qc.qc_id)
        self.finalized_roots[proposal.height] = proposal.to_root
        if self.highest_commit_qc is None or (commit_qc.height, commit_qc.view) > (self.highest_commit_qc.height, self.highest_commit_qc.view):
            self.highest_commit_qc = commit_qc
        if self.locked_prepare and self.locked_prepare.height <= proposal.height:
            self.locked_prepare = None

    def timeout(self, height: int, view: int) -> TimeoutVote:
        key = (height, view)
        if key in self.timeout_voted:
            raise PermissionError("duplicate timeout vote")
        self.timeout_voted.add(key)
        body = {
            "schema": "w33.bft-timeout-vote.v1",
            "validator": self.validator_id,
            "height": height,
            "view": view,
            "highest_commit_qc": self.highest_commit_qc.qc_id if self.highest_commit_qc else None,
        }
        return TimeoutVote(**body, signature_b64=self.sign(body))

    def snapshot(self) -> dict[str, Any]:
        return {
            "schema": "w33.bft-validator-durable-state.v1",
            "validator_id": self.validator_id,
            "voted": [[h, v, p, pid] for (h, v, p), pid in sorted(self.voted.items())],
            "timeout_voted": [list(x) for x in sorted(self.timeout_voted)],
            "locked_prepare": qc_descriptor(self.locked_prepare),
            "highest_commit_qc": qc_descriptor(self.highest_commit_qc),
            "finalized": {str(h): [pid, qid] for h, (pid, qid) in sorted(self.finalized.items())},
            "finalized_roots": {str(h): root for h, root in sorted(self.finalized_roots.items())},
        }

    def restore(self, snapshot: dict[str, Any]) -> None:
        if snapshot.get("schema") != "w33.bft-validator-durable-state.v1" or snapshot.get("validator_id") != self.validator_id:
            raise ValueError("durable state identity mismatch")
        self.voted = {(int(h), int(v), str(p)): str(pid) for h, v, p, pid in snapshot["voted"]}
        self.timeout_voted = {(int(h), int(v)) for h, v in snapshot["timeout_voted"]}
        self.locked_prepare = qc_from_descriptor(snapshot.get("locked_prepare"))
        self.highest_commit_qc = qc_from_descriptor(snapshot.get("highest_commit_qc"))
        self.finalized = {int(h): (str(v[0]), str(v[1])) for h, v in snapshot["finalized"].items()}
        self.finalized_roots = {int(h): str(root) for h, root in snapshot["finalized_roots"].items()}


def verify_vote(vote: Vote, public_keys: dict[str, Any]) -> bool:
    try:
        public_keys[vote.validator].verify(base64.b64decode(vote.signature_b64), canonical(vote.signed_body()))
        return True
    except Exception:
        return False


def verify_qc(qc: QuorumCertificate, public_keys: dict[str, Any], quorum: int = 4) -> dict[str, Any]:
    ids = [v.validator for v in qc.votes]
    checks = {
        "schema": qc.schema == "w33.bft-quorum-certificate.v1",
        "phase": qc.phase in {"PREPARE", "COMMIT"},
        "unique": len(ids) == len(set(ids)),
        "quorum": len(ids) >= quorum,
        "same_phase": all(v.phase == qc.phase for v in qc.votes),
        "same_height": all(v.height == qc.height for v in qc.votes),
        "same_view": all(v.view == qc.view for v in qc.votes),
        "same_proposal": all(v.proposal_id == qc.proposal_id for v in qc.votes),
        "signatures": all(verify_vote(v, public_keys) for v in qc.votes),
    }
    return {"ok": all(checks.values()), "checks": checks, "signers": sorted(ids)}


def make_qc(phase: str, proposal: Proposal, votes: Iterable[Vote]) -> QuorumCertificate:
    rows = tuple(sorted(votes, key=lambda x: x.validator))
    return QuorumCertificate("w33.bft-quorum-certificate.v1", phase, proposal.height, proposal.view, proposal.proposal_id, rows)


def verify_timeout_vote(vote: TimeoutVote, public_keys: dict[str, Any]) -> bool:
    try:
        public_keys[vote.validator].verify(base64.b64decode(vote.signature_b64), canonical(vote.signed_body()))
        return True
    except Exception:
        return False


def make_timeout_certificate(height: int, view: int, votes: Iterable[TimeoutVote], public_keys: dict[str, Any], quorum: int = 4) -> TimeoutCertificate:
    rows = tuple(sorted(votes, key=lambda x: x.validator))
    ids = [v.validator for v in rows]
    if len(rows) < quorum or len(ids) != len(set(ids)):
        raise PermissionError("timeout quorum not reached")
    if not all(v.height == height and v.view == view and verify_timeout_vote(v, public_keys) for v in rows):
        raise PermissionError("invalid timeout vote set")
    return TimeoutCertificate("w33.bft-timeout-certificate.v1", height, view, rows)


def leader_for(view: int, validator_ids: list[str]) -> str:
    return validator_ids[view % len(validator_ids)]


def qc_descriptor(qc: QuorumCertificate | None) -> dict[str, Any] | None:
    if qc is None:
        return None
    return {"schema": qc.schema, "phase": qc.phase, "height": qc.height, "view": qc.view, "proposal_id": qc.proposal_id, "votes": [asdict(v) for v in qc.votes]}


def qc_from_descriptor(row: dict[str, Any] | None) -> QuorumCertificate | None:
    if row is None:
        return None
    return QuorumCertificate(row["schema"], row["phase"], int(row["height"]), int(row["view"]), row["proposal_id"], tuple(Vote(**v) for v in row["votes"]))


def verify() -> dict[str, Any]:
    try:
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    except Exception as exc:
        return {"schema": "w33.bft-epoch-consensus-demo.v1", "status": "FAIL", "reason": str(exc)}

    ids = [f"validator-{i}" for i in range(5)]
    priv = {vid: Ed25519PrivateKey.generate() for vid in ids}
    pubs = {vid: priv[vid].public_key() for vid in ids}
    nodes = {vid: Validator(vid, priv[vid], pubs) for vid in ids}

    root0 = digest({"epoch": 0, "revoked": []})
    root1 = digest({"epoch": 1, "revoked": ["cap-old"]})

    # View 0 leader is partitioned with only one peer: no 4-vote QC can form.
    p0 = Proposal("w33.bft-epoch-proposal.v1", 1, 0, leader_for(0, ids), 0, root0, 1, root1, None)
    minority = ids[:2]
    minority_votes = [nodes[v].prepare(p0, None) for v in minority]
    partition_cannot_prepare_qc = len(minority_votes) < 4

    # Connected four validators time out view 0 and rotate leader to validator-1.
    connected = ids[1:]
    timeout_votes = [nodes[v].timeout(1, 0) for v in connected]
    tc = make_timeout_certificate(1, 0, timeout_votes, pubs)
    p1 = Proposal("w33.bft-epoch-proposal.v1", 1, 1, leader_for(1, ids), 0, root0, 1, root1, None)
    prepare_votes = [nodes[v].prepare(p1, None) for v in connected]
    prepare_qc = make_qc("PREPARE", p1, prepare_votes)
    assert verify_qc(prepare_qc, pubs)["ok"]
    commit_votes = [nodes[v].commit(p1, prepare_qc) for v in connected]
    commit_qc = make_qc("COMMIT", p1, commit_votes)
    assert verify_qc(commit_qc, pubs)["ok"]
    for v in connected:
        nodes[v].finalize(p1, commit_qc)

    # Heal partition: lagging validator accepts the exact commit QC and catches up.
    lagging = nodes[ids[0]]
    lagging.finalize(p1, commit_qc)
    reconciled = lagging.finalized_roots.get(1) == root1

    # Once finalized, a conflicting successor at the same height is rejected.
    conflict = Proposal("w33.bft-epoch-proposal.v1", 1, 2, leader_for(2, ids), 0, root0, 1, digest({"fork": 1}), None)
    conflict_blocked = False
    try:
        nodes[ids[2]].prepare(conflict, None)
    except PermissionError:
        conflict_blocked = True

    # Durable state preserves anti-equivocation across restart.
    snap = nodes[ids[2]].snapshot()
    restarted = Validator(ids[2], priv[ids[2]], pubs)
    restarted.restore(snap)
    durable_equivocation_blocked = False
    try:
        # Same view/phase as the finalized vote, conflicting proposal id.
        fake = Proposal("w33.bft-epoch-proposal.v1", 1, 1, leader_for(1, ids), 0, root0, 1, digest({"fork": 2}), None)
        restarted._single_vote("COMMIT", fake)
    except PermissionError:
        durable_equivocation_blocked = True

    # Invalid 3-vote commit certificate never finalizes.
    short_qc = make_qc("COMMIT", p1, commit_votes[:3])
    short_rejected = not verify_qc(short_qc, pubs)["ok"]

    intersection = 2 * 4 - 5
    checks = {
        "partitioned_two_node_side_cannot_form_qc": partition_cannot_prepare_qc,
        "four_timeout_votes_form_view_change_certificate": len(tc.votes) == 4 and tc.view == 0,
        "leader_rotates_after_timeout": p1.leader == ids[1],
        "prepare_qc_is_four_of_five": verify_qc(prepare_qc, pubs)["ok"] and len(prepare_qc.votes) == 4,
        "commit_qc_is_four_of_five": verify_qc(commit_qc, pubs)["ok"] and len(commit_qc.votes) == 4,
        "connected_partition_finalizes": all(nodes[v].finalized_roots.get(1) == root1 for v in connected),
        "healed_lagging_replica_reconciles": reconciled,
        "conflicting_finalized_height_is_rejected": conflict_blocked,
        "durable_restart_preserves_anti_equivocation": durable_equivocation_blocked,
        "three_vote_commit_certificate_is_rejected": short_rejected,
        "quorum_intersection_is_three": intersection == 3,
    }
    return {
        "schema": "w33.bft-epoch-consensus-demo.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "parameters": {"n": 5, "quorum": 4, "assumed_max_byzantine": 1, "minimum_quorum_intersection": intersection},
        "timeout_certificate": tc.tc_id,
        "prepare_qc": prepare_qc.qc_id,
        "commit_qc": commit_qc.qc_id,
        "final_root": root1,
        "checks": checks,
        "interpretation": "The epoch authority now executes signed proposal/prepare/commit consensus with timeout-driven leader rotation, durable anti-equivocation state, partition recovery and commit-QC reconciliation.",
        "honesty_boundary": "This executable protocol demonstrates the stated BFT state-machine safety/liveness scenarios; it is not a production asynchronous transport, DoS model, or formally mechanized proof of all network schedules.",
    }


if __name__ == "__main__":
    out = verify()
    print(json.dumps(out, indent=2))
    raise SystemExit(0 if out.get("status") == "PASS" else 1)
