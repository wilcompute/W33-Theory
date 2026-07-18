#!/usr/bin/env python3
"""Pass 454: q=7 central-Fourier census falsifies a universal quadratic atlas."""
from __future__ import annotations
import argparse,json,random
from collections import Counter
from pathlib import Path
import numpy as np
import sympy as sp
from sympy.polys.numberfields import round_two

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass454_q7_field_falsifier.json'
Q=7

def setup():
    q=Q;vecs=[(a,b) for a in range(q) for b in range(q) if (a,b)!=(0,0)]
    pairs=[];used=set()
    for v in vecs:
        nv=(-v[0]%q,-v[1]%q);key=tuple(sorted((v,nv)))
        if key not in used:used.add(key);pairs.append(key)
    ab=[(a,b) for a in range(q) for b in range(q)];idx={v:i for i,v in enumerate(ab)};omega=np.exp(2j*np.pi/q)
    def block(offsets,t):
        f={}
        for (v,nv),c in zip(pairs,offsets):f[v]=c;f[nv]=-c%q
        M=np.zeros((q*q,q*q),complex)
        for i,(a,b) in enumerate(ab):
            for (x,y),z in f.items():M[i,idx[((a+x)%q,(b+y)%q)]]=omega**((t*(z-a*y+x*b))%q)
        return M
    return pairs,block

def quadratic_kernels(values):
    vals=sorted(set(np.round(values,8)));irr=[v for v in vals if abs(v-round(v))>1e-5];out=set();used=set()
    for i,a in enumerate(irr):
        if i in used:continue
        for j in range(i+1,len(irr)):
            if j in used:continue
            b=irr[j];tr=a+b;nm=a*b
            if abs(tr-round(tr))<1e-5 and abs(nm-round(nm))<1e-5:
                d=round(tr)**2-4*round(nm)
                if d>0:
                    ker=1
                    for p,e in sp.factorint(d).items():
                        if e%2:ker*=p
                    out.add(int(ker))
                used|={i,j};break
    return out

def build_payload():
    pairs,block=setup();r=random.Random(454);N=80
    spectra=Counter();quadratic=Counter();field_discs=Counter();maxerr=0.0;examples=[]
    x=sp.symbols('x')
    for sample in range(N):
        offsets=tuple(r.randrange(Q) for _ in pairs);allvals=[]
        blocks={t:block(offsets,t) for t in range(1,Q)}
        for t in blocks:allvals.extend(np.linalg.eigvalsh(blocks[t]))
        spectra[tuple(np.round(sorted(allvals),6))]+=1
        for d in quadratic_kernels(allvals):quadratic[d]+=1
        traces=[float(np.trace(np.linalg.matrix_power(blocks[t],3)).real/Q) for t in (1,2,3)]
        coeff=np.poly(traces);icoeff=[int(round(v)) for v in coeff];maxerr=max(maxerr,float(max(abs(coeff-np.array(icoeff)))))
        P=sp.Poly(sum(icoeff[i]*x**(3-i) for i in range(4)),x)
        disc=int(round_two(P)[1]) if P.is_irreducible else 0;field_discs[disc]+=1
        if sample<3:examples.append({'sample':sample,'offsets':list(offsets),'trace_cubic':str(P.as_expr()),'field_discriminant':disc})
    checks={
      'sample_size_80':N==80,
      'all_spectra_distinct':len(spectra)==N and set(spectra.values())=={1},
      'no_quadratic_integer_trace_norm_pairs':not quadratic,
      'all_trace_cubics_irreducible_real_cyclotomic':field_discs==Counter({49:N}),
      'integer_polynomial_recovery_stable':maxerr<1e-5,
    }
    return {
      'schema':'w33.pass454.q7_field_falsifier.v1','status':'PASS' if all(checks.values()) else 'FAIL',
      'samples':N,'distinct_spectra':len(spectra),'collision_profile':{str(k):v for k,v in Counter(spectra.values()).items()},
      'quadratic_field_kernels':{str(k):v for k,v in quadratic.items()},
      'trace_cube_number_field_discriminants':{str(k):v for k,v in field_discs.items()},
      'examples':examples,'maximum_integer_recovery_error':maxerr,
      'headline':(
        'At q=7, 80 deterministic random sections give 80 distinct nonlinear spectra, zero quadratic '
        'integer-trace/norm pairs, and 80 irreducible trace-cubic fields of discriminant 49. The q=5 sqrt(5) '
        'atlas does not persist as a quadratic phenomenon; it upgrades exactly to Q(zeta_7)^+.'),
      'checks':checks,
    }
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=build_payload();text=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
    if a.check:
        if not a.output.exists() or a.output.read_text()!=text:raise SystemExit('Pass 454 certificate drift')
    else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(text)
    print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks'])}))
    return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
