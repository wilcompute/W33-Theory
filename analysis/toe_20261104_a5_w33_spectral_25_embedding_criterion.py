#!/usr/bin/env python3
"""A5 character decomposition of W33 adjacency eigenspaces vs Reye25 module.

Previous round found an A5-equivariant isometry 25->40, but its image
leaked under W33 adjacency. Test if there is ANY A5-equivariant
isometry onto the NATURAL W33 25-dimensional 12+2 spectral space
or any other 25D adjacency-invariant W33 submodule.
Class char computed from REAL PSp4(3) action, not guessed dimensions.
"""
from __future__ import annotations
import collections,json,sys,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT/"analysis") not in sys.path:sys.path.insert(0,str(ROOT/"analysis"))
import w33_pass999_a5_double_class_census as prior
OUT=ROOT/"data/toe_20261104_a5_w33_spectral_25_embedding_criterion.json"
SRC={"1":2,"3":1,"3prime":1,"4":3,"5":1}
DIMS={"1":1,"3":3,"3prime":3,"4":4,"5":5}
def irrep_counts(chars):
 z2,z3,z5=chars[2],chars[3],chars[5];n=chars[1]
 vals={"1":(n+15*z2+20*z3+24*z5)/60,
       "3":(3*n-15*z2+12*z5)/60,
       "3prime":(3*n-15*z2+12*z5)/60,
       "4":(4*n+20*z3-24*z5)/60,
       "5":(5*n+15*z2-20*z3)/60}
 assert all(abs(round(v)-v)<1e-10 for v in vals.values()),vals
 return {k:round(v) for k,v in vals.items()}
