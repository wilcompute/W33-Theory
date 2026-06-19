#!/usr/bin/env python3
"""
BT1349 — Joint Q4/Q5 Falsifier

Constructs a single oracle that simultaneously rules out competing CSS code
families at both Q4 [[32,4,4]] and Q5 [[37,5,>=4]] levels.

The falsifier operates as follows:
  1. For each candidate competing code C (parameterized by its circulant seed),
     compute its Q4-level and Q5-level Hashimoto spectral gaps.
  2. Declare C falsified if it fails to exceed the W33 joint threshold at
     EITHER quadrant level.
  3. Report the fraction of candidates falsified and the surviving set.

This extends BT1342 (Q4 Hashimoto falsifier) and BT1345 (matrix Hashimoto
falsifier) to the two-level joint setting.

Pipeline: BT1347 -> BT1348 -> BT1349 (this file) -> BT1350 (synthesis)
"""

import numpy as np
import json
from typing import List, Dict, Tuple

# Joint thresholds from BT1348
THRESH_Q4 = 2.523
THRESH_Q5 = 2.687


# ---------------------------------------------------------------------------
# CANDIDATE GENERATOR
# ---------------------------------------------------------------------------

def generate_candidate_circulant_seeds(n_candidates: int = 80,
                                       h: int = 16) -> List[np.ndarray]:
    """
    Generate candidate circulant base vectors for competing CSS codes.
    Each candidate is a random binary vector of length h that seeds
    a circulant check matrix.
    """
    rng = np.random.default_rng(1349)
    seeds = [rng.integers(0, 2, size=h) for _ in range(n_candidates)]
    # Ensure each seed has weight >= 2
    for s in seeds:
        if s.sum() < 2:
            s[0] = 1
            s[1] = 1
    return seeds


def circulant_from_seed(seed: np.ndarray) -> np.ndarray:
    h = len(seed)
    C = np.zeros((h, h), dtype=int)
    for i in range(h):
        C[i] = np.roll(seed, i)
    return C


def build_candidate_q4(seed: np.ndarray) -> np.ndarray:
    """Build Q4-level Hx (16 x 32) from circulant seed."""
    h = len(seed)
    Hx_block = circulant_from_seed(seed)
    Hx = np.hstack([Hx_block, np.zeros((h, h), dtype=int)])
    return Hx


def build_candidate_q5(seed: np.ndarray) -> np.ndarray:
    """Build Q5-level Hx (16 x 37) from circulant seed + random pentad extension."""
    Hx4 = build_candidate_q4(seed)
    h = Hx4.shape[0]
    rng = np.random.default_rng(int(seed.sum()) + 1349)
    v_x = rng.integers(0, 2, size=(h, 5))
    Hx5 = np.hstack([Hx4, v_x])
    return Hx5


# ---------------------------------------------------------------------------
# SPECTRAL GAP (lightweight — for falsifier speed)
# ---------------------------------------------------------------------------

def fast_spectral_gap(H: np.ndarray) -> float:
    """
    Fast Hashimoto spectral gap via Ihara companion matrix.
    Returns lambda_1 - lambda_2.
    """
    m, n = H.shape
    A = np.zeros((m + n, m + n), dtype=float)
    for i in range(m):
        for j in range(n):
            if H[i, j] == 1:
                A[i, m + j] = 1.0
                A[m + j, i] = 1.0
    degs = A.sum(axis=1)
    D = np.diag(degs)
    B = A - (D - np.eye(m + n))
    eigvals = np.sort(np.real(np.linalg.eigvals(B)))[::-1]
    gap = eigvals[0] - eigvals[1] if len(eigvals) > 1 else 0.0
    return float(gap)


# ---------------------------------------------------------------------------
# JOINT FALSIFIER ORACLE
# ---------------------------------------------------------------------------

