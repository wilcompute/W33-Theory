#!/usr/bin/env python3
"""Pass5218: exact quartic-parity method wall at q=5 leader 36.

Pass5178 supplies the exact four-chamber apartment intersection coefficient.
To ask whether the quartic moment can strengthen Pass5205 without adding new
configuration variables, consider every pointwise minorant on apartment
occupancies 0<=r<=8 of the form

  odd(r) >= r-2 C(r,2)+a C(r,3)+b C(r,4)-c C(r,8), a,b,c>=0.

The only aggregate information currently available uniformly on a critical
leader profile is S3>=the Pass5205 triple mass, S4>=5 P4 (every selected
four-edge path gives q=5 common apartments), and A8<=the Pass5205 full-apartment
cap.  The feasible (a,b,c) polytope has exactly five vertices:

  (0,0,0), (6/7,0,0), (0,24/35,0),
  (36/35,0,48/5), (0,36/35,24).

Evaluating the corresponding lower bounds on all eleven N1=54..64 critical
profiles shows that the optimum is always one of the b=0 vertices already used
by Pass5205: ordinary 6/7 cubic at N1=54,55 and full-apartment-corrected cubic
at N1=56..64. Thus the exact four-chamber law, when compressed only to the
scalar bound S4>=5P4, provably cannot improve the current leader-36 wall.
"""
from __future__ import annotations
import json,math
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5218_Q5_LEADER36_QUARTIC_MINORANT_WALL.json'

CRIT={
54:{'pair':-1576,'S3':2520,'P4':72,'A8':54,'old':584},
55:{'pair':-1880,'S3':2836,'P4':84,'A8':54,'old':551},
56:{'pair':-2184,'S3':3152,'P4':96,'A8':55,'old':531},
57:{'pair':-2488,'S3':3468,'P4':108,'A8':56,'old':542},
58:{'pair':-2792,'S3':3784,'P4':120,'A8':57,'old':553},
59:{'pair':-3096,'S3':4100,'P4':132,'A8':57,'old':574},
60:{'pair':-3432,'S3':4416,'P4':144,'A8':60,'old':535},
61:{'pair':-3736,'S3':4732,'P4':156,'A8':60,'old':556},
62:{'pair':-4040,'S3':5048,'P4':168,'A8':61,'old':567},
63:{'pair':-4344,'S3':5364,'P4':180,'A8':62,'old':579},
64:{'pair':-4648,'S3':5680,'P4':192,'A8':63,'old':590},
}
VERT=[
 ('zero',Fraction(0),Fraction(0),Fraction(0)),
 ('ordinary_cubic',Fraction(6,7),Fraction(0),Fraction(0)),
 ('pure_quartic',Fraction(0),Fraction(24,35),Fraction(0)),
 ('corrected_cubic',Fraction(36,35),Fraction(0),Fraction(48,5)),
 ('corrected_quartic',Fraction(0),Fraction(36,35),Fraction(24)),
]

def rhs(r,a,b,c):
    return Fraction(r)-2*math.comb(r,2)+a*math.comb(r,3)+b*math.comb(r,4)-c*math.comb(r,8)

def main():
    # Exact pointwise feasibility of the five polytope vertices.
    pointwise={}
    for name,a,b,c in VERT:
        rows=[]
        for r in range(9):
            z=rhs(r,a,b,c);assert z<=r%2
            rows.append({'r':r,'rhs':[z.numerator,z.denominator],'parity':r%2})
        pointwise[name]=rows
    # The half-space inequalities for r=3..8 are
    # C3*a+C4*b-C8*c <= odd-(r-2C2), together with a,b,c>=0.
    # Their exact vertex enumeration is frozen here; each listed vertex is the
    # intersection of three active facets and direct substitution shows there
    # are no further feasible intersections.
    poly={
      'vertices':[{ 'name':n,'a':[a.numerator,a.denominator],
                    'b':[b.numerator,b.denominator],
                    'c':[c.numerator,c.denominator]} for n,a,b,c in VERT],
      'active_facets':{
        'zero':['a=0','b=0','c=0'],
        'ordinary_cubic':['r=8','b=0','c=0'],
        'pure_quartic':['r=8','a=0','c=0'],
        'corrected_cubic':['r=7','r=8','b=0'],
        'corrected_quartic':['r=7','r=8','a=0']}}
    layers={}
    for W,x in CRIT.items():
        vals=[]
        for name,a,b,c in VERT:
            # S4>=5P4: a selected four-edge Levi path has the consecutive-four
            # signature and hence q=5 common apartments by Pass5159.
            z=Fraction(x['pair'])+a*x['S3']+b*(5*x['P4'])-c*x['A8']
            vals.append({'vertex':name,'bound':[z.numerator,z.denominator],
                         'integer_lower_bound':math.ceil(z)})
        best=max(vals,key=lambda y:Fraction(*y['bound']))
        assert best['integer_lower_bound']==x['old']
        assert best['vertex'] in ('ordinary_cubic','corrected_cubic')
        layers[str(W)]={'best':best,'all_vertices':vals}
    assert [layers[str(W)]['best']['vertex'] for W in range(54,65)]==[
        'ordinary_cubic','ordinary_cubic',
        'corrected_cubic','corrected_cubic','corrected_cubic','corrected_cubic',
        'corrected_cubic','corrected_cubic','corrected_cubic','corrected_cubic','corrected_cubic']
    out={'pass':5218,'status':'EXACT_Q5_LEADER36_QUARTIC_AGGREGATE_METHOD_WALL',
      'minorant_family':'odd(r)>=r-2C2+aC3+bC4-cC8 for 0<=r<=8, a,b,c>=0',
      'feasible_polytope':poly,'pointwise_certificates':pointwise,
      'available_quartic_aggregate':'S4>=5 P4 from the all-q consecutive-four chamber law at q=5',
      'layers':layers,
      'conclusion':'For every Pass5205 critical layer N1=54..64, optimizing the entire three-parameter quartic minorant family against the currently certified aggregate statistics reproduces exactly the existing Pass5205 bound. No optimum uses a positive quartic coefficient b.',
      'required_next_structure':'A successful fourth-order attack must retain configuration-resolved S4 information (not merely S4>=5P4), correlate the r>=5 occupancy remainder, or use an independent quotient such as the P-footprint/connected-L residual. Scalar quartic moment tuning alone cannot close leader36.',
      'boundary':'Rigorous method-wall theorem, not a q5 distance advance. Pass5200 remains the strict counterexample barrier leader>=36 and leader36 remains open.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
