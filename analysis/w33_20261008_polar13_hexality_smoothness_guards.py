#!/usr/bin/env python3
"""Physical/source firewalls: full discrete charge ledger, polar13 alternating
radical, and a finite-field smoothness preflight at new good-prime candidates.
"""
import json,itertools,math,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261008_polar13_symplectic_module import rref_rank
from w33_20261008_five_physics_frontiers import projective_points_and_lines
from w33_20261008_h27_h13_five_frontiers import canon,um,J
from w33_20261008_physical_five_controls import tetraquadric_affine_sieve
OUT=ROOT/"data"/"w33_20261008_polar13_hexality_smoothness_guards.json"
Q={"Q":0,"Uc":1,"Dc":5,"L":4,"Ec":1,"Nc":3,"Hu":5,"Hd":1}
X={"Q":2,"Uc":0,"Dc":2,"L":2,"Ec":2,"Nc":0,"Hu":1,"Hd":2}
Y={"Q":1,"Uc":-4,"Dc":2,"L":-3,"Ec":6,"Nc":0,"Hu":3,"Hd":-3}
multiplicity={"Q":6,"Uc":3,"Dc":3,"L":2,"Ec":1,"Nc":1,"Hu":2,"Hd":2}
matter=("Q","Uc","Dc","L","Ec","Nc")
def charge_ledger():
    def cubic(table):
        return 3*sum(multiplicity[v]*table[v]**3 for v in matter)+sum(multiplicity[v]*table[v]**3 for v in ("Hu","Hd"))
    def anomalies(table):
        a3=3*(2*table["Q"]+table["Uc"]+table["Dc"])
        a2=3*(3*table["Q"]+table["L"])+table["Hu"]+table["Hd"]
        grav=3*sum(multiplicity[v]*table[v] for v in matter)+sum(multiplicity[v]*table[v] for v in ("Hu","Hd"))
        y2=3*sum(multiplicity[v]*table[v]*Y[v]**2 for v in matter)+sum(multiplicity[v]*table[v]*Y[v]**2 for v in ("Hu","Hd"))
        zy2=3*sum(multiplicity[v]*table[v]**2*Y[v] for v in matter)+sum(multiplicity[v]*table[v]**2*Y[v] for v in ("Hu","Hd"))
        return {"2T_SU3":a3,"2T_SU2":a2,"gravity":grav,"U1Y2Z":y2,"U1YZ2":zy2,"Z3":cubic(table)}
    p=anomalies(Q);x=anomalies(X)
    assert p["2T_SU3"]==18 and p["2T_SU2"]==18 and p["gravity"]==102
    # Necessary modular congruences (not sufficient for a valid gauged
    # discrete symmetry, even with family-universal spectrum).
    assert all(v%3==0 for v in p.values())
    assert all(v%3==0 for v in x.values())
    # Z3 alone fails to forbid Q L D and L L E: both charges zero.
    bad={"QLDc":["Q","L","Dc"],"LLEc":["L","L","Ec"],"QQQL":["Q","Q","Q","L"],"UcDcDc":["Uc","Dc","Dc"]}
    op={}
    for name,fields in bad.items():
        p6=sum(Q[v] for v in fields)%6;z3=sum(X[v] for v in fields)%3
        op[name]={"P6":p6,"X3":z3,"P6_mod2":p6%2}
    assert op["QLDc"]["P6"]==3 and op["QLDc"]["X3"]==0
    assert op["LLEc"]["P6"]==3 and op["LLEc"]["X3"]==0
    return {"fields":list(Q),"P6_charges":Q,"X3_charges":X,"P6_anomaly_integer_necessary_ledgers":p,
            "X3_anomaly_integer_necessary_ledgers":x,
            "P6_mod3_checks":{name:val%3 for name,val in p.items()},
            "X3_mod3_checks":{name:val%3 for name,val in x.items()},
            "dangerous_operators":op,
            "physical_gauged_Z6_remnant_constructed":False,
            "anomaly_boundary":"integer necessary checks only; no Green-Schwarz, thresholds, heavy exotics, discrete instanton or UV charges verified"}

