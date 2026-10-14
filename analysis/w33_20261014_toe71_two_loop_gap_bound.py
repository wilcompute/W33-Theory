"""TOE71: explicit native TWO-LOOP complement and full-rotor gap bound.

Exact integer electric/Gauss census and rational operator-norm bounds;
previous TOE70 numerical Ritz eigenvalues are INPUT, NOT interval-certified.
Consequently full-rotor numerical endpoints are CONDITIONAL on those finite
eigenvalues, although block min-max inequalities are mathematically exact.
"""
from pathlib import Path
from itertools import product
import json,sys,math
import numpy as np
from scipy.sparse import coo_matrix
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261014_toe69_two_octagon_covariance import patch,exact_gauss_electric

def certificate():
    p=patch()
    assert len(p["nodes"])==11 and len(p["support"])==12
    assert len(p["P"])==3 and len(p["chords"])==2
    nferm=int(sum(p["background"]))
    fock=[x for x in range(1<<11) if x.bit_count()==nferm]
    occ=np.asarray([[(x>>i)&1 for i in range(11)] for x in fock],int)
    assert len(occ)==462
    off=np.asarray([exact_gauss_electric(o,np.array((0,0)),p) for o in occ])
    A=np.asarray([
       exact_gauss_electric(occ[0],np.array(f),p)-off[0]
       for f in ((1,0),(0,1))]).T
    assert A.shape==(12,2)
    # Every flux outside |m_i|<=3 must be inspected. A finite search to
    # |m_i|<=12 is exact, since each n_chord=m_i and |m_i|>=13 implies
    # electric energy >= (g²/2)*13². The mass term is >=-1.5.
    # Adding three beta/g² magnetic constants gives >=54.455>18.215.
    g=.8;kappa=.7;beta=.4;mass=.3
    stagger=mass*np.asarray([
       (1-2*p["background"])@o for o in occ])
    outside_min=(1e100,None,None)
    for f in product(range(-12,13),repeat=2):
        if max(map(abs,f))<=3:continue
        n=off+(A@np.array(f))
        es=(g*g/2)*np.einsum("ij,ij->i",n,n)+stagger+3*beta/(g*g)
        j=int(np.argmin(es))
        if es[j]<outside_min[0]:
            outside_min=(float(es[j]),tuple(f),fock[j])
    assert abs(outside_min[0]-18.215)<1e-10
    no_outside_min=(g*g/2)*13**2-1.5+3*beta/g**2
    assert no_outside_min>outside_min[0]
    Q_offdiag=12*kappa+3*beta/g**2
    Q_lower=outside_min[0]-Q_offdiag
    assert abs(Q_lower-7.94)<1e-10
    # The coupling P(L=3)->Q touches only shell max|m_i|=4.
    inside=list(product(range(-3,4),repeat=2))
    ring=[f for f in product(range(-4,5),repeat=2)
          if max(map(abs,f))==4]
    ifidx={x:i for i,x in enumerate(fock)}
    pi={f:i for i,f in enumerate(inside)}
    qi={f:i for i,f in enumerate(ring)}
    ni=len(inside);nq=len(ring)
    rows=[];cols=[];vals=[]
    for i,bits in enumerate(fock):
        o=occ[i]
        hops=[]
        for edge,(a,b) in enumerate(p["p_ed"]):
            if edge not in p["chords"] or o[a]==o[b]:continue
            target=bits^(1<<a)^(1<<b)
            sign=(-1)**sum((bits>>j)&1 for j in range(min(a,b)+1,max(a,b)))
            hops.append((edge,ifidx[target],1 if o[a] else -1,sign))
        for mi,f in enumerate(inside):
            r=i*ni+mi
            for edge,dest,direction,sign in hops:
                z=list(f)
                z[p["chords"].index(edge)]-=direction
                t=qi.get(tuple(z))
                if t is not None:
                    rows.append(r);cols.append(dest*nq+t);vals.append(-kappa*sign)
            for delta in p["P"][:,p["chords"]]:
                for direction in (-1,1):
                    t=qi.get(tuple(np.asarray(f)+direction*delta))
                    if t is not None:
                        rows.append(r);cols.append(i*nq+t)
                        vals.append(-beta/(2*g*g))
    K=coo_matrix((vals,(rows,cols)),shape=(len(fock)*ni,len(fock)*nq)).tocsr()
    assert K.nnz==28476 and K.shape==(22638,14784)
    rowmax=float(np.asarray(abs(K).sum(axis=1)).max())
    colmax=float(np.asarray(abs(K).sum(axis=0)).max())
    # This is a RIGOROUS operator 2-norm upper bound:
    # ||K||² <= ||K||_1*||K||_infty.
    d2=rowmax*colmax
    assert abs(rowmax-2.65)<1e-12
    assert abs(colmax-1.325)<1e-12
    assert abs(d2-3.51125)<1e-12
    # Ritz inputs from previously reproduced TOE70 L=3:
    E0=-3.1898474481159673
    gap=1.0643124872613563
    E1=E0+gap
    # For QHQ>=Qlower I and ||K||²<=d2, block min-max lower:
    low0=(E0+Q_lower-math.sqrt((Q_lower-E0)**2+4*d2))/2
    # Inertia/Schur complement at lambda<=0: since Qlower>0,
    # the j-th negative eigenvalue of full H lies >=lambda_j(P)-d2/Qlower.
    low1=E1-d2/Q_lower
    gap_lower=low1-E0
    assert gap_lower>.62
    return {
       "status":"PASS_TOE71_TWO_LOOP_OPERATOR_COMPLEMENT_BOUND",
       "native_patch":[11,12,5],"flux_cutoff_L":3,
       "P_dimension":22638,"first_complement_shell_dimension":14784,
       "charge_sector_Fock_states":462,
       "exact_diagonal_Q_min":outside_min[0],
       "Q_min_attaining_flux":list(outside_min[1]),
       "Q_min_attaining_Fock_bitmask":outside_min[2],
       "high_flux_tail_diagonal_lower":no_outside_min,
       "Q_offdiagonal_row_sum_bound":Q_offdiag,
       "Q_spectral_lower_bound":Q_lower,
       "interface_nonzero_elements":K.nnz,
       "interface_max_row_abs_sum":rowmax,
       "interface_max_column_abs_sum":colmax,
       "interface_norm_squared_upper":d2,
       "P_numerical_ground":E0,"P_numerical_first_excited":E1,
       "conditional_full_ground_bracket":[low0,E0],
       "conditional_full_first_excited_lower":low1,
       "conditional_full_spectral_gap_lower":gap_lower,
       "mathematical_statement":"Given rigorous lower E0(P), lower E1(P) and upper E0(P) enclosures, the stated Gershgorin and interface norms imply a full unbounded-rotor energy bracket and strictly positive gap by block spectral min-max / Schur inertia.",
       "important_limitation":"E0(P),E1(P) are numerical TOE70 Ritz estimates, not interval-certified ordered eigenvalues. The decimal infinite-rotor energy and gap bounds remain CONDITIONAL, not computer-assisted proofs, until those eigenvalue enclosures are provided."
    }
if __name__=="__main__":
    out=certificate()
    (ROOT/"data/w33_20261014_toe71_two_loop_gap_bound.json").write_text(
      json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print(out["status"],out["conditional_full_spectral_gap_lower"])
