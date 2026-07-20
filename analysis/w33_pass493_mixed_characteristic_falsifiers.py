#!/usr/bin/env python3
"""Pass 493: exact mixed-characteristic falsifiers for determinant depth.

The earlier size-only Hjelmslev guess predicts depth |P^1(R)| for every local
ring of odd residue characteristic.  Two exact mixed-characteristic witnesses
refute that extension:

* R = Z/9[x]/(3x, x^2-3), |R|=27, character order 9: depth 18, not 36.
* R = GR(9,2), |R|=81, character order 9: depth 24, not 90.

A nonlocal Frobenius control R=Z/9 x F_3 also attains depth 18.  All three
attained depths equal v_lambda(|R|).  Together with Z/p^n, this exposes a
competition between an arithmetic ramification budget and a projective-line
budget rather than a law depending on ring size alone.
"""
from __future__ import annotations
import argparse, itertools, json, math, random, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass493_mixed_characteristic_falsifiers.json"

class Cyc:
    def __init__(self, p: int, n: int):
        self.p, self.n, self.m = p, n, p**n
        self.pn1 = p ** (n - 1)
        self.deg = self.pn1 * (p - 1)
        self.red = [j * self.pn1 for j in range(p - 1)]
    def zero(self): return (0,) * self.deg
    def one(self): return (1,) + (0,) * (self.deg - 1)
    def rat(self, k): return (k,) + (0,) * (self.deg - 1)
    def canon(self, v):
        v = list(v) + [0] * max(0, self.deg - len(v))
        for k in range(len(v) - 1, self.deg - 1, -1):
            c = v[k]
            if c:
                v[k] = 0
                for j in self.red:
                    v[k - self.deg + j] -= c
        return tuple(v[:self.deg])
    def from_exp(self, e):
        e %= self.m
        v = [0] * self.m
        v[e] = 1
        return self.canon(v)
    def add(self, a, b): return tuple(x + y for x, y in zip(a, b))
    def sub(self, a, b): return tuple(x - y for x, y in zip(a, b))
    def smul(self, k, a): return tuple(k * x for x in a)
    def mul(self, a, b):
        acc = [0] * (2 * self.deg - 1)
        for i, x in enumerate(a):
            if x:
                for j, y in enumerate(b):
                    if y:
                        acc[i + j] += x * y
        return self.canon(acc)
    def sigma(self, a, x):
        acc = [0] * self.m
        for i, c in enumerate(x):
            if c:
                acc[(i * a) % self.m] += c
        return self.canon(acc)
    def norm(self, x):
        acc = self.one()
        for a in range(1, self.m):
            if a % self.p:
                acc = self.mul(acc, self.sigma(a, x))
        if any(acc[1:]):
            raise AssertionError("norm did not land in Z")
        return acc[0]
    def vlam(self, x):
        if not any(x): return 10**9
        n = abs(self.norm(x)); v = 0
        while n and n % self.p == 0:
            n //= self.p; v += 1
        return v

