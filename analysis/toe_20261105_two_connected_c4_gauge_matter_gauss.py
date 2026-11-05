#!/usr/bin/env python3
"""Two interconnected Z2 loop gauge-matter rings: exact 32D physical sector.

Vertices 0..3 and 4..7 each form C4; bridge (3,4) connects.
One mobile Z2 charge plus a fixed background charge at vertex0.
Raw Hilbert C8 * (C2)^9 dimension 4096, Gauss+ dim8*2^(9-8+1)=32.
Explicitly construct the orthonormal Gauss+ basis by gauge orbits,
not by assuming a static flux. H has covariant dressed matter hopping,
two dynamical Wilson loops, nine electric X fields. Verify [H,Gv]=0
and projection H Q=Q Hphys for every term, including off-block bridge.
The NAKED inter-loop hopping violates Gauss: a practical no-go for
joining two E8-root sheets with un-gauged ordinary adjacency.

A chain of 120 C4 loops joined by119 bridge edges has V480,E599
and 120 independent cycle Wilson bits; with one mobile charge and a
neutralizing background, the physical dimension is 480*2^120.
That graph is a deliberately minimal connected 480-site scaffold,
NOT the real complete root E8 adjacency graph.
"""
from __future__ import annotations
import itertools,collections,json,math
from pathlib import Path
import numpy as np
from scipy.sparse import csr_matrix,diags
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261105_two_connected_c4_gauge_matter_gauss.json"
edges=[(0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),(3,4)]
V=8;E=len(edges);N=1<<E;D=V*N
masks=[sum(1<<j for j,(x,y) in enumerate(edges) if v in (x,y)) for v in range(V)]
def build_Q():
 visited=set();rows=[];cols=[];data=[];labels=[]
 for v in range(V):
  unseen=set(range(N))
  while unseen:
   seed=min(unseen)
   orbit={seed:1};queue=[seed]
   while queue:
    x=queue.pop()
    for gv,mask in enumerate(masks):
     y=x^mask
     sign=-1 if (gv==v)^(gv==0) else 1
     phase=orbit[x]*sign
     if y in orbit:assert orbit[y]==phase
     else:orbit[y]=phase;queue.append(y)
   assert len(orbit)==128
   col=len(labels);labels.append((v,seed))
   unseen-=set(orbit)
   for bit,ph in orbit.items():
    rows.append(v*N+bit);cols.append(col);data.append(ph/math.sqrt(128))
 Q=csr_matrix((data,(rows,cols)),shape=(D,len(labels)))
 assert Q.shape==(D,32)
 assert np.max(abs((Q.T@Q).toarray()-np.eye(32)))<1e-12
 return Q,labels
def sparse_op(typ):
 rr=[];cc=[];vv=[]
 if typ=="W0" or typ=="W1":
  offset=0 if typ=="W0" else 4
  return diags([np.array([(-1)**((bit>>offset &15).bit_count()) for v in range(V) for bit in range(N)],float)],[0],format="csr")
 if typ=="hop" or typ=="naked":
  for e,(u,v) in enumerate(edges):
   for bit in range(N):
    sign=(-1)**((bit>>e)&1) if typ=="hop" else 1
    rr.extend((v*N+bit,u*N+bit));cc.extend((u*N+bit,v*N+bit));vv.extend((sign,sign))
 if typ=="electric":
  for v in range(V):
   for bit in range(N):
    for e in range(E):
     rr.append(v*N+(bit^(1<<e)));cc.append(v*N+bit);vv.append(1)
 return csr_matrix((vv,(rr,cc)),shape=(D,D),dtype=float)
def main():
 Q,labels=build_Q()
 T=sparse_op("hop");B=[sparse_op("W0"),sparse_op("W1")]
 Xsum=sparse_op("electric")
 naked=sparse_op("naked")
 reduced=[(Q.T@O@Q).toarray() for O in [T,*B,Xsum,naked]]
 t,b0,b1,x,n=reduced
 for O,R in zip([T,*B,Xsum],reduced[:4]):
  residue=(O@Q).toarray()-np.asarray(Q@R)
  assert np.max(abs(residue))<1e-11
 assert np.max(abs((naked@Q).toarray()-np.asarray(Q@n)))>1e-4
 assert np.max(abs(b0@b1-b1@b0))<1e-12
 assert np.max(abs(b0@t-t@b0))<1e-12
 assert np.max(abs(b1@t-t@b1))<1e-12
 assert np.max(abs(x@b0-b0@x))>1
 assert np.max(abs(x@b1-b1@x))>1
 assert np.max(abs(t-t.T))<1e-12
 sectors={}
 for f0,f1 in itertools.product((1,-1),repeat=2):
  # Gauge flux signs are diagonal commuting B0,B1 at g0.
  projector=(np.eye(32)+f0*b0)@(np.eye(32)+f1*b1)/4
  spec,vv=np.linalg.eigh(projector)
  Z=vv[:,spec>.5]
  assert Z.shape==(32,8)
  eig=np.linalg.eigvalsh(Z.T@(-t)@Z)
  sectors[f"{f0},{f1}"]=dict(W0=f0,W1=f1,
    kinetic_eigenvalues_J1=eig.tolist(),ground_kinetic_energy=float(eig.min()))
 assert sectors["1,1"]["ground_kinetic_energy"]<min(v["ground_kinetic_energy"] for k,v in sectors.items() if k!="1,1")
 rows=[]
 for K in (-.4,0,.2):
  for g in (0,.03,.15,.4):
   H=-t-K*(b0+b1)-g*x
   e,v=np.linalg.eigh(H)
   psi=v[:,0]
   f=[float(psi@B@psi) for B in (b0,b1)]
   rows.append(dict(K_per_loop=K,g_electric=g,energy=float(e[0]),
    gap=float(e[1]-e[0]),W0=f[0],W1=f[1]))
 # Validate global graph topological count, no 2^120 simulation.
 nloops=120;vertices=4*nloops;ed=4*nloops+(nloops-1)
 assert ed-vertices+1==nloops
 result=dict(status="PASS_TWO_COUPLED_C4_FULL_GAUSS_INVARIANT_32D_MATTER_AND_GAUGE",
  vertex_count=V,edge_count=E,independent_cycles=E-V+1,
  one_particle_background_neutral_gauss_subspace_dimension=Q.shape[1],
  raw_hilbert_dimension=D,Gauss_orbit_size=128,
  all_dressed_hopping_and_flux_and_electric_terms_preserve_physical_sector=True,
  bare_hopping_across_link_breaks_local_Gauss_law=True,
  two_flux_sector_hopping_spectra=sectors,
  scan=rows,
  connected_120_loop_scaffold_sites=vertices,connected_120_loop_scaffold_edges=ed,
  connected_120_loop_scaffold_cycle_rank=nloops,
  one_charge_physical_hilbert_dimension_for_120_loops_decimal=str(vertices*(1<<nloops)),
  full_E8_root_graph_and_interlayer_links_not_implemented=True,
  priority="Ordinary Z2 lattice gauge matter and AB flux energetics are prior art; exact 32D two-ring control is a validated adjacent-loop extension of the earlier 8D single-ring E8 local toy.",
  scope="No derived full 480-mode E8 many-body action or spontaneous flux selection in a vacuum. Connected scaffold requires gauging every bridge; naked E8 adjacency cannot be appended without Gauss dressing.")
 OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
 print(result["status"],"ground",[(k,round(v["ground_kinetic_energy"],5)) for k,v in sectors.items()],flush=True)
 return result
if __name__=="__main__":main()
