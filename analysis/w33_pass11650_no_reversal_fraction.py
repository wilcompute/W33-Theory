"""Pass 11650: classes of one magic gate with NO reversal at all -- linear algebra decides, and the fraction.

(S) of Pass 11350 asks for a symplectic Q with M s^-k Q (J M J) = Q, Q z1 = z1.  Without the symplectic condition this is
an affine system: an intertwiner Q from (V, JMJ) to (V, s^k M^-1) fixing z1.
FOUND HERE.
  * Exhaustively at n = 2 (every class) and n = 3 (every orbit of Pass 11373 within the cap): (S) has a symplectic
    solution for some k  iff  the affine system is solvable for some k.  So "no reversal" is decided by Gaussian
    elimination; no enumeration of symplectic solutions is needed.
  * Exact fractions of Sp(2n, 3) with no reversal (every frame violates):
        n = 2: 1296/51840 = 1/40 (all in the cell 'same line, other', half of it);
        n = 3: 1/28 = 3/182 (non-collinear) + 1/52 ('same line, other').
  * Sampled (affine test, uniform M): n = 4: 0.0373 +- 0.0008, n = 5: 0.0376 +- 0.0011 -- the fraction settles near
    0.037 rather than growing.  No closed formula is claimed.
"""
import json, sys
from collections import Counter
from fractions import Fraction
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11350_linear_decider as L  # noqa: E402
import w33_pass11352_three_qutrit_geometry as GEO  # noqa: E402
import w33_pass11498_magic_axis_law_all_n as T  # noqa: E402
OUT = ROOT / "data" / "w33_pass11650_no_reversal_fraction.json"


def exhaustive(n):
    if n == 2:
        import w33_pass11330_orbit_census as O
        D = L.Decider(2)
        items = [(M, 1) for M in np.array(O.all_symplectic(D.wl)[0]) % 3]
        cap = 3 ** 8
        total = 51840
    else:
        import w33_pass11373_three_qutrit_exact_fraction as X
        D = L.Decider(3)
        items = [(np.asarray(M) % 3, int(s)) for M, s in X.read_orbits(3)]
        cap = 3 ** 9
        total = sum(int(s) for _, s in items)          # = |Sp(6,3)| = 9170703360
    st, mass = Counter(), Counter()
    for M, w in items:
        aff = any(D.symplectic_solutions(M, k) is not None for k in range(3))
        sols = [T.solutions(D, M, k, cap) for k in range(3)]
        if any(s is None for s in sols):
            mass["beyond cap"] += w
            st["affine solvable (beyond cap)"] += aff
            continue
        sym = any(len(s) for s in sols)
        st[f"affine {aff} / symplectic {sym}"] += 1
        if not sym:
            cell = GEO.cell(M, D.z1, D.wl.Om)
            mass[f"no reversal: {cell}"] += w
            mass["no reversal"] += w
    return dict(counts=dict(st), fractions={k: str(Fraction(v, total)) for k, v in mass.items()},
                affine_decides=all(("True / False" not in k and "False / True" not in k) or v == 0 for k, v in st.items()))


def _job(args):
    n, N, seed = args
    D = __import__("w33_pass11421_four_qutrits").SparseDecider(n)
    rng = np.random.default_rng(seed)
    gens = GEO.gen_mats(n)
    st = Counter()
    for _ in range(N):
        M = GEO.random_symplectic(rng, gens) % 3
        st[all(D.symplectic_solutions(M, k) is None for k in range(3))] += 1
    return st


def sample(n, N, nproc=6):
    from multiprocessing import Pool
    tot = Counter()
    with Pool(nproc) as p:
        for s in p.imap_unordered(_job, [(n, N // 30, 11650 + 100 * n + i) for i in range(30)]):
            tot.update(s)
    b, a = tot[True], tot[True] + tot[False]
    f = b / a
    return dict(samples=a, no_reversal=b, fraction=f, stderr=(f * (1 - f) / a) ** 0.5)


def main():
    stage = sys.argv[1]
    res = json.load(open(OUT)) if OUT.exists() else dict(pass_id=11650)
    if stage in ("n2", "n3"):
        out = exhaustive(int(stage[1]))
    else:
        out = sample(int(stage[1]), int(sys.argv[2]))
    print(stage, out, flush=True)
    res = json.load(open(OUT)) if OUT.exists() else dict(pass_id=11650)
    res[stage] = out
    json.dump(res, open(OUT, "w"), indent=1, default=str)


if __name__ == "__main__":
    main()
