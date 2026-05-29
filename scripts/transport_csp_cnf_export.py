"""Export the transport CSP as a DIMACS CNF for external SAT solvers.

This script imports the repo packet builder, constructs the same
symmetry-reduced CSP used by the in-repo search, and writes a DIMACS CNF
plus a JSON variable map so external SAT/MaxSAT/Solver farms can be used.

Usage (run inside repo venv):
  python scripts/transport_csp_cnf_export.py --out data/transport_seed0.cnf --seed 0

By default the script will emit three CNFs with the first orbit representative
fixed to 0,1,2 (three symmetry-break seeds) to explore the symmetric quotient.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import List, Optional, Tuple


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def compute_branch_perm_if_consistent(perm: Tuple[int, ...], n_cells: int, per_cell: int) -> Optional[Tuple[int, ...]]:
    if len(perm) != n_cells * per_cell:
        return None
    f0 = tuple(perm[j] % per_cell for j in range(per_cell))
    for cell in range(n_cells):
        fc = tuple(perm[cell * per_cell + j] % per_cell for j in range(per_cell))
        if fc != f0:
            return None
    return f0


def varnum(i: int, b: int, per_cell: int) -> int:
    return i * per_cell + b + 1


def build_cnf(packet_cycles: List[Tuple[int, ...]], packet_image: List[Tuple[int, ...]], per_cell: int = 3, seed_fix: Optional[int] = None, lexleader: bool = False, lexleader_strong: bool = False, lexleader_prefix_length: int = 8, commander_size: int = 0):
    n = len(packet_cycles)
    # detect per_cell if inconsistent
    if per_cell <= 0:
        per_cell = 3
    if n % per_cell != 0:
        for d in [2, 3, 4, 5]:
            if n % d == 0:
                per_cell = d
                break
    n_cells = n // per_cell

    # group_map: list of (perm, branch|None)
    group_raw = [tuple(p) for p in packet_image]
    group_map: List[Tuple[Tuple[int, ...], Optional[Tuple[int, ...]]]] = []
    for perm in group_raw:
        branch = compute_branch_perm_if_consistent(perm, n_cells, per_cell)
        group_map.append((perm, branch))

    clauses: List[List[int]] = []

    # each quadrangle picks exactly one label (at-least-one + at-most-one)
    # We'll use a sequential-counter-style encoding for the at-most-one constraints
    # to reduce CNF size instead of naive pairwise encoding.
    next_aux = n * per_cell + 1

    def add_at_most_one_seq(vars_list):
        """Add sequential-encoding at-most-one for variables in vars_list.

        vars_list: list of positive var numbers
        returns: modifies clauses in-place and returns the next available aux var id
        """
        nonlocal clauses, next_aux
        m = len(vars_list)
        if m <= 1:
            return next_aux
        # allocate m-1 auxiliary s1..s_{m-1}
        s = list(range(next_aux, next_aux + (m - 1)))
        next_aux += (m - 1)
        # (¬x1 ∨ s1)
        clauses.append([-vars_list[0], s[0]])
        # for i=2..m-1: (¬xi ∨ si)
        for i in range(1, m - 1):
            clauses.append([-vars_list[i], s[i]])
        # for i=2..m: (¬xi ∨ ¬s_{i-1})
        for i in range(1, m):
            clauses.append([-vars_list[i], -s[i - 1]])
        # for i=2..m-1: (¬s_{i-1} ∨ s_i)
        for i in range(1, m - 1):
            clauses.append([-s[i - 1], s[i]])
        return next_aux

    def add_commander(vars_list, commander_size: int):
        """Add a commander encoding at-most-one constraint for vars_list.

        This partitions vars_list into small groups of size commander_size,
        enforces pairwise at-most-one inside each group (since groups are small),
        introduces a commander variable per group, links each group member to
        its commander, and enforces at-most-one on commanders (via sequential encoding).
        Returns: updates clauses and next_aux and returns next_aux.
        """
        nonlocal clauses, next_aux
        m = len(vars_list)
        if m <= 1 or commander_size <= 1 or commander_size >= m:
            return add_at_most_one_seq(vars_list)
        groups = [vars_list[i : i + commander_size] for i in range(0, m, commander_size)]
        commander_vars = []
        for group in groups:
            # small group -> use pairwise at-most-one inside group
            for i in range(len(group)):
                for j in range(i + 1, len(group)):
                    clauses.append([-group[i], -group[j]])
            c = next_aux
            next_aux += 1
            commander_vars.append(c)
            # link each variable to commander: (¬x ∨ c)
            for v in group:
                clauses.append([-v, c])
        # enforce at-most-one across commander_vars using sequential encoding
        next_aux = add_at_most_one_seq(commander_vars)
        return next_aux

    for i in range(n):
        # at least one
        clauses.append([varnum(i, b, per_cell) for b in range(per_cell)])
        # at most one via sequential encoding
        vars_list = [varnum(i, b, per_cell) for b in range(per_cell)]
        if commander_size and len(vars_list) > commander_size:
            next_aux = add_commander(vars_list, commander_size)
        else:
            next_aux = add_at_most_one_seq(vars_list)

    # per-cell: each label b used exactly once per cell (at-least-one + at-most-one)
    for cell in range(n_cells):
        indices = [cell * per_cell + j for j in range(per_cell)]
        for b in range(per_cell):
            # at least one index in the cell takes label b
            clauses.append([varnum(idx, b, per_cell) for idx in indices])
            # at most one: use sequential encoding on the variables for this label across the cell
            vars_list = [varnum(idx, b, per_cell) for idx in indices]
            if commander_size and len(vars_list) > commander_size:
                next_aux = add_commander(vars_list, commander_size)
            else:
                next_aux = add_at_most_one_seq(vars_list)

    # equivariance implications: x[i,b] -> x[perm[i], branch[b]] (or equality when branch is None)
    for perm, branch in group_map:
        for i in range(n):
            for b in range(per_cell):
                if branch is None:
                    # enforce equivalence both ways (-x_{i,b} or x_{perm[i],b}) and (-x_{perm[i],b} or x_{i,b})
                    clauses.append([-varnum(i, b, per_cell), varnum(perm[i], b, per_cell)])
                    clauses.append([-varnum(perm[i], b, per_cell), varnum(i, b, per_cell)])
                else:
                    clauses.append([-varnum(i, b, per_cell), varnum(perm[i], branch[b], per_cell)])

    # symmetry-breaking: if seed_fix provided, fix representative 0 to seed value
    if seed_fix is not None:
        # pick rep 0 as first index
        rep0 = 0
        # fix x[rep0,seed_fix] true and others false
        clauses.append([varnum(rep0, seed_fix, per_cell)])
        for b in range(per_cell):
            if b != seed_fix:
                clauses.append([-varnum(rep0, b, per_cell)])

    # optional lex-leader canonicalization across full group orbits
    # This forbids any representative in an orbit having a strictly greater
    # numeric label than any of its images under the group. For per_cell=3
    # labels are ordered 0<1<2; we ban (rep>img) by forbidding (rep=2 and img=0/1)
    # and (rep=1 and img=0). This is a lightweight lexicographic breaker.
    if lexleader:
        # compute full group permutations (ignore branch permutations for canonicalization)
        group_raw = [tuple(p) for p in packet_image]
        # build orbits of indices under group action
        indices = list(range(n))
        visited = set()
        orbits: List[List[int]] = []
        for i in indices:
            if i in visited:
                continue
            orbit = set()
            stack = [i]
            while stack:
                cur = stack.pop()
                if cur in orbit:
                    continue
                orbit.add(cur)
                for perm in group_raw:
                    nxt = perm[cur]
                    if nxt not in orbit:
                        stack.append(nxt)
            for v in orbit:
                visited.add(v)
            orbits.append(sorted(orbit))
        if not lexleader_strong:
            # lightweight per-index forbids (existing behavior)
            for orbit in orbits:
                if len(orbit) <= 1:
                    continue
                rep = min(orbit)
                for j in orbit:
                    if j <= rep:
                        continue
                    if per_cell >= 3:
                        clauses.append([-varnum(rep, 2, per_cell), -varnum(j, 0, per_cell)])
                        clauses.append([-varnum(rep, 2, per_cell), -varnum(j, 1, per_cell)])
                        clauses.append([-varnum(rep, 1, per_cell), -varnum(j, 0, per_cell)])
                    else:
                        for b_rep in range(per_cell):
                            for b_j in range(per_cell):
                                if b_rep > b_j:
                                    clauses.append([-varnum(rep, b_rep, per_cell), -varnum(j, b_j, per_cell)])
        else:
            # stronger lex-leader: enforce prefix lexicographic minimality of the orbit
            # Compare sequences of labels on the first `lexleader_prefix_length` positions
            # (or full orbit length if smaller). We introduce auxiliary variables for
            # equality at each position and prefix-equality flags and then forbid the
            # pattern where the representative is strictly greater than an image at
            # the first differing position.
            for orbit in orbits:
                L = len(orbit)
                if L <= 1:
                    continue
                rep = min(orbit)
                prefix_len = L if lexleader_prefix_length is None else min(lexleader_prefix_length, L)
                for perm in group_raw:
                    # compare the ordered orbit sequence to its permuted image
                    # build per-position equality auxiliaries and prefix auxiliaries
                    eq_vars = []
                    for pos in range(prefix_len):
                        i_rep = orbit[pos]
                        i_img = perm[i_rep]
                        # e_{pos,b} variables for rep(i_rep,b) AND img(i_img,b)
                        e_vars = []
                        for b in range(per_cell):
                            e_var = next_aux
                            next_aux += 1
                            # e_var -> rep and img
                            clauses.append([-e_var, varnum(i_rep, b, per_cell)])
                            clauses.append([-e_var, varnum(i_img, b, per_cell)])
                            # rep and img -> e_var
                            clauses.append([-varnum(i_rep, b, per_cell), -varnum(i_img, b, per_cell), e_var])
                            e_vars.append(e_var)
                        # eq_pos variable is OR of e_vars
                        eq_var = next_aux
                        next_aux += 1
                        for ev in e_vars:
                            clauses.append([-ev, eq_var])
                        clauses.append([-eq_var] + e_vars)
                        eq_vars.append(eq_var)

                    # prefix flags pref_t for t=0..prefix_len (pref_0 is true)
                    pref_vars = []
                    # pref_0 true sentinel
                    pref0 = next_aux
                    next_aux += 1
                    clauses.append([pref0])
                    pref_vars.append(pref0)
                    for t in range(1, prefix_len + 1):
                        pref_t = next_aux
                        next_aux += 1
                        # pref_t -> pref_{t-1}
                        clauses.append([-pref_t, pref_vars[t - 1]])
                        # pref_t -> eq_{t-1}
                        clauses.append([-pref_t, eq_vars[t - 1]])
                        # pref_{t-1} and eq_{t-1} -> pref_t
                        clauses.append([-pref_vars[t - 1], -eq_vars[t - 1], pref_t])
                        pref_vars.append(pref_t)

                    # forbid case where for first differing position t rep > img
                    for t in range(prefix_len):
                        i_rep = orbit[t]
                        i_img = perm[i_rep]
                        # for each pair (b_rep > b_img) create g var for conjunction
                        for b_rep in range(per_cell):
                            for b_img in range(per_cell):
                                if b_rep <= b_img:
                                    continue
                                gvar = next_aux
                                next_aux += 1
                                # gvar <-> (rep(i_rep,b_rep) AND img(i_img,b_img))
                                clauses.append([-varnum(i_rep, b_rep, per_cell), -varnum(i_img, b_img, per_cell), gvar])
                                clauses.append([-gvar, varnum(i_rep, b_rep, per_cell)])
                                clauses.append([-gvar, varnum(i_img, b_img, per_cell)])
                                # forbid pref_t AND gvar
                                clauses.append([-pref_vars[t], -gvar])

    return clauses, n, per_cell


def write_dimacs(clauses: List[List[int]], nvars: int, out_path: Path, var_map: dict):
    # header: p cnf <vars> <clauses>
    with out_path.open("w", encoding="utf-8") as fh:
        fh.write(f"c generated by transport_csp_cnf_export.py\n")
        fh.write(f"c varmap: {json.dumps(var_map)}\n")
        fh.write(f"p cnf {nvars} {len(clauses)}\n")
        for cl in clauses:
            fh.write(" ".join(str(lit) for lit in cl) + " 0\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="data/transport_seed0.cnf")
    parser.add_argument("--seeds", default="0,1,2", help="comma-separated seed fixes for first rep; use '' for no seed")
    parser.add_argument("--lexleader", action="store_true", help="Add lex-leader symmetry-breaking constraints to the CNF (rep_label <= images)")
    parser.add_argument("--lexleader-strong", action="store_true", help="Use stronger prefix lex-leader canonicalization (may increase CNF size)")
    parser.add_argument("--lexleader-prefix-length", type=int, default=8, help="Prefix length for strong lex-leader (default 8)")
    parser.add_argument("--lexleader-full", action="store_true", help="Use full-orbit lex-leader canonicalization (compare full orbit sequences)")
    parser.add_argument("--commander-size", type=int, default=0, help="Use commander encoding with this group size for at-most-one (0 disables)")
    args = parser.parse_args()

    out = Path(args.out)
    out.parent.mkdir(exist_ok=True, parents=True)

    try:
        from scripts.w33_h4_orbital_no_go import compute_quadrangle_adjacent_transport_packet_action_data
    except Exception as exc:
        print(json.dumps({"status": "missing_repo_function", "error": str(exc)}))
        return

    try:
        data = compute_quadrangle_adjacent_transport_packet_action_data()
    except Exception as exc:
        print(json.dumps({"status": "compute_failed", "error": str(exc)}))
        return

    packet_cycles = data.get("packet_cycles") or []
    packet_image = list(data.get("packet_image") or [])

    if not packet_cycles:
        print(json.dumps({"status": "no_packet_cycles_found", "n": 0}))
        return

    seeds = [s for s in args.seeds.split(",") if s != ""]
    if not seeds:
        seeds = [None]
    for s in seeds:
        seed_val = None if s is None else int(s)
        # If --lexleader-full is passed, instruct build_cnf to use full-orbit prefix length
        lexleader_prefix = None if args.lexleader_full else args.lexleader_prefix_length
        clauses, n, per_cell = build_cnf(
            packet_cycles,
            packet_image,
            per_cell=3,
            seed_fix=seed_val,
            lexleader=args.lexleader,
            lexleader_strong=args.lexleader_strong,
            lexleader_prefix_length=lexleader_prefix,
            commander_size=int(args.commander_size),
        )
        # compute actual number of variables including any auxiliary vars introduced
        maxvar = 0
        for cl in clauses:
            for lit in cl:
                maxvar = max(maxvar, abs(int(lit)))
        nvars = maxvar
        if seed_val is None:
            fname = out
        else:
            fname = out.parent / f"{out.stem}_seed{seed_val}.cnf"
        # variable map for interpreting solver output
        var_map = {str(varnum(i, b, per_cell)): [i, b] for i in range(n) for b in range(per_cell)}
        write_dimacs(clauses, nvars, fname, var_map)
        meta = {
            "status": "wrote_cnf",
            "cnf_path": str(fname),
            "nvars": nvars,
            "nclauses": len(clauses),
            "seed": seed_val,
            "lexleader": bool(args.lexleader),
            "lexleader_strong": bool(args.lexleader_strong),
            "lexleader_prefix_length": (None if args.lexleader_full else int(args.lexleader_prefix_length)),
            "lexleader_full": bool(args.lexleader_full),
            "commander_size": int(args.commander_size),
        }
        meta_path = fname.with_suffix(fname.suffix + ".meta.json")
        meta_path.write_text(json.dumps(meta, indent=2))
        print(json.dumps(meta))


if __name__ == "__main__":
    main()
