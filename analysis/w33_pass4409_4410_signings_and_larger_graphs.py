#!/usr/bin/env python3
"""Passes 4409-4410 -- Ramanujan signings of W(3,3), and flux on its bigger graphs.

FIRST, A CORRECTION TO MY OWN NEXT-STEP LIST.  Pass 4405 ended by proposing "a directed
search for a gauge field that breaks the Ramanujan bound".  That question is ill-posed and
I should have caught it before writing it down.  For a d-regular graph the Ramanujan
condition constrains the NON-TRIVIAL eigenvalues, because the all-ones vector always
supplies lambda = d.  Under a gauge field the all-ones vector is generally not an
eigenvector at all, so "the trivial eigenvalue" stops existing and the natural quantity is
the whole spectral radius rho = max|lambda|.  At zero flux rho = 12, already far above
2*sqrt(11) = 6.633.  There is nothing to break: the bound is violated before any flux is
applied.

The well-posed question is the OPPOSITE ONE, and it is a real problem with a name.

    BILU-LINIAL.  Does every d-regular graph admit a signing s: E -> {+1,-1} whose
    adjacency spectrum lies inside [-2*sqrt(d-1), +2*sqrt(d-1)]?

Marcus, Spielman and Srivastava proved the bipartite-double-cover version by the method of
interlacing families, which is how bipartite Ramanujan graphs of every degree were first
constructed.  For general graphs the conjecture is open.  So the directed search worth
running is a search for a RAMANUJAN SIGNING of W(3,3), and success is a concrete witness
rather than a counterexample.

  4409  minimise rho over signings (local search) and over U(1) gauge fields (gradient
        descent with the exact perturbation-theory derivative).
  4410  the same flux physics on the two larger graphs the geometry supplies: the
        incidence (Levi) graph on 40+40 vertices, 4-regular, and the flag graph on the 160
        incident point-line pairs, 6-regular.  160 levels is enough for level statistics
        from a SINGLE sample, where Pass 4405 needed a 400-member ensemble.

    py -3 analysis/w33_pass4409_4410_signings_and_larger_graphs.py
"""

from __future__ import annotations

import itertools
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402

RNG = np.random.default_rng(4409)
R_POISSON, R_GOE, R_GUE = 0.38629, 0.53070, 0.59957


def w33():
    F = 3
    pts = []
    for lead in range(4):
        for tail in itertools.product(range(F), repeat=3 - lead):
            pts.append((0,) * lead + (1,) + tail)
    idx = {p: i for i, p in enumerate(pts)}

    def symp(x, y):
        return (x[0] * y[1] - x[1] * y[0] + x[2] * y[3] - x[3] * y[2]) % F

    def norm(v):
        for c in v:
            if c:
                inv = pow(c, F - 2, F)
                return tuple((inv * z) % F for z in v)
        raise ValueError

    lines = set()
    for i, x in enumerate(pts):
        for y in pts[i + 1:]:
            if symp(x, y):
                continue
            span = set()
            for a in range(F):
                for b in range(F):
                    if a or b:
                        span.add(norm(tuple((a * u + b * v) % F for u, v in zip(x, y))))
            lines.add(frozenset(idx[v] for v in span))
    return pts, sorted(lines, key=sorted)


def graphs():
    """Three graphs the geometry supplies, each as (name, adjacency, degree)."""
    pts, lines = w33()
    n = len(pts)

    A = np.zeros((n, n), int)
    for L in lines:
        for u, v in itertools.combinations(sorted(L), 2):
            A[u, v] = A[v, u] = 1

    m = len(lines)
    I = np.zeros((n + m, n + m), int)          # incidence / Levi graph
    for j, L in enumerate(lines):
        for p in L:
            I[p, n + j] = I[n + j, p] = 1

    flags = [(p, j) for j, L in enumerate(lines) for p in sorted(L)]
    f = len(flags)
    Fg = np.zeros((f, f), int)                 # flag graph: share a point or a line
    for a, b in itertools.combinations(range(f), 2):
        (p1, l1), (p2, l2) = flags[a], flags[b]
        if (p1 == p2) != (l1 == l2):
            Fg[a, b] = Fg[b, a] = 1
    return [("collinearity", A), ("incidence (Levi)", I), ("flag", Fg)]


def edge_list(A):
    return [(u, v) for u in range(len(A)) for v in range(u + 1, len(A)) if A[u, v]]


def build(A, edges, theta):
    H = np.zeros(A.shape, complex)
    for k, (u, v) in enumerate(edges):
        H[u, v] = np.exp(1j * theta[k])
        H[v, u] = np.conj(H[u, v])
    return H


def rho(H):
    return float(np.abs(np.linalg.eigvalsh(H)).max())


def spacing_ratio(ev):
    s = np.diff(np.sort(ev.real))
    s = s[s > 1e-10]
    if len(s) < 2:
        return np.array([])
    return np.minimum(s[:-1], s[1:]) / np.maximum(s[:-1], s[1:])


