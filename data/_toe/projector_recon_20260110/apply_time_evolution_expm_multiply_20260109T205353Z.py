"""Apply time evolution psi(t)=exp(-i H t) psi0 using Krylov expm_multiply.

Usage:
  python apply_time_evolution_expm_multiply.py --H_npz <path> --t 1.0 --in_npy <psi0.npy> --out_npy <psi_t.npy>

Notes:
- H is assumed real-symmetric or complex-Hermitian.
- Vector length must match H dimension.
"""

import argparse
import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import expm_multiply

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--H_npz', required=True)
    ap.add_argument('--t', type=float, required=True)
    ap.add_argument('--in_npy', required=True)
    ap.add_argument('--out_npy', required=True)
    args = ap.parse_args()

    H = sp.load_npz(args.H_npz).tocsr()
    psi0 = np.load(args.in_npy)
    if psi0.ndim != 1 or psi0.shape[0] != H.shape[0]:
        raise ValueError(f"psi0 must be shape ({H.shape[0]},), got {psi0.shape}")

    # U(t)=exp(-i H t)
    psi_t = expm_multiply((-1j*args.t)*H, psi0)
    np.save(args.out_npy, psi_t)

if __name__ == '__main__':
    main()
