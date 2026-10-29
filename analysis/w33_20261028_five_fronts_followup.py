#!/usr/bin/env python3
"""Five post-compression W33 native gauge/matter tests, with exact scope fences.

Use actual repository certificates: native commutators, 105 zero-voltage faces,
H27 deck voltages, 6-form common-cone metric. No invented spacetime dynamics.
"""
import json
import sys
from pathlib import Path
from itertools import combinations
from fractions import Fraction
import numpy as np
import sympy as sp
from scipy import linalg
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import eigsh

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261028_three_mixed_loop_minimal_maxwell import certificate,rank_mod,bloch_row,frac_matrix
from w33_20261027_native_bloch_face_module import geometry

R=sp.Matrix([[1,0,5,-5,1,0],[0,1,-1,0,1,0],[0,0,5,-5,0,1]])
REF=sp.Matrix([[-1,0,0,0],[1,1,0,0],[-1,0,1,0],[0,0,0,1]])
ELECTRIC_GRAM=sp.Matrix([[794,-42,768],[-42,22,-52],[768,-52,766]])
CHARGES=[(1,0,0),(0,1,0),(0,0,1),(3,-4,-4),(3,-4,-3),(3,4,-3),(4,-4,-3),(4,-3,-4),(4,4,-3)]
WEIGHTS=[Fraction(1,10000)]*3+[Fraction(49937,630000),Fraction(21313,378000),
Fraction(49241,1350000),Fraction(1241,90000),Fraction(142189,3150000),Fraction(1,56)]
PAIRS=list(combinations(range(4),2))

def compound(T):
    return sp.Matrix([[T[a,c]*T[b,d]-T[a,d]*T[b,c] for c,d in PAIRS] for a,b in PAIRS])

def action_and_reduction():
    source=json.loads((ROOT/"data/w33_20261027_native_bloch_face_module.json").read_text())
    metric=json.loads((ROOT/"data/w33_20261027_five_front_followthrough.json").read_text())
    H=frac_matrix(source["engineered_matched_metric"]["six_loop_flux_coupling_H"])
    J=frac_matrix(metric["metric_classification"]["J"])
    M=frac_matrix(source["effective_symbol"]["harmonic_link_gram_M"])
    W=sp.Matrix(source["deck_loop_periods"])
    S=compound(W*REF*W.inv())
    assert REF.det()==-1 and REF*REF==sp.eye(4) and REF.T*M*REF==M
    assert S.T*H*S==H and S.T*J*S==-J
    assert S.T*(H-2*J)*S==H+2*J
    star=2*H.inv()*J
    assert star*star==sp.eye(6) and star.trace()==0
    assert (sp.eye(6)-star).rank()==(sp.eye(6)+star).rank()==3
    assert R.T*frac_matrix(certificate()["positive_K_3x3"])*R==H-2*J
    even=sp.Matrix.hstack(*(REF-sp.eye(4)).nullspace())
    odd=sp.Matrix.hstack(*(REF+sp.eye(4)).nullspace())
    assert even.rank()==3 and odd.rank()==1 and even.T*M*odd==sp.zeros(3,1)
    assert even.T*M*even==sp.Matrix([[10,0,-6],[0,12,-6],[-6,-6,12]])
    assert odd.T*M*odd==sp.Matrix([[18]])
    n=sp.Matrix([1,0,0,0]);u=W*n
    C=sp.Matrix([[u[a]*W[b,k]-u[b]*W[a,k] for k in range(4)] for a,b in PAIRS])
    speeds={}
    for eps in (sp.Rational(0),sp.Rational(1,100),sp.Rational(1,10)):
        Hmag=C.T*(H-2*J+eps*sp.eye(6))*C
        speeds[str(eps)]=[float(x) for x in linalg.eigh(np.array(Hmag,dtype=float),
                             np.array(M,dtype=float),eigvals_only=True)[1:]]
    assert max(speeds["0"])-min(speeds["0"])<1e-12
    assert max(speeds["1/100"])-min(speeds["1/100"])>0.002
    return {"status":"EXACT_ORIENTATION_REFLECTION_INTERCHANGES_ENDPOINTS",
      "hodge_involution":"star=2 H0^-1 J, star^2=I, eigenvalue multiplicities 3+3",
      "rank_H_ends":[3,3],"endpoint_exchange":True,"single_cone_splitting":speeds,
      "dimensional_reduction":{"three_even_period_metric":[[10,0,-6],[0,12,-6],[-6,-6,12]],
                               "even_determinant":648,"odd_norm_squared":18},
      "boundary":"This uses the period representation, not a lift to the full charged action. A reflection-invariant choice exchanges endpoints, and supplied external time is not selected."}

