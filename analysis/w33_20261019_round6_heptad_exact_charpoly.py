"""Round6 front2 extension: EXACT characteristic polynomials in Z[x]
of 21Q for each of the five heptad spectrum families.

21Q has Eisenstein-integer entries a+b*omega, omega^2+omega+1=0;
Hermiticity forces integer characteristic coefficients.
Compute matrix power traces and Newton recursions over Z[omega].
"""
from __future__ import annotations
import json
from collections import Counter
from pathlib import Path
from fractions import Fraction
import numpy as np
from w33_20261019_round6_heptad_symmetry import H,out as prior,torbits
from w33_20261019_tick_operator_frame_majorization import points,build_projectors
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261019_round6_heptad_exact_charpoly.json"
pts=points(); allP=build_projectors(pts).reshape(40,3,9,9)
units=((1,0),(0,1),(-1,-1))
def matrix21(choices):
    A=np.zeros((9,9),dtype=object);B=np.zeros((9,9),dtype=object)
    for p,k in zip(H,choices):
        a,b,c,d=pts[p]
        for i in range(3):
            for j in range(3):
                n=3*i+j
                A[n,n]+=1
                for power in (1,2):
                    dest=3*((i+power*a)%3)+((j+power*b)%3)
                    expo=(power*(c*i+d*j)+(power*(power-1)//2)*(a*c+b*d)-power*k)%3
                    x,y=units[expo]
                    A[dest,n]+=x;B[dest,n]+=y
    return A,B
def multiply(U,V):
    a,b=U;c,d=V
    bd=b@d
    return (a@c-bd,a@d+b@c-bd)
def traces(U):
    I=np.eye(9,dtype=object)
    cur=(I,np.zeros((9,9),dtype=object))
    tr=[]
    for n in range(1,10):
        cur=multiply(cur,U)
        x,y=cur
        ytr=sum(y[i,i] for i in range(9))
        assert ytr==0,(n,ytr)
        tr.append(int(sum(x[i,i] for i in range(9))))
    return tr
def integer_coeff(s):
    c=[1]
    for k in range(1,10):
        u=sum(c[k-j]*s[j-1] for j in range(1,k+1))
        assert u%k==0
        c.append(-u//k)
    return c
def run():
    family=[]
    for f in prior["five_spectral_families"]:
        k=f["sample_outcome_labels"]
        exact=matrix21(k)
        npM=np.asarray(exact[0],dtype=float)+np.asarray(exact[1],dtype=float)*np.exp(2j*np.pi/3)
        Q=sum(allP[p,j] for p,j in zip(H,k))/7
        err=float(np.linalg.norm(npM-21*Q))
        s=traces(exact)
        coeff=integer_coeff(s)
        eigen=np.linalg.eigvalsh(Q)
        numeric=np.poly(eigen*21)
        perr=float(max(abs(float(coeff[i])-numeric[i]) for i in range(10)))
        family.append({"count":f["size"],"translation_orbits":f["translation_cosets"],
           "one_label":k,"characteristic_polynomial_of_21Q_integer_coefficients_high_to_low":coeff,
           "power_traces_1_through_9_exact_integers":s,
           "trace_Q_exact":"3",
           "reconstruction_error":err,"floating_poly_coeff_error":perr})
    keys=[tuple(f["characteristic_polynomial_of_21Q_integer_coefficients_high_to_low"]) for f in family]
    exact_orbit_polys=Counter(tuple(integer_coeff(traces(matrix21(min(orb))))) for orb in torbits)
    checks={"five_distinct_integer_polynomials":len(set(keys))==5,
         "all_27_translation_cosets_exactly_classified":len(exact_orbit_polys)==5 and set(exact_orbit_polys)==set(keys) and sorted(exact_orbit_polys.values())==[1,2,6,6,12],
         "full_2187_assignment_count":sum(f["count"] for f in family)==2187,
         "all_eisenstein_reconstructions":all(f["reconstruction_error"]<1e-10 for f in family),
         "numeric_eigenpoly_crosscheck":all(f["floating_poly_coeff_error"]<1e-3 for f in family),
         "integer_trace_normalization":all(f["power_traces_1_through_9_exact_integers"][0]==63 for f in family)}
    result={"schema":"w33.round6.heptad_exact_integer_charpoly.v1",
      "mathematical_principle":"M=21Q=SUM_[seven P outcomes] (I+omega^-k W_p+omega^-2k W_p^2) belongs to Mat9(Z[omega]). It is Hermitian; charpoly coefficients belong to real Z[omega], hence to Z. Matrix traces computed by exact integer pair arithmetic with omega²=-1-omega and coefficients by Newton identities.",
      "families":family,
      "exact_27_translation_orbit_polynomial_multiplicities":[{"characteristic_polynomial_21Q":list(k),"orbit_count":v} for k,v in exact_orbit_polys.items()],
      "stronger_classification":"Five distinct exact integer characteristic polynomials, each representing one of the five Pauli-translation-invariant spectrum families for uniform heptad weights. Group transitivity transports to all 2880 heptads.",
      "scope":"Exact Eisenstein-arithmetic characteristic polynomials computed for ALL 27 Pauli-translation orbit representatives. Group action preserves spectrum exactly by unitary conjugation, and the five polynomial classes are therefore an exact classification of all 2187 assignments on the heptad and via Clifford action all 2880 heptads at uniform weights. No continuous mass optimization.",
      "checks":{k:bool(v) for k,v in checks.items()},"all_checks_pass":bool(all(checks.values()))}
    OUT.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"checks":result["checks"],"coefficients":[f["characteristic_polynomial_of_21Q_integer_coefficients_high_to_low"] for f in family]},indent=2))
    assert result["all_checks_pass"]
    return result
if __name__=="__main__":run()
