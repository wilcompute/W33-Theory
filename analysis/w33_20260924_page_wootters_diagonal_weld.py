#!/usr/bin/env python3
from __future__ import annotations
import itertools, json, math
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20260924_page_wootters_diagonal_weld.json"
E8_JSON=ROOT/"data/w33_diagonal_weld_e8_lie_generation.json"
CUBIC_JSON=ROOT/"data/w33_e6_cubic_diagonal_phase_weld.json"

omega=np.exp(2j*np.pi/3)
TOL=1e-9

FORMS={
    "center":(1,0),
    "external":(0,1),
    "plus":(1,1),
    "minus":(1,2),
}

def lin(form,c,p):
    a,b=form
    return (a*c+b*p)%3

def projective(v):
    a,b=v
    if a:
        s=1 if a==1 else 2
    else:
        s=1 if b==1 else 2
    return ((s*a)%3,(s*b)%3)
def shift():
    X=np.zeros((3,3),dtype=complex)
    for t in range(3):
        X[(t+1)%3,t]=1
    return X

def basis(i,n=3):
    v=np.zeros(n,dtype=complex)
    v[i]=1
    return v

def history_state(r,orientation):
    # orientation +1: U^t; orientation -1: U^{-t}.
    out=np.zeros(9,dtype=complex)
    for t in range(3):
        amp=omega**((orientation*r*t)%3)/math.sqrt(3)
        out+=amp*np.kron(basis(t),basis(r))
    return out

def phase_support(state):
    # Clock X-eigenbasis |p> = sum_t omega^(-p t)|t>/sqrt(3).
    rows=[]
    for p in range(3):
        clock=sum(
            (omega**((-p*t)%3))*basis(t)
            for t in range(3)
        )/math.sqrt(3)
        for c in range(3):
            amp=np.vdot(np.kron(clock,basis(c)),state)
            if abs(amp)>TOL:
                rows.append((p,c,amp))
    return rows