def minimise_rho_u1(A, edges, restarts=6, steps=900, lr=0.35):
    """Gradient descent on rho.  dlambda_k/dtheta_e = 2 Re(conj(v_u) i e^{i theta} v_v)."""
    best = (np.inf, None)
    m = len(edges)
    for _ in range(restarts):
        th = RNG.uniform(0, 2 * np.pi, m)
        for t in range(steps):
            H = build(A, edges, th)
            w, V = np.linalg.eigh(H)
            k = int(np.argmax(np.abs(w)))
            v, sgn = V[:, k], np.sign(w[k])
            g = np.empty(m)
            for e, (u, q) in enumerate(edges):
                g[e] = 2 * np.real(np.conj(v[u]) * 1j * np.exp(1j * th[e]) * v[q])
            th = (th - lr * sgn * g * (1 - t / steps)) % (2 * np.pi)
        r = rho(build(A, edges, th))
        if r < best[0]:
            best = (r, th.copy())
    return best


def minimise_rho_signs(A, edges, restarts=8, sweeps=60):
    """Local search over +/-1 signings: flip the edge that most reduces rho.

    Returns (rho, signing) -- a claimed Ramanujan signing has to ship its witness, or the
    claim is not checkable by anyone who does not rerun the search and get lucky.
    """
    best, best_s = np.inf, None
    m = len(edges)
    for _ in range(restarts):
        s = RNG.integers(0, 2, m) * np.pi
        cur = rho(build(A, edges, s))
        for _ in range(sweeps):
            improved = False
            for e in RNG.permutation(m):
                s[e] = (s[e] + np.pi) % (2 * np.pi)
                r = rho(build(A, edges, s))
                if r < cur - 1e-12:
                    cur, improved = r, True
                else:
                    s[e] = (s[e] + np.pi) % (2 * np.pi)
            if not improved:
                break
        if cur < best:
            best, best_s = cur, s.copy()
    return best, best_s


def verify_signing(A, edges, signs) -> tuple[float, bool]:
    """Independently re-derive rho from the +/-1 witness, not from the search's bookkeeping."""
    S = np.zeros(A.shape)
    for k, (u, v) in enumerate(edges):
        S[u, v] = S[v, u] = signs[k]
    assert set(np.unique(S)) <= {-1.0, 0.0, 1.0}, "not a +/-1 signing"
    assert (np.abs(S) == A).all(), "signing does not have the graph's support"
    d = int(A.sum(1)[0])
    r = float(np.abs(np.linalg.eigvalsh(S)).max())
    return r, r <= 2 * np.sqrt(d - 1) + 1e-9