def polar_alternating_radical():
    pts,_=projective_points_and_lines()
    polar=sorted(v for v in pts if v[3]==0)
    idx={v:i for i,v in enumerate(polar)}
    p0=idx[(1,0,0,0)]
    e=np.zeros(13,dtype=np.int64);e[p0]=1
    u=np.ones(13,dtype=np.int64)
    M=(np.outer(u,e)-np.outer(e,u))%3
    assert np.array_equal(M.T%3,(-M)%3)
    rank=rref_rank(M)
    assert rank==2
    B=np.zeros((13,12),dtype=np.int64)
    for col,i in enumerate(k for k in range(13) if k!=p0):
        B[i,col]=1;B[p0,col]=2
    assert np.count_nonzero((B.T@M@B)%3)==0
    assert rref_rank(B)==12
    # Fixed P0 and all-ones vector ensure invariance under ANY
    # projective point stabilizer, not just a five-generator subgroup.
    for g in [um(1,0,0),um(0,1,0)]:
        permutation=[idx[canon(g@np.array(v))] for v in polar]
        assert np.array_equal(M[np.ix_(permutation,permutation)],M)
    return {"polar_points":13,
            "explicit_stabilizer_invariant_alt_form_rank":rank,
            "alt_form_radical_dimension":13-rank,
            "augmentation_restriction_rank":rref_rank((B.T@M@B)%3),
            "canonical_alternating_form":"ones wedge indicator_of_fixed_anchor",
            "12D_non_degenerate_phase_space_from_13D_permutation_module":False,
            "2D_symplectic_quotient_action":"trivial as the two defining covectors (sum, anchor coordinate) are invariant; not the H27 address symplectic action"}

def finite_point_sieve(prime=11):
    prior=json.loads((ROOT/"data"/"w33_20261008_h27_h13_five_frontiers.json").read_text())["flavor_polynomial_candidate"]
    terms=[(int(coef),tuple(qq)) for coef,orb in zip(prior["coefficients"],prior["degree_vectors_in_each_orbit"]) for qq in orb]
    # 16 patch enumeration with all (Fp)^4 affine coordinates.
    # At each projective position (1,k) or (0,1). All partials computed
    # in the chart where the fixed homogeneous coordinate is 1.
    n=0;zeros=0;sing=0;witness=[]
    for idxs in itertools.product(range(prime+1),repeat=4):
        xy=[(1,k) if k<prime else (0,1) for k in idxs]
        use=[0 if k<prime else 1 for k in idxs]
        x=[b if use[i]==0 else a for i,(a,b) in enumerate(xy)]
        F=0;grad=[0]*4
        for c,ds in terms:
            power=[ds[i] if use[i]==0 else 2-ds[i] for i in range(4)]
            term=[pow(x[i],power[i],prime) for i in range(4)]
            prod=c
            for t in term:prod*=t
            F=(F+prod)%prime
            for i in range(4):
                if power[i]==0:continue
                g=c*power[i]*pow(x[i],power[i]-1,prime)
                for j in range(4):
                    if i!=j:g*=term[j]
                grad[i]=(grad[i]+g)%prime
        n+=1
        if F==0:
            zeros+=1
            if not any(grad):
                sing+=1
                if len(witness)<5:witness.append(list(idxs))
    assert n==(prime+1)**4
    return {"p":prime,"ambient_rational_points":n,"hypersurface_Fp_points":zeros,
            "singular_Fp_rational_points":sing,"singular_witnesses":witness,
            "geometric_smooth_mod_p_proven":False,
            "complex_smoothness_proven":False,
            "logic":"No Fp-rational Jacobian zero only tests rational points; Fpbar singularities still possible"}

def build():
    return {"discrete_P6":charge_ledger(),"polar13":polar_alternating_radical(),"tetraquadric_F11":finite_point_sieve(11),"tetraquadric_F13":finite_point_sieve(13)}
if __name__=="__main__":
    x=build()
    OUT.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n",encoding="utf8")
    for k,v in x.items():print(k,json.dumps(v),flush=True)
    print("GUARDS_PASS",flush=True)
