#!/usr/bin/env python3
"""One Z2-charged coherent matter excitation on four-node/edge gauge C4.

Hilbert C4(matter position) tensor C2^4(link qubits), dim64.
Background static charge at v0 permits total parity even. Gauss
G_v=(-1)^(n_v+delta_v0) X_(v-1) X_v; only three independent.
Gauge-invariant H=-J sum (|v+1><v| + h.c.) tensor Z_v
                  -K I tensor B -g I tensor sum(X_e),
B=product_e Z_e.
Gauss+ subspace rank8. For g=K=0, unlike pure gauge theory,
matter kinetic energy dynamically prefers W=+1 over W=-1
because 4-site periodic ground -2J is below pi-flux -sqrt2 J.
The exact g0 flux transition at K=-(2-sqrt2)J/2 is an
elementary Aharonov-Bohm tight-binding competition, NOT new
fundamental physics or a full 480-site E8 Hamiltonian.
"""
from __future__ import annotations
import json,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261104_matter_dynamical_z2_flux_competition.json"
I2=np.eye(2); X=np.array([[0,1],[1,0.]])
Z=np.diag([1.,-1.])
def kron4(ops):
 y=np.array([[1.]])
 for a in ops:y=np.kron(y,a)
 return y
XX=[kron4([X if i==e else I2 for i in range(4)]) for e in range(4)]
ZZ=[kron4([Z if i==e else I2 for i in range(4)]) for e in range(4)]
B=kron4([Z]*4)
Im=np.eye(4);I16=np.eye(16);I64=np.eye(64)
Nm=[np.diag([1 if j==v else -1 for j in range(4)]) for v in range(4)]
def matter_hop(edge):
 m=np.zeros((4,4));u=edge;v=(edge+1)%4;m[u,v]=m[v,u]=1
 return m
HOP=sum(np.kron(matter_hop(v),ZZ[v]) for v in range(4))
G=[np.kron((-1 if v==0 else 1)*Nm[v],XX[(v-1)%4]@XX[v]) for v in range(4)]
P=I64.copy()
for a in G:P=P@(I64+a)/2
def reduced(H,Q):return Q.T@H@Q
def main():
 assert np.max(abs(P@P-P))<1e-12
 assert np.linalg.matrix_rank(P,tol=1e-10)==8
 assert np.max(abs(G[0]@G[1]@G[2]@G[3]-I64))<1e-12
 for a in G:
  assert np.max(abs(P@a-P))<1e-12
  assert np.max(abs(HOP@a-a@HOP))<1e-12
  assert np.max(abs(np.kron(Im,B)@a-a@np.kron(Im,B)))<1e-12
  for x in XX:assert np.max(abs(np.kron(Im,x)@a-a@np.kron(Im,x)))<1e-12
 vals,Q=np.linalg.eigh(P)
 Q=Q[:,vals>.5]
 assert Q.shape==(64,8)
 assert np.max(abs(Q.T@Q-np.eye(8)))<1e-12
 flux=reduced(np.kron(Im,B),Q)
 T=reduced(HOP,Q)
 Elec=reduced(np.kron(Im,sum(XX)),Q)
 assert np.max(abs(T@flux-flux@T))<1e-12
 assert np.max(abs(Elec@flux-flux@Elec))>1e-5
 assert np.max(abs(flux@flux-np.eye(8)))<1e-12
 eflu,W=np.linalg.eigh(flux)
 assert sum(eflu>0)==4 and sum(eflu<0)==4
 E0=[];Epi=[]
 for sign,where,record in [(1,eflu>.5,E0),(-1,eflu<-.5,Epi)]:
  V=W[:,where];He=-T
  spec=np.linalg.eigvalsh(V.T@He@V)
  assert len(spec)==4
  record.extend(float(x) for x in spec)
 assert np.max(abs(np.array(E0)-[-2,0,0,2]))<1e-10
 assert np.max(abs(np.array(Epi)-[-math.sqrt(2),-math.sqrt(2),math.sqrt(2),math.sqrt(2)]))<1e-10
 threshold=-(2-math.sqrt(2))/2
 rows=[]
 for K in (-.5,threshold-.01,threshold,threshold+.01,0,.2):
  for g in (0,.02,.1,.3):
   H=-T-K*flux-g*Elec
   assert np.max(abs(H-H.T))<1e-12
   eig,vec=np.linalg.eigh(H)
   psi=vec[:,0]
   fl=float(psi@flux@psi)
   rows.append(dict(matter_hopping_J=1.,plaquette_K=K,electric_g=g,
    ground_energy=float(eig[0]),first_gap=float(eig[1]-eig[0]),
    Wilson_expectation=fl,local_Gauss_constraints_exact=True))
   if g==0 and K>threshold+1e-5: assert abs(fl-1)<1e-10
   if g==0 and K<threshold-1e-5: assert abs(fl+1)<1e-10
 # Initial exact flux0 localized dressed matter has coherent physical
 # state in each site*link superposition; 4D fermionic matter alone
 # cannot be specified independently of gauge dressing.
 Q0=np.zeros((64,64))
 for i in range(16):Q0[i,i]=1
 Ps=Q0@P@Q0
 assert np.linalg.matrix_rank(Ps,tol=1e-10)==2
 result=dict(status="PASS_GAUSS_COVARIANT_MATTER_HOPPING_INDUCES_ZERO_FLUX_SELECTION",
  Hilbert_dimension_raw=64,Gauss_invariant_dimension=8,
  static_background_charge_at_vertex=0,
  dynamic_matter_excitation_count=1,
  full_Gauss_product_identity=True,
  matter_covariant_hop_commutes_all_Gauss=True,
  electric_link_X_commutes_all_Gauss=True,
  Wilson_plaquette_commutes_all_Gauss=True,
  Wilson_commutes_hopping_at_g0=True,
  electric_term_does_not_commute_Wilson=True,
  zero_flux_matter_hop_spectrum_J1=E0,
  pi_flux_matter_hop_spectrum_J1=Epi,
  zero_flux_vs_pi_ground_kinetic_advantage_J1=2-math.sqrt(2),
  threshold_K_where_pi_flux_wins_when_g0_J1=threshold,
  sweep=rows,
  physical_sector_site0_localized_dimension=2,
  relevance="The E8-interlayer 120 four-cycles can each support this gauge-covariant matter-plaquette local model. At g0 and J1, MATTER hopping prefers zero flux unless externally negative K overcomes finite-size kinetic offset.",
  scope="Toy one C4 with a chosen static neutralizing background charge and one mobile Z2 charge, NOT derivation of the sign of K, an E8 root graph many-body Hamiltonian, spontaneous symmetry breaking, cosmological vacuum or TOE.",
  prior_art="AB ring flux dependence and Kogut-Susskind Z2 Gauss law are classical; here the specific 120-root plaquette geometry from the Reye/icosian sheets motivates the coupled local falsifier.")
 OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf8")
 print(result["status"],"threshold",threshold,"physical dimension",Q.shape[1],flush=True)
 return result
if __name__=="__main__": main()
