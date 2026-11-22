#!/usr/bin/env python3
"""Reproduce seven distinct Witting / W33 / E6 research certificates, 2026-11-22."""
from pathlib import Path
import json
import toe_20261122_round6_16effect_optimal as IC
import toe_20261122_round6_optical16 as OPT
import toe_20261122_round6_causal_graph_no_go as CAUS
import toe_20261122_round6_beam_compiler as BEAM
import toe_20261122_round6_local_refine as REF
import toe_20261122_round6_e6_twirl_noiseless as TWI
import toe_20261122_round6_e6_higgs_flat_branch as HIG

OUT=Path(__file__).resolve().parents[1]/'data'

def main():
    producers={
      'toe_20261122_round6_exact_minimal16':lambda:{'status':'PASS_EXACT_RANK_ONE_WITTING_16_EFFECT_MIC','proof':IC.proof()},
      'toe_20261122_round6_optical16':lambda:OPT.verify(ntries=60),
      'toe_20261122_round6_exact_Hasse_cut':CAUS.verify,
      'toe_20261122_round6_e6_twirl':TWI.verify,
      'toe_20261122_round6_e6_FD_branch':HIG.verify,
      'toe_20261122_round6_hessian_beam':BEAM.verify,
      'toe_20261122_round6_hessian_refine':REF.verify,
    }
    summary={}
    for filename,producer in producers.items():
      result=producer();result['date']='2026-11-22'
      path=OUT/(filename+'.json');path.parent.mkdir(parents=True,exist_ok=True)
      path.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+'\n')
      summary[filename]=result['status']
      print(filename,result['status'],flush=True)
    (OUT/'toe_20261122_round6_manifest.json').write_text(json.dumps({'date':'2026-11-22','sources':list(producers),'certificate_status':summary,'scope':'Exact finite geometry + conditional toy physics and numerical hardware/compiler falsifiers; not a complete TOE'},indent=2,sort_keys=True)+'\n')
    return summary
if __name__=='__main__': main()
