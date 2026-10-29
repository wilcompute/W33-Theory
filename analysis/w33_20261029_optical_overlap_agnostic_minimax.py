#!/usr/bin/env python3
"""Minimax fixed-port three-photon W33/dual discrimination for unknown s.
Scope: three pure photons with uniform REAL pairwise overlap s in [0,1].
"""
import json
from fractions import Fraction
import numpy as np
from scipy.stats import binom

DEN=15**6
S_DMAX=Fraction(83,192)

def probabilities(s):
 return ((17496+52488*s*s+34992*s**3)/DEN,
         (3376+1328*s*s-2048*s**3)/DEN)

def minimum_trials(pW,pD,alpha=.001,N_max=150000):
 assert pW>pD>=0
 N=np.arange(1,N_max+1)
 cutoff=np.asarray(binom.isf(alpha,N,pD),dtype=np.int64)+1
 fp=binom.sf(cutoff-1,N,pD)
 cutoff+=(fp>=alpha)
 fp=binom.sf(cutoff-1,N,pD)
 fn=binom.cdf(cutoff-1,N,pW)
 valid=(fp<alpha)&(fn<alpha)&(cutoff<=N)
 if not valid.any():return dict(status='NO_FEASIBLE_N',N_max=N_max)
 idx=int(np.flatnonzero(valid)[0]);assert not valid[:idx].any()
 return dict(N=int(N[idx]),threshold=int(cutoff[idx]),
             false_positive=float(fp[idx]),false_negative=float(fn[idx]),
             globally_minimal_among_scanned_N=True)

def verify():
 pW0,pD0=probabilities(0)
 _,pDmax=probabilities(float(S_DMAX))
 assert pDmax>pD0 and pDmax>probabilities(1)[1]
 calibrated=minimum_trials(pW0,pD0)
 minimax=minimum_trials(pW0,pDmax)
 loss=minimum_trials(.85**3*pW0,pDmax)
 assert (calibrated['N'],calibrated['threshold'])==(19427,15)
 assert (minimax['N'],minimax['threshold'])==(20333,16)
 assert (loss['N'],loss['threshold'])==(54144,31)
 return dict(status='PASS',same_ports=True,
             common_real_photon_overlap_range=[0,1],
             W33_min_event_probability=pW0,
             dual_max_overlap=str(S_DMAX),
             dual_max_event_probability=pDmax,
             known_s0_optimum=calibrated,
             unknown_overlap_minimax_optimum=minimax,
             unknown_overlap_and_unknown_eta_in_085_to1_beta0=loss,
             each_hypothesis_error_ceiling=0.001,
             minimax_proof="W probability increases with s; dual probability maximized at 83/192; errors are monotone in event probability; every N tested for threshold.",
             boundary="No robustness for unknown complex Gram data, independent pair overlaps, drifts, mode-dependent loss or hypothesis-dependent background.")
if __name__=="__main__":print(json.dumps(verify(),indent=2))
