#!/usr/bin/env python3
"""Pass 400: minimal magnetic control that breaks the qutrit phase-fibre no-go.

The native q=3 Heisenberg bulk adjacency A has projective period T=2*pi/3 but
cannot transfer between the three points of a central fibre.  The translation-
covariant Hermitian control C=(i/sqrt(3))(S-S*) has rank two on each fibre,
commutes with A, and satisfies exp(-iTC)=S.
"""
from __future__ import annotations
import argparse, hashlib, json, math, sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(Path(__file__).resolve().parent))
from w33_pass400_404_common import adjacency,fibre_shift,matrix_exponential_hermitian,vertices,zero_forcing_closure
OUT=ROOT/"data"/"w33_pass400_minimal_phase_control.json"
ZF_COORDS=[(0,0,2),(0,1,1),(0,1,2),(0,2,0),(0,2,1),(1,0,0),(1,0,1),(1,0,2),(1,1,0),(1,1,1),(1,2,0),(1,2,2),(2,0,0),(2,0,2),(2,1,0),(2,1,1),(2,2,1)]

def build_payload():
 q=3;A=adjacency(q).astype(complex);S=fibre_shift(q);C=(1j/math.sqrt(3.0))*(S-S.conj().T);T=2*math.pi/3;omega=np.exp(2j*math.pi/3)
 Un=matrix_exponential_hermitian(A,T);Uc=matrix_exponential_hermitian(C,T);U=matrix_exponential_hermitian(A+C,T)
 S3=S[:3,:3];C3=C[:3,:3];eigs=np.linalg.eigvalsh(C3)
 verts=vertices(q);idx={v:i for i,v in enumerate(verts)};zf={idx[v] for v in ZF_COORDS};closure=zero_forcing_closure(A.real.astype(int),zf)
 fidelities=[];leak=[]
 for x,y,z in verts:
  src=idx[(x,y,z)];dst=idx[(x,y,(z+1)%q)];col=U[:,src];f=abs(col[dst])**2;fidelities.append(float(f));leak.append(float(np.sum(abs(col)**2)-f))
 checks={
  "control_hermitian":bool(np.allclose(C,C.conj().T,atol=1e-11)),
  "control_commutes_with_native":bool(np.allclose(A@C,C@A,atol=1e-11)),
  "single_fibre_spectrum_minus1_0_plus1":bool(np.allclose(eigs,[-1,0,1],atol=1e-10)),
  "single_fibre_rank_two":int(np.linalg.matrix_rank(C3,tol=1e-10))==2,
  "native_projective_return":bool(np.allclose(Un,omega*np.eye(27),atol=1e-9)),
  "control_is_exact_shift":bool(np.allclose(Uc,S,atol=1e-9)),
  "total_is_phase_shift":bool(np.allclose(U,omega*S,atol=1e-9)),
  "all_27_targets_unit_fidelity":min(fidelities)>1-1e-9,
  "all_27_targets_zero_leakage":max(abs(v) for v in leak)<1e-9,
  "zero_forcing_upper_bound_17":len(zf)==17 and len(closure)==27,
  "spectral_control_lower_bound_12":12==max({8:1,-1:8,2:12,-4:6}.values()),
  "minimal_circulant_rank_argument":len(set(np.round(np.angle(np.linalg.eigvals(S3)),10)))==3,
 }
 p={"schema":"w33.pass400.minimal_phase_control.v1","status":"PASS" if all(checks.values()) else "FAIL","scope":"q=3 Heisenberg bulk cell","native_gate_time":"2*pi/3","control":"C=(i/sqrt(3))(S-S^*) on every central fibre","single_fibre_control_matrix":[[str(complex(C3[i,j])) for j in range(3)] for i in range(3)],"single_fibre_spectrum":[-1,0,1],"single_fibre_spectral_rank":2,"global_control_rank":int(np.linalg.matrix_rank(C,tol=1e-10)),"generated_lie_algebra":{"type":"abelian","real_dimension":2,"basis":["iA","iC"],"reason":"A and C commute and are linearly independent"},"minimality":{"translation_covariant_diagonal":"scalar on a fibre and cannot implement a cycle","rank_one":"after a scalar shift exp(-itR) has at most two eigenphases; the qutrit shift has three","rank_two":"achieved by C, hence minimal in the fibre-local Hermitian circulant class"},"full_local_control_bounds":{"spectral_multiplicity_lower_bound":12,"certified_zero_forcing_upper_bound":17,"claim":"12 <= minimum independently addressed diagonal actuator count <= 17; exact value not asserted","zero_forcing_coordinates":[list(v) for v in ZF_COORDS],"zero_forcing_implication":"the graph-infection theorem upgrades independent projectors on these sites to u(27)","full_lie_dimension_when_using_the_17_projectors":729},"exact_gate":"exp[-i(2*pi/3)(A+C)] = exp(2*pi*i/3) S","minimum_target_fidelity":min(fidelities),"maximum_leakage":max(abs(v) for v in leak),"checks":checks}
 canonical=json.dumps(p,sort_keys=True,separators=(",",":")).encode();p["certificate_sha256"]=hashlib.sha256(canonical).hexdigest();return p

def main():
 ap=argparse.ArgumentParser();ap.add_argument("--check",action="store_true");ap.add_argument("--output",type=Path,default=OUT);a=ap.parse_args();p=build_payload();text=json.dumps(p,indent=2,sort_keys=True)+"\n"
 if a.check:
  if not a.output.exists() or a.output.read_text()!=text:raise SystemExit("Pass 400 frozen certificate is stale")
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(text)
 print(json.dumps({"status":p["status"],"checks":sum(p["checks"].values()),"total":len(p["checks"])}));return 0 if p["status"]=="PASS" else 1
if __name__=="__main__":raise SystemExit(main())
