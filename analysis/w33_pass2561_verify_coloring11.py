#!/usr/bin/env python3
from pathlib import Path
import json,hashlib,collections,itertools
ROOT=Path(__file__).resolve().parents[1]
def digest(d):
 x=dict(d);x.pop('sha256_without_hash_field',None);return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def main():
 O=json.loads((ROOT/'data/w33_pass2551_canonical_frame_ordering.json').read_text());F=[set(x) for x in O['frozen_frame_edges']];E=set()
 for e in range(240):
  C=[i for i,f in enumerate(F) if e in f];assert len(C)==9
  E.update(tuple(sorted(x)) for x in itertools.combinations(C,2))
 q=(ROOT/'data/w33_pass2561_coloring11.txt').read_text().split();K=int(q[0]);c=list(map(int,q[1:]));bad=[e for e in E if c[e[0]]==c[e[1]]]
 old=json.loads((ROOT/'data/w33_pass2551_complete_cover_link_k8_refutation.json').read_text())
 out={'schema':'w33.pass2561.chromatic_interval_10_11.v1','status':'PASS_EXACT_ELEVEN_COLORING_WITH_NINE_REFUTED','graph':{'vertices':540,'edges':len(E)},'chromatic':{'proved_lower_bound':old['chromatic_consequence']['proved_lower_bound'],'explicit_upper_bound':K,'color_class_sizes':dict(collections.Counter(c)),'coloring':c},'checks':{'length540':len(c)==540,'colors_0_10':min(c)==0 and max(c)==10,'all_8640_edges_proper':len(E)==8640 and not bad,'lower_bound10':old['chromatic_consequence']['proved_lower_bound']==10},'theorem':'The frozen 540-frame graph has a literal proper eleven-colouring. Together with the complete Pass-2551 refutation of nine-colourability, this gives 10 <= chi(H) <= 11.','boundary':'The exact choice between 10 and 11 remains open; unsuccessful bounded ten-colour searches are not mathematical evidence.'}
 assert all(out['checks'].values());out=json.loads(json.dumps(out,sort_keys=True,separators=(',',':')));out['sha256_without_hash_field']=digest(out);(ROOT/'data/w33_pass2561_chromatic_interval_10_11.json').write_text(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n');print(out['sha256_without_hash_field'])
if __name__=='__main__':main()
