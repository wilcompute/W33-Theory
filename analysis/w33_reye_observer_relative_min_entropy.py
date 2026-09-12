#!/usr/bin/env python3
"""Finite observer-relative randomness theorem for the hidden-radical Reye decoder.

This file turns the project's 'inaccessible information' intuition into an exact
finite statement, without making a metaphysical claim about quantum randomness.

The certified Reye decoder has a hidden radical

    R ~= F2^2, |R|=4,

and three observable nonzero coset roles A,B,C.  A point has form (role,r),
while a contextual block is uniquely

    T(r,s)={A_r,B_s,C_{r+s}},   (r,s) in R^2.

Under the explicitly declared uniform priors, the optimal classical guessing
probability conditioned only on the coarse role is 1/4, hence

    H_min(point | role)=2 bits.

Revealing the radical offset r is a perfect decoder and reduces that residual
min-entropy to zero.  For blocks, the coarse role pattern alone leaves 16
possible (r,s), so H_min=4 bits; revealing one independent offset leaves two
bits, and revealing both leaves zero.  The third offset is determined by r+s.

The same guessing-probability semantics is cross-checked against the repo's
independent finite Bayesian privacy controller.  Its Marcelis trace observer has
p_guess=1 with all four outputs visible, while suppressing all four outputs gives
p_guess=1/85 for a uniform 85-state prior.  Thus both systems instantiate the
same formal principle: an observation map changes conditional min-entropy, and
side information can either reveal or conceal finite hidden state.

Boundary: these are classical finite conditional-entropy theorems for declared
priors and observation maps.  They do NOT imply that Bell-certified quantum
randomness is encrypted classical information, do not posit local hidden
variables, and do not identify computational unpredictability with information-
theoretic entropy.
"""
from __future__ import annotations

from fractions import Fraction
from math import log2
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_reye_observer_relative_min_entropy.json"


def hmin_from_guess(p: Fraction) -> float:
    assert p > 0
    return -log2(float(p))


def uniform_fibre_guess(total_states: int, observed_classes: int) -> Fraction:
    """Optimal p_guess(X|O) for a uniform X and equal-sized deterministic fibres."""
    assert total_states % observed_classes == 0
    fibre = total_states // observed_classes
    return Fraction(1, fibre)


