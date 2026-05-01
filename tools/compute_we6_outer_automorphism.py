#!/usr/bin/env python3
"""Compute and certify the outer automorphism of WE6 and its effect on the
SP43 embedding.

This script reads the We6 true action artifact and the previously-fixed
SP43->WE6 even embedding (root and line permutations). It then:

1. Constructs the WE6 even subgroup and verifies its order (25920).
2. Selects an odd generator from the full WE6 action and checks that it is
   not contained in the even subgroup, demonstrating index-two normality.
3. Verifies that conjugation by this odd element normalizes the even subgroup.
4. Uses the odd element to conjugate the SP43 root and line permutations,
   producing a second copy of the SP43 action ("outer" embedding) which
   corresponds to the alternative BN-pair/geometric structure.
5. Emits new artifacts describing the outer permutations and records
   verification data.

The resulting bundle of artifacts can be used to inspect how the outer
automorphism swaps the symplectic vs unitary geometries and to connect the
whole story back to the CE2/Weil phase mapping.
"""

import json
import math
import sys
from collections import deque
from pathlib import Path

import numpy as np

# make sure project root and the scripts directory are available on
# sys.path so that imports such as ``ce2_global_cocycle`` work regardless of
# the current working directory.  this mirrors the logic inside
# ``scripts/ce2_global_cocycle.py`` itself and fixes the error seen when the
# script was invoked directly from the tools directory.
ROOT = Path(__file__).resolve().parents[1]
for p in (ROOT, ROOT / "scripts"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

# constants used by multiple helpers
SU3_ALPHA = np.array([1.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
SU3_BETA = np.array([0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0])


def su3_weight(r: np.ndarray):
    """Return the SU(3) weight (alpha,beta) of a root vector.

    This is a small convenience used for diagnostics when choosing orbits.
    """
    return (
        int(round(float(np.dot(r, SU3_ALPHA)))),
        int(round(float(np.dot(r, SU3_BETA)))),
    )


# utility helpers copied/modified from verify_bundle.py


def inv_perm(p):
    inv = np.empty_like(p)
    inv[p] = np.arange(len(p), dtype=p.dtype)
    return inv


def perm_order(p):
    n = len(p)
    seen = np.zeros(n, dtype=bool)
    l = 1
    for i in range(n):
        if not seen[i]:
            j = i
            L = 0
            while not seen[j]:
                seen[j] = True
                j = int(p[j])
                L += 1
            l = l * L // math.gcd(l, L)
    return l


def gen_group_n(gens, n, max_size=100000):
    idp = np.arange(n, dtype=np.uint16)
    seen = {idp.tobytes(): idp}
    q = deque([idp])
    while q and len(seen) < max_size:
        p = q.popleft()
        for g in gens:
            h = g[p]
            k = h.tobytes()
            if k not in seen:
                seen[k] = h
                q.append(h)
    return seen


def load_perm_list(path):
    with open(path, "r") as f:
        data = json.load(f)
    # convert to 0-based numpy arrays
    return [np.array(p, dtype=np.uint16) for p in data]


def resolve_sp43_fixed_artifact(name: str) -> Path:
    for candidate in (
        ROOT / "artifacts" / name,
        ROOT
        / "archive"
        / "dirs"
        / "SP43_TO_WE6_TRUE_FIXED_BUNDLE_v01_2026-02-25"
        / name,
        ROOT / "SP43_TO_WE6_TRUE_FIXED_BUNDLE_v01_2026-02-25" / name,
    ):
        if candidate.exists():
            return candidate
    raise FileNotFoundError(ROOT / "artifacts" / name)


def perm_to_list(p):
    return list(int(x) for x in p)


# ---------------------------------------------------------------------------
# helpers for root→E6id mapping (used by main and tests)
# ---------------------------------------------------------------------------


def e6_key(r: np.ndarray):
    """Compute E6 key (27‑class) of a normalized E8 root vector r."""
    A = np.stack([SU3_ALPHA, SU3_BETA], axis=1)
    G = A.T @ A
    coeffs = np.linalg.solve(G, A.T @ r)
    re6 = r - (A @ coeffs)
    return tuple(int(round(2 * float(x))) for x in re6.tolist())


def build_root_to_e6id(roots_array, orbit_list, p_perm=None):
    """Select a triple of 27‑orbits and build a root->E6‑ID map.

    Parameters
    ----------
    roots_array : np.ndarray
        Array of 240 normalized root vectors.
    orbit_list : List[List[int]]
        Partition of {0,...,239} into orbits under some subgroup.
    p_perm : sequence of int, optional
        Permutation of 240 indices (e.g. an outer automorphism element).
        If provided, the chosen triple will also satisfy that applying
        ``p_perm`` to any root in the union produces a root whose E6 key
        lies among the same 27 keys, ensuring closure under the permutation.

    Returns
    -------
    root_to_e6id : Dict[int,int]
        Map from root index to E6 ID in 0..26.
    color_orbs : List[List[int]]
        The three orbits chosen for the E6 color decomposition.
    triple : Tuple[int,int,int]
        Indices of the selected orbits within ``orbit_list``.

    The algorithm brute‑forces triples of orbits of size 27 and tests whether
    the multiset of their e6_keys has exactly 27 distinct values each
    occurring three times.  If ``p_perm`` is given the triple must also
    satisfy the closure condition described above.  If no suitable triple
    exists, the first three mix‑orbits are used with a warning instead of
    raising an error.  Warning messages will distinguish between a failure
    to find any valid colouring and a failure to satisfy the closure
    requirement when ``p_perm`` is provided.
    """
    mix = [oi for oi, orb in enumerate(orbit_list) if len(orb) == 27]
    from collections import Counter
    from itertools import combinations

    # precompute keys for each candidate orbit
    orbit_keys = {
        oi: [e6_key(roots_array[ridx]) for ridx in orbit_list[oi]] for oi in mix
    }

    # helper for closure check
    def triple_closes(triple_indices):
        if p_perm is None:
            return True
        # valid keys for the chosen triple
        valid_keys = set()
        for oi in triple_indices:
            valid_keys.update(orbit_keys[oi])
        # test every root in union
        for oi in triple_indices:
            for rid in orbit_list[oi]:
                rid2 = int(p_perm[rid])
                k2 = e6_key(roots_array[rid2])
                if k2 not in valid_keys:
                    return False
        return True

    first_valid = None
    for triple in combinations(mix, 3):
        combined = []
        for oi in triple:
            combined.extend(orbit_keys[oi])
        counts = Counter(combined)
        if len(counts) == 27 and set(counts.values()) == {3}:
            if first_valid is None:
                first_valid = triple
            if not triple_closes(triple):
                # try another triple if we have a permutation requirement
                continue
            # found a triple that both has correct multiplicities and closes
            color_orbs = [orbit_list[oi] for oi in triple]
            e6_groups = {}
            rt = {}
            for oi in triple:
                for rid in orbit_list[oi]:
                    k = e6_key(roots_array[rid])
                    if k not in e6_groups:
                        e6_groups[k] = len(e6_groups)
                    rt[rid] = e6_groups[k]
            return rt, color_orbs, triple

    # if we reach here, either no triple satisfied the multiplicity test at all,
    # or there were valid triples but none closed under p_perm.
    if first_valid is not None:
        if p_perm is not None:
            print(
                "WARNING: no 27-triple satisfies closure under provided permutation;",
                "defaulting to first valid triple without closure",
            )
        triple = first_valid
    else:
        print("WARNING: no valid triple found; defaulting to first three mix_orbs")
        if len(mix) < 3:
            raise RuntimeError("not enough 27-orbits available for fallback")
        triple = tuple(mix[:3])
    color_orbs = [orbit_list[oi] for oi in triple]
    e6_groups = {}
    rt = {}
    for oi in triple:
        for rid in orbit_list[oi]:
            k = e6_key(roots_array[rid])
            if k not in e6_groups:
                e6_groups[k] = len(e6_groups)
            rt[rid] = e6_groups[k]
    return rt, color_orbs, triple


# main workflow


def main():
    # load we6 action
    with open("artifacts/we6_true_action.json", "r") as f:
        we6 = json.load(f)
    roots = np.array(we6["roots_int2"], dtype=np.int16)
    original_roots = roots.copy()
    # we6_true_action stores roots scaled by 2; normalize to unit length roots
    roots = roots.astype(np.float64) / 2.0
    dot = roots @ roots.T
    # parse generators
    even_gens = [np.array(p, dtype=np.uint16) - 1 for p in we6["we6_even_generators"]]
    all_gens = [np.array(p, dtype=np.uint16) - 1 for p in we6.get("we6_generators", [])]
    assert len(all_gens) >= 1, "no full WE6 generators available"

    # build even group
    G_even = gen_group_n(even_gens, 240, max_size=60000)
    order_even = len(G_even)
    print(f"WE6 even subgroup size: {order_even}")
    assert order_even == we6["we6_even_order"]
    assert order_even == 25920

    # pick an odd element from all_gens and check membership
    p = all_gens[0]
    print("selected odd generator of full WE6 for outer automorphism")
    if p.tobytes() in G_even:
        raise RuntimeError("chosen element unexpectedly lies in even subgroup")

    # verify p normalizes G_even
    p_inv = inv_perm(p)
    for g in even_gens:
        # compute conjugate p*g*p^{-1}
        h = p[g[p_inv]]
        if h.tobytes() not in G_even:
            raise AssertionError("conjugation by p left even subgroup")
    print("odd element normalizes WE6_even (as expected index-2 subgroup)")

    # load previously fixed SP43 root perms and eps
    root_path = resolve_sp43_fixed_artifact("sp43_root_perms_fixed.json")
    eps_path = resolve_sp43_fixed_artifact("sp43_line_eps_fixed.json")
    sp43_roots = load_perm_list(root_path)
    sp43_eps = [np.array(x, dtype=np.int8) for x in json.load(open(eps_path))]
    # compute conjugated (outer) root perms
    sp43_roots_outer = [p[r][p_inv] for r in sp43_roots]  # p*r*p^{-1}
    # compute corresponding line perms and eps by recomputing canonical rep logic
    # reuse canonical line reps assumption (#0-119 paired with #120-239)
    root_to_line = np.empty(240, dtype=np.uint16)
    for i in range(120):
        root_to_line[i] = i
        root_to_line[i + 120] = i

    def line_perm_and_eps(root_perm):
        rep = np.arange(120, dtype=np.uint16)
        img = root_perm[rep]
        line_img = root_to_line[img]
        rep_img = rep[line_img]
        eps = np.where(img == rep_img, 1, -1).astype(np.int8)
        return line_img.astype(np.uint16), eps

    sp43_lines_outer = []
    sp43_eps_outer = []
    for rperm in sp43_roots_outer:
        lp, eps = line_perm_and_eps(rperm)
        sp43_lines_outer.append(lp)
        sp43_eps_outer.append(eps)

    # verify that outer perms still preserve antipodes and dot
    antip = None
    # build antipodes using original unscaled roots
    root_to_i = {tuple(r): i for i, r in enumerate(original_roots.tolist())}
    antip = np.empty(240, dtype=np.uint16)
    for i, r in enumerate(original_roots.tolist()):
        antip[i] = root_to_i[tuple([-x for x in r])]
    for idx, pperm in enumerate(sp43_roots_outer):
        assert np.array_equal(antip[pperm], pperm[antip])
        assert np.array_equal(dot[pperm][:, pperm], dot)
    print("outer SP43 perms still legitimate isometries")

    # write new artifacts
    out_dir = "artifacts"
    with open(out_dir + "/sp43_root_perms_outer.json", "w") as f:
        json.dump([perm_to_list(p) for p in sp43_roots_outer], f)
    with open(out_dir + "/sp43_line_perms_outer.json", "w") as f:
        json.dump([perm_to_list(p) for p in sp43_lines_outer], f)
    with open(out_dir + "/sp43_line_eps_outer.json", "w") as f:
        json.dump([eps.tolist() for eps in sp43_eps_outer], f)

    # also output the outer automorphism permutation p itself and a note
    with open(out_dir + "/we6_outer_element.json", "w") as f:
        json.dump(
            {
                "perm": perm_to_list(p),
                "description": "odd WE6 generator used for outer automorphism",
            },
            f,
        )

    print("Wrote outer automorphism artifacts")

    # ------------------------------------------------------------------
    # compute root->E6id mapping and effect of outer element on CE2 coordinates
    # ------------------------------------------------------------------
    # the ``build_root_to_e6id`` helper can select a triple of 27‑orbits and
    # optionally enforce closure under a permutation.  rather than re‑implement
    # the SU3 weight logic here we convert the canonical orbits computed by
    # ``compute_double_sixes`` into the artifact ordering and let the helper do
    # the work.  this also allows us to pass ``p`` so that if a perfectly
    # closed colouring exists it will be found automatically.

    # our earlier experiments showed that the 27‑orbit colouring only
    # appears when we work with the canonical W(E6) orbits rather than the
    # raw even‑subgroup orbits on the artifact ordering.  therefore we
    # reconstruct the canonical roots, compute their W(E6) orbits, and then
    # translate those orbits into the artifact index space.  the generic
    # ``build_root_to_e6id`` helper will then pick a good triple (and respect
    # ``p_perm`` if possible).

    import importlib.util
    from pathlib import Path

    cds_path = Path(__file__).resolve().parents[1] / "tools" / "compute_double_sixes.py"
    spec = importlib.util.spec_from_file_location("compute_double_sixes", cds_path)
    cds = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(cds)
    cds_roots = cds.construct_e8_roots()
    cds_scaled = (cds_roots * 2).astype(np.int16)
    art_list = [tuple(r.tolist()) for r in original_roots]
    cds_to_art = {}
    for i, r in enumerate(cds_scaled):
        t = tuple(r.tolist())
        if t in art_list:
            cds_to_art[i] = art_list.index(t)
        else:
            cds_to_art[i] = art_list.index(tuple((-r).tolist()))

    cds_orbits = cds.compute_we6_orbits(cds_roots)
    artifact_orbits = [[cds_to_art[r] for r in orb] for orb in cds_orbits]

    print("searching for 27-triple closed under outer permutation...")
    root_to_e6id, color_orbs, triple = build_root_to_e6id(
        original_roots, artifact_orbits, p_perm=p
    )
    print(f"selected root triple (artifact indices) {triple}")
    # report SU3 weights of first representatives for additional diagnostics
    for oi in triple:
        w = su3_weight(original_roots[artifact_orbits[oi][0]])
        print(f" orbit {oi} SU3 weight {w}")
    from collections import Counter

    counts = Counter(root_to_e6id.values())
    print(
        f"counts per e6id: {sorted(counts.values())[:5]} (unique {set(counts.values())})"
    )
    eid = len(set(root_to_e6id.values()))

    # compute mapping of E6 ids under outer element p using key lookup
    # build key->eid map from the colouring we just computed.
    key_to_eid = {}
    for rid, eid in root_to_e6id.items():
        key_to_eid[e6_key(original_roots[rid])] = eid
    # compute mapping of E6 ids under outer element p (may be partial)
    e6id_after: dict[int, int] = {}
    for rid, eid in root_to_e6id.items():
        rid2 = int(p[rid])
        key2 = e6_key(original_roots[rid2])
        if key2 in key_to_eid:
            # record mapping; later entries may overwrite but all valid ones
            e6id_after[eid] = key_to_eid[key2]
    # identify e6ids with no representatives remaining inside the colour set
    all_eids = set(root_to_e6id.values())
    completely_unmapped = sorted(all_eids - set(e6id_after.keys()))
    if completely_unmapped:
        print(
            "outer element sends these e6ids completely outside colour set:",
            completely_unmapped,
        )
    else:
        print("every e6id has at least one representative remaining in colour set")
    # optionally also report partial failures
    partial_unmapped = sorted(
        {eid for eid in all_eids if eid not in completely_unmapped}
    )
    print("(partial unmapped counts will be visible in perm27 if present)")
    # build perm27 list with -1 for completely unmapped ids
    perm27 = [-1] * 27
    for eid, eid2 in e6id_after.items():
        perm27[eid] = eid2
    # write artifact
    with open(out_dir + "/we6_outer_e6id_perm.json", "w") as f:
        json.dump(perm27, f)
    if completely_unmapped:
        with open(out_dir + "/we6_outer_e6id_unmapped.json", "w") as f:
            json.dump(completely_unmapped, f)

    # CE2 coordinate transformation (allow partial mapping)
    try:
        from ce2_global_cocycle import _heisenberg_vec_maps

        e6id_to_vec, _ = _heisenberg_vec_maps()
        # compute u,z before/after for each e6id
        u_before = [
            (int(e6id_to_vec[i][0]) % 3, int(e6id_to_vec[i][1]) % 3) for i in range(27)
        ]
        z_before = [int(e6id_to_vec[i][2]) % 3 for i in range(27)]
        u_after = []
        z_after = []
        for i in range(27):
            if perm27[i] >= 0:
                u_after.append(u_before[perm27[i]])
                z_after.append(z_before[perm27[i]])
            else:
                u_after.append(None)
                z_after.append(None)
        with open(out_dir + "/we6_outer_e6id_coords.json", "w") as f:
            json.dump(
                {
                    "u_before": u_before,
                    "z_before": z_before,
                    "u_after": u_after,
                    "z_after": z_after,
                },
                f,
            )
        # also build a permutation of the 27 H27 points, using lexicographic
        # ordering of (u1,u2,z) triples to index the set.
        h27_list = sorted(
            (u_before[i][0], u_before[i][1], z_before[i]) for i in range(27)
        )
        vec_to_hidx = {v: i for i, v in enumerate(h27_list)}
        h27_perm = [-1] * 27
        for eid, eid2 in enumerate(perm27):
            if eid2 >= 0:
                before_vec = (u_before[eid][0], u_before[eid][1], z_before[eid])
                after_vec = (u_before[eid2][0], u_before[eid2][1], z_before[eid2])
                h27_perm[vec_to_hidx[before_vec]] = vec_to_hidx[after_vec]
        with open(out_dir + "/we6_outer_h27_perm.json", "w") as f:
            json.dump(h27_perm, f)
    except Exception as exc:
        print("Failed to compute CE2 coordinate transform:", exc)


if __name__ == "__main__":
    main()
