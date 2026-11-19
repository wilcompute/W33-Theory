"""Exact qutrit SIC Plucker/baryon moments and SU(3)-invariant alignment.

The 3-vs-12 dependent triple distinction is known SIC geometry. We
implement its gauge-invariant determinant/Hesse-line moment form.
"""
from pathlib import Path
from collections import Counter
from itertools import combinations
import json
import sympy as s

ROOT=Path(__file__).resolve().parents[1]
w=(-1+s.I*s.sqrt(3))/2
X=s.Matrix([[0,0,1],[1,0,0],[0,1,0]])
Z=s.diag(1,w,w**2)
def exact(q):
    return s.simplify(s.expand_complex(q))
def orbit(sign):
    v=s.Matrix([1,sign,0])
    # Index = 3*b+a, with (a,b) affine-plane coordinates.
    return [X**b*Z**a*v for b in range(3) for a in range(3)]
def affine_lines():
    lines=set()
    for da,db in ((1,0),(0,1),(1,1),(1,2)):
        for a in range(3):
            for b in range(3):
                line=tuple(sorted(3*((b+t*db)%3)+(a+t*da)%3 for t in range(3)))
                lines.add(line)
    assert len(lines)==12
    return lines
LINES=affine_lines()

def cert(sign):
    cols=orbit(sign)
    frame=sum((v*v.conjugate().T for v in cols),s.zeros(3))
    frame=frame.applyfunc(exact)
    assert frame==6*s.eye(3)
    r=exact((cols[0].conjugate().T*cols[0])[0])
    assert r==2
    pair=[]
    for i,j in combinations(range(9),2):
        inner=(cols[i].conjugate().T*cols[j])[0]
        pair.append(exact(inner*s.conjugate(inner)))
    assert set(pair)=={1} and len(pair)==36
    assert all(4*q==r*r for q in pair)
    distribution=Counter()
    on_line=Counter()
    for i,j,k in combinations(range(9),3):
        b=s.Matrix.hstack(cols[i],cols[j],cols[k]).det()
        val=str(exact(b*s.conjugate(b)))
        distribution[val]+=1
        if (i,j,k) in LINES:
            on_line[val]+=1
    assert sum(distribution.values())==84 and sum(on_line.values())==12
    m=[sum(int(t)**power*v for t,v in distribution.items()) for power in (1,2,3)]
    assert m[0]==exact(frame.det())==216 # Cauchy-Binet
    line_sum=sum(int(k)*v for k,v in on_line.items())
    return dict(sign=sign,frame_det="216",
        pair_count=36,pair_overlap_sq_unscaled="1",potential_value="0",
        baryonic_minor_squared_distribution=dict(sorted(distribution.items(),key=lambda t:int(t[0]))),
        baryonic_det_squared_moments=m,
        hesse_line_minor_squared_distribution=dict(sorted(on_line.items(),key=lambda t:int(t[0]))),
        hesse_line_baryon_sextic_sum=line_sum)

plus,minus=cert(1),cert(-1)
assert plus["baryonic_minor_squared_distribution"]=={"0":3,"1":18,"3":54,"4":9}
assert minus["baryonic_minor_squared_distribution"]=={"0":12,"3":72}
assert plus["baryonic_det_squared_moments"]==[216,648,2052]
assert minus["baryonic_det_squared_moments"]==[216,648,1944]
assert plus["hesse_line_minor_squared_distribution"]=={"0":3,"4":9}
assert minus["hesse_line_minor_squared_distribution"]=={"0":12}
assert plus["hesse_line_baryon_sextic_sum"]==36
assert minus["hesse_line_baryon_sextic_sum"]==0
# Nine equal norm-square r, pair overlap-square r²/4 implies
# Tr(S)=9r, Tr(S²)=9r²+72r²/4=27r²=(Tr S)²/3.
# By equality in Cauchy-Schwarz for the 3 eigenvalues, S=3r I.
result={
 "setup":"Nine SU(3) fundamental species norm-square r and SIC overlap-square r^2/4",
 "nonnegative_gauge_invariant_alignment":"mu*sum_j (Q_j^dag Q_j-r)^2 + kappa*sum_{i<j}(4*abs(Q_i^dag Q_j)^2-r^2)^2",
 "zero_potential_enforces":"S=sum_j Q_j Q_j^dag=3*r*I_3, so D^a=0",
 "frame_trace":"9r","frame_squared_trace":"27r^2",
 "plus":plus,"minus":minus,
 "all_84_baryon_minor_first_moment":216,
 "all_84_baryon_minor_second_moment":648,
 "all_84_baryon_minor_third_moment_difference":108,
 "hesse_line_count":12,
 "hesse_line_sextic_baryon_sum_plus":36,
 "hesse_line_sextic_baryon_sum_minus":0,
 "hesse_line_sum_is_su3_gauge_and_h27_translation_invariant":True,
 "limits":"The Hesse-line sextic is gauge-invariant but distinguishes only these test vacua; it does not prove global plus-SIC uniqueness. This is bosonic, not a holomorphic SUSY UV superpotential. Flavor phases and continuous degeneracies remain."
}
dst=ROOT/"data"/"toe_20261119_sic_baryon_plucker_alignment.json"
dst.write_text(json.dumps(result,indent=2)+"\n",encoding="utf8")
print("PASS: SU3-invariant SIC alignment -> D-flat; Plucker 3 vs 12 zero triples; Hesse-line sextic 36 vs 0")
print(dst)
