#!/usr/bin/env python3
"""Passes 4497--4499: higher Ihara coefficients, Clifford lift, and thermal enumerator.

4497  Pushes the line-signed Hashimoto/Artin-Ihara expansion through u^8.
      The first coefficient beyond the line sum S and apartment Walsh sum W4 is
      u^5.  Its undirected simple-C5 holonomy sum decomposes exactly as
          U5 = 6 W_P3 + W_C5*
      over 2160 induced P3 triples and 5184 induced C5s of the dual W33 graph.
      A two-signing witness has the same S and W4 but different U5.

4498  Places the irreducible apartment 8-core in explicit four-qubit Pauli
      coordinates q=sum_i x_i z_i, conjugates five PSp generators plus the
      outer PGSp involution into Sp(8,2), and gives verified decompositions into
      binary symplectic transvections.  Each transvection is the projective
      Clifford action of a pi/4 Pauli rotation; no hardware realization follows.

4499  Uses the now-proved low primal weight enumerator to give an exact
      low-temperature partition expansion.  The complete 2^39 weight enumerator
      remains open and is stated as such.
"""
from __future__ import annotations
import itertools, json, math
from collections import Counter
from pathlib import Path
import numpy as np

from w33_pass4495_4502_distance_prism_reconstruction import (
    geometry, transvection3, build_line_perm, perm_group, J3
)
from w33_pass4496_h10_extension_cohomology import (
    rref2, rank2, nullspace2, inv2, permute_vector, matrix_group
)

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"PART_W33_PASS4497_4499_IHARA_CLIFFORD_THERMAL.json"
DIST=ROOT/"data"/"PART_W33_PASS4495_4502_DISTANCE_PRISM_RECONSTRUCTION.json"

def point_graph(lines):
    A=np.zeros((40,40),dtype=np.uint8);edge_line={}
    for li,L in enumerate(lines):
        for u,v in itertools.combinations(sorted(L),2):
            A[u,v]=A[v,u]=1;edge_line[(min(u,v),max(u,v))]=li
    return A,edge_line

def simple_cycles(A,k):
    adj=[list(np.flatnonzero(A[i])) for i in range(len(A))];out=[]
    for s in range(len(A)):
        def rec(path,used):
            cur=path[-1]
            if len(path)==k:
                if A[cur,s] and path[1]<cur: out.append(tuple(path))
                return
            for nxt in adj[cur]:
                if nxt<=s or nxt in used: continue
                rec(path+[nxt],used|{nxt})
        for n1 in adj[s]:
            if n1>s: rec([s,n1],{s,n1})
    return out

def cyc_line_mask(cyc,edge_line):
    m=0
    for i in range(len(cyc)):
        u,v=cyc[i],cyc[(i+1)%len(cyc)]
        m^=1<<edge_line[(min(u,v),max(u,v))]
    return m

def pseq(lam,K,q=11):
    p=[2,lam]
    for _ in range(2,K+1):p.append(lam*p[-1]-q*p[-2])
    return p

def primitive_counts(Btr):
    N={}
    for n in range(1,9):
        rem=Btr[n]-sum(d*N[d] for d in range(1,n) if n%d==0)
        assert rem%n==0;N[n]=rem//n
    return N

def build_middle8(pts,pidx,lines,Astar):
    all_trans=[build_line_perm(transvection3(v),pts,pidx,lines) for v in pts]
    selected=[];Gperm={tuple(range(40))}
    for p in all_trans:
        trial=perm_group(selected+[p])
        if len(trial)>len(Gperm):selected.append(p);Gperm=trial
        if len(Gperm)==25920:break
    _,piv=rref2(Astar);piv=piv[:10];B10=Astar[:,piv]
    _,rp=rref2(B10.T);rows=rp[:10];left=inv2(B10[rows,:])
    def q10(p):
        cols=[]
        for j in range(10):
            y=permute_vector(B10[:,j],p);c=(left@y[rows])%2
            assert np.array_equal((B10@c)%2,y);cols.append(c)
        return np.column_stack(cols).astype(np.uint8)
    G10=[q10(p) for p in selected];F10=Astar[np.ix_(piv,piv)].astype(np.uint8)
    fixed=nullspace2(np.vstack([g^np.eye(10,dtype=np.uint8) for g in G10]))
    assert len(fixed)==1;v=fixed[0]
    vperp=nullspace2((v.reshape(1,-1)@F10)%2)
    Ucols=[v.copy()]
    for x in vperp:
        if rank2(np.column_stack(Ucols+[x]))==len(Ucols)+1:Ucols.append(x)
        if len(Ucols)==9:break
    U=np.column_stack(Ucols);_,urp=rref2(U.T);ur=urp[:9];Uleft=inv2(U[ur,:])
    def q8(g):
        cols=[]
        for j in range(1,9):
            y=(g@U[:,j])%2;c=(Uleft@y[ur])%2
            assert np.array_equal((U@c)%2,y);cols.append(c[1:])
        return np.column_stack(cols).astype(np.uint8)
    G8=[q8(g) for g in G10];F8=((U.T@F10@U)%2)[1:,1:]
    outer3=np.diag([1,2,1,2])%3
    outerp=build_line_perm(outer3,pts,pidx,lines)
    O8=q8(q10(outerp))
    return G8,O8,F8

