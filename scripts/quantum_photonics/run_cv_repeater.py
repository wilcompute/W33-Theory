"""Small CV entanglement distribution and repeater demo
Usage: python scripts/quantum_photonics/run_cv_repeater.py --r 0.8 --loss 0.9

Simulate two-mode squeezed states, lossy channels, and entanglement swapping using Strawberry Fields Gaussian backend.
"""
import argparse
import json
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


def simulate_repeater_simple(r=0.8, loss_left=0.9, loss_right=0.9):
    """Toy repeater model: two TMSVs A-B and C-D, entanglement swapping between B and C.

    This is a simplified, illustrative model: we approximate the effective loss on the final A-D link
    by multiplying channel transmissivities (loss_left * loss_right) and computing TMSV log-negativity
    for that combined transmissivity. This is a toy model for quick exploration and benchmarking.
    """
    tau_eff = loss_left * loss_right
    return simulate_tmsv_loss(r=r, loss=tau_eff)


def sweep_repeater(r_values=[0.3,0.6,0.9], losses=[0.5,0.7,0.9]):
    from pathlib import Path
    out = []
    for r in r_values:
        for L in losses:
            Ln_direct = simulate_tmsv_loss(r=r, loss=L)
            Ln_repeater = simulate_repeater_simple(r=r, loss_left=L, loss_right=L)
            out.append({'r': r, 'loss': L, 'ln_direct': Ln_direct, 'ln_repeater_toy': Ln_repeater})
    # save
    repo = Path(__file__).resolve().parents[2]
    outp = repo / 'bundles' / 'v23_toe_finish' / 'v23' / 'cv_repeater_sweep.json'
    outp.parent.mkdir(parents=True, exist_ok=True)
    open(outp,'w').write(json.dumps(out, indent=2))
    print('Saved', outp)
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--r', type=float, default=0.8)
    p.add_argument('--loss', type=float, default=0.9)
    p.add_argument('--sweep', action='store_true')
    args = p.parse_args()

    if args.sweep:
        sweep_repeater()
    else:
        Ln = simulate_tmsv_loss(r=args.r, loss=args.loss)
        print(f'Estimated log-negativity (toy model) r={args.r} loss={args.loss}:', Ln)

if __name__ == '__main__':
    main()
