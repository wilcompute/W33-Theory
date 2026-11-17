"""Conditional finite Heisenberg quantization of M/IIB discrete winding labels.

The real M/IIB circle bundle has pi1=Z_g and the M C-field flat
translation subgroup Z_g^2. An optional nondegenerate projective
2-cocycle extends that quotient to H_g of order g^3:
 (a,b,c)*(a',b',c')=(a+a', b+b', c+c'+b*a') mod g.
This is a mathematical quantization model. The actual physical C-field
Berry/Wess-Zumino cocycle has NOT been derived.

Existing repo script w33_pass5727_5730_torsion_family_heisenberg.py
already constructs H27. This pass tests a new flux-indexed
topological interface, CRT factorization and its near-equal collapse.
"""
import itertools,json,math,cmath
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261116_M_IIB_flux_Heisenberg_CRT.json"

def mul(v,w,g):
    a,b,c=v;A,B,C=w
    return ((a+A)%g,(b+B)%g,(c+C+b*A)%g)

def inv(v,g):
    a,b,c=v
    return ((-a)%g,(-b)%g,(-c+a*b)%g)

def comm(v,w,g):
    return mul(mul(mul(v,w,g),inv(v,g),g),inv(w,g),g)

def rho(g):
    z=cmath.exp(2j*math.pi/g)
    X=np.roll(np.eye(g,dtype=complex),1,axis=0)
    Z=np.diag([z**j for j in range(g)])
    return X,Z,z

def rep(v,g,X,Z,z):
    a,b,c=v
    return z**c*np.linalg.matrix_power(X,a)@np.linalg.matrix_power(Z,b)

def group_certificate(g):
    if g<1:raise ValueError("g>=1")
    elements=list(itertools.product(range(g),repeat=3))
    e=(0,0,0)
    assert all(mul(v,inv(v,g),g)==e for v in elements)
    # Associativity is algebraic in this biadditive 2-cocycle:
    # b a' + (b+b')a'' = b'a'' + b(a'+a'').
    for x in range(g):
        for y in range(g):
            for z in range(g):
                assert ((x*y)+(x+y)*z-(y*z)-x*(y+z))%g==0
    p=(1%g,0,0);q=(0,1%g,0)
    assert comm(p,q,g)==(0,0,(-1)%g)
    center=[v for v in elements if comm(v,p,g)==e and comm(v,q,g)==e]
    assert center==[(0,0,c) for c in range(g)]
    return {"g":g,"group_order":g**3,"center_order":g,"quotient_order":g*g,
        "commutator_of_charge_vectors":"(0,0,b*a_prime-b_prime*a) modulo g",
        "nonabelian":g>1}

def verify_qutrit():
    g=3;X,Z,z=rho(g)
    el=list(itertools.product(range(3),repeat=3))
    for v in el:
        for w in el:
            lhs=rep(mul(v,w,g),g,X,Z,z)
            rhs=rep(v,g,X,Z,z)@rep(w,g,X,Z,z)
            assert np.max(np.abs(lhs-rhs))<1e-11
    F=np.array([[z**(i*j) for j in range(3)] for i in range(3)],complex)/math.sqrt(3)
    P=np.diag([1,1,z])
    assert np.linalg.norm(F@X@F.conj().T-Z)<1e-11
    assert np.linalg.norm(F@Z@F.conj().T-np.linalg.matrix_power(X,2))<1e-11
    assert np.linalg.norm(P@X@P.conj().T-X@Z)<1e-11
    return {"g":3,"Schrodinger_dimension":3,
            "matrix_group_order":27,
            "Fourier_and_phase_Clifford_checks":True,
            "existing_repo_comparison":"The H27 finite Clifford algebra itself already appears in w33_pass5727_5730_torsion_family_heisenberg.py."}

def crt_certificate(g,h):
    if math.gcd(g,h)!=1:raise ValueError("coprime CRT factors only")
    N=g*h
    for v,w in itertools.product(itertools.product(range(N),repeat=3),repeat=2):
        lhs=mul(v,w,N)
        a=mul(tuple(x%g for x in v),tuple(x%g for x in w),g)
        b=mul(tuple(x%h for x in v),tuple(x%h for x in w),h)
        assert tuple(x%g for x in lhs)==a and tuple(x%h for x in lhs)==b
    return {"g":g,"h":h,"H_gh_order":N**3,
            "CRT_group_isomorphism":f"H_{N} is H_{g} x H_{h}",
            "qutrit_factor_appears":g==3 or h==3}

def topology_sequence(N):
    if N<2:raise ValueError("N>=2")
    ge=math.gcd(N,N);gn=math.gcd(N+1,N)
    return {"equal_charge_pair":[N,N],"equal_g":ge,
            "equal_candidate_quantized_space_dimension":ge,
            "equal_candidate_H_group_order":ge**3,
            "near_equal_charge_pair":[N+1,N],"near_equal_g":gn,
            "near_equal_candidate_H_group_order":1,
            "warning":"Topological torsion and a chosen projective quantization may disappear although actual eleven-dimensional propagating KK modes vary smoothly."}

def verify():
    rows=[group_certificate(g) for g in (1,2,3,4,6,9)]
    q=verify_qutrit()
    c=crt_certificate(2,3)
    assert rows[2]["group_order"]==27
    assert rows[-1]["center_order"]==9
    assert rows[-1]["group_order"]==729
    topo=[topology_sequence(N) for N in (2,3,6,9,10,100)]
    return {"status":"PASS_FLUX_INDEXED_HEISENBERG_CANDIDATE_AND_CRT_FALSIFIER",
            "mathematical_model_only":True,
            "not_proven_physically":"Actual flux C-field translation operators' projective commutator and their overlap with IIB winding Hilbert space have not been computed.",
            "checks":rows,"qutrit":q,"CRT_example":c,
            "H9_not_H3_times_H3":"H9 center has exponent 9 whereas center of H3 x H3 has exponent 3.",
            "quantized_flux_topology_contrast":topo}
if __name__=="__main__":
    o=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(o,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(o["status"],o["CRT_example"])
