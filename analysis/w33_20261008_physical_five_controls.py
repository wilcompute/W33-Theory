"""Five frontier controls: modular tetraquadric sieve, optical depth crossover,
proton selection-rule bookkeeping and equivariance firewalls."""
from __future__ import annotations
import json,itertools,math,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
D=R/"data"
OUT=D/"w33_20261008_physical_five_controls.json"

def tetraquadric_affine_sieve():
 q=json.loads((D/"w33_20261008_h27_h13_five_frontiers.json").read_text())["flavor_polynomial_candidate"]
 cs=q["coefficients"]
 mons=[]
 for coefficient,orbit in zip(cs,q["degree_vectors_in_each_orbit"]):
  for v in orbit:mons.append((coefficient,tuple(v)))
 res={}
 for p in (3,5,7):
  solutions=0;singular=0
  witnesses=[]
  charts=0
  vectors=[(1,k) for k in range(p)]+[(0,1)]
  for corners in itertools.product(vectors,repeat=4):
   bits=[0 if a==1 else 1 for a,b in corners]
   x=[(b if a==1 else a) for a,b in corners]
   f=0;grad=[0,0,0,0]
   for c,ds in mons:
    powers=[(ds[i] if bits[i]==0 else 2-ds[i]) for i in range(4)]
    terms=[pow(x[i],powers[i],p) for i in range(4)]
    val=c
    for y in terms:val*=y
    f=(f+val)%p
    for i in range(4):
     if not powers[i]:continue
     dv=c*powers[i]*pow(x[i],powers[i]-1,p)
     for j in range(4):
      if j!=i:dv*=terms[j]
     grad[i]=(grad[i]+dv)%p
   if f==0:
    solutions+=1
    if not any(grad):
     singular+=1
     if len(witnesses)<3:witnesses.append({"coordinates":[list(c) for c in corners]})
  res[str(p)]={"all_projective_ambient_Fp_points":(p+1)**4,
              "hypersurface_Fp_points":solutions,
              "singular_Fp_points":singular,
              "singular_Fp_point_witnesses":witnesses,
              "what_it_proves":"rational Fp point sieve only, not geometric smoothness over Fpbar or C"}
 return {"sieve":res,"smoothness_proved":False}

def optical_crossover():
 d=json.loads((D/"w33_20261008_h27_h13_five_frontiers.json").read_text())["photonic_optimization"]
 data=d["tested_depths"]
 ranks={}
 for eta in (.98,.99,.9902,.995,.999):
  vals=sorted([(x["total_required_successful_detections"]/eta**x["stages"],x["stages"]) for x in data])
  ranks[str(eta)]={"optimal_tested_stages":vals[0][1],
                    "minimum_expected_launches":math.ceil(vals[0][0])}
 pair=next(x for x in data if x["stages"]==36),next(x for x in data if x["stages"]==72)
 a,b=pair
 equal=(b["total_required_successful_detections"]/a["total_required_successful_detections"])**(1/(b["stages"]-a["stages"]))
 assert .98<equal<1
 return {"loss_per_stage_phase_diagram":ranks,
         "36_vs_72_stage_survival_threshold_eta":equal,
         "note":"depth threshold is only for prespecified discrete tested circuits, fixed ideal gap-based detection requirement; not chip-calibrated"}

def proton_selection():
 x=json.loads((D/"w33_20261008_h27_h13_five_frontiers.json").read_text())["proton_hexality"]["X3_charges"]
 q={"Q":0,"Uc":1,"Dc":5,"L":4,"Ec":1,"Nc":3,"Hu":5,"Hd":1}
 operators={"up_Yukawa":["Q","Uc","Hu"],
            "down_Yukawa":["Q","Dc","Hd"],"charged_lepton_Yukawa":["L","Ec","Hd"],
            "neutrino_Yukawa":["L","Nc","Hu"],"mu_term":["Hu","Hd"],
            "QLDc":["Q","L","Dc"],"UcDcDc":["Uc","Dc","Dc"],
            "LLEc":["L","L","Ec"],"QQQL":["Q","Q","Q","L"],
            "UcUcDcEc":["Uc","Uc","Dc","Ec"]}
 charges={k:{"P6":sum(q[v] for v in vs)%6,
             "X3":sum(x[v] for v in vs)%3} for k,vs in operators.items()}
 assert all(charges[k]["P6"]==0 for k in ("up_Yukawa","down_Yukawa","charged_lepton_Yukawa","neutrino_Yukawa","mu_term"))
 assert all(charges[k]["P6"]!=0 for k in ("QLDc","UcDcDc","LLEc","QQQL","UcUcDcEc"))
 return {"operator_charges":charges,
         "warning":"P6 charges are stipulated field assignments; checking charge arithmetic does not derive residual discrete gauge symmetry, full anomalies, instanton or worldsheet selection rules"}

def build():
 return {"tetraquadric":tetraquadric_affine_sieve(),
         "photonic":optical_crossover(),"proton":proton_selection()}

if __name__=="__main__":
 x=build()
 OUT.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n")
 for k,v in x.items():print(k,json.dumps(v),flush=True)
 print("PHYSICAL_FIVE_CONTROLS_PASS")
