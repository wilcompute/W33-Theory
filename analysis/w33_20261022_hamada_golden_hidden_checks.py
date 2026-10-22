#!/usr/bin/env python3
"""Projective line-check incompleteness for Pascal symplectic codes.

The CSS code from B=J-I-A of W(3,q) has exact distance q+1, but
the *sparse ambient projective-line checks* need not span C_B^perp.
At q=4 they span only rank61 of dimension69; at q=8, rank401 of 521.
Hamada's known p-rank transfer yields a GOLDEN-ratio eigenvalue pair
5±sqrt5 in characteristic two. Neither this known incidence formula
nor the general code geometry is claimed novel in mathematical literature.
"""
from __future__ import annotations
import itertools,json,math
from pathlib import Path
import numpy as np
from analysis.w33_20261022_six_algebra_optics_frontiers import field,rank_modp

def polynomial_coeffs(p):
    a=[1]
    for _ in range(4):
        z=[0]*(len(a)+p-1)
        for i,x in enumerate(a):
            for j in range(p):z[i+j]+=x
        a=z
    return a

def hamada_transfer(p):
    c=polynomial_coeffs(p)
    return np.array([[c[p*i-j] if p*i-j>=0 else 0 for j in (1,2)]
                     for i in (1,2)],dtype=np.int64)

def exact_trace_power(M,t):
    a=np.eye(2,dtype=object)
    b=np.asarray(M,dtype=object)
    for _ in range(t):a=a@b
    return int(a.trace())

def projective_points(q):
    return [(0,)*i+(1,)+v for i in range(4)
            for v in itertools.product(range(q),repeat=3-i)]

def projective_lines(q,add,mul):
    P=projective_points(q)
    index={p:i for i,p in enumerate(P)}
    lines=[]
    for pivot1,pivot2 in itertools.combinations(range(4),2):
        f1=[i for i in range(pivot1+1,4) if i!=pivot2]
        f2=[i for i in range(pivot2+1,4)]
        for coeffs in itertools.product(range(q),repeat=len(f1)+len(f2)):
            a=[0]*4;b=[0]*4
            a[pivot1]=1;b[pivot2]=1
            for i,c in zip(f1,coeffs):a[i]=c
            for i,c in zip(f2,coeffs[len(f1):]):b[i]=c
            line=[index[tuple(b)]]
            for c in range(q):
                line.append(index[tuple(add[a[i],mul[c,b[i]]] for i in range(4))])
            assert len(line)==q+1 and len(set(line))==q+1
            lines.append(tuple(sorted(line)))
    assert len(lines)==(q*q+1)*(q*q+q+1)
    assert len(set(lines))==len(lines)
    return lines,len(P)

def rank_binary_line_masks(lines):
    piv={}
    for line in lines:
        x=sum(1<<j for j in line)
        while x:
            b=x.bit_length()-1
            if b in piv:x^=piv[b]
            else:piv[b]=x;break
    return len(piv)

def direct_rank(p,t,poly):
    q,add,mul,inv,neg=field(p,t,poly)
    lines,n=projective_lines(q,add,mul)
    if p==2:
        rank=rank_binary_line_masks(lines)
    else:
        H=np.zeros((len(lines),n),dtype=np.int64)
        for i,ln in enumerate(lines):H[i,ln]=1
        rank=rank_modp(H,p)
    return {"q":q,"p":p,"t":t,"points":n,"lines":len(lines),
            "direct_line_check_rank_Fp":rank}

def symbolic_case(p,t):
    q=p**t;v=(q+1)*(q*q+1)
    d=math.comb(p+2,3)**t
    M=hamada_transfer(p)
    rank_lines=1+exact_trace_power(M,t)
    rank_dual=v-d
    gap=rank_dual-rank_lines
    assert gap>=0
    return {"p":p,"t":t,"q":q,"points":v,
            "line_check_rank_Hamada":rank_lines,
            "dual_code_rank":rank_dual,
            "independent_checks_missing_from_lines":gap,
            "CSS":[v,v-2*d,q+1],
            "Hamada_matrix":M.tolist()}

