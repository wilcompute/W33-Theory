#!/usr/bin/env python3
"""Pass 4486 -- the repeated U/J core is null in the radical and O+(8,2) when protected.

Pass 4485 proved that the literal quotient U/J occurs twice in the apartment
code: as a submodule of the 29-dimensional radical K/J and as the middle factor
of the protected 10-space M/K ~= I=im(A*).

This pass compares the forms, not just the actions.

Radical occurrence:
  y in U <= K gives apartment vector H^T y.  Since K/J is the radical of
  C_ap, its polar pairing is identically zero.  The Hamming quadratic
  q_ap=wt/2 mod2 is also identically zero on U/J.

Protected occurrence:
  A*: M/K -> I is an isomorphism.  For y=A*b and z=A*c in I define

      B_prot(y,z) = b^T A* c,
      q_prot(y)   = wt(Nb)/2 mod 2.

  These are lift-independent because changing b by k in K changes Nb only by
  the doubly-even sentinel code C=ker N^T.  Restricted to U, J is exactly the
  radical; hence U/J inherits a nondegenerate 8-dimensional alternating form.
  Exhaustion gives 136 singular classes including zero and 120 anisotropic,
  i.e. plus type O+(8,2).

Thus the same irreducible U/J representation is "form-null" on the radical
side and carries the protected O+(8,2) metric on the quotient side.  This is the
exact bridge to parallel Passes 4477/4478, without importing their hardware
interpretation.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
from w33_pass158_chiral_trade_lattice_two_480s import build_w33, w33_lines
from w33_pass4461_line_signing_apartment_trace import geometry, simple_four_cycles
from w33_pass4469_apartment_css_h10_intertwiner import nullspace_mod2, rref_rows
from w33_pass4470_apartment_h10_quadratic_fixed_layer import q_half_weight, solve_mod2
from w33_pass4481_apartment_radical_module_filtration import inter

ROOT=Path(__file__).resolve().parents[1]
def rank2(M): return len(rref_rows(np.asarray(M,dtype=np.uint8)))
def quotient_reps(big,small):
    cur=rref_rows(small); reps=[]; r=len(cur)
    for v in rref_rows(big):
        trial=rref_rows(np.vstack((cur,v)))
        if len(trial)>r:
            reps.append(v.copy()); cur=trial; r+=1
    return np.asarray(reps,dtype=np.uint8)
def main():
    _,A,_=build_w33(); lines=w33_lines(A); N=np.zeros((40,40),dtype=np.uint8)
    for li,L in enumerate(lines):N[list(L),li]=1
    Ast=(N.T@N)%2; K=rref_rows(nullspace_mod2(Ast)); I=rref_rows(Ast); R=rref_rows(nullspace_mod2(N)); U=inter(R,I); J=np.ones((1,40),dtype=np.uint8)
    # Apartment H from the canonical geometry helper to verify the null occurrence directly.
    _,_,Ap,N0,edge_line=geometry(); aps=[frozenset(edge_line[e] for e in c) for c in simple_four_cycles(Ap)]
    H=np.zeros((40,len(aps)),dtype=np.uint8)
    for j,S in enumerate(aps):H[list(S),j]=1
    reps=quotient_reps(U,J); assert len(reps)==8
    # Protected lifts b_i with A*b_i = reps_i.
    lifts=np.asarray([solve_mod2(Ast,v) for v in reps],dtype=np.uint8)
    F=(lifts@Ast@lifts.T)%2
    # q on protected core via H10 representatives N b.
    qbasis=np.asarray([q_half_weight((N@b)%2) for b in lifts],dtype=np.uint8)
    # q is quadratic, so evaluate all classes explicitly from representatives.
    qprot=[]; qrad=[]
    for m in range(256):
        c=np.array([(m>>i)&1 for i in range(8)],dtype=np.uint8)
        b=(c@lifts)%2; y=(c@reps)%2
        qprot.append(q_half_weight((N@b)%2))
        qrad.append(q_half_weight((H.T@y)%2))
    # Restriction on U before quotient: J should be the unique polar radical.
    Ureps=np.vstack((J,reps)); Ulifts=np.asarray([solve_mod2(Ast,v) for v in Ureps],dtype=np.uint8)
    FU=(Ulifts@Ast@Ulifts.T)%2
    checks={
      'dims':(len(J),len(U),len(I),len(K))==(1,9,10,30),'UmodJ_dim8':len(reps)==8,
      'protected_F_alternating':np.all(np.diag(F)==0),'protected_F_rank8':rank2(F)==8,
      'U_restriction_rank8':rank2(FU)==8,'J_is_restriction_radical':np.all(FU[0]==0) and np.all(FU[:,0]==0),
      'protected_plus_counts':qprot.count(0)==136 and qprot.count(1)==120,
      'radical_q_identically_zero':qrad==[0]*256,
      'radical_polar_zero':not np.any(((H.T@reps.T).T @ ((H.T@reps.T).T).T)%2),
      'parallel_counts_match_4477':(qprot.count(0)-1,qprot.count(1))==(135,120)}
    # Lift independence spot-check/exhaustion: adding every K-basis vector to each lift leaves q and B row unchanged.
    lift_independent=True
    for i,b in enumerate(lifts):
        for k in K:
            b2=b^k
            if q_half_weight((N@b2)%2)!=q_half_weight((N@b)%2):lift_independent=False;break
            if not np.array_equal((b2@Ast@lifts.T)%2,(b@Ast@lifts.T)%2):lift_independent=False;break
        if not lift_independent:break
    checks['protected_forms_lift_independent']=lift_independent
    assert all(checks.values()),checks
    out={'pass':4486,'theorem':'W33 repeated 8-core form-resurrection theorem','core':'U/J','dimension':8,
      'radical_occurrence':{'polar_rank':0,'quadratic':'identically zero on all 256 classes'},
      'protected_occurrence':{'polar_rank':8,'quadratic_type':'O+(8,2)','singular_including_zero':136,'singular_nonzero':135,'anisotropic':120,'lift_independent':True},
      'connection':'The exact 135/120 protected counts are the same finite 8-core used by parallel Passes 4477/4478.',
      'boundary':'Same module does not mean same form: the radical occurrence is totally null. No physical metric creation, E8 dynamics, or four-qubit hardware is inferred.',
      'checks':{'passed':sum(checks.values()),'total':len(checks)}}
    p=ROOT/'data/PART_W33_PASS4486_REPEATED_CORE_FORM_RESURRECTION.json';p.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
