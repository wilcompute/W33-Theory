#!/usr/bin/env python3
"""Exact discrete overlap channel and its *classical* channel capacity for
the 216 equiprobable W33 route states and matching 216-port measurement.

The 216 outputs do not mean 216 distinguishable messages per photon;
Holevo bound for 24D signal is log2(24), independent of optical port count.
"""
from collections import Counter
from math import log2
from pathlib import Path
import sys,json
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261102_five_deeper_fronts import route_frame
def main():
    Z,_=route_frame(); assert Z.shape==(216,40)
    H=Z@Z.T
    assert np.all(np.diag(H)==40)
    K=H.astype(np.int64)**2
    assert np.all(K.sum(axis=0)==14400)
    assert np.all(K.sum(axis=1)==14400)
    hists=[Counter(map(int,row)) for row in K]
    assert all(h==hists[0] for h in hists)
    counts=hists[0]
    nonzero={k:v for k,v in counts.items() if k}
    row_entropy=-sum(v*(k/14400)*log2(k/14400) for k,v in nonzero.items())
    cap=log2(216)-row_entropy
    # weakly-symmetric classical channel = equal row distributions + constant
    # column sums, hence its capacity is log2(outcome count)-row entropy.
    assert -1e-12<=cap<=log2(24)+1e-12
    q=K.astype(float)/14400
    samples=[]
    rng=np.random.default_rng(20261102)
    for nshots in (1,10,100):
        s=int(rng.integers(216))
        obs=rng.choice(216,size=nshots,p=q[s])
        samples.append({'source_route':s,'shots':nshots,
                        'same_route_detected':int(np.count_nonzero(obs==s)),
                        'unique_detector_ports':int(len(set(obs)))})
    out={'status':'PASS_EXACT_WEAKLY_SYMMETRIC_216_ROUTE_CLASSICAL_CHANNEL',
        'signal_dimension':24,'input_route_alphabet':216,'output_detector_ports':216,
        'conditional_probability':'P(t|s)=(Z_s dot Z_t)^2/14400',
        'single_row_numerators_histogram':{str(k):v for k,v in sorted(counts.items())},
        'conditional_shannon_entropy_bits':row_entropy,
        'uniform_output_entropy_bits':log2(216),
        'matched_route_prepare_measure_mutual_information_bits':cap,
        'matched_route_alphabet_classical_channel_capacity_bits_per_detected_photon':cap,
        'Holevo_bound_bits_per_signal_log2_24':log2(24),
        'Holevo_ratio_of_fixed_channel_capacity_to_general_upper_bound':cap/log2(24),
        'simulated_source_samples':samples,
        'scope':'Capacity theorem only for 216 specified frame-state inputs under this ONE fixed 216-outcome POVM (a weakly symmetric classical channel); not the arbitrary-ensemble accessible information/capacity of a 24D quantum channel. No photon loss or collective coding. Fewer than one useful classical bit per detected photon is possible despite >7 bits of raw detector label.'}
    (ROOT/'data/w33_20261102_216_route_holevo_capacity.json').write_text(json.dumps(out,indent=2)+'\n')
    print('HOLEVO_ROUTE',json.dumps({'hist':out['single_row_numerators_histogram'],
         'matched_channel_capacity':cap,'holevo_log24':log2(24),'ratio':cap/log2(24)})[:2500],flush=True)
    return out
if __name__=='__main__':main()
