#!/usr/bin/env python3
"""H27 regular-versus-three-qutrit algebra benchmark; S3 generator search.

Carefully distinguishes H27 group algebra (dimension 27 in left regular)
from irreducible 3-qutrit Weyl operator algebra (dimension 729).
Tests how many dynamically meaningful S3 gauge invariants are needed
to reach numerically irreducible 27D physical operator action.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
import numpy as np
from toe_20261105_s3_exchange_mobile_obstruction import matrix_family,PERMS,INDEX,TRANS,mul,inv,irrep
from toe_20261105_s3_algebra_square_followthrough import exchange_difference
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261105_h27_regular_pauli_gauge_algebra_compare.json"

def h27_compare():
    group=list(itertools.product(range(3),repeat=3))
    index={x:i for i,x in enumerate(group)}
    def op(x,y):
        a,b,c=x;d,e,f=y
        return ((a+d)%3,(b+e)%3,(c+f+a*e)%3)
    N=27
    left=[];right=[]
    for g in group:
        L=np.zeros((N,N),dtype=np.uint8)
        R=np.zeros((N,N),dtype=np.uint8)
        for j,x in enumerate(group):
            L[index[op(g,x)],j]=1
            R[index[op(x,g)],j]=1
        left.append(L);right.append(R)
    assert len(left)==27
    assert np.linalg.matrix_rank(np.array([x.ravel() for x in left],float))==27
    assert np.linalg.matrix_rank(np.array([x.ravel() for x in right],float))==27
    assert max(np.max(abs(L.astype(int)@R.astype(int)-R.astype(int)@L.astype(int)))
               for L in left for R in right)==0
    center=left[index[(0,0,1)]]
    assert np.linalg.matrix_power(center,3).tolist()==np.eye(27,dtype=int).tolist()
    zvalues=np.linalg.eigvals(center)
    counts={str(j):int(sum(abs(zvalues-np.exp(2j*np.pi*j/3))<1e-8)) for j in range(3)}
    assert sorted(counts.values())==[9,9,9]
    w=np.exp(2j*np.pi/3)
    X=np.roll(np.eye(3,dtype=complex),1,axis=0)
    Z=np.diag(w**np.arange(3))
    assert np.max(abs(Z@X-w*X@Z))<2e-12
    ops=[np.linalg.matrix_power(X,a)@np.linalg.matrix_power(Z,b)
         for a,b in itertools.product(range(3),repeat=2)]
    gram=np.array([[np.trace(A.conj().T@B)/3 for B in ops] for A in ops])
    assert np.max(abs(gram-np.eye(9)))<2e-12
    return {"H27_order":27,"H27_left_regular_associative_algebra_dimension":27,
       "H27_right_regular_commutant_contains_dim":27,
       "H27_center_eigenspace_dimensions":counts,
       "three_qutrit_Weyl_operator_basis_dimension":9**3,
       "single_qutrit_Weyl_Hilbert_Schmidt_orthonormal":True,
       "full_Mat27_dimension":27**2,
       "nonidentification":"A regular representation of the 27-element Heisenberg H27 is not an irreducible representation of the 729-dimensional three-qutrit full operator algebra. H27's center has 9+9+9 sectors in the left regular representation."}

def connectivity(ops,seed=61873):
    gen=list(ops)+[1j*(ops[0]@ops[1]-ops[1]@ops[0])]
    min_gap=0
    rng=np.random.default_rng(seed)
    for attempt in range(12):
        c=rng.uniform(.07,1.,len(gen))*rng.choice((-1,1),len(gen))
        H=sum(z*A for z,A in zip(c,gen))
        H=(H+H.conj().T)/2
        eig,V=np.linalg.eigh(H)
        gap=float(min(np.diff(eig)))
        if gap>1e-6:break
    weight=np.maximum.reduce([abs(V.conj().T@A@V) for A in ops])
    np.fill_diagonal(weight,0)
    adj=weight>1e-8
    seen=set();sizes=[]
    for k in range(27):
        if k in seen:continue
        stack=[k];seen.add(k);n=0
        while stack:
            i=stack.pop();n+=1
            for j in np.flatnonzero(adj[i]):
                j=int(j)
                if j not in seen:seen.add(j);stack.append(j)
        sizes.append(n)
    return {"generic_simple_spectral_gap":gap,"components":sorted(sizes,reverse=True),
      "connected_component_decomposition_interpretable":gap>1e-6,
      "commutant_scalar_if_simple_and_connected":gap>1e-6 and len(sizes)==1,
      "nonzero_transition_edges":int(np.count_nonzero(adj)//2),
      "minimum_nonzero_edge_magnitude":float(min(weight[adj])) if adj.any() else 0,
      "is_numerical_not_interval_certified":True}

def s3_progress():
    reps,U,P,(E,M,C),F=matrix_family("tensor")
    D=exchange_difference();I4=np.eye(4)
    W1=np.zeros((144,144));W2=W1.copy()
    Cd=np.zeros((144,144));Cx=np.zeros((144,144));Ush=np.zeros((144,144))
    Uinv=np.zeros((144,144))
    for i,g in enumerate(PERMS):
        for j,k in enumerate(PERMS):
            sl=slice(4*(6*i+j),4*(6*i+j)+4)
            rg=(reps[i]+reps[i].T)/2
            rk=(reps[j]+reps[j].T)/2
            W1[sl,sl]=np.trace(reps[i])/2*I4
            W2[sl,sl]=np.trace(reps[j])/2*I4
            Cd[sl,sl]=np.kron(rg,np.eye(2))-np.kron(np.eye(2),rk)
            cross=np.kron(reps[i],reps[j])
            Cx[sl,sl]=(cross+cross.T)/2
            b=INDEX[mul(g,k)]
            Ush[slice(4*(6*i+b),4*(6*i+b)+4),sl]=I4
            ni=INDEX[inv(g)]
            Uinv[slice(4*(6*ni+j),4*(6*ni+j)+4),sl]=I4
    S=(Ush+Ush.T)/2
    for X in (D,W1,W2,Cd,Cx,S,Uinv):
        assert np.max(abs(X-X.T))<1e-12
        assert max(np.max(abs(X@u-u@X)) for u in U)<2e-12
    physical={name:F.T@X@F for name,X in [
       ("E",E),("M",M),("C",C),("D",D),
       ("W1",W1),("W2",W2),("Cdiff",Cd),("Ccross",Cx),
       ("Nielsen_shear",S),("loop_inverse",Uinv)]}
    sets=[
       ("original_EMC",["E","M","C"]),
       ("add_electric_difference",["E","M","C","D"]),
       ("add_loop_Wilson_trace",["E","M","C","D","W1"]),
       ("add_two_Wilson_traces",["E","M","C","D","W1","W2"]),
       ("add_color_difference",["E","M","C","D","Cdiff"]),
       ("add_correlated_matter",["E","M","C","D","Ccross"]),
       ("add_holonomy_shear",["E","M","C","D","Nielsen_shear"]),
       ("full_10_operator_family",list(physical))
    ]
    records=[]
    for name,keys in sets:
        test=connectivity([physical[k] for k in keys])
        records.append({"name":name,"generators":keys,**test})
    optional=["W1","W2","Cdiff","Ccross","Nielsen_shear","loop_inverse"]
    base=["E","M","C","D"]
    minimal=[]
    for k in range(1,len(optional)+1):
        for extra in itertools.combinations(optional,k):
            test=connectivity([physical[t] for t in base+list(extra)])
            if test["commutant_scalar_if_simple_and_connected"]:
                minimal.append({"added_generators":list(extra),
                                "generic_simple_spectral_gap":test["generic_simple_spectral_gap"],
                                "smallest_witnessed_transition":test["minimum_nonzero_edge_magnitude"]})
        if minimal:break
    assert minimal  # Ten gauge-invariant operators do give a full-27 numerical witness.
    minimal_keys=base+minimal[0]["added_generators"]
    robust=[{"random_seed":seed,**connectivity([physical[t] for t in minimal_keys],seed)}
            for seed in (61873,12345,96731)]
    assert all(row["commutant_scalar_if_simple_and_connected"] for row in robust)
    assert all(row["minimum_nonzero_edge_magnitude"]>1e-5 for row in robust)
    return {"records":records,"gauge_invariance_of_extra_generators":True,
            "minimal_ensemble_robustness":robust,
            "smallest_irreducibility_addition_size":len(minimal[0]["added_generators"]),
            "minimal_irreducible_additions":minimal,
            "guard":"If the full family becomes irreducible, it still does not endow a *canonical* H27 history interpretation. These are finite, numerical common-commutant screens."}

def main():
    out={"status":"PASS_H27_GROUP_ALGEBRA_VS_QUTRIT_ALGEBRA_AND_S3_EXTENSION",
         "H27":h27_compare(),"S3_gauge":s3_progress()}
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
    for a in out["S3_gauge"]["records"]:print("COMMUTANT",a["name"],a["components"],a["generic_simple_spectral_gap"])
    print("CERTIFICATE",OUT)
    return out
if __name__=="__main__":main()
