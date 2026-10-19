"""Round6 front4: Construct E8 Chevalley simple root generators directly
IN the repo's sl9 + Lambda3 + Lambda3* elementary 248-coordinate
basis, test integer E8 Cartan/Serre and root-system closure.
Root-generator recursion is subject to direct numerical rank checks.
"""
from __future__ import annotations
import collections,json,itertools
from pathlib import Path
import numpy as np
import w33_pass11681_e8_from_two_qutrits as E
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261019_round6_chevalley_realform.json"
ZERO=np.zeros(84,complex);Z9=np.zeros((9,9),complex)
Slbasis,Sl,Slp=E.e8_basis()
def Aij(i,j):
    M=np.zeros((9,9),complex);M[i,j]=1
    return M,ZERO,ZERO
def T(grade,tri,coeff=1.):
    v=np.zeros(84,complex);v[E.TI[tuple(tri)]]=coeff
    return (Z9,v,ZERO) if grade=="plus" else (Z9,ZERO,v)
def scal(a,x):return (a*x[0],a*x[1],a*x[2])
def minus(a,b):return (a[0]-b[0],a[1]-b[1],a[2]-b[2])
def norm(x):return float(np.linalg.norm(E._vec(x)))
def co(x):return np.concatenate([Slp@x[0].ravel(),x[1],x[2]])
e=[Aij(i,i+1) for i in range(7)]+[T("minus",(0,1,2))]
f=[Aij(i+1,i) for i in range(7)]+[T("plus",(0,1,2),-1)]
h=[E.bracket(ei,fi) for ei,fi in zip(e,f)]
def gr(root):
    out=[tuple(1 if j==i else 0 for j in range(8)) for i in range(8)]
    known=set(out);q=collections.deque(out)
    # Weyl orbit starting +/- simple roots
    while q:
        x=q.popleft()
        for i in range(8):
            b=sum(x[j]*root[i,j] for j in range(8))
            y=list(x);y[i]-=int(b);t=tuple(y)
            if t not in known:known.add(t);q.append(t)
    return known
def generated(roots,gens):
    start={tuple(1 if k==i else 0 for k in range(8)):g for i,g in enumerate(gens)}
    for r in sorted((x for x in roots if min(x)>=0),key=sum):
        if r in start:continue
        for i in range(8):
            parent=list(r);parent[i]-=1;parent=tuple(parent)
            if parent in start:
                v=E.bracket(gens[i],start[parent])
                if norm(v)>1e-8:
                    start[r]=v;break
        if r not in start:raise RuntimeError("root not generated "+str(r))
    return start
def run():
    K=np.zeros((8,8),dtype=int)
    errhf=0.;errhh=0.;errdiag=0.
    for i in range(8):
        for j in range(8):
            he=E.bracket(h[i],e[j]);hf=E.bracket(h[i],f[j])
            ei=co(e[j])
            K[i,j]=int(round((np.vdot(ei,co(he))/np.vdot(ei,ei)).real))
            errhf=max(errhf,norm(minus(he,scal(K[i,j],e[j]))),
                      norm(minus(hf,scal(-K[i,j],f[j]))))
            errhh=max(errhh,norm(E.bracket(h[i],h[j])))
            ef=E.bracket(e[i],f[j])
            errdiag=max(errdiag,norm(minus(ef,h[i] if i==j else E._zero())))
    det=int(round(np.linalg.det(K)))
    expected=np.eye(8,dtype=int)*2
    for i in range(6):expected[i,i+1]=expected[i+1,i]=-1
    expected[7,2]=expected[2,7]=-1
    serre=0.
    for i in range(8):
        for j in range(8):
            if i==j:continue
            for gs in (e,f):
                z=gs[j]
                for _ in range(1-K[i,j]):
                    z=E.bracket(gs[i],z)
                serre=max(serre,norm(z))
    roots=gr(K)
    positive=sorted((r for r in roots if min(r)>=0),key=sum)
    neg=sorted((r for r in roots if max(r)<=0),key=lambda v:sum(-z for z in v))
    ev=generated(roots,e);fv=generated(roots,f)
    mat=np.column_stack([co(x) for x in list(ev.values())+list(fv.values())+h])
    rank=int(np.linalg.matrix_rank(mat,tol=1e-8))
    # Check computed negative/eigen root vectors and Cartan form.
    charge_err=0.
    for (r,v) in list(ev.items())+list(fv.items()):
        for i in range(8):
            target=sum(r[j]*K[i,j] for j in range(8))
            # negative generators fv keys represent NEGATIVE root, so sign flips
            if r in fv and v is fv[r]:target=-target
            charge_err=max(charge_err,norm(minus(E.bracket(h[i],v),scal(target,v))))
    checks={"Cartan_exact_E8":np.array_equal(K,expected) and det==1,
         "normalized_simple_sl2":errdiag<1e-11,
         "cartan_commutes":errhh<1e-11,
         "h_e_and_h_f_roots":errhf<1e-11,
         "all_Serre_relations":serre<1e-11,
         "Weyl_roots_240":len(roots)==240 and len(positive)==len(neg)==120,
         "all_248_root_and_cartans_span":rank==248,
         "root_h_weights":charge_err<1e-8}
    out={"schema":"w33.round6.chevalley_serre_e8.v1",
      "construction":"Seven sl9 simple root e_i=E_(i,i+1), f_i=E_(i+1,i), i=0..6, plus 8th simple root e_7=dual Lambda3 basis (0,1,2), f_7=- Lambda3 basis (0,1,2). h_i=[e_i,f_i]. Coordinates in EXISTING repo Pass11681 sl9+Lambda3+Lambda3* elementary 248-basis.",
      "cartan_matrix":K.tolist(),"cartan_determinant":det,
      "rank_of_generated_root_vectors_and_h":rank,
      "positive_roots_generated":len(ev),"negative_roots_generated":len(fv),
      "Serre_max_error":serre,"sl2_max_error":errdiag,
      "Cartan_commutator_max_error":errhh,"Cartan_action_max_error":errhf,
      "root_weight_max_error":charge_err,
      "real_form":"All specified simple Chevalley generators have REAL coefficients in the underlying Pass11681 elementary basis; their real span yields SPLIT E8(8), with Cartan decomposition 128 noncompact and 120 compact generators, Killing signature +8. This does NOT realize E8(-24), whose maximal compact part has dim136 and Killing signature -24.",
      "prior_art":"The Pass11681 E8 bracket and Jacobi (gamma=-1) already exist. Chevalley Serre construction is standard, here executed as explicit generator coordinates and full 248 rank in that repo basis.",
      "checks":{k:bool(v) for k,v in checks.items()},"all_checks_pass":bool(all(checks.values()))}
    OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"checks":out["checks"],"rank":rank,"serre":serre,"hf":errhf,"weights":charge_err},indent=2))
    assert out["all_checks_pass"]
if __name__=="__main__":run()
