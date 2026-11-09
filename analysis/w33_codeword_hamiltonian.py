"""Item 2: a canonical theta-invariant Hamiltonian: H_cw = sum of |e><e| over the 90 states of a codeword's left and right pentads (theta
swaps them, Pass 12641).  Spectrum; commutation with parity and theta; Kramers doublets in the parity -1 sector; comparison with the
single-pentad operator H_L (not theta-invariant).
usage: py -3 analysis/w33_codeword_hamiltonian.py"""
import json, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
ek = {"__name__": "x", "__file__": os.path.join(HERE, "w33_explicit_kramers.py")}
import contextlib, io
src = open(os.path.join(HERE, "w33_explicit_kramers.py"), encoding="utf-8").read().split("# (d) factor exchange")[0]
with contextlib.redirect_stdout(io.StringIO()):
    exec(src, ek)
U, maxsets, lines, bases, Par, hk = ek["U"], ek["maxsets"], ek["lines"], ek["bases"], ek["Par"], ek["hk"]
L = sorted(maxsets[0]); R = sorted(maxsets[hk[0]])
def H_of(S_):
    return sum(np.outer(e, e.conj()) for Lx in S_ for e in bases[Lx].T)
HL, HR = H_of(L), H_of(R)
H = HL + HR
theta_inv = bool(np.allclose(U @ H.conj() @ U.conj().T, H, atol=1e-8))
par_comm = bool(np.allclose(Par @ H, H @ Par, atol=1e-8))
ev = np.linalg.eigvalsh(H)
Podd = (np.eye(9) - Par) / 2
w_, V_ = np.linalg.eigh(Podd); sec = V_[:, w_ > 0.5]
ev_odd = np.linalg.eigvalsh(sec.conj().T @ H @ sec) if par_comm else None
res = dict(theta_invariant=theta_inv, commutes_with_parity=par_comm, spectrum=[round(float(x), 6) for x in ev],
           odd_sector_spectrum=[round(float(x), 6) for x in ev_odd] if ev_odd is not None else None,
           HL_spectrum=[round(float(x), 6) for x in np.linalg.eigvalsh(HL)])
print(res)
json.dump(res, open(os.path.join(ROOT, "data", "w33_codeword_hamiltonian.json"), "w"), indent=1)

# two-copy level: M_L + M_R on Sym^2 (theta (x) theta swaps M_L and M_R); spectrum and its Kramers-type structure
d = 9
Sw = np.zeros((81, 81))
for i in range(d):
    for j in range(d): Sw[i * d + j, j * d + i] = 1
Pi = (np.eye(81) + Sw) / 2
def M_of(S_):
    M = np.zeros((81, 81), complex)
    for Lx in S_:
        for e in bases[Lx].T:
            A = np.outer(e, e.conj()) - np.eye(d) / d
            M += np.kron(A, A)
    return M
ML, MR = M_of(L), M_of(R)
UU = np.kron(U, U)
swap_ok = bool(np.allclose(UU @ ML.conj() @ UU.conj().T, MR, atol=1e-8))
w2, V2 = np.linalg.eigh(Pi)
B = V2[:, w2 > 0.5]
Mcw = B.conj().T @ (ML + MR) @ B
from collections import Counter
spec = sorted(Counter(np.round(np.linalg.eigvalsh((Mcw + Mcw.conj().T) / 2) * 9, 5)).items())
comm = bool(np.allclose(B.conj().T @ ML @ B @ B.conj().T @ MR @ B, B.conj().T @ MR @ B @ B.conj().T @ ML @ B, atol=1e-8))
res.update(two_copy_swap=swap_ok, two_copy_spectrum_times9=[(float(a), b) for a, b in spec], ML_MR_commute=comm)
print("theta(x)theta swaps M_L and M_R:", swap_ok, "| spec(M_L + M_R) x 9 on Sym^2:", spec, "| [M_L, M_R] = 0:", comm)
json.dump(res, open(os.path.join(ROOT, "data", "w33_codeword_hamiltonian.json"), "w"), indent=1)
