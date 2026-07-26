#!/usr/bin/env python3
"""BT1901 legacy demonstrator click-rate estimator.

CORRECTION (Pass 1080 / Pass 1086): this script does NOT estimate the
Abramsky-Barbosa contextual fraction. It estimates a dark/loss-corrected signal
click rate for rows labelled ``diagonal_contextual`` and compares that rate with
the historical, currently underived target 1/10.

The mathematical contextual fraction of the W(3,3) KS empirical model is 1,
because the model has no global section. Therefore this click-rate target must
not be used as a contextual-fraction falsifier.
"""
from __future__ import annotations
import json,math,sys
from pathlib import Path
TARGET_CLICK_RATE=0.1
DEFAULT_Z=2.0

def load_rows(path:str)->list[dict]:
    return [json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()]
def is_click(row:dict)->bool:
    return str(row.get('click_pattern','')).strip().lower() not in {'','0','none','no_click','false'}
def estimate(rows:list[dict],z:float=DEFAULT_Z)->dict:
    signal=[r for r in rows if r.get('witness_class')=='diagonal_contextual' and not r.get('dark_reference') and not r.get('loss_probe')]
    dark=[r for r in rows if r.get('dark_reference')];loss=[r for r in rows if r.get('loss_probe')]
    if not signal:raise SystemExit('BT1901 estimator failed: no diagonal_contextual signal rows')
    clicks=sum(is_click(r) for r in signal);dark_rate=sum(map(is_click,dark))/len(dark) if dark else 0.0;loss_rate=1.0-sum(map(is_click,loss))/len(loss) if loss else 0.0
    raw=clicks/len(signal);corrected=max(0.0,min(1.0,(raw-dark_rate)/max(1e-12,1.0-loss_rate)))
    se=math.sqrt(max(TARGET_CLICK_RATE*(1-TARGET_CLICK_RATE),1e-12)/len(signal));lo=TARGET_CLICK_RATE-z*se;hi=TARGET_CLICK_RATE+z*se
    return {'target_signal_click_rate':TARGET_CLICK_RATE,'signal_rows':len(signal),'signal_clicks':clicks,'raw_signal_click_rate':raw,'dark_rows':len(dark),'dark_click_rate':dark_rate,'loss_rows':len(loss),'loss_rate_estimate':loss_rate,'corrected_signal_click_rate':corrected,'z_window':z,'normal_approx_interval':[lo,hi],'compatible_with_historical_one_tenth_click_target':lo<=corrected<=hi,'Abramsky_Barbosa_contextual_fraction_estimate':None,'boundary':'Demonstrator click-rate estimator only. The 1/10 target is underived and is not a contextual fraction or valid substrate falsifier.'}
def main(path:str)->None:print(json.dumps(estimate(load_rows(path)),indent=2,sort_keys=True))
if __name__=='__main__':
    if len(sys.argv)!=2:raise SystemExit('usage: bt1901_contextual_fraction_estimator.py shots.jsonl')
    main(sys.argv[1])
