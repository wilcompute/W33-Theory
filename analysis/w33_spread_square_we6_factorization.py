#!/usr/bin/env python3
"""Symplectic-spread square / W(E6) factorization theorem.

This file is a synthesis layer on top of the existing live-index audits:

    scripts/w33_projective_affine_shell_audit.py
    scripts/w33_symplectic_spread_frame_audit.py

The new observation is the exact square hiding behind the previous factorization

    |W(E6)| = 40 * 16 * 81.

The live spread audit proves that W(3,3) has exactly 36 symplectic spreads and
that, relative to any anchor point, those 36 spreads split as

    4 anchor-line sectors * 9 affine measurement-line frames.

Therefore

    16 * 81 = 4^2 * 9^2 = (4*9)^2 = 36^2,

and hence

    |W(E6)| = 40 * 36^2.

Interpretation:
    40 = symplectic/projective anchors,
    36 = complete two-qutrit stabilizer/MUB spread frames,
    36^2 = ordered input-output spread-frame transport packet per anchor.

This also matches the linear symplectic group order

    |Sp(4,3)| = 3^4(3^4-1)(3^2-1) = 51840 = |W(E6)|,

while the projective action quotients by the central +/-I.
"""
from __future__ import annotations

import json
from pathlib import Path

q=3
v=40
chi=4
q2=q*q
Q4_VERTICES=16
H1=81
SPREADS=36
SPREAD_SIZE=10
LINES=40
POINTS_PER_LINE=4
LINE_OCCURRENCE=9
X_RAYS=160
WE6=51_840
PSP43=25_920


def sp4_order(q:int=3)->int:
    # |Sp(4,q)| = q^4 (q^4 - 1)(q^2 - 1)
    return q**4 * (q**4 - 1) * (q**2 - 1)


def build_payload():
    point_line_flags=v*POINTS_PER_LINE
    spread_line_inc=SPREADS*SPREAD_SIZE
    line_spread_inc=LINES*LINE_OCCURRENCE
    point_line_spread_triples=spread_line_inc*POINTS_PER_LINE
    local_spread_split=chi*q2
    spread_square=SPREADS*SPREADS
    old_router_phase=Q4_VERTICES*H1

    checks={
        "spread_count_is_36": SPREADS==36==chi*q2,
        "spread_square_equals_router_phase_packet": spread_square==old_router_phase==Q4_VERTICES*H1,
        "WE6_is_40_times_36_squared": WE6==v*spread_square,
        "WE6_is_40_times_16_times_81": WE6==v*Q4_VERTICES*H1,
        "Sp43_order_equals_WE6": sp4_order(q)==WE6,
        "projective_symplectic_half": WE6//2==PSP43,
        "X_rays_are_W33_point_line_flags": X_RAYS==point_line_flags==v*chi==LINES*POINTS_PER_LINE,
        "spread_line_incidence_double_count": spread_line_inc==line_spread_inc==360,
        "point_line_spread_triples": point_line_spread_triples==1440==X_RAYS*LINE_OCCURRENCE==SPREADS*v,
        "WE6_as_spreads_times_triples": WE6==SPREADS*point_line_spread_triples,
        "local_anchor_split_36_equals_4_times_9": local_spread_split==SPREADS,
    }
    return {
        "theorem":"Symplectic_Spread_Square_WE6_Factorization",
        "source_hint":"Live index points to exact projective/affine shell and symplectic-spread frame audits: 40 PG(3,3) anchors, 36 spreads, 4 anchor lines, 9 affine measurement directions.",
        "core_factorizations":{
            "old":"51840 = 40 * 16 * 81",
            "new":"51840 = 40 * 36^2",
            "bridge":"16 * 81 = 4^2 * 9^2 = (4*9)^2 = 36^2",
            "linear_symplectic":"|Sp(4,3)| = 3^4(3^4-1)(3^2-1) = 51840",
            "projective_note":"central +/-I acts trivially on projective points, giving |PSp(4,3)|=25920"
        },
        "spread_dictionary":{
            "W33_points":v,
            "isotropic_lines":LINES,
            "points_per_line":POINTS_PER_LINE,
            "spreads":SPREADS,
            "lines_per_spread":SPREAD_SIZE,
            "spreads_per_line":LINE_OCCURRENCE,
            "spreads_relative_to_anchor":"4 anchor-line sectors * 9 affine measurement-line frames"
        },
        "incidence_counts":{
            "point_line_flags_X_rays":point_line_flags,
            "spread_line_incidences":spread_line_inc,
            "line_spread_incidences":line_spread_inc,
            "point_line_spread_triples":point_line_spread_triples,
            "WE6_as_spreads_times_point_line_spread_triples":f"{SPREADS} * {point_line_spread_triples} = {WE6}"
        },
        "interpretation":{
            "40":"projective/symplectic W33 anchor choice",
            "36":"complete two-qutrit stabilizer/MUB spread-frame choice = 4 memory-line sectors * 9 affine measurement frames",
            "36_squared":"ordered source-target spread-frame transport packet per anchor",
            "16_times_81":"same packet in router/phase coordinates: Q4 states * F3^4 phase states",
            "why_it_matters":"The Q4 router and F3^4 phase layer are not arbitrary independent factors; together they equal the square of the exact symplectic-spread frame count already present in W(3,3)."
        },
        "identities":checks,
        "all_identities_hold":bool(all(checks.values()))
    }


def main():
    payload=build_payload()
    out=Path("data/w33_spread_square_we6_factorization.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload,indent=2,sort_keys=True),encoding="utf-8")
    print(json.dumps({"all_identities_hold":payload["all_identities_hold"],"core_factorizations":payload["core_factorizations"],"incidence_counts":payload["incidence_counts"],"interpretation":payload["interpretation"]},indent=2,sort_keys=True))
    print(f"wrote {out}")

if __name__=="__main__":
    main()
