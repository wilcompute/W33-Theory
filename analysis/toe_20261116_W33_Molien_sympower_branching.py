#!/usr/bin/env python3
"""Exact PSp4(3) Molien / character census for W33 40-mode bosonic powers.

Conjugation-free enumerate all 25,920 permutation group elements using
five independent symplectic transvections, carrying both 40-point and
27-cubic-line permutations. Exact integer characters of symmetric
powers follow from cycle index product ∏(1-t^cycle_length)^-1.

The 27-dimensional target permutation representation decomposes as
1+20+6. Compute Hom_G(Sym^d C40, 1/20/6) dimensions d=0..8.
"""
from collections import Counter,deque
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from toe_20261116_W33_symmetry_minimal_fourcopy import build_geometry,generators
OUT=ROOT/"data"/"toe_20261116_W33_sym_power_Molien_characters.json"
MAXD=9
def cycles(perm):
    seen=set();out=[]
    for i in range(len(perm)):
        if i in seen:continue
        p=i;length=0
        while p not in seen:
            seen.add(p);p=perm[p];length+=1
        out.append(length)
    return tuple(sorted(out))

def symchar(cyc,maxd=MAXD):
    dp=[1]+[0]*maxd
    for L in cyc:
        for d in range(L,maxd+1):dp[d]+=dp[d-L]
    return dp

def run():
    geometry=build_geometry()
    A=geometry[6]
    gens=generators(geometry)
    identity=(tuple(range(40)),tuple(range(27)))
    seen={identity}
    queue=deque([identity])
    hom=[[0,0,0,0] for d in range(MAXD+1)]
    classes=Counter()
    n=0
    while queue:
        pp,ll=queue.popleft();n+=1
        cyc=cycles(pp)
        coeffs=symchar(cyc)
        fixed=sum(i==ll[i] for i in range(27))
        atrace=sum(A[i][ll[i]] for i in range(27))
        chi6_num=3*fixed-3*atrace+27
        assert chi6_num%18==0
        chi6=chi6_num//18
        chi20=fixed-1-chi6
        assert -6<=chi6<=6 and -20<=chi20<=20
        classes[(cyc,chi6,chi20,fixed)]+=1
        for d,mul in enumerate(coeffs):
            hom[d][0]+=mul*fixed
            hom[d][1]+=mul
            hom[d][2]+=mul*chi20
            hom[d][3]+=mul*chi6
        for sp,sl in gens:
            nxt=(tuple(sp[x] for x in pp),tuple(sl[x] for x in ll))
            if nxt not in seen:
                seen.add(nxt);queue.append(nxt)
    assert n==25920 and len(seen)==n
    assert all(all(z%n==0 for z in row) for row in hom)
    dims=[dict(degree=d,Sym_power_dimension=__import__("math").comb(40+d-1,d) if d else 1,
               Hom_to_27=row[0]//n,Hom_to_uniform1=row[1]//n,
               Hom_to_Schlafli20=row[2]//n,Hom_to_Schlafli6=row[3]//n)
          for d,row in enumerate(hom)]
    assert all(a["Hom_to_27"]==a["Hom_to_uniform1"]+a["Hom_to_Schlafli20"]+a["Hom_to_Schlafli6"] for a in dims)
    assert [(x["Hom_to_27"],x["Hom_to_Schlafli6"]) for x in dims[:4]]==[(1,0),(1,0),(5,0),(19,0)]
    assert dims[4]["Hom_to_Schlafli6"]>0
    data={"status":"EXACT_PSP43_SYM_POWER_CHARACTER_MOLIEN_BRANCHING",
          "group_size":n,"mode_permutation_degree":40,"Schlafli_target_degree":27,
          "Schlafli_irrep_dimensions":[1,20,6],
          "symmetric_power_degrees":dims,
          "class_fingerprints":[{"cycle_partition":list(k[0]),"character6":k[1],"character20":k[2],
                                 "character27":k[3],"group_element_count":v}
                                for k,v in sorted(classes.items(),key=lambda kv:(kv[0][0],kv[0][1]))],
          "character_proof":"Each input multiset forms a permutation basis of Sym^d; trace_g(Sym^d)= coefficient [t^d] ∏_{cycles c of g}(1-t^|c|)^-1. Target Schläfli projectors: P1=J/27, P6=(3I-3A+J)/18 and P20=I-P1-P6, hence chi6=(3 fix(g)-3 sum_i A(i,g(i))+27)/18. Average each exact character product over all 25920 G elements.",
          "scope":"Full PSp4(3)-equivariant complex-linear hom dimensions for symmetric boson powers, NOT minimal degree for LOQC with ancillas, adaptivity, different target representations or symmetry-breaking states."}
    OUT.write_text(json.dumps(data,indent=2)+"\n")
    return data
if __name__=="__main__":
    d=run()
    print("PASS",d["status"], [(x["degree"],x["Hom_to_27"],x["Hom_to_Schlafli6"]) for x in d["symmetric_power_degrees"]],flush=True)
