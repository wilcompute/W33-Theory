"""Follow-up front 5: resolve Forty Points evidence-label aliases, classify
unresolved items without inventing proofs, and test a device-falsifiable
but not TOE-discriminating W33 commutator echo 240/540 census.
"""
from __future__ import annotations
import json,subprocess,re,math
from pathlib import Path
import numpy as np
from w33_20261019_tick_operator_frame_majorization import points,symp,build_projectors

ROOT=Path(__file__).resolve().parents[1]
H=Path("C:/Repos/Holotrade")
OUT=ROOT/"data"/"w33_20261019_nextfive_evidence_prediction.json"
previous=json.loads((ROOT/"data"/"w33_20261019_allfive_forty_points_audit.json").read_text())
unresolved=previous["unresolved_labels_sample"]
def git(repo,*args):
    if not repo.exists():return (1,"")
    x=subprocess.run(["git","-C",str(repo),*args],capture_output=True,text=True,errors="replace")
    return x.returncode,x.stdout.strip()
def tracked(repo):
    e,x=git(repo,"ls-files")
    return x.splitlines() if e==0 else []
wpaths=tracked(ROOT);hpaths=tracked(H)
def classify(label):
    candidate=label.split("Holotrade",1)[1] if label.startswith("Holotrade") else label
    p=Path(candidate).name
    names=[]
    for repo,files,kind in ((ROOT,wpaths,"w33"),(H,hpaths,"holotrade")):
        exact=[f for f in files if f.replace("\\","/").split("/")[-1]==p]
        if exact:
            names.extend({"repository":kind,"path":f} for f in exact[:6])
    commits=[]
    if re.fullmatch(r"[0-9a-f]{7,40}",candidate):
        for repo,kind in ((ROOT,"w33"),(H,"holotrade")):
            rc,s=git(repo,"rev-parse","--verify",candidate+"^{commit}")
            if rc==0 and re.fullmatch("[0-9a-f]{40}",s):
                commits.append({"repository":kind,"sha":s})
    return {"label":label,"matching_repository_files":names,
            "matching_commit_identifiers":commits,
            "status":"PATH_MATCH" if names else "COMMIT_MATCH" if commits else "MANUAL_OR_EXTERNAL"}
lookup=[classify(q) for q in unresolved]
tally={k:sum(x["status"]==k for x in lookup) for k in ("PATH_MATCH","COMMIT_MATCH","MANUAL_OR_EXTERNAL")}
# Exact ideal normalized echo incidence census over the 40 W33 labels.
P=build_projectors(points())[::3]
I=np.eye(9,dtype=complex)
theta=np.pi/2
def phase(A):return I+(np.exp(1j*theta)-1)*A
U=np.array([phase(p) for p in P])
census={"commuting":0,"noncommuting":0}
maxerr=0.
threshold=4/27
correct=0
pairs=0
for i in range(40):
    for j in range(i+1,40):
        comm=symp(points()[i],points()[j])==0
        W=U[i]@U[j]@U[i].conj().T@U[j].conj().T
        delta=1-np.trace(W).real/9
        expected=0 if comm else 8/27
        maxerr=max(maxerr,abs(delta-expected))
        census["commuting" if comm else "noncommuting"]+=1
        correct+=int((delta>threshold)==(not comm))
        pairs+=1
# Hoeffding, single vs calibrated control under equal visibility.
alpha=.05
delta0=8/27
ideal_n=math.ceil(32*math.log(4/alpha)/delta0**2)
checks={
    "all_23_old_unresolved_labels_rechecked":len(lookup)==23,
    "nontrivial_evidence_resolution":tally["PATH_MATCH"]+tally["COMMIT_MATCH"]>=1,
    "w33_instrument_40_choose_2":pairs==780,
    "commuting_240_and_noncommuting_540":census=={"commuting":240,"noncommuting":540},
    "parameter_free_echo_census_exact":maxerr<1e-12 and correct==780,
}
out={
 "schema":"w33.nextfive.evidence_prediction.v1",
 "evidence_source":"Previously enumerated 23 Forty Points labels not resolved by analysis/data/tests scripts; now search all git-tracked paths in W33 and Holotrade local clones and reachable commit IDs",
 "unresolved_before":len(unresolved),"post_classification":tally,
 "lookup":lookup,
 "interpretation":"A matching basename or commit SHA is a LOCATOR, not a proof witness. Non-matches need manual or external lookup; evidence correctness remains unevaluated.",
 "operational_parameter_free_test":{
   "target":"Two-qutrit Pauli tick-projector echo at a calibrated theta=pi/2, across all 780 pairs of 40 projective Pauli directions",
   "ideal_null_count":240,"ideal_signal_count":540,
   "ideal_deficit_null":"0",
   "ideal_deficit_signal":"8/27",
   "threshold_deficit":"4/27",
   "correctly_classified_ideal_pairs":correct,
   "max_numerical_error":maxerr,
   "ideal_shots_per_condition_95pc_conservative":ideal_n,
   "falsifiability":"On a calibrated gate-level quantum device, noncommuting and commuting pairs must separate with 240:540 incidence and 0 vs 8/27 trace deficit, allowing device noise tolerances. A significant statistically controlled deviation would falsify the gate model/calibration, not the Standard Model or a TOE.",
   "TOE_priority_firewall":"This is a parameter-free prediction of existing two-qutrit quantum mechanics, not a new parameter-free prediction of fundamental physical constants."
 },
 "checks":checks,"all_checks_pass":all(checks.values())
}
OUT.write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"classifications":tally,"lookups":lookup,"echo_counts":census,
  "maxerr":maxerr,"checks":checks},indent=2))
assert out["all_checks_pass"]