def main():
 c=prior.core_objects()
 A=np.zeros((40,40),dtype=np.int64)
 for i,j in c["edges"]:A[i,j]=A[j,i]=1
 J=np.ones((40,40),dtype=np.float64)
 I=np.eye(40)
 projections={"12":J/40,
   "2":(40*I+10*A-4*J)/60,
   "-4":(32*I-16*A+4*J)/96}
 for name,P in projections.items():
  assert np.max(abs(P@P-P))<1e-11
  lam=int(name)
  assert np.max(abs(A@P-lam*P))<1e-11
 assert abs(sum(np.trace(P) for P in projections.values())-40)<1e-11
 assert [round(np.trace(projections[k])) for k in ("12","2","-4")]==[1,24,15]
 results=[]
 for idx,H in enumerate(c["A5_classes"]):
  chars={}
  for name,P in projections.items():
   X=collections.defaultdict(set)
   for g in H:
    order=prior.order_of(g)
    trace=float(sum(P[i,g[i]] for i in range(40)))
    assert abs(trace-round(trace))<1e-9
    X[order].add(round(trace))
   assert all(len(v)==1 for v in X.values()),X
   assert set(X)=={1,2,3,5}
   chars[name]={k:next(iter(v)) for k,v in X.items()}
  chars["12plus2"]={k:chars["12"][k]+chars["2"][k] for k in (1,2,3,5)}
  chars["target"]={k:sum(chars[j][k] for j in ("12","2","-4")) for k in (1,2,3,5)}
  counts={name:irrep_counts(v) for name,v in chars.items()}
  assert counts["target"]=={"1":2,"3":2,"3prime":2,"4":4,"5":2}
  assert sum(v*DIMS[k] for k,v in counts["12plus2"].items())==25
  match_source=counts["12plus2"]==SRC
  source_rank_capacity=sum(DIMS[k]*min(SRC[k],counts["12plus2"][k]) for k in SRC)
  assert source_rank_capacity<=25
  # Construct a selected isometry by projecting the previously
  # certified F25->40 and polar-normalizing its positive Gram,
  # if the projection is FULL RANK. Test the actual condition,
  # rather than inferring surjectivity from character matching.
  old=json.loads((ROOT/"data/toe_20261104_actual_a5_w33_25_to40_intertwiner.json").read_text())
  F=np.array(old["both_W33_class_certificates"][idx]["intertwiner_matrix_40x25"])
  P=projections["12"]+projections["2"]
  M=P@F
  gram=M.T@M
  w,U=np.linalg.eigh(gram)
  projected_rank=int(sum(w>1e-10))
  polar_isometry=False
  polar_residual=None
  if projected_rank==25:
   E=U@np.diag(1/np.sqrt(w))@U.T
   W=M@E
   polar_isometry=bool(np.max(abs(W.T@W-np.eye(25)))<1e-10)
   assert polar_isometry
   assert np.max(abs(P@W-W))<1e-10
   assert np.max(abs(A@W-W@(W.T@A@W)))<1e-10
   polar_residual=float(np.linalg.norm(A@W-W@(W.T@A@W)))
  # The simple earlier F need not have full-rank projection onto
  # an isomorphic spectral module. Build the ENTIRE Hom_A5 space
  # statistically by averaging a generic real linear operator over
  # all 60 actual W33 A5 automorphisms. This gives a full-rank map
  # iff all source irreps can be carried in the spectral 25-sector.
  rng=np.random.default_rng(20261104+idx)
  R=rng.normal(size=(40,25))
  H=c["A5_classes"][idx]
  avg=np.zeros((40,25))
  all_transforms=[]
  for g in H:
   Ug=np.eye(40)[:,list(g)].T # row-g perm is U_g^T; use explicit
   Ug=np.zeros((40,40))
   Ug[np.array(g),np.arange(40)]=1
   S=F.T@Ug@F
   assert np.max(abs(S@S.T-np.eye(25)))<1e-11
   assert np.max(abs(Ug@F-F@S))<1e-11
   avg+=Ug@R@S.T
   all_transforms.append((Ug,S))
  M2=P@avg/60
  wg,Ug2=np.linalg.eigh(M2.T@M2)
  averaged_rank=int(sum(wg>1e-10))
  averaged_polar=False
  explicit_spectral_intertwiner=None
  if averaged_rank==25:
   W2=M2@Ug2@np.diag(1/np.sqrt(wg))@Ug2.T
   assert np.max(abs(W2.T@W2-np.eye(25)))<1e-9
   assert np.max(abs(P@W2-W2))<1e-9
   assert np.max(abs(A@W2-W2@(W2.T@A@W2)))<1e-9
   assert all(np.max(abs(Ug@W2-W2@S))<1e-9 for Ug,S in all_transforms)
   averaged_polar=True
   assert sorted(round(float(x)) for x in np.linalg.eigvalsh(W2.T@A@W2))==[2]*24+[12]
   # Two A5-trivial vectors exist on source and target. Polar
   # normalization leaves an arbitrary rotation of this 2D
   # multiplicity. Fix it so uniform packet mode becomes W33's
   # unique Perron eigenvector, without breaking A5 equivariance.
   u=np.ones(25)/5
   tt=np.ones(40)/np.sqrt(40)
   v=W2.T@tt
   assert abs(np.linalg.norm(v)-1)<1e-9
   if np.linalg.norm(u-v)>1e-10:
    e=u-v
    R=np.eye(25)-2*np.outer(e,e)/(e@e)
    assert np.max(abs(R@R-np.eye(25)))<1e-9
    W2=W2@R
   assert np.max(abs(W2@u-tt))<1e-9
   assert all(np.max(abs(Ug@W2-W2@S))<1e-9 for Ug,S in all_transforms)
   explicit_spectral_intertwiner=W2.tolist()
   # Eight source row/column zero-sum potentials belong to the
   # 25-packet ->60-axis incidence kernel from preceding certificate.
   labels=[(i,j) for i in range(5) for j in range(5)]
   B=np.zeros((25,8))
   for j,(r,col) in enumerate(labels):
    for k in range(4):
     B[j,k]=(r==k+1)-(r==0)
     B[j,k+4]=(col==k+1)-(col==0)
   assert np.linalg.matrix_rank(B)==8
   assert np.max(abs(A@W2@B-2*W2@B))<1e-9
   uniform=np.ones(25)/5
   assert np.max(abs(A@W2@uniform-12*W2@uniform))<1e-9
   S=np.zeros((25,25))
   ix={x:i for i,x in enumerate(labels)}
   for j,(r,col) in enumerate(labels):S[ix[col,r],j]=1
   Q=W2@S@W2.T+np.eye(40)-W2@W2.T
   assert np.max(abs(Q@Q-np.eye(40)))<1e-9
   assert np.max(abs(Q@A-A@Q))<1e-9
   assert np.max(abs(Q@W2-W2@S))<1e-9
   assert sum(abs(x+1)<1e-8 for x in np.linalg.eigvalsh(Q))==10
   assert not np.allclose(Q,np.round(Q),atol=1e-8)
   spectral_swap_certificate=dict(
     packet_axis_A4plusA4_kernel_rank=8,
     kernel_maps_to_W33_eigenvalue2=True,
     uniform_maps_to_W33_eigenvalue12=True,
     source_factor_swap_becomes_dense_orthogonal_involution=True,
     full_40label_operator_commutes_with_W33_adjacency=True,
     eigenvalues={"+1":30,"-1":10},
     graph_label_permutation=False,
     dense_real_40x40_swap_operator=Q.tolist())
  else:spectral_swap_certificate=None
  if match_source:
   assert averaged_rank==25 and averaged_polar
  else:
   assert averaged_rank<=source_rank_capacity
  results.append(dict(A5_class_index=idx,
   group_averaged_25to40_spectral_rank=averaged_rank,
   group_averaged_min_G_eigenvalue=float(wg[0]),
   group_averaged_polar_isometric_spectral_intertwiner=averaged_polar,
   explicit_group_averaged_40x25_spectral_intertwiner=explicit_spectral_intertwiner,
   row_column_E8_kernel_spectral_swap_certificate=spectral_swap_certificate,
   spectral_projection_of_explicit_25to40_F_rank=projected_rank,
   spectrum_of_FtPF=[float(x) for x in w],
   polar_25to40_spectral_isometry_exists_for_this_explicit_F=polar_isometry,
   polar_W33_adjacency_leakage_frobenius=polar_residual,
   characters_by_element_order={name:{str(k):v for k,v in x.items()} for name,x in chars.items()},
   irreducible_decompositions=counts,
   packet25_module_multiplicities=SRC,
   W33_12plus2_submodule_isomorphic_to_packet25=match_source,
   max_25_to_W33_12plus2_intertwiner_rank=source_rank_capacity,
   minimum_dimension_of_packet_source_NOT_fit_in_W33_12plus2=25-source_rank_capacity))
 result=dict(status="PASS_A5_W33_SPECTRAL_SUBMODULE_CHARACTER_GATE",
   W33_40_spectrum={"12":1,"2":24,"-4":15},
   actual_A5_conjugacy_classes_checked=2,
   source_25_A5_module_irreps=SRC,
   records=results,
   criterion="A5-equivariant unitary isometry of the WHOLE Reye25 module onto W33's 12+2 eigenspace exists iff the A5 character multiplicities agree. If no, rank of maximal intertwiner into that eigenspace is the sum over irreps dim*min multiplicities.",
   novelty="New actual-character check after the previous explicit A5-isometric map was shown to leak under W33 adjacency. Prior Pass999 separately classified two A5 classes.",
   physics_limit="A5 representations of 25 and 40 scalar labels, not a qutrit Pauli operator map or photonic ququart gate. Even if source module fits an eigenspace, nothing derives a Lorentzian TOE.")
 OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf8")
 print(result["status"],[(x["W33_12plus2_submodule_isomorphic_to_packet25"],x["max_25_to_W33_12plus2_intertwiner_rank"],x["irreducible_decompositions"]["12plus2"]) for x in results],flush=True)
 return result
if __name__=="__main__":main()
