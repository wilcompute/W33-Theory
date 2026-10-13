"""TOE53 pinned 27-frame torsor ↔ W33 H27 group-label dictionary.

A fully explicit group-equivariant *address map*. Generator choice is
deterministic, not a physically canonical line-to-frame identification.
"""
import json,runpy
from pathlib import Path
R=Path(__file__).resolve().parents[1]
h=json.loads((R/"data/w33_20261013_toe53_holotrade_frame27_snapshot.json").read_text())
v=runpy.run_path(str(R/"analysis/w33_20261013_toe52_h27_bridge.py"))
P=[tuple(x) for x in h["frame_elation_permutations_lex_order"]]
pix={z:i for i,z in enumerate(P)}
e=tuple(range(27));Ie=pix[e]
def mulh(i,j):return pix[tuple(P[i][P[j][k]] for k in range(27))]
w=v["mult"];wid=v["identity"]
# Concrete W33 basis with a=(1,0,0), b=(0,1,0)
a=9;b=3
assert all(int(x)==x for x in w.ravel())
def closure(i,j):
 s={Ie};front=[Ie]
 for k in front:
  for q in (i,j):
   z=mulh(k,q)
   if z not in s:s.add(z);front.append(z)
 return len(s)
pair=next((i,j) for i in range(27) for j in range(27)
 if mulh(i,j)!=mulh(j,i) and closure(i,j)==27)
# Map w->h respecting these ordered generators.
m={wid:Ie};front=[wid]
for z in front:
 for p,q in [(a,pair[0]),(b,pair[1])]:
  k=int(w[z,p]);image=mulh(m[z],q)
  if k not in m:m[k]=image;front.append(k)
  else:assert m[k]==image
assert len(m)==27 and len(set(m.values()))==27
assert all(m[int(w[i,j])]==mulh(m[i],m[j]) for i in range(27) for j in range(27))
address=[P[m[i]][0] for i in range(27)]
assert len(set(address))==27
maxerr=0
for g in range(27):
 for j in range(27):
  assert P[m[g]][address[j]]==address[int(w[g,j])]
# Holotrade Qpsi assignment. All H27 elations act regularly
# so a nontrivial frame charge cannot commute with full H27.
q=h["frame_overlap_Qpsi_charges"]; good=[]
for k in range(12):
 if all((k*q[addr])%12==(k*q[P[m[g]][addr]])%12
   for g in range(27) for addr in range(27)):good.append(k)
assert good==[0,4,8]
out={"status":"PASS_PINNED_H27_GROUP_GENERATOR_AND_27_FRAME_ADDRESS_MATCH",
 "source":h["source_repo"],"source_commit":h["source_commit"],
 "source_script_blob_sha256":h["source_script_blob_sha256"],
 "W33_a_M_1_0_0_index":a,"W33_b_M_0_1_0_index":b,
 "chosen_Holotrade_generator_indices_lex_action":list(pair),
 "W33_group_index_to_Holotrade_lex_group_index":[m[i] for i in range(27)],
 "W33_group_index_to_Holotrade_frame_address":address,
 "group_multiplication_cases_checked":729,
 "frame_left_equivariance_cases_checked":729,
 "Qpsi_mu12_powers_commuting_with_frame_H27":good,
 "frame_Qpsi_counts":{str(t):q.count(t) for t in sorted(set(q))},
 "boundary":"These are exact concrete 27-frame permutation and H27 group-label correspondences under selected generator images, replayed from pinned Holotrade source snapshot. There is NO natural map from all 40 W33 lines to 27 distinct frames; 40 and 27 are different G-sets, and group identification is non-unique up to automorphisms. The chosen pair is lexicographic rather than supplied by an actual microscopic Hamiltonian."}
(R/"data/w33_20261013_toe53_crossrepo_h27_frame_address.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"status":out["status"],"pair":pair,"good":good,"checks":729}))
