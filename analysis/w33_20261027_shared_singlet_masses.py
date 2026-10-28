"""Correlated fractional-state masses from a supplied common singlet potential.

Pass12311 owns the selection-rule graph and degree<=2 perfect matching.
Here witnesses, conjugate scalar bookkeeping and a radial potential are explicit.
No string-derived scalar potential or full realistic vacuum is claimed.
"""
from pathlib import Path
from itertools import combinations_with_replacement,combinations
from collections import defaultdict,Counter
from functools import lru_cache
import sys,json,re
import sympy as s
import numpy as np
import networkx as nx
from scipy.optimize import linprog
from sympy.matrices.normalforms import hermite_normal_form
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis/search_drivers_12286'))
from lr_hypercharge import solve,fermions
PATH=ROOT/'analysis/search_drivers_12281/bro/Z6II_60_SM_20260917_810_v9__w6odd.nsoq'
TH=s.diag(s.Matrix([[1,-1],[1,0]]),s.Matrix([[0,-1],[1,-1]]),-s.eye(2))


def records():
    c,_,sol=solve(fermions(PATH));ss=sol[0]
    free=sorted((set(c)-set(ss))|{z for v in ss.values()for z in s.sympify(v).free_symbols},key=str)
    cv=[s.sympify(ss.get(ci,ci)).subs(free[0],s.Rational(-1,148))for ci in c];out=[]
    for line in PATH.read_text().splitlines():
        m=re.match(r'FIELD (\d+) m=(\S+) k=\S+ mm=(\S+) n=(\S+) lat=(\S+) dim=(\S*) q=(\S*)',line)
        if not m or int(m[2])not in(15,16,19):continue
        q=tuple(s.nsimplify(float(x),tolerance=1e-9,rational=True)for x in m[7].split(',')if x)
        out.append(dict(id=int(m[1]),kind=int(m[2]),mm=int(m[3]),n=int(m[4]),lat=tuple(int(s.Rational(x))for x in m[5].split(',')),
            dims=tuple(int(re.match(r'-?\d+',x)[0])for x in m[6].split(',')),q=q,y=sum(a*b for a,b in zip(cv,q))))
    return out


@lru_cache(None)
def sector_lattice(sectors):
    matrices=[s.eye(6)-TH**k for k in sectors if k%6]
    H=hermite_normal_form(s.Matrix.hstack(*matrices))if matrices else s.zeros(6,0)
    return H,H.inv()if H.shape==(6,6)else None


def translation_allowed(vec,sectors):
    H,inverse=sector_lattice(tuple(sorted(set(k%6 for k in sectors))));v=s.Matrix(vec)
    if inverse is not None:return all(z.q==1 for z in inverse*v)
    if not H.cols:return not any(v)
    try:x,free=H.gauss_jordan_solve(v)
    except ValueError:return False
    assert not free.rows
    return all(z.q==1 for z in x)


@lru_cache(None)
def lattice_class(vec,sectors):
    H,_=sector_lattice(sectors);rows=H.T.rref()[1]
    if not rows:return tuple(s.Matrix(vec))
    x=H[list(rows),:].inv()*s.Matrix([vec[i]for i in rows]);residual=s.Matrix(vec)-H*x
    return tuple(z%s.Integer(1)for z in x)+tuple(residual)


@lru_cache(None)
def rotated(vec):return tuple(tuple(int(z)for z in TH**k*s.Matrix(vec))for k in range(6))


def orbit_witness(fields):
    """Necessary space-group membership allowing point-group conjugates.

    Does not sum gamma-eigenstate amplitudes or impose world-sheet vertices.
    """
    sectors=tuple(sorted(set(x['n']%6 for x in fields)));H,_=sector_lattice(sectors);rank=H.cols
    states={(s.S.Zero,)*(rank+6):[]}
    for field in fields:
        choices={lattice_class(v,sectors):k for k,v in enumerate(rotated(field['lat']))};nextstates={}
        for a,history in states.items():
            for b,k in choices.items():
                key=tuple((x+y)%1 if i<rank else x+y for i,(x,y)in enumerate(zip(a,b)))
                nextstates.setdefault(key,history+[k])
        states=nextstates
    return states.get((s.S.Zero,)*(rank+6))


