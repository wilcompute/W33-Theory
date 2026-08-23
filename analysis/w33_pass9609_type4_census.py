import sys, numpy as np, itertools
sys.path.insert(0,'analysis')
from w33_pass7333_leech_d4_form import load_flat, invariant_gram
from pathlib import Path
SP='C:/Users/wiljd/AppData/Local/Temp/claude/c--Repos-Theory-of-Everything/4e98df7e-146b-472d-b3f7-862c4ae1e8b0/scratchpad/'
G0,_=invariant_gram(load_flat(Path('analysis/_co0_G.txt')))
G=-G0
I=np.eye(24,dtype=np.int64)
M=load_flat(Path('analysis/_co0_M8.txt'))[0]
N=I-M
V=np.load(SP+'minvec.npy')
type4=set((v%2).tobytes() for v in V)
print('type-4 classes:',len(type4))
def rref2(rows):
    R=[np.array(r,dtype=np.int64)%2 for r in rows]; piv=[];r=0
    for c in range(24):
        sel=next((i for i in range(r,len(R)) if R[i][c]),None)
        if sel is None: continue
        R[r],R[sel]=R[sel],R[r]
        for i in range(len(R)):
            if i!=r and R[i][c]: R[i]=(R[i]+R[r])%2
        piv.append(c);r+=1
    return [R[i] for i in range(r)],piv
def colspace(A): return rref2(list((np.array(A,dtype=np.int64)%2).T))[0]
Vs={j:colspace(np.linalg.matrix_power(N,j)) for j in (1,2,3)}
print()
print('HOW MANY MINIMAL-VECTOR (type-4) CLASSES LIE IN EACH FILTRATION LEVEL?')
print('  This is a COORDINATE-FREE weight invariant: it needs no basis of Leech/2Leech,')
print('  only the classes themselves.\n')
print(f"   {'level':>6s} {'dim':>4s} {'nonzero classes':>16s} {'type-4 among them':>18s} {'expected if random':>19s}")
tot_sing=8390655
res={}
for j in (3,2,1):
    B=Vs[j]; d=len(B); nz=2**d-1
    cnt=0
    for coef in itertools.product([0,1],repeat=d):
        if not any(coef): continue
        v=np.zeros(24,dtype=np.int64)
        for c,b in zip(coef,B):
            if c: v=(v+b)%2
        if v.tobytes() in type4: cnt+=1
    exp=nz*98280/ (2**24-1)
    res[j]=(d,nz,cnt,exp)
    print(f"   {('V_%d'%j):>6s} {d:4d} {nz:16d} {cnt:18d} {exp:19.1f}")
print()
d,nz,cnt,exp = res[2]
print(f'  V_2 (the Type II code) contains {cnt} minimal-vector classes out of {nz}.')
print(f'  A random 12-space would hold about {exp:.0f}.  Ratio to random: {cnt/exp:.2f}')
print()
print('  In coding terms this is the count of MINIMUM-WEIGHT words of the Type II code,')
print('  read through the Leech type function instead of through coordinates.')
