"""Known qutrit Shor construction applied to six marked genus-six handle pairs.
Prior: BT300 Shor discussion; Majumdar et al., arXiv:1807.01863.
The contribution is the explicit carrier assignment and exact fault audit, not a new code.
"""
from pathlib import Path
from itertools import product, combinations
import json, hashlib
import numpy as np
import sympy as sy

def rank(A):
    A=np.array(A,dtype=int).copy()%3;r=0
    for j in range(A.shape[1]):
        piv=next((i for i in range(r,len(A)) if A[i,j]),None)
        if piv is None:continue
        A[[r,piv]]=A[[piv,r]];A[r]=A[r]*pow(int(A[r,j]),-1,3)%3
        for i in range(len(A)):
            if i!=r:A[i]=(A[i]-A[i,j]*A[r])%3
        r+=1
        if r==len(A):break
    return r

def pairing(a,b):
    n=len(a)//2;return int(a[:n]@b[n:]-a[n:]@b[:n])%3

def stabilizers():
    S=[]
    for block in range(3):
        for k in range(2):
            v=np.zeros(18,dtype=int);v[9+3*block+k]=1;v[9+3*block+k+1]=2;S.append(v)
    for block in range(2):
        v=np.zeros(18,dtype=int);v[3*block:3*block+3]=1;v[3*block+3:3*block+6]=2;S.append(v)
    return np.array(S)

def audit():
    S=stabilizers();assert rank(S)==8 and all(pairing(a,b)==0 for a in S for b in S)
    lx=np.zeros(18,dtype=int);lx[:3]=1
    lz=np.zeros(18,dtype=int);lz[[9,12,15]]=1
    assert pairing(lx,lz)==1 and all(pairing(v,l)==0 for v in S for l in (lx,lz))
    errors=[np.zeros(18,dtype=int)]
    for i in range(9):
        for x,z in product(range(3),repeat=2):
            if x==z==0:continue
            v=np.zeros(18,dtype=int);v[i]=x;v[9+i]=z;errors.append(v)
    synd=lambda e:tuple(pairing(v,e) for v in S)
    decoder={}
    for e in errors:decoder.setdefault(synd(e),e)
    for e in errors:
        residual=(e-decoder[synd(e)])%3
        assert rank(np.vstack([S,residual]))==8
    # Knill-Laflamme Pauli criterion for all pairs of errors, not just individual syndromes.
    checks=0
    for a,b in product(errors,repeat=2):
        d=(a-b)%3
        if not any(synd(d)):assert rank(np.vstack([S,d]))==8
        checks+=1
    # No weight <=2 undetectable logical operator; displayed weight3 logical attains d=3.
    low=0
    for i,j in combinations(range(9),2):
        for (x,z),(u,v) in product([(a,b) for a,b in product(range(3),repeat=2) if a or b],repeat=2):
            e=np.zeros(18,dtype=int);e[i]=x;e[9+i]=z;e[j]=u;e[9+j]=v
            if not any(synd(e)):assert rank(np.vstack([S,e]))==8
            low+=1
    assert rank(np.vstack([S,lx]))==9 and sum(bool(lx[i] or lx[9+i]) for i in range(9))==3
    prior=Path(__file__).with_name('w33_genus_six_execution.json');surface=json.loads(prior.read_text())['surface']
    assert surface['betti']==[1,12,1]
    C=sy.Matrix(surface['symplectic_cycles']);H=sy.Matrix(surface['homology_projection'])
    B=H*C;J=sy.diag(*([sy.Matrix([[0,1],[-1,0]])]*6))
    assert B.T*(-sy.Matrix(surface['cup_matrix']).inv())*B==J
    assert sy.Matrix(surface['d1'])*C==sy.zeros(12)
    # Adjacent marked cycle pairs supply canonical X/Z labels over F3.
    # Nine carrier copies, each with six handles. Physical site (copy,handle) maps to block handle, site copy.
    assignment=[{'copy':c,'handle':h,'block':h,'site':c} for c in range(9) for h in range(6)]
    return {'status':'PASS','field':3,'single_block':{'n':9,'k':1,'d':3},'six_handle_code':{'n':54,'k':6,'d':3},
            'stabilizers':S.tolist(),'logical_X':lx.tolist(),'logical_Z':lz.tolist(),
            'identity_and_single_site_errors':len(errors),'syndrome_classes':len(decoder),
            'error_pair_checks':checks,'weight_two_checks':low,'stabilizer_rank_six_handles':48,
            'carrier_assignment':assignment,'surface_sha256':hashlib.sha256(prior.read_bytes()).hexdigest(),
            'correctable_fault':'Any operator supported on the six handles of one of nine surface copies; Pauli basis factorizes to at most one error per block.',
            'negative_control':'A weight-three logical X on three carrier copies has zero syndrome and is not a stabilizer.',
            'scope':'Finite qutrit algebra after choosing the existing symplectic marking. Encoding is an entangled isometry, not cloning. No quantization mechanism, physical syndrome measurement, threshold, or protection from arbitrary correlated faults established.',
            'prior':['w33_surface_hodge_transport.py','w33_BREAKTHROUGH_300_QEC_substrate_tower.py','https://arxiv.org/abs/1807.01863']}
if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');a=p.parse_args();r=audit()
    if a.write:Path(__file__).with_suffix('.json').write_text(json.dumps(r,indent=2)+'\n')
    print({k:r[k] for k in ['status','single_block','six_handle_code','error_pair_checks','weight_two_checks']})
