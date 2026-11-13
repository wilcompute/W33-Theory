"""Signed knight-board translation lifts and a shared E6 gauge obstruction."""

import json
from itertools import product
from pathlib import Path

import numpy as np

import toe_20261113_exft_lattice_gauge as lattice


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/toe_20261113_knight_translation_flux.json"
IDENTITY = np.eye(16, dtype=np.int64)


def board_mask(x, y):
    gray = (x ^ (x >> 1)) | ((y ^ (y >> 1)) << 2)
    return gray ^ (15 if gray.bit_count() % 2 else 0)


def knight_sign(mask, axis):
    return (-1)**((mask & ((1 << axis)-1)).bit_count())


def lift_translation(board, gammas, dx, dy):
    perm = [board_mask((x+dx) % 4, (y+dy) % 4) for x, y in board]
    axes = [(perm[0] ^ perm[1 << i]).bit_length()-1 for i in range(4)]
    assert sorted(axes) == list(range(4))
    signs = {0: 1}
    queue = [0]
    for mask in queue:
        for i, j in enumerate(axes):
            neighbor = mask ^ (1 << i)
            assert perm[mask] ^ perm[neighbor] == 1 << j
            sign = signs[mask]*knight_sign(mask, i)*knight_sign(perm[mask], j)
            if neighbor in signs:
                assert signs[neighbor] == sign
            else:
                signs[neighbor] = sign
                queue.append(neighbor)
    lift = IDENTITY[:, perm]*[signs[m] for m in range(16)]
    for i, j in enumerate(axes):
        np.testing.assert_array_equal(lift @ gammas[i], gammas[j] @ lift)
    return lift, axes


def calculate():
    board = sorted(product(range(4), repeat=2), key=lambda xy: board_mask(*xy))
    gammas = [IDENTITY[:, np.arange(16) ^ (1 << i)]
              *[knight_sign(m, i) for m in range(16)] for i in range(4)]
    for i, j in product(range(4), repeat=2):
        np.testing.assert_array_equal(gammas[i] @ gammas[j] + gammas[j] @ gammas[i],
                                      2*IDENTITY if i == j else 0*IDENTITY)
    knight_offsets = {(a % 4, b % 4)
                      for a, b in ((1, 2), (-1, 2), (2, 1), (2, -1))}
    for mask, (x, y) in enumerate(board):
        assert {board_mask((x+a) % 4, (y+b) % 4) for a, b in knight_offsets} == {
            mask ^ (1 << i) for i in range(4)
        }
    a, x_axes = lift_translation(board, gammas, 1, 0)
    b, y_axes = lift_translation(board, gammas, 0, 1)
    assert np.array_equal(np.linalg.matrix_power(a, 4), -IDENTITY)
    assert np.array_equal(np.linalg.matrix_power(b, 4), -IDENTITY)
    assert np.array_equal(a @ b, -b @ a)
    assert len({(np.linalg.matrix_power(a, i) @ np.linalg.matrix_power(b, j)*sign).tobytes()
                for i, j, sign in product(range(4), range(4), (-1, 1))}) == 32

    tensor, y_tensor, five, six = lattice.exft.setup()
    section = tuple(sorted(set(five) & set(six)))
    gauge, trivial = lattice.operators(tensor, y_tensor, section)
    # With only two derivatives, DG factors into one coefficient matrix
    # and the commutator of the two site shifts.
    r, s = next((i, j) for i in range(4) for j in range(i+1, 4)
                if (gauge[i] @ trivial[j]).any())
    coefficient = gauge[r] @ trivial[s]
    shift_commutator = a @ b - b @ a
    out, potential = np.argwhere(coefficient)[0]
    site_out, site_in = np.argwhere(shift_commutator)[0]
    defect = int(coefficient[out, potential]*shift_commutator[site_out, site_in])
    assert abs(defect) == 2
    # Squaring both lifts kills the commutator but leaves period-two
    # steps, and can no longer distinguish all original translation modes.
    assert np.array_equal(a @ a @ b @ b, b @ b @ a @ a)
    # A compensating two-component internal action cancels the cocycle.
    swap = np.array([[0, 1], [1, 0]], dtype=np.int64)
    parity = np.diag([1, -1])
    lifted_x = np.kron(a, swap)
    lifted_y = np.kron(b, parity)
    identity32 = np.eye(32, dtype=np.int64)
    np.testing.assert_array_equal(lifted_x @ lifted_y, lifted_y @ lifted_x)
    # Over C one common scalar phase gives both generators period four.
    assert np.array_equal(np.linalg.matrix_power(lifted_x, 4), -identity32)
    assert np.array_equal(np.linalg.matrix_power(lifted_y, 4), -identity32)
    traces = [
        int(np.trace(np.linalg.matrix_power(lifted_x, i) @ np.linalg.matrix_power(lifted_y, j)))
        for i, j in product(range(4), repeat=2)
    ]
    assert traces == [32]+[0]*15
    return dict(status="PASS", board_in_mask_order=board, x_axis_permutation=x_axes,
                y_axis_permutation=y_axes, translation_fourth_powers=[-1, -1],
                translation_commutator_sign=-1, real_lift_group_order=32,
                compensated_translation=dict(internal_dimension=2, complex_period=4,
                                             copies_of_regular_representation=2),
                gauge_defect=dict(derivative_axes=[section[r], section[s]], operator_row=int(out),
                                  potential_component=int(potential), site_in=int(site_in),
                                  site_out=int(site_out), value=defect))


if __name__ == "__main__":
    result = calculate()
    OUT.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(result, indent=2), flush=True)