def main():
    # Four controls are exactly P1(F3).
    dirs={projective(v) for v in FORMS.values()}
    assert len(dirs)==4
    all_dirs={
        projective(v)
        for v in itertools.product(range(3),repeat=2)
        if v!=(0,0)
    }
    assert dirs==all_dirs

    zeros={}
    for name,f in FORMS.items():
        Z={(c,p) for c,p in itertools.product(range(3),repeat=2) if lin(f,c,p)==0}
        assert len(Z)==3
        zeros[name]=sorted(Z)

    assert zeros["plus"]==[(0,0),(1,2),(2,1)]
    assert zeros["minus"]==[(0,0),(1,1),(2,2)]
    assert zeros["center"]==[(0,0),(0,1),(0,2)]
    assert zeros["external"]==[(0,0),(1,0),(2,0)]

    # Page-Wootters stationarity and Fourier support.
    X=shift()
    U=np.diag([1,omega,omega**2])
    forward=[]
    reverse=[]
    for r in range(3):
        hp=history_state(r,+1)
        hm=history_state(r,-1)
        assert np.linalg.norm(np.kron(X,U)@hp-hp)<TOL
        assert np.linalg.norm(np.kron(X,np.linalg.matrix_power(U,2))@hm-hm)<TOL
        sp=phase_support(hp)
        sm=phase_support(hm)
        assert len(sp)==len(sm)==1
        p,c,_=sp[0]
        q,d,_=sm[0]
        assert c==d==r
        assert (c+p)%3==0
        assert (c-q)%3==0
        forward.append((p,c))
        reverse.append((q,d))
    assert sorted(forward)==zeros["plus"]
    assert sorted(reverse)==zeros["minus"]

    # Generic history states span the same 3D invariant sectors.
    Dplus=np.diag([
        omega**((c+p)%3)
        for p in range(3) for c in range(3)
    ])
    Dminus=np.diag([
        omega**((c-p)%3)
        for p in range(3) for c in range(3)
    ])
    plus_fixed=sum(abs(z-1)<TOL for z in np.diag(Dplus))
    minus_fixed=sum(abs(z-1)<TOL for z in np.diag(Dminus))
    assert plus_fixed==minus_fixed==3

    e8=json.loads(E8_JSON.read_text(encoding="utf-8"))
    cubic=json.loads(CUBIC_JSON.read_text(encoding="utf-8"))
    grid=e8["dimension_grid_mod_103"]
    # Exact closure law: factor-axis controls only ->24; a correlated graph
    # direction on either side -> full E8.
    for a,b in itertools.product(FORMS,repeat=2):
        diagonal=(a in {"plus","minus"} or b in {"plus","minus"})
        expected=248 if diagonal else 24
        assert grid[a][b]==expected

    rank=cubic["rank_and_alignment"]
    assert rank["center"]["quotient_projection_rank"]==36
    assert rank["external"]["quotient_projection_rank"]==36
    assert rank["center_plus_external"]["quotient_projection_rank"]==54
    assert rank["center_minus_external"]["quotient_projection_rank"]==54

    out={
      "schema":"w33.20260924.page_wootters_diagonal_weld.v1",
      "status":"PASS_PAGE_WOOTTERS_PHASE_MATCHING_IS_THE_DIAGONAL_E8_WELD",
      "phase_plane":{
        "carrier":"F3^2 with coordinates (c,p)",
        "projective_control_space":"P1(F3)",
        "controls":{k:list(v) for k,v in FORMS.items()},
        "zero_sets":{k:[list(x) for x in v] for k,v in zeros.items()},
        "factor_axes":["c=0","p=0"],
        "correlated_graphs":["c+p=0 (p=-c)","c-p=0 (p=c)"],
      },
      "page_wootters":{
        "forward_constraint":"(X_clock tensor U)|Psi_+>=|Psi_+>",
        "reverse_constraint":"(X_clock tensor U^-1)|Psi_->=|Psi_->",
        "clock_phase_basis":"X|p>=omega^p|p>",
        "forward_phase_support":[list(x) for x in sorted(forward)],
        "reverse_phase_support":[list(x) for x in sorted(reverse)],
        "forward_equals_plus_zero_set":True,
        "reverse_equals_minus_zero_set":True,
        "invariant_dimension_each":3,
      },
      "existing_E8_switch_reinterpreted":{
        "source":str(E8_JSON.relative_to(ROOT)).replace("\\","/"),
        "pure_axis_pair_dimension":24,
        "any_correlated_graph_side_dimension":248,
        "all_16_entries_match_rule":True,
        "matched_plus_minus_orientation_required":False,
      },
      "cubic_quotient":{
        "source":str(CUBIC_JSON.relative_to(ROOT)).replace("\\","/"),
        "axis_projection_rank":36,
        "diagonal_projection_rank":54,
        "full_retyped_dimension":54,
      },
      "theorem":(
        "The four H27-center/external-qutrit backgrounds c, p, c+p, c-p are "
        "exactly the four projective linear directions of F3^2. Their kernels "
        "split into two factor axes and two graph subgroups p=+/-c. For an "
        "order-three qutrit evolution, the Page-Wootters stationarity constraints "
        "X_C tensor U^(+/-1) become precisely these two graph subgroups in the "
        "clock-phase basis. The previously certified E8 closure table is exactly "
        "controlled by this distinction: pairs using only factor-axis backgrounds "
        "close to 24 dimensions, while a graph-correlated background on either "
        "side generates all 248 dimensions. Thus the diagonal weld has an exact "
        "relational-clock interpretation, not merely a suggestive phase name."
      ),
      "boundary":(
        "This proves equality of finite phase constraints and the existing Lie-"
        "generation switch. It does not derive a Wheeler-DeWitt Hamiltonian, "
        "physical time evolution, vacuum selection, or continuum clock dynamics."
      ),
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({
      "status":out["status"],
      "forward":out["page_wootters"]["forward_phase_support"],
      "reverse":out["page_wootters"]["reverse_phase_support"],
      "closure_rule":out["existing_E8_switch_reinterpreted"],
    },indent=2,sort_keys=True))

if __name__=="__main__":
    main()