def qbase(F,x):
    s=0
    for i in range(len(x)):
        for j in range(i+1,len(x)):
            if F[i,j] and x[i] and x[j]:s^=1
    return s

def transvection(v,J):
    v=v.reshape(-1,1)
    return (np.eye(len(v),dtype=np.uint8)+v@((J@v).T))%2

def maskvec(m,n=8): return np.array([(m>>i)&1 for i in range(n)],dtype=np.uint8)
def pauli_label(mask):
    labs=[]
    for q in range(4):
        x=(mask>>(2*q))&1;z=(mask>>(2*q+1))&1
        labs.append({(0,0):"I",(1,0):"X",(0,1):"Z",(1,1):"Y"}[(x,z)])
    return "".join(labs)

def main():
    pts,pidx,lines,Astar,apartments,apmasks,H=geometry()
    A,edge_line=point_graph(lines)

    # ---- Pass 4497: higher prime/Ihara coefficients -----------------------
    c5=simple_cycles(A,5);assert len(c5)==18144
    mask_mult=Counter(cyc_line_mask(c,edge_line) for c in c5)
    profile=Counter((m.bit_count(),mult) for m,mult in mask_mult.items())
    assert profile==Counter({(3,6):2160,(5,1):5184})
    p3=0;c5dual=0
    for m,mult in mask_mult.items():
        vs=[i for i in range(40) if (m>>i)&1]
        deg=sorted(sum(int(Astar[x,y]) for y in vs if y!=x) for x in vs)
        e=sum(int(Astar[x,y]) for x,y in itertools.combinations(vs,2))
        if m.bit_count()==3:
            assert mult==6 and e==2 and deg==[1,1,2];p3+=1
        else:
            assert mult==1 and e==5 and deg==[2]*5;c5dual+=1
    assert (p3,c5dual)==(2160,5184)

    spec=[(12,1),(2,24),(-4,15)]
    Btr={}
    for k in range(1,9):
        Btr[k]=sum(mult*pseq(lam,8)[k] for lam,mult in spec)+200*(1+(-1)**k)
    assert Btr=={1:0,2:0,3:960,4:13920,5:181440,6:1818240,7:19178880,8:214015200}
    N=primitive_counts(Btr)
    assert N=={1:0,2:0,3:320,4:3480,5:36288,6:302880,7:2739840,8:26750160}

    def signs(neg):
        s=np.ones(40,dtype=int);s[list(neg)]=-1;return s
    def W4(s): return int(sum(np.prod(s[list(ap)]) for ap in apartments))
    def U5(s):
        negmask=sum(1<<i for i,x in enumerate(s) if x<0);tot=0
        for m,mult in mask_mult.items():
            tot+=mult*(-1 if ((m&negmask).bit_count()&1) else 1)
        return int(tot)
    witnessA=[1,4,6,7,8,10,11,15,18,19,20,21,22,25,28,30,31,32,33,37,39]
    witnessB=[2,3,4,5,8,9,10,12,16,19,21,22,23,24,25,28,33,34,36,37,38]
    sa,sb=signs(witnessA),signs(witnessB)
    assert (int(sa.sum()),W4(sa),U5(sa))==(-2,8,600)
    assert (int(sb.sum()),W4(sb),U5(sb))==(-2,8,-136)
    var_U5=2160*6**2+5184
    assert var_U5==82944 and int(math.isqrt(var_U5))==288
    var_C5=4*var_U5
    null={"E_U5":0,"Var_U5":var_U5,"SD_U5":288,
          "E_C5":0,"Var_C5":var_C5,"SD_C5":576,
          "Cov_S_U5":0,"Cov_W4_U5":0}

    # ---- Pass 4498: explicit four-qubit Clifford coordinates --------------
    G8,O8,F8=build_middle8(pts,pidx,lines,Astar)
    assert len(matrix_group(G8))==25920 and len(matrix_group(G8+[O8]))==51840
    invariant_ell=[]
    for em in range(256):
        ell=maskvec(em);ok=True
        for g in G8:
            for xm in range(256):
                x=maskvec(xm);gx=(g@x)%2
                if (qbase(F8,x)^int(np.dot(ell,x)%2)) != (qbase(F8,gx)^int(np.dot(ell,gx)%2)):
                    ok=False;break
            if not ok:break
        if ok:invariant_ell.append(ell)
    assert len(invariant_ell)==1 and invariant_ell[0].tolist()==[1,1,1,1,1,1,0,0]
    ell=invariant_ell[0]
    def qinv(x):return qbase(F8,x)^int(np.dot(ell,x)%2)
    supports=[[0,2],[1,2],[0,1,3],[0,1,2,3],[0,3,6],[0,3,4,6],[0,2,3,7],[2,5,6,7]]
    P=np.column_stack([np.array([int(i in s) for i in range(8)],dtype=np.uint8) for s in supports])
    Jcan=np.zeros((8,8),dtype=np.uint8)
    for i in range(0,8,2):Jcan[i,i+1]=Jcan[i+1,i]=1
    assert rank2(P)==8 and np.array_equal((P.T@F8@P)%2,Jcan)
    def qcan(x):return sum(int(x[i]&x[i+1]) for i in range(0,8,2))%2
    for xm in range(256):
        x=maskvec(xm);assert qinv((P@x)%2)==qcan(x)
    Pinv=inv2(P);Gcan=[(Pinv@g@P)%2 for g in G8];Ocan=(Pinv@O8@P)%2
    seqs=[[224,176,112,48,11,7],[224,176,112,48,13,3],
          [176,112,13,11,7,3],[252,172,107,43,13,3],[185,113,77,76,27,19]]
    seqO=[172,151,75,13]
    def product(seq):
        M=np.eye(8,dtype=np.uint8)
        for m in seq:M=(transvection(maskvec(m),Jcan)@M)%2
        return M
    assert all(np.array_equal(product(seq),g) for seq,g in zip(seqs,Gcan))
    assert np.array_equal(product(seqO),Ocan)
    clifford={
      "hyperbolic_basis_old_coordinate_supports":supports,
      "canonical_quadratic":"q=x1*z1+x2*z2+x3*z3+x4*z4 mod 2",
      "inner_generator_transvection_masks":seqs,
      "inner_generator_Pauli_rotations":[[pauli_label(m) for m in seq] for seq in seqs],
      "outer_transvection_masks":seqO,"outer_Pauli_rotations":[pauli_label(m) for m in seqO],
      "inner_image_order":25920,"outer_image_order":51840}

    # ---- Pass 4499: exact low-temperature enumerator ----------------------
    dist=json.loads(DIST.read_text(encoding="utf-8"))
    low={int(k):int(v) for k,v in dist["4495_primal_distance"]["exact_low_weight_counts"].items()}
    assert low=={162:40,270:240,312:540,324:200}
    thermal={
      "exact_identity":"Z(beta)=2*exp(1620*beta)*W_C(exp(-2*beta))",
      "proved_low_weight_enumerator":{"0":1,**{str(k):v for k,v in low.items()}},
      "low_temperature_expansion":"2 e^(1620 beta) [1 + 40 e^(-324 beta) + 240 e^(-540 beta) + 540 e^(-624 beta) + 200 e^(-648 beta) + R(beta)]",
      "remainder":"R(beta)=sum_{w>324} A_w exp(-2 beta w); the complete weight enumerator is not yet computed.",
      "full_enumerator_status":"OPEN"}

    result={
      "passes":[4497,4498,4499],
      "4497_ihara":{
        "signed_trace_formulas":{"trB3":"T3","trB4":"T4 - 11040","trB5":"T5 - 55*T3",
          "trB6":"T6 - 66*T4 + 416640","trB7":"T7 - 77*T5 + 1694*T3",
          "trB8":"T8 - 88*T6 + 2420*T4 - 9050400"},
        "logL_coefficients":{"u3":"8*S, S=sum_l sigma_l","u4":"240 + 2*W4","u5":"C5",
          "u6":"160 + C6","u7":"C7","u8":"1740 + C8"},
        "unsigned_oriented_primitive_prime_counts":{str(k):int(v) for k,v in N.items() if k>=3},
        "simple_C5_count":18144,
        "pentagonal_shadow":{"dual_P3_masks":2160,"multiplicity_each_P3":6,
          "dual_C5_masks":5184,"multiplicity_each_C5":1,
          "identity":"U5 = 6*W_P3 + W_C5star; C5=2*U5"},
        "random_line_sign_null":null,
        "first_new_information_witness":{"common_S":-2,"common_W4":8,"common_apartment_weight":806,
          "signing_A_negative_lines":witnessA,"U5_A":600,"C5_A":1200,"trB5_A":6000,
          "signing_B_negative_lines":witnessB,"U5_B":-136,"C5_B":-272,"trB5_B":-1360},
        "conclusion":"u^5 is the first coefficient not determined by the line sum S and apartment Walsh sum W4.",
        "boundary":"Cn denotes the signed sum over oriented primitive nonbacktracking prime classes of length n. The u6/u8 constants are fixed repetitions of length-3/length-4 primes."},
      "4498_clifford":clifford,
      "4499_thermal":thermal}
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("PASS 4497-4499")
    print("  log L through u^8 classified; u^5 is first new invariant")
    print("  C5 shadow: 2160 P3 x6 + 5184 dual C5 x1")
    print("  explicit four-qubit Clifford transvection lifts verified")
    print("  low-temperature enumerator extended exactly; full enumerator remains open")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
