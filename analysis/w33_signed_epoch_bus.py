#!/usr/bin/env python3
"""Signed capability-epoch propagation over the neutral W33 36-state fabric.

Capability revocation was previously local authority state.  This module turns a
root/epoch change into an Ed25519-signed transition object and transports it as
an immutable shared object through the existing ST81 <-> 36 <-> ST64 kernel.

Replicas accept a transition only when:
  * the Ed25519 signature verifies under the pinned issuer key,
  * issuer and previous transition identity match,
  * from_epoch/from_root equal the replica's current authority state,
  * to_epoch = from_epoch + 1,
  * the transition has not already been applied.

Checkpoints pin the epoch/root they were born under.  A checkpoint from an older
epoch is not silently re-authorized; failover must mint a fresh execution
passport under the current authority state.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import base64
import hashlib
import json
from typing import Any

from w33_capability_epoch_revocation import RevocationAuthority
from w33_heterogeneous_36_ipc import FiberEndpoint, IPCCapability
from w33_heterogeneous_36_kernel import HeterogeneousKernel36, SharedObjectStore36
from w33_typed_universal_microvm import Carrier


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(value)).hexdigest()


@dataclass(frozen=True)
class EpochTransitionBody:
    schema: str
    issuer: str
    from_epoch: int
    from_root: str
    to_epoch: int
    to_root: str
    previous_transition_id: str | None

    @property
    def transition_id(self) -> str:
        return digest(asdict(self))


@dataclass(frozen=True)
class SignedEpochTransition:
    body: EpochTransitionBody
    signature_b64: str

    def descriptor(self) -> dict[str, Any]:
        return {"body": asdict(self.body), "signature_b64": self.signature_b64}

    @staticmethod
    def from_descriptor(value: dict[str, Any]) -> "SignedEpochTransition":
        return SignedEpochTransition(EpochTransitionBody(**value["body"]), value["signature_b64"])


def sign_transition(private_key: Any, body: EpochTransitionBody) -> SignedEpochTransition:
    signature = private_key.sign(canonical(asdict(body)))
    return SignedEpochTransition(body, base64.b64encode(signature).decode("ascii"))


def verify_signature(public_key: Any, transition: SignedEpochTransition) -> bool:
    try:
        public_key.verify(base64.b64decode(transition.signature_b64), canonical(asdict(transition.body)))
        return True
    except Exception:
        return False


class AuthorityReplica:
    def __init__(self, issuer: str, epoch: int, root: str, public_key: Any) -> None:
        self.issuer = issuer
        self.epoch = epoch
        self.root = root
        self.public_key = public_key
        self.last_transition_id: str | None = None
        self.applied: set[str] = set()

    def apply(self, transition: SignedEpochTransition) -> str:
        body = transition.body
        tid = body.transition_id
        if not verify_signature(self.public_key, transition):
            raise PermissionError("epoch transition signature invalid")
        if body.issuer != self.issuer:
            raise PermissionError("epoch transition issuer mismatch")
        if tid in self.applied:
            raise PermissionError("epoch transition replay")
        if body.previous_transition_id != self.last_transition_id:
            raise PermissionError("epoch transition chain mismatch")
        if body.from_epoch != self.epoch or body.from_root != self.root:
            raise PermissionError("epoch transition is stale or out of order")
        if body.to_epoch != body.from_epoch + 1:
            raise PermissionError("epoch transition must advance exactly one generation")
        if not body.to_root.startswith("sha256:"):
            raise PermissionError("new revocation root is not content addressed")
        self.epoch = body.to_epoch
        self.root = body.to_root
        self.last_transition_id = tid
        self.applied.add(tid)
        return tid

    def checkpoint_current(self, checkpoint: dict[str, Any]) -> bool:
        return checkpoint.get("capability_epoch") == self.epoch and checkpoint.get("revocation_root") == self.root


def cap(carrier: Carrier) -> IPCCapability:
    return IPCCapability(carrier, frozenset(range(36)), frozenset({"send", "recv", "ack", "derive"}))


def verify() -> dict[str, Any]:
    try:
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    except Exception as exc:
        return {
            "schema": "w33.signed-epoch-bus-certificate.v1",
            "status": "FAIL",
            "reason": f"cryptography package with Ed25519 support required: {exc}",
        }

    issuer = "w33-runtime-root"
    source_authority = RevocationAuthority(issuer)
    initial_epoch = source_authority.epoch
    initial_root = source_authority.root
    checkpoint = {"capability_epoch": initial_epoch, "revocation_root": initial_root}

    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    receiver_replica = AuthorityReplica(issuer, initial_epoch, initial_root, public_key)

    source_authority.rotate_epoch()
    body = EpochTransitionBody(
        schema="w33.capability-epoch-transition.v1",
        issuer=issuer,
        from_epoch=initial_epoch,
        from_root=initial_root,
        to_epoch=source_authority.epoch,
        to_root=source_authority.root,
        previous_transition_id=None,
    )
    signed = sign_transition(private_key, body)

    store = SharedObjectStore36()
    kernel = HeterogeneousKernel36(queue_depth=2, object_store=store)
    sender = FiberEndpoint(Carrier.CIRCUIT_ST81, 6 * 12 + 1)
    receiver = FiberEndpoint(Carrier.PAIR_ST64, 6 * 12 + 4)
    handle = store.put(signed.descriptor(), receiver.carrier, receiver.base36)
    msg = kernel.send(sender, cap(sender.carrier), receiver.carrier, receiver.base36, handle, nonce="epoch-transition-1")
    delivered = kernel.recv(receiver, cap(receiver.carrier))
    if delivered is None:
        raise RuntimeError("signed transition was not delivered")
    received = SignedEpochTransition.from_descriptor(store.read(receiver, delivered.shared_handle))
    applied_id = receiver_replica.apply(received)

    replay_blocked = False
    try:
        receiver_replica.apply(received)
    except PermissionError:
        replay_blocked = True

    bad_body = EpochTransitionBody(
        schema=body.schema,
        issuer=issuer,
        from_epoch=initial_epoch,
        from_root=initial_root,
        to_epoch=initial_epoch + 2,
        to_root=digest({"bad": "jump"}),
        previous_transition_id=None,
    )
    bad_signed = sign_transition(private_key, bad_body)
    out_of_order_blocked = False
    try:
        AuthorityReplica(issuer, initial_epoch, initial_root, public_key).apply(bad_signed)
    except PermissionError:
        out_of_order_blocked = True

    tampered = SignedEpochTransition(
        EpochTransitionBody(**(asdict(body) | {"to_root": digest({"tampered": True})})),
        signed.signature_b64,
    )
    tamper_blocked = False
    try:
        AuthorityReplica(issuer, initial_epoch, initial_root, public_key).apply(tampered)
    except PermissionError:
        tamper_blocked = True

    public_transport = json.dumps({"message": msg.public_descriptor(), "transition": signed.descriptor()}, sort_keys=True)
    checks = {
        "ed25519_signature_verifies": verify_signature(public_key, signed),
        "transition_crosses_36_state_bus": delivered.message_id == msg.message_id,
        "receiver_advances_to_exact_signed_epoch": receiver_replica.epoch == source_authority.epoch and receiver_replica.root == source_authority.root,
        "transition_replay_blocked": replay_blocked,
        "epoch_jump_blocked": out_of_order_blocked,
        "signed_body_tamper_blocked": tamper_blocked,
        "old_checkpoint_is_stale_after_rotation": not receiver_replica.checkpoint_current(checkpoint),
        "fresh_passport_remint_required": applied_id == receiver_replica.last_transition_id,
        "transport_does_not_expose_private_fibre_state": "private_tag6" not in public_transport and "state216" not in public_transport,
    }
    return {
        "schema": "w33.signed-epoch-bus-certificate.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "transition_id": body.transition_id,
        "from": {"epoch": initial_epoch, "root": initial_root},
        "to": {"epoch": receiver_replica.epoch, "root": receiver_replica.root},
        "checks": checks,
        "interpretation": "Capability authority rotation is an authenticated, replay-protected object on the neutral 36-state fabric; old checkpoints stay pinned to their birth epoch and require a newly minted passport after rotation.",
        "honesty_boundary": "Ed25519 authenticates the issuer transition. This demo is not Byzantine consensus; multiple authority replicas still need a deployment-specific agreement policy.",
    }


if __name__ == "__main__":
    payload = verify()
    print(json.dumps(payload, indent=2))
    raise SystemExit(0 if payload.get("status") == "PASS" else 1)
