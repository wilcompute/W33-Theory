"""Pass 12683: the F_4 regulus (five MUBs of C^16) as a weighted four-qubit Pauli model, for the symmetric degree-8 SOS pipeline
(w33_f8_symmetric_sos8.py, WHICH = Q4).  Covered Paulis = those diagonal in one of the five bases (identity + the four CZ-model
bases built as in w33_f8_global_sos6.py with field(2)); weight 1 each.  The symmetry group is the full stabiliser of the covered
set in Sp(8,2), found by backtracking over images of the symplectic basis e_0..e_3, f_0..f_3 (points packed p = x | z << 4).
Defines: nq, N, weights {(x, z): 1}, maps [ {(x, z): (x', z')} ].   usage: exec'd by w33_f8_symmetric_sos8.py; standalone prints counts."""
import os
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_g = {"__name__": "x", "__file__": os.path.join(_HERE, "w33_regulus_constants_q16_q32.py")}
_src = open(os.path.join(_HERE, "w33_regulus_constants_q16_q32.py"), encoding="utf-8").read()
exec(_src[: _src.index("def model(")], _g)
_q, _mul, _trace = _g["field"](2)
nq = 4
N = 16
_pc = lambda n: bin(n).count("1") & 1
_Xi = np.array([[1 - 2 * _trace(_mul(a, b)) for b in range(4)] for a in range(4)], float)
_Phi = np.array([[[1 - 2 * _trace(_mul(t, _mul(a, b))) for b in range(4)] for a in range(4)] for t in range(4)], float)
_U = [np.eye(16)]
for t in range(4):
    Ut = np.zeros((16, 16))
    for x in range(16):
        e = np.zeros((4, 4)); e.flat[x] = 1; Ut[:, x] = (_Xi @ (e * _Phi[t]) @ _Xi / 4).ravel()
    assert np.allclose(Ut.T @ Ut, np.eye(16))
    _U.append(Ut)


def _pauli(x, z):
    M = np.zeros((16, 16))
    for y in range(16): M[y, y ^ x] = (-1) ** _pc(z & (y ^ x))
    return M


def _diag_in(M, Ut):
    D = Ut @ M @ Ut.T
    return np.allclose(D, np.diag(np.diag(D)))


weights = {(x, z): 1 for x in range(16) for z in range(16) if (x, z) != (0, 0) and any(_diag_in(_pauli(x, z), Ut) for Ut in _U)}
assert len(weights) == 75, len(weights)
_cov = {x | (z << 4) for (x, z) in weights}


def _om(p, r):
    return _pc((p & 15) & (r >> 4) ^ (p >> 4) & (r & 15))


_basis = [1 << i for i in range(4)] + [1 << (4 + i) for i in range(4)]
_found = []


def _search(img, span_src, span_img, span_set):
    k = len(img)
    if k == 8:
        _found.append(list(img)); return
    b = _basis[k]
    for c in range(1, 256):
        if c in span_set: continue
        if any(_om(c, img[j]) != _om(b, _basis[j]) for j in range(k)): continue
        ok = True
        new_src, new_img = [], []
        for s, t in zip(span_src, span_img):
            s2, t2 = s ^ b, t ^ c
            if (s2 in _cov) != (t2 in _cov): ok = False; break
            new_src.append(s2); new_img.append(t2)
        if ok: _search(img + [c], span_src + new_src, span_img + new_img, span_set | set(new_img))


def _run():
    _search([], [0], [0], {0})


_cache = os.path.join(os.environ.get("TEMP", _HERE), "w33_f4_symmetry_images.json")
if os.path.exists(_cache):
    import json as _json
    _found = _json.load(open(_cache))
else:
    _run()
    import json as _json
    _json.dump(_found, open(_cache, "w"))
assert len(_found) == 14400, len(_found)
# the five bases as Lagrangians (covered points diagonal in basis t)
bases = [frozenset((x, z) for (x, z) in weights if _diag_in(_pauli(x, z), Ut)) for Ut in _U]
assert all(len(B) == 15 for B in bases) and len(set().union(*bases)) == 75
maps = []
for img in _found:
    m = {}
    for p in range(256):
        r = 0
        for i in range(8):
            if p >> i & 1: r ^= img[i]
        m[(p & 15, p >> 4)] = (r & 15, r >> 4)
    maps.append(m)
assert all(all(m[p] in weights for p in weights) for m in maps)
full_order = len(maps)
# SUB = number of bases fixed setwise (0 = full group); a subgroup keeps the SOS pipeline's per-sample group sums affordable
_sub = int(os.environ.get("Q4_SUB", "2"))
maps = [m for m in maps if all(frozenset(m[p] for p in bases[t]) == bases[t] for t in range(_sub))]
if __name__ == "__main__":
    print("covered:", len(weights), "| symmetry group order (mod Paulis):", full_order, "| subgroup fixing", _sub, "bases:", len(maps))