def lifted_chain(loop,V,edges):
    position=[0,0,0,0];vertex=0;chain={}
    for eid,sgn in loop:
        eid=int(eid);sgn=int(sgn);a,b=map(int,edges[eid])
        if sgn==1:
            assert vertex==a,(eid,vertex,a,b)
            key=(tuple(position),eid)
            position=[position[j]+int(V[eid][j]) for j in range(4)]
            vertex=b
        else:
            assert vertex==b,(eid,vertex,a,b)
            position=[position[j]-int(V[eid][j]) for j in range(4)]
            key=(tuple(position),eid)
            vertex=a
        chain[key]=chain.get(key,0)+sgn
    assert vertex==0 and position==[0,0,0,0]
    return {key:n for key,n in chain.items() if n}

def native_bloch_and_gauss():
    _,V,edges,_,_=geometry()
    old=json.loads((ROOT/"data/w33_20261027_native_bloch_face_module.json").read_text())
    faces=json.loads((ROOT/"data/PART_20261023_NATIVE_ZERO_HOLONOMY_FACE_COMPLETION.json").read_text())["independent_face_basis"]
    loops=old["commutator_boundaries"]
    chains=[lifted_chain(loop,V,edges) for loop in loops]
    mixed=[]
    for i in range(3):
        row={}
        for a in range(6):
            for key,n in chains[a].items():row[key]=row.get(key,0)+int(R[i,a])*n
        mixed.append({key:n for key,n in row.items() if n})
    gram=sp.Matrix([[sum(n*mixed[j].get(key,0) for key,n in mixed[i].items()) for j in range(3)] for i in range(3)])
    assert gram==ELECTRIC_GRAM
    corners=[]
    for mask in range(16):
        z=tuple(-1 if mask>>j&1 else 1 for j in range(4))
        short=[bloch_row(f["boundary"],V,z,101) for f in faces]
        six=[bloch_row(loop,V,z,101) for loop in loops]
        three=[[sum(int(R[i,j])*six[j][k] for j in range(6))%101 for k in range(135)] for i in range(3)]
        r0=rank_mod(short,101)
        r1=rank_mod(short+three,101)
        assert r0==105 and r1==(105 if mask==0 else 108)
        corners.append({"mask":mask,"signs":list(z),"short_rank":r0,"mixed_rank":r1})
    return {"status":"NATIVE_GAUSS_PLUS_ALL_16_BLOCH_CORNERS_MOD101",
        "mixed_link_support":[len(x) for x in mixed],
        "integer_lifted_gauss_exact":True,"electric_gram":[[int(v) for v in row] for row in ELECTRIC_GRAM.tolist()],
        "corners":corners,
        "boundary":"Full maximal rank certified only at 15 nontrivial order-two Bloch corners and previous generic specializations, not everywhere in the Brillouin zone."}

def rotor(L,g):
    mside=2*L+1;dim=mside**3;idx=np.arange(dim)
    coords=np.stack(np.unravel_index(idx,(mside,)*3),axis=1).astype(np.int64)-L
    G=np.array(ELECTRIC_GRAM,dtype=np.int64)
    onsite=(g*g/2)*np.einsum('ni,ij,nj->n',coords,G,coords,optimize=True)+sum(map(float,WEIGHTS))
    rr=[idx];cc=[idx];vv=[onsite];strides=np.array([mside**2,mside,1])
    for q,w in zip(CHARGES,WEIGHTS):
        shift=np.array(q);valid=np.all((coords+shift>=-L)&(coords+shift<=L),axis=1)
        source=idx[valid];dest=source+shift@strides
        rr.extend([source,dest]);cc.extend([dest,source])
        vv.extend([np.full(len(source),-float(w)/2),np.full(len(source),-float(w)/2)])
    H=coo_matrix((np.concatenate(vv),(np.concatenate(rr),np.concatenate(cc))),shape=(dim,dim)).tocsr()
    eig,vec=eigsh(H,k=2,which="SA",tol=1e-10,maxiter=30000)
    order=np.argsort(eig);eig=eig[order];vec=vec[:,order]
    resid=np.linalg.norm(H@vec-vec*eig,axis=0)
    return {"L":L,"g":g,"states":dim,"ground_energy":float(eig[0]),
            "excitation_gap_in_truncated_sector":float(eig[1]-eig[0]),
            "boundary_mass":float(np.sum(abs(vec[np.any(abs(coords)==L,axis=1),0])**2)),
            "max_Ritz_residual":float(np.max(resid))}

