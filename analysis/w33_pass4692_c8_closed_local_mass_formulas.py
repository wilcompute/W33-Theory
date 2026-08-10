#!/usr/bin/env python3
"""Pass 4692 -- closed primitive-C8 local mass formulas and the exact obstruction to an (s,t)-only law.

Pass4635 reduced apartment/star degree-four primitive-C8 coefficients to six raw
walk signatures.  This pass closes those masses.  Put u=s-1.  Two apartment
invariants and one star invariant are genuinely required:

 rho   = number of intersecting pairs between the two size-u families of
         external transversals to the two opposite apartment-line pairs;
 sigma = number of intersecting pairs consisting of one such external
         transversal and one outside line meeting exactly one apartment line;
 tau   = number of outside common transversals to the three leaf lines of an
         induced K1,3 (the selected central line is excluded).

The six exact raw masses are

 A1111|22 = 16[(4u^2+2)rho + u^2 sigma + (4t-2)u^4 + 2(t-1)]
 A1115    = 64u(u^3-u^2+2u-1)
 A1133    = 96u^2(u-1)^2
 A1111|4  = 64(u+1)u(u-1)(t-1)
 S1111|22 = 48(u+1)u^3
 S1113|2  = 48(u+1)u tau.

The need for embedding data is decisive: W33 and its dual both have order (3,3)
but (rho,sigma,tau)=(0,16,1) and (4,0,3), respectively.  Direct mask-only
nonbacktracking computation gives apartment/star coefficients (712,180) versus
(728,252).  Therefore no (s,t)-only primitive-C8 formula can describe both.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,defaultdict
from pathlib import Path
import w33_pass4573_general_gq_c8_selector_obstruction as p4573
import w33_pass4635_c8_six_signature_collision_criterion as p4635
from w33_pass4495_4502_distance_prism_reconstruction import geometry
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4692_C8_CLOSED_LOCAL_MASS_FORMULAS.json'

def st(lines):
    ss=len(lines[0])-1
    incid=Counter(p for L in lines for p in L);tt=next(iter(incid.values()))-1
    assert set(incid.values())=={tt+1}
    return ss,tt

def apt_invariants(lines,target):
    adj=lambda i,j:bool(lines[target[i]]&lines[target[j]])
    opp=[(i,j) for i,j in itertools.combinations(range(4),2) if not adj(i,j)];assert len(opp)==2
    oset=[]
    for i,j in opp:
        T=[o for o in range(len(lines)) if o not in target and lines[o]&lines[target[i]] and lines[o]&lines[target[j]]]
        oset.append(T)
    s,_=st(lines);assert [len(x) for x in oset]==[s-1,s-1]
    rho=sum(bool(lines[a]&lines[b]) for a in oset[0] for b in oset[1])
    TALL=set(oset[0]+oset[1]);singles=[]
    for o in range(len(lines)):
        if o in target or o in TALL:continue
        hits=sum(bool(lines[o]&lines[x]) for x in target)
        if hits==1:singles.append(o)
    sigma=sum(bool(lines[a]&lines[b]) for a in TALL for b in singles)
    return rho,sigma

def star_tau(lines,target):
    deg={x:sum(bool(lines[x]&lines[y]) for y in target if y!=x) for x in target}
    central=next(x for x in target if deg[x]==3);leaves=[x for x in target if x!=central]
    return sum(1 for o in range(len(lines)) if o not in target and all(lines[o]&lines[L] for L in leaves))

def raw_formula(s,t,rho,sigma,tau):
    u=s-1
    return {
      'apartment_raw_signatures':{
        '1111|22':16*((4*u*u+2)*rho + u*u*sigma + (4*t-2)*u**4 + 2*(t-1)),
        '1115|':64*u*(u**3-u**2+2*u-1),
        '1133|':96*u*u*(u-1)**2,
        '1111|4':64*(u+1)*u*(u-1)*(t-1)},
      'star_raw_signatures':{
        '1111|22':48*(u+1)*u**3,
        '1113|2':48*(u+1)*u*tau}}

def coeff(raw):return sum(raw.values())//8

def half(start,steps,trans):
    cur={(start,0):1}
    for _ in range(steps):
        z=defaultdict(int)
        for (q,m),c in cur.items():
            for j,li in trans[q]:z[(j,m^(1<<li))]+=c
        cur=z
    by=defaultdict(Counter)
    for (q,m),c in cur.items():by[q][m]+=c
    return by

def direct_coeff(pts,lines,target):
    dedges,nxt,rev=p4573.nb_tables(pts,lines);tm=p4573.mask(target);total=0
    for q in range(len(dedges)):
        f=half(q,4,nxt);r=half(q,4,rev)
        for mid in set(f)&set(r):
            rr=r[mid]
            for m,c in f[mid].items():total+=c*rr.get(m^tm,0)
    assert total%8==0;return total//8

def row(name,pts,lines,expected=None):
    ap,star=p4635.choose_supports(lines);s,t=st(lines);rho,sigma=apt_invariants(lines,ap);tau=star_tau(lines,star)
    F=raw_formula(s,t,rho,sigma,tau);ca=coeff(F['apartment_raw_signatures']);cs=coeff(F['star_raw_signatures'])
    if expected is not None:assert (ca,cs)==expected
    return {'geometry':name,'s':s,'t':t,'rho':rho,'sigma':sigma,'tau':tau,**F,'apartment_coefficient':ca,'star_coefficient':cs}

def main()->int:
    old=json.loads((ROOT/'data/PART_W33_PASS4635_C8_SIX_SIGNATURE_COLLISION_CRITERION.json').read_text(encoding='utf-8'))
    p22,l22=p4573.symplectic_gq22();p24,l24=p4573.qminus_gq24();p42,l42=p4635.dual_gq(p24,l24);pts,_,lines,*_=geometry()
    rows=[row('GQ(2,2)',p22,l22,(36,36)),row('GQ(2,4)',p24,l24,(60,36)),row('GQ(4,2)',p42,l42,(2812,792)),row('W33',pts,lines,(712,180))]
    # Every old raw anchor is reproduced entry-by-entry; omit literal zero species in old JSON.
    for new,prev in zip(rows,old['anchors']):
        for side in ('apartment_raw_signatures','star_raw_signatures'):
            assert {k:v for k,v in new[side].items() if v}==prev[side]
    dpts,dlines=p4635.dual_gq(pts,lines);dual=row('dual W33 = Q(4,3)',dpts,dlines)
    apd,std=p4635.choose_supports(dlines)
    assert (direct_coeff(dpts,dlines,apd),direct_coeff(dpts,dlines,std))==(dual['apartment_coefficient'],dual['star_coefficient'])==(728,252)
    assert (rows[-1]['s'],rows[-1]['t'])==(dual['s'],dual['t'])==(3,3)
    assert (rows[-1]['rho'],rows[-1]['sigma'],rows[-1]['tau'])==(0,16,1)
    assert (dual['rho'],dual['sigma'],dual['tau'])==(4,0,3)
    out={'pass':4692,'formulas':{
      'u':'s-1',
      'rho':'intersecting cross-pairs of the two external-transversal families of an apartment',
      'sigma':'intersecting external-transversal / single-apartment-hit outside-line pairs',
      'tau':'outside common transversals of the three K1,3 leaf lines',
      'A_1111_22':'16*((4u^2+2)rho + u^2 sigma + (4t-2)u^4 + 2(t-1))',
      'A_1115':'64u(u^3-u^2+2u-1)','A_1133':'96u^2(u-1)^2','A_1111_4':'64(u+1)u(u-1)(t-1)',
      'S_1111_22':'48(u+1)u^3','S_1113_2':'48(u+1)u tau'},
      'exact_anchors':rows,'same_parameter_counterexample':{'W33':rows[-1],'dual_W33':dual,'direct_dual_coefficients_verified':[728,252]},
      'theorem':'All six Pass4635 primitive-C8 raw masses have closed local formulas.  Four depend only on s,t; apartment 1111|22 requires rho and sigma, and star 1113|2 requires tau.  W33 and its dual have the same order (3,3) but different invariants and exact coefficients, proving that no (s,t)-only law exists.',
      'boundary':'Exact generalized-quadrangle local combinatorics.  rho, sigma and tau are incidence invariants of the selected embedded support; they are not replaced by numerological functions of s,t.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