def release():
    samples=[direct_rank(*x) for x in (
        (2,1,(0,1)),(3,1,(0,1)),
        (2,2,(1,1,1)),(5,1,(0,1)),
        (2,3,(1,1,0,1))
    )]
    for x in samples:
        b=symbolic_case(x["p"],x["t"])
        assert x["direct_line_check_rank_Fp"]==b["line_check_rank_Hamada"]
    extended=[symbolic_case(p,t) for p,t in
              [(2,1),(2,2),(2,3),(2,4),(3,1),(3,2),(5,1),(5,2)]]
    vals={(r["p"],r["t"]):r["independent_checks_missing_from_lines"] for r in extended}
    assert vals=={(2,1):0,(2,2):8,(2,3):120,(2,4):1312,
                  (3,1):0,(3,2):130,(5,1):0,(5,2):3400}
    # This closed all-p formula follows by substituting the explicit
    # multinomial Hamada 2x2 transfer and factoring the t=2 rank difference.
    square_field_gaps={}
    for p in (2,3,5,7,11):
        closed=p*p*(p-1)**2*(5*p*p+4*p+8)//18
        assert closed==symbolic_case(p,2)["independent_checks_missing_from_lines"]
        square_field_gaps[str(p)]=closed
    assert hamada_transfer(2).tolist()==[[4,1],[4,6]]
    assert hamada_transfer(3).tolist()==[[10,4],[16,19]]
    assert hamada_transfer(5).tolist()==[[35,20],[80,85]]
    # For p=2 the eigenvalues of [[4,1],[4,6]] are 5±sqrt5.
    # Since (8,2) majorizes (5+sqrt5,5-sqrt5), strict convexity of
    # x^t for t>1 gives hidden check gap strictly >0 for every t>=2.
    return {"status":"PASS_EXACT_HAMADA_AND_DIRECT_RANKS",
            "classical_RH_proved":False,
            "matrix_formula":"M_p[i,j] = [x^(p*(i+1)-(j+1))](1+x+...+x^(p-1))^4, i,j=0,1",
            "projective_line_rank_formula":"rank_Fp(H_point_line)=1+tr(M_p^t)",
            "noncollinearity_dual_rank_formula":"(q+1)(q²+1)-binomial(p+2,3)^t",
            "hidden_check_gap":"dim(C_B^perp)-rank(H_point_line)",
            "characteristic_two_eigenvalues":["5+sqrt5","5-sqrt5"],
            "characteristic_two_closed_gap":"8^t+2^t-(5+sqrt5)^t-(5-sqrt5)^t",
            "all_prime_square_field_gap":"p²(p-1)²(5p²+4p+8)/18",
            "square_field_gap_samples":square_field_gaps,
            "general_Hamada_transfer_entries":"[[p(p+1)(p+2)/6, p(p-1)(p+1)/6], [2p(p-1)(p+1)/3, p(2p²+1)/3]]",
            "binary_strict_gap_theorem":"For all t>=2, rank(line checks)<dim(C_B^perp); majorization and strict convexity prove positivity.",
            "local_recovery":"Each point lies on q²+q+1 projective lines, each giving a disjoint-by-helper repair group of q other symbols in the classical C_B code.",
            "direct_finite_field_rank_samples":samples,
            "exact_transfer_predictions":extended,
            "caveat":"Projective-line words are dual checks for the classical code but nontrivial logical operators for its CSS quantum code; they CANNOT be substituted for CSS stabilizers.",
            "prior_art":"Hamada's p-rank formula for point-line projective incidence (1968), see Eric Moorhouse p-Ranks Lecture 5; symplectic rank and W33 q=3 code preexisting."}

if __name__=="__main__":
    packet=release()
    out=Path(__file__).resolve().parents[1]/"data"/"w33_20261022_hamada_golden_hidden_checks.json"
    out.write_text(json.dumps(packet,indent=2,sort_keys=True)+"\n")
    print({str((v["p"],v["t"])):v["independent_checks_missing_from_lines"] for v in packet["exact_transfer_predictions"]})