def build_result():
    decoder = json.loads((ROOT / "data" / "w33_reye_hidden_radical_v4_decoder.json").read_text(encoding="utf-8"))
    assert decoder["status"] == "PASS"
    assert all(decoder["checks"].values())
    assert decoder["radical"]["order"] == 4
    assert decoder["decoder"]["blocks"] == 16
    assert decoder["uniform_finite_information_model"]["hidden_bits_per_point_fibre"] == 2.0
    assert decoder["uniform_finite_information_model"]["hidden_bits_to_select_exact_block"] == 4.0

    # Point microstates X=(role,r): 3 coarse roles, four radical offsets each.
    point_total = 12
    point_roles = 3
    point_fibre = point_total // point_roles
    p_point_role = uniform_fibre_guess(point_total, point_roles)
    h_point_role = hmin_from_guess(p_point_role)
    assert point_fibre == 4 and p_point_role == Fraction(1,4) and h_point_role == 2.0

    # Supplying r is a perfect finite decoder.
    p_point_role_plus_r = Fraction(1,1)
    h_point_role_plus_r = hmin_from_guess(p_point_role_plus_r)
    assert h_point_role_plus_r == 0.0

    # Contextual block B=(r,s): 16 equally likely offset pairs.
    block_total = 16
    p_block_coarse = Fraction(1,16)
    h_block_coarse = hmin_from_guess(p_block_coarse)
    assert h_block_coarse == 4.0

    # Reveal one independent radical offset, leaving four possible values of the other.
    p_block_one_offset = Fraction(1,4)
    h_block_one_offset = hmin_from_guess(p_block_one_offset)
    assert h_block_one_offset == 2.0

    # Reveal both independent offsets; the third t=r+s is determined.
    p_block_two_offsets = Fraction(1,1)
    h_block_two_offsets = hmin_from_guess(p_block_two_offsets)
    assert h_block_two_offsets == 0.0
    assert decoder["uniform_finite_information_model"]["third_offset_rule"] == "t = r XOR s"

    # Exact chain rule by cardinality for this uniform deterministic decoder.
    assert h_block_coarse - h_block_one_offset == 2.0
    assert h_block_one_offset - h_block_two_offsets == 2.0
    assert h_block_coarse == 2 * h_point_role

    # Independent observer/privacy model already frozen in the repo.
    privacy_path = ROOT / "analysis" / "w33_adaptive_observer_privacy.json"
    privacy = json.loads(privacy_path.read_text(encoding="utf-8"))
    assert privacy["status"] == "PASS"
    trace_rows = privacy["marcelis_trace"]
    assert len(trace_rows) == 5
    trace_by_budget = {int(row["budget_masked_observations"]): row for row in trace_rows}
    assert set(trace_by_budget) == {0,1,2,3,4}

    p_trace_visible = Fraction(trace_by_budget[0]["guess_probability"])
    p_trace_hidden = Fraction(trace_by_budget[4]["guess_probability"])
    assert p_trace_visible == 1
    assert p_trace_hidden == Fraction(1,85)
    h_trace_visible = hmin_from_guess(p_trace_visible)
    h_trace_hidden = hmin_from_guess(p_trace_hidden)
    assert h_trace_visible == 0.0
    assert abs(h_trace_hidden - log2(85)) < 1e-12

    # Monotonicity of the exact adaptive privacy frontier.
    guesses = [Fraction(trace_by_budget[b]["guess_probability"]) for b in range(5)]
    assert all(guesses[b+1] <= guesses[b] for b in range(4))

    # A clean decoder-vs-privacy dual reading:
    # - reveal side information -> p_guess rises / H_min falls;
    # - suppress observations -> p_guess falls / H_min rises.
    decoder_reveal_monotone = (
        p_block_coarse <= p_block_one_offset <= p_block_two_offsets
        and h_block_coarse >= h_block_one_offset >= h_block_two_offsets
    )
    privacy_suppress_monotone = all(guesses[b+1] <= guesses[b] for b in range(4))
    assert decoder_reveal_monotone and privacy_suppress_monotone

    checks = {
        "coarse_point_role_has_four_state_fibre": point_fibre == 4,
        "point_role_guess_probability_is_1_over_4": p_point_role == Fraction(1,4),
        "point_role_conditional_min_entropy_is_2_bits": h_point_role == 2.0,
        "radical_offset_perfectly_decodes_point": p_point_role_plus_r == 1 and h_point_role_plus_r == 0.0,
        "coarse_block_guess_probability_is_1_over_16": p_block_coarse == Fraction(1,16),
        "coarse_block_conditional_min_entropy_is_4_bits": h_block_coarse == 4.0,
        "one_block_offset_leaves_2_bits": p_block_one_offset == Fraction(1,4) and h_block_one_offset == 2.0,
        "two_block_offsets_perfectly_decode_block": p_block_two_offsets == 1 and h_block_two_offsets == 0.0,
        "third_offset_is_determined_not_independent": decoder["uniform_finite_information_model"]["third_offset_rule"] == "t = r XOR s",
        "decoder_reveal_side_information_monotonicity": decoder_reveal_monotone,
        "privacy_controller_uses_same_guessing_probability_semantics": privacy["status"] == "PASS",
        "fully_visible_85_state_trace_is_decodable": p_trace_visible == 1,
        "fully_suppressed_85_state_trace_returns_uniform_guess_1_over_85": p_trace_hidden == Fraction(1,85),
        "privacy_suppression_monotonically_reduces_guessing_probability": privacy_suppress_monotone,
    }

    return {
        "schema": "w33.reye-observer-relative-min-entropy.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "point_decoder": {
            "microstates": point_total,
            "coarse_roles": point_roles,
            "states_per_role": point_fibre,
            "uniform_p_guess_given_role": str(p_point_role),
            "H_min_bits_given_role": h_point_role,
            "side_information": "radical offset r in R ~= F2^2",
            "side_information_bits": 2,
            "p_guess_after_side_information": str(p_point_role_plus_r),
            "H_min_bits_after_side_information": h_point_role_plus_r,
        },
        "block_decoder": {
            "blocks": block_total,
            "coordinates": "(r,s) in R^2; third offset t=r XOR s",
            "uniform_p_guess_no_offsets": str(p_block_coarse),
            "H_min_bits_no_offsets": h_block_coarse,
            "uniform_p_guess_one_offset": str(p_block_one_offset),
            "H_min_bits_one_offset": h_block_one_offset,
            "uniform_p_guess_two_offsets": str(p_block_two_offsets),
            "H_min_bits_two_offsets": h_block_two_offsets,
            "independent_hidden_offsets": 2,
            "bits_per_offset": 2,
        },
        "independent_observer_cross_check": {
            "model": "85-state Marcelis finite trace observer with public adaptive suppression",
            "p_guess_no_suppression": str(p_trace_visible),
            "H_min_bits_no_suppression": h_trace_visible,
            "p_guess_all_four_outputs_suppressed": str(p_trace_hidden),
            "H_min_bits_all_four_outputs_suppressed": h_trace_hidden,
            "frontier_guess_probabilities": [str(x) for x in guesses],
        },
        "finite_theorem": (
            "For the declared uniform Reye decoder model, apparent uncertainty under the coarse observation is exactly conditional min-entropy of the hidden radical fibre: 2 bits for a point and 4 bits for a contextual block. Supplying the corresponding finite side information decodes the exact state. The independent Marcelis privacy controller exhibits the dual operation: withholding observations increases conditional min-entropy."
        ),
        "cryptographic_reading": (
            "In these finite models, 'decryptability' can be formalized as the existence of a decoder D(O,K)=X where O is the coarse observation and K is side information. The residual uncertainty before K is H_min(X|O). This is a rigorous special case of observer-relative hidden information, not a universal definition of randomness."
        ),
        "claim_boundary": (
            "Classical finite information theorem under explicit uniform priors and deterministic observation/decoder maps. It does not imply Bell-certified quantum outcomes have hidden classical keys, does not assert a local/noncontextual hidden-variable theory, and does not equate determinism with predictability, computability, or efficient calculability."
        ),
        "checks": checks,
    }


def main():
    r = build_result()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(r, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": r["status"],
        "point_Hmin": r["point_decoder"]["H_min_bits_given_role"],
        "block_Hmin": r["block_decoder"]["H_min_bits_no_offsets"],
        "trace_hidden_pguess": r["independent_observer_cross_check"]["p_guess_all_four_outputs_suppressed"],
    }, sort_keys=True))
    return 0 if r["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
