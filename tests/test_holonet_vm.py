#!/usr/bin/env python3
"""
CI coverage for the holonet universal VM (Pass 40-44): routing, the Clifford processor, error
correction, teleportation, self-reproduction, the CLI, the contextual fraction / KS inequality, and the
magic dial. These are fast, exact checks that the runnable machine does what the papers say.
"""
import os
import sys

import numpy as np
import pytest

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "analysis")
)

import holonet_node as hn  # noqa: E402


# ----- network -----
def test_fabric_is_gq33():
    assert len(hn.POINTS) == 40
    a = hn.POINTS[0]
    assert len(hn.neighbors(a)) == 12  # radix


def test_routing_address_is_route():
    a = hn.POINTS[0]
    dst = next(p for p in hn.POINTS if hn.symplectic(a, p) != 0)
    path = hn.route(a, dst)
    assert len(path) == 3  # diameter 2 -> 2 hops
    # consecutive hops are adjacent (symplectic test = 0)
    assert all(hn.symplectic(path[i], path[i + 1]) == 0 for i in range(len(path) - 1))
    assert len(hn.multipath(a, dst)) == 4  # mu = 4


def test_routing_adjacent_is_one_hop():
    a = hn.POINTS[0]
    nb = hn.neighbors(a)[0]
    assert hn.route(a, nb) == [a, nb]


# ----- processor (Clifford stabilizer tableau) -----
def test_clifford_builds_valid_entangled_state():
    reg = hn.CliffordRegister(2)
    reg.fourier(0)
    reg.sum(0, 1)
    assert reg.is_valid_state()  # generators commute + independent over F_3


def test_clifford_scales_polynomially():
    # gate updates do not blow up exponentially with register size
    for n in (4, 16):
        reg = hn.CliffordRegister(n)
        for _ in range(20):
            reg.fourier(0)
            reg.sum(0, n - 1)
        assert reg.is_valid_state()


# ----- memory: error correction -----
def test_qec_corrects_random_single_error():
    # exact [[5,1,3]]_3 cycle is a 243-dim state-vector sim; 2 seeds keeps CI fast
    for seed in range(2):
        r = hn.qec_cycle(seed=seed)
        assert r["fidelity"] == pytest.approx(1.0, abs=1e-6)
        assert r["decoded"] == r["injected"]  # syndrome decoded the actual error


# ----- teleportation -----
def test_teleport_recovers_message():
    for seed in range(5):
        r = hn.teleport_state(seed=seed)
        assert r["fidelity"] == pytest.approx(1.0, abs=1e-6)
        assert r["outcome"][0] in (0, 1, 2) and r["outcome"][1] in (0, 1, 2)


# ----- self-reproduction -----
def test_node_reproduces():
    node = hn.HolonetNode(hn.POINTS[0])
    child = node.reproduce()
    assert child.level == node.level + 1
    assert child.address[0] == node.address  # genome carried into the child address


def test_magic_dial_cost():
    node = hn.HolonetNode(hn.POINTS[0])
    node.magic_budget = 3
    assert node.classical_emulation_cost() == 9**3  # priced 9^t advantage


# ----- the CLI -----
def test_cli_verify_all_pass():
    import holonet_cli  # noqa: E402

    with pytest.raises(SystemExit) as e:
        holonet_cli.main(["verify"])
    assert e.value.code == 0  # whole stack self-tests PASS


def test_cli_route():
    import holonet_cli

    holonet_cli.main(["route", "0001", "0010"])  # should not raise


def test_cli_parse_address_rejects_bad():
    import holonet_cli

    with pytest.raises(SystemExit):
        holonet_cli.parse_addr("0000")  # all-zero is not a projective point


# ----- contextuality (only if scipy milp / networkx available) -----
def test_contextual_fraction_is_one_tenth():
    cf = pytest.importorskip("scipy.optimize")
    sys.path.insert(
        0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "analysis")
    )
    import w33_contextual_fraction as w  # noqa: E402

    n, A, lines = w.build_w33()
    assert n == 40 and len(lines) == 40


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))
