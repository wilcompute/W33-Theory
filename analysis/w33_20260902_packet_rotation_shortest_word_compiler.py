#!/usr/bin/env python3
"""Exact shortest-word compiler for the E8 completion-chart packet rotations.

The 2026-09-01 port-holonomy certificate found four deterministic local
packet rotations, at packet indices [0,9,11,33], which generate the complete
order-25920 PSp(4,3) action on the 27 completion charts.  This pass turns that
existence theorem into an exact compiler metric.

We use the four rotations and their inverses as an eight-letter symmetric
alphabet and breadth-first search the full paired 45-packet/27-chart action.
For every group element we record its exact shortest packet-rotation length.
The already-certified S3^45 port cocycle then gives two gauge costs directly
from the resulting group element, independent of which shortest word was
chosen:

  * correction support = number of packets with nonidentity local S3 action;
  * transposition cost = sum of minimal transposition lengths in S3
    (identity=0, transposition=1, 3-cycle=2).

These are finite compiler/gauge metrics, not physical optical gate costs.
"""
from __future__ import annotations

import json
from collections import Counter, deque
from pathlib import Path

import w33_20260901_e8_chart_port_holonomy as H

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data/PART_W33_20260902_PACKET_ROTATION_SHORTEST_WORD_COMPILER.json'


def sigma(ports, g45, g27, p):
    target = g45[p]
    pos = {c: i for i, c in enumerate(ports[target])}
    return tuple(pos[g27[c]] for c in ports[p])


def s3_transposition_length(p):
    if p == (0, 1, 2):
        return 0
    # odd permutations in S3 are transpositions; even nonidentity ones are
    # 3-cycles and require two transpositions.
    inversions = sum(p[i] > p[j] for i in range(3) for j in range(i + 1, 3))
    return 1 if inversions % 2 else 2


def deterministic_rotations(incident, G):
    ports = {p: incident[p] for p in range(45)}
    cyc = (1, 2, 0)
    rotations = []
    for p in range(45):
        candidates = [
            g for g in G
            if g[0][p] == p
            and sigma(ports, g[0], g[1], p) == cyc
            and H.orderp(g[0]) == 3
            and H.orderp(g[1]) == 3
        ]
        assert len(candidates) == 24
        rotations.append(sorted(candidates)[0])

    selected = []
    generated = {tuple(range(27))}
    packet_ids = []
    growth = []
    for p, pair in enumerate(rotations):
        trial = H.closure27([x[1] for x in selected] + [pair[1]])
        if len(trial) > len(generated):
            selected.append(pair)
            generated = trial
            packet_ids.append(p)
            growth.append(len(generated))
        if len(generated) == 25920:
            break
    assert packet_ids == [0, 9, 11, 33]
    assert growth == [3, 9, 288, 25920]
    return ports, rotations, selected, packet_ids, growth