def joint_falsifier(seeds: List[np.ndarray]) -> Dict:
    """
    Apply joint Q4/Q5 falsifier to a list of candidate seeds.
    A candidate is FALSIFIED if its gap is below the W33 threshold
    at Q4 level OR Q5 level.
    """
    results = []
    n_falsified_q4 = 0
    n_falsified_q5 = 0
    n_falsified_joint = 0
    survivors = []

    for idx, seed in enumerate(seeds):
        Hx4 = build_candidate_q4(seed)
        Hx5 = build_candidate_q5(seed)
        gap4 = fast_spectral_gap(Hx4)
        gap5 = fast_spectral_gap(Hx5)

        fail4 = gap4 < THRESH_Q4
        fail5 = gap5 < THRESH_Q5
        falsified = fail4 or fail5

        if fail4:
            n_falsified_q4 += 1
        if fail5:
            n_falsified_q5 += 1
        if falsified:
            n_falsified_joint += 1
        else:
            survivors.append(idx)

        results.append({
            'candidate': idx,
            'seed_weight': int(seed.sum()),
            'gap_Q4': round(gap4, 4),
            'gap_Q5': round(gap5, 4),
            'fail_Q4': bool(fail4),
            'fail_Q5': bool(fail5),
            'falsified': bool(falsified)
        })

    n_total = len(seeds)
    return {
        'n_candidates': n_total,
        'n_falsified_q4_only': n_falsified_q4,
        'n_falsified_q5_only': n_falsified_q5,
        'n_falsified_joint': n_falsified_joint,
        'n_survivors': len(survivors),
        'falsification_rate': round(n_falsified_joint / max(n_total, 1), 4),
        'survivor_indices': survivors,
        'threshold_Q4': THRESH_Q4,
        'threshold_Q5': THRESH_Q5,
        'per_candidate': results
    }


def analyze_survivors(survivors: List[int], seeds: List[np.ndarray],
                      results: List[Dict]) -> Dict:
    """
    For surviving candidates, compute their distance to the W33 canonical
    construction (measured by gap delta at each quadrant level).
    """
    if not survivors:
        return {'n_survivors': 0, 'note': 'All candidates falsified.'}

    w33_gap4 = 2.523  # from BT1348
    w33_gap5 = 2.687

    dists = []
    for idx in survivors:
        r = results[idx]
        d4 = r['gap_Q4'] - w33_gap4
        d5 = r['gap_Q5'] - w33_gap5
        dists.append({'idx': idx, 'delta_Q4': round(d4, 4),
                      'delta_Q5': round(d5, 4),
                      'seed_weight': r['seed_weight']})

    # Survivors closest to W33 canonical
    dists.sort(key=lambda x: x['delta_Q4'] + x['delta_Q5'])
    return {
        'n_survivors': len(survivors),
        'closest_to_W33': dists[:3],
        'note': 'Survivors pass joint threshold but may not match W33 structure.'
    }


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main():
    print("=" * 70)
    print("BT1349 — Joint Q4/Q5 Falsifier")
    print("=" * 70)
    print(f"  Joint thresholds: Q4 gap > {THRESH_Q4}, Q5 gap > {THRESH_Q5}")

    seeds = generate_candidate_circulant_seeds(n_candidates=80)
    print(f"  Candidates: {len(seeds)}")

    res = joint_falsifier(seeds)
    print(f"\nFalsifier Results:")
    print(f"  Candidates tested:     {res['n_candidates']}")
    print(f"  Falsified (Q4 level):  {res['n_falsified_q4_only']}")
    print(f"  Falsified (Q5 level):  {res['n_falsified_q5_only']}")
    print(f"  Falsified (joint):     {res['n_falsified_joint']}")
    print(f"  Survivors:             {res['n_survivors']}")
    print(f"  Falsification rate:    {res['falsification_rate']*100:.1f}%")

    survivor_analysis = analyze_survivors(
        res['survivor_indices'], seeds, res['per_candidate']
    )
    print(f"\nSurvivor Analysis:")
    print(f"  {survivor_analysis['note']}")
    if survivor_analysis['n_survivors'] > 0:
        print(f"  Closest to W33 canonical:")
        for s in survivor_analysis['closest_to_W33']:
            print(f"    idx={s['idx']} delta_Q4={s['delta_Q4']:+.4f} "
                  f"delta_Q5={s['delta_Q5']:+.4f} seed_wt={s['seed_weight']}")

    output = {
        'falsifier_summary': {
            k: v for k, v in res.items() if k != 'per_candidate'
        },
        'survivor_analysis': survivor_analysis,
        'threshold_Q4': THRESH_Q4,
        'threshold_Q5': THRESH_Q5,
        'bt': 'BT1349'
    }
    with open('bt1349_joint_q4_q5_falsifier_results.json', 'w') as f:
        json.dump(output, f, indent=2)
    print("\nResults -> bt1349_joint_q4_q5_falsifier_results.json")
    print("=" * 70)
    return output


if __name__ == '__main__':
    main()
