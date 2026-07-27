from __future__ import annotations

import json
from collections import Counter, deque
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass1121_e8_a2_cubic_incidence.json"

E8_SIMPLE_ROOTS = np.array([
    [1,-1,0,0,0,0,0,0], [0,1,-1,0,0,0,0,0],
    [0,0,1,-1,0,0,0,0], [0,0,0,1,-1,0,0,0],
    [0,0,0,0,1,-1,0,0], [0,0,0,0,0,1,-1,0],
    [0,0,0,0,0,1,1,0], [-.5,-.5,-.5,-.5,-.5,-.5,-.5,-.5],
], dtype=float)
E6_SIMPLE_ROOTS = E8_SIMPLE_ROOTS[2:8]
SU3_ALPHA_K2=(2,-2,0,0,0,0,0,0)
SU3_BETA_K2=(0,2,0,0,0,0,0,-2)

def construct_e8_roots():
    roots=[]
    for i in range(8):
        for j in range(i+1,8):
            for si in (1.0,-1.0):
                for sj in (1.0,-1.0):
                    r=np.zeros(8);r[i]=si;r[j]=sj;roots.append(r)
    for bits in range(256):
        signs=np.array([1.0 if (bits>>k)&1 else -1.0 for k in range(8)])
        if int(np.sum(signs<0))%2==0: roots.append(signs*.5)
    return np.asarray(roots)

def snap(v): return tuple(float(x) for x in np.round(v*2)/2)

def compute_we6_orbits(roots):
    index={snap(r):i for i,r in enumerate(roots)}
    used=np.zeros(len(roots),dtype=bool);out=[]
    for seed in range(len(roots)):
        if used[seed]: continue
        used[seed]=True;orb=[seed];q=[seed]
        while q:
            i=q.pop();v=roots[i]
            for alpha in E6_SIMPLE_ROOTS:
                image=v-2*np.dot(v,alpha)/np.dot(alpha,alpha)*alpha
                j=index[snap(image)]
                if not used[j]: used[j]=True;orb.append(j);q.append(j)
        out.append(orb)
    return out

def e6_key(r):
    rk=k2(r)
    a=sum(rk[i]*SU3_ALPHA_K2[i] for i in range(8))
    b=sum(rk[i]*SU3_BETA_K2[i] for i in range(8))
    proj=[(2*a+b)*SU3_ALPHA_K2[i]+(a+2*b)*SU3_BETA_K2[i] for i in range(8)]
    return tuple(12*rk[i]-proj[i] for i in range(8))

def k2(r: np.ndarray) -> Tuple[int, ...]:
    return tuple(int(round(2 * float(x))) for x in r.tolist())

def rank_mod(A: np.ndarray, p: int) -> int:
    M = np.asarray(A, dtype=np.int64).copy() % p
    m, n = M.shape
    r = 0
    for c in range(n):
        nz = np.flatnonzero(M[r:, c])
        if len(nz) == 0:
            continue
        pivot = r + int(nz[0])
        if pivot != r:
            M[[r, pivot]] = M[[pivot, r]]
        inv = pow(int(M[r, c]), -1, p)
        M[r, :] = (M[r, :] * inv) % p
        rows = np.flatnonzero(M[:, c])
        rows = rows[rows != r]
        if len(rows):
            factors = M[rows, c].copy()
            M[rows, :] = (M[rows, :] - factors[:, None] * M[r, :]) % p
        r += 1
        if r == m:
            break
    return r

def root_reflection_perm(roots: np.ndarray, root_index: Dict[Tuple[int, ...], int], alpha: Iterable[float]) -> np.ndarray:
    a = np.asarray(tuple(alpha), dtype=float)
    out = []
    for beta in roots:
        coeff = int(round(float(np.dot(beta, a))))
        image = beta - coeff * a
        out.append(root_index[k2(image)])
    return np.asarray(out, dtype=np.int16)