def fractional(r):
    d=r['dims'];y=r['y'];tl=[s.Rational(1,2),-s.Rational(1,2)]if abs(d[1])==2 else[0];tr=[s.Rational(1,2),-s.Rational(1,2)]if abs(d[2])==2 else[0]
    return any((3*(a+b+y)if abs(d[0])==3 else a+b+y).q!=1 for a in tl for b in tr)


def pairable(a,b):
    d=a['dims'];conjugate=(-d[0]if abs(d[0])==3 else d[0],d[1],d[2],-d[3]if abs(d[3])in(8,28,56)else d[3])
    return conjugate==b['dims']and a['y']+b['y']==0


def run():
    raw=records();S=[r for r in raw if r['kind']==16 and all(abs(x)==1 for x in r['dims'])and r['y']==0]
    conjugates=[r for r in raw if r['kind']==15 and all(abs(x)==1 for x in r['dims'])and r['y']==0]
    assert len(S)==len(conjugates)==25
    # Identify25 independent complex scalar coordinates, not50 independent vevs.
    G=nx.Graph();G.add_nodes_from(range(50))
    for i,a in enumerate(S):
        for j,b in enumerate(conjugates):
            if all(x+y==0 for x,y in zip(a['q'],b['q']))and(a['n']+b['n'])%6==0 and(a['mm']+b['mm'])%2==0:
                if orbit_witness((a,b))is not None:G.add_edge(i,25+j)
    matching=nx.max_weight_matching(G,maxcardinality=True);assert len(matching)==25
    scalar_conjugate_pairs=sorted([S[min(i,j)]['id'],conjugates[max(i,j)-25]['id']]for i,j in matching)
    conjugate_map={min(i,j):conjugates[max(i,j)-25]for i,j in matching}
    atoms=[(i,sign)for i in range(25)for sign in(-1,1)];monomials=defaultdict(list)
    # Keep S*Sdagger: it is a degree2 operator, not the bare operator1.
    # Bare masses are excluded because this probe asks for vev-induced masses.
    for terms in [(a,)for a in atoms]+list(combinations_with_replacement(atoms,2)):
        charge=tuple(sum(sign*S[i]['q'][j]for i,sign in terms)for j in range(5))
        n=sum(sign*S[i]['n']for i,sign in terms);mm=sum(sign*S[i]['mm']for i,sign in terms)
        atomfields=tuple(S[i]if sign>0 else conjugate_map[i]for i,sign in terms)
        monomials[(charge,n%6,mm%2)].append((terms,atomfields))
    Fr=[r for r in raw if r['kind']==19 and fractional(r)];graph=nx.Graph();graph.add_nodes_from(range(len(Fr)));witness={};control_e5=0
    for i,j in combinations(range(len(Fr)),2):
        a,b=Fr[i],Fr[j]
        if not pairable(a,b):continue
        key=(tuple(-x-y for x,y in zip(a['q'],b['q'])),(-a['n']-b['n'])%6,(-a['mm']-b['mm'])%2)
        candidates=[];shifted=False
        for terms,atomfields in monomials.get(key,[]):
            rotation=orbit_witness((a,b)+atomfields)
            if rotation is not None:candidates.append((terms,rotation))
            shifted_b={**b,'lat':tuple(x+(k==4)for k,x in enumerate(b['lat']))}
            if orbit_witness((a,shifted_b)+atomfields)is not None:shifted=True
        if candidates:
            best=min(candidates,key=lambda t:(len(t[0]),t[0]));graph.add_edge(i,j,weight=100-len(best[0]));witness[(i,j)]=best
            control_e5+=int(shifted)
    Mt=nx.max_weight_matching(graph,maxcardinality=True);assert len(Fr)==48 and len(Mt)==24 and control_e5==0
    # Strictly convex, gauge-invariant non-SUSY radial TEST potential:
    # V/v^4=-1^T t + t^T[I+kappa Q^T Q]t/2, t_i=|S_i|^2/v^2.
    Q=s.Matrix.hstack(*[s.Matrix(r['q'])for r in S]);kappa=s.Rational(1,10**6);A=s.eye(25)+kappa*Q.T*Q
    t=A.inv()*s.ones(25,1);assert all(x>0 for x in t)and A*t==s.ones(25,1)
    dflat=linprog(np.zeros(25),A_eq=np.vstack((np.array(Q,float),np.ones(25))),b_eq=np.r_[np.zeros(5),1],bounds=[(0,None)]*25,method='highs')
    selected=[]
    for i,j in sorted(tuple(sorted(e))for e in Mt):
        terms,rotations=witness[(i,j)];degree=len(terms)
        # With v/Lambda=.1, each coefficient is set to1. Conjugate vevs
        # have exactly the same modulus, sharing the SAME25 radial coordinates.
        mass=(.1**degree)*np.prod([np.sqrt(float(t[k]))for k,sign in terms])
        selected.append(dict(fermion_ids=[Fr[i]['id'],Fr[j]['id']],degree=degree,point_group_rotations=rotations,
            singlet_monomial=[dict(field_id=S[k]['id'],conjugated=sign<0,coordinate=k)for k,sign in terms],
            mass_over_cutoff=float(mass)))
    # Isolated selected pair operators lift48 multiplet labels. Switching off
    # unselected allowed Yukawas is a supplied sparse coupling choice.
    masses=[x['mass_over_cutoff']for x in selected]
    components=sum(int(np.prod([abs(z)for z in r['dims']]))for r in Fr)
    assert components==sum(2*int(np.prod([abs(z)for z in Fr[i]['dims']]))for i,j in Mt)
    return dict(schema='shared_singlet_radial_vacuum_and_pair_witnesses_v1',independent_complex_singlets=25,raw_scalar_records=50,
        scalar_conjugate_pairs=scalar_conjugate_pairs,fractional_Weyl_multiplets=48,allowed_pair_count_degree_at_most2=graph.number_of_edges(),
        selection_rule_correction='Fixed canonical representatives alone need not contain a field and its CPT conjugate. Allow independent theta-orbit representatives in the necessary space-group test. Gamma-eigenstate coefficients and non-SUSY world-sheet vertices remain uncomputed; kinematic allowance is not a nonzero string amplitude.',
        shifted_e5_allowed_edges=control_e5,matched_pairs=selected,degree_counts=dict(Counter(x['degree']for x in selected)),
        paired_Weyl_gauge_components=components,
        mass_rank_certificate='Each selected pair consists of distinct multiplets with dual nonabelian representations and nonzero mass. Their invariant contraction is nonsingular. Disjoint pairs therefore give full rank on all listed Weyl gauge components, conditional on the supplied operator coefficients; this is not a computed string amplitude.',
        potential=dict(definition='V/v^4=-sum(t)+t^T(I+kappa Q^T Q)t/2, t=|S|^2/v^2',kappa=str(kappa),
            exact_squared_vevs=list(map(str,t)),scalar_field_ids=[r['id']for r in S],charge_matrix=[[str(x)for x in row]for row in Q.tolist()],
            exact_stationarity=True,squared_modulus_coordinate_Hessian_lower=1,
            proof='A=I+kappa Q^TQ is strictly positive. Exact t=A^-1 1 has all positive entries, hence is the unique global minimum in the nonnegative radial orthant. Scalar phases remain flat, with gauge directions among them.',
            Dflat_zero_FI_feasible=bool(dflat.success),Dflat_solver_message=dflat.message,
            unbroken_U1_dimension=5-int(Q.rank()),mass_ratio_max_to_min=float(max(masses)/min(masses))),
        scope='Explicit correlated fractional-state pair masses at the global radial minimum of a SUPPLIED gauge-invariant non-SUSY test potential, with selected Yukawa coefficients1 and all other pair coefficients0. Nonabelian singlet vevs preserve SU2R and cannot independently split its multiplets. Not the string scalar potential, all exotic masses, left-right breaking, a full threshold fit or an isolated phase-stabilized vacuum.',
        inherited_candidate_window='Pass12316 empty-window claim was withdrawn in12322. Current statement: R6<sqrt(3/8) string units survives computed e6 conditions; e5 winding projections/potential remain unresolved. Do not use the withdrawn empty-window assertion.',
        prior_owner='analysis/search_drivers_12311/vacuum.py; Pass12322-12333; Oct27 representation threshold witness')


if __name__=='__main__':
    d=run();(ROOT/'data/w33_20261027_shared_singlet_masses.json').write_text(json.dumps(d,indent=2)+'\n');print(json.dumps(d,indent=2))
