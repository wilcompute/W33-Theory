#!/usr/bin/env python3
"""Configurable analytic 10x4 OAM/time-frequency channel model for Pass 2963."""
from __future__ import annotations
import argparse,json,math
import numpy as np
from scipy.linalg import expm

def evaluate(loss_db,detector_eff,oam_coupling,phase_sigma,dark):
    A=np.zeros((10,10))
    for i in range(10): A[i,(i-1)%10]=A[i,(i+1)%10]=1
    C=expm(1j*oam_coupling*A)
    po=float(abs(C[0,0])**2)
    ps=.25+.75*math.exp(-phase_sigma**2)
    pa=po*ps; survival=10**(-loss_db/10)*detector_eff; no_other=(1-dark)**39
    correct=survival*pa*no_other+(1-survival)*dark*no_other
    wrong=survival*(1-pa)*no_other+(1-survival)*39*dark*no_other
    erasure=1-correct-wrong
    return {'oam_correct_probability':po,'slot_correct_probability':ps,'address_correct_given_survival_no_dark':pa,'unconditional_correct_click':correct,'unconditional_wrong_click':wrong,'erasure_or_multiclick':erasure,'conditional_address_fidelity':correct/(correct+wrong),'detected_click_probability':correct+wrong}

def main():
    p=argparse.ArgumentParser();p.add_argument('--loss-db',type=float,default=1);p.add_argument('--detector-eff',type=float,default=.85);p.add_argument('--oam-coupling',type=float,default=.03);p.add_argument('--phase-sigma',type=float,default=.05);p.add_argument('--dark',type=float,default=1e-6);p.add_argument('--output');a=p.parse_args()
    out={'parameters':vars(a)|{'output':None},'result':evaluate(a.loss_db,a.detector_eff,a.oam_coupling,a.phase_sigma,a.dark),'claim_boundary':'Configurable synthetic channel model, not a fabricated-device calibration.'}
    text=json.dumps(out,indent=2,sort_keys=True)+'\n'
    if a.output:open(a.output,'w').write(text)
    print(text,end='')
if __name__=='__main__':main()