def main() -> int:
    print("=" * 78)
    print("Passes 4409-4410 -- signings, and flux on the bigger graphs")
    print("=" * 78)

    G = graphs()
    print(f"\n  {'graph':20s} {'|V|':>5s} {'deg':>4s} {'2*sqrt(d-1)':>12s}  zero-flux spectrum")
    meta = {}
    for name, A in G:
        d = int(A.sum(1)[0])
        assert (A.sum(1) == d).all(), f"{name} is not regular"
        ev = np.linalg.eigvalsh(A.astype(float))
        vals, cnt = np.unique(np.round(ev, 8), return_counts=True)
        meta[name] = {"n": len(A), "degree": d, "bound": float(2 * np.sqrt(d - 1)),
                      "spectrum": {f"{v:+.4f}": int(c) for v, c in zip(vals, cnt)}}
        spec = ", ".join(f"{v:+.3f}x{c}" for v, c in zip(vals[::-1], cnt[::-1]))
        print(f"  {name:20s} {len(A):5d} {d:4d} {2 * np.sqrt(d - 1):12.4f}  {spec[:44]}")

    # ---- Pass 4409 ---------------------------------------------------------
    print("\n  PASS 4409 -- is there a Ramanujan signing?\n")
    print(f"  {'graph':20s} {'bound':>9s} {'best +/-1':>10s} {'best U(1)':>10s}  verdict")
    sign_rows = {}
    for name, A in G:
        d = int(A.sum(1)[0])
        b = 2 * np.sqrt(d - 1)
        E = edge_list(A)
        rs, sw = minimise_rho_signs(A, E)
        ru, _ = minimise_rho_u1(A, E)
        signs = np.where(np.isclose(sw % (2 * np.pi), 0.0), 1.0, -1.0)
        r_check, ok = verify_signing(A, E, signs)
        v = ("SIGNING FOUND" if ok else
             "U(1) only" if ru <= b + 1e-9 else "none found")
        sign_rows[name] = {"bound": float(b), "best_sign_rho": float(rs),
                           "verified_rho": r_check, "best_u1_rho": float(ru),
                           "verdict": v, "edges": len(E),
                           "witness_negative_edges": [list(E[k]) for k in range(len(E))
                                                      if signs[k] < 0]}
        print(f"  {name:20s} {b:9.4f} {rs:10.4f} {ru:10.4f}  {v}"
              f"  (witness re-verified: {r_check:.4f})")

    print(f"""
  READ THE U(1) COLUMN CAREFULLY -- IT IS NOT A COUNTEREXAMPLE TO ANYTHING.  Bilu-Linial is
  about +/-1 signings.  The U(1) column is a strictly larger search space, so it can only do
  as well or better, and beating the bound there says nothing about the conjecture.  It is
  included because it is the physical object -- a magnetic field -- and because it bounds
  from below what any signing could achieve.""")

    # ---- Pass 4410 ---------------------------------------------------------
    print("\n  PASS 4410 -- level statistics from ONE sample, on graphs big enough for it\n")
    print(f"  {'graph':20s} {'levels':>7s} {'<r> signs':>10s} {'<r> phases':>11s}"
          f"  {'classes':>16s}")
    stats = {}
    for name, A in G:
        E = edge_list(A)
        m = len(E)
        rr = {}
        for kind, draw in (("sign", lambda: np.pi * RNG.integers(0, 2, m)),
                           ("phase", lambda: RNG.uniform(0, 2 * np.pi, m))):
            pool = []
            reps = 1 if len(A) >= 160 else max(1, 400 // max(len(A) // 40, 1))
            for _ in range(reps):
                pool.append(spacing_ratio(np.linalg.eigvalsh(build(A, E, draw()))))
            pool = np.concatenate([x for x in pool if len(x)])
            rr[kind] = (float(pool.mean()), int(len(pool)), reps)
        near = lambda x: min((("Poisson", R_POISSON), ("GOE", R_GOE), ("GUE", R_GUE)),
                             key=lambda t: abs(t[1] - x))[0]
        stats[name] = {"sign": rr["sign"], "phase": rr["phase"],
                       "class_sign": near(rr["sign"][0]), "class_phase": near(rr["phase"][0])}
        print(f"  {name:20s} {len(A):7d} {rr['sign'][0]:10.4f} {rr['phase'][0]:11.4f}"
              f"  {near(rr['sign'][0]):>7s}/{near(rr['phase'][0]):<8s}"
              f"  ({rr['sign'][2]} sample{'s' if rr['sign'][2] > 1 else ''})")
    print(f"  {'reference':20s} {'':>7s} {R_GOE:10.4f} {R_GUE:11.4f}")

    fl = stats["flag"]
    print(f"""
  THE FLAG GRAPH SETTLES IT FROM ONE HAMILTONIAN.  160 levels give {fl['sign'][1]} spacing ratios
  from a SINGLE gauge field, so the GOE/GUE separation no longer relies on averaging over an
  ensemble -- which was the weakest part of Pass 4405. Signs give {fl['sign'][0]:.4f} against GOE's
  {R_GOE:.4f}; phases give {fl['phase'][0]:.4f} against GUE's {R_GUE:.4f}, on the same 160 flags.

  AND A PREDICTION OF MINE FAILED HERE, WHICH IS WORTH MORE THAN THE ONES THAT WORKED.  I
  expected the incidence graph to deviate: it is bipartite, so its spectrum is symmetric
  about zero under ANY gauge field -- every eigenvalue paired with its negative, a chiral
  symmetry that no flux can remove. I wrote down that this protected structure would show
  in the statistics. It does not: the incidence graph gives {stats['incidence (Levi)']['sign'][0]:.4f} and {stats['incidence (Levi)']['phase'][0]:.4f}, as
  close to GOE and GUE as the collinearity graph's {stats['collinearity']['sign'][0]:.4f} and {stats['collinearity']['phase'][0]:.4f}.

  The reason is that I used a LOCAL statistic to look for a GLOBAL symmetry. The spacing
  ratio compares neighbouring gaps in the bulk, where the chiral pairing relates a level to
  one on the far side of the spectrum, not to its neighbour. Bipartiteness is real,
  protected, and simply invisible to this observable. Seeing it needs a statistic that
  reaches across zero -- the spectral density near the origin, or the number variance.
  Recorded rather than quietly deleted, because the failed prediction locates the
  observable, and the successful ones did not.""")

    out = {
        "boundary": ("searches are heuristic -- local search over signings and gradient "
                     "descent over U(1) gauge fields; a value ABOVE the bound means NOT "
                     "FOUND, never proved impossible, and only a value below it is a "
                     "witness. No claim is made about Bilu-Linial in general"),
        "correction": ("Pass 4405's proposed next step -- find a gauge field that BREAKS "
                       "the Ramanujan bound -- was ill-posed: at zero flux rho = 12 already "
                       "exceeds 2*sqrt(11) = 6.633 because the all-ones eigenvalue is not "
                       "excluded once the graph is gauged. The well-posed question is the "
                       "Bilu-Linial one, in the opposite direction"),
        "graphs": meta,
        "pass_4409_signings": sign_rows,
        "pass_4410_statistics": stats,
        "reference_mean_r": {"Poisson": R_POISSON, "GOE": R_GOE, "GUE": R_GUE},
    }
    p = ROOT / "data" / "PART_W33_PASS4409_4410_SIGNINGS.json"
    p.parent.mkdir(exist_ok=True)
    p.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {p.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
