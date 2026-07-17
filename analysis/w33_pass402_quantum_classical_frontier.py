#!/usr/bin/env python3
"""Pass 402: exact expansion/transfer frontier for fibre augmentation."""
from __future__ import annotations
import argparse,hashlib,json,math,sys
from collections import Counter
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(Path(__file__).resolve().parent))
from w33_pass400_404_common import adjacency,fibre_complete,fibre_shift,matrix_exponential_hermitian
OUT=ROOT/"data"/"w33_pass402_quantum_classical_frontier.json"
def spectrum_formula(q,alpha):
 d=Counter();d[q*q-1+alpha*(q-1)]+=1;d[-1+alpha*(q-1)]+=q*q-1;d[q-1-alpha]+=q*(q*q-1)//2;d[-q-1-alpha]+=q*(q-1)*(q-1)//2;return dict(d)
def numerical_spectrum(H):
 vals=np.linalg.eigvalsh(H.astype(float));r=np.rint(vals).astype(int)
 if not np.allclose(vals,r,atol=1e-8):raise AssertionError("weighted spectrum is not integral")
 return dict(sorted(Counter(int(v) for v in r).items()))
def build_payload():
 cases=[];checks={}
 for q,alphas in ((3,range(0,7)),(5,range(0,5)),(7,range(0,4))):
  A=adjacency(q);F=fibre_complete(q);checks[f"q{q}_native_commutes_with_fibre_complete"]=bool(np.array_equal(A@F,F@A));num,den=q+2,q-2
  for alpha in alphas:
   H=A+alpha*F;obs=numerical_spectrum(H);exp=dict(sorted(spectrum_formula(q,alpha).items()));degree=(q-1)*(q+1+alpha);radius=max(abs(l) for l in exp if l!=degree);front=alpha*den<=num;exact=radius*(q-1)==degree;checks[f"q{q}_a{alpha}_spectrum"]=obs==exp;checks[f"q{q}_a{alpha}_frontier_law"]=exact==front;cases.append({"q":q,"alpha":alpha,"degree":degree,"spectrum":{str(k):v for k,v in exp.items()},"nontrivial_radius":radius,"normalized_radius":{"numerator":radius,"denominator":degree},"preserves_native_contraction_exactly":exact,"frontier_condition":f"alpha <= ({q}+2)/({q}-2) = {num}/{den}"})
 q=3;A=adjacency(q).astype(complex);F=fibre_complete(q).astype(complex);S=fibre_shift(q);C=(1j/math.sqrt(3.0))*(S-S.conj().T);T=2*math.pi/3;gates=[]
 for alpha in range(0,6):
  U=matrix_exponential_hermitian(A+alpha*F+C,T);phase=np.exp(2j*math.pi*(1+alpha)/3);fid=float(np.min(np.max(abs(U)**2,axis=0)));err=float(np.max(abs(U-phase*S)));checks[f"q3_a{alpha}_exact_controlled_shift"]=err<1e-8;gates.append({"alpha":alpha,"gate_time":"2*pi/3","exact_unitary":f"omega^{1+alpha} S","maximum_matrix_error":err,"minimum_column_target_fidelity":fid})
 theta=.371;verts=[(x,y,z) for x in range(3) for y in range(3) for z in range(3)];G=np.diag([np.exp(1j*theta*z) for x,y,z in verts]);Aphase=G.conj().T@A@G;checks["voltage_only_magnetic_phase_is_pure_gauge"]=bool(np.allclose(np.linalg.eigvalsh(Aphase),np.linalg.eigvalsh(A),atol=1e-9))
 p={"schema":"w33.pass402.quantum_classical_frontier.v1","status":"PASS" if all(checks.values()) else "FAIL","real_fibre_augmentation":"H_alpha=A+alpha F, where F is q^2 disjoint copies of K_q","spectrum_formula":{"degree":"q^2-1+alpha(q-1)","base_sector":"-1+alpha(q-1), multiplicity q^2-1","positive_character_sector":"q-1-alpha, multiplicity q(q^2-1)/2","negative_character_sector":"-q-1-alpha, multiplicity q(q-1)^2/2"},"exact_contraction_frontier":"0 <= alpha <= (q+2)/(q-2) implies normalized nontrivial radius exactly 1/(q-1)","beyond_frontier":"the base-sector eigenvalue alpha(q-1)-1 dominates and classical contraction worsens","qutrit_no_tradeoff_gate":{"Hamiltonian":"A+alpha F+(i/sqrt(3))(S-S^*)","allowed_integer_alpha":[0,1,2,3,4,5],"result":"at T=2*pi/3, U=omega^(1+alpha)S with unit fidelity and no leakage","interpretation":"the real routing layer retains the native 1/2 contraction while the magnetic layer supplies exact phase transfer"},"gauge_obstruction":"phases depending only on z'-z are G^*AG and are physically gauge-equivalent to native propagation","cases":cases,"qutrit_gate_checks":gates,"checks":checks};canonical=json.dumps(p,sort_keys=True,separators=(",",":")).encode();p["certificate_sha256"]=hashlib.sha256(canonical).hexdigest();return p
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--check",action="store_true");ap.add_argument("--output",type=Path,default=OUT);a=ap.parse_args();p=build_payload();text=json.dumps(p,indent=2,sort_keys=True)+"\n"
 if a.check:
  if not a.output.exists() or a.output.read_text()!=text:raise SystemExit("Pass 402 frozen certificate is stale")
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(text)
 print(json.dumps({"status":p["status"],"checks":sum(p["checks"].values()),"total":len(p["checks"])}));return 0 if p["status"]=="PASS" else 1
if __name__=="__main__":raise SystemExit(main())
