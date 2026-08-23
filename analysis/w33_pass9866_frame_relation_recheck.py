import sys, numpy as np
sys.path.insert(0,'analysis')
from w33_pass7333_leech_d4_form import load_flat, invariant_gram
from pathlib import Path
from collections import Counter
SP='C:/Users/wiljd/AppData/Local/Temp/claude/c--Repos-Theory-of-Everything/4e98df7e-146b-472d-b3f7-862c4ae1e8b0/scratchpad/'
G0,_=invariant_gram(load_flat(Path('analysis/_co0_G.txt'))); G=-G0
I=np.eye(24,dtype=np.int64)
M=load_flat(Path('analysis/_co0_M8.txt'))[0]; N=I-M
V=np.load(SP+'minvec.npy')
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
V2,_=rref2(list((np.linalg.matrix_power(N,2)%2).T))
def inV2(x):
    v=np.array(x,dtype=np.int64)%2
    for b in V2:
        p=next(i for i,y in enumerate(b) if y)
        if v[p]: v=(v+b)%2
    return not v.any()
def frame_of(f):
    ipf=V@G@f; out=[f,-f]
    for k in np.flatnonzero(ipf==-4):
        g=f+2*V[k]
        if int(g@G@g)==8: out.append(g)
    for k in np.flatnonzero(ipf==4):
        g=-f+2*V[k]
        if int(g@G@g)==8: out.append(g)
    u={}
    for g in out: u[g.tobytes()]=g
    reps=[]
    for g in u.values():
        if not any(np.array_equal(g,-h) for h in reps): reps.append(g)
    return np.array(reps,dtype=np.int64)
reps=[]; seen=set()
for base in range(8):
    v=V[base]; ip=V@G@v
    for k in np.flatnonzero(ip==0):
        f=v+V[k]; key=(f%2).tobytes()
        if inV2(f%2) and key not in seen:
            seen.add(key); reps.append(f)
        if len(reps)>=34: break
    if len(reps)>=34: break
Fs=[frame_of(f) for f in reps]
def rel(a,b): return tuple(sorted(Counter(np.abs(Fs[a]@G@Fs[b].T).ravel().tolist()).items()))
pairs={}
for a in range(len(Fs)):
    for b in range(a+1,len(Fs)):
        pairs[(a,b)]=rel(a,b)
print('RE-TESTING "the relation depends only on the sum class" at',len(Fs),'classes')
bysum={}
for (a,b),r in pairs.items():
    s=((reps[a]+reps[b])%2).tobytes()
    bysum.setdefault(s,set()).add(r)
shared={s:rs for s,rs in bysum.items() if sum(1 for (a,b) in pairs if ((reps[a]+reps[b])%2).tobytes()==s)>1}
bad={s:rs for s,rs in bysum.items() if len(rs)>1}
print('  pairs:',len(pairs),'  distinct sum classes:',len(bysum))
print('  sum classes reached by more than one pair:',len(shared))
print('  sum classes with DISAGREEING relations:',len(bad))
print('  verdict:', 'CONSISTENT -- still a function of the sum class' if not bad
      else 'REFUTED at this sample size')
print()
print('  relation types seen:',len(set(pairs.values())))
for r,n in sorted(Counter(pairs.values()).items(),key=lambda t:-t[1]):
    print('   ',dict(r),' x',n)