def compact_quantum():
    assert ELECTRIC_GRAM.det()==260784
    assert all(ELECTRIC_GRAM[:i,:i].det()>0 for i in range(1,4))
    Hessian=sp.eye(3)/10000
    for q,w in zip(CHARGES[3:],WEIGHTS[3:]):
        v=sp.Matrix(q);Hessian+=sp.Rational(w.numerator,w.denominator)*v*v.T
    assert Hessian==frac_matrix(certificate()["positive_K_3x3"])
    records=[rotor(L,g) for g in (.1,.2) for L in (3,4,5)]
    for g in (.1,.2):
        case=[r for r in records if r["g"]==g]
        assert case[0]["ground_energy"]>case[1]["ground_energy"]
        assert case[2]["ground_energy"] <= case[1]["ground_energy"]+1e-9
        assert case[1]["ground_energy"]-case[2]["ground_energy"]<1e-6
        assert all(r["max_Ritz_residual"]<1e-8 for r in case)
    return {"status":"THREE_GAUSS_LOOP_COMPACT_ROTOR_FINITE_CUTOFF_ED",
        "kinetic_gram":[[int(v) for v in row] for row in ELECTRIC_GRAM.tolist()],"hessian_exact":True,"samples":records,
        "boundary":"Variational three-loop-electric subspace, not full link Hilbert space. Truncated ground upper bounds and gaps are not infinite-volume gap proofs."}

def E6_charge_response():
    mult=[10,5,1,5,5,1]
    charges=[(1,1),(-3,1),(5,1),(-2,-2),(2,-2),(0,4)]
    moments={}
    for a,b in [(1,0),(0,1),(2,0),(0,2),(1,1),(3,0),(0,3),(2,1),(1,2),(4,0),(0,4)]:
        moments[f"{a},{b}"]=sum(m*q**a*r**b for m,(q,r) in zip(mult,charges))
    for key in ("1,0","0,1","1,1","3,0","0,3","2,1","1,2"):
        assert moments[key]==0
    assert moments["2,0"]==120 and moments["0,2"]==72
    byname=dict(zip(("t","p","z","u","v","S"),charges))
    types=(("S","u","v"),("z","p","u"),("p","t","v"),("t","t","u"))
    for names in types:
        assert all(sum(byname[x][j] for x in names)==0 for j in (0,1))
    return {"status":"EXACT_E6_TWO_U1_CUBIC_WARD_AND_QUADRATIC_RESPONSE",
        "multiplicities":mult,"charge_pairs":charges,"moments":moments,
        "cubic_counts":{"Suv":5,"zpu":5,"ptv":20,"ttu":15},
        "equal_matter_response_trace_metric":[[120,0],[0,72]],
        "boundary":"Classical E6 branching charge traces. 5:3 response is conditional on an identical species response kernel; no matter determinant, chiral anomaly measure or physical coupling selection derived."}

def run():
    return {"schema":"w33.2026-10-28.five-front-native-followup.v1",
            "action_and_reduction":action_and_reduction(),
            "native_bloch":native_bloch_and_gauss(),
            "compact_quantum":compact_quantum(),
            "E6_matter":E6_charge_response(),
            "physics_boundary":"All four deck directions are spatial and the clock/time structure is externally supplied. No TOE or Lorentzian dynamics derived."}

if __name__=="__main__":
    data=json.dumps(run(),indent=2)+"\n"
    target=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/"data/w33_20261028_five_fronts_followup.json"
    target.write_text(data,encoding="utf8")
    print(target)
