"""Small CV entanglement distribution and repeater demo
Usage: python scripts/quantum_photonics/run_cv_repeater.py --r 0.8 --loss 0.9

Simulate two-mode squeezed states, lossy channels, and entanglement swapping using Strawberry Fields Gaussian backend.
"""
import argparse
import numpy as np

try:
    import strawberryfields as sf
    from strawberryfields.ops import Sgate, BSgate, MeasureX
    from strawberryfields.backends.gaussianbackend import GaussianBackend
except Exception as e:
    print('Missing dependencies:', e)
    raise

from math import log


def tmsv_variance(r):
    # quadrature variance for TMSV
    v = 0.5 * np.cosh(2 * r)
    return v


def simulate_tmsv_loss(r=0.8, loss=0.8):
    # simple analytical model: TMSV entanglement degraded by transmissivity
    V = tmsv_variance(r)
    # after loss tau on one mode, covariance entries scale accordingly; compute log-negativity approx
    tau = loss
    # symplectic eigenvalue approximation for partially transposed CM (toy model)
    nu = 0.5 * np.sqrt((2*V*tau + 1 - tau) * (2*V + 1))
    return -np.log2(2 * nu) if 2*nu < 1 else 0.0


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--r', type=float, default=0.8)
    p.add_argument('--loss', type=float, default=0.9)
    args = p.parse_args()

    Ln = simulate_tmsv_loss(r=args.r, loss=args.loss)
    print(f'Estimated log-negativity (toy model) r={args.r} loss={args.loss}:', Ln)

if __name__ == '__main__':
    main()
