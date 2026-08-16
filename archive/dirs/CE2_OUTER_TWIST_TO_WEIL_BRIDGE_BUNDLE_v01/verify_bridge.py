import os
from pathlib import Path
os.chdir(Path(__file__).resolve().parent)  # Pass 5548: JSONs opened by bare filename
\
import json, numpy as np, itertools, random
from collections import deque, defaultdict

def mat_mod3(M): return np.array(M,dtype=int)%3
def mat_mul(A,B): return (A@B)%3
def mat_inv(M):
    M=M.copy()%3
    n=M.shape[0]
    aug=np.concatenate([M, np.eye(n,dtype=int)%3], axis=1)%3
    r=0
    for c in range(n):
        piv=None
        for rr in range(r,n):
            if aug[rr,c]%3!=0:
                piv=rr; break
        if piv is None: raise ValueError("singular")
        if piv!=r: aug[[r,piv]]=aug[[piv,r]]
        pv=aug[r,c]%3
        inv_pv=1 if pv==1 else 2
        aug[r,:]=(aug[r,:]*inv_pv)%3
        for rr in range(n):
            if rr==r: continue
            factor=aug[rr,c]%3
            if factor!=0:
                aug[rr,:]=(aug[rr,:]-factor*aug[r,:])%3
        r+=1
    return aug[:,n:]%3

def mat_bytes(M): return bytes(int(x) for x in (M%3).reshape(-1).tolist())

def det2(A):
    return int((A[0,0]*A[1,1]-A[0,1]*A[1,0])%3)

# Load saved artifacts
Udat=json.load(open("heisenberg_U_generators.json"))
x=mat_mod3(Udat["x"])
y=mat_mod3(Udat["y"])
z=mat_mod3(Udat["z_center"])
mu=json.load(open("mu_recovery.json"))
outer=json.load(open("outer_twist_on_sl2_layer.json"))

# Basic Heisenberg checks
def commutator(A,B):
    return mat_mul(mat_mul(mat_mul(A,B), mat_inv(A)), mat_inv(B))

c=commutator(x,y)
assert mat_bytes(c)==mat_bytes(z) or mat_bytes(c)==mat_bytes(mat_mul(z,z))

# Check n5 determinant bit
A=np.array(outer["induced_GL2_on_U_over_Z"],dtype=int)%3
assert det2(A)==2
print("ALL CHECKS PASSED (structural): U is Heisenberg with center; outer twist induces det=-1 on U/Z.")
