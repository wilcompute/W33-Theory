"""Check whether actual 600-cell antipodal adjacency is a Cayley graph
for the 60 Clifford A5-torsor group law. Tests all group left/right
multiplications, and right/left neighbor labels. Avoids assuming
that abstract group identification preserves actual H4 geometry.
"""
from pathlib import Path
import sys,json,collections,numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"analysis"));sys.path.insert(0,str(ROOT))
from PART_MCCCCXVII_MCCCCXXXII_clifford_fibration_selector_verifier import build_600cell,build_adjacency
from w33_clifford_antipodal_spread_incidence_bridge import antipodal_pair_index
from w33_clifford_antipodal_a5_selector_group import clifford_antipodal_permutations,compose
OUT=ROOT/"data/w33_20261008_H4_Clifford_A5_Cayley_test.json"
def main():
 vv=build_600cell();aa=build_adjacency(np.array(vv),len(vv));idx=antipodal_pair_index()
 grp=clifford_antipodal_permutations()
 keys={g:k for k,g in grp.items()}
 assert len(keys)==60
 E={tuple(sorted((idx[u],idx[v]))) for u in range(120) for v in range(u+1,120) if aa[u][v]}
 assert len(E)==360
 hist={}
 samples={}
 for side in ("left","right"):
  passers=[];preserved={}
  for label,element in grp.items():
   if side=="left":
    action={i:keys[compose(element,g)] for i,g in grp.items()}
   else:
    action={i:keys[compose(g,element)] for i,g in grp.items()}
   mapped={tuple(sorted((action[u],action[v]))) for u,v in E}
   count=len(mapped&E)
   preserved[label]=count
   if count==len(E):passers.append(label)
  hist[side]=dict(collections.Counter(preserved.values()))
  samples[side]={"full_automorphisms":passers,"full_count":len(passers),
   "min_preserved_edges":min(preserved.values()),"max_preserved_edges":max(preserved.values())}
 idlabel=keys[tuple(range(6))]
 N=sorted(j if i==idlabel else i for i,j in E if i==idlabel or j==idlabel)
 assert len(N)==12
 return {"actual_600cell_antipodal_60_graph_edges":len(E),
  "Clifford_A5_actual_group_elements":60,
  "left_translations_edges_preserved_hist":hist["left"],
  "right_translations_edges_preserved_hist":hist["right"],
  "full_translation_subgroups":samples,
  "identity_12_neighbor_labels":N,
  "is_left_A5_Cayley":samples["left"]["full_count"]==60,
  "is_right_A5_Cayley":samples["right"]["full_count"]==60,
  "claim_boundary":"All translations checked against actual H4 coordinates. A5-as-permutations does not by itself grant geometric translation invariance."}
if __name__=="__main__":
 x=main();OUT.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n")
 print({k:v for k,v in x.items() if k!="identity_12_neighbor_labels"},flush=True)
 print("H4_A5_CAYLEY_FULL_TRANSLATION_AUDIT_PASS")
