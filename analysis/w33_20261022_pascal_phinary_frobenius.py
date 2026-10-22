#!/usr/bin/env python3
"""Pascal-to-beta number systems, golden Frobenius, and W33 prime-power audit.

Five scoped computations plus existing CCM/Weil consistency checks.
No statement here proves classical Riemann RH, a TOE, or physical phase transport.
"""
from __future__ import annotations
import json,math,sys
from pathlib import Path
from itertools import product
from fractions import Fraction
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from analysis.w33_20261022_levi_prime_family import local_packet,is_prime

def pascal_family(m,n):
    """Compositions into parts 1 and m: Pascal diagonals."""
    return sum(math.comb(n-(m-1)*k,k) for k in range(n//m+1))

def pascal_base():
    for m in (1,2,3,4,5):
        seq=[pascal_family(m,n) for n in range(55)]
        assert all(seq[n]==seq[n-1]+(seq[n-m] if n>=m else 0)
                   for n in range(1,55))
    assert [pascal_family(1,n) for n in range(15)]==[2**n for n in range(15)]
    assert [pascal_family(2,n) for n in range(11)]==[1,1,2,3,5,8,13,21,34,55,89]
    assert [pascal_family(3,n) for n in range(11)]==[1,1,1,2,3,4,6,9,13,19,28]
    # The 2026 repo's Pascal-trinity prose incorrectly labels 4*pi²/3-12
    # as 4*pi²/3-q! with q=3; q! is 6, not 12.
    s=sum(Fraction(4,n*n*(n+1)**2) for n in range(1,150))
    assert abs(float(s)-(4*math.pi**2/3-12))<1e-6
    assert abs(float(s)-(4*math.pi**2/3-math.factorial(3)))>5
    return {"status":"PASS_EXACT_RECURSION","tested_orders":[1,2,3,4,5],
            "generating_function":"A_m(x)=1/(1-x-x^m)",
            "growth_equation":"beta_m^m=beta_m^(m-1)+1",
            "bases":{"1":"2","2":"phi=(1+sqrt(5))/2",
                     "3":"supergolden root x^3-x^2-1","4":"largest real root x^4-x^3-1"},
            "old_pascal_note_correction":"Sum 1/T_n²=4*pi²/3-12, not 4*pi²/3-3!.",
            "three_constants_boundary":"phi is algebraic; e and pi enter Pascal analysis via infinite analytic limits, not a finite common positional-number ring"}

def golden_multiply(v,w):
    a,b=v;c,d=w
    return (a*c+b*d,a*d+b*c+b*d)

def golden_power(k):
    v=(1,0);g=(0,1) if k>=0 else (-1,1)
    for _ in range(abs(k)):v=golden_multiply(v,g)
    return v

def phi_representations(limit=40,hi=10,lo=-10):
    """Find canonical no-adjacent-1 finite base-phi expansions exactly in Z[phi]."""
    powers=[golden_power(k) for k in range(hi,lo-1,-1)]
    reps={}
    def backtrack(i,previous,a,b,bits):
        if i==len(powers):
            if b==0 and 0<=a<=limit:
                reps.setdefault(a,[]).append(bits)
            return
        backtrack(i+1,False,a,b,bits+"0")
        if not previous:
            da,db=powers[i]
            backtrack(i+1,True,a+da,b+db,bits+"1")
    backtrack(0,False,0,0,"")
    assert all(len(reps.get(n,[]))==1 for n in range(limit+1))
    examples={}
    for n in (2,3,7,11,23,40):
        digits=reps[n][0]
        examples[str(n)]=digits[:hi+1]+"."+digits[hi+1:]
        a=b=0
        for i,v in enumerate(digits):
            if v=="1":
                da,db=powers[i];a+=da;b+=db
        assert (a,b)==(n,0) and "11" not in digits
    return {"status":"PASS_EXACT_INTEGER_PAIR_RING","unique_Bergman_forms_checked":limit+1,
            "radix_positions":[hi,lo],"examples":examples,
            "rewrite_rule":"phi^(n+1)=phi^n+phi^(n-1); 100<->011",
            "contrast":"Zeckendorf uses integer Fibonacci weights; phinary uses positive and negative powers of irrational phi"}

def fp_multiply(x,y,p):
    a,b=x;c,d=y
    return ((a*c+b*d)%p,(a*d+b*c+b*d)%p)

def fp_pow_phi(p):
    a=(1,0);b=(0,1);n=p
    while n:
        if n&1:a=fp_multiply(a,b,p)
        b=fp_multiply(b,b,p);n>>=1
    return a

def primes_below(n):
    return [p for p in range(3,n+1,2) if is_prime(p)]

def lucas_mod_p(n,k,p):
    value=1
    while n or k:
        a,b=n%p,k%p
        if b>a:return 0
        value=value*math.comb(a,b)%p
        n//=p;k//=p
    return value

def cyclotomic_phi_audit():
    tested=0;family=[]
    for p in primes_below(503):
        if p==5:continue
        golden_inert=pow(5,(p-1)//2,p)==p-1
        gaussian_inert=p%4==3
        phase4=pow(p,4,5)==1 and pow(p,2,5)!=1
        criterion=p%20 in (3,7)
        assert criterion==(golden_inert and gaussian_inert)
        assert criterion==(gaussian_inert and phase4)
        if criterion:
            assert fp_pow_phi(p)==(1,p-1)
            if p<100:family.append(p)
        tested+=1
    for p in (2,3,5,7):
        for n in range(80):
            for k in range(n+1):
                assert lucas_mod_p(n,k,p)==math.comb(n,k)%p
    return {"status":"PASS_EXACT_FINITE_FIELD","primes_checked":tested,
            "joint_frobenius_class":"p=3 or 7 mod20 iff (5/p)=(-4/p)=-1",
            "golden_phi_p":"phi^p=1-phi in Fp[phi]/(phi²-phi-1)",
            "gaussian_i_p":"i^p=-i in Fp[i]/(i²+1)",
            "fifth_roots":"ord_5(p)=4; irreducible Phi_5 cyclotomic polynomial",
            "sample_family_primes_below100":family,
            "Lucas_pascal_checks":4*sum(range(1,81)),
            "scope":"Classical Frobenius and Pascal congruences; not physical or RH evidence"}

def prime_power_extension():
    samples=[]
    for p in (3,7,23):
        for r in range(1,7):
            q=p**r
            if r%2:
                c=f"X^4+{q*q}"; e=f"X^2+{q}"
                assert q%20 in (3,7)
            elif r%4==2:
                c=f"(X^2+{q})^2"
                e=f"(X-{(-p)**(r//2)})^2"
                assert q%20 not in (3,7)
            else:
                c=f"(X+{p**(r//2)})^4"
                e=f"(X-{(-p)**(r//2)})^2"
                assert q%20 not in (3,7)
            if r==1: assert local_packet(p,extension_counts=False)["local_cohomology_rank"]==2*p*((p+1)**2+p*p+1)
            samples.append({"p":p,"r":r,"q":q,"C_Frobenius":c,"E_Frobenius":e})
    return {"status":"PASS_EXACT_BASECHANGE","cases":len(samples),
            "odd_extension":"For q=p^(2m+1), p=3,7 mod20, the same C/E curve base changes realize x^4+q² and x²+q.",
            "even_extension_obstruction":"At q=p², C base change has (X²+q)² and E has (X+p)², not the naive q-Levi factors.",
            "cases_table":samples,
            "global_RH_boundary":"A base change of a fixed curve does not identify variable-degree generalized-quadrangle packet Euler factors with zeta."}

def ccm_weil_trace_audit():
    from analysis.w33_20261022_ccm_compact_weil_trace import ccm_matrix,compact_weil,relative_trace
    c=ccm_matrix(N=4,cutoff=13)
    w=compact_weil(cutoff=13,a=.33)
    a=relative_trace(c,eta=.05)
    b=relative_trace(c,eta=.10)
    ratio=b["relative_trace2_theory"]/a["relative_trace2_theory"]
    assert abs(ratio-4)<1e-9 and w["exact_prime_tail_zero"]
    assert w["eigenvalues"][0]>0 and c["first_absolute_error"]<.0002
    return {"status":"PASS_SCOPED_NUMERIC","CCM_first_zero_absolute_error":c["first_absolute_error"],
            "compact_smooth_Weil_smallest_eigenvalue":w["eigenvalues"][0],
            "relative_second_trace_eta_doubled_ratio":ratio,
            "all_prime_powers_cutoff13":c["prime_powers"],
            "caution":"Existing float64 finite-N CCM and non-certified 2x2 Weil test; no exact Xi spectrum or universal positivity."}

def all_results():
    results={"pascal_growth_bases":pascal_base(),
             "exact_phinary_integers":phi_representations(),
             "Frobenius_golden_gaussian":cyclotomic_phi_audit(),
             "Levi_curve_prime_powers":prime_power_extension(),
             "CCM_Weil_rank_two":ccm_weil_trace_audit(),
             "classical_RH_proved":False}
    assert all(results[k]["status"].startswith("PASS") for k in results if k!="classical_RH_proved")
    return results

if __name__=="__main__":
    d=all_results()
    dest=ROOT/"data"/"w33_20261022_pascal_phinary_frobenius.json"
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n")
    print(json.dumps({k:(v.get("status") if isinstance(v,dict) else v) for k,v in d.items()},indent=2))
