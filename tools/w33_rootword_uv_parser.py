#!/usr/bin/env python3
"""W33 root-word -> (u,v) parser

Given an 8-edge E8 root-word (list of 8 root 8-tuples), reconstruct the W33
8-cycle (vertex sequence), detect the two N12 lines appearing in the cycle,
map them to direction vectors in F3^2 via the canonical slope mapping, and
return both (k_if_uv, k_if_vu) and a canonical (u_canonical, v_canonical, k_canonical)
by rotating the cycle so the smaller N12 vertex appears first.

This is intentionally lightweight and contains robust handling of the two
common edge->root JSON formats used in this repo.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple

Int8Vec = Tuple[int, ...]


class W33RootwordParser:
    def __init__(
        self,
        edge_root_json: str | Path = Path("artifacts/edge_to_e8_root_combined.json"),
        n12_csv: str | Path = Path(
            "analysis/w33_bundle_temp/N12_vertices_as_affine_lines.csv"
        ),
    ) -> None:
        self.edge_root_json = Path(edge_root_json)
        self.n12_csv = Path(n12_csv)

        # load edge->root mapping (format: {"(i, j)": [..root..], ...})
        self.edge_to_root: Dict[Tuple[int, int], Int8Vec] = {}
        self._load_edge_to_root()

        # build vector->edge map: map vector tuple -> stored (i,j) edge
        self.vec_to_edge: Dict[Int8Vec, Tuple[int, int]] = {}
        for e, r in self.edge_to_root.items():
            rt = tuple(int(x) for x in r)
            self.vec_to_edge[rt] = e

        # load N12 table
        self.n12_info: Dict[int, Dict] = {}
        self._load_n12_table()

        # slope -> direction (u) mapping (F3^2)
        self.slope_to_uv = {"inf": (0, 1), "0": (1, 0), "2": (1, 2), "1": (1, 1)}

    # ------------------------ loading helpers ------------------------
    def _parse_edge_key(self, k: str) -> Tuple[int, int]:
        s = k.strip()
        if s.startswith("(") and s.endswith(")"):
            s = s[1:-1]
        parts = [p.strip() for p in s.split(",") if p.strip()]
        if len(parts) != 2:
            raise RuntimeError(f"Unsupported edge key: {k}")
        return int(parts[0]), int(parts[1])

    def _load_edge_to_root(self) -> None:
        data = (
            json.loads(self.edge_root_json.read_text(encoding="utf-8"))
            if self.edge_root_json.exists()
            else {}
        )
        raw_map: Dict[Tuple[int, int], Tuple[int, ...]] = {}
        if isinstance(data, dict):
            for k, v in data.items():
                a, b = self._parse_edge_key(k)
                coords = tuple(int(x) for x in v)
                raw_map[(a, b)] = coords
        else:
            # fallback: list of objects with v_i, v_j, root_coords
            for ent in data:
                a = int(ent["v_i"])
                b = int(ent["v_j"])
                coords = tuple(int(x) for x in ent["root_coords"])
                raw_map[(a, b)] = coords

        # Aggregate candidate oriented edges for each vector from multiple sources
        # Track source tags so we can prefer canonical bijection edges when choosing between solutions
        vec_to_edges: Dict[Tuple[int, ...], List[Tuple[Tuple[int, int], str]]] = {}

        def add_candidate(vec: Tuple[int, ...], edge: Tuple[int, int], tag: str):
            vec_to_edges.setdefault(tuple(vec), []).append((edge, tag))

        # populate from raw_map (and also add +-1 offsets to be robust)
        for (a, b), coords in raw_map.items():
            add_candidate(coords, (a, b), "raw")
            add_candidate(tuple(-x for x in coords), (b, a), "raw")
            add_candidate(coords, (a + 1, b + 1), "raw-offset")
            add_candidate(tuple(-x for x in coords), (b + 1, a + 1), "raw-offset")
            add_candidate(coords, (a - 1, b - 1), "raw-offset")
            add_candidate(tuple(-x for x in coords), (b - 1, a - 1), "raw-offset")

        # canonical bijection list (prefer this source)
        try:
            cand_list = json.loads(
                Path("artifacts/edge_root_bijection_canonical.json").read_text(
                    encoding="utf-8"
                )
            )
            for ent in cand_list:
                a = int(ent["v_i"])
                b = int(ent["v_j"])
                coords = tuple(int(x) for x in ent["root_coords"])
                add_candidate(coords, (a + 1, b + 1), "canon")
                add_candidate(tuple(-x for x in coords), (b + 1, a + 1), "canon")
        except Exception:
            pass

        # additional mapping sources (we6 orbit file, e8 root->edge mapping, archive)
        try:
            # artifacts/e8_root_to_w33_edge.json contains a 'root_to_edge' mapping keyed by stringified vectors
            e8_root_map_path = Path("artifacts/e8_root_to_w33_edge.json")
            if e8_root_map_path.exists():
                em = json.loads(e8_root_map_path.read_text(encoding="utf-8"))
                rtmap = em.get("root_to_edge", {})
                for k, v in rtmap.items():
                    try:
                        if isinstance(k, str):
                            if k.strip().startswith("["):
                                coords = tuple(int(x) for x in json.loads(k))
                            else:
                                coords = tuple(
                                    int(x.strip()) for x in k.strip("()").split(",")
                                )
                        else:
                            coords = tuple(int(x) for x in k)
                        a = int(v[0])
                        b = int(v[1])
                        add_candidate(coords, (a + 1, b + 1), "e8root")
                        add_candidate(
                            tuple(-x for x in coords), (b + 1, a + 1), "e8root"
                        )
                    except Exception:
                        continue
        except Exception:
            pass

        try:
            # artifacts/edge_to_e8_root_we6_orbits.json contains float (half-integer) coords; multiply by 2 to get integer vectors
            we6_path = Path("artifacts/edge_to_e8_root_we6_orbits.json")
            if we6_path.exists():
                we6 = json.loads(we6_path.read_text(encoding="utf-8"))
                for k, coords in we6.items():
                    a, b = self._parse_edge_key(k)
                    coords_int = tuple(int(round(float(x) * 2)) for x in coords)
                    add_candidate(coords_int, (a + 1, b + 1), "we6")
                    add_candidate(tuple(-x for x in coords_int), (b + 1, a + 1), "we6")
        except Exception:
            pass

        try:
            # artifacts/e8_root_to_edge.json maps string root keys to 0-based edge pairs
            e8r_path = Path("artifacts/e8_root_to_edge.json")
            if e8r_path.exists():
                e8r = json.loads(e8r_path.read_text(encoding="utf-8"))
                for k, v in e8r.items():
                    try:
                        coords = tuple(int(x.strip()) for x in k.strip("()").split(","))
                        a, b = int(v[0]), int(v[1])
                        add_candidate(coords, (a + 1, b + 1), "e8root_to_edge")
                        add_candidate(
                            tuple(-x for x in coords), (b + 1, a + 1), "e8root_to_edge"
                        )
                    except Exception:
                        continue
        except Exception:
            pass

        # archived mapping as a final fallback
        try:
            archive = Path("artifacts_archive/e8_root_to_w33_edge.json")
            if archive.exists():
                arc = json.loads(archive.read_text(encoding="utf-8"))
                for s, v in arc.items():
                    coords = tuple(int(x.strip()) for x in s.strip("[]").split(","))
                    a = int(v[0])
                    b = int(v[1])
                    add_candidate(coords, (a, b), "archive")
                    add_candidate(tuple(-x for x in coords), (b, a), "archive")
        except Exception:
            pass

        # normalize, filter invalid vertices, and deduplicate while keeping tags
        def valid_edge(e):
            a, b = e
            return 1 <= a <= 40 and 1 <= b <= 40

        cleaned: Dict[Tuple[int, ...], List[Tuple[Tuple[int, int], str]]] = {}
        for vec, entries in vec_to_edges.items():
            seen = []
            for edge, tag in entries:
                if valid_edge(edge) and (edge, tag) not in seen:
                    seen.append((edge, tag))
            if seen:
                cleaned[vec] = seen

        self.vec_to_edges_map = cleaned

        # Build a convenient canonical edge->root mapping (prefer raw_map with presumed 0-base -> to 1-based)
        if raw_map:
            min_idx = min(min(k) for k in raw_map.keys())
            for (a, b), coords in raw_map.items():
                if min_idx == 0:
                    self.edge_to_root[(a + 1, b + 1)] = coords
                    self.edge_to_root[(b + 1, a + 1)] = tuple(-x for x in coords)
                else:
                    self.edge_to_root[(a, b)] = coords
                    self.edge_to_root[(b, a)] = tuple(-x for x in coords)

        # Overlay aggregated vec->edges candidates into edge_to_root, prefer high-quality tags
        # Expanded priorities to prefer canonical & raw mappings, then we6/e8root sources
        priority = {
            "canon": 6,
            "raw": 5,
            "we6": 4,
            "e8root": 4,
            "e8root_to_edge": 4,
            "raw-offset": 3,
            "fallback": 2,
            "archive": 1,
        }
        recorded_tags: Dict[Tuple[int, int], str] = {}
        for vec, entries in self.vec_to_edges_map.items():
            for edge, tag in entries:
                a, b = edge
                if not (1 <= a <= 40 and 1 <= b <= 40):
                    continue
                cur_tag = recorded_tags.get(edge)
                if cur_tag is None or priority.get(tag, 0) > priority.get(cur_tag, 0):
                    self.edge_to_root[edge] = vec
                    self.edge_to_root[(b, a)] = tuple(-x for x in vec)
                    recorded_tags[edge] = tag

        # Rebuild single-mapping vec->edge for quick lookup fallbacks
        self.vec_to_edge = {}
        for e, r in self.edge_to_root.items():
            rt = tuple(int(x) for x in r)
            self.vec_to_edge[rt] = e

    def _load_n12_table(self) -> None:
        if not self.n12_csv.exists():
            return
        with self.n12_csv.open("r", encoding="utf-8") as f:
            rdr = csv.DictReader(f)
            for r in rdr:
                nid = int(r["N12_vertex"])
                slope = str(r["slope_m"]).strip()
                # parse H vertices in coset (space separated)
                hv = [int(x) for x in r["H_vertices_in_coset"].split() if x.strip()]
                # parse phase points like "(0,0); (0,1); (0,2)"
                pp = []
                for part in r.get("phase_points", "").split(";"):
                    part = part.strip()
                    if not part:
                        continue
                    if part.startswith("(") and part.endswith(")"):
                        inner = part[1:-1]
                    else:
                        inner = part
                    a, b = [int(x.strip()) for x in inner.split(",")]
                    pp.append((a, b))
                self.n12_info[nid] = {
                    "slope": slope,
                    "H_vertices": set(hv),
                    "phase_points": pp,
                }

    # ------------------------ core parsing ------------------------
    def _negate_vec(self, v: Int8Vec) -> Int8Vec:
        return tuple(-int(x) for x in v)

    def _map_vec_to_oriented_edge(self, v: Int8Vec) -> Tuple[int, int]:
        # If v matches a stored vector exactly -> oriented edge is stored (a,b)
        # If -v matches stored vector -> oriented edge is reversed (b,a)
        vt = tuple(int(x) for x in v)
        if vt in self.vec_to_edge:
            return self.vec_to_edge[vt]
        nvt = self._negate_vec(vt)
        if nvt in self.vec_to_edge:
            a, b = self.vec_to_edge[nvt]
            return (b, a)
        # no mapping
        raise KeyError(f"Root vector not found in edge->root mapping: {vt}")

    def _try_chain(self, roots: List[Int8Vec]) -> Optional[List[Tuple[int, int]]]:
        # Build candidate lists for each root using aggregated vec->edges map
        candidates: List[List[Tuple[int, int]]] = []
        for r in roots:
            rt = tuple(int(x) for x in r)
            nrt = self._negate_vec(rt)
            cands = []
            # add direct candidates and candidates from negated vector
            if hasattr(self, "vec_to_edges_map"):
                cands.extend(self.vec_to_edges_map.get(rt, []))
                cands.extend(self.vec_to_edges_map.get(nrt, []))
            # fall back to single-mapping if available (wrap as tagged pair)
            if not cands and rt in getattr(self, "vec_to_edge", {}):
                e = self.vec_to_edge[rt]
                cands.append((e, "fallback"))
            if not cands and nrt in getattr(self, "vec_to_edge", {}):
                e = self.vec_to_edge[nrt]
                cands.append(((e[1], e[0]), "fallback"))

            # Scaled fallbacks: sometimes coordinates are half/doubled in other artifacts
            if not cands:
                try:
                    scaled_up = tuple(int(round(2 * x)) for x in rt)
                    scaled_up_neg = tuple(-x for x in scaled_up)
                    if getattr(self, "vec_to_edges_map", None):
                        cands.extend(self.vec_to_edges_map.get(scaled_up, []))
                        cands.extend(self.vec_to_edges_map.get(scaled_up_neg, []))
                    # try scale down (x/2) if divisible
                    if all(x % 2 == 0 for x in rt):
                        scaled_down = tuple(int(x // 2) for x in rt)
                        scaled_down_neg = tuple(-x for x in scaled_down)
                        cands.extend(self.vec_to_edges_map.get(scaled_down, []))
                        cands.extend(self.vec_to_edges_map.get(scaled_down_neg, []))
                except Exception:
                    pass

            if not cands:
                return None
            candidates.append(cands)

        n = len(candidates)
        chosen: List[Optional[Tuple[int, int]]] = [None] * n
        solutions: List[List[Tuple[int, int]]] = []

        def dfs_collect(i: int):
            if i == n:
                # check closure: last edge end == first edge start
                if chosen[-1][0][1] == chosen[0][0][0]:
                    solutions.append(list(chosen))
                return
            for cand in candidates[i]:
                if i == 0:
                    chosen[0] = cand
                    dfs_collect(1)
                else:
                    # chosen[i-1] and cand are tuples (edge, tag)
                    prev_edge = chosen[i - 1][0]
                    curr_edge = cand[0]
                    if prev_edge[1] == curr_edge[0]:
                        chosen[i] = cand
                        dfs_collect(i + 1)

        dfs_collect(0)

        if not solutions:
            return None

        # choose the solution that maximizes use of canonical-bijection edges (then raw matches), tie-broken by lexicographic canonical cycle
        def canon_count(sol):
            return sum(1 for (_, tag) in sol if tag == "canon")

        def raw_count(sol):
            return sum(1 for (_, tag) in sol if tag == "raw")

        best_sol = None
        best_key = None  # tuple (canon_count, raw_count, canonical_cycle)
        for sol in solutions:
            # compute canonical cycle tuple; skip malformed solutions
            try:
                v0 = sol[0][0][0]
                cyc = [int(v0)] + [int(e[0][1]) for e in sol]
                cyc = cyc[:-1]
            except Exception:
                continue
            if not all(isinstance(x, int) for x in cyc):
                continue
            can = tuple(self._find_canonical_cycle_rotation(cyc))
            ccount = canon_count(sol)
            rcount = raw_count(sol)
            # prefer higher canonical count, then more raw matches, then lexicographically smallest canonical cycle
            if (
                best_key is None
                or ccount > best_key[0]
                or (ccount == best_key[0] and rcount > best_key[1])
                or (
                    ccount == best_key[0]
                    and rcount == best_key[1]
                    and can < best_key[2]
                )
            ):
                best_key = (ccount, rcount, can)
                best_sol = sol

        # return chosen oriented-edge list (strip tags)
        return [edge for (edge, tag) in best_sol]

    def _rotate(self, seq: List[Int8Vec], s: int) -> List[Int8Vec]:
        n = len(seq)
        return [seq[(i + s) % n] for i in range(n)]

    def _find_canonical_cycle_rotation(self, cyc: List[int]) -> List[int]:
        # canonicalize up to rotation+reversal: pick lexicographically smallest tuple
        n = len(cyc)
        rots = [tuple(cyc[i:] + cyc[:i]) for i in range(n)]
        rev = list(reversed(cyc))
        rots += [tuple(rev[i:] + rev[:i]) for i in range(n)]
        canon = list(min(rots))
        return canon

    def parse(self, rootword: List[List[int]]) -> Dict:
        """Parse an 8-edge E8 root-word and return parsed data.

        Returned dict contains at least:
          - cycle_vertices: List[int] (length 8)
          - oriented_edges: List[ (a,b) ] (length 8)
          - n12_pair: List[int] (two N12 vertex indices chosen)
          - u, v: direction vectors (tuples)
          - k_if_uv, k_if_vu: ints in {0,1,2}
          - u_canonical, v_canonical, k_canonical: canonical ordering result
        """
        if len(rootword) != 8:
            raise ValueError("Expected 8-edge rootword")
        roots = [tuple(int(x) for x in r) for r in rootword]

        # Try rotations of original sequence
        oriented_edges = None
        used_rotation = None
        used_reversed = False

        for s in range(8):
            cand = self._rotate(roots, s)
            chained = self._try_chain(cand)
            if chained is not None:
                oriented_edges = chained
                used_rotation = s
                used_reversed = False
                break
        if oriented_edges is None:
            # try reversed + negated sequence
            revneg = [self._negate_vec(r) for r in reversed(roots)]
            for s in range(8):
                cand = self._rotate(revneg, s)
                chained = self._try_chain(cand)
                if chained is not None:
                    oriented_edges = chained
                    used_rotation = s
                    used_reversed = True
                    break

        if oriented_edges is None:
            raise RuntimeError("Could not reconstruct W33 cycle from rootword")

        # build cycle vertices
        v0 = oriented_edges[0][0]
        cycle_vertices = [v0] + [e[1] for e in oriented_edges]
        # last equals first; drop duplicate final to represent cycle
        cycle_vertices = cycle_vertices[:-1]

        # find two candidate N12s by counts of membership in their H cosets
        counts = []
        for nid, info in self.n12_info.items():
            cnt = sum(1 for v in cycle_vertices if v in info["H_vertices"])
            counts.append((nid, cnt))
        if not counts:
            raise RuntimeError("No N12 table loaded; cannot map to directions")
        counts.sort(key=lambda x: (-x[1], x[0]))
        n1, c1 = counts[0]
        n2, c2 = counts[1]

        # map slopes -> uv
        s1 = self.n12_info[n1]["slope"]
        s2 = self.n12_info[n2]["slope"]
        u = tuple(self.slope_to_uv.get(str(s1), (None, None)))
        v = tuple(self.slope_to_uv.get(str(s2), (None, None)))
        if None in u or None in v:
            raise RuntimeError(f"Unknown slope for N12 {n1} or {n2}: {s1},{s2}")

        def det_mod3(u, v):
            d = (u[0] * v[1] - u[1] * v[0]) % 3
            return d

        k_if_uv = (-det_mod3(u, v)) % 3
        k_if_vu = (-det_mod3(v, u)) % 3

        # canonical ordering: rotate the cycle so the smaller N12 vertex appears first
        small = min(n1, n2)
        other = n2 if small == n1 else n1
        # find earliest cycle vertex index that belongs to the small N12 coset
        idx_small = next(
            (
                i
                for i, cv in enumerate(cycle_vertices)
                if cv in self.n12_info[small]["H_vertices"]
            ),
            None,
        )
        if idx_small is None:
            # fallback: choose the first occurrence of any vertex that is in either coset
            idx_small = next(
                (
                    i
                    for i, cv in enumerate(cycle_vertices)
                    if cv
                    in (
                        self.n12_info[n1]["H_vertices"]
                        | self.n12_info[n2]["H_vertices"]
                    )
                ),
                0,
            )
        # rotate so that vertex is first
        n = len(cycle_vertices)
        rotated = [cycle_vertices[(i + idx_small) % n] for i in range(n)]

        # determine canonical u,v order by which coset appears first after rotation
        # find earliest index where any rotated vertex belongs to small or other coset
        pos_small = next(
            (
                i
                for i, cv in enumerate(rotated)
                if cv in self.n12_info[small]["H_vertices"]
            ),
            None,
        )
        pos_other = next(
            (
                i
                for i, cv in enumerate(rotated)
                if cv in self.n12_info[other]["H_vertices"]
            ),
            None,
        )
        if pos_small is None or pos_other is None:
            # if one of them didn't appear, break ties by numeric order
            u_can, v_can = (
                tuple(self.slope_to_uv[str(self.n12_info[small]["slope"])]),
                tuple(self.slope_to_uv[str(self.n12_info[other]["slope"])]),
            )
        else:
            if pos_small <= pos_other:
                u_can = tuple(self.slope_to_uv[str(self.n12_info[small]["slope"])])
                v_can = tuple(self.slope_to_uv[str(self.n12_info[other]["slope"])])
            else:
                u_can = tuple(self.slope_to_uv[str(self.n12_info[other]["slope"])])
                v_can = tuple(self.slope_to_uv[str(self.n12_info[small]["slope"])])

        # compute canonical k
        k_canonical = (-det_mod3(u_can, v_can)) % 3

        # compute basepoint p as intersection of the two N12 line phase-point sets
        pp1 = set(self.n12_info[n1].get("phase_points", []))
        pp2 = set(self.n12_info[n2].get("phase_points", []))
        inter = pp1 & pp2
        p = tuple(next(iter(inter))) if len(inter) == 1 else None

        out = {
            "cycle_vertices": cycle_vertices,
            "oriented_edges": oriented_edges,
            "n12_pair": [n1, n2],
            "n12_counts": {n1: c1, n2: c2},
            "u": u,
            "v": v,
            "k_if_uv": int(k_if_uv),
            "k_if_vu": int(k_if_vu),
            "u_canonical": tuple(u_can),
            "v_canonical": tuple(v_can),
            "k_canonical": int(k_canonical),
            "p": p,
            "used_rotation": used_rotation,
            "used_reversed": used_reversed,
        }
        return out


if __name__ == "__main__":
    import sys

    p = W33RootwordParser()
    if len(sys.argv) > 1:
        path = Path(sys.argv[1])
        rw = json.loads(path.read_text(encoding="utf-8"))
        print(p.parse(rw))
    else:
        print("W33RootwordParser ready. Use parse(rootword) with a list of 8 roots.")