def exact_div(a, b, C):
    num = a
    for k in range(2, C.m):
        if k % C.p:
            num = C.mul(num, C.sigma(k, b))
    nb = C.norm(b)
    if nb == 0: raise ZeroDivisionError
    if any(c % nb for c in num): raise ArithmeticError("inexact Bareiss division")
    return tuple(c // nb for c in num)

def det_bareiss(M, C):
    n = len(M); A = [row[:] for row in M]; sign = 1; prev = C.one()
    for k in range(n - 1):
        if not any(A[k][k]):
            piv = next((i for i in range(k + 1, n) if any(A[i][k])), None)
            if piv is None: return C.zero()
            A[k], A[piv] = A[piv], A[k]; sign = -sign
        for i in range(k + 1, n):
            aik = A[i][k]
            for j in range(k + 1, n):
                num = C.sub(C.mul(A[i][j], A[k][k]), C.mul(aik, A[k][j]))
                A[i][j] = exact_div(num, prev, C)
            A[i][k] = C.zero()
        prev = A[k][k]
    d = A[-1][-1]
    return d if sign > 0 else tuple(-x for x in d)

class Zmod:
    def __init__(self, p, n):
        self.p, self.n, self.mod = p, n, p**n
        self.size = self.mod; self.char_order = self.mod
        self.name = f"Z/{self.mod}"
        self.elems = list(range(self.mod)); self.zero = 0; self.one = 1
    def add(self,a,b): return (a+b)%self.mod
    def neg(self,a): return (-a)%self.mod
    def mul(self,a,b): return (a*b)%self.mod
    def smul(self,n,a): return (n*a)%self.mod
    def chi_exp(self,a): return a

class Eisenstein27:
    """Z/9[x]/(3x,x^2-3), a length-three chain ring of order 27."""
    p=3; size=27; char_order=9; name="Z/9[x]/(3x,x^2-3)"
    elems=[(a,b) for a in range(9) for b in range(3)]
    zero=(0,0); one=(1,0); radical_size=9; projective_line_size=36
    @staticmethod
    def add(u,v): return ((u[0]+v[0])%9,(u[1]+v[1])%3)
    @staticmethod
    def neg(u): return ((-u[0])%9,(-u[1])%3)
    @staticmethod
    def mul(u,v):
        a,b=u; c,d=v
        return ((a*c+3*b*d)%9,(a*d+b*c)%3)
    @staticmethod
    def smul(n,u): return ((n*u[0])%9,(n*u[1])%3)
    @staticmethod
    def chi_exp(u): return u[0]%9

class GR9_2:
    """GR(9,2)=Z/9[u]/(u^2+1), trace character exp(2a)."""
    p=3; size=81; char_order=9; name="GR(9,2)"
    elems=[(a,b) for a in range(9) for b in range(9)]
    zero=(0,0); one=(1,0); radical_size=9; projective_line_size=90
    @staticmethod
    def add(u,v): return ((u[0]+v[0])%9,(u[1]+v[1])%9)
    @staticmethod
    def neg(u): return ((-u[0])%9,(-u[1])%9)
    @staticmethod
    def mul(u,v):
        a,b=u; c,d=v
        return ((a*c-b*d)%9,(a*d+b*c)%9)
    @staticmethod
    def smul(n,u): return ((n*u[0])%9,(n*u[1])%9)
    @staticmethod
    def chi_exp(u): return (2*u[0])%9

class ProductZ9F3:
    p=3; size=27; char_order=9; name="Z/9 x F_3"
    elems=[(a,b) for a in range(9) for b in range(3)]
    zero=(0,0); one=(1,1); projective_line_size=48
    @staticmethod
    def add(u,v): return ((u[0]+v[0])%9,(u[1]+v[1])%3)
    @staticmethod
    def neg(u): return ((-u[0])%9,(-u[1])%3)
    @staticmethod
    def mul(u,v): return ((u[0]*v[0])%9,(u[1]*v[1])%3)
    @staticmethod
    def smul(n,u): return ((n*u[0])%9,(n*u[1])%3)
    @staticmethod
    def chi_exp(u): return (u[0]+3*u[1])%9

class Heis:
    def __init__(self, R, C):
        self.R, self.C, self.q = R, C, R.size
        E = R.elems; self.idx = {e:i for i,e in enumerate(E)}
        vecs = [(a,b) for a in E for b in E if (a,b)!=(R.zero,R.zero)]
        pairs=[]; used=set()
        for v in vecs:
            nv=(R.neg(v[0]),R.neg(v[1])); key=tuple(sorted((v,nv)))
            if key not in used: used.add(key); pairs.append(key)
        self.pairs=pairs
    def full_sec(self, offs):
        f={}; R=self.R
        for (v,nv),c in zip(self.pairs,offs): f[v]=c; f[nv]=R.neg(c)
        return f
    def block(self, fsec):
        R,C,q=self.R,self.C,self.q; two=R.smul(2,R.one)
        B=[[C.zero() for _ in range(q)] for _ in range(q)]
        for (a,b),c in fsec.items():
            ab=R.mul(a,b)
            for xi,x in enumerate(R.elems):
                z=R.add(c,R.add(R.mul(two,R.mul(x,b)),ab))
                j=self.idx[R.add(x,a)]
                B[j][xi]=C.add(B[j][xi],C.from_exp(R.chi_exp(z)))
        return B

def generating_character_check(R):
    """For every nonzero a, the principal ideal aR is not inside ker(chi)."""
    return all(any(R.chi_exp(R.mul(a,r)) % R.char_order for r in R.elems)
               for a in R.elems if a != R.zero)

def witness(R, sections):
    C=Cyc(R.p, int(round(math.log(R.char_order,R.p)))); H=Heis(R,C); q=R.size
    t0=time.time(); flat=H.full_sec(tuple(R.zero for _ in H.pairs)); F=H.block(flat)
    detF=det_bareiss(F,C)
    formula=(q-1)**((q+1)//2)*(-(q+1))**((q-1)//2)
    out=[]
    for name, maker in sections:
        offs=maker(H)
        d=det_bareiss(H.block(H.full_sec(offs)),C)
        delta=C.sub(d,detF)
        out.append({"name":name,"depth":C.vlam(delta),"real":C.sigma(C.m-1,delta)==delta})
    s=int(round(math.log(q,R.p))); phi=(R.p-1)*R.p**(int(round(math.log(R.char_order,R.p)))-1)
    return {"ring":R.name,"size":q,"character_order":R.char_order,
            "additive_log_p_size":s,"v_lambda_size":s*phi,
            "projective_line_size":R.projective_line_size,
            "generating_character":generating_character_check(R),
            "flat_det_formula":not any(detF[1:]) and detF[0]==formula,
            "witnesses":out,"attained_depth":min(x["depth"] for x in out),
            "seconds":round(time.time()-t0,3)}

def single(c, idx=0):
    return lambda H: tuple(c if i==idx else H.R.zero for i in range(len(H.pairs)))

def main_payload(full=True):
    E=Eisenstein27(); P=ProductZ9F3(); G=GR9_2()
    rings=[
        witness(E,[('single_unit',single(E.one)),('single_x',single((0,1),1))]),
        witness(P,[('single_product_unit',single(P.one)),('single_Z9',single((1,0),1)),('single_F3',single((0,1),2))]),
    ]
    if full:
        rings.append(witness(G,[('single_unit',single(G.one))]))
    checks={}
    for r in rings:
        tag=r['ring'].replace('/','_').replace(' ','_')
        checks[tag+'_character_generating']=r['generating_character']
        checks[tag+'_flat_formula']=r['flat_det_formula']
        checks[tag+'_real_deltas']=all(w['real'] for w in r['witnesses'])
        checks[tag+'_arithmetic_budget_attained']=r['attained_depth']==r['v_lambda_size']
        checks[tag+'_size_only_Hjelmslev_refuted']=r['attained_depth']<r['projective_line_size']
    status='PASS' if all(checks.values()) else 'FAIL'
    return {"schema":"w33.pass493.mixed_characteristic_falsifiers.v1","status":status,
            "headline":"Mixed-characteristic exact witnesses refute a size-only Hjelmslev depth law.",
            "rings":rings,
            "result":"All tested order-9 mixed rings attain v_lambda(|R|), below |P^1(R)|.",
            "boundary":"Exact attained witnesses, not a proof of a universal minimum law.",
            "checks":checks}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--quick',action='store_true'); ap.add_argument('--check',action='store_true'); ap.add_argument('--output',type=Path,default=OUT); a=ap.parse_args()
    pl=main_payload(full=not a.quick); text=json.dumps(pl,sort_keys=True,separators=(',',':'))+'\n'
    if a.check:
        if not a.output.exists() or a.output.read_text()!=text: raise SystemExit('Pass 493 certificate drift')
    else:
        a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(text)
    print(json.dumps({'status':pl['status'],'checks':sum(pl['checks'].values()),'total':len(pl['checks'])}))
    return 0 if pl['status']=='PASS' else 1
if __name__=='__main__': raise SystemExit(main())
