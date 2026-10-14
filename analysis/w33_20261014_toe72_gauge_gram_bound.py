"""TOE72: exact integral K K^T interface bound and improved Q complement.

Full native 11-site/12-edge 5-fermion two-loop Gauss patch. All matrix
entries scaled to integers; no claim that previously computed ordered
finite P eigensolver values are mathematically interval certified.
"""
from __future__ import annotations
import itertools,json,sys,math
from pathlib import Path
import numpy as np
from scipy.sparse import coo_matrix
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261014_toe69_two_octagon_covariance import patch,exact_gauss_electric

def certificate():
    p=patch()
    fock=[b for b in range(1<<11) if b.bit_count()==5]
    fi={b:i for i,b in enumerate(fock)}
    occupations=np.asarray([[(b>>i)&1 for i in range(11)] for b in fock],int)
    offsets=np.asarray([exact_gauss_electric(o,np.zeros(2,int),p) for o in occupations])
    A=np.asarray([exact_gauss_electric(occupations[0],np.array(d),p)-offsets[0]
                  for d in ((1,0),(0,1))]).T
    assert len(fock)==462 and A.shape==(12,2)
    chord={e:i for i,e in enumerate(p["chords"])}
    shifts=[tuple(map(int,x)) for x in p["P"][:,p["chords"]]]
    # Full omitted-sector Gershgorin lower bound in integer units 1/2000.
    # diagonal = .32*sum(electric^2)+.3*stagger+1.875
    # hop abs=.7, magnetic abs=.3125.
    all_f=[(a,b) for a,b in itertools.product(range(-9,10),repeat=2)
           if max(abs(a),abs(b))>3]
    best=(10**15,None,None)
    for index,bits in enumerate(fock):
        o=occupations[index]
        stagger=int(np.dot(1-2*p["background"],o))
        hopping=[]
        for e,(a,b) in enumerate(p["p_ed"]):
            if o[a]==o[b]:continue
            d=[0,0]
            if e in chord:d[chord[e]]= -1 if o[a] else 1
            hopping.append(tuple(d))
        for f in all_f:
            electric=offsets[index]+A@np.asarray(f)
            diagonal=640*int(electric@electric)+600*stagger+3750
            hcount=sum(max(abs(f[0]+dx),abs(f[1]+dy))>3 for dx,dy in hopping)
            mcount=sum(max(abs(f[0]+s*dx),abs(f[1]+s*dy))>3
                       for dx,dy in shifts for s in (-1,1))
            lower=diagonal-1400*hcount-625*mcount
            if lower<best[0]:best=(int(lower),f,bits)
    assert best[0]==28330 and best[1]==(-4,2)
    # Any |m|>=10 has at least one chord flux squared >=100.
    # Minimal stagger contribution -1.5, magnetic +1.875.
    # Worst row abs <=12*.7+6*.3125=10.275; lower >=22.1.
    tail_scaled=640*100-3000+3750-1400*12-625*6
    assert tail_scaled==44200 and tail_scaled>best[0]
    # Explicit P-Q interface; entries rescaled by 80 are integers:
    # hopping +/-56, Wilson +/-25. This permits EXACT integer Gram bounds.
    inside=list(itertools.product(range(-3,4),repeat=2))
    outer=[f for f in itertools.product(range(-4,5),repeat=2)
           if max(map(abs,f))==4]
    lookup={f:i for i,f in enumerate(outer)}
    rows=[];cols=[];vals=[]
    ni=len(inside);nq=len(outer)
    for index,bits in enumerate(fock):
        o=occupations[index]
        hops=[]
        for e,(a,b) in enumerate(p["p_ed"]):
            if e not in chord or o[a]==o[b]:continue
            dst=bits^(1<<a)^(1<<b)
            sign=(-1)**sum((bits>>j)&1 for j in range(min(a,b)+1,max(a,b)))
            hops.append((fi[dst],chord[e],1 if o[a] else -1,sign))
        for k,f in enumerate(inside):
            r=index*ni+k
            for dest,e,dr,sign in hops:
                z=list(f);z[e]-=dr
                t=lookup.get(tuple(z))
                if t is not None:
                    rows.append(r);cols.append(dest*nq+t);vals.append(-56*sign)
            for dx,dy in shifts:
                for s in (-1,1):
                    t=lookup.get((f[0]+s*dx,f[1]+s*dy))
                    if t is not None:
                        rows.append(r);cols.append(index*nq+t);vals.append(-25)
    Ki=coo_matrix((np.array(vals,dtype=np.int64),(rows,cols)),
                  shape=(len(fock)*ni,len(fock)*nq)).tocsr()
    assert Ki.shape==(22638,14784) and Ki.nnz==28476
    gram=Ki@Ki.T
    gram_row_sum=np.asarray(abs(gram).sum(axis=1)).ravel()
    numerator=int(gram_row_sum.max())
    assert numerator==12822
    operator_upper=numerator/6400
    Q_lower=best[0]/2000
    assert Q_lower==14.165 and operator_upper==2.0034375
    E0=-3.1898474481159673
    gap=1.0643124872613563
    improved_gap=gap-operator_upper/Q_lower
    assert .922<improved_gap<.924
    return {
      "status":"PASS_TOE72_INTEGER_INTERFACE_AND_GERSHGORIN",
      "native_sites_links_fermions":[11,12,5],
      "P_dimension":22638,"first_Q_shell_dimension":14784,
      "Q_omitted_diagonal_minus_allowed_rowsum_min_exact_units_2000":best[0],
      "Q_min_location_flux":list(best[1]),
      "Q_min_location_fermion_bitmask":best[2],
      "rigorous_far_flux_tail_lower_units_2000":tail_scaled,
      "rigorous_Q_spectral_lower":Q_lower,
      "integer_interface_nonzeros":int(Ki.nnz),
      "integer_interface_scale":80,
      "exact_KKT_max_abs_row_sum_integer":numerator,
      "rigorous_K_norm_squared_upper":operator_upper,
      "P_ground_numeric":E0,"P_gap_numeric":gap,
      "conditional_full_rotor_gap_lower":improved_gap,
      "mathematical_scope":"Exact finite matrix Gram/Gershgorin bounds for infinite omitted flux complement; Schur min-max gap deduction conditional on exact ordering/enclosures for finite 22638x22638 P eigenvalues.",
      "not_claimed":"Not a certified unbounded-rotor gap or 80-site field-theory gap."
    }

if __name__=="__main__":
    o=certificate()
    (ROOT/"data/w33_20261014_toe72_gauge_gram_bound.json").write_text(json.dumps(o,indent=2)+"\n")
    print(o["status"],o["conditional_full_rotor_gap_lower"])
