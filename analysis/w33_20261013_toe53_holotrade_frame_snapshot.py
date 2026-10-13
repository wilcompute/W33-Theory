"""TOE53 optional source-bound cross-repo H27 27-frame action replay.

Requires local Holotrade git OBJECTS for pinned b026 commit plus its exact
tracked source helper. The resulting snapshot can be independently replayed
inside W33 without live Holotrade paths.
"""
import json,subprocess,hashlib,runpy
from pathlib import Path
R=Path(__file__).resolve().parents[1]
H=Path("C:/Repos/Holotrade")
sha="b0264880d7c5fd24c6af932b892324247ab57808"
path="analysis/w33_frame_bundle_three_k81_slices.py"
helper="analysis/the_27_factorisation_frames_carry_the_so10_weights.py"
def get(ref):
 return subprocess.check_output(["git","-C",str(H),"show",f"{sha}:{ref}"])
raw=get(path);helper_bytes=get(helper)
assert subprocess.check_output(["git","-C",str(H),"hash-object",str(H/helper)]).decode().strip()==subprocess.check_output(["git","-C",str(H),"rev-parse",f"{sha}:{helper}"]).decode().strip(),"Local helper Git-cleaned blob differs from pinned tracked Git blob; refuse to run."
scope={"__file__":str(H/path),"__name__":"holo53_extract"}
exec(compile(raw.decode(),str(H/path),"exec"),scope)
frames,perms,qpsi=scope["frame_elation_action"]()
assert len(frames)==len(perms)==27
P=sorted(tuple(map(int,p)) for p in perms)
n={p:i for i,p in enumerate(P)}
I=tuple(range(27));identity=n[I]
mult=[[n[tuple(a[b[i]] for i in range(27))] for b in P] for a in P]
assert all(mult[i][identity]==i for i in range(27))
# 27 frames form an exact free transitive action under H27.
assert len({p[0] for p in P})==27
orders=[]
for g in range(27):
 t=g;k=1
 while t!=identity:
  t=mult[t][g];k+=1
 assert k<=3
 orders.append(k)
assert orders.count(3)==26
payload={
"status":"PINNED_HOLOTRADE_27_FRAME_H27_ACTION",
"source_repo":"wilcompute/Holotrade","source_commit":sha,
"source_script_blob_sha256":hashlib.sha256(raw).hexdigest(),
"source_helper_blob_sha256":hashlib.sha256(helper_bytes).hexdigest(),
"frame_elation_permutations_lex_order":P,
"frame_base_reference":0,
"frame_overlap_Qpsi_charges":qpsi,
"n_regular_frames":27,
"all_group_elements_order3_except_identity":True,
"original_group_action_index":"The lexicographically sorted tuple indices of 27 permutation actions, not 4x4 symplectic matrix generators. A separate H27 automorphism remains a labeling choice.",
"no_physical_claim":"This data only identifies the abstract regular 27-frame action and Qpsi charges. Canonical geometric correspondence between W33 40 lines and 27 frames is not implied."
}
O=R/"data/w33_20261013_toe53_holotrade_frame27_snapshot.json"
O.write_text(json.dumps(payload,indent=2)+"\n")
print("FRAME_SNAPSHOT",json.dumps({"status":payload["status"],"Qpsi_counts":{str(k):qpsi.count(k) for k in set(qpsi)},"blob":payload["source_script_blob_sha256"]}))
