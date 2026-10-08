"""Exact MILP minimum X logical operator for 20-octagon binary CSS.

The rank constraints are integral equalities imposing parity. Gaps and
termination statuses are recorded; 'proven' only for HiGHS status=0.
"""
import sys,json,numpy as np
from pathlib import Path
from scipy.optimize import milp,LinearConstraint,Bounds
from scipy.sparse import csc_matrix
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261008_twenty_apartment_binary_CSS_F20 import topology,add,nullspace
OUT=ROOT/"data/w33_20261008_twenty_apartment_X_cosystole.json"
def main():
 V,E,F,stab,H,b1,b2=topology()
 B={};Z={}
 for x in b1:add(x,B)
 for x in b2:add(x,Z)
 logz=[]
 for v in nullspace(b1,60):
  if add(v,Z):logz.append(v)
 assert len(logz)==2
 rows=[]
 for z in logz:
  nz=[int(z>>j&1) for j in range(60)]
  matrix=np.zeros((21,81),dtype=float)
  for i,f in enumerate(b2):
   for j in range(60):
    if (f>>j)&1:matrix[i,j]=1
   matrix[i,60+i]=-2
  matrix[20,:60]=nz;matrix[20,80]=-2
  con=LinearConstraint(csc_matrix(matrix),np.r_[np.zeros(20),1],np.r_[np.zeros(20),1])
  lb=np.zeros(81);ub=np.r_[np.ones(60),np.full(20,4),np.array([20])]
  o=milp(np.r_[np.ones(60),np.zeros(21)],integrality=np.ones(81,dtype=int),bounds=Bounds(lb,ub),constraints=con,
    options={"time_limit":40,"mip_rel_gap":0.0})
  witness=[]
  if o.x is not None:
   witness=[i for i in range(60) if o.x[i]>.5]
   if o.status==0:
    assert sum((z>>i)&1 for i in witness)%2==1
    assert all(sum((f>>i)&1 for i in witness)%2==0 for f in b2)
  rows.append({"logical_Z_index":len(rows),"MILP_status":int(o.status),"MILP_message":str(o.message),
    "minimum_X_operator_weight_if_proven":len(witness) if o.status==0 else None,
    "upper_bound_witness_weight":len(witness) if witness else None,
    "X_operator_support_edge_indices":witness,
    "MIP_gap":float(o.mip_gap) if getattr(o,"mip_gap",None) is not None else None,
    "dual_bound":float(o.mip_dual_bound) if getattr(o,"mip_dual_bound",None) is not None else None})
 return {"logical_operators":rows,"exact_X_minimum_proven":all(r["MILP_status"]==0 for r in rows),
  "minimal_X_weight":min(r["minimum_X_operator_weight_if_proven"] for r in rows) if all(r["MILP_status"]==0 for r in rows) else None}
if __name__=="__main__":
 x=main();OUT.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n");print(json.dumps(x,indent=2),flush=True);print("CSS_X_MILP_END")
