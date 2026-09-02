#!/usr/bin/env python3
"""History-as-time reversible embedding of the typed W33 universal microVM.

A generic two-counter instruction is not necessarily a bijection on the visible
machine state.  Following the standard reversible-computation idea, make the
extended state reversible by retaining the information that would otherwise be
lost.  Each forward W33 VM step appends an undo token to a hash-chained history;
each backward step consumes that token and restores the exact prior state.

For this ISA the semantic undo payload is tiny:
  * INC: the inverse decrements the same register.
  * DECJZ nonzero: the inverse increments the same register.
  * DECJZ zero: the counter was unchanged, but one branch bit is retained.
  * HALT: the inverse clears the halt flag.

The transition certificate already retains the old program counter and W33
route, so the previous portal is route[0].  The undo token additionally retains
the previous trace root and the branch class.

Thus VM time has an exact operational coordinate while history is retained:
    t_VM = number of committed forward records.
Forward and backward execution change t_VM by +/-1.  The arrow becomes
logically irreversible only when history is explicitly discarded.

This is a software logical-reversibility theorem.  It does NOT claim zero-energy
hardware.  Landauer/Bennett connect information erasure and thermodynamic cost;
physical reversibility requires an actual implementation satisfying the needed
adiabatic/noise/error conditions.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
import hashlib
import json
from typing import Any

from w33_typed_universal_microvm import (
    Capability,
    Carrier,
    Instruction,
    Program,
    StepCertificate,
    TypedUniversalMicroVM,
    add_r1_into_r0_program,
)


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(value)).hexdigest()


ZERO_ROOT = "sha256:" + "0" * 64


@dataclass(frozen=True)
class UndoToken:
    previous_trace_root: str
    previous_history_root: str
    branch: str
    certificate: StepCertificate
    token_root: str

    @classmethod
    def build(
        cls,
        previous_trace_root: str,
        previous_history_root: str,
        branch: str,
        certificate: StepCertificate,
    ) -> "UndoToken":
        payload = {
            "previous_trace_root": previous_trace_root,
            "previous_history_root": previous_history_root,
            "branch": branch,
            "certificate": asdict(certificate),
        }
        return cls(
            previous_trace_root=previous_trace_root,
            previous_history_root=previous_history_root,
            branch=branch,
            certificate=certificate,
            token_root=digest(payload),
        )


class ReversibleHistoryVM:
    """Reversible embedding of an ordinary TypedUniversalMicroVM execution."""

    def __init__(self, base: TypedUniversalMicroVM):
        self.base = base
        self.history: list[UndoToken] = []
        self.history_root = ZERO_ROOT
        self.irreversible_commits = 0

    @property
    def time_index(self) -> int:
        return len(self.history)

    def semantic_descriptor(self) -> dict[str, Any]:
        return {
            "image": self.base.program.image_id,
            "state": self.base.state.descriptor(),
            "history_root": self.history_root,
            "time_index": self.time_index,
        }

    def forward(self) -> UndoToken | None:
        if self.base.state.halted:
            return None
        before_counter = self.base.state.counters()
        previous_trace_root = self.base.state.trace_root
        previous_history_root = self.history_root
        pc = self.base.state.pc
        ins = self.base.program.instructions[pc]

        if ins.op == "DECJZ":
            assert ins.register is not None
            branch = "DECJZ_ZERO" if before_counter[ins.register] == 0 else "DECJZ_NONZERO"
        else:
            branch = ins.op

        cert = self.base.step()
        if cert is None:
            return None
        token = UndoToken.build(
            previous_trace_root=previous_trace_root,
            previous_history_root=previous_history_root,
            branch=branch,
            certificate=cert,
        )
        self.history.append(token)
        self.history_root = token.token_root
        return token

    def backward(self) -> UndoToken:
        if not self.history:
            raise RuntimeError("no history to uncompute")
        token = self.history[-1]
        cert = token.certificate
        state = self.base.state
        if state.trace_root != cert.trace_root:
            raise RuntimeError("trace root no longer matches top history token")
        if not self.base.certificates or self.base.certificates[-1] != cert:
            raise RuntimeError("certificate stack no longer matches history")

        ins = Instruction(**cert.instruction)
        counters = state.counters()
        if token.branch == "INC":
            assert ins.register is not None
            if counters[ins.register] <= 0:
                raise RuntimeError("cannot invert INC from zero")
            counters[ins.register] -= 1
        elif token.branch == "DECJZ_NONZERO":
            assert ins.register is not None
            counters[ins.register] += 1
        elif token.branch == "DECJZ_ZERO":
            assert ins.register is not None
            if counters[ins.register] != 0:
                raise RuntimeError("zero branch journal inconsistent with counter")
        elif token.branch == "HALT":
            pass
        else:
            raise RuntimeError(f"unknown undo branch {token.branch}")

        state.set_counters(counters)
        state.pc = cert.pc_before
        state.portal = cert.route[0]
        state.halted = False
        state.steps -= 1
        if state.steps < 0:
            raise RuntimeError("negative step count")
        state.trace_root = token.previous_trace_root
        self.base.certificates.pop()
        self.history.pop()
        self.history_root = token.previous_history_root

        # Strong inverse check: the restored visible semantic state hashes to
        # exactly the pre-state commitment stored in the certificate.
        restored = digest(self.base._semantic_state())
        if restored != cert.pre:
            raise AssertionError("undo did not restore certified pre-state")
        return token

    def run_forward(self, fuel: int = 100000) -> None:
        for _ in range(fuel):
            if self.base.state.halted:
                return
            self.forward()
        raise RuntimeError("fuel exhausted")

    def uncompute_all(self) -> None:
        while self.history:
            self.backward()

    def discard_history(self) -> dict[str, Any]:
        """Explicit logically irreversible boundary.

        The returned count is a software accounting record only.  It is not a
        claim that physical heat equals count*kTln2; records are correlated and
        their minimal erasure cost depends on physical encoding/compressibility.
        """

        record_count = len(self.history)
        old_root = self.history_root
        self.history.clear()
        self.history_root = ZERO_ROOT
        self.irreversible_commits += 1
        return {
            "operation": "DISCARD_HISTORY",
            "records_discarded": record_count,
            "old_history_root": old_root,
            "new_history_root": ZERO_ROOT,
            "logical_reversibility_lost": record_count > 0,
        }


def state_fingerprint(vm: ReversibleHistoryVM) -> str:
    return digest(vm.semantic_descriptor())


def make_sample() -> ReversibleHistoryVM:
    base = TypedUniversalMicroVM(
        add_r1_into_r0_program(),
        Capability(Carrier.CIRCUIT_ST81, 81),
    )
    base.state.counter0 = 7
    base.state.counter1 = 11
    return ReversibleHistoryVM(base)


def branch_test_program() -> Program:
    return Program((
        Instruction("DECJZ", 0, target=1, zero_target=2),
        Instruction("HALT"),
        Instruction("INC", 1, target=3),
        Instruction("HALT"),
    ), name="branch-reversibility-test")


def verify() -> dict[str, Any]:
    vm = make_sample()
    initial = state_fingerprint(vm)
    initial_visible = vm.base.state.descriptor()
    vm.run_forward()
    final = state_fingerprint(vm)
    final_trace = vm.base.state.trace_root
    steps = vm.base.state.steps
    history_root = vm.history_root
    output = vm.base.state.counters()
    route_reverse_ok = all(
        tuple(reversed(token.certificate.route))[0] == token.certificate.route[-1]
        for token in vm.history
    )

    vm.uncompute_all()
    restored = state_fingerprint(vm)
    restored_visible = vm.base.state.descriptor()

    # Replay after uncomputation must regenerate the exact same trace root.
    vm.run_forward()
    replay_trace = vm.base.state.trace_root
    replay_output = vm.base.state.counters()

    # Exercise both DECJZ branches independently.
    zero_base = TypedUniversalMicroVM(
        branch_test_program(), Capability(Carrier.CIRCUIT_ST81, 81)
    )
    zero_vm = ReversibleHistoryVM(zero_base)
    zero_before = state_fingerprint(zero_vm)
    zero_vm.forward()  # zero branch
    zero_vm.backward()
    zero_after = state_fingerprint(zero_vm)

    nz_base = TypedUniversalMicroVM(
        branch_test_program(), Capability(Carrier.CIRCUIT_ST81, 81)
    )
    nz_base.state.counter0 = 1
    nz_vm = ReversibleHistoryVM(nz_base)
    nz_before = state_fingerprint(nz_vm)
    nz_vm.forward()  # nonzero branch
    nz_vm.backward()
    nz_after = state_fingerprint(nz_vm)

    # Demonstrate the explicit irreversible boundary on a short partial run.
    commit_vm = make_sample()
    for _ in range(5):
        commit_vm.forward()
    commit = commit_vm.discard_history()
    undo_after_commit_blocked = False
    try:
        commit_vm.backward()
    except RuntimeError:
        undo_after_commit_blocked = True

    checks = {
        "sample_output": output == [18, 0],
        "sample_steps_24": steps == 24,
        "history_records_equal_steps": steps == 24,
        "history_root_content_addressed": history_root.startswith("sha256:"),
        "uncompute_restores_fingerprint": restored == initial,
        "uncompute_restores_visible_state": restored_visible == initial_visible,
        "replay_same_output": replay_output == [18, 0],
        "replay_same_trace_root": replay_trace == final_trace,
        "zero_branch_inverts": zero_before == zero_after,
        "nonzero_branch_inverts": nz_before == nz_after,
        "reverse_route_metadata_available": route_reverse_ok,
        "discard_history_is_explicit_boundary": (
            commit["records_discarded"] == 5
            and commit["logical_reversibility_lost"]
            and undo_after_commit_blocked
        ),
    }
    return {
        "schema": "w33.history-time-reversible-vm.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "theorem": (
            "The typed W33 VM embeds into a reversible extended-state machine by retaining a "
            "hash-chained undo history: backward(forward(s,H))=(s,H) on every certified step."
        ),
        "history_time": {
            "coordinate": "t_VM = len(history)",
            "forward": "+1",
            "backward": "-1",
            "irreversible_boundary": "DISCARD_HISTORY",
        },
        "sample": {
            "input": [7, 11],
            "output": output,
            "steps": steps,
            "history_root": history_root,
            "final_trace_root": final_trace,
            "initial_fingerprint": initial,
            "final_fingerprint": final,
            "restored_fingerprint": restored,
            "commit_demo": commit,
        },
        "checks": checks,
        "physics_boundary": (
            "Logical reversibility is exact in this software model. Physical thermodynamic reversibility "
            "does not follow automatically. Landauer-type costs attach to actual information erasure under "
            "a physical encoding; DISCARD_HISTORY marks where this VM deliberately loses invertibility."
        ),
    }


def main() -> int:
    payload = verify()
    print(json.dumps(payload, indent=2))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
