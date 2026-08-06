#!/usr/bin/env python3
"""Protected frontier reconciler for Passes 4129-4136.

This validates the standalone packet and ordered theorem manifest. It never edits
or replaces docs/index.html.
"""
from __future__ import annotations
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CERT=ROOT/'data/PART_4129_4136_ANOMALY_GATES_DECODER_HYBRID_ORBITS_BONKERS.json'
NS=ROOT/'data/w33_pass_namespace_registry_v2.d/4129-4136.json'
MAN=ROOT/'analysis/W33_CURRENT_FRONTIER_MANIFEST.tex'
INSERT='\\input{analysis/BT4129_BT4136_anomaly_gates_decoder_hybrid_orbits_insert}%'
PREV='\\input{analysis/BT4121_BT4128_explicit_gauge_dfs_decoder_foundry_attractors_insert}%'
NEXT='\\input{analysis/BT4137_BT4144_matrix_horizon_rg_scar_curvature_insert}%'

def chash(d):
 x=dict(d);x.pop('semantic_sha256',None)
 return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def main():
 cert=json.loads(CERT.read_text());ns=json.loads(NS.read_text());man=MAN.read_text()
 assert chash(cert)==cert['semantic_sha256']=='e8a48ff8074816830fedd753bd76f10daa9c16eddc604a6e1654fb32b3b605dd'
 assert ns['status'].startswith('source_complete_exact_certificate_')
 assert ns['certificates']['exact_packet']==cert['semantic_sha256']
 assert man.count(INSERT)==1 and man.index(PREV)<man.index(INSERT)<man.index(NEXT)
 assert (ROOT/'docs/index.html').is_file()
 assert (ROOT/'docs/anomaly-gates-decoder-hybrid-orbits-4129-4136.html').is_file()
 print(json.dumps({'status':'PASS_FRONTIER_RECONCILED','range':[4129,4136],'certificate':cert['semantic_sha256'],'docs_index_untouched_by_design':True},sort_keys=True))
if __name__=='__main__':main()