def main():
    _supports, _charts, incident, _genpairs, G = H.build()
    assert len(G) == 25920
    ports, _rotations, selected, packet_ids, growth = deterministic_rotations(incident, G)

    # Symmetric eight-letter packet-rotation alphabet.
    moves = []
    move_labels = []
    for packet_id, pair in zip(packet_ids, selected):
        moves.append(pair)
        move_labels.append(f'p{packet_id}+')
        moves.append((H.inv(pair[0]), H.inv(pair[1])))
        move_labels.append(f'p{packet_id}-')

    e = (tuple(range(45)), tuple(range(27)))
    dist = {e: 0}
    parent = {e: None}
    parent_move = {e: None}
    q = deque([e])
    while q:
        a45, a27 = q.popleft()
        d = dist[(a45, a27)]
        for mi, (m45, m27) in enumerate(moves):
            z = (H.compose(m45, a45), H.compose(m27, a27))
            if z not in dist:
                dist[z] = d + 1
                parent[z] = (a45, a27)
                parent_move[z] = mi
                q.append(z)
    assert len(dist) == 25920
    assert set(dist) == set(G)

    diameter = max(dist.values())
    length_hist = Counter(dist.values())
    chart_stab = [g for g in G if g[1][0] == 0]
    assert len(chart_stab) == 960
    chart_stab_hist = Counter(dist[g] for g in chart_stab)

    support_hist = Counter()
    transposition_cost_hist = Counter()
    layer = {}
    zero_correction = 0
    for g45, g27 in G:
        local = [sigma(ports, g45, g27, p) for p in range(45)]
        support = sum(s != (0, 1, 2) for s in local)
        tc = sum(s3_transposition_length(s) for s in local)
        support_hist[support] += 1
        transposition_cost_hist[tc] += 1
        if support == 0:
            zero_correction += 1
        ell = dist[(g45, g27)]
        rec = layer.setdefault(ell, {
            'elements': 0,
            'supportSum': 0,
            'supportMin': 45,
            'supportMax': 0,
            'transpositionCostSum': 0,
            'transpositionCostMin': 90,
            'transpositionCostMax': 0,
        })
        rec['elements'] += 1
        rec['supportSum'] += support
        rec['supportMin'] = min(rec['supportMin'], support)
        rec['supportMax'] = max(rec['supportMax'], support)
        rec['transpositionCostSum'] += tc
        rec['transpositionCostMin'] = min(rec['transpositionCostMin'], tc)
        rec['transpositionCostMax'] = max(rec['transpositionCostMax'], tc)
    assert zero_correction == 1

    # Recover deterministic shortest words for a small set of diameter
    # witnesses.  These serve as directly replayable compiler witnesses without
    # bloating the certificate with all 25,920 words.
    diameter_states = sorted(g for g, d in dist.items() if d == diameter)
    witness_words = []
    for state in diameter_states[:8]:
        word = []
        cur = state
        while parent[cur] is not None:
            word.append(move_labels[parent_move[cur]])
            cur = parent[cur]
        word.reverse()
        assert len(word) == diameter
        witness_words.append(word)

    # Exact consistency checks for every layer.
    assert sum(length_hist.values()) == 25920
    assert sum(chart_stab_hist.values()) == 960
    assert sum(support_hist.values()) == 25920
    assert sum(transposition_cost_hist.values()) == 25920
    assert length_hist[0] == 1

    out = {
        'schema': 'w33.20260902.packet-rotation-shortest-word-compiler.v1',
        'status': 'PASS',
        'groupOrder': 25920,
        'packetGeneratorIds': packet_ids,
        'generatorGrowth': growth,
        'alphabet': move_labels,
        'alphabetSize': len(moves),
        'shortestWord': {
            'diameter': diameter,
            'lengthHistogram': {str(k): v for k, v in sorted(length_hist.items())},
            'diameterElementCount': length_hist[diameter],
            'diameterWitnessWords': witness_words,
        },
        'baseChartStabilizer': {
            'order': 960,
            'ambientShortestLengthHistogram': {str(k): v for k, v in sorted(chart_stab_hist.items())},
            'ambientMaximumShortestLength': max(chart_stab_hist),
        },
        'portCorrectionGauge': {
            'zeroCorrectionElements': zero_correction,
            'supportHistogram': {str(k): v for k, v in sorted(support_hist.items())},
            'transpositionCostHistogram': {str(k): v for k, v in sorted(transposition_cost_hist.items())},
            'maximumSupport': max(support_hist),
            'maximumTranspositionCost': max(transposition_cost_hist),
            'definition': 'support counts nonidentity S3 packet corrections; transposition cost uses minimal S3 transposition length 0/1/2',
        },
        'byShortestLength': {str(k): v for k, v in sorted(layer.items())},
        'theorem': 'Using the four deterministic packet rotations at indices 0, 9, 11, and 33 together with their inverses, breadth-first search gives the exact word metric on all 25,920 PSp(4,3) compiler states. Every state has a certified shortest packet-rotation word no longer than the reported diameter, while its unique S3^45 correction cocycle has the independently tabulated support and transposition costs.',
        'boundary': 'Word length counts abstract packet rotations and port-correction cost counts gauge permutations. Neither quantity is asserted to equal optical depth, wall-clock latency, fault-tolerant cost, or physical energy.',
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + '\n')
    print(json.dumps({
        'status': 'PASS',
        'groupOrder': 25920,
        'diameter': diameter,
        'diameterElements': length_hist[diameter],
        'chartStabilizerMaxLength': max(chart_stab_hist),
        'maxCorrectionSupport': max(support_hist),
        'maxCorrectionTranspositionCost': max(transposition_cost_hist),
    }, sort_keys=True))


if __name__ == '__main__':
    main()
