"""Pass 12069: flavour CP is a bosonic time reversal, not an observer (Claude track; joins 12004/12044 to 12059-12060).

The generalised CP transformations of the Siegel flavour chain are CP o g with CP: Omega -> -conj(Omega), i.e. the
similitude M_CP = diag(I, -I) of multiplier -1, and g in Sp(4,Z): the theta-group T^{2b} x T^{2b'} family (12004) and
the S-type S x S, S x T^{2b} family (12044). Reduced mod 3 (the level-3 structure = W(3,3), 11869) they act on the
forty events. Exact results:
  1. Every reduced CP element J is ANTI-symplectic with J^2 = +1 (a bosonic time reversal), never J^2 = -1, so no
     flavour CP is a Kramers reversal -- no flavour CP is an observer or a mirror frame (12059-12060).
  2. Anti-symplectic involutions of F_3^4: 1080 elements, 540 up to sign, in bijection with the 540 unordered pairs of
     opposite contexts (L+, L-) = the +-1 eigenspaces. Each fixes exactly the 8 events of L+ u L-.
  3. At every event it fixes, J inverts the tick: J t_p J^-1 = t_p^-1. Flavour CP reverses the time of exactly the eight
     events on its two contexts, and moves the other 32 (J t_p J^-1 = t_{Jp}^-1).
  4. The 16 distinct named CP elements (CP itself = T^0 x T^0, the 9 theta-group T^{2b} x T^{2b'}, S x S, S x T^{2b} and
     T^{2b} x S) reduce to 16 DISTINCT context pairs; CP itself gives (span(e1,e2), span(e3,e4)). The pairs are listed in
     the certificate.
Reading. The geometry has two kinds of time reversal: fermionic (Kramers, J^2 = -1, 36, the observers with their
Lorentz groups) and bosonic (J^2 = +1, 540, the context pairs). The flavour sector's CP is of the second kind. Strong
CP in the corpus is solved by a Nelson-Barr row on CP-fixed loci (12004-12005, 12044); this pass identifies what those
CP elements are on the forty events.
Scope: mod-3 reduction of the named CP elements; the identification of the Siegel CP with M_CP = diag(I,-I) is the
standard one (Ding-Feruglio-Liu arXiv:2010.07952, cited in 12044).
"""

import itertools
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass12059_observers_see_space_not_time as M  # noqa: E402

OUT = ROOT / "data" / "w33_pass12069_flavour_cp_is_a_bosonic_time_reversal.json"
I2 = np.eye(2, dtype=np.int64)
Z2 = np.zeros((2, 2), dtype=np.int64)


def blocks(A, B, C, D):
    return np.block([[A, B], [C, D]]) % 3


def product(m1, m2):  # SL(2) elements on the two torus factors embedded in Sp(4): (a b; c d) per factor
    A = np.diag([m1[0][0], m2[0][0]]); B = np.diag([m1[0][1], m2[0][1]])  # noqa: E702
    C = np.diag([m1[1][0], m2[1][0]]); D = np.diag([m1[1][1], m2[1][1]])  # noqa: E702
    return blocks(A, B, C, D)


def main():
    checks, res = {}, {}
    Om = M.Om
    pts = sorted({M.norm(v) for v in M.VEC if v.any()})
    G = M.build_group(pts)
    MCP = blocks(I2, Z2, Z2, (2 * I2) % 3)
    checks["M_CP = diag(I,-I) is anti-symplectic with J^2 = 1"] = bool(
        np.array_equal((MCP.T @ Om @ MCP) % 3, (2 * Om) % 3) and np.array_equal((MCP @ MCP) % 3, np.eye(4, dtype=int)))
    S = [[0, 2], [1, 0]]
    T = lambda n: [[1, n % 3], [0, 1]]  # noqa: E731
    named = {"CP": product([[1, 0], [0, 1]], [[1, 0], [0, 1]])}
    for b, b2 in itertools.product(range(3), repeat=2):
        named["T^%d x T^%d" % (2 * b, 2 * b2)] = product(T(2 * b), T(2 * b2))
    named["S x S"] = product(S, S)
    for b in range(3):
        named["S x T^%d" % (2 * b)] = product(S, T(2 * b))
        named["T^%d x S" % (2 * b)] = product(T(2 * b), S)
    Js = {k: (g @ MCP) % 3 for k, g in named.items()}
    ok_g = all(np.array_equal((g.T @ Om @ g) % 3, Om % 3) for g in named.values())
    ok_bos = all(np.array_equal((J.T @ Om @ J) % 3, (2 * Om) % 3) and np.array_equal((J @ J) % 3, np.eye(4, dtype=int)) for J in Js.values())
    checks["every named CP o g (theta-group T^2b x T^2b', S x S, S x T^2b) reduces to an anti-symplectic J with J^2 = +1"] = bool(ok_g and ok_bos)
    checks["no flavour CP is a Kramers reversal (J^2 = -1)"] = all(not np.array_equal((J @ J) % 3, (2 * np.eye(4, dtype=int)) % 3) for J in Js.values())

    def eig(J, s):
        return {M.norm(v) for v in M.VEC if v.any() and np.array_equal((J @ v) % 3, (s * v) % 3)}
    # all anti-symplectic involutions: G-conjugates of M_CP
    seen, allJ = set(), []
    for g in G:
        gi = (2 * Om @ g.T @ Om) % 3  # g^-1 = Om^-1 g^T Om with Om^-1 = -Om
        J = (g @ MCP @ gi) % 3
        k = M.key(J)
        if k not in seen:
            seen.add(k)
            allJ.append(J)
    pairs = {frozenset([frozenset(eig(J, 1)), frozenset(eig(J, 2))]) for J in allJ}
    lines = {frozenset(eig(J, 1)) for J in allJ}
    res["antisymplectic_involutions"] = len(allJ)
    checks["anti-symplectic involutions: 1080 (540 up to sign) = 540 pairs of opposite contexts"] = bool(
        len(allJ) == 1080 and len(pairs) == 540 and len(lines) == 40
        and all(len(eig(J, 1)) == 4 and len(eig(J, 2)) == 4 for J in allJ[:60]))
    inv_ok = True
    for J in list(Js.values()) + allJ[::37]:
        Ji = J  # J^2 = 1
        fixed = eig(J, 1) | eig(J, 2)
        for p in pts:
            conj = (J @ M.tv(p) @ Ji) % 3
            jp = M.norm(J @ np.array(p))
            want = (M.tv(jp) @ M.tv(jp)) % 3
            inv_ok &= np.array_equal(conj, want) and ((jp == p) == (p in fixed))
        inv_ok &= len(fixed) == 8
    checks["each CP fixes exactly 8 events (L+ u L-), inverts their ticks, and maps t_p to t_{Jp}^-1 elsewhere"] = bool(inv_ok)
    res["named_context_pairs"] = {k: [sorted(eig(J, 1)), sorted(eig(J, 2))] for k, J in Js.items()}
    distinct = {frozenset([frozenset(eig(J, 1)), frozenset(eig(J, 2))]) for J in Js.values()}
    res["named_distinct_pairs"] = len(distinct)
    checks["the named flavour CPs give distinct context pairs (CP + 9 theta-group-type + S-type)"] = len(distinct) == 16
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(checks, indent=1), res["all_checks_pass"], res["named_distinct_pairs"])
    return res


if __name__ == "__main__":
    main()
