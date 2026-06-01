from collections import Counter, defaultdict
from itertools import combinations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'PART_MMCCCLXXIV_Q4_RM13_BRIDGE_results.json'

def bits(n,w): return tuple((n>>i)&1 for i in reversed(range(w)))
def ix(x):
    n=0
    for b in x: n=(n<<1)|b
    return n
def add(a,b): return tuple(x^y for x,y in zip(a,b))
def wt(x): return sum(x)
def supp(x): return tuple(i for i,b in enumerate(x) if b)
def comp(m): return tuple(1^b for b in m)
def pair(m): return tuple(sorted((m,comp(m)), key=ix))

def basis():
    d=[bits(i,3) for i in range(8)]
    x1=tuple(x[0] for x in d); x2=tuple(x[1] for x in d); x3=tuple(x[2] for x in d)
    p=tuple(1^x[0]^x[1]^x[2] for x in d)
    assert add(add(x1,x2),add(x3,p)) == (1,)*8
    return [x1,x2,x3,p]

def enc(m,B):
    y=(0,)*8
    for b,row in zip(m,B):
        if b: y=add(y,row)
    return y

def q4_edges(V): return [(a,b) for a,b in combinations(V,2) if wt(add(a,b))==1]

def fano_lines(A):
    L=set()
    for a,b in combinations(range(1,8),2):
        c=A.index(pair(add(A[a][0],A[b][0])))
        if c not in (0,a,b): L.add(tuple(sorted((a,b,c))))
    return sorted(L)

def main():
    B=basis(); V=[bits(i,4) for i in range(16)]; C={m:enc(m,B) for m in V}
    W=sorted(C.values(),key=ix); A=sorted({pair(m) for m in V},key=lambda z:ix(z[0]))
    E=q4_edges(V); idx={m:i for i,a in enumerate(A) for m in a}; QE=defaultdict(list)
    for a,b in E: QE[tuple(sorted((idx[a],idx[b])))].append((a,b))
    QE=dict(QE); even=[i for i,a in enumerate(A) if wt(a[0])%2==0]; odd=[i for i,a in enumerate(A) if wt(a[0])%2]
    K44={tuple(sorted((a,b))) for a in even for b in odd}; inc=[e for e in QE if 0 in e]; non=[e for e in QE if 0 not in e]
    S=[[supp(C[m]) for m in a] for a in A]; L=fano_lines(A)
    deg=Counter(x for l in L for x in l); pl=Counter(tuple(sorted(p)) for l in L for p in combinations(l,2))
    blocks=[supp(w) for w in W if wt(w)==4]; tri=Counter(t for B4 in blocks for t in combinations(B4,3))
    checks={
      'sixteen_words':len(set(W))==16,
      'weight_profile':dict(Counter(map(wt,W)))=={0:1,4:14,8:1},
      'distance_four':min(wt(add(a,b)) for a,b in combinations(W,2))==4,
      'complements':all(add(C[m],C[comp(m)])==(1,)*8 for m in V),
      'one_plus_seven_axes':len(A)==8 and set(S[0])=={(),tuple(range(8))},
      'seven_44_axes':all(sorted(map(len,S[i]))==[4,4] for i in range(1,8)),
      'q4_counts':len(V)==16 and len(E)==32,
      'quotient_counts':len(QE)==16 and all(len(v)==2 for v in QE.values()),
      'k44':set(QE)==K44 and len(even)==len(odd)==4,
      'tomo_vector':(len(inc),len(non),len(QE),len(A))==(4,12,16,8),
      'tomo_sum':len(inc)+len(non)+len(QE)+len(A)==40,
      'fano':len(L)==7 and set(deg.values())=={3} and len(pl)==21 and set(pl.values())=={1},
      'sqs8':len(tri)==56 and set(tri.values())=={1},
    }
    assert all(checks.values()), checks
    R={'part':'MMCCCLXXIV','theorem':'Q4/RM13 tomotope bridge','weight_enumerator':dict(Counter(map(wt,W))),
       'q4_quotient':{'vertices':16,'edges':32,'axes':8,'quotient_edges':16,'is_K44':set(QE)==K44},
       'tomotope':{'V':len(inc),'E':len(non),'F':len(QE),'C':len(A),'sum':40},
       'fano_lines':L,'flag_identity':'16*12=24+168=192','checks':checks,'n_verified':sum(checks.values()),'n_checks':len(checks)}
    OUT.write_text(json.dumps(R,indent=2,sort_keys=True)+'\n')
    return R
if __name__=='__main__':
    r=main(); print(r['part'], r['theorem']); print('checks', r['n_verified'], '/', r['n_checks']); print(r['tomotope'])
