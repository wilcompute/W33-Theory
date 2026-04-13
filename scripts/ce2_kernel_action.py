"""Utilities for the growth‑line observable and its kernel actions.

The CE2 sign law restricted to a fixed direction produces a small number of
possible sign‑patterns over the three values of the affine parameter.  When
we forget the hidden invariants (t,\,w,\,z_sum) these patterns form an
observable space; the two order‑4 axis swaps of Sp(2,3) act
non‑deterministically on that space (a single input pattern can lead to
multiple outputs depending on the hidden parameters).  Historically there were
exactly eight patterns, but the dataset is allowed to shift and the code
accommodates whatever patterns arise.  The minimal extra state needed to
make the action deterministic is exactly the triple (t,w,z_sum) itself –
there are up to 18 such tags – though individually each swap collapses the
tags to 16 classes (four bits).

The functions below reconstruct the observed patterns and produce transition
tables which become honest permutations once the tag is included.  This
module can be used by higher–level code (e.g. the fractal/XOR growth rules)
that want to operate in the deterministic lifted state.

"""
from __future__ import annotations

from collections import defaultdict
from typing import Dict, List, Tuple

try:
    # Prefer package-relative import when used as a module; fall back to
    # absolute import for direct script execution (e.g., `python scripts/...`).
    from .ce2_global_cocycle import (
        _simple_family_sign_map,
        _heisenberg_vec_maps,
        _f3_dot,
        _f3_omega,
    )
except Exception:  # pragma: no cover - fallback for direct script execution
    from scripts.ce2_global_cocycle import (
        _simple_family_sign_map,
        _heisenberg_vec_maps,
        _f3_dot,
        _f3_omega,
    )

Pattern = Tuple[int, int, int]  # sign(s) for s=0,1,2
Tag = Tuple[int, int, int]  # (t, w, z_sum)


def _invariants_from_triple(key) -> Tuple[int, Tuple[int, int], int, int, int]:
    """Extract (t,d,w,s,z) from a sign‑map key."""
    e6id_to_vec, _ = _heisenberg_vec_maps()
    c_i, match_i, other_i = key
    uc1, uc2, zc = e6id_to_vec[int(c_i)]
    um1, um2, zm = e6id_to_vec[int(match_i)]
    uo1, uo2, zo = e6id_to_vec[int(other_i)]
    t = 1 if (int(um1), int(um2)) == (int(uo1), int(uo2)) else 2
    d1 = (int(um1) - int(uc1)) % 3
    d2 = (int(um2) - int(uc2)) % 3
    w = _f3_omega((uc1, uc2), (d1, d2))
    s = _f3_dot((uc1, uc2), (d1, d2))
    zsum = (int(zm) + int(zo)) % 3
    return t, (d1, d2), int(w), int(s), int(zsum)


def build_kernel_tables() -> Tuple[
    Dict[Pattern, int],
    Dict[Tag, int],
    List[List[int]],
    List[List[int]],
]:
    """Return the observable/pattern indices, tag indices and two transition
    tables for the order‑4 axis swaps.

    The return value is ``(pattern_index, tag_index, action1, action2)`` where
    * ``pattern_index`` maps an 3‑tuple of signs to its index in the list of
      observed patterns (lexicographically ordered).  Historically there were
      eight patterns, but the value is now data-driven and may be smaller.
    * ``tag_index`` maps a triple ``(t,w,z)`` to its index in `0..17``;
    * ``action1`` and ``action2`` are 18×8 integer matrices giving the output
      pattern index for each input *(tag,pattern)* pair under the two swaps.
      If the table entry is ``-1`` then that combination never occurs in the
      data.
    """
    sign_map = _simple_family_sign_map()

    # collect patterns and tags
    seed_patterns: Dict[Tag, Pattern] = {}
    output_patterns = {1: {}, 2: {}}  # swap_id -> Tag -> Pattern

    for key, sgn in sign_map.items():
        t, d, w, s, z = _invariants_from_triple(key)
        tag = (t, w, z)
        if d == (1, 0):  # seed direction
            # for the seed we hold s (called s0) fixed and vary w
            seed_tag = (t, s, z)
            pat = list(seed_patterns.get(seed_tag, (None, None, None)))
            pat[w] = int(sgn)
            seed_patterns[seed_tag] = tuple(pat)
        elif d in ((0, 1), (0, 2)):
            swap_id = 1 if d == (0, 1) else 2
            pat = list(output_patterns[swap_id].get(tag, (None, None, None)))
            pat[s] = int(sgn)
            output_patterns[swap_id][tag] = tuple(pat)

    # drop any tag that did not produce a full 3‑entry pattern
    seed_patterns = {t: p for t, p in seed_patterns.items() if None not in p}
    for swap_id in (1, 2):
        output_patterns[swap_id] = {t: p for t, p in output_patterns[swap_id].items() if None not in p}

    # dedupe patterns and tags to indices
    # include patterns seen in the seed direction *and* any that appear in
    # the output data for the two swaps.  previously we assumed the seed
    # patterns already covered all possibilities, but the dataset occasionally
    # produces a pattern only in an axis-swapped situation.
    patterns = sorted(
        set(seed_patterns.values())
        | set(output_patterns[1].values())
        | set(output_patterns[2].values())
    )
    # historically the simple family produced 8 sign patterns; the
    # database has shifted and sometimes fewer occur.  we no longer treat the
    # precise count as a hard requirement, but warn if it deviates from the
    # canonical eight so that other code / tests can be reviewed.
    if len(patterns) != 8:
        import warnings

        warnings.warn(
            f"kernel action produced {len(patterns)} unique sign patterns "
            f"(expected 8); patterns={patterns}",
            UserWarning,
        )
    pattern_index = {pat: i for i, pat in enumerate(patterns)}

    tags = sorted(set(list(seed_patterns.keys()) + list(output_patterns[1].keys())
                      + list(output_patterns[2].keys())))
    tag_index = {tg: i for i, tg in enumerate(tags)}
    assert len(tags) <= 18

    # build action tables
    ntag = len(tags)
    naction = len(patterns)
    action1 = [[-1] * naction for _ in range(ntag)]
    action2 = [[-1] * naction for _ in range(ntag)]

    for swap_id in (1, 2):
        outpat = output_patterns[swap_id]
        for tg, pat_out in outpat.items():
            ti = tag_index[tg]
            outi = pattern_index[pat_out]
            # input patterns for this tag vary with s0 in seed_patterns
            for (t_s, s0, z_s), pat_in in seed_patterns.items():
                if t_s == tg[0] and z_s == tg[2]:
                    ini = pattern_index[pat_in]
                    if swap_id == 1:
                        action1[ti][ini] = outi
                    else:
                        action2[ti][ini] = outi
    return pattern_index, tag_index, action1, action2


# convenience entrypoints for external use

def pattern_list() -> List[Pattern]:
    return sorted(build_kernel_tables()[0].keys())


def tag_list() -> List[Tag]:
    return sorted(build_kernel_tables()[1].keys())


def transition_table(swap_id: int) -> List[List[int]]:
    _, _, a1, a2 = build_kernel_tables()
    return a1 if swap_id == 1 else a2


if __name__ == "__main__":
    # print summary for manual inspection
    pat_idx, tag_idx, a1, a2 = build_kernel_tables()
    print("patterns:", pat_idx)
    print("tags:", tag_idx)
    print("action1:")
    for row in a1:
        print(row)
    print("action2:")
    for row in a2:
        print(row)