def orbit_partition(gens: List[np.ndarray], degree: int) -> List[List[int]]:
    unseen = np.ones(degree, dtype=bool)
    out: List[List[int]] = []
    for seed in range(degree):
        if not unseen[seed]:
            continue
        unseen[seed] = False
        q = deque([seed])
        orb: List[int] = []
        while q:
            x = q.popleft()
            orb.append(x)
            for g in gens:
                y = int(g[x])
                if unseen[y]:
                    unseen[y] = False
                    q.append(y)
        out.append(sorted(orb))
    return sorted(out, key=lambda x: (len(x), x[0]))

def main() -> None:
    canonical_path = ROOT / "data" / "w33_pass1121_e6_projection_fixture.json"
    canonical = json.loads(canonical_path.read_text(encoding="utf-8"))
    roots = construct_e8_roots()
    orbits = compute_we6_orbits(roots)
    sizes = [len(o) for o in orbits]
    assert sorted(sizes) == [1, 1, 1, 1, 1, 1, 27, 27, 27, 27, 27, 27, 72]
    root_index = {k2(roots[i]): i for i in range(len(roots))}

    orbs_3 = [int(x["orbit"]) for x in canonical["orbits_3"]]
    orbs_3bar = [int(x["orbit"]) for x in canonical["orbits_3bar"]]
    triads = [tuple(sorted(map(int, t))) for t in canonical["triads"]]
    triad_index = {t: i for i, t in enumerate(triads)}
    if len(triads) != 45 or len(triad_index) != 45:
        raise RuntimeError("expected 45 distinct cubic triads")

    key27_list = [tuple(map(int, x)) for x in canonical["e6_keys_27_k2"]]
    key27b_list = [tuple(map(int, x)) for x in canonical["e6_keys_27bar_k2"]]
    key27 = {x: i for i, x in enumerate(key27_list)}
    key27b = {x: i for i, x in enumerate(key27b_list)}
    dual_b_to_27 = {key27b[tuple(-v for v in k)]: i for k, i in key27.items()}
    if len(dual_b_to_27) != 27:
        raise RuntimeError("27/27bar dual map is not bijective")

    root_meta: Dict[int, Tuple[int, int, int]] = {}
    for color, oi in enumerate(orbs_3):
        for ridx in orbits[oi]:
            root_meta[ridx] = (1, color, key27[e6_key(roots[ridx])])
    for color, oi in enumerate(orbs_3bar):
        for ridx in orbits[oi]:
            bid = key27b[e6_key(roots[ridx])]
            root_meta[ridx] = (-1, color, dual_b_to_27[bid])
    assert len(root_meta) == 162

    a2_set = set()
    for i in range(240):
        ri = k2(roots[i])
        for j in range(i + 1, 240):
            rj = k2(roots[j])
            target = tuple(-(ri[t] + rj[t]) for t in range(8))
            k = root_index.get(target)
            if k is not None and j < k:
                a2_set.add((i, j, k))
    a2 = sorted(a2_set)
    a2_index = {t: i for i, t in enumerate(a2)}
    assert len(a2) == 2240

    cubic = np.zeros((45, 27), dtype=np.int8)
    for c, tri in enumerate(triads):
        cubic[c, list(tri)] = 1

    firewall_data = json.loads((ROOT / "data" / "w33_pass1103_hesse_firewall_cubic_transport.json").read_text())
    firewall_triads = [tuple(sorted(map(int, r["fiber_triad_sorted"]))) for r in firewall_data["records"]]
    firewall_idx = [triad_index[t] for t in firewall_triads]
    firewall = cubic[firewall_idx, :]

    signed_root_projection = np.zeros((2240, 27), dtype=np.int8)
    unsigned_root_projection = np.zeros((2240, 27), dtype=np.int8)
    lift_plus = np.zeros((2240, 45), dtype=np.int8)
    lift_minus = np.zeros((2240, 45), dtype=np.int8)
    root_type_hist = Counter()

    for ti, triple in enumerate(a2):
        meta = [root_meta.get(r) for r in triple]
        kinds = tuple(sorted(0 if x is None else x[0] for x in meta))
        root_type_hist[str(kinds)] += 1
        for item in meta:
            if item is None:
                continue
            sign, _color, e6id = item
            signed_root_projection[ti, e6id] += sign
            unsigned_root_projection[ti, e6id] += 1
        if all(x is not None for x in meta):
            signs = {x[0] for x in meta if x is not None}
            colors = {x[1] for x in meta if x is not None}
            ids = tuple(sorted(x[2] for x in meta if x is not None))
            ci = triad_index.get(ids)
            if colors == {0, 1, 2} and ci is not None:
                if signs == {1}:
                    lift_plus[ti, ci] = 1
                elif signs == {-1}:
                    lift_minus[ti, ci] = 1

    lift_total = lift_plus + lift_minus
    lift_signed = lift_plus - lift_minus
    cubic_score_signed = signed_root_projection @ cubic.T
    cubic_score_unsigned = unsigned_root_projection @ cubic.T
    firewall_score_signed = signed_root_projection @ firewall.T
    firewall_score_unsigned = unsigned_root_projection @ firewall.T

    root_gens = [root_reflection_perm(roots, root_index, alpha) for alpha in E6_SIMPLE_ROOTS]
    triple_gens = []
    e6id_gens = []
    cubic_gens = []
    ref_orbit = orbs_3[0]
    root_by_id = [-1] * 27
    for ridx in orbits[ref_orbit]:
        root_by_id[key27[e6_key(roots[ridx])]] = ridx
    assert all(x >= 0 for x in root_by_id)
    for gp in root_gens:
        tg = np.empty(2240, dtype=np.int16)
        for i, triple in enumerate(a2):
            image = tuple(sorted(int(gp[x]) for x in triple))
            tg[i] = a2_index[image]
        triple_gens.append(tg)

        eg = np.empty(27, dtype=np.int8)
        for e, ridx in enumerate(root_by_id):
            eg[e] = key27[e6_key(roots[int(gp[ridx])])]
        if len(set(map(int, eg))) != 27:
            raise RuntimeError("E6-id generator is not a permutation")
        e6id_gens.append(eg)

        cg = np.empty(45, dtype=np.int8)
        for ci, tri in enumerate(triads):
            image = tuple(sorted(int(eg[e]) for e in tri))
            cg[ci] = triad_index[image]
        if len(set(map(int, cg))) != 45:
            raise RuntimeError("cubic generator is not a permutation")
        cubic_gens.append(cg)

    equivariance = []
    for tg, eg, cg in zip(triple_gens, e6id_gens, cubic_gens):
        root_ok = all(np.array_equal(signed_root_projection[int(tg[t]), eg], signed_root_projection[t]) for t in range(2240))
        lift_ok = all(np.array_equal(lift_plus[int(tg[t]), cg], lift_plus[t]) and np.array_equal(lift_minus[int(tg[t]), cg], lift_minus[t]) for t in range(2240))
        equivariance.append({"root_projection": bool(root_ok), "cubic_lifts": bool(lift_ok)})

    a2_orbits = orbit_partition(triple_gens, 2240)
    orbit_records = []
    for orb in a2_orbits:
        plus = int(lift_plus[orb].sum())
        minus = int(lift_minus[orb].sum())
        orbit_records.append({
            "size": len(orb),
            "stabilizer_order": 51840 // len(orb),
            "cubic_lift_plus": plus,
            "cubic_lift_minus": minus,
            "cubic_lift_total": plus + minus,
            "mixed_root_count_histogram": dict(Counter(int(unsigned_root_projection[t].sum()) for t in orb)),
        })

    matrices = {
        "cubic_45x27": cubic,
        "firewall_9x27": firewall,
        "signed_root_projection_2240x27": signed_root_projection,
        "unsigned_root_projection_2240x27": unsigned_root_projection,
        "lift_plus_2240x45": lift_plus,
        "lift_minus_2240x45": lift_minus,
        "lift_total_2240x45": lift_total,
        "lift_signed_2240x45": lift_signed,
        "cubic_score_signed_2240x45": cubic_score_signed,
        "cubic_score_unsigned_2240x45": cubic_score_unsigned,
        "firewall_score_signed_2240x9": firewall_score_signed,
        "firewall_score_unsigned_2240x9": firewall_score_unsigned,
    }
    ranks = {}
    for name, M in matrices.items():
        rq = rank_mod(M, 1000003)
        r3 = rank_mod(M, 3)
        ranks[name] = {
            "rank_Q_certified_mod_1000003": rq,
            "rank_F3": r3,
            "row_kernel_dimension_Q": int(M.shape[0] - rq),
            "column_kernel_dimension_Q": int(M.shape[1] - rq),
            "shape": list(M.shape),
        }

    plus_per_cubic = lift_plus.sum(axis=0).astype(int).tolist()
    minus_per_cubic = lift_minus.sum(axis=0).astype(int).tolist()
    firewall_lifts = [plus_per_cubic[i] + minus_per_cubic[i] for i in firewall_idx]

    checks = {
        "canonical_fixture_hash_locked": canonical["source_artifact_sha256"] == "81444a3d3f2c93a2078bf23e3eea52f6b043ccb39b115aed4a9fbc62062ce135",
        "e8_roots_240": len(roots) == 240,
        "a2_triples_2240": len(a2) == 2240,
        "mixed_roots_162": len(root_meta) == 162,
        "cubic_triads_45": len(triads) == 45,
        "firewall_triads_9": len(firewall_idx) == 9,
        "positive_cubic_lifts_270": int(lift_plus.sum()) == 270,
        "negative_cubic_lifts_270": int(lift_minus.sum()) == 270,
        "total_cubic_lifts_540": int(lift_total.sum()) == 540,
        "six_lifts_per_sign_per_cubic": set(plus_per_cubic) == {6} and set(minus_per_cubic) == {6},
        "twelve_lifts_per_firewall_term": set(firewall_lifts) == {12},
        "all_six_simple_generators_equivariant": all(x["root_projection"] and x["cubic_lifts"] for x in equivariance),
        "a2_orbits_partition_2240": sum(len(x) for x in a2_orbits) == 2240,
        "cubic_lift_support_is_union_of_orbits": all(r["cubic_lift_total"] in {0, r["size"]} for r in orbit_records),
        "lift_total_rank_45": ranks["lift_total_2240x45"]["rank_Q_certified_mod_1000003"] == 45,
        "firewall_rank_9": ranks["firewall_9x27"]["rank_Q_certified_mod_1000003"] == 9,
    }
    if not all(checks.values()):
        raise AssertionError((checks, orbit_records, ranks))

    out = {
        "schema": "w33.pass1121.e8_a2_cubic_incidence.v1",
        "status": "PASS",
        "headline": "The 2240 E8 A2 root triples contain an exact W(E6)-equivariant 540-element cubic-lift subcarrier: every one of the 45 E6 cubic supports has six lifts in the 27x3 sheet and six conjugate lifts in the 27barx3bar sheet. Restriction to the nine firewall fibers gives exactly twelve A2 lifts per deleted cubic term. The firewall restriction is a selected support projection, not a full W(E6)-stable submodule.",
        "counts": {"a2_triples": 2240, "cubic_supports": 45, "firewall_supports": 9, "positive_cubic_lifts": int(lift_plus.sum()), "negative_cubic_lifts": int(lift_minus.sum()), "total_cubic_lifts": int(lift_total.sum())},
        "per_cubic_lifts": {"positive_histogram": dict(Counter(plus_per_cubic)), "negative_histogram": dict(Counter(minus_per_cubic)), "total_histogram": dict(Counter(a + b for a, b in zip(plus_per_cubic, minus_per_cubic)))},
        "firewall": {"triad_indices": firewall_idx, "lift_histogram": dict(Counter(firewall_lifts)), "equivariance_boundary": "The nine selected firewall fibers are not asserted to be W(E6)-stable; only the complete 45-support cubic map is tested equivariantly."},
        "a2_orbits": orbit_records,
        "root_type_histogram": dict(root_type_hist),
        "matrix_ranks": ranks,
        "equivariance_by_simple_generator": equivariance,
        "check_count": len(checks),
        "checks": checks,
        "scope": "Exact E8-root enumeration, canonical E6xA2 projection, exact cubic supports, and six-generator equivariance. Rank over Q is certified by a nonzero minor modulo 1000003 and the column bound; F3 ranks are computed independently.",
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": out["status"], "counts": out["counts"], "orbits": orbit_records, "ranks": ranks}, indent=2))

if __name__ == "__main__":
    main()
